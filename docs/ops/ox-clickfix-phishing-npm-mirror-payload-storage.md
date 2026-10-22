# OX Security: ClickFix phishing pages hidden in 24 npm packages, using registry mirrors as payload storage

## Summary
OX Security (August 25, 2026) identified a **fake Cloudflare CAPTCHA phishing campaign distributed through 24 malicious npm packages** sharing the exact same HTML page. The packages do not execute code on install — the actor's use of npm is to exploit registry **mirrors (unpkg, npmmirror, yarn, tencent, and others) as free, trusted-domain payload storage**: mirrors serve package files (including bare `index.html`) directly on their own domains, so anyone opening a mirror URL sees a fully rendered phishing page on a reputable host. The page presents a fake Cloudflare verification, then redirects through obfuscated JavaScript to attacker-controlled infrastructure. Packages typically reach 50–300 weekly downloads before removal, but mirror copies persist after registry takedowns.

## Tags
- ops
- operations
- OX Security
- npm
- npm mirrors
- unpkg
- npmmirror
- ClickFix
- fake CAPTCHA
- fake Cloudflare
- phishing
- payload storage
- Microsoft typosquat
- keyval.org
- trusted-domain abuse
- supply chain

## Campaign mechanics
- Each package's content is a single **fake Cloudflare verification HTML page** with obfuscated JavaScript.
- **First wave:** the JS redirected to the typosquatted Microsoft domain `login[.]microsofte[.]live` (now blacklisted).
- **Current wave ("keyval new logic"):** the JS fetches an encrypted value from the legitimate key-value store **`api.keyval.org`**, decrypts it, and browses to the result. OX observed the value currently resolving to the legitimate ChatGPT website, but the actor can point it at **ClickFix pages or any phishing domain** on demand — the npm package is the persistent, trusted-domain front end.
- Distribution: links to the mirror-hosted pages are shared via social channels; the packages exist to keep the phishing HTML alive on trusted domains even after removal from npm.

## Indicators
- **IOCs (OX):** `login[.]microsofte[.]live`, `api.keyval.org` (legitimate service abused for storage; not itself malicious).
- **Example mirror URL:** `https://unpkg[.]com/ndmxchdjxn2@1.0.0/index.html` (rendered fake-CAPTCHA page).
- **Affected packages (24, published 2026-08-04 → 2026-08-24 UTC):** `bgzxcuite2`, `prezdentkxheiw`, `egair0810`, `mnteckets`, `airdzticket`, `egypt0811`, `passport811`, `vxhjkseuiaqkb`, `ndmushdkeqe`, `ndmxchdjxn2`, `ndmfguyhoxc3`, `mjsdqwocvn`, `m2fcsfyjkuxb`, `m3fdfocdoewn`, `@worrisome/reutil`, `testdgdbcsd`, `tesgfvbncsdbcv`, `mndsxcusiwlk1`, `mn2adskhweox`, `mn3sadkoiewu`, `mn4xcouzvhus`, `mbxcnsuwgs1`, `skxcmwuncbg2`, `mobiwaefhxc3` — "Microsoft Typosquat" family (random-string names, 7 taken down by August 11) plus "keyval new logic" family (8 live at publication).

## Defender heuristics
1. **Treat npm mirror domains (unpkg, npmmirror, yarn, tencent, etc.) as potential phishing hosts** when URLs are not part of normal package-download workflows; add mirror URL shapes to phishing detection and URL-reputation pipelines.
2. **Check proxy/DNS logs for direct `.html` requests** (especially `index.html`) to mirror domains — legitimate tooling downloads package tarballs, not bare HTML pages.
3. **Hunt the fake-CAPTCHA primitive** in email/browser telemetry: a page claiming browser security verification that offers a "run this command" clipboard action is the ClickFix shape (see the macOS ClickFix fingerprinting-gate page and the ACR Stealer page).
4. **Abuse of trusted key-value/short-link services** (`api.keyval.org` encrypted-value redirection) should be treated as an indicator of phishing redirect infrastructure; monitor outbound resolution of such lookups from user browsers.
5. **Assume persistence after takedown:** mirror copies of removed packages survive; hunt for mirror-hosted `index.html` URLs in social links and phishing reports even when the npm package no longer exists.

## Same-day updates

### <a id="october-21-scope-re-arm-and-enforcement-closure"></a>October 21, 2026: the scope RE-ARMED under its own advisory — then the lane closed (this wiki forensics, one-hundred-and-sixty-seventh sweep)

The campaign lane this page was written about **came back to life today, on a name that had carried a public OSV record for ≈56 days.** Captured live by this wiki at ~21:2x–21:5x UTC Oct 21:

- **`@worrisome/reutil`** — in OX's original 24-name list, `MAL-2026-15604` since **Aug-26**, yet NEVER holder-seized: the name stayed installable with `latest` serving (downloads `162`/wk in the Oct 12–18 window measured by this wiki). Registry `time` block (read directly): today at **`02:12:50Z` the publisher shipped a NEW version `1.0.5`** (prior versions `1.0.0`–`1.0.3` all date Aug-14) = **a re-arm commit landed on an already-advised, still-installable name ≈19 h before enforcement noticed.**
- **`@worrisome/aaaa`** — NOT in OX's published 24-name list; `1.0.0` dates **Sep-8** = scope expansion AFTER the campaign post. New `1.0.1` shipped today **`02:15:43Z`** — three minutes after the sibling's re-arm. Downloads `4`/wk.
- **Enforcement, one second wide:** holder-seizure doc re-creation `21:19:43.7`/`21:19:52.4Z`, holder versions `0.0.0-stage` + `0.0.1-security` through `21:20:48Z`, GHSA pair SAME SECOND `21:20:33Z` (`GHSA-fxf3-w84v-3v6g` aaaa, `GHSA-4f5p-mp5p-863f` reutil, `>= 0` blankets), OSV `MAL-2026-18125` minted for aaaa with **alias-at-birth**, and `MAL-2026-15604` **forward-joined** to its new GHSA at the `21:30:24Z` importer tick ≈10 min after the seizure.
- **Artifact state:** BOTH re-arm tarballs (`1.0.5`, `1.0.1`) are `404` on the registry and jsDelivr at check = the new-build content is unknowable; jsDelivr still serves the OLD `reutil@1.0.3` = CDN survivor class. The VERSION EVENT is what the registry `time` block proves; the payload is recorded-not-executed.
- **Lane closure:** the seven `keyval new logic` names not in tonight's pair (`mndsxcusiwlk1`, `mn2adskhweox`, `mn3sadkoiewu`, `mn4xcouzvhus`, `mbxcnsuwgs1`, `skxcmwuncbg2`, `mobiwaefhxc3`) re-read holder-seized, `modified` frozen at the `02:42–02:43Z` Sept-23 wave that **skipped reutil** — tonight's pair finishes what that wave started, `≈58 d` after OX's post.

**DURABLE (defender rule):** an OSV record is a label, not a lock. Advised package names can be — and here **were** — re-weaponized with fresh versions while the advisory sits public and the registry keeps serving `latest`. Consumer-facing detection must key on **registry VERSION events for names that already carry advisories**, not on advisory presence alone; the bbmarker law (advisory ≠ enforcement ≠ alert) now has its first RE-ARM counter-instance: the unadvised-lane survivors are the re-arm candidates. Cross-stream ledger: [one-hundred-and-sixty-seventh sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-21-one-hundred-and-sixty-seventh-sweep).

### <a id="october-22-scope-probe-trap-and-survivor-end-candidate"></a>October 22, 2026: the jsDelivr `reutil@1.0.3` survivor reads `404` — survivor-END candidate at seizure+`≈40 h`, caught behind a scoped-name probe trap (this wiki forensics, one-hundred-and-seventy-fifth sweep)

The CDN survivor re-attested `200` on nine straight sweeps (165th–174th) read `404` this sweep — recorded as an **END CANDIDATE**, one more scoped read pending, because two clean `404`s are state-change evidence while flap class is `000`/`502`. The self-capture is the probe itself: the sweep's FIRST read used the BARE name `reutil@1.0.3`, which on jsDelivr resolves to a DIFFERENT, legitimate 2024-era package (`reutil`, maintainer `neeswebservice`, versions `0.0.2–0.0.5`, unscoped root `200`) — the bare probe measured the wrong package entirely and its `404` carried zero information about the survivor. Only the SCOPED route `@worrisome/reutil@1.0.3` addresses the survivor; it read `404` on two independent re-verifications. **DURABLE: an unscoped probe of a scoped name is a null measurement — survivor sweeps keyed on package name alone systematically miss (and mis-score) scoped scopes.** Registry state holds meanwhile: `@worrisome/reutil` + `/aaaa` both frozen `[0.0.0-stage, 0.0.1-security]`, `modified` `21:20Z` Oct-21 = no re-arm at `+16 h`. Sweep context → [175th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-22-one-hundred-and-seventy-fifth-sweep).

## Related pages
- [ACR Stealer](../tools/acr-stealer.md)
- [macOS ClickFix fingerprinting-gate campaign](macos-clickfix-fingerprinting-gate-campaign.md)
- [RedC2 4.0 and the trojanized-npm delivery wave](../tools/redc2.md)
- [MCP stdio command-execution boundary](../patterns/mcp-stdio-command-execution.md)

## Sources
- OX Security: [ClickFix Phishing Pages Discovered in 24 npm Packages](https://www.ox.security/blog/research-clickfix-phishing-npm-packages)
