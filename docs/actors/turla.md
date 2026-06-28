# Turla

## Summary
**Turla** is a long-running Russia-linked cyber-espionage group also tracked publicly as **SUMMIT**, **Secret Blizzard**, **VENOMOUS BEAR**, and **UAC-0194**. CISA has publicly attributed Turla's Snake implant activity to Center 16 of Russia's Federal Security Service (FSB).

Google Threat Intelligence Group's June 2026 STOCKSTAY disclosure reinforces Turla's continued development of custom Windows espionage tooling. GTIG reported that Turla has developed and deployed the .NET STOCKSTAY backdoor since at least December 2022 against Ukrainian government and military organizations and entities with Italian foreign-policy interests, with code and functional overlaps to the Turla KAZUAR toolkit.

ESET's June 2026 Gamaredon retrospective reports an early-2025 **Gamaredon / Turla collaboration** and notes prior Gamaredon collaboration with InvisiMole. Treat the ESET statement as an activity-specific linkage, not as a merger of actor identities.

## Tags
- groups
- espionage
- Turla
- SUMMIT
- Secret Blizzard
- VENOMOUS BEAR
- UAC-0194
- Russia-linked
- FSB Center 16
- Snake
- KAZUAR
- STOCKSTAY
- WILDDAY
- DIAMONDBACK
- Ukraine targeting
- Gamaredon collaboration
- foreign affairs targeting
- defense targeting
- Signal interception
- legacy botnet hijacking

## Why this matters
- Turla remains active after years of public exposure and law-enforcement / government reporting, including continuing evolution beyond the Snake-era public narrative.
- GTIG's STOCKSTAY analysis ties newer .NET WebSocket backdoor development to the same broader ecosystem as KAZUAR, indicating parallel tooling and potential fallback access paths.
- Reported targeting of Ukrainian government and military organizations, western foreign-affairs interests, and defense-sector contexts keeps Turla relevant for government, diplomatic, military, and policy organizations.
- The group has a history of blending bespoke implants, compromised infrastructure, and hijacked third-party/criminal infrastructure, so defenders should not rely on a single C2 or malware-family lens.

## Public activity profile
- Suspected activity dates back to at least 2004, according to GTIG's public summary.
- Public reporting associates Turla with western ministries of foreign affairs, defense organizations, Ukrainian organizations, and foreign-policy-adjacent targets.
- GTIG noted recent Turla activity including specialized scripts to intercept Signal Messenger communications, hijacking legacy criminal botnets to target Ukrainian organizations, and KAZUAR campaigns against military defense sectors.
- In a late-2023 Ukrainian compromise reviewed by Mandiant, Turla deployed WILDDAY, DIAMONDBACK, KAZUAR, and STOCKSTAY through malicious GPO installation from a compromised domain controller.
- ESET reports early-2025 collaboration between Gamaredon and Turla in Ukraine-focused activity; during triage, preserve evidence that could show handoff, co-resident tooling, or shared infrastructure rather than assuming all artifacts belong to one cluster.

## Tooling and tradecraft
- **Snake** — long-running Turla implant publicly attributed by CISA to FSB Center 16.
- **KAZUAR** — Turla toolkit with code / functional overlap to STOCKSTAY; GTIG observed KAZUAR C2 detections near a STOCKSTAY deployment in a Ukrainian incident.
- **STOCKSTAY** — multi-component .NET Windows backdoor with encrypted WebSocket C2, `WM_COPYDATA` component IPC, environment-keyed or hard-coded protected configuration, screen/file/registry/process capabilities, and downloader/installer support.
- **K1MORPHER** — GTIG-tracked obfuscation mechanism observed in STOCKSTAY components and select KAZUAR samples, increasing confidence in a shared development ecosystem.
- **Operational deployment** — malicious GPO installation from domain controllers, RDP-file spear phishing, malicious HTA / archive lures, compromised Ukrainian infrastructure for payload hosting, and registry-run persistence.

## Defender heuristics
- In Ukrainian, diplomatic, defense, and foreign-policy environments, treat KAZUAR, STOCKSTAY, WILDDAY, or DIAMONDBACK indicators as potentially related intrusion stages rather than isolated detections.
- Hunt for domain-controller staging of ZIP archives, registry files, PowerShell backdoors, or malware components during suspected Turla incidents.
- Review outbound secure WebSocket traffic from unusual .NET processes, especially when paired with encrypted stock-market-themed configuration files or business-hours beacon windows.
- Preserve environment-specific configuration material and domain-controller artifacts before remediation; environmental keying can make recovered files critical for reconstructing victim-specific C2.

## Related pages
- [Turla STOCKSTAY backdoor operations](../ops/turla-stockstay-backdoor-operations.md)
- [STOCKSTAY](../tools/stockstay.md)
- [Gamaredon 2025 tunnels, workers, dead drops, and cloud exfiltration](../ops/gamaredon-2025-tunnels-workers-dead-drops.md)

## Sources
- ESET WeLiveSecurity: https://www.welivesecurity.com/en/eset-research/gamaredon-2025-leveraging-tunnels-workers-dead-drops-new-alliances/
- Google Cloud / Google Threat Intelligence Group: https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering
