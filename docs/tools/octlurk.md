# OctLurk

## Summary
**OctLurk** is a heavily obfuscated, modular Windows backdoor reported by Kaspersky GReAT in a Chinese-speaking but unattributed espionage campaign against government organizations in Central Asia and nearby countries. Its loader binds payload decryption to the victim's `C:` drive serial number, decompresses the payload with zlib, and reflectively injects the backdoor. C2-delivered memory-only plugins provide command-shell, file-management, and interactive desktop control.

## Tags
- tools
- malware
- backdoor
- OctLurk
- Windows
- in-memory malware
- reflective loading
- environmental keying
- drive serial number
- zlib
- XOR
- modular malware
- cyber-espionage

## Capabilities
- Collects OS, computer, user, hostname, local IP, and local-time information.
- Uses TCP/443 with double-XOR and zlib-protected proprietary messages.
- Receives commands or plugin code from C2 and injects plugins into memory.
- Command-shell plugin launches `cmd.exe`, executes commands, and returns output.
- File-manager plugin enumerates volumes and files; searches, reads, writes, copies, moves, renames, deletes, creates directories, changes attributes, and sets timestamps.
- Interaction plugin captures screenshots and clipboard data and synthesizes mouse and keyboard input.
- Served as a foothold for credential dumping, keylogging, browser-password theft, internal scanning, email access, Pandora RC deployment, LurkProxy, and SilkLurk delivery in the reported campaign.

## Loading and persistence
Observed deployment used administrative credentials and a one-shot `GoogleUpDate` scheduled task running as SYSTEM. Batch scripts created services such as `NgcCIntSvc` that loaded a DLL like `oleasapi.dll` and invoked its `RegisterService` export. Other reported service names include `specitsrc`, `cmtastsvc`, `PNRPHostSvc`, `vmictimerosync`, and `vmicagent`.

The loader double-XOR-decrypts and zlib-decompresses the payload path and bytes. One XOR key is hard-coded; the other derives from the system-drive serial number. Preserve that host property when analyzing captured loaders.

## Public indicators
- C2: `dns.multitoconference[.]com`, `tj.tajikistandip[.]com`, `fm01.clouddevicemetrics[.]com`, `confbase.mdpsupport[.]net`, `digital.leroymerling[.]com`, `api2.annoyingremote[.]com`, `about.blsouqs[.]com`, `ssl.blsouqs[.]com`, `45.138.157[.]165`.
- Loader MD5s: `082d49ef9f14e6811d68c7e0e82e5069`, `f4578e869a735cfad691f927bae3e638`, `7c2f64461bb519c6cbf1fc687675514c`.
- Backdoor MD5: `a0cc7accc79abb0287aaba825d0351f0`.
- Plugin MD5s: file manager `a56cce62930a6bee80d679b4c495a340`; command shell `1415a78b75de7db4ba3d1e61d7db4501`; interaction manager `a4d550a3ba0cd073fe3839b99d98a7a8`.
- Representative paths: `C:\Windows\System32\oleasapi.dll`, `C:\Windows\System32\msbasesysdc.dll`, and `C:\Windows\Media\Welcome01.wav`.

## Defender notes
- Acquire memory and preserve the drive serial before changing or rebuilding the host.
- Hunt for SYSTEM scheduled tasks named `GoogleUpDate`, service DLLs exporting `RegisterService`/`Refresh`, and services that load unsigned DLLs from unusual paths.
- Correlate TCP/443 to the public C2 set with service-created processes, reflective-memory indicators, `cmd.exe`, screenshots, clipboard access, or synthetic input.
- Scope beyond the loader: investigate domain-controller access, browser and email credentials, remote agents, internal scanning, proxy deployment, and SilkLurk co-infection.

## Related pages
- [OctLurk and SilkLurk Central Asia espionage campaign](../ops/octlurk-silklurk-central-asia-espionage.md)
- [SilkLurk](silklurk.md)
- [LurkProxy](lurkproxy.md)

## Sources
- Kaspersky GReAT: [https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/](https://securelist.com/octlurk-silklurk-backdoors-central-asia/120840/)
