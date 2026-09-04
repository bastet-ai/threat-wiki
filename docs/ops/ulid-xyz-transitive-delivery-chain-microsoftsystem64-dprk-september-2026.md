# ulid-xyz transitive delivery chain: a MicrosoftSystem64 RAT three npm dependencies deep (SafeDep, Sep 1, 2026)

## Tags
- ops
- supply-chain
- npm
- transitive dependency
- typosquat
- MicrosoftSystem64
- FAMOUS CHOLLIMA
- Contagious Interview
- DPRK
- remote access trojan
- postinstall
- WebSocket C2
- persistence
- cross-platform
- SafeDep
- Hetzner

## Summary
SafeDep published a malicious-package analysis on **September 1, 2026** documenting a **cross-platform remote access trojan delivered three npm dependencies deep** under the name `ulid-xyz` (SafeDep ID **MAL-2026-6672**). The chain: `ioredis-xyz` (a byte-for-byte copy of the real `ioredis` Redis client) → `redis-type-xyz` (an empty manifest posing as Redis OM) → `ulid-xyz` (a typosquat of `ulidx` carrying the payload). The payload arrives **19 minutes after the top of the chain ships**, so the entry package looked clean on publication day. The operator planted the dependency ranges in **28 purpose-built GitHub repositories** (mostly AI/fintech/trading-themed repos with hundreds of stars) that add `ioredis-xyz` as a dependency. The implant persists as **`MicrosoftSystem64`** on Windows, macOS, and Linux — the same name, persistence design, port 8010, Hetzner hosting, and `whisdev` operator overlap as the earlier `js-logger-pack` / `terminal-logger-utils` cluster that **kmsec.uk and OX Security attribute to FAMOUS CHOLLIMA (Contagious Interview, DPRK-linked)**.

## Reported chain
1. **Layer 1 — `ioredis-xyz`:** a copy of `ioredis` (89 files, identical except `package.json`); version **5.11.2** adds one unused dependency, `redis-type-xyz@^1.10.5`. Published **2026-06-17 07:37 UTC**.
2. **Layer 2 — `redis-type-xyz`:** a manifest-only package posing as Redis OM (no `.js`/`.ts`/`.mjs`/`.cjs` files; `main` points at a nonexistent `dist/index.js`). Version **1.10.6** (published **2026-06-17 07:56 UTC**, 19 minutes after layer 1) adds `ulid-xyz@^2.12.2`. Its advisory is MAL-2026-11205. The README still references `redis-type-os`, which npm removed 18 hours earlier under MAL-2026-5882 — the operator rebuilt under a new name and reused the documentation.
3. **Layer 3 — `ulid-xyz`:** typosquats `ulidx` (sortable-UID generator, zero runtime dependencies). The malicious 2.12.x releases declare ten dependencies including a WebSocket client and a package named `postinstall`; the `postinstall` script reads as a build-file existence check, then runs `node dist/node/utils.js` → `dist/node/payload.js`, a **467 KB bundled trojan** that decodes an obfuscated configuration, beacons to a hardcoded command server over **WebSocket**, and installs persistence under the name **MicrosoftSystem64**. The package grew 64 KB → 536 KB when the payload arrived.

Because `redis-type-xyz@^1.10.5` matches any 1.x ≥ 1.10.5, the chain armed the moment 1.10.6 existed — without the operator ever republishing `ioredis-xyz`.

## The 28 planted repositories
SafeDep traced the delivery to **28 attacker-created GitHub repositories** (not compromised upstream projects) that declare `ioredis-xyz@^5.10.2`–`^5.11.2` — AI-agent, fintech, trading-bot, sports-prediction, and "MCP"-themed repositories, several with 80–150 stars and hundreds of forks. Examples include `Cesarjoquin/Marketing-Skills`, `jaipreet15/tradingview-mcp`, `pueschel88/Tradingview-MCP`, `FR0ZON3/notion-mcp`, and `whisdev/flash-loan-trading-bot`. A copied trading-bot repository added `ioredis-xyz@^5.11.2` on **2026-08-25**, seven and a half hours before npm removed `ulid-xyz`.

## The payload
- **Analysis evasion:** the launcher exits when the host reports fewer than four processors, avoiding sandboxes and CI runners.
- **Capability set:** `ping`, `get_system_info`, `list_drives`, `list_dir`, `deploy_binary`, `remove_agent`. The bundle does **not** steal credentials by itself (no wallet/browser/keychain strings) — it is a **first-stage RAT** that fingerprints the host, exposes the file system to the operator, and then executes whatever the operator sends: `deploy_binary` accepts base64, writes it to disk, installs persistence, and restarts into that code, so the operator chooses the second-stage capability set per machine after reading the reconnaissance.
- **Persistence (all three OSes, name `MicrosoftSystem64`):** Windows scheduled task (`\MicrosoftSystem64` + `MicrosoftSystem64.vbs`), macOS LaunchAgent (`~/Library/LaunchAgents/com.launchkeeper.MicrosoftSystem64.plist`), Linux systemd user unit (`~/.config/systemd/user/MicrosoftSystem64.service`); lock file `pkg-agent.lock` in the temp directory.
- **C2:** two command servers, base64 + repeating XOR hidden: `65.21.30[.]171:8010` (June 17) and `95.216.232[.]162:8010` (June 29, introduced when `ulid-xyz` 2.12.3 was published 2026-06-29), both at **Hetzner Online GmbH, Germany**. MAL-2026-6672 records only the second address.

## Cluster attribution: MicrosoftSystem64 / FAMOUS CHOLLIMA
SafeDep ties this chain to the cluster previously analyzed in `js-logger-pack` / `terminal-logger-utils` (May 2026, an 81 MB Node.js single executable that steals browser credentials, 80+ crypto-wallet extensions, Telegram sessions, and SSH keys, exfiltrating to Hugging Face; kmsec.uk and OX Security attribute it to **FAMOUS CHOLLIMA**, tracked as **Contagious Interview**, DPRK-linked):
1. **Same implant name** `MicrosoftSystem64` and the same cross-platform persistence design.
2. **Same C2 port, 8010** (earlier binary used `195.201.194[.]107:8010`).
3. **Same hosting provider, Hetzner**, for all three observed addresses.
4. **Direct operator overlap:** the `whisdev` persona that JFrog traced through `copilot-ai.whisdev[.]org` on the earlier command server **owns two of the 28 repositories** above.

The likely second stage delivered through `deploy_binary` is the credential stealer documented in the earlier analysis. SafeDep's stated limit: no second stage appears in any published archive of the three packages, so what reached any specific machine cannot be said from public material.

## Timeline (UTC)
| Date/time | Event |
| --- | --- |
| 2026-06-16 11:53 | npm removes `redis-type-os` (MAL-2026-5882) |
| 2026-06-16 17:08 | `redis-type-xyz@1.10.5` published, no payload dependency |
| 2026-06-17 06:07 | `ulid-xyz@2.12.2` published, no payload dependency |
| 2026-06-17 07:37 | `ioredis-xyz@5.11.2` adds `redis-type-xyz@^1.10.5` |
| 2026-06-17 07:56 | `redis-type-xyz@1.10.6` adds `ulid-xyz@^2.12.2`; **the chain is armed** |
| 2026-06-29 15:10 | `ulid-xyz@2.12.3` published with the new command server |
| 2026-08-25 08:41 | A copied trading-bot repository adds `ioredis-xyz@^5.11.2` |
| 2026-08-25 16:36 | npm removes `ulid-xyz` (MAL-2026-6672) |

## Indicators of compromise
- Entry package: `ioredis-xyz@5.11.2`
- Relay packages: `redis-type-xyz@1.10.5`–`1.10.6`
- Payload package: `ulid-xyz@2.12.2`–`2.12.3`
- Command servers: `hxxp[:]//65[.]21[.]30[.]171:8010`, `ws://65[.]21[.]30[.]171:8010`, `hxxp[:]//95[.]216[.]232[.]162:8010`, `ws://95[.]216[.]232[.]162:8010` (Hetzner, Germany)
- XOR key: `5A 3C 7E 12 9F 4B 6D 8A`
- Persistence name: `MicrosoftSystem64` (Windows task `\MicrosoftSystem64` + `MicrosoftSystem64.vbs`; macOS `~/Library/LaunchAgents/com.launchkeeper.MicrosoftSystem64.plist`; Linux `~/.config/systemd/user/MicrosoftSystem64.service`)
- Lock file: `pkg-agent.lock` in the temp directory
- Payload SHA-256 (2.12.2): `a3c28435295fed4babdeefedcefdd0ed037ff24ed3ff363a49d080c2768d07f2`
- Payload SHA-256 (2.12.3): `3a9089e9db3650dd6d1584fae709022002dc34854b961abfb014a90f0a7c6a50`
- Launcher SHA-256: `aa01a83c7a420c22a719b02ec327451ddd751ab5b189fd0127824ea43533b96a`
- Related advisories: MAL-2026-6672, MAL-2026-11205, MAL-2026-5882

## Defender heuristics
- **Hunt the persistence name, not the package:** any host with a user-level persistence entry named `MicrosoftSystem64` (scheduled task, LaunchAgent `com.launchkeeper.MicrosoftSystem64`, systemd user unit) should be treated as compromised, regardless of how it arrived — the name overlaps the `js-logger-pack` cluster's implants.
- **Transitive-dependency delivery defeats top-of-tree review:** the entry package looked clean on publication day and was never republished; auditors who snapshot `package-lock.json` at install time, or lock and pin all three layers, would have stopped the chain. Treat "a dependency added to a previously-clean manifest after the fact" (especially via a caret range) as a supply-chain review trigger.
- **Star/fork count is not provenance:** the 28 seed repositories were purpose-built with realistic names, stars, and forks; the durable tell is the dependency on a same-day, never-imported, zero-runtime-dependency typosquat.
- **Low-core-count exit is an evasion tell:** install-time payloads that bail out on hosts reporting <4 processors are tuned to evade sandboxes/CI; flag install scripts with processor-count gates.
- **Hetzner:8010 WebSocket C2** is now a three-observation indicator for the cluster; correlate new `MicrosoftSystem64` sightings with 8010/WSS connections to Hetzner ranges.

## Attribution notes
SafeDep does not itself name the actor; the link to FAMOUS CHOLLIMA / Contagious Interview (DPRK-linked) is carried from kmsec.uk and OX Security's attribution of the earlier `MicrosoftSystem64` binary analysis, reinforced here by the direct `whisdev` operator overlap. Track this as a **durable MicrosoftSystem64 cluster expansion** — second delivery chain, second operator persona overlap — rather than a new, unrelated campaign.

## Related pages
- [js-logger-pack Hugging Face exfiltration campaign (MicrosoftSystem64 cluster)](js-logger-pack-hugging-face-exfiltration.md)
- [StegaBin Pastebin steganography npm campaign (Contagious Interview)](stegabin-pastebin-steganography-npm-campaign.md)
- [FAMOUS CHOLLIMA Packagist dev-branch loader](famous-chollima-packagist-dev-branch-loader.md)
- [Rust supply-chain attack: arrayref 0.3.10 and the proc-macro1 typosquat](arrayref-proc-macro1-rust-crate-supply-chain-attack.md)

## Sources
- SafeDep — "A malicious npm package hidden three dependencies deep: the ulid-xyz delivery chain" (Kunal Singh, 2026-09-01): [https://safedep.io/ulid-xyz-transitive-dependency-delivery-chain](https://safedep.io/ulid-xyz-transitive-dependency-delivery-chain)
- SafeDep — MicrosoftSystem64 binary payload analysis (2026-05-28, earlier cluster phase): [https://safedep.io/microsoftsystem64-binary-payload-analysis/](https://safedep.io/microsoftsystem64-binary-payload-analysis/)
- JFrog Security Research — js-logger-pack / Hugging Face exfil (whisdev persona): [https://research.jfrog.com/post/hugging-face-exfil/](https://research.jfrog.com/post/hugging-face-exfil/)
