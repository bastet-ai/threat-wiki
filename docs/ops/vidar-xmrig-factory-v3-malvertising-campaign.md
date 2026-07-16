# Vidar / XMRig Factory-v3 malvertising campaign

## Summary
On July 7, 2026, Unit 42 published analysis of a financially motivated April 2026 campaign that delivered **Vidar Stealer** and **XMRig** through malvertising for cracked / pirated software. The campaign used password-protected archives with `.bin` filenames, Go-compiled **Factory-v3 / UpdateFactory** loader builds, fake Authenticode certificate branding, file-size inflation, an in-memory AMSI bypass, and persistence through Run keys, scheduled tasks, and Startup-folder scripts.

Unit 42 assesses the operator as a Vidar stealer malware-as-a-service affiliate targeting consumer and SMB victims, with observed activity concentrated in the United States and European Union. The same builder/toolchain and certificate infrastructure also appeared in a concurrent Lumma Stealer campaign, suggesting the loader service is shared across stealer affiliates.

## Tags
- ops
- Vidar Stealer
- XMRig
- Factory-v3
- UpdateFactory
- X3D MINER
- malvertising
- cracked software
- password-protected archive
- `.bin`
- Go loader
- Go malware
- file inflation
- null-byte padding
- AMSI bypass
- AmsiScanBuffer
- DLL sideloading
- MpClient.dll
- Windows Defender
- Authenticode impersonation
- fake certificate
- JustWatch
- Bleacher Report
- Lumma Stealer
- browser credential theft
- cookie theft
- cryptocurrency wallet theft
- Monero mining
- Telegram notification
- persistence
- Run key
- scheduled task
- Startup folder
- Unit 42

## Timeline
- **2026-04:** Unit 42 observed a spike of Vidar samples and identified 43 loader binaries delivering Vidar plus XMRig.
- **2026-04-24:** Unit 42 pivoted from the initial loaders to 56 additional samples of a follow-on variant that retained the same builder, delivery, Telegram dead-drop, payload, and C2 infrastructure but changed certificate impersonation.
- **2026-07-07:** Unit 42 published campaign analysis.

## Attack chain
1. Victims search for cracked or pirated copies of popular software and land on malvertising-driven download pages.
2. The operator serves password-protected archives with `.bin` filenames, limiting automated email-gateway and sandbox inspection.
3. The extracted loader presents a branded-but-untrusted Authenticode signature to increase victim trust.
4. The Factory-v3 / UpdateFactory loader runs anti-analysis checks, patches `AmsiScanBuffer` in memory, and stages Vidar Stealer plus the XMRig mining package tracked by Unit 42 as **X3D MINER**.
5. Vidar collects browser credentials, cookies, cryptocurrency-wallet data, file and host metadata, and exfiltrates an archive to C2.
6. XMRig launches with an in-memory-built configuration and mines Monero through `pool.supportxmr[.]com`, using a victim-specific HWID in the pool auth token.
7. The operator receives Telegram notifications labeled `X3D MINER • NEW LOG` for successful infections and stolen data.

## Technical notes
- **Factory-v3 / UpdateFactory builder:** Unit 42 found embedded Go build metadata and PDB strings referencing `C:\Users\Administrator\Desktop\UpdateFactory\compiler\1.25.9\go\src\runtime\cgo`. The builder produced many unique hashes; Unit 42 observed 27 unique build UUIDs across 43 samples.
- **Anti-forensics:** samples zeroed the PE `TimeDateStamp`, omitted PE version information, reduced imports to `kernel32.dll`, and obfuscated user-defined type names to `V######` patterns.
- **Certificate impersonation:** the first 43 loader samples used a fabricated Authenticode signature with subject `CN=justwatch[.]com` and issuer `CN=WR3`; JustWatch was not compromised. A later variant used `CN=\*.bleacherreport[.]com` with a cloned `GlobalSign Atlas R3 DV TLS CA 2026 Q1` issuer name; Bleacher Report was not compromised.
- **DLL sideloading cluster:** one loader cluster exported Windows Defender `MpClient.dll`-style API functions, including `MpAllocMemory`, `MpClientUtilExportFunctions`, `MpConfigOpen`, and `MpFreeMemory`, enabling DLL search-order hijacking when placed in a higher-priority path.
- **File-size inflation:** x64 and x86 Go loader clusters appended hundreds of megabytes of null bytes after the last PE section; the largest observed sample was 491 MB even though the real malicious content was about 2.3 MB and compressed to about 2.4 MB.
- **AMSI bypass:** the Vidar core payload sample `7ed4a256e1d281cb4f194d13ff554fb280dafde0a67a18115ea038ea6c87d` resolved and patched `AmsiScanBuffer` so it returned `E_INVALIDARG`; `amsi.dll` and `AmsiScanBuffer` strings were XOR-obfuscated with key `0x05`.
- **Payload files:** Unit 42 reported `%TEMP%\MicrosoftUpdate.exe` for Vidar, `%AppData%\Roaming\Microsoft\Windows\Temp\MicrosoftEdgeUpdate.exe` for XMRig, `%AppData%\Roaming\Microsoft\Windows\Temp\NisSrv.exe` as a persistence copy, plus `libuv-1.dll`, `WinRing0x64.sys`, and `mgwthmc2.dat` in the same Temp path.
- **Persistence:** `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` value `SystemAgentService`, an `onlogon` scheduled task named `SystemAgentService`, and Startup-folder batch script `%StartUp%\FEbJCNWOCKMJ.bat` all pointed back to the `NisSrv.exe -s` persistence copy.

## Selected indicators
- `116.203.243[.]208`
- `136.243.203[.]109`
- `136.243.203[.]111`
- `138.199.246[.]13`
- `pool.supportxmr[.]com`
- Telegram channel `ci0iiif`
- Certificate serial `2f:7e:f0:15:7d:17:62:5c:09:86:91:ce:f1:ff:7d:63`
- Certificate SHA1 `ab92f731ab20774dfdb95664ee41a2fbafe2a284`
- Cluster imphashes: `d42595b695fc008ef2c56aabd8efd68e`, `d8b31f8c03e0c76ff245ed05a15ffe6c`, `1aae8bf580c846f39c71c05898e57e88`, `c10333c92889b65c3590ef2b3819b420`

## Defender guidance
- Do not trust certificate display names alone. Enforce full Authenticode chain validation and alert on recognizable-brand subject names that do not chain to a trusted root.
- Configure endpoint and sandbox tooling to scan oversized executables rather than skipping files above 50-100 MB. Strip or normalize appended null-byte padding before size-based triage decisions.
- Hunt for `MpClient.dll` loading from non-standard directories, especially adjacent to suspicious Windows Defender binaries or cracked-software download paths.
- Alert on the combined pattern of `MicrosoftUpdate.exe`, `MicrosoftEdgeUpdate.exe`, `NisSrv.exe`, `WinRing0x64.sys`, and `mgwthmc2.dat` under user-writable Temp / Roaming paths.
- Monitor for `AmsiScanBuffer` memory patching, `E_INVALIDARG` AMSI bypass stubs, and XOR-obfuscated `amsi.dll` / `AmsiScanBuffer` strings.
- Treat Vidar findings as credential-compromise incidents: rotate browser-saved credentials, revoke active web sessions, invalidate cookies/tokens where supported, inspect cryptocurrency-wallet exposure, and check downstream account access.
- Block or investigate outbound traffic to the listed C2 addresses and `pool.supportxmr[.]com`; preserve the original padded sample because size and certificate artifacts are part of detection and attribution pivots.

## Related pages
- [Perplexity AI-spoofing Chromium extension search hijacker](perplexity-ai-chromium-extension-search-hijacker.md)
- [Silent Swap Google Notes crypto clipper](silent-swap-google-notes-crypto-clipper.md)
- [VPN Go browser-extension clipboard stealer](vpn-go-browser-extension-clipboard-stealer.md)
- [StealC / Amadey infrastructure disruption](stealc-amadey-infrastructure-disruption.md)

## Sources
- [Unit 42](https://unit42.paloaltonetworks.com/vidar-stealer-xmrig-miner-campaign-analysis/)
