# OceanLotus

## Summary
**OceanLotus** is a Vietnam-aligned espionage group also widely reported as **APT32**. Public reporting tracks the group back to at least 2012, with targeting across China, Southeast Asia, Vietnamese diaspora or activist communities, and — in ESET's 2026 reporting — a stronger recent emphasis on domestic Vietnamese targets.

ESET's June 2026 report describes two 2024-2026 OceanLotus operations that deployed **SPECTRALVIPER**: a selective supply-chain compromise of the FireAnt MetaKit stock-investor platform and a long-running intrusion at a Vietnamese infrastructure and transport construction corporation.

## Tags
- Vietnam-aligned
- APT32
- espionage
- Southeast Asia
- Vietnam
- supply chain compromise
- FireAnt MetaKit
- SPECTRALVIPER
- DLL side-loading
- process injection
- named pipes
- Microsoft SQL Server
- domestic espionage

## Primary motivation
- **Espionage** against strategic, regional, and domestic targets.
- **Selective collection** from high-value victims even when a supply-chain channel could expose a much larger population.
- **Operational access** through custom backdoors, side-loading chains, and orchestration across compromised hosts.

## Naming and attribution
- Use **OceanLotus** as the page title because it is the name used by ESET in the June 2026 report and remains a durable public label.
- **APT32** is a common alias; attribution to Vietnamese state interests should stay source-attributed rather than treated as legal fact.
- ESET describes the 2024-2026 shift as an observed operational pattern, not a final judgment that OceanLotus has permanently changed priorities.

## Core tradecraft
- Custom Windows and Linux backdoors with unusual network protocols or victim-specific data-collection behavior.
- DLL side-loading through renamed signed executables.
- Process injection into legitimate host processes.
- HTTPS command and control with encrypted host profiling embedded in HTTP `Cookie` headers.
- Carefully themed C2 domains that fit victim context, such as finance-themed domains for stock-investor targeting.
- Orchestration among compromised hosts through named pipes, with one SPECTRALVIPER instance acting as the C2-facing coordinator.
- Possible public-facing server exploitation for initial access in enterprise intrusions; ESET specifically suspected Microsoft SQL Server RCE in one Vietnamese infrastructure / transport construction victim network.

## 2024-2026 activity
### FireAnt MetaKit supply-chain compromise
ESET estimates that the FireAnt MetaKit supply-chain attack ran from around **October 2025 through March 2026**. FireAnt MetaKit is part of a Vietnamese stock-market data, analysis, and investment-support platform. ESET observed only a small subset of exposed stock investors ultimately receiving SPECTRALVIPER, suggesting selective targeting despite the broader reach of the update channel.

The chain abused weaknesses in the MetaKit update process:
- the update configuration at `http://metakit.fireant.vn/Software/version.xml` lacked integrity validation;
- update retrieval used HTTP rather than TLS; and
- `Metakit.exe` executed the malicious downloader as if it were a legitimate update.

The downloader performed host reconnaissance, POSTed profiling data to `V1/Update/GetUpdate`, and retrieved the next stage from staging infrastructure that ESET saw move from `139.162.11[.]152` to `142.91.98[.]77`. The next stage side-loaded `DtlCrashCatch.dll` with a renamed signed executable, `IntelAudioService.exe`, then injected SPECTRALVIPER into `OneDrive.Sync.Service.exe`.

ESET reported the SPECTRALVIPER beacon URL `https://financemachinelearning[.]com/apparatus/wind/twig/statement.html` and noted a `zd_cs_pm=` encrypted-cookie prefix in this campaign, a variation from the previously observed `euconsent-v2=` prefix. ESET had not observed further malicious updates through this channel after **2026-03-09**, suggesting the supply-chain phase had probably ended.

### Vietnamese infrastructure / transport construction intrusion
ESET assesses that OceanLotus compromised a Vietnamese infrastructure and transport construction corporation from as early as **November 2024** until **February 2026**. The initial access vector was not directly observed, but ESET's review of public-facing servers suggested possible Microsoft SQL Server remote-code-execution exploitation.

Observed SPECTRALVIPER deployments used renamed signed `Toolbox.exe` variants such as `Genuine.exe`, `Updater.exe`, and `AutoCAD242.exe`, each requiring the `-uiDll` argument for the side-loading mechanism. ESET listed C2 domains including `gatewayrvcenter[.]com`, `coachcybersecurity[.]com`, `mxprodesign[.]com`, and `power-sync-services[.]com`.

## SPECTRALVIPER notes
ESET's 2026 analysis, building on earlier Elastic Security Labs reporting, exposed additional SPECTRALVIPER structure because some samples retained RTTI class names. The backdoor:
- communicates over HTTPS to hardcoded C2 addresses;
- embeds encrypted host-profiling data in cookies prefixed with `euconsent-v2=` or `zd_cs_pm=`;
- can operate as an orchestrator that distributes commands to peer compromised hosts over named pipes;
- includes internal `XGU::Pivot`-style methods for inter-host orchestration; and
- can inject itself, additional binaries, or C2-provided shellcode into target processes.

## Defender signals
- FireAnt MetaKit clients fetching `version.xml` or update binaries over cleartext HTTP, especially around the October 2025-March 2026 window.
- Requests to `V1/Update/GetUpdate` followed by executable staging from `139.162.11[.]152` or `142.91.98[.]77`.
- `Metakit.exe` spawning unexpected update binaries, followed by `IntelAudioService.exe /appmodel /StateRepository /Service` from a user profile path.
- `DtlCrashCatch.dll` side-loaded by a renamed signed binary and injection into `OneDrive.Sync.Service.exe`.
- HTTPS beacons with encrypted host data in Cookie headers using `zd_cs_pm=` or `euconsent-v2=` prefixes.
- Side-loading hosts renamed to environment-plausible names such as `Genuine.exe`, `Updater.exe`, or `AutoCAD242.exe` and launched with `-uiDll`.
- Named-pipe traffic or process-injection behavior connecting multiple compromised hosts where only one host communicates outward to C2.

## Related pages
- [ScarCruft Yanbian game-platform supply-chain attack](../ops/scarcruft-yanbian-game-platform-supply-chain.md)
- [Stock exchange executive mailbox espionage](../ops/stock-exchange-executive-mailbox-espionage.md)
- [Operation Dragon Weave Azure Blob C2 campaign](../ops/operation-dragon-weave-azure-blob-c2.md)

## Sources
- ESET Research: [https://www.welivesecurity.com/en/eset-research/oceanlotus-external-espionage-domestic-targeting/](https://www.welivesecurity.com/en/eset-research/oceanlotus-external-espionage-domestic-targeting/)
- The Hacker News summary: [https://thehackernews.com/2026/06/oceanlotus-hits-vietnam-investors-with.html](https://thehackernews.com/2026/06/oceanlotus-hits-vietnam-investors-with.html)
