# CL-STA-1062

## Summary
**CL-STA-1062** is a Unit 42-tracked Chinese-speaking espionage activity cluster active since at least March 2022. Unit 42 assesses with high confidence that CL-STA-1062 is the same cluster Cisco Talos reported as **UAT-7237** in 2025 Taiwanese web-hosting infrastructure campaigns.

Unit 42's June 25, 2026 public report expands the cluster's public profile to Southeast Asian government and critical-infrastructure targeting, including state-owned energy entities, and documents a newly reported custom Windows backdoor named **TinyRCT** alongside web shells, SoftEther VPN, VNT, yuze, Mimikatz, fscan, JuicyPotato, and password-protected RAR staging.

## Tags
- groups
- espionage
- CL-STA-1062
- UAT-7237
- China-linked
- Chinese-speaking
- Southeast Asia
- Taiwan
- government targeting
- critical infrastructure
- energy sector
- web shells
- ASPX web shells
- SoftEther VPN
- VNT
- yuze
- TinyRCT
- Mimikatz
- JuicyPotato
- RAR staging

## Why this matters
- The reporting links 2025 Southeast Asian government and energy-sector intrusions to a longer-running East Asia cluster previously associated with Taiwan web-hosting infrastructure compromises.
- CL-STA-1062 blends commodity and open-source tooling with custom malware, so defenders should hunt both familiar administrative/tunneling binaries and bespoke payload behavior.
- Unit 42 observed the actor compressing findings into password-protected RAR archives, using web shells as execution hubs, and disguising tunneling tools as VMware or endpoint-security-looking executables.
- The TinyRCT disclosure gives concrete host, persistence, C2, and cleanup pivots for a cluster that may otherwise look like ordinary web-app post-exploitation plus VPN tunneling.

## Public activity profile
- Unit 42 says the cluster has operated across East Asia since 2022 and expanded activity in Southeast Asia during 2025.
- September 2025 telemetry included a Southeast Asian government compromise with ASPX web shells, MSSQL data exfiltration, web-server source-code staging, and reconnaissance against a separate government entity in the same country.
- Between October and December 2025, Unit 42 observed likely compromise of at least ten organizations in Southeast Asia.
- Mid-2025 activity focused on critical infrastructure; Unit 42 identified attacks against a critical-infrastructure entity over several months and compromise of two state-owned critical energy infrastructure entities in the same Southeast Asian country.
- Reported operations used outbound victim requests to actor-controlled infrastructure to download payloads, including SoftEther VPN components and RAR archives containing tools.

## Tradecraft
- Initial footholds commonly start with exploited web applications and deployed ASPX web shells.
- Web shells provide command execution, tool deployment, and initial reconnaissance.
- Unit 42 observed network and system enumeration results sent directly to actor-controlled infrastructure using `curl`.
- Tunneling / C2 / exfiltration tooling includes SoftEther VPN, yuze, and VNT, often renamed to look like legitimate VMware or XDR components.
- Privilege escalation and discovery can include open-source tools such as JuicyPotato and fscan.
- Data staging and exfiltration often use password-protected RAR archives.

## Defender heuristics
- Treat internet-facing web applications with unexpected ASPX web shells, command-execution artifacts, and direct `curl` posts of enumeration output as high-priority CL-STA-1062-like behavior when paired with Southeast Asia / East Asia targeting.
- Hunt for tunneling tools renamed as `vmtools.exe`, VMware-looking executables, or endpoint-security-looking components, especially when launched from web-server writable directories or scheduled tasks.
- Review outbound HTTP(S) from government and energy web servers to the reported Unit 42 infrastructure and to unusual VPN/tunnel staging paths.
- Preserve web roots, IIS logs, command-line telemetry, RAR archives, scheduled-task history, and memory from suspected hosts before cleanup.
- Rotate credentials exposed to compromised web applications, database servers, and service accounts; Unit 42 reported MSSQL exfiltration and broader reconnaissance.

## Public indicators highlighted by Unit 42
Use Unit 42's IOC table as the canonical source. High-value pivots from the public report include:

| Indicator | Type | Context |
| --- | --- | --- |
| `139.180.134[.]221` | IP address | Staging server hosting CL-STA-1062 tools and `PerfWatson2.exe` |
| `202.182.102[.]5` | IP address | Reported C2 server |
| `45.76.210[.]43` | IP address | Reported C2 server |
| `45.32.113[.]172` | IP address | TinyRCT C2 server |
| `hxxp[:]//139.180.134[.]221/PerfWatson2.exe` | URL | TinyRCT payload staging |
| `hxxp[:]//139.180.134[.]221/sdksdk608/win-vpn.rar` | URL | Tool archive staging |
| `GoogleUpdaterTaskSystem140.0.7272.0 {ACE7A46F-50FD-481C-AB32-3D838871DB40}` | Scheduled task | TinyRCT loader persistence |

## Related pages
- [CL-STA-1062 Southeast Asia government and energy intrusions](../ops/cl-sta-1062-southeast-asia-tinyrct.md)
- [TinyRCT](../tools/tinyrct.md)
- [Operation Dragon Weave Azure Blob C2 campaign](../ops/operation-dragon-weave-azure-blob-c2.md)

## Sources
- [Unit 42](https://unit42.paloaltonetworks.com/cl-sta-1062-tinyrct-backdoor/)
