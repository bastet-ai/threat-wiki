# VEIL#DROP Blogger-hosted PureLogs stealer chain

## Summary
**VEIL#DROP** is a multi-stage Windows malware delivery chain reported by Securonix and summarized by The Hacker News on July 1, 2026. The chain uses social engineering, a fake PDF-named JavaScript file, PowerShell, Blogger-hosted staging, fileless .NET loading, and a cascading set of Microsoft-signed living-off-the-land binaries to deploy **PureLogs Stealer**.

Securonix assesses initial delivery likely occurs through spear-phishing or a drive-by compromise path. The notable defender value is not a new stealer family, but the loader pattern: trusted Google/Blogger infrastructure for staging, per-execution URL mutation, in-memory payload reconstruction, and fallback execution through multiple signed .NET tooling binaries when reflective loading is blocked.

## Tags
- ops
- operations
- malware delivery
- infostealer
- PureLogs Stealer
- VEIL#DROP
- Blogger abuse
- blogspot staging
- PowerShell
- Windows Script Host
- JavaScript masquerading
- fileless malware
- reflective .NET loading
- living-off-the-land binaries
- LOLBins
- XOR obfuscation
- runtime mutation
- polymorphic loader
- credential theft
- cloud credential risk

## Why this matters
- Blogger / Blogspot hosting lets the attacker blend payload retrieval into trusted Google-owned infrastructure and can bypass simple reputation-based filtering.
- The lure uses double-extension masquerading such as `transcript.pdf.js`; users and mail controls that key on the visible document name can miss that the payload is executable JavaScript.
- The loader mutates URL construction and script content at runtime, reducing the usefulness of static URL, hash, and script-signature detections.
- PureLogs theft can become an enterprise credential incident: browser, session, application, and cloud secrets harvested from one endpoint can support lateral movement and SaaS or cloud compromise.

## Attack chain
1. A victim receives or reaches a deceptively named JavaScript file masquerading as a document, with `transcript.pdf.js` given as a representative example.
2. Opening the file runs through Windows Script Host and launches PowerShell with execution-policy bypasses.
3. The first PowerShell stage retrieves a follow-on payload from Blogger / Blogspot infrastructure; Securonix reported `htlwub00klocate.blogspot[.]com` as the staging host.
4. The user may be shown a benign web page, such as Google, to create the impression that a PDF opened while the background infection proceeds.
5. The loader attempts to terminate selected processes such as `wscript.exe`, remove the original JavaScript evidence, and decrypt an embedded payload.
6. After XOR decryption, the chain dynamically constructs next-stage Blogspot URLs by inserting a random number of `/` characters into the URL string, complicating static URL matching.
7. The decoded script replaces placeholders with randomly generated values during execution, creating runtime mutation and polymorphic script content.
8. The next stage executes in memory and reflectively loads the core .NET malware assembly.
9. If in-memory .NET execution is blocked, the loader falls back to trusted Microsoft-signed binaries, including `regsvcs.exe`, `installutil.exe`, `msbuild.exe`, and `aspnet_compiler.exe`.
10. The final payload is PureLogs Stealer, which harvests sensitive data from the compromised host.

## Defender heuristics
- Hunt for `wscript.exe` or `cscript.exe` launching PowerShell from recently downloaded `*.pdf.js`, `*.doc.js`, or other double-extension script files.
- Search command-line telemetry for PowerShell execution-policy bypasses shortly after browser or mail-client download events.
- Investigate PowerShell network retrieval from `blogspot.com` / `blogger.com` domains, especially when followed by in-memory .NET execution or child processes from .NET framework tooling.
- Alert on suspicious process chains where PowerShell spawns or stages execution through `regsvcs.exe`, `installutil.exe`, `msbuild.exe`, or `aspnet_compiler.exe` outside known build, deployment, or admin workflows.
- Look for short-lived deletion of the original JavaScript lure, termination of `wscript.exe`, and follow-on browser opens to benign pages used as user distraction.
- In script-block logs, prioritize XOR decode loops, dynamic URL assembly involving repeated slash insertion, placeholder replacement with random strings, and reflective assembly loading.
- Treat confirmed PureLogs execution as credential compromise: revoke browser sessions, rotate credentials present on the endpoint, and review cloud/SaaS sign-ins after the suspected theft window.

## Response guidance
1. Preserve the original lure file, browser download metadata, mail artifacts, PowerShell script-block logs, AMSI/EDR telemetry, process trees, prefetch data, and network logs before remediation.
2. Scope other endpoints for the same double-extension lure names, Blogspot staging host access, and LOLBin fallback process chains.
3. Block the reported staging host and related resolved infrastructure where appropriate, but assume URL mutation and hosted-infrastructure rotation.
4. Reset or revoke credentials and sessions available to the compromised user, including browser-saved passwords, SSO sessions, cloud CLI credentials, source-control tokens, package-registry tokens, and admin portals.
5. Review downstream access from the stolen identity for mailbox rules, OAuth grants, cloud API calls, SaaS exports, and source-repository or CI/CD access.
6. Harden controls for script attachments and downloaded JavaScript: show file extensions, block Windows Script Host execution for ordinary users where feasible, and restrict PowerShell child-process patterns from mail clients and browsers.

## Related pages
- [StealC / Amadey infrastructure disruption](stealc-amadey-infrastructure-disruption.md)
- [Photo ZIP hospitality Node.js implant campaign](photo-zip-hospitality-nodejs-implant.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Securonix: [https://www.securonix.com/blog/veildrop-blogspot-hosted-powershell-loader/](https://www.securonix.com/blog/veildrop-blogspot-hosted-powershell-loader/)
- The Hacker News: [https://thehackernews.com/2026/07/veildrop-malware-chain-uses-blogger.html](https://thehackernews.com/2026/07/veildrop-malware-chain-uses-blogger.html)
