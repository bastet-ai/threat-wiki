# AI chatbot and SEO poisoning GPU-cryptojacking campaign

## Summary
Microsoft reported an active cryptojacking campaign that pushes malicious system-utility download sites through traditional search-engine poisoning and, in observed April 2026 cases, through AI chatbot software recommendations.

The operators impersonate common PC and hardware utilities such as CrystalDiskInfo, HWMonitor, Display Driver Uninstaller, FurMark, K-Lite Codec Pack, and PDFgear. Microsoft assesses that the targeting is deliberate: those utilities attract users likely to own high-performance GPUs, making each compromise more valuable for cryptocurrency mining.

## Tags
- ops
- operations
- cryptojacking
- SEO poisoning
- AI search poisoning
- AI chatbot abuse
- software impersonation
- DLL sideloading
- ScreenConnect
- RMM abuse
- process hollowing
- Microsoft .NET
- Defender evasion
- dynamic DNS
- gleeze.com
- Dynu

## Why this matters
- The campaign extends poisoned-download operations from search results into AI-assisted discovery flows. Defenders should treat AI-generated software recommendations as another referral surface that can point users to attacker-controlled domains.
- The operators are optimizing for GPU yield rather than raw infection count. That changes triage priorities for gaming, workstation, rendering, ML, and engineering endpoints.
- The chain installs ScreenConnect for persistent remote access before mining. Even if mining is the visible payload, the same foothold can support later data theft, lateral movement, or ransomware activity.
- The payload repeatedly repairs persistence and Defender exclusions. Removal needs to verify scheduled tasks, Run keys, Startup-folder shortcuts, exclusions, ScreenConnect service configuration, and hollowed .NET processes together.

## Reported tradecraft
1. Users search for trusted system utilities or ask AI chatbot tools for software download recommendations.
2. Poisoned results or generated recommendations send users to attacker-controlled lookalike download domains.
3. The fake site serves a ZIP archive from a campaign-specific `gleeze[.]com` subdomain hosted on Dynu-associated dynamic-DNS infrastructure.
4. The ZIP contains the legitimate utility executable plus a malicious `autorun.dll` that is sideloaded when the user launches the utility.
5. The DLL invokes `msiexec.exe` to silently install `vcredist_x64.dll`, which packages ScreenConnect / ConnectWise Control.
6. The ScreenConnect client calls back to attacker-controlled infrastructure, including `directdownload[.]icu` and `193.42.11[.]108`, then receives a dropper such as `SimpleRunPE.exe`.
7. `SimpleRunPE.exe` copies itself as `RuntimeHost.exe` under a hidden path using campaign identifier `D3F4E2A1` and establishes persistence through three scheduled tasks, two Run keys, and a Startup-folder shortcut.
8. The dropper hollows Microsoft-signed .NET binaries such as `InstallUtil.exe`, `RegAsm.exe`, `RegSvcs.exe`, `MSBuild.exe`, `AppLaunch.exe`, `AddInProcess.exe`, or `aspnet_compiler.exe`.
9. The hollowed process collects host, GPU, OS, network, antivirus, idle-time, and mining-state telemetry, then connects over WebSocket to `wss[:]//minemine.gleeze[.]com:8443/ws` with TLS certificate pinning.
10. The loader downloads and runs GPU mining software such as gminer, lolMiner, or SRBMiner-MULTI, while pausing mining when user or analyst activity is detected.

## Notable indicators and pivots
- More than 150 malicious domains impersonating system utilities, according to Microsoft.
- Fake download infrastructure under `gleeze[.]com`, with Dynu-linked dynamic-DNS hosting.
- ScreenConnect callback: `directdownload[.]icu` on port `8041` and IP `193.42.11[.]108`.
- Campaign identifier: `D3F4E2A1`, including mutex `Global\D3F4E2A1_Svc` and hidden install-path artifacts.
- Persistence names: `Windows System Health`, `Windows System Health Monitor`, `Windows System Health Check`, `WinSysCache`, and `RuntimeHost.lnk`.
- C2: `wss[:]//minemine.gleeze[.]com:8443/ws`.
- TLS certificate fingerprint: `EB:C3:5D:4A:08:D9:3A:88:0E:90:AE:AD:2D:3F:7F:B4:3F:DC:08:EA:77:DB:9D:D5:2F:80:78:1E:6B:FD:88:67`.

## Defender heuristics
- Warn users to prefer vendor homepages, signed installers, package managers, or managed software portals over search-result or chatbot-provided download links for utilities.
- Hunt for consumer utility installs that are immediately followed by `autorun.dll`, `msiexec.exe`, unexpected ScreenConnect installation, or outbound ScreenConnect sessions to non-corporate hosts.
- Correlate ScreenConnect file-transfer activity with `SimpleRunPE.exe`, `RuntimeHost.exe`, scheduled tasks named like Windows health telemetry, and Defender `Add-MpPreference` exclusion changes.
- Look for Microsoft .NET utilities running with unusual parent processes, GPU-mining network behavior, or command-line patterns inconsistent with normal developer/build activity.
- In incident response, preserve browser/download history, referrer metadata, AI-chatbot prompt/output artifacts if available, ZIP contents, ScreenConnect logs, scheduled-task XML, Defender preference history, and hollowed-process memory.
- For high-GPU endpoints, baseline legitimate miner, rendering, gaming, and ML activity separately so sudden miner deployment plus RMM installation is not dismissed as normal GPU use.

## Attribution notes
Microsoft did not attribute the activity to a named actor. Track it as a financially motivated cryptojacking operation with notable AI-search-poisoning and RMM-abuse delivery tradecraft unless future primary reporting links it to a stable cluster.

## Related pages
- [Ollama P2P cryptominer RAT campaign](ollama-p2p-cryptominer-rat.md)
- [ConnectWise ScreenConnect exploitation wave](connectwise-screenconnect-exploitation-wave.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [TamperedChef-style productivity malware clusters](tamperedchef-productivity-malware-clusters.md)

## Sources
- [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/26/poisoned-search-results-gpu-mining-cryptojacking-campaign-abusing-screenconnect-microsoft-net-utilities/)
- [The Hacker News summary](https://thehackernews.com/2026/05/ai-chatbot-recommendations-redirect.html)
