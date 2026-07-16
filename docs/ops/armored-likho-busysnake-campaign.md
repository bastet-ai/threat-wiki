# Armored Likho BusySnake campaign

## Summary
Kaspersky reported an active **Armored Likho** campaign on July 3, 2026 that uses spear-phishing archives, AI-looking loaders, GitHub-hosted staging, Python runtime deployment, and the newly documented **[BusySnake Stealer](../tools/busysnake-stealer.md)** against government and electric-power-sector targets in Russia, Kazakhstan, and Brazil.

## Tags
- ops
- operations
- APT
- spear phishing
- Windows malware
- infostealer
- Python malware
- PyArmor
- LNK
- PowerShell
- GitHub abuse
- scheduled task persistence
- browser credential theft
- cookie theft
- reverse SSH tunneling
- government targeting
- electric power sector
- Armored Likho
- Eagle Werewolf
- BusySnake Stealer

## Campaign flow
1. **Spear phishing:** targets receive archives with themes such as psychological tests, humanitarian aid applications, government notices, social programs, or debt-clearance certificates.
2. **First stage:** archives contain either an NSIS executable or an LNK file. The LNK variant uses command-line hiding associated with ZDI-CAN-25373 and launches a `rundll32.exe` / PowerShell download chain.
3. **Decoy:** victims see a survey application or decoy DOCX while staging continues.
4. **Payload retrieval:** loaders fetch Python 3.12, `get-pip.py`, PyArmor runtime material, `data.zip`, and `module.pyw`, with Kaspersky noting GitHub repository / release abuse for staging and rotation.
5. **Persistence:** the malware builds `%APPDATA%\\WindowsHelper`, creates VBScript helpers, and registers a scheduled task to run BusySnake repeatedly.
6. **Collection and C2:** BusySnake steals browser credentials and cookies, collects screenshots / clipboard / documents / key-like strings, polls for tasks, and can establish reverse SSH tunnels.

## What is durable
- Armored Likho is moving from standalone tunneling tools toward embedding reverse SSH control directly in the stealer.
- Kaspersky says first-stage payload source included verbose comments and emoji-style formatting that strongly suggests LLM-generated code, complicating attribution and loader-signature stability.
- BusySnake's handler architecture and C2 status model overlap with Armored Likho's AquilaRAT tooling, supporting Kaspersky's medium-confidence attribution.
- The newer BusySnake version moved scheduled-task creation into the `Schedule.Service` COM object via `win32com.client`, a quieter persistence implementation than direct `schtasks` command lines.

## Victimology
Kaspersky reports confirmed victims in:

- Russia
- Kazakhstan
- Brazil

Primary sectors called out publicly:

- government agencies
- electric power infrastructure

## Defender response
- Treat a confirmed BusySnake infection as credential compromise. Rotate browser-stored credentials, session cookies, source-control tokens, cloud credentials, VPN credentials, and any secrets stored in user documents or files with long hexadecimal keys.
- Scope for `%APPDATA%\\WindowsHelper`, `module.pyw`, `run.vbs`, `wh_selfdelete.vbs`, Python 3.12 sideload bundles, PyArmor runtime artifacts, and scheduled tasks named like Windows helper / update components.
- Hunt for LNK-to-`rundll32.exe`-to-PowerShell chains, NSIS droppers launching `pnx.exe`, and user-writable Python processes that read Chromium `Login State` / `Login Data`, Firefox `logins.json` / `key4.db`, or browser cookie stores.
- Block or investigate outbound traffic to the public C2 names and IPs published by Kaspersky, including `grked[.]online`, `winupdate[.]live`, `arvax[.]xyz`, `159.198.32[.]222`, and related infrastructure.
- Detect reverse SSH usage with `-R 0.0.0.0:<port>`, disabled host-key checking, and keys supplied at runtime from untrusted infrastructure.

## Sources
- Kaspersky Securelist: [https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/](https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/)
