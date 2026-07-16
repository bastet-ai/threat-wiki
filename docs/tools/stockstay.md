# STOCKSTAY

## Summary
**STOCKSTAY** is a multi-component .NET Windows backdoor publicly documented by Google Threat Intelligence Group (GTIG) in June 2026 and attributed to **Turla** (SUMMIT / Secret Blizzard / VENOMOUS BEAR / UAC-0194).

GTIG assesses that Turla has developed and deployed STOCKSTAY since at least December 2022. Reported targeting includes Ukrainian government and military organizations and entities tied to Italian foreign-policy interests. The toolset overlaps with the Turla **KAZUAR** development ecosystem and uses encrypted WebSocket C2, component-to-component IPC, environmental or hard-coded configuration protection, and business-hours beacon shaping.

## Tags
- tools
- malware
- backdoor
- RAT
- STOCKSTAY
- Turla
- Secret Blizzard
- SUMMIT
- VENOMOUS BEAR
- UAC-0194
- Russia-linked
- FSB Center 16
- Ukraine targeting
- Italian foreign-policy targeting
- .NET
- Windows Forms
- WebSocket C2
- websocket-sharp
- WM_COPYDATA IPC
- KAZUAR overlap
- K1MORPHER
- MARKETMAKER

## Why this matters
- STOCKSTAY is not a single binary: defenders need to correlate the orchestrator, tunneler, backdoor, downloader, encrypted configuration, and server-side WebSocket behavior.
- The malware can masquerade as stock-market, PDF-viewer, calculator, ILSpy, or MicrosoftUpdateOneDrive-like software, so file-name reputation alone is weak.
- Turla used STOCKSTAY next to KAZUAR, WILDDAY, and DIAMONDBACK in at least one Ukrainian incident, suggesting it can serve as a failsafe or parallel persistence channel.
- The C2 path uses secure WebSockets and third-party hosting / web-service platforms; detection should combine process lineage, configuration artifacts, run keys, and `wss://` destinations.

## Components
- **STOCKSTAY.STOCKBROKER** (`net`) — proxy-aware tunneler that establishes a secure WebSocket connection and relays C2 traffic between the server and the orchestrator.
- **STOCKSTAY.STOCKMARKET** (`cor`) — orchestrator that loads encrypted configuration, coordinates components over `WM_COPYDATA` IPC, generates a 4096-bit RSA key pair on first execution, sends the implant public key to C2, and uses an infection identifier for tasking.
- **STOCKSTAY.STOCKTRADER** (`sys`) — host backdoor supporting file, registry, process-execution, screen-capture, archive, and system-survey operations.
- **STOCKSTAY.MARKETMAKER** — proxy-aware downloader that retrieves and extracts additional payloads, establishes registry-run persistence, and has been observed masquerading as `MicrosoftUpdateOneDrive`.
- **Server-side controller** — GTIG found a public GitHub repository containing a Python victim-facing STOCKSTAY WebSocket server controller, consistent with lightweight third-party hosting use.

## Backdoor capabilities reported by GTIG
- Delete files or directories (`Del`, `RmDir`).
- Enumerate directories (`Dir`).
- Retrieve files, including extension-filtered recursive collection into in-memory ZIP archives (`Get`).
- Capture the victim screen and return the image (`Image`).
- Create directories (`MkDir`).
- Process batches of serialized tasks (`MultyTask`).
- Append uploaded file content to a target path (`Put`).
- Read, write, and delete registry values (`RegRead`, `RegWrite`, `RegDelete`).
- Execute processes windowless with redirected stdout and a default 60-second timeout (`Run`).
- Survey OS, hardware, user, machine, disk, and running-process data via WMI (`Sysinfo`).
- Extract ZIP archives in place (`UnpackArchive`).

## Configuration and C2 notes
- Encrypted configuration data is embedded inside decoy fields that look like a stock-market information application and include legitimate cryptocurrency-market WebSocket URLs.
- Decrypted configuration fields include the WebSocket C2 URL, server identifiers / keys, weekday exclusions, and active-hour bounds.
- GTIG observed many configurations using Monday-Friday, 0900-1800 local-time windows, likely to blend into business traffic.
- Configurations can be environment-keyed, including domain-name-based decryption, or protected with a hard-coded password when the actor may not know the victim environment in advance.
- Outbound data is encrypted with a per-infection RSA key pair before transmission over WebSockets.

## Defender heuristics
- Hunt for unusual .NET Windows Forms executables communicating over `wss://` using `websocket-sharp.dll`, especially from user-writable install paths.
- Correlate multiple STOCKSTAY-looking components in the same directory (`StockMarketView.exe`, `StockMarketNet.exe`, `StockMarketSystem.exe`, `SMNet.exe`, `SMEditor.exe`, `default.conf`, `fonts`, or stock/PDF/calculator-themed variants).
- Review `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` and adjacent autorun keys for MicrosoftUpdateOneDrive-, stock-market-, ILSpy-, PDF-, or calculator-themed values launching unsigned .NET binaries from `%LOCALAPPDATA%`.
- Search JSON-like configuration files containing `SystemConfiguration`, `An application for getting information about current events on trading platforms`, decoy `BinanceApi` / `CoinbaseCloudApi` fields, or embedded `wss://` service lists.
- Alert on RDP-file phishing that writes or launches payloads from staging directories, followed by WebSocket traffic to actor domains or compromised Ukrainian infrastructure.
- Preserve configuration files before cleanup; environmental keying can make them valuable for scoping and victim-specific C2 reconstruction.

## Public indicators highlighted by GTIG
| Indicator | Type | Context |
| --- | --- | --- |
| `d1e54270433a94aa3d45d888e4c62299bee3480eb2cb4a5489c7dda69d476c3e` | SHA-256 | Actor-compiled `websocket-sharp.dll` artifact |
| `wss://wool-basalt-clock.glitch[.]me/ws` | WebSocket URL | STOCKSTAY C2 observed in Ukraine / Italy operations |
| `wss://weatherdataai.theworkpc[.]com/ws` | WebSocket URL | STOCKSTAY C2 observed in 2025 Ukraine RDP-phishing operation |
| `https://www.drs.gov[.]ua/wp-content/themes/twentytwentyfive/docs.zip` | URL | Compromised State Regulatory Service of Ukraine infrastructure serving STOCKSTAY archive |
| `MicrosoftUpdateOneDrive.exe` | Filename | STOCKSTAY.MARKETMAKER downloader masquerade |
| `40a3b969d81ef1ef35dd9ebcc6774e060b1b8949d3d74f38ca6b7d789c95cdb3` | SHA-256 | STOCKSTAY configuration file from 2025 Ukraine operation |
| `9fe944147c15a87963b06baf6473288d64c23655a0ba9369c35566272d8efc73` | SHA-256 | `docs.zip` archive containing STOCKSTAY components |
| `da8a96bc74e265f945f1cc6992c6dc0f9ea36ed1991f7b8d312db79d9bf78c40` | SHA-256 | `MicrosoftUpdateOneDrive.exe` downloader |

## Related pages
- [Turla](../actors/turla.md)
- [Turla STOCKSTAY backdoor operations](../ops/turla-stockstay-backdoor-operations.md)

## Sources
- Google Cloud / Google Threat Intelligence Group: <https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering>
