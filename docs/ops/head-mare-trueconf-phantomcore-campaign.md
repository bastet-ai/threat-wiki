# Head Mare: TrueConf server exploitation delivers PhantomCore and PhantomGraph

## Summary
Kaspersky Threat Response reported a **July 2026 campaign by the Head Mare group** that exploited a chain of two unpatched-at-the-time vulnerabilities in **TrueConf** video-conferencing servers to compromise them and infect video-conference participants. The attackers used the server-side foothold to replace legitimate TrueConf client installers with trojanized copies that install the **PhantomCore** backdoor, and to deploy a second backdoor, **PhantomGraph**, from the web shell.

Kaspersky now classifies Head Mare as an **APT group** (previously tracked as a hacktivist cluster) based on the sophistication of its TTPs and the absence of destructive activity (encryption, wiping) in its target infrastructure.

## Tags
- ops
- operations
- Head Mare
- TrueConf
- PhantomCore
- PhantomGraph
- KLCERT-26-057
- KLCERT-26-058
- video conferencing
- web shell
- client installer poisoning
- OneDrive C2
- APT
- espionage
- service DLL persistence

## Attack chain
1. **Unauthenticated access on port 4307/TCP.** The attackers connect to the TrueConf server without prior authorization via TCP port 4307, which is open by default according to the product documentation. The attack covers TrueConf Server **5.3.x – 5.3.9, 5.4.x – 5.4.9, and 5.5.x – 5.5.5**.
2. **Malicious script execution (KLCERT-26-057).** A server function is abused to transmit and execute a malicious script on the server. The script runs in an isolated environment that by default has no access to operating-system functions.
3. **Isolation escape (KLCERT-26-058).** A second vulnerability lets the script escape the isolation environment and execute commands in the context of the operating system, achieving arbitrary code execution as **NT AUTHORITY\SYSTEM**.
4. **Web shell persistence.** The attackers replace `...\public\js\locale.php` with a web shell used for subsequent remote control of the server: IT-infrastructure reconnaissance, privileged access to the TrueConf database, and — the key distribution step — **replacing the original TrueConf Client distribution with an infected version that carries the PhantomCore backdoor**.
5. **Participant infection.** Users who download the trojanized client installer from the compromised server install PhantomCore. Persistence is established through the registry key `HKEY_CURRENT_USER\Software\Classes\CLSID\{0340F119-A598-4ed9-B0AC-6F6A12D3E755}\InprocServer32`, pointing to the malicious file.
6. **PhantomGraph from the web shell.** The web shell also deploys a two-module backdoor named **PhantomGraph**:
   - `SysExcSvc.dll` — receives commands from the attackers and transmits execution results; uses a **Microsoft OneDrive cloud-storage account as C2**.
   - `SysReadSvc.dll` — reads the command, executes it (via a `cmd.exe /c cmd /c "<temp>\cmd_cmd_*.bat"` style batch invocation), and stores the result.
   - Persistence: a Base64-encoded PowerShell command installs both DLLs as Windows services. Kaspersky notes the command is deliberately split across two components to complicate EDR detection, and that the code partially matches PhantomCore, indicating it belongs to Head Mare's arsenal.

## Patching and vendor response
The two exploited vulnerabilities were patched by the TrueConf vendor in the latest server updates (**5.3.9, 5.4.9, and 5.5.5**, released **June 18, 2026**). Kaspersky detections: `Trojan.Win32.Phoenax`-family naming aside, the backdoor was detected by Kaspersky products; the article publishes MD5 file hashes, IPs, domains, Windows service names, file paths, registry keys, and YARA rules.

## Defender priorities
1. **Patch TrueConf Server immediately** to 5.3.9 / 5.4.9 / 5.5.5 (or later) and verify the build; this campaign hit unpatched servers over a default-open port (4307/TCP).
2. **Assume client-distribution poisoning on any compromised TrueConf server.** Audit TrueConf deployments for replacement of the client installer files, and compare current client distributions against vendor-published integrity values; force re-download of clients through trusted channels.
3. **Hunt for the `locale.php` web shell** (`...\public\js\locale.php` modification) and privileged database access on TrueConf servers.
4. **Hunt on endpoints** for the `InprocServer32` CLSID persistence key (`{0340F119-A598-4ed9-B0AC-6F6A12D3E755}`), PhantomCore artifacts, and the `SysExcSvc` / `SysReadSvc` Windows services.
5. **Watch OneDrive-backed C2.** PhantomGraph's command channel ran through a Microsoft OneDrive account; cloud-storage C2 via personal/cloud accounts is increasingly common and is often out of scope for corporate egress controls — review OneDrive (and similar) web-traffic and file-sync telemetry for service-name anomalies.
6. **Treat Head Mare as an espionage actor, not a hacktivist**, in Triage and threat-modeling: Kaspersky's reclassification means the durable behavior is persistent, low-destructive access rather than disruption.

## Assessment limits
- Reporting is Kaspersky Threat Response (August 11, 2026); no independent vendor corroboration is published as of this scan.
- KLCERT-26-057 / KLCERT-26-058 are Kaspersky internal identifiers; the corresponding public CVEs, if any, were not referenced in the article.
- Victim scope beyond "participants of compromised TrueConf conferences" is not further detailed in the article.

## Related pages
- [Cloud Atlas](../actors/cloud-atlas.md) — Kaspersky has previously noted operational parallels with Head Mare activity
- [Cavern Manticore](../actors/cavern-manticore.md) — another 2026 Iran/region-adjacent espionage cluster with modular .NET C2
- [Cavern](../tools/cavern.md)

## Sources
- Kaspersky Threat Response: [Head Mare APT is exploiting vulnerabilities in an unpatched TrueConf server to deliver PhantomCore and PhantomGraph to video conference participants](https://securelist.com/tr/head-mare-targets-trueconf-server-with-phantomcore/120988/) — August 11, 2026
