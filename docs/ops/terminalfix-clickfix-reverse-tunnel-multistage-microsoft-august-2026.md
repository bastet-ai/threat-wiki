# TerminalFix: ClickFix variant deploys a reverse-tunnel implant through a multi-stage chain (Aug 28, 2026)

## Tags
- ops
- operations
- ClickFix
- TerminalFix
- DLL sideloading
- steganography
- reverse tunnel
- Active Directory
- persistence
- reconnaissance
- Microsoft Defender
- PowerShell
- LockScreenContentServer
- pythonw
- WebSocket C2
- gitnow

## Summary

Microsoft Threat Intelligence reported on **August 28, 2026** (published UTC 2026-08-29T03:43Z) a new ClickFix campaign it labels **TerminalFix**. The campaign targets organizations across multiple industries and deploys a sophisticated multi-stage attack chain: DLL sideloading, steganographic payload extraction, extensive Active Directory reconnaissance, and a custom Python reverse-tunnel implant that gives the attacker full SOCKS-style TCP proxy access through the compromised host.

Unlike classic ClickFix campaigns that direct victims to the Windows **Run** dialog, TerminalFix directs users to **Windows Terminal** or **PowerShell**, increasing the likelihood that complex multi-line scripts execute successfully. The initial lure is a fake **Cloudflare Turnstile CAPTCHA** overlay on a compromised website (`hxxps://linked-log[.]com/`).

## Attack chain

1. **Initial access (drive-by / social engineering):** A compromised website displays a fake Cloudflare Turnstile verification overlay. The user is instructed to copy a "verification" PowerShell command to their clipboard.
2. **PowerShell execution:** The pasted command masquerades as a Cloudflare verification process. It clears the terminal, prints fake status messages, downloads a ZIP archive (`SHA-256: 18c2090e8a0ae0568af9b87e59eaf8270f23d2909600ed9db91a9444fd8b278f`) from attacker infrastructure to `C:\ProgramData\f47f2a8c21c9df4e`, and silently launches `1.bat`.
3. **DLL sideloading:** `1.bat` executes `LockScreenContentServer.exe` (a legitimate signed Windows binary). The attacker's `dui70.dll` (masquerading as "Windows DirectUI Engine", unsigned, forged future timestamp 2104) is loaded from the working directory via the static import dependency. This is **T1574.002 Hijack Execution Flow: DLL Side-Loading**.
4. **Steganographic payload retrieval:** The sideloaded DLL's resource section decodes in memory and executes a PowerShell script that downloads three PNG images from two content domains (`bestsocialmedianewspapper[.]com` and `offlineupdater[.]com`) with failover. An `Extract-RawFileFromImage` function reads RGBA pixel channels; the first 8 bytes encode payload length as a 64-bit integer. An executable is extracted from the first image and a DLL is split across the second and third images, then concatenated. Source images are deleted.
5. **Persistence:** Dual persistence under the masquerading name `LockScreenContentServer_MuODG5yBM`:
   - `HKCU\...\Run` registry key (T1547.001)
   - Scheduled task re-executing `LockScreenContentServer.exe` every 60 minutes (T1053.005)
   - Payload directory hidden with `attrib +h +s` (T1564.001)
6. **Reconnaissance / AD enumeration:** Domain trust discovery (`nltest /domain_trusts`, `/dclist`), domain admin group enumeration (`net group "domain admins" /domain`), Active Directory user and computer enumeration via ADSI searcher including user-description harvesting, and targeted ping sweeps of common infrastructure roles (domain controllers, databases, backup, gateways, mail). System-information collection includes English, Spanish, and German locale variants.
7. **Asynchronous command execution loop:** A PowerShell file-watch loop monitors a "watch" text file for new commands, executes via `Invoke-Expression`, and writes results to an output file — a primitive asynchronous C2 channel.
8. **Reverse-tunnel deployment:** A signed embeddable **Python 3.14.5** runtime is downloaded from python.org over TLS 1.2 and a custom `client.py` implant is launched with `pythonw.exe` (no visible window). The implant dials outbound to **`gitnow[.]dev:443`** over TLS, upgrades to WebSocket at `/tunnel`, disables certificate verification (`CERT_NONE`), and relays arbitrary TCP connections on behalf of the operator — a full SOCKS-style pivot. A 7-byte binary protocol header (type + stream ID + length) multiplexes connections. The C2 can remotely terminate the implant via `MSG_SHUTDOWN` (`os._exit()`).

## Indicators of Compromise

**Files (SHA-256):**
- `18c2090e8a0ae0568af9b87e59eaf8270f23d2909600ed9db91a9444fd8b278f` — initial ZIP archive (`verify_pkg.zip`)
- `b8d107800403b9197e5b7609ceacd8e4cac1b0f9a1d156e6dacd6c3f7794b36a` — custom tunnel implant (`client.py`)
- `ba77feed86bcda49308746421bdc684a432dd5d68c363975b2a3c6831bda3f07`
- `026478003fe354134c03acf6890e7d3b153ba08a836eca42350db48f213872ab`
- `032b529fac61e550f5dc9489686f519b82d64625fa05a8d9ecf8ba8be9b2ad22`
- `df8221a933b38284ebdcb8bffc2df62123c9f5b5f421dd0b070e13e668b3eabf`
- `eb1b4be34d05b394fb74efdeb95faecd1d1963be6ecc1b9db2b4757b491f01f0`
- `5d43abf5c36ea203176d3300ff14af27b4be81810ad2679b3a62b255e3d6e1c8`
- `9a7b4dcd51d9251c177d323d6aaecdfc86674f69bc1af048dc872926d22aaa24`
- `342df92235c9dec81203b837addaa38bb85b64b4a48fe71b5303ca86d991991e`
- `ededeacf30e493dd632d477fe770ba419aa2848f685ea049381a0a8d2cc3e84d`
(all listed `dui70.dll` variants)

**Network:**
- `gitnow[.]dev` — C2 server for the custom reverse-tunnel implant (port 443)
- `bestsocialmedianewspapper[.]com` — steganographic image hosting / payload delivery
- `offlineupdater[.]com` — steganographic image hosting / failover
- `hxxps://linked-log[.]com/` — compromised website (initial access)

**Filesystem:**
- `C:\ProgramData\f47f2a8c21c9df4e\` — payload directory
- `1.bat` — initial batch launcher
- `LockScreenContentServer.exe` — sideloading host
- `dui70.dll` — malicious DLL

**MITRE ATT&CK:** T1189, T1059.001, T1204.002, T1547.001, T1053.005, T1574.002, T1027.003, T1564.001, T1036.005, T1018, T1069.002, T1482, T1087.002, T1082, T1572, T1071.001, T1105.

## Am I affected?

- **Defender XDR (Microsoft):** Run the advanced-hunting queries from the post — `LockScreenContentServer.exe` sideloading from non-standard paths, `powershell.exe` → `cmd.exe` with `1.bat`/`LockScreenContentServer.exe` in `ProcessCommandLine`, `pythonw.exe`/`python.exe` with `client.py --server --uuid cert.pem gitnow.dev` in `ProcessCommandLine`, and `DeviceNetworkEvents` to `gitnow.dev` / `bestsocialmedianewspapper.com` / `offlineupdater.com`.
- **Generic:** hunt for `LockScreenContentServer.exe` outside `C:\Windows\SystemApps\`, `dui70.dll` co-located with it, a `C:\ProgramData\f47f2a8c21c9df4e\` directory, `pythonw.exe` running `client.py`, and outbound TLS/WebSocket to `gitnow.dev`.
- **Treat affected hosts as network pivot points** — the reverse tunnel gives the attacker SOCKS-style access to everything reachable from the victim. Assume lateral movement and credential exposure, especially if the host was domain-joined.

## Recovery

- Isolate the host and **rotate credentials accessible from it**, prioritizing domain admin accounts if domain-joined.
- Remove `C:\ProgramData\f47f2a8c21c9df4e\`, the `dui70.dll` copy, and any `LockScreenContentServer_MuODG5yBM` registry / scheduled-task persistence.
- Review the AD reconnaissance footprint (user descriptions, domain trusts, server ping sweeps) for follow-on targeting.
- Educate users about fake CAPTCHA / verification overlays that instruct pasting commands into Windows Terminal or the Run dialog.
- Restrict PowerShell execution for standard users (AppLocker / App Control / GPO); enable Windows Terminal multi-line paste warnings.

## Why this matters

- **ClickFix is evolving:** the shift from the Run dialog to Windows Terminal / PowerShell is a meaningful capability upgrade — multi-line scripts execute reliably, enabling complex multi-stage chains that the classic single-paste ClickFix pattern cannot.
- **Steganography over split PNGs** is a strong detection-evasion primitive: payloads are not recognizable as executables in transit and the split makes content inspection harder.
- **The reverse-tunnel implant** turns any compromised host into a network pivot. Combined with the AD reconnaissance, a single terminal infection gives the attacker a persistent, network-level proxy back into the victim's environment — the classic pre-ransomware foothold.
- **The Python-embeddable-runtime technique** is notable: the attacker ships an unmodified, signed python.org runtime and keeps all malicious logic in a user-space `client.py`, inheriting the trust of a legitimate open-source runtime.

## Related pages

- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [macOS ClickFix fingerprinting-gate campaign](macos-clickfix-fingerprinting-gate-campaign.md)
- [OX ClickFix-in-npm / registry-mirror payload storage](ox-clickfix-phishing-npm-mirror-payload-storage.md)
- [TELEPUZ ClickFix → VIDAR campaign](telepuz-clickfix-vidar-campaign.md)

## Sources

- Microsoft Security Blog — "TerminalFix campaign deploys a reverse tunnel through multistage intrusion" (Microsoft Threat Intelligence, Sagar Patil, Suriyaraj Natarajan, Parasharan Raghavan; published 2026-08-28, UTC 2026-08-29T03:43Z): [https://www.microsoft.com/en-us/security/blog/2026/08/28/terminalfix-campaign-deploys-reverse-tunnel-through-multistage-intrusion/](https://www.microsoft.com/en-us/security/blog/2026/08/28/terminalfix-campaign-deploys-reverse-tunnel-through-multistage-intrusion/)
