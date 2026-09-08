# NodeRabbit

## Summary
**NodeRabbit** is a cross-platform remote access trojan written in **Node.js**, attributed by Kaspersky GReAT to **Mirage Kitten**. It targets **Windows, Linux, macOS, and WSL**. It is one of the group's first publicly documented Node.js/JavaScript-based implants, departing from its historical native (C/C++/Go) DLL-search-order-hijacking malware. Kaspersky detected it as `Trojan.JS.MirageKitten.*`.

## Tags
- tool
- tools
- NodeRabbit
- Mirage Kitten
- UNC1549
- Node.js
- cross-platform
- Windows
- Linux
- macOS
- WSL
- RAT
- backdoor
- trojanized coding challenge
- bundled npm package
- persistence
- Git hook
- VS Code extension
- Azure Websites C2

## Delivery
- Delivered inside **trojanized "coding challenge" archives** (e.g. a `Front-Technical-Challenge.zip` "TaskFlow" Express/React/Vite project) hosted on **Amazon S3**, reached through recruiter-themed outreach on LinkedIn and other job-search platforms.
- The challenge's `server.js` first line imports a **bundled, registry-absent npm package** (`colorized_terminal` v2.1.0, later variants use `pretty-log` v2.1.0). The package is placed directly in the challenge's `node_modules/` (not published to the npm registry) and silently launches the implant from `node_modules/.cache/.320697f1/index.js` as a detached background process.
- The README explicitly tells the candidate that `server.js` is "bug-free" and must not be modified, and bans AI assistants / imposes a time limit — steering attention away from the one altered file.

## Agent identity and anti-analysis
- Generates a unique agent ID: SHA-256 of hostname + username + OS version + architecture + MAC address, truncated to the first 32 hex characters.
- **Variant 1** binds a TCP listener to `127.0.0.1:48739` as a single-instance check (exits silently if the port is taken).
- **Variant 2** adds anti-analysis: terminates if it sees low memory, low CPU count, short uptime, analyst-associated user/hostnames, or common analysis tools; before exiting it issues benign `HEAD` requests to `www.google.com`, `www.microsoft.com`, and `www.cloudflare.com`.
- **Variant 2** adds corporate-proxy support: reads HTTP(S) proxy env vars, Windows Internet Settings (incl. explicit PAC URL), and WinHTTP config; tunnels HTTPS C2 through `HTTP CONNECT`; falls back to `curl.exe --proxy-anyauth --proxy-user` for NTLM/Negotiate; caches proxy discovery for five minutes and re-discovers on NIC/IP change.
- **Variant 2** single-instance port: `41984 + (first 4 hex chars of agent ID as int, mod 5000)` → range `41984`–`46983`, host-specific.

## Persistence (per platform)
| Platform | Variant 1 | Variant 2 | Variant 3 |
| --- | --- | --- | --- |
| Windows | `%APPDATA%\Microsoft\EdgeUpdate\msedge_update.js`; clone local `node.exe` → `nodew.exe`, patch PE subsystem Console→GUI; `HKCU\...\Run\MicrosoftEdgeUpdate` | `%LOCALAPPDATA%\Intel\DSA\idriver_support.js`; clone `node.exe` → `IntelDSA.exe` (PE GUI); scheduled task **IntelDriverSupportUpdate** daily 10AM | ProgramData (`/ru SYSTEM /rl highest`, chosen by probing `C:\Windows\System32\config`) or LocalAppData; build-specific daily 10AM task |
| Linux | `~/.config/microsoft-edge-update/msedge_update.js` + `@reboot` cron | `~/.config/intel-dsa/idriver_support.js` + `@reboot` cron | `~/.local/share` payload + `@reboot` cron (skipped if `crontab -l` fails) |
| macOS | `~/Library/LaunchAgents/com.microsoft.edgeupdate.plist` (RunAtLoad+KeepAlive) | `com.intel.dsa.helper` LaunchAgent (RunAtLoad+KeepAlive) | LaunchAgent RunAtLoad/KeepAlive |
| WSL | — | — | Reuses the Linux payload; writes `launcher.vbs` under the Windows profile + daily 10AM Windows task relaunching via `wscript.exe` + `wsl.exe` |

## C2 and commands
- **Variant 1** Azure-hosted C2 chain: `plugplay.azurewebsites[.]net`, `Rgbteller.azurewebsites[.]net`, `Wslwebui.azurewebsites[.]net` (falls over the chain on failure). Endpoints: `POST /api/rabbit/checkin`, `POST /api/rabbit/task`, `POST /api/rabbit/result`.
- **Variant 3** C2 chain (Azure + Cloudflare): `visitfinancedentists[.]com`, `kyrasey-f8hfexa5cqamh7fk.westeurope-01.azurewebsites[.]net`, `healthcomfsdpower[.]com`. Endpoints: `POST /sdk/v2/ready`, `POST /sdk/v2/config`, `POST /sdk/v2/events`.
- C2 serialization: JSON wrapped in **AES-256-GCM**; the key is the SHA-256 digest of an ASCII seed embedded in the agent; fresh 12-byte IV + 16-byte tag per request. Wire structure `{"d":"base64(IV||ciphertext||tag)","_r":"<8 hex>","_t":"<epoch>"}`.
- **Variant 1 commands (11):** `sys:info`, `proc:list`, `proc:start`, `fs:list`, `fs:read`, `fs:write`, `fs:delete`, `fs:mkdir`, `net:config`, `agent:sleep`, `script:exec` (write+run+delete a Base64 Node.js script to a random `.tmp` file).
- **Variant 3 adds 12 more (23 total):** `fs:drives`, `proc:exec`, `proc:kill`, `agent:servers` (replace live C2 list, can persist to `.sv.json`), `agent:getchain`, `outlook:emails` (harvest addresses from Outlook OST/PST), `persist:check`, `persist:vscode`, `persist:vscode:remove`, `persist:projects:scan`, `persist:project:inject`, `persist:project:remove`.
- **Variant 3 developer-workflow persistence:** `persist:vscode` drops a fake VS Code extension displayed as **"GitHub Copilot Helper"** (activation `onStartupFinished`, spoofed trusted publisher name from local extension metadata / `trustedPublishers` in `state.vscdb`, no signature copied; also disables Workspace Trust and adds a Run key). `persist:project:inject` scans recent VS Code workspace paths (`~/projects`, `~/source`; first 60 immediate children, up to 20 repos) and appends a marked launcher to `.git/hooks/post-merge` and `.git/hooks/post-checkout` under the `# shepherd-persist` marker.

## Public indicators
### Lure / archive
- `Front-Technical-Challenge.zip` MD5 `1EA83E4E4592B01E4ACAB63EB867BEE5`
- Lure host: `oracle-challenge.s3[.]us-east-1.amazonaws[.]com`
- Bundled trojanized packages: `colorized_terminal@2.1.0`, `pretty-log@2.1.0`; implant at `node_modules/.cache/.320697f1/index.js`

### C2 domains
- `plugplay.azurewebsites[.]net`, `rgbteller.azurewebsites[.]net`, `wslwebui.azurewebsites[.]net`
- `healthcomfsdpower[.]com`, `visitfinancedentists[.]com`, `kyrasey-f8hfexa5cqamh7fk.westeurope-01.azurewebsites[.]net`

## Detection pivots
- A `node`/`node.exe` (or renamed `nodew.exe`/`IntelDSA.exe` with PE subsystem patched to GUI) spawning from a project's `node_modules/.cache/` path, or importing a non-registry `colorized_terminal`/`pretty-log` package, after a "coding challenge" archive.
- The fixed `127.0.0.1:48739` single-instance port (Variant 1) or host-specific listener in `41984`–`46983` (Variant 2).
- Persistence named `MicrosoftEdgeUpdate`, `IntelDriverSupportUpdate`, `com.microsoft.edgeupdate`, `com.intel.dsa.helper`.
- Outbound HTTPS to the listed Azure/Cloudflare C2 domains, especially with the `{"d":…,"_r":…,"_t":…}` AES-GCM body shape.
- A fake "GitHub Copilot Helper" VS Code extension, or a `# shepherd-persist` line appended to `.git/hooks/post-merge` / `post-checkout` in repositories under the developer's control.

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [Mirage Kitten NodeRabbit / PollCat coding-challenge campaign](../ops/mirage-kitten-noderabbit-pollcat-coding-challenge-september-2026.md)
- [PollCat](pollcat.md)

## Sources
- Kaspersky GReAT, September 1, 2026: [Mirage Kitten targeting aviation and FinTech sectors across the Middle East and Africa with a new malware set](https://securelist.com/mirage-kitten-new-backdoors-noderabbit-pollcat/121244/)
