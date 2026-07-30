# OctLurk and SilkLurk Central Asia espionage campaign

## Summary
Kaspersky GReAT reported a previously unattributed Chinese-speaking espionage operation using the tailored **OctLurk** and **SilkLurk** backdoors against government organizations, primarily in Central Asia, since January 2025. Confirmed victim countries include Afghanistan, Kyrgyzstan, Tajikistan, Uzbekistan, Kazakhstan, and Syria. The campaign combines victim-bound payload decryption, reflective in-memory loading, modular command/file/interaction plugins, credential theft, internal reconnaissance, email collection, LurkProxy tunneling, Pandora RC access, and PlugX fallback persistence.

Kaspersky assesses with medium confidence that one actor operates both backdoors and that the actor is Chinese-speaking, but it does not assign the activity to a known group. Some victims had both malware families, and OctLurk was observed delivering SilkLurk. Public infrastructure also overlaps a Linux campaign tracked by Kazakhstan's State Technical Service as TrustFall and by other vendors as MystRodX or SilentRaid; the overlap does not by itself prove that every campaign was concurrent or operated identically.

## Tags
- ops
- operations
- cyber-espionage
- Chinese-speaking
- unattributed
- Central Asia
- Afghanistan
- Kyrgyzstan
- Tajikistan
- Uzbekistan
- Kazakhstan
- Syria
- government targeting
- healthcare
- foreign affairs targeting
- law enforcement targeting
- OctLurk
- SilkLurk
- LurkProxy
- PlugX
- Pandora RC
- Fscan
- Impacket
- credential theft
- email theft
- DLL sideloading
- reflective loading
- environmental keying
- SOCKS5

## Why this matters
- Both loader families bind payload decryption to victim properties: OctLurk uses the system-drive serial number and SilkLurk hashes the computer name. Captured components may not decrypt or execute away from the intended host without preserved machine context.
- The actor maintains redundant access through two custom backdoors, LurkProxy, PlugX, Pandora RC, command-shell plugins, and stolen administrative credentials.
- OctLurk's memory-only plugins provide command execution, filesystem control, screenshots, clipboard access, and synthetic keyboard/mouse events.
- Post-compromise activity includes domain-controller hash dumping, keylogging, browser-password theft, internal scanning, email access, network-share document search, and WinRAR/7-Zip staging.
- The campaign spans ministries, foreign affairs, law enforcement, healthcare, research, logistics, urban planning, facilities management, and public education.

## Campaign and deployment chain
### OctLurk
The actor used administrative credentials to create one-shot `GoogleUpDate` scheduled tasks running as SYSTEM. Batch files such as `C:\Users\<user>\Videos\1.bat` created services including `NgcCIntSvc`, which loaded an OctLurk loader DLL such as `oleasapi.dll`. Other reported loader-service names include `specitsrc`, `cmtastsvc`, `PNRPHostSvc`, `vmictimerosync`, and `vmicagent`.

The loader double-XOR-decrypts and zlib-decompresses its configuration and payload. One key is embedded; the other derives from the `C:` drive serial number. It then reflectively injects the backdoor. OctLurk connects over TCP/443, inventories the host, and receives memory-only plugins for command-shell, file-manager, and interaction-manager functions.

### LurkProxy
The actor deployed LurkProxy through a similar obfuscated loader and a service such as `Cusrxsrv`. The observed implant listened on all interfaces on TCP/64980 and established a TLS-encrypted proprietary channel to `154.196.162[.]76`. Its static configuration selected either SOCKS5 reverse-proxy behavior or transparent forwarding; Kaspersky observed the SOCKS5 mode.

### SilkLurk
SilkLurk used legitimate NVIDIA and Realtek executables—including `nvgwls.exe`, `NetSetSvc.exe`, `RtkSmbus.exe`, and `RtkNGUI64.exe`—to sideload malicious DLLs such as `vulkan-1.dll`, `nvml.dll`, `RtkSmbusLoc.dll`, or `RtkNGUI64Loc.dll`. The loader moved a payload such as `OneDrive.dat` to a victim-specific path and created an auto-start service such as `RmSs` with restart-on-failure behavior.

SilkLurk hashes the computer name to decrypt the payload path, payload bytes, PE metadata, sections, relocations, and entry point before reflective injection. It supports up to four C2 endpoints and optional authenticated HTTP proxies. Commands can retrieve or update configuration and inject additional plugins directly into memory.

## Post-compromise activity
- Collected system, process, session, network, Defender, startup, scheduled-task, DNS-cache, certificate-cache, hardware, and event-log state through batch, PowerShell, WMIC, `wevtutil`, and native commands.
- Exported successful remote-interactive logon events and queried activity for specific users.
- Ran a packaged Impacket `secretsdump` build named `Adobe.exe` against domain controllers, then enumerated the Domain Controllers group.
- Installed a keylogger masquerading as `C:\Users\Public\Pictures\AnyDesk.exe`, persisted it through an `AnyDesk` scheduled task, and wrote keystrokes and clipboard data to `C:\Users\Public\Libraries\msect\dev0` and `dev1`.
- Used a browser-password decryptor in a user Libraries directory against Chrome `Login Data`/`Local State` and Firefox `logins.json`.
- Installed Pandora RC agents through SYSTEM tasks for secondary remote access.
- Ran Fscan as `%TEMP%\fc.exe` with password file `pp.txt` to scan internal and public SSH and MySQL services.
- Used `curl` with credentials to access email inboxes.
- Used SilkLurk shells and `net use` with administrative credentials to search shared drives for confidential documents, then disconnected and staged data with WinRAR or 7-Zip.
- Delivered PlugX through `kmsonline.exe`, sideloading `RasTls.dll` beside legitimate `RasTls.exe` and persisting as the `SymantecRAS` service.

## Public indicators
### Network
| Role | Indicators |
| --- | --- |
| OctLurk C2 | `dns.multitoconference[.]com`, `tj.tajikistandip[.]com`, `fm01.clouddevicemetrics[.]com`, `confbase.mdpsupport[.]net`, `digital.leroymerling[.]com`, `api2.annoyingremote[.]com`, `about.blsouqs[.]com`, `ssl.blsouqs[.]com`, `45.138.157[.]165` |
| LurkProxy C2 | `dns.ssentialserv[.]xyz`, `154.196.162[.]76` |
| SilkLurk / PlugX C2 | `tyhbgtyuj.gleeze[.]com`, `wedfcvbn.gleeze[.]com`, `rgnojb.casacam[.]net`, `ctyuhjerf.kozow[.]com`, `uyhvfredc.accesscam[.]org`, `gycudore.kozow[.]com`, `95.179.210[.]138`, `45.77.136[.]228`, `95.179.141[.]26`, `45.32.152[.]50`, `212.11.39[.]138`, `195.86.120[.]2`, `154.196.187[.]73`, `45.61.149[.]112`, `64.7.198[.]130` |

### Representative MD5 hashes
| Artifact | MD5 |
| --- | --- |
| OctLurk loader `oleasapi.dll` | `082d49ef9f14e6811d68c7e0e82e5069` |
| OctLurk loader `msbasesysdc.dll` | `f4578e869a735cfad691f927bae3e638` |
| OctLurk backdoor | `a0cc7accc79abb0287aaba825d0351f0` |
| SilkLurk loader `vulkan-1.dll` | `8269d6ba1b6842f9152c90cf7add9b93` |
| PlugX dropper `kmsonline.exe` | `3c9a1ba8e0c7475706adc6376e9d7b7c` |
| PlugX loader `RasTls.dll` | `ef59aad625eebda8650aec5820d6ce69` |
| Packaged Impacket `Adobe.exe` | `32a5985543433a4f60da2fafd873b927` |
| Keylogger `AnyDesk.exe` | `2a571f6cee42a17d873f4c942649813f` |
| Browser stealer | `37dc84e4bcad92fa28f1e7778d088283` |
| Fscan `fc.exe` | `cf903e4a1629aa0582fd0363b5786676` |

## Defender heuristics
- Preserve the original host's computer name and system-drive serial number during triage. Acquire memory before shutdown where practical because backdoors and plugins are reflectively injected and victim-bound.
- Hunt for one-shot SYSTEM tasks named `GoogleUpDate`, suspicious services with `ServiceMain` DLL exports, and uncommon service names loading DLLs from System32, ProgramData, user media, or vendor-lookalike directories.
- Detect legitimate NVIDIA, Realtek, and Symantec binaries loading adjacent `vulkan-1.dll`, `nvml.dll`, `RtkSmbusLoc.dll`, `RtkNGUI64Loc.dll`, or `RasTls.dll` outside expected signed installation paths.
- Alert on inbound listening TCP/64980 combined with outbound TLS to the LurkProxy infrastructure and lateral internal connections from the same process.
- Review domain-controller access for `secretsdump` behavior, remote scheduled-task creation, service installation, and immediate Domain Controllers group enumeration.
- Hunt the `AnyDesk.exe`/`dev0`/`dev1` keylogger path cluster, but distinguish it from legitimate AnyDesk by signer, path, hash, process behavior, and scheduled-task command.
- Review `net use` access followed by recursive document discovery, share disconnection, and WinRAR/7-Zip execution from `Libraries` or `C:\windows\vss`.
- If a loader is found, treat decryption failure in a sandbox as a reason to preserve victim context—not evidence that the file is benign.
- Rotate domain, email, browser, and administrative credentials after containment; remove redundant backdoors and remote agents through a trusted rebuild where compromise scope is uncertain.

## Attribution notes
Kaspersky assesses with medium confidence that OctLurk and SilkLurk share one Chinese-speaking operator. Evidence includes co-infection, shared staging directories, OctLurk delivering SilkLurk, related infrastructure, and SilkLurk delivering PlugX. The operation remains unattributed to a named group. Three OctLurk/LurkProxy servers overlap the Kazakhstan STS TrustFall/MystRodX/SilentRaid Linux campaign; treat this as an infrastructure pivot, not conclusive actor equivalence.

## Related pages
- [OctLurk](../tools/octlurk.md)
- [SilkLurk](../tools/silklurk.md)
- [LurkProxy](../tools/lurkproxy.md)
- [GoSerpent Southeast Asia espionage](goserpent-southeast-asia-espionage-campaign.md)
- [Mirage Kitten NightLedger, BridgeHead, and ArcBridge](mirage-kitten-nightledger-bridgehead-arcbridge.md)

## Sources
- Kaspersky GReAT: [https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/](https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/)
