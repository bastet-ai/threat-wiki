# Ghostwriter

## Summary
**Ghostwriter** is a Belarus-aligned cyberespionage and influence-operations cluster also tracked publicly as **UAC-0057** and **UNC1151**. CERT-UA's May 21, 2026 reporting documents a spring 2026 phishing campaign against Ukrainian government organizations that abused compromised email accounts and Prometheus-themed certificate lures.

The campaign delivered JavaScript malware staged as **OYSTERFRESH**, **OYSTERSHUCK**, and **OYSTERBLUES**, with possible follow-on **Cobalt Strike** deployment. The activity is durable threat.wiki material because it adds named malware components, host artifacts, registry persistence paths, and network-infrastructure patterns for a long-running state-aligned actor.

## Tags
- Belarus
- Ukraine
- APT
- espionage
- phishing
- compromised accounts
- JavaScript malware
- Cobalt Strike
- OYSTERFRESH
- OYSTERSHUCK
- OYSTERBLUES

## Primary motivation
- **Espionage** against Ukrainian government organizations and other strategic targets.
- **Credential and access collection** through phishing and staged malware.
- **Long-term access** using registry-staged payloads, startup persistence, and possible post-exploitation tooling.

## Naming and affiliation
- CERT-UA tracks the activity as `UAC-0057` and links it to `UNC1151`.
- The Hacker News describes the same cluster as `Ghostwriter`, a Belarus-aligned actor.
- Keep this page distinct from Russian military clusters such as APT28/Sandworm unless a primary source explicitly joins the operations.

## 2026 Prometheus-themed campaign
- **Targeting:** Ukrainian government organizations, active since spring 2026.
- **Initial access:** phishing emails sent from compromised accounts. Lures referenced receiving certificates through the Ukrainian Prometheus online-learning platform.
- **Delivery chain:** PDF attachment → embedded link → ZIP archive → JavaScript payload.
- **Stage 1:** `certificate.js` / **OYSTERFRESH** displays a decoy document, writes the obfuscated and encoded **OYSTERBLUES** payload into the Windows Registry, and downloads/launches **OYSTERSHUCK**.
- **Stage 2:** **OYSTERSHUCK** decodes OYSTERBLUES using string reversal, ROT13, and URL decoding.
- **Stage 3:** **OYSTERBLUES** collects host/user/OS/process information, posts it to C2, then waits for JavaScript returned by the server and executes it via `eval`.
- **Follow-on:** CERT-UA says Cobalt Strike can be downloaded at the next stage.
- **Infrastructure:** CERT-UA notes Cloudflare-fronted infrastructure and heavy use of `.icu` domains, typical for UAC-0057.

## Defender signals
- Government or enterprise mailboxes sending Prometheus/certificate-themed PDFs with archive-download links.
- JavaScript launched from downloaded ZIP/RAR archives, especially `certificate.js`, `amplifier.js`, `EdgeTaskMachine.js`, `dist.js`, `tags`, or similarly themed scripts.
- Registry staging under `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\Blue\'Oyster'`.
- Startup persistence using `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\'MicrosoftEdgeUpdate'` or `'WindowsEdgeStartup'`.
- Host artifacts under `%APPDATA%\EdgeMachineData\` and `%PROGRAMDATA%\WindowsEdgeApp\`, including `MicrosoftEdgeUpdate.exe`, `EdgeApp.exe`, and `EdgeSystemConfig.dll`.
- Scheduled task `MicrosoftEdgeUpdateTaskMachine` in contexts where that exact task is not expected.
- Outbound traffic to newly observed Cloudflare-fronted `.icu` domains, especially Prometheus/certificate-themed paths.
- Standard-user execution of `wscript.exe`; CERT-UA recommends restricting it to reduce the attack surface.

## Selected indicators
- **Malware/component names:** `OYSTERFRESH`, `OYSTERSHUCK`, `OYSTERBLUES`, `EdgeSystemConfig.dll` / `CSBEACON`.
- **Example SHA-256 hashes:** `65752ab1d78b215e70a543b790a1946b9e316474fce114bd2089f35030801988`, `859462bc01536e70ca024f0457f03f6f3f7833d13a032bf30e59c97d10ea691e`, `10a83a7e45de345d72d203e0ee6414f057b00d0bdd48bf2141364ae00e020203`, `b640a99ab2af33024af7217de718cc5fde9c44b819d4f0943a8cbe27655b9eef`.
- **Domains:** `a3ufz.xsjdsb[.]icu`, `ifo-jupyter.natter[.]icu`, `easiestnewsfromourpointofview.algsat[.]icu`, `mickeymousegamesdealer.alexavegas[.]icu`, `advancedaisolutionsforeveryone.a1si[.]icu`, `productionsamplesoftheyear.cgdirector[.]icu`.

## Notes
- Treat the CERT-UA indicator list as campaign-scoped: prioritize behavior and staging patterns over single-use infrastructure.
- The combination of compromised-account delivery, JavaScript archive execution, registry-staged payloads, and Cobalt Strike follow-on should trigger incident-response handling even if individual domains have rotated.

## Sources
- CERT-UA: https://cert.gov.ua/article/6315762
- The Hacker News: https://thehackernews.com/2026/05/ghostwriter-targets-ukraine-government.html
