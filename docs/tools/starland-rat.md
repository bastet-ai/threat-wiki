# Starland RAT

## Summary
**Starland RAT** is a Python-based Windows remote-access trojan reported by Cisco Talos in July 2026 and used by [UAT-11795](../actors/uat-11795.md). It is delivered through trojanized installers that bundle `pythonw.exe` and a compiled Python loader disguised as `LICENSE.txt`.

Starland performs anti-analysis checks, establishes persistence, collects host and domain reconnaissance, steals browser and cryptocurrency-wallet material, registers victims with C2 using a hardware identifier, and receives commands to run shellcode, shell commands, or downloaded payloads.

## Tags
- tools
- malware
- RAT
- Python
- Windows
- ClickFix
- trojanized installers
- credential theft
- cryptocurrency theft
- process injection
- Telegram
- Polygon
- UAT-11795

## Why this matters
- The delivery chain deliberately reaches developer and administrator workstations by impersonating tools such as MobaXterm and DBeaver.
- The loader executes a Python RAT in memory from an NSIS installer, which can look like ordinary software installation noise until the bundled Python runtime and `LICENSE.txt` payload are inspected.
- Starland can deploy 32-bit and 64-bit shellcode, run Windows shell commands, and download/execute EXE, MSI, DLL, and ZIP payloads, giving operators an interactive staging point.
- C2 resilience uses both hardcoded C2 domains and a Polygon smart-contract fallback, so simple domain blocking may not be sufficient if the host remains compromised.

## Delivery and execution
- Likely ClickFix social engineering launches a weaponized HTA through `mshta.exe`.
- The HTA drops a batch file in the user profile's application temp area and downloads a trojanized installer from actor-controlled staging.
- The trojanized NSIS installer bundles `pythonw.exe` and a compiled Python loader disguised as `LICENSE.txt`.
- The Python loader uses XOR key `198` / `0xC6` to decrypt the embedded Starland payload and execute it in memory.

## Capabilities
- Anti-analysis checks against sandbox usernames and hostnames, including `WDAGUtilityAccount`, Cuckoo, Any.Run, Joe Sandbox, and Hybrid Analysis artifacts.
- Zone.Identifier check for the trojanized installer in the Downloads folder, apparently to confirm browser-delivery conditions.
- Persistence through a randomized scheduled task named `PythonLauncher-{3 random characters}` and a Startup-folder LNK targeting `pythonw.exe` with `LICENSE.txt` as an argument.
- UAC elevation attempt using `ShellExecuteW` with the `runas` verb.
- Host reconnaissance through `Get-CimInstance`, `wmic memorychip`, SecurityCenter antivirus queries, and Active Directory/domain checks.
- Desktop screenshot capture and staging for victim registration.
- Cryptocurrency-wallet and browser-data theft reported by Talos.
- Commands for 32-bit / 64-bit shellcode execution, Windows shell command execution, payload download/execution, and HTTP 403-triggered self-deletion.

## Network and C2 pivots
- Primary C2 domains reported by Talos: `windowscreenrepairnearme[.]com` and `aipythondevs[.]com`.
- All C2 URLs include a victim hardware identifier derived from the C: drive volume serial number as the final URL path component.
- Fallback C2 is stored XOR-encrypted in Polygon smart contract `0x6ae382ed2154cc84c6672e4e908cd2c69c1b35ba` and retrieved through public JSON-RPC calls.
- Telegram bot `8384531459` / `skuefq_bot` receives installer execution notifications in the reported chain.

## Defender heuristics
- Hunt for recently downloaded trojanized installers that spawn `pythonw.exe` from installer extraction paths or pass `LICENSE.txt` as a Python input.
- Alert on scheduled tasks matching `PythonLauncher-*` created near execution of downloaded installers.
- Review Startup-folder LNK files targeting `pythonw.exe` and unusual `LICENSE.txt` arguments.
- Correlate `mshta.exe` persistence under `HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run` with subsequent Python, PowerShell, Telegram, Polygon RPC, or reported C2-domain traffic.
- Treat affected hosts as credential-exposure incidents and rotate browser-stored, cryptocurrency-wallet, SSH, source-control, cloud, and administrative credentials after evidence preservation and isolation.

## Related pages
- [UAT-11795 Starland / WLDR campaign](../ops/uat-11795-starland-wldr-campaign.md)
- [UAT-11795](../actors/uat-11795.md)
- [WLDR agent](wldr-agent.md)

## Sources
- Cisco Talos: [https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/](https://blog.talosintelligence.com/uat-11795-deploys-novel-starland-rat-and-bespoke-wldr-c2-implant-in-financially-motivated-campaign/)
