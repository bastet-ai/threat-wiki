# Turla STOCKSTAY backdoor operations

## Summary
Google Threat Intelligence Group (GTIG) reported a multi-year Turla campaign using **STOCKSTAY**, a multi-component .NET Windows backdoor. GTIG says Turla has developed and deployed STOCKSTAY since at least December 2022, with observed targeting of Ukrainian government and military organizations and entities tied to Italian foreign-policy interests.

STOCKSTAY communicates over secure WebSockets, splits responsibilities across tunneler / orchestrator / backdoor components, protects configuration through encryption and environmental or hard-coded keys, and overlaps with the Turla **KAZUAR** development ecosystem. GTIG's operational timeline includes malicious GPO deployment from a compromised Ukrainian domain controller, an Italy-themed MSI / web lure, Ukrainian university RDP-file phishing, compromised Ukrainian government infrastructure used as payload staging, and later K1MORPHER-obfuscated STOCKSTAY samples.

## Tags
- ops
- operations
- Turla
- Secret Blizzard
- SUMMIT
- VENOMOUS BEAR
- UAC-0194
- Russia-linked
- espionage
- STOCKSTAY
- KAZUAR
- K1MORPHER
- WILDDAY
- DIAMONDBACK
- Ukraine targeting
- Italy targeting
- foreign policy targeting
- RDP phishing
- malicious GPO
- WebSocket C2
- .NET malware
- registry persistence
- compromised infrastructure

## Why this matters
- The disclosure adds a durable Turla capability that has reportedly been in development since at least 2022 but was only publicly documented in June 2026.
- STOCKSTAY can sit alongside better-known Turla tools such as KAZUAR, WILDDAY, and DIAMONDBACK, giving the actor a parallel or fallback access channel.
- The campaign uses several delivery styles: domain-controller GPO deployment, MSI/lure staging, RDP-file phishing, malicious HTA/archive delivery, and compromised legitimate infrastructure.
- C2 over WebSockets plus stock-market-themed encrypted configuration makes network-only detection brittle unless defenders also hunt host artifacts and business-hours beacon shaping.

## Public operational timeline from GTIG
- **December 2022** — GTIG identified a uniquely trackable actor-compiled `websocket-sharp.dll` artifact bundled with most observed STOCKSTAY.STOCKBROKER samples, giving a development anchor.
- **September 2023 / Germany** — an early `DriversPrinterGraphic.rar` sample was uploaded to VirusTotal shortly after creation, likely from the malware developer.
- **Late 2023 / January 2024 / Ukraine** — during review of a Ukrainian organization compromise, Mandiant observed Turla deploying WILDDAY, DIAMONDBACK, KAZUAR, and STOCKSTAY via malicious GPO installation from a compromised domain controller. STOCKSTAY archives and configuration were staged on the domain controller near WILDDAY registry staging and a PowerShell backdoor (`iclsClient.ps1`).
- **February 2024 / Italy** — a `Copia.msi` package masqueraded as ILSpy and installed STOCKSTAY under `%LOCALAPPDATA%/Programs/SMN/` with registry-run persistence. The MSI opened an Italian-language election / foreign-affairs-themed URL and reused `wss://wool-basalt-clock.glitch[.]me/ws` C2.
- **March-April 2025 / Ukraine** — a compromised email account sent a university-themed message with a malicious RDP file. After the victim connected to actor infrastructure, Turla deployed STOCKSTAY.MARKETMAKER, which downloaded `docs.zip` from compromised State Regulatory Service of Ukraine infrastructure and used `wss://weatherdataai.theworkpc[.]com/ws` C2.
- **May 2025 / Poland submissions** — GTIG observed STOCKSTAY.STOCKBROKER samples obfuscated with **K1MORPHER**, a mechanism later seen in all core STOCKSTAY components and selected KAZUAR samples.
- **Mid-2025 / Ukraine** — GTIG reported additional Ukrainian delivery through calculator-themed archive / HTA activity hosted on compromised infrastructure.

## Attack chain and tradecraft
1. Initial access and deployment vary by operation: malicious GPO from a compromised domain controller, MSI installation, RDP-file spear phishing, or malicious HTA/archive lures.
2. The actor stages core STOCKSTAY components and an encrypted configuration file. Configuration may be environment-keyed, such as by domain name, or protected with a hard-coded password when the victim environment is not known in advance.
3. STOCKSTAY.STOCKMARKET orchestrates the malware ecosystem, decrypts configuration, coordinates the tunneler and backdoor through `WM_COPYDATA` IPC, and generates per-infection RSA material.
4. STOCKSTAY.STOCKBROKER establishes secure WebSocket C2 and acts as a relay between server and orchestrator.
5. STOCKSTAY.STOCKTRADER provides registry, file, command-execution, screenshot, archive, and system-survey operations.
6. STOCKSTAY.MARKETMAKER can download additional payloads and establish registry-run persistence while masquerading as legitimate software such as `MicrosoftUpdateOneDrive`.

## Hunt pivots
- `StockMarketView.exe`, `StockMarketNet.exe`, `StockMarketSystem.exe`, `SMNet.exe`, `SMEditor.exe`, `MicrosoftUpdateOneDrive.exe`, `default.conf`, or `fonts` appearing together in user-writable directories.
- .NET Windows Forms executables with adjacent `websocket-sharp.dll` and outbound `wss://` traffic.
- Registry-run persistence launching stock-market, PDF-viewer, calculator, ILSpy, or MicrosoftUpdateOneDrive-themed binaries from `%LOCALAPPDATA%`.
- Encrypted JSON-like configuration files containing `SystemConfiguration`, cryptocurrency WebSocket decoy service lists, `wss://` entries, or stock-market application descriptions.
- RDP-file phishing from compromised accounts followed by file writes from RDP staging directories and WebSocket traffic to actor-controlled domains.
- Domain-controller staging of ZIP archives, registry installation material, and Turla toolsets during Ukrainian or diplomatic-sector incidents.
- Business-hours beacon windows, especially Monday-Friday 0900-1800 local time, in STOCKSTAY configuration or network telemetry.

## Response guidance
1. Treat STOCKSTAY findings as espionage intrusion indicators and preserve evidence before cleanup: configuration files, staged archives, registry hives, domain-controller artifacts, RDP files, email headers, process telemetry, and WebSocket destinations.
2. Scope laterally for Turla-adjacent tooling such as KAZUAR, WILDDAY, DIAMONDBACK, PowerShell backdoors, malicious GPOs, and compromised domain-controller deployment paths.
3. Do not remove only the active executable. Remove run-key persistence, downloader artifacts, extracted component directories, and staged ZIP/MSI/HTA/RDP lures.
4. Rotate credentials and review domain-controller / GPO integrity where deployment occurred from privileged infrastructure.
5. Block known C2 where appropriate, but prioritize behavior and artifact hunts because GTIG documented multiple third-party-hosted or compromised-infrastructure paths.

## Public indicators highlighted by GTIG
| Indicator | Type | Context |
| --- | --- | --- |
| `wss://wool-basalt-clock.glitch[.]me/ws` | WebSocket URL | STOCKSTAY C2 in Ukraine / Italy operations |
| `wss://weatherdataai.theworkpc[.]com/ws` | WebSocket URL | STOCKSTAY C2 in 2025 Ukraine operation |
| `https://www.drs.gov[.]ua/wp-content/themes/twentytwentyfive/docs.zip` | URL | Compromised State Regulatory Service of Ukraine staging path |
| `https://circoloesteri.elezioni.idnet[.]it/admin-election/riepilogo.php` | URL | Italian-language voting / foreign-affairs lure opened by MSI custom action |
| `d1e54270433a94aa3d45d888e4c62299bee3480eb2cb4a5489c7dda69d476c3e` | SHA-256 | Actor-compiled `websocket-sharp.dll` |
| `b064a3efb04ed77e6c57955089ce639e193d166c8ea2216c98c3e9b701ea2cff` | SHA-256 | `Copia.msi` STOCKSTAY installer |
| `da8a96bc74e265f945f1cc6992c6dc0f9ea36ed1991f7b8d312db79d9bf78c40` | SHA-256 | `MicrosoftUpdateOneDrive.exe` STOCKSTAY.MARKETMAKER downloader |
| `9fe944147c15a87963b06baf6473288d64c23655a0ba9369c35566272d8efc73` | SHA-256 | `docs.zip` STOCKSTAY archive |
| `40a3b969d81ef1ef35dd9ebcc6774e060b1b8949d3d74f38ca6b7d789c95cdb3` | SHA-256 | STOCKSTAY configuration file |

## Related pages
- [Turla](../actors/turla.md)
- [STOCKSTAY](../tools/stockstay.md)
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)

## Sources
- Google Cloud / Google Threat Intelligence Group: https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering
