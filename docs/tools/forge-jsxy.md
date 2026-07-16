# forge-jsxy

## Summary
**forge-jsxy** is an actively maintained malicious npm remote-access tool that continued the earlier `forge-jsx` campaign after npm took the original package down. SafeDep reports that the same operator published `forge-jsxy` under maintainer account `jacksonkaandorp2`, shipped 22 versions from 2026-05-04 through 2026-05-26, and resumed at version `1.0.66`, exactly where `forge-jsx` ended.

The tool is notable because it behaves like a managed endpoint implant rather than a one-off npm stealer: it survives package removal, receives relay-pushed upgrades, steals developer secrets, captures input and screenshots, harvests cryptocurrency wallets and Chromium-extension databases, and uses WebSocket, HTTP, Discord, and Hugging Face channels for control and exfiltration.

## Tags
- tools
- malware
- npm
- supply-chain
- RAT
- keylogger
- credential-theft
- wallet-theft
- Hugging Face
- Discord
- persistence

## Why this matters
- The package was still being actively developed as of SafeDep's 2026-05-26 report, with version `1.0.91` adding browser-extension database theft and auto-upgrade behavior.
- The implant copies itself outside `node_modules`, so uninstalling the npm package does not remove persistence or the running agent.
- The operator uses legitimate developer and collaboration platforms for parts of the workflow: npm for delivery, Hugging Face for bulk exfiltration, Discord webhooks for screenshots, and WebRTC for peer-to-peer file/screenshot transfer.
- Wallet theft is not keyword-only: SafeDep reports checksum/range validation for BIP39 mnemonics, Solana keypairs, and secp256k1 private keys, enabling lower-noise automated theft.

## Operational characteristics
- **Delivery:** npm packages `forge-jsx` and `forge-jsxy`, masquerading as an Autodesk Forge integration layer.
- **Continuity:** `forge-jsxy@1.0.66` appeared within hours of npm replacing `forge-jsx` with `0.0.1-security`; SafeDep links the campaigns through version continuity, package metadata, encrypted C2 configuration, session password, and shared infrastructure.
- **Execution:** a `postinstall` chain runs clipboard/input, build/materialization, bootstrap, and agent scripts on non-CI developer systems.
- **Durable install paths:** `~/.local/share/cfgmgr/.forge-jsxy/` on Linux, `~/Library/Application Support/CfgMgr/data/.forge-jsxy/` on macOS, and `%LOCALAPPDATA%\CfgMgr\data\.forge-jsxy\` on Windows.
- **Persistence:** systemd user service `~/.config/systemd/user/forge-js-worker.service`, macOS LaunchAgent `~/Library/LaunchAgents/com.forgejs.worker.plist`, Windows scheduled task `ForgeJSWorker`, and `HKCU\...\Run\ForgeJSWorker`.
- **Control and exfiltration:** WebSocket relay `ws://204[.]10[.]194[.]247:9877`, HTTP API `hxxp://204[.]10[.]194[.]247:8765`, short-lived Discord webhooks for screenshots, and attacker-controlled Hugging Face repositories for bulk files.
- **C2 infrastructure:** `204.10.194.247` hosted in AS206216 Advin Services LLC, Nürnberg, Germany.
- **Capabilities:** keylogging, clipboard monitoring, `.env` scanning, shell-history collection, host inventory, remote filesystem access, desktop screenshots, wallet/secret scanning, Chromium extension LevelDB harvesting across 21+ browsers, WebRTC data channels, and relay-pushed auto-upgrades.

## Defender heuristics
- Search lockfiles, package-manager caches, developer endpoints, and internal mirrors for `forge-jsx` versions `1.0.0`-`1.0.66` and `forge-jsxy` versions `1.0.66`-`1.0.91`.
- Hunt for durable agent directories, vault paths such as `<durable>/.vault/secret-audit/result.json`, extension staging under `<durable>/.vault/secret-audit/extension-db-staging/`, and the persistence artifacts listed above.
- Treat any host that installed the package as an endpoint compromise: collect evidence, isolate before cleanup, and rotate credentials typed, stored, or available on the host.
- Review developer browsers and wallet extensions; if the latest package versions ran, assume Chromium extension LevelDB databases may have been copied and uploaded.
- Block or alert on traffic to `204.10.194.247` ports `8765` and `9877`, unexpected Discord webhook creation/use, and unusual Hugging Face Hub uploads from developer workstations.
- Do not rely on npm uninstall or dependency cleanup alone; remove the durable copy and OS persistence, then rebuild trusted developer environments where practical.

## Indicators
- Package: `forge-jsxy` versions `1.0.66`-`1.0.91`
- Related package: `forge-jsx` versions `1.0.0`-`1.0.66`
- npm maintainer: `jacksonkaandorp2`
- C2 IP: `204.10.194.247`
- WebSocket relay: `ws://204[.]10[.]194[.]247:9877`
- HTTP API: `hxxp://204[.]10[.]194[.]247:8765`
- Default session password observed by SafeDep: `secret`
- Package artifact SHA-256 for `forge-jsxy@1.0.91`: `4938d47fe6216f8f9fee0527bf5112c04c15a9ea62f87869677619aa5400f09f`
- OSV advisory: `MAL-2026-3609`

## Sources
- [SafeDep](https://safedep.io/malicious-forge-jsxy-npm-rat-evolution/)

