# StealC / Amadey infrastructure disruption

## Summary
Microsoft Threat Intelligence, Microsoft Defender Security Research, and Microsoft's Digital Crimes Unit reported a June 24, 2026 disruption of StealC and Amadey infrastructure. Microsoft says DCU worked with Europol and industry partners to take down, suspend, block, or notify providers for more than 200 malicious command-and-control domains and IP addresses used by the StealC infostealer and Amadey malware-as-a-service loader.

Treat this as both malware-family reference and intrusion-prevention guidance. The durable lesson is that commodity infostealer infections on unmanaged or personal devices can become enterprise compromise when stolen VPN, SSO, cloud, email, browser-cookie, and session-token material is later sold or reused by access brokers, ransomware operators, or other criminals.

## Tags
- ops
- operations
- malware
- infostealer
- loader
- malware-as-a-service
- credential theft
- browser cookie theft
- session token theft
- StealC
- Amadey
- Microsoft Digital Crimes Unit
- Europol
- infrastructure disruption
- access brokers
- ransomware enablement
- ClickFix
- SEO poisoning
- malvertising
- PowerShell
- MSI
- rundll32
- scheduled task
- RC4
- App-Bound Encryption bypass

## Why this matters
- StealC and Amadey are commodity services, but the downstream impact is enterprise-grade: stolen logs can include corporate VPN credentials, SSO tokens, session cookies, cloud accounts, and email access.
- The initial infection often starts outside managed endpoints, so identity telemetry may be the first enterprise signal.
- Microsoft highlights a consistent monetization path: stealer logs are sold, validated, and reused for account takeover, fraud, data theft, or ransomware.
- The disruption reduces exposed infrastructure, but defenders should not treat it as cleanup for already-stolen credentials or session material.

## Reported ecosystem path
1. Delivery begins through scalable user-driven lures such as SEO poisoning, malvertising, fake or cracked software, game cheats, phishing, or ClickFix-style pages that trick users into pasting commands into Windows Run or a terminal.
2. A loader such as Amadey establishes execution, persistence, C2 communication, and optional plugin or follow-on payload delivery.
3. StealC or another infostealer harvests browser secrets, session cookies, wallet data, application credentials, files, screenshots, and host context.
4. Stolen logs are exfiltrated to attacker-controlled panels and then used directly or sold through access-broker markets.
5. Enterprise impact may happen hours, days, or months later when valid credentials, session cookies, or SSO material are reused against corporate services.

## StealC behavior highlighted by Microsoft
- Malware-as-a-service stealer written in C++ with a builder and centralized panel for customized payloads and stolen-data management.
- Collects browser passwords and cookies, cryptocurrency wallet and extension data, messaging-application data, email-client credentials, Steam session data, screenshots, and configured file grabs.
- Performs host fingerprinting and language checks; Microsoft reports termination behavior when the default language matches Russian, Ukrainian, Belarusian, Kazakh, or Uzbek.
- Registers to C2 with an RC4-encrypted, Base64-encoded HTTP POST containing request type, hardware ID, and build ID.
- Receives JSON configuration that can enable browser targets, file-grab rules, screenshots, loader execution, Steam theft, Outlook theft, Foxmail theft, WinSCP theft, and self-deletion.
- Uses process injection into a suspended sacrificial process to bypass Chromium App-Bound Encryption, then writes decrypted output to an IPC file under `C:\ProgramData\<HWID>.txt` before exfiltration and cleanup.
- Supports follow-on payload execution from C2 as `.exe` downloads, silent MSI installation through `msiexec.exe /i ... /passive`, or PowerShell download-and-execute cradles.
- Sends stolen material in individual RC4-encrypted and Base64-encoded HTTP POST requests.

## Amadey behavior highlighted by Microsoft
- Active since at least 2018 and used as a malware-as-a-service loader for StealC, Lumma Stealer, RATs, cryptominers, and sometimes ransomware.
- Communicates with C2 over HTTP, uses embedded RC4 configuration keys, and supports file download, DLL execution, command execution, self-update, self-uninstall, SOCKS proxying, screenshot capture, and plugin delivery.
- Microsoft reports default copy / persistence paths such as `C:\Users\<user>\e079729711\nudwee.exe` on Windows 10 / 11 or `%TEMP%\e079729711\nudwee.exe` on other systems, followed by scheduled-task persistence.
- Checks keyboard layout IDs for Russian, Ukrainian, and Belarusian before some functionality.
- Runtime plugins include `cred.dll` for credential theft and `clip.dll` for clipboard theft, loaded through `rundll32.exe` from C2 `/Plugins/` paths.
- Backdoor commands include EXE / DLL / MSI drops, PowerShell script execution, process injection, elevated `cmd.exe`, RDP enablement, hidden administrator creation, VNC / remote-access component installation, and SOCKS proxy start / stop.

## Defender heuristics
### Identity and credential response
- Treat confirmed StealC, Amadey, or related infostealer execution as a credential incident, not just endpoint malware.
- Rotate passwords and revoke sessions for browser-saved corporate accounts, VPN, SSO, email, cloud, Git, registry, and remote-access services used from the host.
- Review sign-ins from unmanaged devices, unusual geographies, new user agents, stale session cookies, token reuse after password reset, and successful logins that follow bursts of failed attempts.
- Preserve host and identity evidence before broad cleanup when ransomware or data-theft follow-on activity is possible.

### Endpoint hunting
- Hunt for ClickFix-style command execution: browsers or document viewers leading users to paste PowerShell, `mshta`, `cmd`, `curl`, `iwr`, or `iex` commands.
- Investigate unusual scheduled tasks launching from user-writable directories such as `%TEMP%`, `%APPDATA%`, `%USERPROFILE%`, or paths resembling `C:\Users\<user>\e079729711`.
- Look for `rundll32.exe` loading unexpected `cred.dll` or `clip.dll` from downloaded or user-writable paths.
- Alert on PowerShell download cradles, silent `msiexec.exe` installs from suspicious locations, and unknown executables shortly after browser-download, cracked-software, game-cheat, or fake-utility activity.
- Search for short-lived IPC artifacts under `C:\ProgramData\<hardware-id>.txt` and suspicious suspended-process injection sequences using `CreateProcessA`, `VirtualAllocEx`, `WriteProcessMemory`, `QueueUserAPC`, and `ResumeThread` patterns where EDR telemetry supports it.
- Review unexpected RDP enablement, firewall-rule changes for Terminal Services, hidden local administrator creation, and VNC component drops after loader execution.

### Infrastructure disruption follow-up
- Do not rely on domain takedown as remediation for already-exfiltrated logs.
- Re-scan previously infected or exposed endpoints for alternate C2, new loader plugins, and second-stage malware installed before the disruption.
- If using Microsoft Defender or another EDR, correlate detections for StealC / Amadey with identity-risk events and downstream access-broker or ransomware-linked behavior.

## Related pages
- [Crypto Clipper Tor / USB worm](crypto-clipper-tor-usb-worm.md)
- [FortiClient EMS CVE-2026-35616 EKZ Infostealer campaign](forticlient-ems-cve-2026-35616-ekz-infostealer.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [Operation Endgame SocGholish disruption](operation-endgame-socgholish-disruption.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/06/24/stealc-and-amadey-breaking-down-infostealers-and-the-cybercrime-services-that-deliver-them/>
