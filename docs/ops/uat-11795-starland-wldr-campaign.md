# UAT-11795 Starland / WLDR campaign

## Summary
Cisco Talos disclosed **UAT-11795** on July 16, 2026: a Russian-speaking, financially motivated actor active since at least June 2025 and targeting users in the United States and Europe with ClickFix-style social engineering and trojanized installers. The campaign delivers [Starland RAT](../tools/starland-rat.md), a Python-based Windows RAT, and can deploy [WLDR agent](../tools/wldr-agent.md), CastleStealer, and Remcos RAT as follow-on payloads.

This is durable defender intel because the campaign blends multiple high-signal workstation risks: fake installer distribution for developer/admin tooling, HTA and `mshta.exe` persistence, bundled Python runtime execution, PowerShell memory-resident C2, Telegram notification infrastructure, and Polygon smart-contract fallback C2.

## Tags
- ops
- operations
- cybercrime
- ClickFix
- trojanized installers
- HTA
- mshta
- Python
- PowerShell
- RAT
- credential theft
- cryptocurrency theft
- Starland RAT
- WLDR agent
- UAT-11795
- Cisco Talos

## Why this matters
- Trojanized MobaXterm and DBeaver-style lures can land on systems with SSH keys, database credentials, cloud tokens, source-code access, and administrative reach.
- The chain persists before C2 registration, so blocked first-contact traffic does not prove the host is clean.
- Starland can receive shellcode, shell commands, EXE/MSI/DLL/ZIP payloads, and a self-delete instruction, giving the actor flexible post-exploitation control.
- WLDR adds an in-memory PowerShell C2 layer with encrypted tasking and Runspace execution, making script-block, memory, and network telemetry important.

## Victimology and lures
Talos reports telemetry primarily in the United States, with lower-volume potential impact in Germany, Romania, and Venezuela. The trojanized installer set spans multiple user profiles:

| Trojanized installer | Impersonated software | Target profile |
| --- | --- | --- |
| `MobaXterm_v26.1.exe` | MobaXterm | SSH, remote desktop, and network administration users. |
| `WebEx_Client.exe` and Zoom installer | WebEx / Zoom | Enterprise collaboration users. |
| `dbeaver-ce-windows-x86_64.exe` | DBeaver Community Edition | Database administrators and developers. |
| `FaceitInstaller_x64.exe` | FACEIT | Consumer gaming users. |

## Infection chain
1. **Initial lure:** likely ClickFix social engineering persuades the victim to run a command that launches a remote HTA through Microsoft HTML Application Host (`mshta.exe`).
2. **HTA / VBScript stage:** the HTA drops a batch file into the user profile's application temp area and downloads a trojanized installer from actor-controlled staging.
3. **First persistence:** the VBScript creates `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run` value `MyApp` pointing back to `mshta.exe` and the hosted HTA for logon re-execution. Talos found a Russian-language developer comment in this stage.
4. **Installer execution:** the NSIS installer runs a bundled `pythonw.exe` against a compiled Python loader disguised as `LICENSE.txt`.
5. **Starland launch:** the Python loader uses XOR key `198` / `0xC6` to decrypt and execute Starland RAT in memory.
6. **Victim registration and tasking:** Starland fingerprints the host, collects reconnaissance and screenshot data, registers with C2 using an HWID path component, and receives commands for shellcode, shell, downloads, or self-deletion.
7. **Follow-on payloads:** Talos observed a command that downloaded WLDR C2 PowerShell stages; Talos also reports CastleStealer and Remcos RAT payload capability through custom shellcode loaders.

## Tooling and payloads
- **Starland RAT:** Python RAT with anti-analysis checks, scheduled-task / Startup-folder persistence, UAC elevation attempt, host/domain reconnaissance, screenshot capture, browser and cryptocurrency-wallet theft, Polygon fallback C2, and flexible payload execution.
- **WLDR agent:** PowerShell C2 memory implant with encrypted beaconing, WMI reconnaissance, 10-second HTTPS polling, task queues, and RunspacePool execution.
- **CastleStealer:** .NET infostealer reported by Talos as targeting Chromium-family and Firefox browser data, crypto wallet extensions, Discord and Telegram sessions, Steam credentials, and selected filesystem paths. Talos notes a Russian-locale exclusion and build-expiry timestamp.
- **Remcos RAT:** commercially available RAT abused as a follow-on payload; Talos reports x32 shellcode delivery in this campaign.

## Infrastructure and indicators

| Type | Indicator | Notes |
| --- | --- | --- |
| Domain | `eorthopaedics[.]com` | Likely hijacked; hosts PowerShell stage chain under `/feed/` and can serve HWID-bound C2 envelopes. |
| Domain | `sastoro[.]com` | Hosts PowerShell stage chain under `/alpha/` and parallel HWID-bound C2. |
| Domain | `web-devtools[.]com` | Shellcode / archive staging; paths include `/starlandfox`, `/x32remka`, and `/dopfile`. |
| Domain | `zynaris[.]io` | HTA stager and trojanized-installer lure hosting. |
| Domain | `windowscreenrepairnearme[.]com` | Starland primary C2; likely hijacked according to Talos. |
| Domain | `aipythondevs[.]com` | Starland primary C2. |
| Polygon contract | `0x6ae382ed2154cc84c6672e4e908cd2c69c1b35ba` | XOR-encrypted fallback C2 domain storage. |
| Telegram bot | `8384531459` / `skuefq_bot` | Execution notification beacons. |
| Telegram bot | `7993597060` / `komandastuk_bot` | Notification / inventory reporting. |
| Registry | `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\MyApp` | HTA persistence through `mshta.exe`. |
| Scheduled task | `PythonLauncher-*` | Starland persistence pattern. |
| File argument | `LICENSE.txt` | Compiled Python loader disguised as a license file. |
| Password | `odg5t8mvssvh` | WLDR loader decryption password reported by Talos. |

## Detection and response guidance
- Hunt for browser or shell-initiated `mshta.exe` executions followed by downloaded HTA/VBScript, temp batch files, and installer execution.
- Diff suspicious NSIS installers for bundled `pythonw.exe`, unusual `LICENSE.txt` bytecode, or NSI script instructions that run the disguised loader.
- Search EDR and Windows telemetry for scheduled tasks named `PythonLauncher-*`, Startup-folder LNKs targeting `pythonw.exe`, and `ShellExecuteW` / `runas` elevation attempts following installer launch.
- Monitor for PowerShell WMI reconnaissance, encrypted HTTPS polling every ~10 seconds, Chrome 124-like headers, and C2 URL path components derived from C: drive volume serial numbers.
- Treat detections as full workstation compromise. Preserve installer, HTA, PowerShell, memory, process, registry, scheduled-task, browser, and network evidence before cleanup.
- Rotate credentials reachable from the user and host after isolation: browser-stored credentials, cryptocurrency wallets, SSH keys, Git/source-control tokens, database credentials, cloud credentials, messaging sessions, and administrative credentials.

## Related pages
- [UAT-11795](../actors/uat-11795.md)
- [Starland RAT](../tools/starland-rat.md)
- [WLDR agent](../tools/wldr-agent.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)

## Sources
- Cisco Talos: [https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/](https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/)
