# StrikeShark SharkLoader / Cobalt Strike campaign

## Summary
Kaspersky reported `StrikeShark` in June 2026 after investigating SharkLoader infections that began with a diplomatic organization in Indonesia and expanded across government, software-development, and other targets in multiple countries.

The durable defender lesson is the combination of old internet-facing application exploitation, custom droppers disguised as legitimate software or PDFs, DLL sideloading through copied Windows binaries, and in-memory Cobalt Strike Beacon execution. Kaspersky did not attribute the activity to a known APT or cybercrime group.

## Tags
- ops
- malware
- SharkLoader
- Cobalt Strike
- DLL sideloading
- web shells
- edge exploitation
- scheduled tasks
- Windows

## Reported intrusion shape
- Initial access included exploitation of internet-facing applications and network appliances, plus custom droppers masquerading as legitimate applications.
- Kaspersky observed Microsoft Exchange exploitation including `CVE-2021-26855` in an Indonesian diplomatic-entity incident, Openfire `CVE-2023-32315` in Taiwan software-development compromises, and GeoServer `CVE-2024-36401` in a Colombian incident.
- Kaspersky also listed activity involving older or widely exploited public-facing vulnerabilities in Apache Shiro, Hikvision products, Microsoft SharePoint, Zimbra Collaboration Suite, Microsoft Exchange Server, F5 BIG-IP, Fortinet FortiOS, React Server Components, and Cisco IOS XE Web UI.
- Post-exploitation activity included web-shell use, command execution, copying legitimate Windows binaries such as `SystemSettings.exe`, and launching sideloading chains from directories such as `C:\ProgramData\` or application-data paths.
- Separate droppers used lures such as a Cisco AnyConnect installer, Google Update-themed binaries, or decoy PDF documents while silently placing SharkLoader components.

## SharkLoader execution chain
Kaspersky described SharkLoader as a multi-component loader for Cobalt Strike Beacon:

- A legitimate executable such as `SystemSettings.exe` is copied into the malware working directory.
- A malicious DLL such as `SystemSettings.dll` is placed beside it for DLL sideloading. Kaspersky also observed variants using side-loading targets such as `msedge.dll`, `PrintDialog.dll`, and `miracastview.dll`.
- Encrypted modules such as `DscCoreR.mui` and `SyncRes.dat` are stored beside the loader. Observed working directories included `%APPDATA%\xwreg` and `%APPDATA%\xgdf`.
- `DscCoreR.mui` is Blowfish-decrypted and reflectively loaded; it then decrypts and loads `SyncRes.dat`.
- `SyncRes.dat` installs Microsoft Detours-based API hooks. The loader also uses MinHook to hook `VirtualAlloc` and `Sleep` around Cobalt Strike Beacon execution.
- The final Cobalt Strike Beacon shellcode is decompressed and executed in memory from a suspended thread.

Kaspersky highlighted SharkLoader's use of a `Perfect DLL Hijacking` technique: the loader manipulates Windows loader-lock state from `DllMain` before creating a malicious thread, reducing the deadlock risk that normally comes from thread creation during DLL initialization.

## Persistence and post-compromise activity
Reported persistence and follow-on behavior included:

- Dropper-created scheduled tasks that immediately and repeatedly launched the copied `SystemSettings.exe` from the malware working directory.
- A registry Run key named `MFUpdate` launching `%APPDATA%\Identities\SystemSettings.exe` in one Hong Kong incident.
- A daily scheduled task named `\Microsoft\Windows\Edge\Edgeupdate` executing `C:\ADriveLogs_Logs\SystemSettings.exe /F` as `SYSTEM` in the Indonesian diplomatic-entity incident.
- Active Directory enumeration through Cobalt Strike and web-shell access.

## Victimology and attribution
Kaspersky said related activity affected a diplomatic organization in Indonesia, government organizations in Taiwan, software-development companies across multiple countries, and entities in Hong Kong, Lebanon, Syria, Colombia, North Macedonia, Nepal, Serbia, and other locations.

Attribution remains unset. Kaspersky noted open-source post-compromise tools associated with Chinese-speaking developers but said it found no direct code reuse, infrastructure overlap, or operational similarity sufficient to connect SharkLoader / StrikeShark to a known actor.

## Defender notes
- Patch and exposure-reduce legacy internet-facing application stacks before investigating SharkLoader-specific artifacts; many listed initial-access paths are old public-exploit surfaces.
- Hunt for copied legitimate Windows binaries such as `SystemSettings.exe` outside normal Windows directories, especially under `C:\ProgramData\`, `%APPDATA%`, `C:\ADriveLogs_Logs\`, or security-vendor-themed directories.
- Hunt for sibling files such as `SystemSettings.dll`, `DscCoreR.mui`, `SyncRes.dat`, and `SyncRest.dat` near copied legitimate binaries.
- Review scheduled tasks named like `\Microsoft\Windows\Edge\Edgeupdate` or high-frequency newly created tasks executing copied Windows binaries from user-writable paths.
- Review `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` values such as `MFUpdate` that launch copied Windows binaries from `%APPDATA%`.
- Treat web-shell traces, SharkLoader artifacts, and Cobalt Strike telemetry as one intrusion chain: preserve server evidence before rebuilding, and scope Active Directory enumeration and credential exposure.
- Do not collapse this campaign into a named China-linked actor without additional sourcing; keep attribution separate from tool-language or public-tool provenance.

## Sources
- Kaspersky Securelist, StrikeShark / SharkLoader campaign: [https://securelist.com/strikeshark-campaign/120326/](https://securelist.com/strikeshark-campaign/120326/)
