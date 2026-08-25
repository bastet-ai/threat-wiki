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

## Related pages
- [ACR Stealer](../tools/acr-stealer.md)
- [macOS ClickFix fingerprinting-gate campaign](macos-clickfix-fingerprinting-gate-campaign.md)
- [RedC2 4.0 and the trojanized-npm delivery wave](../tools/redc2.md)
- [MCP stdio command-execution boundary](../patterns/mcp-stdio-command-execution.md)

## Sources
- OX Security: [ClickFix Phishing Pages Discovered in 24 npm Packages](https://www.ox.security/blog/research-clickfix-phishing-npm-packages)
