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

## Related pages
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [BufferZoneCorp RubyGems / Go module CI poisoning](bufferzonecorp-ruby-go-ci-poisoning.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)

## Sources
- JFrog: https://research.jfrog.com/post/hugging-face-exfil/
- SafeDep earlier phase: https://safedep.io/malicious-js-logger-pack-npm-stealer/
