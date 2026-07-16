# Thailand healthcare RAR / Python stealer campaign

## Summary
Seqrite reported a targeted 2026 campaign against Thailand's healthcare sector, including Ministry of Health personnel and affiliated healthcare organizations. The operation used healthcare-themed spear-phishing lures packaged as malicious RAR archives, obfuscated batch loaders, GitHub-hosted payload retrieval, Windows Startup-folder persistence, a bundled Python runtime, and a Python information stealer that attempted Telegram-based exfiltration.

Seqrite assessed with moderate confidence that the campaign was targeted at Thailand's healthcare ecosystem and observed sample uploads from April 7 through June 3, 2026. Seqrite did not attribute the activity to a named group and said the available evidence did not support definitive attribution.

## Tags
- ops
- operations
- Thailand
- healthcare
- spear phishing
- RAR archives
- batch loader
- Rouki obfuscation
- GitHub payload delivery
- Startup folder persistence
- Python stealer
- Telegram exfiltration
- Windows malware
- no attribution

## Why this matters
- The lures mirror healthcare workflows instead of generic invoice spam: Ministry of Health equipment approvals, hospital admission requests, radiology and dental records, CT scan results, and medical-supply procurement themes.
- The chain mixes low-friction user execution with living-off-the-land components: batch files, PowerShell download cradles, `curl`, Startup-folder persistence, GitHub-hosted stages, and a bundled Python interpreter.
- Manifest or archive-name review is insufficient. The durable pivots are staged script artifacts, Startup-folder writes, `C:\Users\Public\Desktops.zip`, bundled `python` execution, and Telegram Bot API traffic from healthcare endpoints.
- GitHub-hosted payloads let the operator update later stages without changing the initial RAR lure or the persistent Startup-folder script.

## Reported chain
1. A victim receives a healthcare-themed RAR archive such as `Health_Ministry_Approved_Equipment_2026.rar`.
2. The archive contains an obfuscated batch file such as `Health_Ministry_Approved_Equipment_2026.bat`, which writes encoded content to a temporary artifact, uses PowerShell to decode it, and executes a secondary `payload.bat`.
3. `payload.bat` is heavily obfuscated with a framework Seqrite identified as Rouki. It reconstructs PowerShell commands that fetch additional stages from GitHub.
4. One PowerShell path downloads a file masquerading as `up-t2.png` and stores it as `WindowSecuryt.bat` in the user's Windows Startup folder, establishing logon persistence.
5. A second PowerShell path downloads `T2.zip` from GitHub to `C:\Users\Public\Desktops.zip`, extracts it to `C:\Users\Public\Desktops`, and executes the bundled Python payload.
6. The persistent `WindowSecuryt.bat` later uses `curl` to retrieve `u-t2.bat` from `raw.githubusercontent.com`, writes it under the user's temporary directory, and calls it.
7. `u-t2.bat` attempts to relaunch with elevated privileges, then runs `C:\Users\Public\Desktops\python C:\Users\Public\Desktops\Lib\sim.py` with a hidden PowerShell window.
8. `sim.py` acts as a Python-based information stealer. Seqrite reported browser data collection, Chromium-family browser termination, local-file collection, system profiling, screenshot capture, and Telegram Bot API exfiltration attempts.

## Defender heuristics
- Block or detonate RAR archives with healthcare procurement, admission, radiology, dental, CT-scan, or Ministry of Health themes before user delivery.
- Hunt for `cmd.exe`, PowerShell, or `curl` retrieving scripts from GitHub / `raw.githubusercontent.com` after a user opens `.rar`, `.bat`, `.cmd`, or archive-extracted content.
- Monitor user Startup folders for newly written batch scripts, especially names resembling `WindowSecuryt.bat` or scripts with large junk-data sections.
- Alert on creation or execution from `C:\Users\Public\Desktops.zip` and `C:\Users\Public\Desktops\`, particularly bundled `python` execution of `Lib\sim.py`.
- Review browser-kill behavior (`taskkill` against Chrome, Edge, Brave, or other Chromium browsers) followed by Python execution or archive extraction from user-writable paths.
- Treat Telegram Bot API traffic from healthcare workstations as suspicious when preceded by script execution, Python runtime staging, screenshot tooling, or credential-store access.
- Preserve the original RAR, extracted scripts, `%TEMP%` payloads, Startup-folder artifacts, PowerShell logs, and GitHub download URLs before cleanup; the later stages may be updated remotely.

## Public indicators
Seqrite published hashes and additional IOCs. High-level pivots include:

- `Health_Ministry_Approved_Equipment_2026.rar`
- `Health_Ministry_Approved_Equipment_2026.bat`
- `payload.bat`
- `WindowSecuryt.bat`
- `u-t2.bat`
- `Desktops.zip`
- `sim.py` / `SIM.PY`
- GitHub repositories and raw-content paths under `ud-7-te/ud-vtn` and `d7-te/vtn`
- `C:\Users\Public\Desktops.zip`
- `C:\Users\Public\Desktops\python`
- Telegram Bot API exfiltration attempts

## Attribution notes
- Seqrite did not name a known actor for the campaign.
- Seqrite assessed the targeting of Thailand's healthcare sector with moderate confidence, based on lure themes, observed samples, and sample-upload geography.
- The operational consistency across samples may indicate one operator or closely related cluster, but that is not enough for group-level attribution.

## Related pages
- [Operation GriefLure Southeast Asia LNK dropper](operation-grieflure-southeast-asia-lnk-dropper.md)
- [WhatsApp VBScript ManageEngine RMM campaign](whatsapp-vbscript-manageengine-rmm-campaign.md)
- [Stock exchange executive mailbox espionage](stock-exchange-executive-mailbox-espionage.md)

## Sources
- Seqrite Labs: <https://www.seqrite.com/blog/threat-actors-weaponizing-rar-archives-to-target-thailands-healthcare-sector/>
