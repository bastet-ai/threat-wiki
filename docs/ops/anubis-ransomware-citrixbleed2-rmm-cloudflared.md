# Anubis ransomware CitrixBleed 2 / RMM / cloudflared intrusions

## Summary
Arctic Wolf reported on July 1, 2026 that it has investigated multiple **Anubis ransomware** intrusions since the start of 2026 involving valid VPN credential use and exploitation of **CitrixBleed 2** (**CVE-2025-5777**) against Citrix NetScaler ADC / Gateway.

The report frames the activity as affiliate-level tradecraft across Anubis ransomware-as-a-service (RaaS) intrusions rather than one uniform operator. Common intrusion patterns included abuse of legitimate remote management and monitoring (RMM) tools, hands-on-keyboard lateral movement, credential access, high-value infrastructure targeting, and alternate outbound access paths through `cloudflared`, authenticated proxies, and SSH-based SOCKS tunnels.

## Tags
- ops
- operations
- ransomware
- Anubis ransomware
- Sphinx ransomware
- CitrixBleed 2
- CVE-2025-5777
- Citrix NetScaler
- NetScaler ADC
- NetScaler Gateway
- VPN session hijacking
- MFA bypass
- valid accounts
- RMM abuse
- ScreenConnect
- Zoho Assist
- MeshAgent
- Remotely
- UltraVNC
- Total Software Deployment
- cloudflared
- SOCKS tunneling
- PsExec
- Mimikatz
- NTDS.dit
- rclone
- S3 Browser
- s5cmd
- backup targeting
- NAS targeting
- Arctic Wolf

## Why this matters
- Arctic Wolf links Anubis intrusions to **CitrixBleed 2 exploitation**, adding ransomware-affiliate post-exploitation detail to a high-priority edge/VPN vulnerability already tracked in CISA KEV.
- The intrusion pattern turns edge-session theft or valid VPN credentials into a familiar ransomware chain: RDP/SMB movement, PsExec service execution, RMM deployment, credential dumping, cloud/data-transfer tooling, and encryption.
- Legitimate RMM tooling can hide in normal IT operations. Arctic Wolf observed ScreenConnect, Zoho Assist, MeshAgent, Remotely, UltraVNC, and Total Software Deployment across reviewed incidents.
- The targeting focus—Remote Desktop Services, domain controllers, hypervisors, backup-adjacent systems, and NAS devices—raises recovery-denial risk even before encryption.
- Alternate access paths such as `cloudflared`, authenticated proxies, and SSH SOCKS tunnels mean defenders should not scope containment to the first VPN/RMM channel discovered.

## Public reporting details
- **Operation / malware:** Anubis ransomware; Arctic Wolf describes Anubis as a RaaS operation that emerged in late 2024 as a Sphinx ransomware rebrand, with encrypted file extension changing from `.sphinx` to `.anubis`.
- **Public RaaS launch:** Arctic Wolf says Anubis was announced on the RAMP criminal forum on February 23, 2025.
- **Victim claims:** Arctic Wolf cites up to 83 victims on the Anubis leak site at publication time.
- **Observed initial access:** valid VPN credential use and CitrixBleed 2 / CVE-2025-5777 exploitation against Citrix NetScaler ADC / Gateway.
- **Exploitation clue:** Arctic Wolf highlighted NetScaler VPN log patterns where `Source` IP differs from the original `Client_ip`, including `45.227.254[.]25` as an example exploitation source from VPS-hosting infrastructure.
- **VPN sources noted by Arctic Wolf:** valid Cisco AnyConnect logins from hosting ASNs including AS20473 / The Constant Company and AS55286 / ServerMania.

## Observed intrusion chain
Arctic Wolf's cases varied by affiliate, but the durable sequence is:

1. Initial access through CitrixBleed 2 session-material exposure or valid VPN credentials.
2. VPN-authenticated internal access followed by RDP and SMB activity.
3. Credential access and lateral movement using tools such as Mimikatz, PsExec, browser credential export, and NTDS.dit collection.
4. Deployment or abuse of legitimate remote-access tools, including ScreenConnect, Zoho Assist, MeshAgent, Remotely, UltraVNC, and Total Software Deployment.
5. Discovery and staging with tooling such as NetScan, Advanced IP Scanner, Nmap, S3 Browser, `s5cmd`, and `rclone`.
6. Establishment of alternate access or egress paths using `cloudflared`, authenticated proxies, and SSH-based SOCKS tunnels.
7. Targeting of Remote Desktop Services hosts, domain controllers, hypervisors, backup-adjacent systems, and NAS devices.
8. Exfiltration to cloud storage and Anubis ransomware encryption / destructive impact.

## Network and artifact pivots
Arctic Wolf's public GitHub IOC bundle includes these durable examples:

- `45[.]227[.]254[.]25` — CVE-2025-5777 exploitation source; AS267784 / Flyservers S.A.
- `45[.]76[.]79[.]92` — Remotely Desktop C2; AS20473 / The Constant Company.
- `149[.]28[.]66[.]79`, `66[.]135[.]2[.]118`, `78[.]141[.]225[.]239`, `95[.]179[.]191[.]47`, `192[.]248[.]145[.]210` — VPN authentication sources in the Arctic Wolf bundle.
- `relay.promotds[.]us` — ScreenConnect relay domain.
- `azuremicrosoft[.]us` and `promotds[.]us` — typosquatted domains called out in Arctic Wolf's defensive guidance.
- `RESTORE FILES.html` — reported Anubis ransom note.
- `.anubis` — encrypted-file extension.
- Staging paths observed by Arctic Wolf include `C:\Apps`, `C:\PerfLogs`, user `Desktop` / `AppData` / `AppData\Local`, `C:\Users\Public`, and `C:\Windows\Temp\netscan`.
- Example encryptor filenames and hashes in the IOC bundle include `4s6d0z.exe` / SHA-256 `91192cc647a6744b5426a7893401ead26a256baffd577acc983093c4f67654fa` and `wa2cz8.exe` / SHA-256 `7efdca00d75724ec8773b35ae4b1154f840694d02f3a66058b5ae04157b367ef`.

## Defensive guidance
1. Treat exposed Citrix NetScaler ADC / Gateway systems affected by CVE-2025-5777 as emergency patch and session-reset candidates. Apply Citrix guidance and terminate active sessions after patching.
2. Review NetScaler VPN logs for mismatches between original `Client_ip` and later `Source` IPs, especially where the source belongs to VPS/hosting providers and is followed by RDP, SMB, or administrative tooling.
3. Correlate VPN logins from hosting ASNs with downstream RDP, SMB, PsExec service creation, credential-access tooling, and RMM installation.
4. Maintain an approved-RMM inventory. Alert when multiple remote-access tools appear in a short window or when ScreenConnect, Zoho Assist, MeshAgent, Remotely, UltraVNC, or Total Software Deployment are installed outside approved deployment paths.
5. Hunt for `cloudflared`, authenticated proxy clients, SSH SOCKS tunnels, and unexpected long-lived outbound tunnels from servers that normally do not require them.
6. Prioritize protection and telemetry on domain controllers, RDS infrastructure, hypervisors, backup servers, and NAS devices; preserve logs before cleanup where feasible.
7. Block or monitor the Arctic Wolf IOC bundle where operationally appropriate, but do not rely on static indicators alone; the core pattern is edge-session theft or valid VPN login followed by LOTL/RMM ransomware tradecraft.
8. Review cloud-storage and transfer-tool usage (`rclone`, S3 Browser, `s5cmd`) from administrative hosts and servers during the suspected exposure window.
9. If Anubis activity is suspected, rotate VPN, domain, service, RMM, cloud-storage, and backup credentials after containment and after removing persistence/tunnel paths.

## Related pages
- [CitrixBleed session-hijack wave](citrixbleed-session-hijack-wave.md)
- [Storm-2603 parallel SharePoint ransomware intrusion](storm-2603-parallel-sharepoint-ransomware-intrusion.md)
- [SimpleHelp CVE-2026-48558 authentication-bypass exploitation](simplehelp-cve-2026-48558-authentication-bypass-exploitation.md)
- [Quest KACE SMA CVE-2025-32975 exploitation](quest-kace-sma-cve-2025-32975-exploitation.md)
- [FortiBleed Fortinet credential exposure](fortibleed-fortinet-credential-exposure.md)

## Sources
- Arctic Wolf: [https://arcticwolf.com/resources/blog/citrixbleed-2-to-cloudflared-the-tools-and-techniques-behind-anubis-ransomware-attacks/](https://arcticwolf.com/resources/blog/citrixbleed-2-to-cloudflared-the-tools-and-techniques-behind-anubis-ransomware-attacks/)
- Arctic Wolf public IOC bundle: [https://github.com/rtkwlf/wolf-tools/tree/main/threat-intelligence/anubis-citrixbleed2-to-cloudflared](https://github.com/rtkwlf/wolf-tools/tree/main/threat-intelligence/anubis-citrixbleed2-to-cloudflared)
- Citrix CVE-2025-5777 guidance: [https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX693420](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX693420)
- CISA KEV catalog: [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
