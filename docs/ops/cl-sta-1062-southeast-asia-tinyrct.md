# CL-STA-1062 Southeast Asia government and energy intrusions

## Summary
Unit 42's June 25, 2026 report describes **CL-STA-1062** intrusions against Southeast Asian government entities and state-owned critical energy infrastructure during 2025. Unit 42 assesses the Chinese-speaking cluster has been active since at least March 2022 and overlaps with Cisco Talos' **UAT-7237**.

The campaign profile combines exploited web applications and ASPX web shells with open-source tunneling / post-exploitation tools and a newly documented custom .NET backdoor, **TinyRCT**. The durable defender lesson is not the label alone: hunt for web-shell-led staging, renamed VPN/tunnel tools, RAR archive exfiltration, and TinyRCT's `PerfWatson2.exe` / scheduled-task persistence.

## Tags
- ops
- operations
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
- state-owned enterprise
- web shells
- ASPX web shells
- TinyRCT
- SoftEther VPN
- VNT
- yuze
- Mimikatz
- fscan
- JuicyPotato
- AppDomainManager injection
- RAR staging

## Why this matters
- Unit 42 observed likely compromise of at least ten Southeast Asian organizations between October and December 2025, plus government and energy-sector activity that suggests regional strategic collection rather than opportunistic compromise.
- The same cluster is assessed with high confidence as overlapping Cisco Talos' UAT-7237 Taiwan web-hosting infrastructure activity, giving defenders a cross-region pivot.
- CL-STA-1062's tooling is deliberately mixed: commodity web shells and tunnels provide reach, while TinyRCT adds custom surveillance, file theft, screen capture, and cleanup capability.
- Energy and government defenders should prioritize web-server evidence preservation, because the actor used web shells for command execution, tool deployment, reconnaissance, and archive staging.

## Reported 2025 activity
- **September 2025:** Unit 42 found a Southeast Asian government entity compromised with web shells and MSSQL data exfiltration.
- During the same intrusion, the actor conducted reconnaissance against a separate government entity in the same country and staged / exfiltrated an entire directory of web-server source code.
- **October-December 2025:** Unit 42 observed likely compromise of at least ten organizations in Southeast Asia.
- **Mid-2025 onward:** the actor focused on critical infrastructure, including a months-long attack against one critical-infrastructure entity and compromise of two state-owned critical energy infrastructure entities in the same Southeast Asian country.
- Victim networks made outbound requests to attacker-controlled infrastructure and downloaded payloads such as SoftEther VPN components and RAR archives containing CL-STA-1062 tooling.

## Tradecraft sequence
1. Exploit internet-facing web applications.
2. Deploy ASPX web shells for command execution and tool staging.
3. Run network and system enumeration; Unit 42 observed results sent to actor-controlled infrastructure using `curl`.
4. Deploy open-source tunneling and post-exploitation tools, including SoftEther VPN, yuze, VNT, fscan, Mimikatz, and JuicyPotato.
5. Rename tunnel tools as legitimate-looking system files such as VMware executables or XDR-agent-looking components.
6. Stage and exfiltrate collected data through password-protected RAR archives.
7. Deploy TinyRCT through an AppDomainManager injection chain when custom Windows backdoor access is useful.

## TinyRCT chain in this operation
- Unit 42 pivoted from `139.180.134[.]221` hosting `PerfWatson2.exe` to a malicious `chrome_setup.zip` archive.
- The archive used a legitimate signed `chrome_setup.exe`, adjacent `chrome_setup.exe.config`, and malicious `MyAppDomainManager.dll` to trigger AppDomainManager injection.
- The loader required execution from `%USERPROFILE%\Downloads` and then staged `PerfWatson2.exe` under `%LOCALAPPDATA%`.
- Persistence used a highest-privilege on-logon scheduled task named `GoogleUpdaterTaskSystem140.0.7272.0 {ACE7A46F-50FD-481C-AB32-3D838871DB40}`.
- TinyRCT checked execution from `%LOCALAPPDATA%`, registered host profile data, beaconed to `45.32.113[.]172`, and supported command execution, directory/file listing, text-file reads, URL download, file exfiltration, screen capture, sleep update, and self-destruct.

## Defender notes
- Prioritize exposed web applications in Southeast Asian government, energy, and state-owned enterprise environments for web-shell review.
- Hunt for ASPX web shells that spawn archive tools, `curl`, `cmd.exe`, `powershell.exe`, database clients, or renamed VPN/tunnel binaries.
- Look for SoftEther VPN, yuze, or VNT binaries renamed to VMware or XDR-looking file names and launched from unusual directories.
- Review for password-protected RAR creation on web servers and application servers, especially followed by outbound HTTP(S) to VPS infrastructure.
- Detect the TinyRCT loader chain: `chrome_setup.zip`, adjacent `.config` AppDomainManager loading, `MyAppDomainManager.dll`, `%LOCALAPPDATA%\PerfWatson2.exe`, and the `GoogleUpdaterTaskSystem140.0.7272.0` scheduled task.
- When activity is suspected, preserve IIS/web logs, web roots, scheduled-task logs, command-line telemetry, RAR archives, database logs, memory, and outbound proxy/DNS records before containment.

## Public indicators highlighted by Unit 42
| Indicator | Type | Context |
| --- | --- | --- |
| `00e09754526d0fe836ba27e3144ae161b0ecd3774abec5560504a16a67f0087c` | SHA-256 | `chrome_setup.zip` |
| `f34bd1d485de437fe18360d1e850c3fd64415e49d691e610711d8d232071a0b1` | SHA-256 | fscan |
| `dce5df29bddff5a4ddaea5c4fec14da91f7b69063a6e1c45ed61e5da4fc6c87b` | SHA-256 | SoftEther VPN |
| `cbfe8de6ffadbb1d396f61e63eb18e8b11c29527c1528641e3223d4c516cf7c3` | SHA-256 | TinyRCT downloader |
| `4e1f8888d020decd09799ec946f1bf677cac6612b24582ddbf4d8ede425d8384` | SHA-256 | TinyRCT |
| `9b481b69cd91b09fa7bae7428f646dd89473a4c03393e43da81fe756cde1c472` | SHA-256 | VNT |
| `139.180.134[.]221` | IP address | Staging server |
| `202.182.102[.]5` | IP address | Reported C2 server |
| `45.76.210[.]43` | IP address | Reported C2 server |
| `45.32.113[.]172` | IP address | TinyRCT C2 server |
| `hxxp[:]//139.180.134[.]221/sdksdk608/1.zip` | URL | Tool staging |
| `hxxp[:]//139.180.134[.]221/sdksdk608/win-vpn.rar` | URL | Tool archive staging |
| `hxxp[:]//139.180.134[.]221/PerfWatson2.exe` | URL | TinyRCT payload staging |

## Related pages
- [CL-STA-1062](../actors/cl-sta-1062.md)
- [TinyRCT](../tools/tinyrct.md)
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)

## Sources
- [Unit 42](https://unit42.paloaltonetworks.com/cl-sta-1062-tinyrct-backdoor/)
