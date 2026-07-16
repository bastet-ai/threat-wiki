# faster-axios / turbo-axios Epsilon Stealer npm campaign

## Summary
SafeDep reports a two-package npm typosquat campaign targeting developers looking for the Axios HTTP client. The packages `turbo-axios` and `faster-axios` copied the legitimate Axios source tree but added a `postinstall` hook that fetched and evaluated remote JavaScript, then delivered a Windows Epsilon Stealer payload.

This is separate from the earlier real-Axios compromise coverage: here the distribution path is typosquatting plus rotating npm accounts after takedown, not compromise of the legitimate Axios maintainer account.

## Tags
- ops
- operations
- supply-chain
- npm
- typosquatting
- postinstall
- infostealer
- RAT
- Epsilon Stealer
- credential-theft
- crypto-wallets
- Windows

## Why this matters
- The packages were trojanized copies of a high-trust dependency, with metadata pointing to the real Axios project and inflated `1.17.x` version numbers to look newer than legitimate releases.
- Install-time execution reached beyond simple credential theft: SafeDep recovered a chain ending in an Electron-based Epsilon Stealer MaaS payload with browser theft, wallet theft, persistence, shellcode injection, and a WebSocket command channel.
- The operator reused infrastructure across `turbo-axios` and `faster-axios`, then rotated packages and npm accounts after takedown, making this a campaign pattern rather than a one-off bad package.

## Reported chain

### Package setup
- `turbo-axios` appeared on npm on May 23, 2026, and was later placed under npm security hold as `MAL-2026-4695`.
- `faster-axios` appeared on June 1, 2026, under a new npm account after the earlier package was removed.
- SafeDep says both packages copied Axios wholesale and added `lib/core/eval.js`, wired through `package.json` as `postinstall: node ./lib/core/eval.js`.
- The `faster-axios` package used a throwaway maintainer identity, forged real Axios metadata such as the original author, repository, and homepage, and carried forged file mtimes from `1985-10-26 08:15:00`.

### Four-stage payload
1. **npm `postinstall` loader** — `lib/core/eval.js` fetched remote JavaScript and ran it through `eval()`. SafeDep reported `faster-axios@1.17.4` fetched `datab1` from `apparently-movers-mysql-heights.trycloudflare[.]com`, while earlier infrastructure included `cold5.gofile[.]io`.
2. **Windows dropper** — the fetched JavaScript downloaded `epsilon` to `%TEMP%\hello.exe` and executed it. SafeDep notes stages 1 and 2 can run on any OS because the C2 controls the JavaScript returned, even though the payload live during analysis was Windows-specific.
3. **NSIS installer** — `hello.exe` was an 86 MB Nullsoft installer with SHA256 `bc46e88b1fdf8c27e3404146306b4651f69728f7d8d939a219dfbcb5a23ef69a`, unpacking to an Electron app.
4. **Epsilon Stealer** — the inner Electron app identified itself as `winhost`, used decoy author `OracleCorporation`, and contained operator license key `SK-754644F96BBA9652C8A2A08042ABAF58827D`.

## Epsilon Stealer behavior
SafeDep's recovered sample reported:

- Browser credential theft from Chrome, Brave, Edge, Vivaldi, Opera, Opera GX, Yandex, and Firefox.
- Chromium DPAPI decryption through `Crypt32.dll` / `CryptUnprotectData`, plus Firefox `logins.json` decryption through an NSS loader.
- Wallet targeting across 30+ browser-extension and desktop wallets, including MetaMask, Phantom, Exodus, Trust Wallet, Ledger Live, Electrum, Bitcoin Core, and Monero GUI.
- Seed-phrase extraction for MetaMask and Exodus vaults.
- Discord token validation and exfiltration, Telegram `tdata` theft, and GitHub 2FA backup-code collection.
- File harvesting from Desktop, Downloads, and Documents using credential, wallet, backup, banking, and French-language keyword patterns.
- Zipped multipart exfiltration to Cloudflare quick-tunnel infrastructure.
- Persistence by copying itself to `%LOCALAPPDATA%\Microsoft\Windows\0\svchost.exe` and setting `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svchost`.
- Shellcode download, XOR decode with key `0xAA`, and injection into suspended `dllhost.exe` through `VirtualAllocEx`, `WriteProcessMemory`, and `CreateRemoteThread`.
- Persistent WebSocket RAT connection with arbitrary `cmd.exe` or `powershell.exe` command execution and output streaming.

## Reported indicators

### Packages
- `faster-axios@1.17.3`
- `faster-axios@1.17.4`
- `turbo-axios@1.17.2`
- `turbo-axios@1.17.3`
- npm malware notice: `MAL-2026-4695` for `turbo-axios`

### Network
- `apparently-movers-mysql-heights.trycloudflare[.]com` — payload delivery and shellcode
- `recorded-distinct-face-girlfriend.trycloudflare[.]com/customer` — exfiltration API
- `consequences-faces-weblogs-clinical.trycloudflare[.]com` — secondary download; shared with `turbo-axios`
- `prep-integer-lit-preferences.trycloudflare[.]com` — WebSocket RAT gateway
- `philosophy-moms-incoming-milton.trycloudflare[.]com` — `turbo-axios` stage-2 infrastructure
- `cold5.gofile[.]io` — earlier `faster-axios` delivery path reported by SafeDep

### Host artifacts
- `%TEMP%\hello.exe`
- `%LOCALAPPDATA%\Microsoft\Windows\0\svchost.exe`
- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svchost`
- Operator key: `SK-754644F96BBA9652C8A2A08042ABAF58827D`
- Installer SHA256: `bc46e88b1fdf8c27e3404146306b4651f69728f7d8d939a219dfbcb5a23ef69a`

## Defender heuristics
- Block or review npm packages that add new lifecycle hooks to otherwise familiar dependency source trees.
- Flag dependency names that append performance or freshness claims to popular package names, such as `faster-*`, `turbo-*`, or inflated version lines above the legitimate project.
- Diff suspected typosquat tarballs against the real upstream package, including hidden or newly added files under plausible source paths.
- Treat install of affected versions as a host compromise, not just package exposure: SafeDep recommends reimaging because the payload adds persistence, injects shellcode, and opens a RAT channel.
- Rotate all credentials reachable from the host after containment: browser-saved passwords, API keys, cloud tokens, SSH keys, environment secrets, Discord, Telegram, GitHub sessions, and any wallet material.
- Move cryptocurrency funds to wallets generated on a clean device if affected hosts contained wallet extensions or desktop wallets.
- Monitor for Cloudflare quick-tunnel download/exfiltration paths launched by `node`, `npm`, Electron `winhost.exe`, `svchost.exe` under user-local paths, or unexpected `dllhost.exe` injection ancestry.

## Related pages
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- SafeDep: <https://safedep.io/malicious-faster-axios-npm-epsilon-stealer>
