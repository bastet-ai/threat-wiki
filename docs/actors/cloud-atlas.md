# Cloud Atlas

## Summary
**Cloud Atlas** is a long-running espionage actor publicly tracked by Kaspersky since 2014. Kaspersky's May 2026 reporting covers activity from late 2025 into early 2026 against government, diplomatic, and commercial organizations in Russia and Belarus, adding new tooling and persistence details to the actor's established phishing playbook.

The current reporting is durable threat.wiki material because it ties the actor to ZIP/LNK phishing, legacy Office Equation Editor exploitation, VBScript and PowerShell backdoors, reverse SSH / ReverseSocks / Tor backup channels, and a newly documented **PowerCloud** PowerShell tool that writes collected administrator and host data into Google Sheets.

## Tags
- APT
- espionage
- phishing
- Russia
- Belarus
- government targeting
- diplomatic targeting
- PowerShell
- VBScript
- LNK files
- SSH tunnels
- Tor
- ReverseSocks
- PowerCloud
- PowerShower
- VBCloud

## Primary motivation
- **Espionage** against government agencies, diplomatic entities, and strategically useful commercial organizations.
- **Credential and document theft** through stealer-focused backdoors and post-compromise credential collection.
- **Access resilience** through overlapping C2, reverse-tunnel, and Tor-based backup channels.

## Naming and affiliation
- Kaspersky tracks the cluster as `Cloud Atlas` and reports confidence based on reused initial-access patterns, victimology, and tooling lineage.
- Keep Cloud Atlas distinct from nearby Russia-nexus or post-Soviet espionage clusters unless primary sources explicitly join the activity.
- Kaspersky notes some operational parallels with recent `Head Mare` activity, but presents them as parallels rather than a firm attribution merge.

## 2025-2026 Russia / Belarus campaign
- **Source/date:** Kaspersky Securelist report published 2026-05-22, covering late-2025 and early-2026 activity.
- **Targeting:** government organizations, diplomatic entities, and commercial companies in Russia and Belarus.
- **Initial access:** phishing emails carrying ZIP archives with malicious LNK files; Kaspersky also notes continued use of malicious Office documents exploiting the old Equation Editor vulnerability CVE-2018-0802.
- **Execution chain:** LNK shortcuts launched externally hosted PowerShell scripts, prepared decoy PDF content, established early persistence, and dropped follow-on payloads.
- **VBCloud:** a VBScript launcher decrypts an encrypted backdoor body and executes it in memory; Kaspersky describes VBCloud as focused on file theft for extensions such as DOC, PDF, and XLS.
- **PowerShower:** a PowerShell backdoor used for network reconnaissance and lateral movement, including process/admin/domain-controller discovery, C2-delivered PowerShell execution, Kerberoasting support, and credential-grabbing scripts that copy SAM and SECURITY hives from Volume Shadow Copy snapshots.
- **RDP enablement:** operators used scripts such as `rdp_new.ps1` to enable RDP, downgrade security settings, patch `termsrv.dll`, and allow concurrent sessions so attacker access would not visibly disconnect the legitimate user.
- **Backup control channels:** Kaspersky observed widespread reverse SSH tunnels, RevSocks / ReverseSocks proxy tooling, and Tor hidden-service setups to preserve access after primary backdoor disruption.
- **PowerCloud:** a newly analyzed obfuscated PowerShell / PS2EXE-packaged tool that collects user and administrator context, encodes it, and appends it to a Google Sheet.

## Defender signals
- Phishing mail with ZIP attachments containing LNK shortcuts that invoke remote PowerShell and retrieve decoy archives.
- Legacy Office Equation Editor exploitation (`CVE-2018-0802`) in environments where Office compatibility features should be tightly controlled.
- VBScript and PowerShell artifacts such as `video.vbs`, `video.mds`, `googleearth.ps1`, `rdp_new.ps1`, `WriteToSchedulerGenerateKey.vbs`, `WriteToSchedulerRunSSH.vbs`, and `WriteToSchedulerKillSSH.vbs` in user, `INF`, `PLA`, or other unusual Windows paths.
- Scheduled tasks that start OpenSSH, RevSocks, Tor, or attacker-staged VBS scripts from system-looking directories.
- Modified or portable OpenSSH binaries, especially where imports are altered from `libcrypto.dll` to a nearby `syruntime.dll`.
- Tor hidden-service configuration on ordinary workstations, especially routing RDP from `.onion` services back to local ports.
- PowerShell or PS2EXE executables writing base64 host/user/admin data to Google Sheets.
- Unauthorized `termsrv.dll` byte patches, concurrent RDP behavior on Windows 10 clients, or RDP security downgrades shortly after phishing execution.

## Notes
- Treat tunneling artifacts as persistence, not merely utilities: reverse SSH, ReverseSocks, and Tor channels can outlive removal of the initial backdoor.
- Prioritize behavior over single-use infrastructure because Kaspersky's report shows both compromised domains and rotating attacker-controlled hosts.
- The actor's mix of file theft, credential access, lateral movement, and redundant tunnels warrants full incident-response scoping if any single component appears.

## Sources
- Kaspersky Securelist: <https://securelist.com/cloud-atlas-2026/119895/>
