# Next.js August 2026 security release

## Summary
On **August 25, 2026**, Vercel published a Next.js security release (second under its formal monthly security program, first released July 21, 2026) fixing **two critical-severity vulnerabilities, both allowing unauthenticated remote code execution**:

| Advisory | Product | Class | Severity | Fix |
|---|---|---|---|---|
| **GHSA-2xp9-vwfh-vxw4** (upstream **GHSA-g89c-p67h-r497** libheif) | `next` (npm) | **Unauth RCE via crafted AVIF** in Image Optimization API | **Critical** (libheif CVSS v3.1 9.8) | Next.js **15.5.24** (Maintenance LTS) / **16.3.3** (Active LTS); AVIF optimization disabled until the libheif fix propagates |
| **GHSA-p293-qw3h-jr36 / CVE-2026-75604** | `next` (npm) | **Unauth RCE on Windows-hosted servers** via path traversal | **Critical** (CVSS 3.1 **9.0**, `AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H`) | Next.js **15.5.24** / **16.3.3** |

**No exploitation of either was reported as of August 27, 2026.** Applications hosted on Vercel are protected from both and require no upgrade.

## Tags
- ops
- Next.js
- Vercel
- unauthenticated RCE
- path traversal
- heap buffer overflow
- AVIF
- HEIF
- HEIC
- libheif
- sharp
- image optimization
- Windows
- Windows filesystem
- GHSA-2xp9-vwfh-vxw4
- GHSA-p293-qw3h-jr36
- GHSA-g89c-p67h-r497
- CVE-2026-75604
- CVSS 9.0
- monthly security release
- upstream dependency
- unpatched transitive library
- npm

## GHSA-2xp9-vwfh-vxw4 / GHSA-g89c-p67h-r497, AVIF / libheif heap buffer overflow (no CVE)
Next.js uses the **sharp** image-processing package for image optimization, and sharp relies on the **libheif** C library to parse AVIF files. The underlying flaw, disclosed by the libheif maintainers as **GHSA-g89c-p67h-r497**, is a **heap buffer overflow in the library's image-scaling code** (`HeifPixelImage::scale_nearest_neighbor()`):

- A crafted HEIC/HEIF/AVIF file with **nested identity-derivation (`iden`) and auxiliary (`auxl`) item references** causes libheif to build a decoded image with **two Alpha-plane entries at different bit depths**.
- The scaler allocates a destination buffer sized for the **first (8-bit) Alpha entry** but then writes **16-bit sample values from the second entry** into the same buffer, overwriting approximately **16,384 bytes past the allocation boundary**.
- The overflow size and written values are **attacker-controlled** via the ISOBMFF container and HEVC bitstream content. Any application calling `heif_decode_image()` is affected; no special API options are required.
- This is a chain of four individually benign behaviors: `transfer_channel_from_image_as()` accepts a duplicate destination channel (an open `// TODO` to reject it), `find_storage_for_channel()` returns only the first match, the scaling path sizes the buffer for one entry, and then writes the other.
- **All libheif versions through v1.23.1 are affected** (as of August 27, 2026 the upstream **v1.23.2 had not been published**, per THN checking the libheif GitHub releases page).

**Affected Next.js ranges (GHSA-2xp9-vwfh-vxw4):** `next` `>= 10.0.0 < 15.5.24` and `< 16.3.3` (all 16.x through 16.3.2). The Vercel advisory reports the flaw as **Critical** with **CVSS v4 9.5**.

**Exposure gate:** Next.js only performs **AVIF optimization when a site explicitly adds `image/avif` to the `formats` configuration** in `next.config.js`. Deployments without that configuration are not exposed to this specific flaw.

**Researcher claims (not independently corroborated):** rootxharsh (Finder) and KarimPwnz (Coordinator) released a **full Python proof-of-concept** reproducing the heap corruption under an AddressSanitizer build and stated "we were able to get RCE using this on multiple applications." The patched Next.js releases **turn off AVIF optimization entirely** until the upstream libheif fix propagates.

## GHSA-p293-qw3h-jr36 / CVE-2026-75604, Windows path traversal → unauth RCE
A vulnerability in Next.js applications that use **both the Pages Router and the App Router without Cache Components** can lead to **remote code execution when the server runs on a Windows filesystem**.

- **Affected:** `next` `>= 13.4 < 15.5.24` and `>= 16.0 < 16.3.3`.
- **Severity:** Critical, CVSS 3.1 **9.0** (`AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H`), **CVE-2026-75604**.
- **No known workaround** for affected Windows-hosted applications. Vercel's advisory: "You should upgrade immediately if your server is hosted on Windows."
- The attack mechanism was **not disclosed** in the advisory. Vercel's changelog credited researchers **evolutionstorm** and **B0RI** for the responsible disclosure of the Windows vulnerability.
- **September 14, 2026 update, mechanism disclosed (OX Security technical analysis):** Next.js builds **incremental-cache file paths** by joining a route-derived cache key onto the server build directory **without verifying the result stays inside it**. Dynamic route segments are escaped for the router's own delimiters (`/`, `#`, `?`), their percent-encoded forms, and the percent-encoded backslash, **but not the literal backslash character**. Windows treats `\` as a path separator while POSIX treats it as a valid filename character, so a catch-all route segment containing traversal sequences **escapes the cache directory only on Windows hosts**. The incremental cache then **reads and writes that escaped path**, giving an unauthenticated attacker **disclosure of files under the build directory, including the server reference manifest containing the Server Actions encryption key**, and **a write of attacker-influenced rendered output to a location of their choosing**. Applications using Pages router, or App router without Cache Components, are affected. (OX published this alongside Netty CVE-2026-75595 and GitPython CVE-2026-78676 in a four-CVE "same trust issue" cluster, see [Four critical trust-failure CVEs](../tools/four-critical-trust-failure-cves-netty-sni-fallback-gitpython-hookspath-ox-september-2026.md).)

## Why it matters
- **Blast radius:** Next.js is one of the most widely deployed React frameworks. Two *unauthenticated* RCE primitives in a single framework release is a patch-now event for self-hosted deployments, especially Windows-hosted ones (the path-traversal RCE has no workaround) and any site that enabled `image/avif` optimization.
- **Upstream-library propagation gap:** the AVIF flaw lives in a transitive C library (libheif, pulled via sharp). Vercel moved the release forward by one day after discovering "an additional critical-severity vulnerability in one of its upstream dependencies," and stopped AVIF optimization in Next.js until the upstream patch propagates, a durable reminder that **image-parsing native dependencies are a standing unauthenticated-RCE surface** and that a framework patch can be a stopgap, not a terminal fix.
- **Vercel monthly-security-program context:** the August release is the second under Vercel's formal monthly program (announced July 13, 2026, which noted rising vulnerability-research volume "driven by LLM-assisted discovery"). The first (July 21, 2026) fixed nine flaws in Next.js 16.2.11 / 15.5.21. Next.js has a run of criticals over the past two years, including the March 2025 middleware-bypass and the December 2025 React2Shell deserialization flaw (CVSS 10.0, actively exploited within hours of disclosure).

## Defender priorities
1. **Upgrade Next.js self-hosted apps to 15.5.24 (Maintenance LTS) or 16.3.3 (Active LTS)** (`npm install next@15.5.24` / `npm install next@16.3.3`). Prioritize **Windows-hosted** servers (no workaround for CVE-2026-75604) and any site with `image/avif` in `next.config.js` `formats` (AVIF/libheif exposure).
2. **Vercel-hosted apps:** already protected from both; no upgrade required (Vercel changelog, Aug 25, 2026).
3. **Image-processing inventory:** treat `sharp` / `libheif` (and any native image/codec parser) as a standing unauthenticated-RCE vector; track the **libheif v1.23.2** publication, since the Next.js AVIF mitigation is only "AVIF optimization off" until that upstream fix ships.
4. **Treat as unattributed / no-exploitation:** no exploitation of either August flaw was reported as of August 27, 2026. The researcher "multiple applications RCE" claim for the AVIF flaw is not independently corroborated. Do not assume a campaign; correlate to your own exposure model.
5. **Watch for exploitation telemetry** on the Windows path-traversal RCE (unauthenticated, no workaround) and for the libheif CVE assignment (currently no CVE on the AVIF advisory).

## Assessment limits
- GHSA-2xp9-vwfh-vxw4 (AVIF) is **Critical with no CVE** at publication; the CVSS figure (v4 9.5) is from the Vercel advisory/THN, while the upstream libheif GHSA-g89c-p67h-r497 carries CVSS 3.1 9.8.
- The libheif v1.23.2 patch had not been published as of August 27, 2026; Next.js's stopgap is disabling AVIF optimization, not an in-tree fix.
- CVE-2026-75604 (Windows) has a CVSS 3.1 9.0 vector; its attack mechanism is undisclosed.
- No in-the-wild exploitation of either August vulnerability was reported as of August 27, 2026 (THN reached out to Vercel; no response by publication).

### September 19, 2026 follow-up: the AVIF advisory now has a CVE

**GHSA-g89c-p67h-r497 was assigned CVE-2026-84383** (NVD publication 2026-09-18 16:17 UTC, the same day the Hacktron "HEIF Heist" story ran, and in a same-minute batch with CVE-2026-84384 / -84446 / -84447 / -84450, all libheif, all backfilling previously un-CVE'd GHSAs). The "Critical with no CVE" framing on this page is historical: at August publication there was no CVE, one shipped roughly three weeks later, only after the exploitation-adjacent story made the gap visible. Newest libheif advisories (Sep 1/6 security-release set + GHSA-q492-cfcm-895h, Sep 18, OpenJPEG pre-decode gate) still carry no CVE. See the [Hacktron HEIF Heist page's September 19 follow-up](hacktron-heif-heist-openai-discourse-breach-opus5-september-2026.md#september-19-follow-up-the-un-cved-advisory-behind-nextjs-finally-got-a-cve-on-heif-heist-day).

## <a id="november-11-249th-rsc-rce-late-arrival"></a>November 11, 249th sweep follow-up: the React Server Components RCE reached the global advisory DB twenty-seven days late

On **November 10 at 22:44:12Z**, `GHSA-xqc2-xf4c-x3h3` ("Unauthenticated Remote Code Execution in React Server Components", CVSS v4 **9.5**, no CVE assigned) appeared in the GitHub **global** advisories database (`api.github.com/advisories`, reviewed lane). The flaw itself is older news to anyone reading React's own repository: the React team published the advisory **October 14, 2026**, and the fixed rungs shipped the same day — this wiki verified the registry `time[]` directly: `react-server-dom-webpack` `19.3.1` `2026-10-14T16:49:15.095Z`, `19.2.9` `16:49:28Z`, `19.0.9` `16:49:54Z`, `19.1.10` `16:55:55Z`. The Next.js twin, `GHSA-673q-mjm6-r5xr` (`next 16.0.0`–`16.4.0` → fixed `16.4.1`, published `2026-10-14T17:43:55.246Z`), entered the global DB **October 22**.

The affected surface is not small: this wiki measured `react-server-dom-webpack` at **3,716,639** and `next` at **92,077,869** downloads in the Nov-4→10 window. The trigger is narrow (a Flight-protocol framing desync when a response carries multiple typed arrays plus an attacker-controlled value; in Next.js that means App Router + Cache Components with a `use cache` function returning typed arrays), no exploitation in the wild was reported as of this read, and there is no workaround — upgrade `next` to `16.4.1`+ (bundling its own copy of the RSC runtime, so bumping `react` alone fixes nothing) or the three `react-server-dom-*` packages to `19.0.9`/`19.1.10`/`19.2.9`/`19.3.1`.

**The durable capture is feed lag, not the flaw.** Three facts stack into the defender lesson: (1) the advisory carries **no CVE**, so CVE-keyed tooling never saw it; (2) it sat in the repository-native advisory lane for **27 days** before the global DB mirrored it, so Dependabot/`npm audit`-class consumers were quiet for a month after the fix shipped; (3) when this wiki's own sweep first saw these rows (the 248th's silent-parameter-drop specimen), they were **junk output from a dropped filter parameter** and went unread = a malformed request can still be the only copy of important news that reaches you. Rules taken forward: read advisory IDs directly on security-critical frameworks, never only via feed mirrors; verify fixed-rung existence in the registry `time[]` (this wiki did, minutes-of-precision publish stamps survive the feed lag); and read the rows even when you believe the query asked for nothing.

## Related pages
- [ALGAMIL7X stream, 249th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-ninth-sweep) (the late-arrival capture + both-heads law)
- [Sep 18, 2026 follow-up: Hacktron "HEIF Heist", libheif bug in OpenAI's Discourse forum chained to employee ChatGPT/Codex account takeover and internal-repo access (fix shipped upstream unflagged, no CVE)](hacktron-heif-heist-openai-discourse-breach-opus5-september-2026.md)
- [GitHub Security Advisories August 29, 2026 (RCE/auth-bypass/sandbox batch)](github-advisories-argocd-mcp-sigma-forms-omnivore-skyvern-bookstack-august-29-2026.md)
- [CISA KEV August 27, 2026 additions (ownCloud / Linux kernel / JFrog Artifactory)](cisa-kev-owncloud-linux-artifactory-august-27-2026.md)

## Sources
- The Hacker News, "Next.js Patches Critical AVIF and Windows Flaws Enabling Unauthenticated RCE" (August 27, 2026): https://thehackernews.com/2026/08/nextjs-patches-critical-avif-and.html
- Vercel changelog, "Next.js August 2026 Security Release": https://vercel.com/changelog/nextjs-august-2026-security-release
- Next.js blog, "August 2026 Security Release": https://nextjs.org/blog/august-2026-security-release
- GitHub Security Advisory: [GHSA-2xp9-vwfh-vxw4, Next.js unauth RCE via AVIF image optimization](https://github.com/vercel/next.js/security/advisories/GHSA-2xp9-vwfh-vxw4)
- GitHub Security Advisory: [GHSA-p293-qw3h-jr36, Next.js unauth RCE on Windows-hosted servers (CVE-2026-75604)](https://github.com/vercel/next.js/security/advisories/GHSA-p293-qw3h-jr36)
- GitHub Security Advisory: [GHSA-g89c-p67h-r497, libheif heap buffer overflow in scale_nearest_neighbor()](https://github.com/strukturag/libheif/security/advisories/GHSA-g89c-p67h-r497)
- Vercel Next.js security release program: https://nextjs.org/blog/next-security-release-program
- GitHub Advisory GHSA-xqc2-xf4c-x3h3 (React Server Components unauth RCE, global-DB entry Nov 10 22:44:12Z): https://github.com/advisories/GHSA-xqc2-xf4c-x3h3
- GitHub Advisory GHSA-673q-mjm6-r5xr (Next.js twin, global-DB entry Oct 22): https://github.com/advisories/GHSA-673q-mjm6-r5xr
