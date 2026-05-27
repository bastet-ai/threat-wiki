# DAEMON Tools Lite supply-chain compromise

## Summary
Kaspersky reported that official DAEMON Tools Lite installers distributed from the legitimate DAEMON Tools website were trojanized from about April 8 through May 5, 2026. The affected Windows versions were reported as `12.5.0.2421` through `12.5.0.2434`, with malicious code added to signed binaries inside the installation directory.

Disc Soft / DAEMON Tools acknowledged unauthorized interference in its infrastructure, removed affected files, rebuilt and validated installation packages, and released DAEMON Tools Lite `12.6.0.2445` on May 5. CISA added **CVE-2026-8398** to the Known Exploited Vulnerabilities catalog on May 27, 2026 with a May 30 remediation due date for covered agencies.

## Tags
- ops
- operations
- supply-chain
- signed-binary
- backdoor
- RAT
- credential-theft
- C2
- Windows
- active-exploitation

## Why this matters
- The compromised installers came from the legitimate vendor distribution channel and the modified binaries were signed with the vendor's code-signing certificate.
- DAEMON Tools is consumer and enterprise-adjacent disk-image software, making the incident a broad trusted-software compromise rather than a narrow targeted installer lure.
- Kaspersky telemetry saw several thousand attempted infections across more than 100 countries, while later-stage payloads were deployed to a much smaller set of hosts in retail, scientific, government, manufacturing, and education environments.
- CISA KEV listing turns this from historical research into an active-exploitation response item for organizations that inventory or allow the product.

## Reported compromise chain
1. Attackers gained unauthorized access to DAEMON Tools build or distribution infrastructure.
2. Official DAEMON Tools Lite installers for versions `12.5.0.2421` through `12.5.0.2434` were distributed in a compromised state from the legitimate website.
3. Three signed binaries were reported as trojanized: `DTHelper.exe`, `DiscSoftBusServiceLite.exe`, and `DTShellHlp.exe`.
4. At startup, the implanted code sent GET requests to the typosquatted C2 domain `env-check.daemontools[.]cc` with the full computer name.
5. The C2 could return shell commands that used PowerShell to download and execute follow-on payloads from `38.180.107[.]76`.
6. Most observed infections received an environment / information collector; only a smaller subset received additional backdoors, suggesting victim profiling and selective tasking.

## Payloads and tradecraft
Kaspersky described three major payload layers:

- **Information collector:** a .NET payload (`envchk.exe`, SHA1 `2d4eb55b01f59c62c6de9aacba9b47267d398fe4`) collected MAC address, hostname, DNS domain, running processes, installed software, and system locale, then posted the data to attacker infrastructure.
- **Minimalistic backdoor:** downloaded loader and encrypted shellcode components, used RC4 decryption, and supported file download, shell-command execution, and in-memory shellcode execution. Kaspersky noted typos in some manually issued deployment commands, such as `chiper` and a missing `c` in `crypto.dll`.
- **QUIC RAT:** a more complex C++ implant observed against one Russian educational institution, with control-flow flattening, static WolfSSL linkage, embedded `msquic.dll`, support for HTTP, UDP, TCP, WSS, QUIC, DNS, and HTTP/3 C2, and process injection into `notepad.exe` and `conhost.exe`.

Kaspersky identified Chinese-language strings in the information collector and other artifacts suggesting a Chinese-speaking operator, but did not attribute the campaign to a named actor.

## Defender heuristics
- Inventory DAEMON Tools Lite installations and installer downloads around April 8 to May 5, 2026; prioritize versions `12.5.0.2421` through `12.5.0.2434` and the vendor-noted affected free `12.5.1` build.
- Treat affected installs as endpoint compromise candidates, not merely as vulnerable software requiring an upgrade.
- Hunt for signed DAEMON Tools binaries `DTHelper.exe`, `DiscSoftBusServiceLite.exe`, and `DTShellHlp.exe` spawning unusual network activity, `cmd.exe`, or PowerShell.
- Search DNS, proxy, EDR, and firewall logs for `env-check.daemontools[.]cc`, `38.180.107[.]76`, and DAEMON Tools processes contacting typosquatted DAEMON Tools infrastructure.
- Look for temporary payload names and paths described in public reporting, including `envchk.exe`, `cdg.exe`, `cdg.tmp`, `mcrypto.chiper`, `mcrypto.dat`, and `crypto.dll` / typo variants under `%TEMP%`, `C:\Windows\Temp`, `%APPDATA%\Microsoft`, or `C:\ProgramData\Microsoft`.
- If evidence is found, isolate before rotating credentials; the collector's process/software inventory plus selective backdoor deployment means affected hosts may have been profiled for follow-on intrusion.
- Update to vendor-validated DAEMON Tools Lite `12.6.0.2445` or later only from official sources after containment, and consider whether the product should remain allowed on managed endpoints.

## CISA KEV update (May 27)
CISA added **CVE-2026-8398** as “Daemon Tools Lite Embedded Malicious Code Vulnerability” to KEV catalog version `2026.05.27`. The due date for covered agencies is May 30, 2026, a shorter remediation window than the Nx Console and TanStack KEV entries added in the same catalog update.

## Related pages
- [CCleaner signed-update compromise](ccleaner-signed-update-compromise.md)
- [3CX desktop app compromise](3cx-desktop-app-compromise.md)
- [TamperedChef-style productivity malware clusters](tamperedchef-productivity-malware-clusters.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)

## Sources
- Kaspersky Securelist: https://securelist.com/tr/daemon-tools-backdoor/119654/
- DAEMON Tools vendor notice: https://blog.daemon-tools.cc/post/security-incident
- DAEMON Tools Lite release notes: https://www.daemon-tools.cc/releasenotes/dtLite
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- GitHub Advisory Database: https://github.com/advisories/GHSA-rm3r-35x9-jv93
