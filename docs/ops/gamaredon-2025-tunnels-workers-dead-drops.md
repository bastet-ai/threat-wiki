# Gamaredon 2025 tunnels, workers, dead drops, and cloud exfiltration

## Summary
ESET's June 25, 2026 research summarizes **Gamaredon** activity during 2025: sustained cyberespionage against Ukrainian government and military institutions, 35 observed spear-phishing campaigns, new PowerShell tooling, resumed VBScript weaponization, and heavier dependence on legitimate online services for C2 discovery, payload staging, infrastructure hiding, and exfiltration.

The update matters because it reframes Gamaredon as an operator that wins through operational tempo and service abuse rather than sophisticated malware alone. By late 2025, ESET says Gamaredon was chaining dead drops to tunnels/workers and moving stolen files into S3-compatible cloud storage, making disruption and network allow/block decisions harder for defenders.

## Tags
- ops
- operations
- Russia
- FSB
- Ukraine
- Gamaredon
- UAC-0010
- espionage
- Turla
- Cloudflare Tunnel
- Cloudflare Workers
- Microsoft dev tunnels
- Loophole
- DDNS
- No-IP
- Supabase
- Clever Cloud
- Telegram
- Telegra.ph
- Teletype
- Rentry
- Dropbox
- GoFile
- Wasabi
- Tebi
- Intercolo
- S3-compatible storage
- PteroPaste
- PteroSetup
- PteroVDoor
- PteroPSDoor
- PteroBox
- CVE-2025-8088
- WinRAR
- HTML smuggling
- HTA
- VBScript
- PowerShell
- USB weaponizer
- lateral movement
- cloud service abuse
- dead drop resolver

## Why this matters
- ESET observed **35 distinct 2025 spear-phishing campaigns** against Ukrainian government and military targets, with larger and more frequent campaigns in the second half of the year.
- From September 26, 2025 onward, Gamaredon abused **WinRAR CVE-2025-8088** to place HTA downloaders in the victim Startup folder, adding login-time execution to chains that had relied more on user interaction.
- ESET reports a **Gamaredon / Turla collaboration** in early 2025 and a prior InvisiMole collaboration, so Russia-aligned incident scoping should not assume Gamaredon intrusions remain single-actor after initial access.
- Gamaredon expanded infrastructure hiding from Cloudflare tunnels into workers, Microsoft `devtunnels.ms`, Loophole, DDNS, PaaS services, and layered dead drops that point to already-hidden infrastructure.
- File exfiltration shifted toward third-party cloud storage: ESET says upgraded **PteroVDoor** and **PteroPSDoor** moved from Wasabi to Tebi and then Intercolo S3-compatible storage, while **PteroBox** continued Dropbox uploads and one newer variant used `rclone`.

## 2025 activity and tooling
- **Targeting:** ESET says Gamaredon exclusively targeted Ukrainian governmental and military institutions throughout 2025.
- **Initial access:** campaigns used archive attachments or XHTML/HTML-smuggling lures to deliver malicious HTA downloaders, and some campaigns likely used malicious hyperlinks instead of attachments.
- **New tools:** ESET describes six new PowerShell tools. `PteroDee` and `PteroCache` fetch/execute PowerShell payloads in memory; `PteroDum` handles VBScript payloads; `PteroOdd` retrieves a PowerShell payload through the Telegra.ph API; `PteroEffigy` uses GoFile to obtain the next C2 server; and `PteroPaste` combines downloader, USB weaponizer, and runner/orchestration behavior.
- **PteroPaste evolution:** early versions used Rentry for encrypted payload staging; later versions retrieved an encrypted C2 hostname from Dropbox, decrypted it locally, and connected to infrastructure hidden behind tunnel services.
- **PteroSetup revival:** ESET says Gamaredon resurrected an older VBScript weaponizer that scans fixed, removable, and network drives for installer-like executables and replaces them with self-extracting archives that run both the original installer and malicious VBScript.
- **Existing tool updates:** ESET also points to updates in `PteroLNK`, `PteroPSLoad`, `PteroPSDoor`, `PteroVDoor`, and `PteroBox` in its white paper.

## Infrastructure shifts
- **Tunnels and workers:** by the end of 2024 Gamaredon already relied on `trycloudflare.com`; in 2025 it added `workers.dev`, Microsoft `devtunnels.ms`, and `loophole.site`, often with primary and fallback paths. ESET also saw isolated experiments with `loca.lt` and `bore.pub`.
- **DDNS / PaaS:** ESET observed renewed No-IP dynamic DNS use and abuse of Clever Cloud (`cleverapps.io`) and Supabase (`supabase.co`) for disposable infrastructure that blends with legitimate traffic.
- **Dead drops:** services abused for C2 resolution, payload delivery, or cloud-storage configuration included Telegram / `t.me`, Telegra.ph, Teletype, Rentry, write.as, Dropbox, GoFile, DEV Community, Mastodon, lesma, nopaste.net, and Paste.ee.
- **Layering change:** ESET says 2025 dead drops increasingly pointed to infrastructure already hidden behind tunnels or workers rather than revealing raw C2 IPs.
- **Cloud exfiltration:** Gamaredon increasingly used third-party cloud storage not just for staging but for receiving stolen data, reducing the need to maintain obvious attacker-owned collection infrastructure.

## Defender notes
- Inventory and patch WinRAR independently of Windows patch tooling; ESET and Trend Micro both show CVE-2025-8088 remained operationally useful months after patch availability.
- Hunt for HTA files written to user Startup paths after archive or XHTML lure handling, especially followed by `mshta.exe`, `wscript.exe`, or PowerShell execution.
- Treat requests from script interpreters or unusual userland processes to tunnel/worker/DDNS/dead-drop services as a hunting pivot, but avoid brittle blocklists because Gamaredon uses legitimate services extensively.
- Watch for USB, mapped-drive, and installer weaponization: hidden/replaced files, `.lnk` launchers, suspicious self-extracting archives, and user-executed installers that also spawn VBScript.
- Monitor cloud-storage uploads from endpoints that normally should not use S3-compatible storage, Dropbox, GoFile, or rclone; preserve local config and registry artifacts before remediation.
- In Russia-linked Ukraine intrusions, scope for possible Turla follow-on tooling or access handoff when Gamaredon artifacts are present.

## Related pages
- [Gamaredon](../actors/gamaredon.md)
- [Gamaredon GammaPhish / GammaWorm / GammaSteel chain](gamaredon-gammaphish-gammaworm-gammasteel-chain.md)
- [Turla](../actors/turla.md)
- [Turla STOCKSTAY backdoor operations](turla-stockstay-backdoor-operations.md)

## Sources
- [ESET WeLiveSecurity](https://www.welivesecurity.com/en/eset-research/gamaredon-2025-leveraging-tunnels-workers-dead-drops-new-alliances/)
