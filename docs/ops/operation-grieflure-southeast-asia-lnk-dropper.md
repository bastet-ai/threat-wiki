# Operation GriefLure Southeast Asia LNK dropper

## Summary
Seqrite Labs reported **Operation GriefLure**, a targeted spear-phishing campaign against senior executives at Viettel Group in Vietnam and St. Luke's Medical Center Quezon in the Philippines, with investigative context tied to Thanh Hoa Provincial Cyber Crime Police. The campaign used authentic, legally sensitive decoy material, nested archives, Windows LNK files, `ftp.exe` as a living-off-the-land dropper, and staged payload assembly from `.doc` chunks.

Seqrite assesses the activity with **moderate-to-high confidence** as a China-nexus threat cluster based on infrastructure, targeting, China-specific security-product enumeration, and WeChat data targeting. Treat that as a vendor assessment, not a confirmed public actor identity.

## Tags
- ops
- operations
- espionage
- Southeast Asia
- Vietnam
- Philippines
- telecom
- healthcare
- spear-phishing
- LNK
- living-off-the-land
- ftp.exe
- DLL sideloading
- process injection
- credential-theft
- China-nexus

## Why this matters
- The lure documents were not generic: Seqrite says the actor harvested genuine legal and investigative documents, increasing credibility and reducing the value of simple awareness training.
- The initial execution chain blends into Windows-native behavior: LNK launches `ftp.exe -s`, a batch script reconstructs payloads with `copy /b`, and the final binaries are assembled only on disk at runtime.
- The implant stack combines loader flexibility, fileless execution, process injection into `explorer.exe`, C2 over HTTPS, screenshot capture, directory reconnaissance, file upload/execution, and credential harvesting.
- The targets — a military-linked telecom operator and a healthcare provider — make the campaign durable for defenders tracking Southeast Asia-focused espionage.

## Reported targeting
- **Campaign 1:** Vietnam, network and telecommunications sector; Seqrite names Viettel Group, which operates under Vietnam's Ministry of National Defence.
- **Campaign 2:** Philippines, healthcare and medical sector; Seqrite names St. Luke's Medical Center Quezon.
- Seqrite says the lures also referenced active investigators from Thanh Hoa Provincial Cyber Crime Police.

## Reported chain

### Archive and lure staging
- The Vietnam-themed package used `Ho so.rar`, a nested archive, PDF decoy documents, and a batch file.
- The Philippines-themed package used `download.zip` with a folder named `Whistleblowing_Report_SLMC_Fraud_and_Misconduct_2026`, a decoy PDF, supporting `doc` and `_rels` directories, and a suspicious batch file.
- Seqrite says both campaigns share the same second-stage LNK and batch logic.

### LNK and `ftp.exe` execution
- The LNK abuses Windows `ftp.exe` with the `-s` flag to run a hidden script.
- The script drops content under `C:\Users\Public`, opens a decoy `1.pdf`, and completes the visible-to-invisible compromise flow in under 10 seconds according to Seqrite.
- Binary chunks disguised as `.doc` files are concatenated into payload files only at runtime, reducing static archive-detection opportunities.

### Runtime payload assembly
- The batch logic uses `copy /b` to combine `header.doc` with `WindowsSecurity.doc` and produce `sfsvc.exe`.
- It separately combines the PE header with a time-selected polymorphic chunk such as `%TIME:~4,1%.doc` plus a random value to generate a uniquely hashed `360.dll` loader on each execution.
- The assembled files are placed under `C:\Users\Public\Update\`, giving them a service-like appearance during quick triage.

### `sfsvc.exe` and `360.dll`
- Seqrite describes `sfsvc.exe` as a custom `regsvr32.exe`-like execution framework that can call DLL exports, register or unregister components, manipulate system paths for persistence, restart the Windows shell, and adjust execution privileges.
- The observed command path launches `sfsvc.exe /calldll 360.%TIME:~4,1%.dll DllRegisterServer` minimized through `cmd.exe`.
- `360.dll` is a multi-stage shellcode loader: it performs anti-analysis checks, decodes hidden payload data, allocates executable memory, runs shellcode in memory, spawns `explorer.exe`, writes payload bytes into it, and starts execution with `CreateRemoteThread`.
- Seqrite also observed additional payload execution via APC injection, remote-thread injection, and an NTFS Alternate Data Stream path like `C:\Users\Public\Update:2.dll`.

### C2 and post-exploitation functions
- The malware uses WinHTTP over HTTPS to a hardcoded server masquerading as a legitimate-looking domain; Seqrite highlights `www.whatsappcenter[.]com`.
- Request payloads and received C2 data are XOR-obfuscated, including a static `0xBB` key in the network handler.
- Reported capabilities include screenshot capture and exfiltration, directory listing and file metadata exfiltration, chunked file upload, conditional payload execution, and secondary remote-control launch behavior such as `tvnserver.exe -controlapp -connect <C2>`.

### Credential and data theft
Seqrite says the malware searches for:

- Browser credential stores, cookies, history, and local state.
- FileZilla configuration.
- PL/SQL Developer preferences.
- Sunlogin and ToDesk remote-access configuration.
- NetSarang Xshell session files.
- WeChat data under user document directories.
- Installed security products through process enumeration, including global AV/EDR tools and China-based products such as 360Safe, Qianxin, and Sangfor.

## Defender notes
- Hunt for LNK launches of `ftp.exe -s`, especially when followed by file writes under `C:\Users\Public\Update\`.
- Review archives containing LNK files plus `.doc` fragments, especially when a decoy PDF opens at the same time as background command execution.
- Search for unexpected `sfsvc.exe`, `360*.dll`, `header.doc`, `WindowsSecurity.doc`, and `C:\Users\Public\Update:2.dll` artifacts.
- Alert on `sfsvc.exe /calldll ... DllRegisterServer`, nonstandard `regsvr32`-like loaders, and `explorer.exe` process injection from recently assembled binaries.
- Inspect outbound HTTPS to `whatsappcenter[.]com` and related domains from endpoints that opened investigation, legal, telecom, or healthcare-themed archives.
- Treat impacted hosts as credential-compromise cases: browser stores, SSH sessions, remote-access tools, database tools, and WeChat data are all in scope.

## Attribution notes
- Seqrite links the campaign to a China-nexus cluster with moderate-to-high confidence.
- The public report does not establish a stable named group profile, so this page tracks the operation rather than creating a separate actor page.

## Sources
- Seqrite Labs — Operation GriefLure: Dissecting an APT Campaign Targeting Vietnam's Military Telecom & Philippine Healthcare: https://www.seqrite.com/blog/operation-grieflure-dissecting-an-apt-campaign-targeting-vietnams-military-telecom-philippine-healthcare/
