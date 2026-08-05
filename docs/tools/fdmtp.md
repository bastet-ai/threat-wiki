# FDMTP

## Summary
**FDMTP** is a modular .NET Windows backdoor named for its use of TouchSocket's Duplex Message Transport Protocol. Public reporting has associated it with Mustang Panda / Twill Typhoon activity, but use of the implant alone is not sufficient actor attribution.

FortiGuard Labs documented FDMTP in the 2025–2026 QuickFox software-supply-chain campaign. A process-filtering JavaScript loader installed the implant through DLL sideloading, after which FDMTP registered with web-based staging infrastructure, received cluster endpoints, collected host information, and loaded server-provided plugins.

## Tags
- tools
- malware
- backdoor
- RAT
- FDMTP
- .NET
- Windows
- TouchSocket
- DMTP
- DLL sideloading
- plugin framework
- registry storage
- Mustang Panda
- Twill Typhoon
- China-nexus

## Architecture and behavior
- A `Client.dll` payload contains compressed modules and uses assembly-resolution handlers to decompress and load them at runtime.
- `Client.FDMTPFrame.dll` orchestrates communication and plugin execution.
- The implant first calls a web staging service with a request such as `GET /GetCluster?protocol=DotNet-TcpFDMTP&tag=<campaign>`.
- The staging response supplies IP address and port nodes for subsequent DMTP communications.
- Initial registration can provide basic endpoint, user, OS, network, .NET, antivirus, process, active-window, and implant metadata for operator-side target selection.
- Reported RPC/plugin functionality supports file transfer, process and scheduled-task management, registry persistence or storage, command execution, and retrieval of additional payloads.
- Server-supplied compressed plugin assemblies can be stored under `HKCU\SOFTWARE\Microsoft\IME\{HWID}` and loaded by hash.
- Fortinet observed an `Assist.dll` plugin download additional files to `%LocalAppData%\Microsoft\WindowsApps` for later execution.

## QuickFox delivery chain
The QuickFox campaign used legitimate Microsoft `csmonitor.exe` to sideload `Microsoft.ServiceHosting.Tools.dll` from `%APPDATA%\Local\Temp\quickfox\updated\`.

- Generation 1 embedded FDMTP `Client.dll` as a byte array in the malicious DLL.
- Generation 2 used a JieJie-obfuscated loader and AES-128-ECB encrypted `update.bin` or `config.bin` payload.
- A one-byte `data.dat` file acted as a reinfection mutex.

See [QuickFox FDMTP software supply-chain compromise](../ops/quickfox-fdmtp-supply-chain-compromise.md) for affected versions, loader behavior, indicators, and response guidance.

## Detection guidance
- Alert on a legitimate `csmonitor.exe` in user-writable temporary directories loading a collocated `Microsoft.ServiceHosting.Tools.dll`.
- Correlate that sideload chain with `update.bin`, `config.bin`, `data.dat`, or a preceding QuickFox/Electron-to-`cmd.exe /c tasklist` process tree.
- Monitor web requests whose query includes `protocol=DotNet-TcpFDMTP`, especially to newly registered CDN- or API-themed domains.
- Hunt the registry path `HKCU\SOFTWARE\Microsoft\IME\{HWID}` for compressed or executable-looking values inconsistent with normal IME configuration.
- Detect .NET processes opening unusual long-lived TCP sessions after querying staging paths such as `/GetCluster`, `/GetSlaver`, `/GetNodes`, `/GetHosts`, or `/GetEndpoints`.
- Preserve loaded-module and network telemetry. Staging APIs, filenames, encrypted payload names, and cluster endpoints changed across generations.

## Attribution limits
Fortinet reported high-confidence infrastructure and tooling continuity between the QuickFox samples and a Darktrace-reported FDMTP campaign associated publicly with Twill Typhoon / Mustang Panda. Fortinet did not confidently attribute the QuickFox supply-chain compromise itself because it lacked visibility into decisive second-stage operator behavior. Track the family and infrastructure independently from actor attribution.

## Sources
- FortiGuard Labs: [QuickFox Supply Chain Attack Used to Deploy FDMTP Implant](https://www.fortinet.com/blog/threat-research/quickfox-supply-chain-attack-used-to-deploy-fdmtp-implant)
