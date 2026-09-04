# js-logger-pack Hugging Face exfiltration campaign

## Summary
JFrog reported that newer malicious `js-logger-pack` npm releases, including `1.1.27`, shifted from using Hugging Face only as a malware CDN to also using private Hugging Face datasets as a stolen-data backend.

The package presented a benign logger in `dist/index.js`, but its `package.json` `postinstall` script launched `print.cjs`, detached a downloader, fetched a platform-specific `MicrosoftSystem64*` Node.js Single Executable Application from `huggingface.co/Lordplay/system-releases`, and installed a persistent cross-platform implant.

## Tags
- ops
- operations
- supply-chain
- npm
- Hugging Face
- credential-theft
- keylogger
- exfiltration
- Linux
- macOS
- Windows

## Why this matters
- Public model/dataset hosting can become both a malware distribution surface and an exfiltration backend, not just a place to stage files.
- The package used a classic bait-and-switch shape: benign exported library code plus malicious install-time behavior hidden in lifecycle scripts.
- The final payload was one cross-platform JavaScript implant wrapped in Node SEA binaries for Windows, macOS, and Linux, which makes string-level platform assumptions misleading.
- Any environment that installed an affected version should be treated as an endpoint compromise, not only a suspicious npm install.

## Reported chain
1. `js-logger-pack` shipped plausible logger code in `dist/index.js`.
2. `package.json` registered `postinstall: node print.cjs`.
3. `print.cjs` detached a child process so `npm install` could finish while the downloader continued.
4. The downloader selected one of four `MicrosoftSystem64` binaries from `https://huggingface.co/Lordplay/system-releases/resolve/main/` based on platform and architecture.
5. JFrog extracted the same embedded JavaScript payload from all four Node SEA containers.
6. The implant registered persistence, beaconed to `195.201.194[.]107:8010`, monitored clipboard and keystrokes, and accepted operator tasks.
7. For `upload_folder_hf` tasks, the implant archived victim files and uploaded them into attacker-controlled private Hugging Face datasets.

## Payload capabilities reported by JFrog
- Persistence through Windows scheduled task / Run key, macOS LaunchAgent, Linux systemd user unit, or XDG autostart.
- System information beacons over WebSocket / HTTP to `195.201.194[.]107:8010`.
- Clipboard monitoring and platform-specific keylogging.
- File browsing, file reads/writes, directory creation/deletion, and folder-size collection.
- Recursive file scanning for credentials, wallets, browser data, shell history, and environment variables.
- Telegram Desktop `tdata` exfiltration on Windows and macOS.
- Browser/session clearing and arbitrary binary deployment.
- Self-update checks against the same Hugging Face repository without signature or checksum validation.
- Private Hugging Face dataset creation/reuse for archived data uploads.

## 2026-05-28 SafeDep live-infrastructure update
SafeDep published a deeper `MicrosoftSystem64` binary analysis on May 28, 2026, reporting that the campaign remained active more than six weeks after the first `js-logger-pack` disclosures. Their live probe found the embedded Hugging Face token still valid at the time of testing, the WebSocket C2 accepting connections, and private datasets containing live victim screenshots and credential archives.

New details from the SafeDep analysis include:

- The analyzed payload was `MicrosoftSystem64` version `1.0.8`, an 81 MB stripped Node.js Single Executable Application using Node.js `v20.18.2`.
- The implant accepted 24 remote commands, uploaded periodic screenshots to Hugging Face every 60 seconds, and self-updated from `jpeek998/system-releases` after the earlier `Lordplay/system-releases` hosting was disabled.
- SafeDep observed three private datasets under the `jpeek998` account containing hundreds of screenshots and a roughly 500 MB credential archive from two active victims.
- The credential archive included SSH keys, browser `Login Data`, cookies, local-state files, Claude Desktop app data, NVIDIA app embedded-browser credentials, Electron app stores, WeChat / xwechat data, Telegram data, Remote Desktop files, Todoist data, and anti-detect browser profiles.
- SafeDep tied the campaign to a broader `toskypi` / `jpeek*` identity cluster also associated with npm accounts `jpeek868`, `jpeek886`, `jpeek895`, `pvnd3540749`, and `yggedd817513`, plus public identifiers including `ptc-bink` / `whisdev` cited from earlier JFrog research.

Additional indicators from this update:

- Linux ELF SHA-256: `b2954c945b51dbd6fa88ac72338b7fbf76dec7d9909ceada9d36b21330842c97`
- Active Hugging Face exfil account: `jpeek998`
- Binary host: `hxxps://huggingface[.]co/jpeek998/system-releases/resolve/main`
- Prior binary host: `Lordplay/system-releases`
- Linux install directory: `~/.local/share/MicrosoftSystem64`
- macOS install directory: `~/Library/Application Support/MicrosoftSystem64`
- Windows install directory: `%LOCALAPPDATA%\\MicrosoftSystem64`
- Persistence labels: `MicrosoftSystem64`, `com.launchkeeper.MicrosoftSystem64`, and Windows scheduled task `MicrosoftSystem64`

## Indicators and hunt pivots
- npm package: `js-logger-pack`.
- Reported malicious version: `1.1.27` and related newer releases analyzed by JFrog.
- Loader file: `print.cjs`.
- Lifecycle script: `postinstall` invoking `node print.cjs`.
- Hugging Face repository: `Lordplay/system-releases`.
- Downloaded filenames:
  - `MicrosoftSystem64-win.exe`
  - `MicrosoftSystem64-darwin-x64`
  - `MicrosoftSystem64-darwin-arm64`
  - `MicrosoftSystem64-linux`
- Process title: `MicrosoftSystem64`.
- C2: `ws://195.201.194[.]107:8010` and `http://195.201.194[.]107:8010`.
- Extracted SEA blob SHA-256: `46b9522ba2dc757ac00a513dbd98b28babb018eae92347f2cbc3c7a5020872b5`.
- Extracted embedded JavaScript SHA-256: `1c83019b52be6da9583d28fe934441a74eacef0cd7dbb9d71017122de6fe7cfc`.

## Defender heuristics
- Treat npm lifecycle scripts as executable code review targets even when the library's exported API appears benign.
- Alert on package installs that fetch executables from model/dataset hosting platforms or GitHub Releases without integrity checks.
- Monitor for user-level persistence named like Microsoft system components on non-Windows hosts.
- Hunt Hugging Face API usage from developer workstations and CI runners that do not normally interact with model/dataset hosting.
- If affected versions were installed, isolate the host before rotating secrets; the implant includes operator-controlled file access and credential collection, so token rotation alone is not enough.

## Attribution notes
JFrog mapped the distribution infrastructure to linked public personas, but the reporting used here does not attribute the campaign to a named threat group. Track it as a malicious npm package operation unless stronger public sourcing ties it to a broader cluster.

## September 1, 2026: second delivery chain in the same cluster
SafeDep's September 1, 2026 analysis of the **`ulid-xyz`** chain (MAL-2026-6672: `ioredis-xyz` → `redis-type-xyz` → `ulid-xyz`, transitive-delivery RAT) found the **same `MicrosoftSystem64` implant name, the same cross-platform persistence design, the same C2 port 8010, the same Hetzner hosting, and a direct `whisdev` operator overlap** with this cluster — the earlier SafeDep analysis of this campaign's 81 MB Node SEA binary (kmsec.uk / OX Security attribution: FAMOUS CHOLLIMA / Contagious Interview, DPRK-linked) is now corroborated across two independent delivery chains. See the [ulid-xyz transitive delivery chain page](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md).

## Related pages
- [ulid-xyz transitive delivery chain (MicrosoftSystem64 cluster, Sep 1, 2026)](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [BufferZoneCorp RubyGems / Go module CI poisoning](bufferzonecorp-ruby-go-ci-poisoning.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)

## Sources
- JFrog: [https://research.jfrog.com/post/hugging-face-exfil/](https://research.jfrog.com/post/hugging-face-exfil/)
- SafeDep earlier phase: [https://safedep.io/malicious-js-logger-pack-npm-stealer/](https://safedep.io/malicious-js-logger-pack-npm-stealer/)
- SafeDep `MicrosoftSystem64` update: [https://safedep.io/microsoftsystem64-binary-payload-analysis/](https://safedep.io/microsoftsystem64-binary-payload-analysis/)
