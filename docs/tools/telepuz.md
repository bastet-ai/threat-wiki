# TELEPUZ

## Summary
Elastic Security Labs reported on July 16, 2026 that **TELEPUZ** is an emerging modular Windows malware family distributed through a **ClickFix → VIDAR** chain since late April 2026. Elastic describes it as lightweight, full-featured, fast-evolving, and likely malware-as-a-service based on the volume and pace of builds submitted to VirusTotal.

The durable defender point: TELEPUZ is not just another loader payload. It combines Windows service persistence, anti-analysis checks, indirect syscalls, WebSocket C2, decentralized fallback C2 resolution through Telegram / Steam / DNS / Polygon, and downloadable keylogger, stealer, web-injector, and Chrome-cookie modules.

## Tags
- tools
- malware
- MaaS
- Windows malware
- ClickFix
- VIDAR
- modular malware
- WebSocket C2
- Telegram dead drop
- Steam profile dead drop
- DNS dead drop
- Polygon blockchain dead drop
- keylogger
- stealer
- web injector
- browser credential theft
- Chrome DevTools Protocol
- Firefox WebDriver BiDi
- Chrome App-Bound Encryption
- indirect syscalls
- AMSI bypass
- ETW bypass
- service persistence
- Elastic Security Labs

## Execution and persistence
- TELEPUZ is delivered as a 64-bit Windows DLL with exports chosen to look like legitimate software.
- The malware re-executes through `rundll32.exe` when needed, migrates from `%TEMP%` into configured install / persistence directories, and creates the mutex `cfgmgr_mtx` in analyzed samples.
- Anti-analysis checks terminate execution for low-resource virtualized-looking systems, common sandbox usernames / hostnames, known hypervisor display devices, and CIS-region locale identifiers.
- Evasion includes mapping a clean copy of NTDLL for unhooking, patching `AmsiScanBuffer` to return `E_INVALIDARG`, and patching ETW functions including `EtwEventWrite`, `NtTraceEvent`, and `NtTraceEventControl`.
- Privilege escalation attempts use the COM elevation moniker technique, then the malware can register itself as a Windows service. Elastic observed service names such as `CipherAllocator` and `PilotmasterMast`.

## C2 and fallback control
TELEPUZ stores one primary C2 domain and tries to contact it up to ten times. If that fails, it retrieves fallback C2 data through four public-resource methods:

| Method | Elastic-reported pivot |
| --- | --- |
| Telegram profile | `t[.]me/chanadarkpart`, XOR-encrypted with key `Goodman`, decrypted to `cal.snehamumbai[.]org`. |
| Steam profile | `steamcommunity[.]com//profiles/76561199705801219`; profile-name history showed both `cal.joycedoula[.]com[.]br` and fallback C2 data. |
| DNS record | Query for `codebasecode[.]com`; Elastic had not found an associated record at publication time. |
| Polygon smart contract | Contract `0xf55Bea1FdCf1c3ABb39ab92567C09aC1BFf6753E`, method selector `0xc3f909d4`, decrypting `h=cal.snehamumbai[.]org|p=443|ssl=1` with an AES-256-CBC key. |

After resolving a C2, TELEPUZ uses WebSockets over optional TLS. The WebSocket path is `/cdn/health?sid=<victim-id>`, and Elastic reports the malware implements TCP / HTTP / WebSocket handling manually rather than relying on standard high-level internet libraries.

## Commands and modules
Elastic recovered 36 command hashes. Capability areas include beaconing, file upload/download, ZIP creation, deletion, command execution, process listing, drive enumeration, screenshot capture, privilege elevation, token theft/reversion, process migration, module execution, malware update, and job control.

Downloaded modules keep the core implant small:

| Module | Default path |
| --- | --- |
| KeyLogger | `/static/modules/kMP6HBGEA8.bin` |
| WebInjector | `/static/modules/yaVaoS3Bw.bin` |
| Stealer | `/static/modules/W2UMxylgG_.bin` |
| Chrome-cookie extractor | `/static/assets/chromelevator.bin` |

The Chrome-cookie extractor is tied to the public Chrome App-Bound Encryption decryption tooling pattern. The WebInjector module can communicate through TELEPUZ or connect directly to C2 at `/ws/inject?cid=<id>`. Elastic reports it targets Chromium-based browsers through the Chrome DevTools Protocol and Firefox through WebDriver BiDi, with default behavior oriented toward manipulating or intercepting financial-form fields such as IBAN values.

## Indicators reported by Elastic
### C2 / fallback infrastructure
- `cal.joycedoula[.]com[.]br` — present in earliest sample configurations.
- `cal.snehamumbai[.]org` — latest C2 and fallback value recovered from Telegram / Polygon paths.
- `t[.]me/chanadarkpart` — Telegram fallback profile.
- `steamcommunity[.]com//profiles/76561199705801219` — Steam fallback profile.
- `codebasecode[.]com` — DNS fallback query target.
- Polygon contract `0xf55Bea1FdCf1c3ABb39ab92567C09aC1BFf6753E`, selector `0xc3f909d4`.

### Sample and module hashes
- `58aec6e3835aaf20f7b4a7e308b36a19e7454673a6f71783871e9bcf6cae8eed` — reference TELEPUZ main payload.
- `bf3b4e645a3c0c23f87c55971069014f7424ad14497371ee7567eff68ffaf343` — TELEPUZ main payload.
- `ff791fe1532a2dc3b3c188a71bfd0177f973ef228e4d1dda1db6d3c4b0d62b3e` — TELEPUZ main payload.
- `a955d7e2819d5fa8b5f879cb970e1a1a91327098a7383f2a03a5e1e7e19435e3` — keylogger module.
- `9733a3f6409de81271f21993c7f8b9865ac9f5c68c3d4336e91afe6b312477eb` — stealer module.
- `444f1c0c82b3f6cc31d685bac68b20edbde5722ce219af9cceab0c2a6537efc1` — web-injector module.

### Host artifacts
- Mutexes: `cfgmgr_mtx`, `bginfod_mtx`, `wfj64_mtx`.
- Persistence paths: `%AppData%\Local\DCFG\Runtime\Themes\Processor\etwhost.dll`, `%AppData%\Roaming\StateRepository\Host\Recovery\systemreset.dll`, `%AppData%\Local\MiravaDevices\noraxrecovery.dll`.
- Install paths: `%ProgramData%\XeroxPrint\Temp\Worker\grpeng.dll`, `%ProgramData%\Jundrax\Tracker\IrenScanner.dll`, `%ProgramData%\QualcommRF\dsp_agent.dll`.
- Registry service keys: `HKLM\SYSTEM\CurrentControlSet\Services\CipherAllocator`, `HKLM\SYSTEM\CurrentControlSet\Services\PilotmasterMast`.

## Defender heuristics
- Treat ClickFix prompts that download from `memshowblob[.]forum` or similar one-command PowerShell chains as potential VIDAR / TELEPUZ delivery.
- Hunt for VIDAR second-stage execution followed by `install.exe` / `telepuz.dll` retrieval from staging domains and `rundll32.exe` loading user-writable DLLs.
- Alert on user-context DLLs that create `cfgmgr_mtx`, patch AMSI/ETW, unhook NTDLL, or register services under update / allocator / print / device-looking names.
- Monitor for WebSocket connections to `/cdn/health?sid=` and module paths under `/static/modules/` or `/static/assets/chromelevator.bin`.
- Block or investigate endpoints that query TELEPUZ fallback channels from workstations: Telegram profile lookups, the Steam profile, `codebasecode[.]com`, or Polygon `eth_call` traffic to the reported contract.
- Browser-defense teams should watch for abnormal Chrome DevTools Protocol or Firefox WebDriver BiDi use from non-browser automation processes, especially if followed by form-field changes, cookie extraction, or financial-data manipulation.

## Related pages
- [TELEPUZ ClickFix / VIDAR campaign](../ops/telepuz-clickfix-vidar-campaign.md)
- [ACR Stealer](acr-stealer.md)
- [ClickFix CPaaS API-driven payload delivery](../ops/clickfix-cpaas-api-driven-payload-delivery.md)
- [Vidar / XMRig Factory-v3 malvertising campaign](../ops/vidar-xmrig-factory-v3-malvertising-campaign.md)

## Sources
- Elastic Security Labs: [TELEPUZ: a modular MaaS malware spreading via CLICKFIX-VIDAR chains](https://www.elastic.co/security-labs/telepuz-maas-malware-clickfix)
