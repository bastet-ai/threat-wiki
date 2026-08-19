# Mustang Panda

## Summary
**Mustang Panda** is a publicly reported China-aligned espionage group that targets government, diplomatic, policy, and strategically relevant regional sectors. Public reporting repeatedly describes the group as aligning intrusion themes with geopolitical developments, bilateral meetings, and region-specific government activity.

For threat.wiki tracking, the current high-signal update is Acronis Threat Research Unit's June 2026 reporting on two Mustang Panda campaigns against Indian government and hydropower-sector targets. Those campaigns introduced **SHARDLOADER**, **MINIRECON**, and **ZOHOMURK**, with ZOHOMURK abusing Zoho WorkDrive for C2, tasking, and exfiltration.

## Tags
- actor
- actors
- Mustang Panda
- China-nexus
- espionage
- government targeting
- diplomatic targeting
- India
- hydropower
- energy sector
- Taiwan
- DLL sideloading
- cloud service abuse
- Zoho WorkDrive
- SHARDLOADER
- MINIRECON
- ZOHOMURK
- TONESHELL

## Public aliases and overlap notes
- Mustang Panda is also commonly tracked in public reporting as a China-aligned espionage cluster.
- Acronis' June 2026 assessment attributed the India hydropower / government-cooperation campaigns to Mustang Panda with high confidence based on targeting, deployment patterns, malware similarities, and infrastructure / operational overlap.
- Acronis specifically noted code and design similarities between MINIRECON and **TONESHELL**, a tool family associated in public reporting with Mustang Panda.

## Current durable coverage
- [QuickFox FDMTP software supply-chain compromise](../ops/quickfox-fdmtp-supply-chain-compromise.md) — trojanized VPN/accelerator installers filtered Windows endpoints and deployed the FDMTP backdoor. Fortinet found high-confidence tooling and infrastructure continuity with Twill Typhoon / Mustang Panda reporting but did not confidently attribute the QuickFox compromise itself.
- [Mustang Panda ZOHOMURK / MINIRECON India campaigns](../ops/mustang-panda-zohomurk-minirecon-india-campaigns.md) — two concurrent India-focused campaigns using Solid PDF Creator DLL sideloading, SHARDLOADER, MINIRECON, ZOHOMURK, Zoho WorkDrive C2/exfiltration, and CERT-In coordination.
- **CoolClient kernel-rootkit evolution (Kaspersky GReAT, August 14, 2026)** — the newest CoolClient variant (observed in intrusions in Pakistan, Mongolia, and Myanmar during late 2025–2026) deploys a **signed kernel-mode driver as a Windows service** and talks to it through dedicated **IOCTL handlers**. The driver hides the CoolClient process, protects related files and registry entries, and blocks inspection/modification — an architecture Kaspersky compares to the kernel-mode enhancements previously seen in ToneShell. In the documented Myanmar intrusion the actor first added Microsoft Defender folder and file exclusions, staged a fake `%ProgramFiles%\Microsoft\Windows Defender` directory, renamed a legitimate Sangfor executable (`Sang.exe`) to `defender.exe` as the DLL sideloader, and established SYSTEM persistence through a scheduled task named `\Microsoft\Windows\Windows Defender Advanced Threat Protection Service` running at startup. Defender pivots: Defender-exclusion additions plus the fake Defender install directory, the `defender.exe`-renamed sideloader, the named scheduled task, and a signed driver whose IOCTL surface enumerates/hides kernel modules and hooks Nsiproxy for data filtering. Kaspersky Securelist: [HoneyMyte upgrades CoolClient with a kernel-level Windows rootkit](https://securelist.com/honeymyte-coolclient-driver-rootkit/121028/).

## Defender notes
- Treat government, diplomatic, defense-cooperation, and energy-sector lures as first-class Mustang Panda hunting context, not just generic phishing.
- Correlate signed-binary DLL sideloading with regionally themed archives and cloud-service API use. In the Acronis case, the interesting signal is not one malicious binary alone but the chain from archive lure to hidden DLL to scheduled-task persistence to Zoho WorkDrive activity.
- Preserve both endpoint and SaaS evidence. Cloud-storage C2 can leave decisive traces in OAuth clients, refresh-token use, folder creation, file upload/download activity, and tenant audit logs.

## Sources
- Acronis Threat Research Unit: [https://www.acronis.com/en/tru/posts/mustang-panda-targets-indias-government-and-energy-sectors/](https://www.acronis.com/en/tru/posts/mustang-panda-targets-indias-government-and-energy-sectors/)
- MITRE ATT&CK group profile: [https://attack.mitre.org/groups/G0129/](https://attack.mitre.org/groups/G0129/)
