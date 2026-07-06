# Cavern Manticore

## Summary
**Cavern Manticore** is an Iran-nexus activity cluster tracked by Check Point Research (CPR) in 2026. CPR says the actor targets Israeli organizations, especially government and IT-provider environments, and links the cluster to Iran's Ministry of Intelligence and Security (MOIS) ecosystem with technical overlap to **MuddyWater / Seedworm** and **Lyceum**.

The durable defender value is not a new brand name alone: CPR documented a modular .NET post-exploitation framework, **Cavern**, deployed after abuse of existing Remote Monitoring and Management (RMM) software and built to frustrate triage through mixed .NET Framework, C++/CLI mixed-mode, and .NET 8 NativeAOT compilation.

## Tags
- actors
- Iran
- MOIS
- Cavern Manticore
- MuddyWater
- Seedworm
- Lyceum
- OilRig
- Israel
- government
- IT providers
- espionage
- RMM abuse
- .NET malware
- NativeAOT
- C2 framework

## Public reporting
Check Point Research reported the activity on July 6, 2026, based on intrusions observed since early 2026. CPR assesses Cavern Manticore as an Iran MOIS-linked actor and notes links to Lyceum, which CPR describes as an OilRig subgroup, plus tactical/technical overlap with MuddyWater.

Observed targeting focused on Israeli organizations, particularly government and IT-provider sectors. In multiple intrusions, CPR says the initial foothold came through abuse of RMM software already deployed in the victim organization, after which the operators staged a WinDirStat DLL-sideloading package under `C:\ProgramData\WinDir\`.

## Tradecraft
- Uses legitimate `WinDirStat.exe` to sideload a trojanized `uxtheme.dll` that acts as the Cavern agent.
- Deploys a separate `n-HTCommp.dll` communication module for HTTPS / WebSocket C2 transport.
- Pulls mission-specific post-exploitation modules for file operations, SQL browsing, LDAP / Active Directory reconnaissance, network reconnaissance, SMB credential brute forcing, and SOCKS5 / WebSocket tunneling.
- Relies on per-module AppDomain isolation and post-execution unload to reduce recoverable managed-assembly artifacts.
- Uses numbered DLL versioning and self-update commands so operators can replace modules or the agent without file-name conflicts.
- Newer builds perform startup cleanup, deleting most working-directory contents except the communication module, `config.txt`, and logs.

## Attribution and infrastructure pivots
CPR identified multiple human and infrastructure fingerprints:

- PDB paths referencing `C:\Users\rick\Desktop\Modules\cavern\` across modules.
- C2 infrastructure under `hospitalinstallation[.]com`, including `auth[.]hospitalinstallation[.]com` in older builds and `google[.]com[.]hospitalinstallation[.]com` in newer builds.
- Legacy `Cav3rn` strings in older variants, suggesting a rename from `Cav3rn` to `Cavern` during development.
- Continuity between older non-modular Cav3rn samples and the newer modular framework through command enums, `ApiEx.*` capability organization, and idiosyncratic method names.

Keep attribution caveated at the public-cluster level: CPR links the activity to the Iran/MOIS ecosystem and notes overlap with MuddyWater and Lyceum, but the Cavern Manticore label is the clearest public handle for this specific toolchain and intrusion set.

## Defender notes
- In Israeli, government, IT-provider, and MSP-adjacent environments, treat unexpected RMM-driven deployment of `C:\ProgramData\WinDir\WinDirStat.exe` plus nearby `uxtheme.dll` as high priority.
- Hunt for fake `uxtheme.dll` exports where most theming exports are inert but `EnableThemeDialogTexture` is live, especially when loaded by WinDirStat from non-standard directories.
- Pivot on Cavern mutexes such as `MYMUTEX123HELLP`, `MYMUTEX123HELLP02`, and `MYMUTEX123HELLP04`.
- Look for C2 traffic using the fixed Microsoft Edge User-Agent reported by CPR and `X-User-token` headers carrying an agent ID with a `00` suffix.
- Treat `hospitalinstallation[.]com` subdomains, particularly `google[.]com[.]hospitalinstallation[.]com`, as a high-confidence pivot in the context of the other host artifacts.
- During response, preserve the RMM deployment trail, WinDirStat directory, DLL timestamps, `config.txt`, logs, loaded modules, memory images, and proxy / EDR telemetry before cleaning startup artifacts.

## Related pages
- [Cavern](../tools/cavern.md)
- [Seedworm / MuddyWater](seedworm-muddywater.md)
- [Mistic / KongTuke ModeloRAT activity](../ops/mistic-backdoor-kongtuke-modelorat.md)

## Sources
- Check Point Research: https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/
- The Hacker News: https://thehackernews.com/2026/07/iran-linked-hackers-use-new-cavern-c2.html
