# html-to-gutenberg / fetch-page-assets VS Code blockchain stealer

## Summary
JFrog Security Research reported two hijacked npm packages, `html-to-gutenberg@4.2.11` and `fetch-page-assets@1.2.9`, that avoided normal npm lifecycle-script execution and instead hid a VS Code `runOn: "folderOpen"` task in the package tree. The task launched JavaScript disguised as a Font Awesome `.woff2` file, pulled encrypted JavaScript through public blockchain transaction data, connected to attacker infrastructure, opened a `socket.io` backdoor, and deployed a cross-platform Python infostealer.

Both malicious versions were removed from npm before publication of JFrog's June 24, 2026 analysis. Treat developer workstations or CI-like analysis hosts that opened the affected package directory as a trusted VS Code / Cursor workspace as potentially compromised, even if package install scripts were blocked or disabled.

## Tags
- ops
- operations
- supply-chain
- npm
- JavaScript
- Python
- VS Code
- Cursor
- folderOpen
- blockchain C2
- Tron
- Aptos
- BSC
- credential-theft
- infostealer
- developer-targeting
- crypto wallets
- backdoor

## Why this matters
- The trigger did not rely on `preinstall`, `postinstall`, or import-time execution. It relied on editor task auto-execution after a workspace was opened and trusted.
- The malicious code was hidden under `public/fonts/fa-solid-400.woff2`, with leading whitespace that could make the file look blank in a non-wrapping editor.
- Blockchain infrastructure was used as a resilient dead-drop layer: the loader resolved transaction data through TronGrid, Aptos, and BSC JSON-RPC rather than storing the next stage plainly in the package.
- The payload combined immediate broad credential theft with interactive command execution through a `socket.io` backdoor.
- npm v12-style lifecycle-script hardening does not cover editor task execution, workspace trust prompts, or package directories opened for manual investigation.

## Reported chain
1. The attacker published or hijacked malicious versions `html-to-gutenberg@4.2.11` and `fetch-page-assets@1.2.9` on May 25, 2026. JFrog notes that `fetch-page-assets` depends on `html-to-gutenberg` but also carried its own copy of the malware.
2. The malicious package preserved normal-looking metadata and project files while adding a hidden VS Code task named `eslint-check`.
3. The task used `runOptions.runOn: "folderOpen"` and executed `node ./public/fonts/fa-solid-400.woff2` when the package directory itself was opened as a trusted workspace, or when the developer explicitly allowed automatic tasks. JFrog cautions that VS Code and forks do not recursively execute every nested package `.vscode/tasks.json`; the package directory must become the workspace trigger surface.
4. The fake `.woff2` file contained JavaScript and began with 752 space characters, making it appear empty in some editor views.
5. Stage 1 exposed Node internals globally, set a victim/version marker such as `_V = "A8-**"`, and retrieved encrypted payloads.
6. The loader resolved a transaction hash from TronGrid first, fell back to Aptos, then queried BSC JSON-RPC and extracted data after a `?.?` marker in the transaction input. The result was XOR-decoded and run through `eval` or a detached `node -e` process.
7. Stage 2 repeated the blockchain dead-drop retrieval pattern, selected HTTP C2 based on the victim marker, and requested `/$/boot` with the marker in the `Sec-V` header.
8. Stage 3 installed or loaded `axios`, `form-data`, and `socket.io-client`, registered the host, and exposed commands for directory changes, shell execution, clipboard reads, public-IP lookup, file upload, recursive directory upload, forced exit, and arbitrary JavaScript through `ss_eval:` / `ss_eval64:`.
9. Stage 4 created a user-level Node dependency directory under `~/.node_modules`, posted environment details to `/snv`, launched detached Node processes, and built a compact Python loader. On Windows it could fetch `python.zip`, `python.7z`, and `7zr.exe`; on Linux and macOS it could retrieve legitimate PyPA `get-pip.py` as part of dependency setup.
10. Stage 5 executed a reversed-base64 / zlib-obfuscated Python infostealer with Windows, macOS, and Linux collection logic.

## Theft scope
JFrog's deobfuscated payload analysis shows collection logic for:

- Chromium-family browser data from Chrome, Chromium, Opera, Opera GX, Brave, Edge, Arc, Dia, Comet, and Vivaldi, including `Login Data`, `Web Data`, cookies, `Local State`, preferences, and saved payment cards where platform keys were available.
- Firefox profile data, including `key4.db`, `logins.json`, and `cookies.sqlite`.
- Password-manager, authenticator, and wallet browser extensions including 1Password, LastPass, NordPass, RoboForm, Keeper, Proton Pass, Bitwarden, MetaMask, Phantom, TronLink, Trust Wallet, Binance, Coinbase, OKX, Rabby, Keplr, Xverse, Exodus, Safepal, Tonkeeper, Solflare, Zerion, Unisat, ArgentX, Braavos, Nami, Cosmostation, Frontier, Alby, TokenPocket, Lace, Bittensor, and Google Authenticator extension data.
- Local wallet and developer application material including Exodus, Atomic, Electrum, Bitcoin, Dogecoin, Ledger Live, Trezor Suite, Monero, Solana keys, Git credentials, GitHub CLI `hosts.yml`, GitHub Desktop logs, VS Code global storage, Proxifier, WinAuth, Windows Credential Manager, Linux Secret Service, KDE Wallet, macOS keychain material, and cloud-storage folder metadata.
- Process environment variables and other host context useful for follow-on identity or developer-account abuse.

Staging paths reported by JFrog include `%USERPROFILE%\.npm` on Windows and `/tmp/.npm` on Linux and macOS. Data was packed into encrypted zip archives, uploaded to HTTP C2, and optionally uploaded to Telegram; the bot token was returned dynamically by `/u/e` rather than hardcoded.

## Reported indicators and pivots
### Package and detection records
- `html-to-gutenberg@4.2.11` — JFrog Xray `XRAY-1008590`
- `fetch-page-assets@1.2.9` — JFrog Xray `XRAY-1008535`
- Host trigger: `.vscode/tasks.json` containing `runOptions.runOn: "folderOpen"`
- Hidden payload path: `public/fonts/fa-solid-400.woff2`
- Example task label: `eslint-check`
- Example victim marker / header relationship: `_V` value sent as `Sec-V`

### Attacker infrastructure
- C2 IPs reported by JFrog:
  - `166[.]88[.]134[.]62`
  - `198[.]105[.]127[.]210`
  - `23[.]27[.]202[.]27`
- C2 URL patterns:
  - `hxxp[:]//166[.]88[.]134[.]62`
  - `hxxp[:]//166[.]88[.]134[.]62:443`
  - `hxxp[:]//198[.]105[.]127[.]210`
  - `hxxp[:]//198[.]105[.]127[.]210:443`
  - `hxxp[:]//23[.]27[.]202[.]27:443`
  - `hxxp[:]//23[.]27[.]202[.]27:27017`
- C2 paths: `/$/boot`, `/$/{id}`, `/verify-human/{channel}`, `/snv`, `/u/e`, `/u/f`, `/d/python.zip`, `/d/python.7z`, `/d/7zr.exe`
- Legitimate services abused as infrastructure or bootstrap helpers:
  - `api[.]trongrid[.]io`
  - `fullnode[.]mainnet[.]aptoslabs[.]com`
  - `bsc-dataseed[.]binance[.]org`
  - `bsc-rpc[.]publicnode[.]com`
  - `bootstrap[.]pypa[.]io/get-pip.py`
- BSC JSON-RPC method: `eth_getTransactionByHash`
- Tron accounts reported by JFrog: `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP`, `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG`, `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`
- Aptos accounts reported by JFrog: `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e`, `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3`, `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1`
- Telegram upload pattern: `hxxps[:]//api[.]telegram[.]org/bot{telegram_bot_token}/sendDocument`
- Observed Telegram bot-token prefix: `7870147428:AAGbYG...`
- Observed Telegram upload target: `7699029999`

### Runtime artifacts
- `~/.node_modules`
- `%LOCALAPPDATA%\Programs\Python\Python3127`
- `%LOCALAPPDATA%\Programs\Python\Python3127\python.exe`
- `%LOCALAPPDATA%\Programs\Python\Python3127\python.zip`
- `%LOCALAPPDATA%\Programs\Python\Python3127\7zr.exe`
- `%LOCALAPPDATA%\Programs\Python\Python3127\python.7z`
- `/tmp/get-pip.py`
- `%USERPROFILE%\.npm`
- `/tmp/.npm`

## Defender heuristics
### Exposure triage
- Search dependency manifests, lockfiles, package caches, private registry mirrors, SBOMs, build logs, and endpoint telemetry for `html-to-gutenberg@4.2.11` and `fetch-page-assets@1.2.9`.
- Include manual investigation hosts in scope. A workstation that opened an unpacked package directory in VS Code, Cursor, or another compatible editor can be affected even if no lifecycle script ran.
- Review workspace-trust decisions and automatic-task prompts around the exposure window, especially for package directories unpacked for analysis.
- Treat affected hosts as credential-compromise incidents. Rotate npm, GitHub, SSH, cloud, package-registry, browser-saved, password-manager, and wallet material reachable from the host.

### Endpoint hunting
- Hunt for `.vscode/tasks.json` with `runOn: "folderOpen"` executing files under `public/fonts/`, especially `fa-solid-400.woff2`.
- Flag `.woff2` or other asset-looking files that contain JavaScript, long leading whitespace, `eval`, blockchain RPC calls, or Node process spawning.
- Hunt `node` processes querying `api.trongrid.io`, Aptos fullnode APIs, BSC RPC endpoints, or `eth_getTransactionByHash` soon before connections to the reported C2 IPs.
- Hunt `node` installing `axios`, `form-data`, or `socket.io-client` into `~/.node_modules` from an unexpected project context.
- Look for `Sec-V` headers, `/$/boot`, `/$/{id}`, `/verify-human/`, `/snv`, `/u/e`, and `/u/f` traffic from developer endpoints.
- Review unexpected Python downloads or execution from `%LOCALAPPDATA%\Programs\Python\Python3127`, `/tmp/get-pip.py`, and the reported `.npm` staging directories.
- Treat Telegram document uploads from developer endpoints as high-signal if paired with package analysis or editor-task activity.

### Review lessons
- Inspect package tarballs in a read-only viewer before opening their directories as trusted editor workspaces.
- Disable automatic tasks by default and avoid approving folder-open tasks for unfamiliar packages.
- Scan editor configuration inside dependencies, not only root repositories, because analysts may open a suspicious dependency directory directly.
- Extend package-risk scoring beyond manifests and lifecycle scripts to workspace-local editor configuration, asset files that execute through task commands, blockchain RPC staging, and runtime bootstrapper behavior.

## Related pages
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [Astro config blockchain C2 PR injection](astro-config-blockchain-c2-pr-injection.md)
- [wshu.net npm credential-stealer campaign](wshu-net-npm-credential-stealer-campaign.md)
- [postcss-minify-selector-parser npm RAT](postcss-minify-selector-parser-npm-rat.md)

## Sources
- JFrog Security Research: <https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/>
