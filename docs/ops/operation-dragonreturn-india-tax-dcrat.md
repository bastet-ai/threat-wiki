# Operation DragonReturn India tax-season DcRAT campaign

## Summary
Seqrite reports **Operation DragonReturn** as an active China-nexus cyber-espionage campaign targeting India's AY2026-27 income-tax filing season. The operation impersonates the Government of India Income Tax Department / Ministry of Finance, lures taxpayers, tax professionals, chartered accountants, and corporate finance teams to a fake offline-utility download, and deploys a multi-stage Windows loader chain ending in encrypted remote-access tooling with DcRAT-like capabilities.

Seqrite assesses the activity with **medium-to-high confidence** as linked to a China-aligned threat cluster based on Chinese-language artifacts, infrastructure overlap, TTP similarity, and hosting pivots. Keep the attribution caveated: infrastructure geography and language artifacts support the assessment but are not standalone proof of a specific actor.

## Tags
- ops
- operations
- espionage
- China-linked
- India
- Ministry of Finance
- tax-season phishing
- spear phishing
- DcRAT
- Windows service persistence
- process injection
- AMSI bypass

## Why this matters
- The lure copies a real high-trust government workflow: the Indian Income Tax Department offline utility for ITR-1 to ITR-4 during AY2026-27 filing season.
- Seqrite says the campaign was first observed on May 18, 2026 and remained active as of June 17, with payload rotation every 7–10 days and a latest observed variant showing 0/66 VirusTotal detection.
- The chain combines credible bilingual legal/tax language, real tax-act citations, fake government memoranda, staged image-container payload delivery, Windows service persistence, process injection into `svchost.exe`, AMSI patching, in-memory .NET loading, TLS-encrypted C2, screenshot / desktop capture capability, and MessagePack host registration.
- The targeting scope is broader than a single ministry intrusion: taxpayers, tax practitioners, and finance teams create a large social-engineering surface with downstream financial and sensitive-document exposure.

## Reported delivery chain
- Initial phishing impersonates India's Income Tax Department and carries an attachment / document related to a tax notice.
- The lure embeds a link to `govtop[.]one/incometax`, which presents a fake Office Memorandum with Government of India emblem styling, Hindi-English formatting, a fabricated reference number `No. TAX/PEN/2026-142`, and real legal citations such as Income Tax Act Sections 271(1)(c) and 276C.
- The download is named `Common_Offline_Utility_ITR-1_to_4_AY2026-27.zip`, closely matching the legitimate Income Tax Department offline-utility naming convention.
- Execution starts a downloader / installer that creates a working directory under `C:\Program Files\Windows Media Player` and uses a trusted-looking binary name, `Mixed Reality.exe`.
- The malware downloads `lllyd.jpg` from `204.194.48[.]250` and stores it as `C:\Windows\background.jpg`; Seqrite reports the image acts as a container for embedded secondary payloads rather than a normal image.
- Persistence is established through a Windows service:
  - service name: `MixedSvc`
  - display name: `Windows Mixed Reality Service`
  - binary path: `C:\Program Files\Windows Media Player\Mixed Reality.exe`
  - startup: automatic
- The installer extracts / uses `nvdaHelperRemote.dll`, performs elevation checks through `CheckTokenMembership()`, can relaunch with `ShellExecuteW(..., "runas", ...)`, and enforces single-instance execution with `Global\ShitSetupOn26126k`.

## Loader and payload behavior
- Seqrite describes timing and environment-validation logic using `GetTickCount64()` and short sleep intervals to detect sandbox acceleration, debugger interference, or API hooking.
- One stage resolves Windows APIs dynamically after XOR string deobfuscation, reads / decrypts roughly 166 KB of shellcode or PE data, enumerates processes with `CreateToolhelp32Snapshot()`, finds `svchost.exe`, allocates executable remote memory, writes the payload, and starts execution through a remote thread before exiting.
- A session-management stage waits for `nvdaHelperRemote.dll`, reads `C:\Windows\background.jpg`, decrypts two payloads, enumerates Terminal Services sessions with `WTSEnumerateSessionsW()`, and appears to deploy distinct payload components per active user session.
- The malware writes status / victim-state data to hidden-system `C:\debug.txt` in a `client=<id>` format.
- Payload A is a .NET loader that:
  - performs anti-analysis delay loops;
  - checks for and patches `amsi.dll` / `AmsiOpenSession()` in memory;
  - decrypts an embedded managed assembly with Windows CNG / AES and a hardcoded 16-byte key;
  - loads .NET Framework `v4.0.30319` through `CLRCreateInstance()`;
  - loads the decrypted assembly directly via `AppDomain::Load_3()`;
  - performs registry operations that may store configuration or persistence-related values.
- The .NET payload creates an encrypted `SslStream` over TCP and sends host registration data using MessagePack plus ZIP compression.
- Reported collected host data includes hardware ID, username, OS version / architecture, executable path, malware version, privilege level, active window title, installed antivirus products, executable timestamp, campaign ID, and related victim-identification fields.
- Desktop-capture and compression libraries reported by Seqrite indicate screenshot / desktop monitoring and data exfiltration capability.

## Infrastructure and indicators
- Lure / download: `govtop[.]one/incometax`
- First-stage image-container payload: `204.194.48[.]250` / `lllyd.jpg`
- Local staged container: `C:\Windows\background.jpg`
- C2 endpoint reported for the .NET payload: `223.26.63[.]40:2671`
- Domain string observed in memory: `ikkkkddd[.]com`
- Payload B hardcoded C2 domain: `kkxqbh[.]top`
- Infrastructure pivots noted by Seqrite include `118.107.0[.]197`, `27.50.54[.]191`, and `117.44.201[.]119`.
- Hosting / ASN context reported by Seqrite includes AS152194 (CTG Server Limited), AS140869 (Turing Group Limited), and AS4134 / CHINANET BACKBONE for a `kkxqbh[.]top` resolution in Nanchang, Jiangxi, China.

## Defender notes
- Treat downloads named like `Common_Offline_Utility_ITR-1_to_4_AY2026-27.zip` outside trusted government distribution paths as high risk, especially when sourced from non-government domains.
- Hunt for the service and path combination `MixedSvc`, `Windows Mixed Reality Service`, and `C:\Program Files\Windows Media Player\Mixed Reality.exe`.
- Hunt for `nvdaHelperRemote.dll`, `C:\Windows\background.jpg` used as a payload container, and hidden-system `C:\debug.txt` containing `client=` values.
- Watch for `sc.exe` creating auto-start services from user-triggered tax-utility downloads, followed by `svchost.exe` injection, `WTSEnumerateSessionsW()`, and `AmsiOpenSession()` memory patching.
- Add network detections for unusual TLS sessions to the listed C2 IP / domains and for connections to `govtop[.]one`, `ikkkkddd[.]com`, or `kkxqbh[.]top` from taxpayer, finance, or accounting endpoints.
- For exposed victims, preserve the ZIP, downloaded image container, service configuration, registry artifacts, prefetch / ShimCache / AmCache, PowerShell / process telemetry, TLS destination logs, and memory images before eradication.
- Because Seqrite's attribution is medium-to-high confidence but not tied to a public named actor, prioritize concrete behavior and infrastructure over actor-label matching.

## Related pages
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)
- [Operation XENOFISCAL SideCopy XenoRAT campaign](operation-xenofiscal-sidecopy-xenorat.md)
- [Thailand healthcare RAR / Python stealer campaign](thailand-healthcare-rar-python-stealer.md)

## Sources
- Seqrite Labs: <https://www.seqrite.com/blog/operation-dragonreturn-china-nexus-cyber-espionage-campaign-targeting-govt-of-india-mof-tax-infrastructure-via-multi-stage-dcrat-deployment/>
