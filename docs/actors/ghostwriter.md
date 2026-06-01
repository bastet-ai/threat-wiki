# Ghostwriter

## Summary
**Ghostwriter** is a Belarus-aligned cyberespionage and influence-operations cluster also tracked publicly as **FrostyNeighbor**, **UAC-0057**, **UNC1151**, **TA445**, **PUSHCHA**, and **Storm-0257**. ESET's May 2026 reporting and CERT-UA's May 21, 2026 reporting both document spring 2026 phishing against Ukrainian government organizations, with different lure themes but the same durable defender pattern: geofenced or account-specific delivery, JavaScript archive execution, downloader staging, and likely Cobalt Strike follow-on.

ESET's FrostyNeighbor report adds a March 2026 Ukrainian-government chain using Ukrtelecom-themed PDF lures, server-side victim validation, RAR/JavaScript delivery, scheduled-task persistence, and a JavaScript **PicassoLoader** variant. CERT-UA's Prometheus-themed reporting adds JavaScript malware staged as **OYSTERFRESH**, **OYSTERSHUCK**, and **OYSTERBLUES**, with possible follow-on **Cobalt Strike** deployment. The activity is durable threat.wiki material because it adds named malware components, host artifacts, persistence paths, and network-infrastructure patterns for a long-running state-aligned actor.

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
- PicassoLoader

## Primary motivation
- **Espionage** against Ukrainian government organizations and other strategic targets.
- **Credential and access collection** through phishing and staged malware.
- **Long-term access** using registry-staged payloads, startup persistence, and possible post-exploitation tooling.

## Naming and affiliation
- ESET tracks the cluster as `FrostyNeighbor` and lists public overlaps with `Ghostwriter`, `UNC1151`, `UAC-0057`, `TA445`, `PUSHCHA`, and `Storm-0257`.
- CERT-UA tracks related activity as `UAC-0057` and links it to `UNC1151`.
- The Hacker News describes the same cluster as `Ghostwriter`, a Belarus-aligned actor.
- Keep this page distinct from Russian military clusters such as APT28/Sandworm unless a primary source explicitly joins the operations.

## 2026 Ukrtelecom-themed FrostyNeighbor campaign
- **Source/date:** ESET report published 2026-05-14, covering activity observed from March 2026.
- **Targeting:** Ukrainian governmental organizations, with broader historical victimology across Ukraine, Poland, Lithuania, and other Eastern European strategic sectors.
- **Initial lure:** a blurry Ukrtelecom-themed PDF attachment with a remote download button.
- **Server-side validation:** the delivery server returned a benign regulatory PDF outside the expected Ukrainian victim profile, but a RAR archive to matching victims.
- **Execution chain:** PDF link → `53_7.03.2026_R.rar` → JavaScript dropper → decoy PDF display → JavaScript **PicassoLoader** staged under `%AppData%\WinDataScope\Update.js`.
- **Persistence:** the dropper downloaded an XML scheduled-task template disguised behind a `.jpg` request and populated it for PicassoLoader execution; it also staged a registry file under `%AppData%\WinDataScope\WinUpdate.reg`.
- **Follow-on:** PicassoLoader fingerprinted the host and retrieved a Cobalt Strike payload disguised as web/image-like content, matching the actor's long-running use of downloader-to-beacon chains.

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
- Government or enterprise mailboxes sending Ukrtelecom, Prometheus, certificate, or electronic-communications-themed PDFs with archive-download links.
- JavaScript launched from downloaded ZIP/RAR archives, especially `53_7.03.2026_R.js`, `certificate.js`, `amplifier.js`, `EdgeTaskMachine.js`, `dist.js`, `tags`, or similarly themed scripts.
- Registry staging under `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\Blue\'Oyster'` or `%AppData%\WinDataScope\WinUpdate.reg`.
- Startup persistence using `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\'MicrosoftEdgeUpdate'` or `'WindowsEdgeStartup'`.
- Host artifacts under `%APPDATA%\EdgeMachineData\` and `%PROGRAMDATA%\WindowsEdgeApp\`, including `MicrosoftEdgeUpdate.exe`, `EdgeApp.exe`, and `EdgeSystemConfig.dll`.
- Scheduled task `MicrosoftEdgeUpdateTaskMachine` or actor-created tasks populated from remote XML templates in contexts where those tasks are not expected.
- Outbound traffic to newly observed Cloudflare-fronted `.icu` domains, especially Prometheus/certificate-themed paths.
- Standard-user execution of `wscript.exe`; CERT-UA recommends restricting it to reduce the attack surface.

## Selected indicators
- **Malware/component names:** `PicassoLoader`, `OYSTERFRESH`, `OYSTERSHUCK`, `OYSTERBLUES`, `EdgeSystemConfig.dll` / `CSBEACON`.
- **Example SHA-256 hashes:** `65752ab1d78b215e70a543b790a1946b9e316474fce114bd2089f35030801988`, `859462bc01536e70ca024f0457f03f6f3f7833d13a032bf30e59c97d10ea691e`, `10a83a7e45de345d72d203e0ee6414f057b00d0bdd48bf2141364ae00e020203`, `b640a99ab2af33024af7217de718cc5fde9c44b819d4f0943a8cbe27655b9eef`.
- **Domains:** `a3ufz.xsjdsb[.]icu`, `ifo-jupyter.natter[.]icu`, `easiestnewsfromourpointofview.algsat[.]icu`, `mickeymousegamesdealer.alexavegas[.]icu`, `advancedaisolutionsforeveryone.a1si[.]icu`, `productionsamplesoftheyear.cgdirector[.]icu`.

## Notes
- Treat the CERT-UA indicator list as campaign-scoped: prioritize behavior and staging patterns over single-use infrastructure.
- The combination of compromised-account delivery, JavaScript archive execution, registry-staged payloads, and Cobalt Strike follow-on should trigger incident-response handling even if individual domains have rotated.

## Sources
- ESET: https://www.welivesecurity.com/en/eset-research/frostyneighbor-fresh-mischief-digital-shenanigans/
- CERT-UA: https://cert.gov.ua/article/6315762
- The Hacker News: https://thehackernews.com/2026/05/ghostwriter-targets-ukraine-government.html
