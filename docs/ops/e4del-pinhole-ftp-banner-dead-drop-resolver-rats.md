# E4del and PINHOLE RATs use FTP banners as dead drop resolvers

## Summary
SOCRadar (via The Hacker News, August 25, 2026) documented the first in-the-wild campaign to use **FTP banners as dead drop resolvers (DDRs)**: malware stagers fetch the next-stage command directly from the FTP server's initial connection response (banner) instead of from web pages. The technique — MITRE **T1102.001 (Non-Standard Port) / protocol-response exfil-adjacent DDR primitive** — delivers two previously unreported RATs, **E4del** and **PINHOLE**. The modus operandi was first highlighted by MalwareHunterTeam in early July 2026. SOCRadar notes the method is less stealthy than web-based DDRs: FTP connections to unknown servers are typically flagged as anomalous by network controls, but it still blends into legitimate service abuse.

## Tags
- ops
- operations
- E4del
- PINHOLE
- FTP banner
- dead drop resolver
- DDR
- T1102.001
- non-standard protocol abuse
- WebDAV
- ClearFake
- ClickFix
- Electron
- signed binary abuse
- Discord masquerade
- Cloudflare Workers
- PowerShell
- MSXML2.XMLHTTP
- Halo's Gate
- MITRE ATT&CK
- SOCRadar

## E4del chain (Node.js / Electron Discord masquerade)
- **Lure:** Spanish-language voucher-claim pages; victim executes a **Windows LNK** shortcut.
- **DDR:** the LNK retrieves the next-stage command from an **FTP banner** at `157.254.194[.]31:21`.
- **Second banner hop:** the command fetches a second FTP banner from `167.148.41[.]164:21`, which executes **PowerShell** to download, extract, and run a binary from a ZIP archive.
- **Payload:** **E4del**, a **Node.js-based RAT embedded in a digitally signed Electron application masquerading as Discord** — signed-binary abuse plus a familiar consumer-app disguise.
- **Capabilities:** defense evasion, persistence, system fingerprinting, encrypted C2; remote commands include interactive reverse shell, screenshot capture, live desktop streaming, file download, and additional payload delivery.
- **Dynamic beaconing:** tiered jitter with three states based on time since last tasking — **Active** (first 20 s after a command: check-in every 200 ms–2 s), **Semi-Active** (no tasking for 20–40 s: 2–5 s intervals), **Inactive** (after 40 s: 5–9 s intervals).

## PINHOLE chain (more advanced, high-reputation DDRs)
- **DDR:** the FTP banner at `209.99.185[.]38:21` carries commands that use the **`MSXML2.XMLHTTP` COM object inside PowerShell** to retrieve a secondary command script from `hxxps[://]cloudflare.milicare[.]in/app/c`.
- The script is saved as `%TEMP%\u.cmd`, executed, and deleted to minimize forensic footprint.
- **First stage:** a wrapper claiming to be an update utility from a **non-existent company, "Weston Computing Systems Ltd."**; it employs the **Halo's Gate** technique to bypass security software.
- **High-reputation DDRs:** PINHOLE uses **Pinterest and SurveyMonkey** as secondary dead drops to obtain C2 server details, and **proxies C2 communication through Cloudflare Workers** — a trust-layer stack (reputable consumer domains + Cloudflare) on top of the FTP-banner primitive.
- Successful C2 resolution allows querying the domain for a next-stage payload.

## Cross-campaign overlap
- The **WebDAV + LNK + `rundll32.exe` (conhost)** delivery shape in the E4del chain matches the **ClearFake / WordlistLoader → Amatera Stealer** campaign documented by Gen Digital and Microsoft — the same threat cluster compromising legitimate websites and planting fake-CAPTCHA ClickFix lures. Track these as one tradecraft cluster, not separate campaigns.
- Both RATs are new family labels; E4del's signed-Electron-Discord disguise and PINHOLE's Cloudflare-Workers-proxied C2 are distinct enough to warrant separate tracking even where infrastructure overlaps.

## Indicators
- `157.254.194[.]31:21` (E4del primary FTP banner DDR)
- `167.148.41[.]164:21` (E4del secondary FTP banner DDR)
- `209.99.185[.]38:21` (PINHOLE FTP banner DDR)
- `cloudflare.milicare[.]in/app/c` (PINHOLE secondary command script)
- `%TEMP%\u.cmd` (PINHOLE dropped command script)
- "Weston Computing Systems Ltd." (PINHOLE fake-vendor wrapper)
- Spanish-language voucher-claim lures driving LNK execution

## Defender heuristics
1. **Flag FTP client/banner traffic from non-service processes** (explorer, cmd, PowerShell, `rundll32`, LNK-launched binaries) — a malware stager opening an FTP session and parsing the banner is the DDR signature; plain web DDRs won't show this.
2. **Hunt `MSXML2.XMLHTTP` inside PowerShell** — a classic living-off-the-land fetch primitive that bypasses many script-block policies.
3. **Track the WebDAV + LNK + `rundll32` (conhost) shape** as the shared ClearFake/ClickFix tradecraft cluster overlapping this campaign (see WordlistLoader / SynkLoader page).
4. **Treat signed Electron apps masquerading as Discord as hostile** when they arrive via ZIP download from a script-execution chain — check Authenticode, parent process, and spawn tree rather than trusting the signature alone.
5. **Alert on Cloudflare Workers domains resolving after C2 discovery** — PINHOLE proxies C2 through Workers, so the visible hostname is a relay, not the endpoint; resolve the actual destination and re-scope blocklists accordingly.
6. **Watch for tiered beacon jitter** (200 ms→2 s → 2–5 s → 5–9 s) in E4del-style C2, which is tuned to look like normal client polling.

## Related pages
- [WordlistLoader / SynkLoader: new ClearFake loaders delivering Amatera (ACR) Stealer](wordlistloader-synkloader-amatera-clearfake-campaigns.md)
- [ACR Stealer](../tools/acr-stealer.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)

## Sources
- The Hacker News: [E4del and PINHOLE RATs Turn FTP Banners Into Dead Drops for Malware Commands](https://thehackernews.com/2026/08/e4del-and-pinhole-rats-turn-ftp-banners.html)
- SOCRadar: [FTP banners: new dead drop resolver for RATs](https://socradar.io/blog/ftp-banners-new-dead-drop-resolver-rats/)
- MalwareHunterTeam (first MoU highlight, July 2026): [status 2077717345007542539](https://x.com/malwrhunterteam/status/2077717345007542539)
- MITRE ATT&CK: [T1102.001 Non-Standard Port](https://attack.mitre.org/techniques/T1102/001/)
