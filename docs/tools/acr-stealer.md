# ACR Stealer

## Summary
Microsoft Threat Intelligence reported on July 16, 2026 that Microsoft Defender Experts observed increased **ACR Stealer** activity across customer environments from late April through mid-June 2026. Microsoft describes ACR Stealer as an information-stealing malware family reportedly sold as malware-as-a-service and associated with a rebrand of Amatera Stealer.

The high-signal defender point: the observed campaigns begin with ClickFix social engineering, then split into two different delivery chains that still converge on browser credential, session-token, authentication-artifact, and document theft.

## Tags
- tools
- malware
- infostealer
- MaaS
- ACR Stealer
- Amatera Stealer
- ClickFix
- WebDAV
- mshta
- PowerShell
- Python
- rundll32
- conhost
- scheduled tasks
- steganography
- EtherHiding
- blockchain dead drop
- browser credential theft
- DPAPI
- token theft
- document theft
- malvertising
- SEO poisoning
- Microsoft Threat Intelligence

## Campaigns observed by Microsoft
### Campaign 1: WebDAV ClickFix, Python loaders, and blockchain C2 resolution
- Initial access uses a ClickFix prompt, likely through malvertising or SEO-poisoned search results, that instructs the target to run a command.
- The command launches `cmd.exe` and then uses `rundll32.exe` to load a DLL from a remote HTTPS WebDAV share.
- Microsoft observed direct `rundll32` execution, `pushd`-mounted WebDAV shares, and a more hidden variant using `conhost.exe --headless` plus delayed environment-variable expansion to hide `pushd`, `rundll32`, and host strings.
- The chain runs heavily obfuscated PowerShell, downloads a ZIP payload into deceptive `%LocalAppData%\Temp` paths such as `LogiOptionsPlus`, launches bundled `pythonw.exe`, cleans prior deployments, creates hidden scheduled-task persistence, timestomps files from `notepad.exe`, and clears PowerShell command history.
- The Python loader reconstructs strings and payloads at runtime through encoding, reversal, Base64, and zlib layers, then runs shellcode in memory using `VirtualAlloc` and the Windows Fiber APIs `ConvertThreadToFiber`, `CreateFiber`, and `SwitchToFiber`.
- A subset uses EtherHiding-style blockchain dead-drop resolution, querying public blockchain RPC / Web3 infrastructure to retrieve follow-on payload or C2 data.

### Campaign 2: MSHTA, obfuscated PowerShell, and steganographic payloads
- The second chain also starts with ClickFix, but launches `mshta.exe` to fetch and execute remote HTA content.
- Embedded VBScript abuses COM objects to decode and run PowerShell.
- The PowerShell stage creates a victim identifier, disables certificate validation, and executes retrieved content in memory.
- Instead of a conventional script download, the chain pulls a JPEG from an image-hosting service, extracts encrypted payload material from image pixels, decrypts/decompresses it, and runs shellcode in memory.
- The payload dynamically resolves APIs such as `LoadLibrary`, `GetProcAddress`, `VirtualAlloc`, `CreateThread`, and `WaitForSingleObject` for reflective execution.

## Theft objectives
Microsoft reports both campaigns target:
- Chromium-family browser credential stores, including Chrome and Edge `Login Data` and `Web Data` databases.
- DPAPI-protected browser passwords, cookies, and authentication tokens.
- PDFs, Microsoft 365 documents, and data under enterprise-synchronized locations such as OneDrive and SharePoint.
- Archived/staged data prepared for exfiltration.

## Indicators reported by Microsoft
### Campaign 1 C2 domains
- `looksta[.]icu`
- `contrite.quirksturdy[.]icu`
- `ux.strainedeasily[.]icu`
- `cpppemwjewjoiwejow[.]sale`
- `breaksd.wifihot[.]icu`
- `walter.filloco[.]icu`
- `fast.raidher[.]icu`
- `apigrokcloud[.]icu`

### Campaign 2 C2 / staging domains
- `enhanceblabber[.]cc` — C2 domain
- `deep-harborio[.]com` — first-stage payload hosting
- `auramatrixa[.]com` — first-stage payload hosting
- `zealpraxis[.]com` — first-stage payload hosting
- `prism-vertex[.]com` — first-stage payload hosting
- `prism-matrixs[.]com` — first-stage payload hosting
- `proton-network[.]com` — first-stage payload hosting
- `creativecommunityinfo[.]art` — payload hosting

## Defender heuristics
- Treat ClickFix prompts that ask users to paste/run shell commands as malware delivery, especially when command history shows `cmd.exe`, `powershell.exe`, `rundll32.exe`, `mshta.exe`, remote HTTPS paths, or `@ssl` WebDAV syntax.
- Hunt for `rundll32.exe` loading DLLs from WebDAV shares, `pushd` to remote `@ssl` paths, and `conhost.exe --headless` in user-driven command chains.
- Alert on PowerShell that creates scheduled tasks with update-looking names, clears PowerShell history, timestomps payload files, or drops bundled Python runtimes into user-writable temporary directories.
- Investigate `pythonw.exe` launched from deceptive `%LocalAppData%\Temp` application-looking folders, especially if paired with network activity, shellcode-loading behavior, or browser database access.
- Monitor for `mshta.exe` fetching remote HTA over HTTPS from user-initiated chains and for VBScript/COM launching encoded PowerShell.
- Hunt for image downloads followed by pixel/parsing routines, decryption, decompression, and in-memory API resolution; treat steganographic JPEG payload delivery as an execution signal, not a benign media fetch.
- Watch for endpoint access to browser `Login Data` / `Web Data`, DPAPI decryption bursts, PDF / Office document enumeration, OneDrive / SharePoint synced-folder collection, and archive creation preceding outbound traffic.
- If compromise is suspected, isolate before rotation, preserve endpoint telemetry, revoke browser/session tokens, rotate affected credentials, and review cloud/SaaS access from harvested sessions.

## Related pages
- [ClickFix CPaaS API-driven payload delivery](../ops/clickfix-cpaas-api-driven-payload-delivery.md)
- [REF6045 / SCMBANKER Mexican banking fraud](scmbanker.md)
- [Silent Swap Google Notes crypto clipper](../ops/silent-swap-google-notes-crypto-clipper.md)
- [ScreenConnect freeware / AsyncRAT SEO campaign](../ops/screenconnect-freeware-asyncrat-seo-campaign.md)

## Sources
- Microsoft Security Blog: [ACR Stealer: Two observed intrusion chains amid increased threat activity](https://www.microsoft.com/en-us/security/blog/2026/07/16/acr-stealer-two-observed-intrusion-chains-amid-increased-threat-activity/)
