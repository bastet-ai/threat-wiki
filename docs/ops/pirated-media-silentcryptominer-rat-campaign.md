# Pirated media SilentCryptoMiner RAT campaign

## Summary
**Pirated media SilentCryptoMiner RAT campaign** is a Kaspersky-reported cybercrime operation distributing a modified SilentCryptoMiner fork and RAT capability through fake plugin/update prompts on illegal movie, TV, and digital-library sites. Kaspersky connects the current April 2026 activity to a broader campaign pattern active since at least 2022, with actors repeatedly updating the delivery chain and malware components.

The durable intelligence value is the blend of high-traffic piracy lures, DLL side-loading, UAC pressure, service and Run-key persistence, watchdog self-restoration, RAT control, and XMRig-style mining. The campaign is not just nuisance cryptomining: the RAT path and persistence model give operators remote control and make host cleanup order matter.

## Tags
- ops
- operations
- Kaspersky
- cybercrime
- piracy
- fake update
- DLL side-loading
- RAT
- remote access
- cryptominer
- XMRig
- SilentCryptoMiner
- Windows
- UAC
- persistence
- watchdog
- process hollowing
- DNS tunneling
- defense evasion

## Why this matters
- Kaspersky observed the campaign on highly trafficked illegal content sites; linked digital-library and streaming sites ranged from thousands to tens of millions of monthly visits, with roughly 40 million April 2026 visits across sites where the malware was detected.
- The lure is ordinary and reusable: a video player or browser/plugin update prompt leads to a ZIP archive containing a legitimate executable and malicious DLL.
- The malware deploys both mining and remote-control functionality, so defenders should treat infections as potential unauthorized access rather than low-priority coin-miner noise.
- Persistence and watchdog behavior can restore files after partial removal; Kaspersky notes the watchdog running inside `explorer.exe` should be terminated before remediation.

## Operational characteristics
- **Initial lure:** illegal movie / TV streaming and digital-library sites display fake update prompts, including outdated video-player-plugin or fake browser-crash style themes.
- **Archive:** the download is a ZIP archive containing a legitimate `HLS Installer.874.exe` executable and a malicious DLL that side-loads into the legitimate process.
- **Campaign continuity:** Kaspersky links the current activity to earlier pirate-library distribution that used `file[.]ipfs[.]us[.]69[.]mu`; the current observed download infrastructure uses `urush1bar4[.]online`.
- **Loader / anti-analysis:** the DLL is inflated with junk data, uses a stack-overflow / ROP-style transition to decrypt the next stage, and reflectively loads the main module.
- **Execution gate:** the main module collects processor data, the `C:/` drive serial number, elevation state, and process-start timestamp, then sends the values as a crafted DNS query. Execution proceeds when the response contains `01 02 03 04`.
- **Elevated path:** when launched with administrator rights, the malware adds broad Windows Defender exclusions for EXE/DLL files and key user/system directories, attempts to disable or block Microsoft Malicious Software Removal Tool (`mrt.exe`), disables sleep/hibernation, copies itself under `C:\ProgramData\Google\Chrome`, and registers `GoogleUpdateTaskMachineQC` as an automatic service.
- **Non-elevated path:** when started as a standard user, it copies itself to `%USERPROFILE%\AppData\Roaming\Sandboxie`, configures Run-key persistence, and repeatedly raises UAC prompts every three minutes until the elevated service path succeeds.
- **Injected components:** the main module injects the RAT agent into `conhost.exe`; watchdog, CPU miner, and optional GPU miner components are injected into `explorer.exe` when the host has a discrete GPU.
- **Watchdog:** the watchdog encrypts copies of files from `C:\ProgramData\Google\Chrome` with XOR key `AFeIboiOmImJS2ypJU0pTpAO61SELkUc`, keeps them in memory, checks the service every five seconds, and rewrites the installed files if the service is damaged or removed.
- **RAT C2:** the RAT builds date-derived C2 domains and polls paths shaped like `http://{domain}.space/index.php?authorization=1` and `http://{domain}.site/index.php?...`; Kaspersky lists several observed `.space` domains.
- **Mining path:** the CPU miner is based on XMRig; the optional GPU miner supports multiple algorithms. Configuration is retrieved from weekly date-derived domains under `strangled.net`, `ignorelist.com`, `ftp.sh`, and `zanity.net`, all resolving to `107[.]172[.]212[.]235` in Kaspersky's analysis.
- **Process hollowing:** retrieved miner configuration is AES-CBC encrypted and passed as a command-line parameter when launching the miner inside `explorer.exe` through process hollowing.

## Defender heuristics
- Treat piracy-site fake-update infections as credential and remote-access incidents, not only as miner cleanup.
- Hunt for `HLS Installer.874.exe` execution followed by unexpected DLL loads, `conhost.exe` / `explorer.exe` injection, or `explorer.exe` child behavior associated with mining or C2 traffic.
- Inspect for `GoogleUpdateTaskMachineQC`, unexpected binaries under `C:\ProgramData\Google\Chrome`, and user Run-key persistence under `%USERPROFILE%\AppData\Roaming\Sandboxie`.
- Check Windows Defender exclusions for broad EXE/DLL or `%USERPROFILE%`, `%PROGRAMDATA%`, and `%WINDIR%` paths added near the infection window.
- Review power configuration changes that disable hibernation and standby on AC or battery, and registry policy values under `HKLM\Software\Policies\Microsoft\MRT` that block MSRT delivery.
- Correlate DNS queries that encode host metadata or use crafted `microsoft.com`-looking domains with direct traffic to unrelated IP addresses.
- Block and investigate traffic to Kaspersky-listed RAT and mining configuration infrastructure, including `107[.]172[.]212[.]235`, while remembering that weekly domain generation means fixed-domain blocks will age out.
- During cleanup, terminate the watchdog injected in `explorer.exe` before deleting service files; otherwise it may rewrite the malware from its in-memory encrypted copies.

## Selected indicators
- **Archive host:** `urush1bar4[.]online`.
- **Earlier distribution domain:** `file[.]ipfs[.]us[.]69[.]mu`.
- **Malicious DLL hashes:** `6A0FE6065D76715FEEBC1526D456DB73`, `7F624407AE489324E96A708A09C17E6F`, `02A43B3423367B9DDDC24CC7DFC070DF`.
- **RAT C2 domains:** `5d14vnfb[.]space`, `r7mvjl67[.]space`, `zgj1tam9[.]space`, `jeaw520i[.]space`, `qdmagva5[.]space`.
- **Mining configuration IP:** `107[.]172[.]212[.]235`.
- **UnamWebPanel addresses:** `m4yuri[.]online`, `kristina[.]quest`.
- **Paths and persistence:** `C:\ProgramData\Google\Chrome`, `%USERPROFILE%\AppData\Roaming\Sandboxie`, `GoogleUpdateTaskMachineQC`.
- **Kaspersky detections:** `HEUR:Trojan.Win64.DllHijack.gen`, `MEM:Trojan.Win32.SEPEH.gen`.

## Related pages
- [Ollama P2P cryptominer RAT campaign](ollama-p2p-cryptominer-rat.md)
- [AI chatbot and SEO poisoning GPU-cryptojacking campaign](ai-chatbot-seo-poisoning-gpu-cryptojacking.md)
- [TamperedChef-style productivity malware clusters](tamperedchef-productivity-malware-clusters.md)

## Sources
- Kaspersky Securelist: https://securelist.com/video-books-pirates-miners-rat/119943/
