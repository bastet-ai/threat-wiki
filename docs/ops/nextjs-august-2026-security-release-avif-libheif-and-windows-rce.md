# Next.js August 2026 security release: two unauthenticated RCEs (libheif/AVIF heap overflow + Windows path traversal)

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

## GHSA-2xp9-vwfh-vxw4 / GHSA-g89c-p67h-r497 — AVIF / libheif heap buffer overflow (no CVE)
Next.js uses the **sharp** image-processing package for image optimization, and sharp relies on the **libheif** C library to parse AVIF files. The underlying flaw, disclosed by the libheif maintainers as **GHSA-g89c-p67h-r497**, is a **heap buffer overflow in the library's image-scaling code** (`HeifPixelImage::scale_nearest_neighbor()`):

- A crafted HEIC/HEIF/AVIF file with **nested identity-derivation (`iden`) and auxiliary (`auxl`) item references** causes libheif to build a decoded image with **two Alpha-plane entries at different bit depths**.
- The scaler allocates a destination buffer sized for the **first (8-bit) Alpha entry** but then writes **16-bit sample values from the second entry** into the same buffer, overwriting approximately **16,384 bytes past the allocation boundary**.
- The overflow size and written values are **attacker-controlled** via the ISOBMFF container and HEVC bitstream content. Any application calling `heif_decode_image()` is affected; no special API options are required.
- This is a chain of four individually benign behaviors: `transfer_channel_from_image_as()` accepts a duplicate destination channel (an open `// TODO` to reject it), `find_storage_for_channel()` returns only the first match, the scaling path sizes the buffer for one entry, and then writes the other.
- **All libheif versions through v1.23.1 are affected** (as of August 27, 2026 the upstream **v1.23.2 had not been published**, per THN checking the libheif GitHub releases page).

**Affected Next.js ranges (GHSA-2xp9-vwfh-vxw4):** `next` `>= 10.0.0 < 15.5.24` and `< 16.3.3` (all 16.x through 16.3.2). The Vercel advisory reports the flaw as **Critical** with **CVSS v4 9.5**.

**Exposure gate:** Next.js only performs **AVIF optimization when a site explicitly adds `image/avif` to the `formats` configuration** in `next.config.js`. Deployments without that configuration are not exposed to this specific flaw.

**Researcher claims (not independently corroborated):** rootxharsh (Finder) and KarimPwnz (Coordinator) released a **full Python proof-of-concept** reproducing the heap corruption under an AddressSanitizer build and stated "we were able to get RCE using this on multiple applications." The patched Next.js releases **turn off AVIF optimization entirely** until the upstream libheif fix propagates.

## GHSA-p293-qw3h-jr36 / CVE-2026-75604 — Windows path traversal → unauth RCE
A vulnerability in Next.js applications that use **both the Pages Router and the App Router without Cache Components** can lead to **remote code execution when the server runs on a Windows filesystem**.

- **Affected:** `next` `>= 13.4 < 15.5.24` and `>= 16.0 < 16.3.3`.
- **Severity:** Critical, CVSS 3.1 **9.0** (`AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H`), **CVE-2026-75604**.
- **No known workaround** for affected Windows-hosted applications. Vercel's advisory: "You should upgrade immediately if your server is hosted on Windows."
- The attack mechanism was **not disclosed** in the advisory. Vercel's changelog credited researchers **evolutionstorm** and **B0RI** for the responsible disclosure of the Windows vulnerability.

## Why it matters
- **Blast radius:** Next.js is one of the most widely deployed React frameworks. Two *unauthenticated* RCE primitives in a single framework release is a patch-now event for self-hosted deployments — especially Windows-hosted ones (the path-traversal RCE has no workaround) and any site that enabled `image/avif` optimization.
- **Upstream-library propagation gap:** the AVIF flaw lives in a transitive C library (libheif, pulled via sharp). Vercel moved the release forward by one day after discovering "an additional critical-severity vulnerability in one of its upstream dependencies," and stopped AVIF optimization in Next.js until the upstream patch propagates — a durable reminder that **image-parsing native dependencies are a standing unauthenticated-RCE surface** and that a framework patch can be a stopgap, not a terminal fix.
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

## Related pages
- [GitHub Security Advisories August 29, 2026 (RCE/auth-bypass/sandbox batch)](github-advisories-argocd-mcp-sigma-forms-omnivore-skyvern-bookstack-august-29-2026.md)
- [CISA KEV August 27, 2026 additions (ownCloud / Linux kernel / JFrog Artifactory)](cisa-kev-owncloud-linux-artifactory-august-27-2026.md)

## Sources
- The Hacker News, "Next.js Patches Critical AVIF and Windows Flaws Enabling Unauthenticated RCE" (August 27, 2026): https://thehackernews.com/2026/08/nextjs-patches-critical-avif-and.html
- Vercel changelog, "Next.js August 2026 Security Release": https://vercel.com/changelog/nextjs-august-2026-security-release
- Next.js blog, "August 2026 Security Release": https://nextjs.org/blog/august-2026-security-release
- GitHub Security Advisory: [GHSA-2xp9-vwfh-vxw4 — Next.js unauth RCE via AVIF image optimization](https://github.com/vercel/next.js/security/advisories/GHSA-2xp9-vwfh-vxw4)
- GitHub Security Advisory: [GHSA-p293-qw3h-jr36 — Next.js unauth RCE on Windows-hosted servers (CVE-2026-75604)](https://github.com/vercel/next.js/security/advisories/GHSA-p293-qw3h-jr36)
- GitHub Security Advisory: [GHSA-g89c-p67h-r497 — libheif heap buffer overflow in scale_nearest_neighbor()](https://github.com/strukturag/libheif/security/advisories/GHSA-g89c-p67h-r497)
- Vercel Next.js security release program: https://nextjs.org/blog/next-security-release-program
