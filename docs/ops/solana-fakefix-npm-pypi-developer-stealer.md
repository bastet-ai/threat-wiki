# Solana FakeFix npm / PyPI developer stealer

## Summary
JFrog Security Research's June 11, 2026 report describes **Solana FakeFix**, a malicious npm and PyPI package campaign aimed at Solana developers. The campaign used package names that looked like patched or community Solana SDK builds, GitHub issue spam that framed the packages as fixes for Solana build problems, npm install hooks, PyPI import-time payloads, Telegram command-and-control, wallet-draining logic, and Windows Deno loader persistence.

The durable defender lesson is that crypto-developer package lures often combine three trust-boundary failures: dependency names that imply a compatibility fix, social proof delivered through GitHub issues, and execution surfaces that run before a developer ever meaningfully reviews the code.

## Tags
- ops
- supply chain
- npm
- PyPI
- Solana
- cryptocurrency
- developer targeting
- credential theft
- wallet theft
- install-time execution
- import-time execution
- GitHub issue spam
- Telegram C2
- Deno
- Windows persistence
- MEV bot lure
- JFrog Security Research

## Why this matters
- JFrog's affected package table lists 25 malicious packages across npm and PyPI, including Solana-themed SDK lookalikes, CMS-themed Windows loaders, and a fake MEV bot lure.
- The campaign targets high-value developer and CI secrets: Solana keypairs, SSH keys, AWS credentials, `.env` files, GitHub / npm / CI tokens, wallet files, and sensitive environment variables.
- The npm branch can execute at install time through lifecycle scripts; the PyPI branch can execute later on import through malicious `__init__.py` code.
- Later npm variants were not just tiny droppers: JFrog says they shipped functional-looking Solana JavaScript bundles with malicious code appended after legitimate exports and source-map markers.

## Compromise chain
### GitHub issue lure
- JFrog reports that the Solana-labs packages appear to have been promoted through GitHub issue spam by the user `PassWord1337`.
- The issue text presented `@solana-labs/web3.js` as a community-maintained drop-in replacement for `@solana/web3.js` v2 and suggested an uninstall / install command.
- The issues were later edited down to a single `x`, which JFrog assesses as likely cleanup or obscuring of the original lure.

### npm install-time execution
- Early npm variants used `postinstall` scripts such as `node install.js`.
- The payload configured Telegram C2 and searched for local developer secrets immediately after installation.
- Solana-labs packages used Telegram bot / chat identifiers reported by JFrog and targeted paths such as:
  - `~/.config/solana/id.json`
  - `~/.solana/id.json`
  - `~/.ssh/id_rsa`
  - `~/.ssh/id_ed25519`
  - `~/.aws/credentials`
  - `.env`
  - `wallet.json`

### PyPI import-time execution
- The PyPI packages placed payload code in `__init__.py`.
- This means compromise may occur when tests, notebooks, scripts, or applications import the package, even if installation happened earlier.
- Treat this separately from npm lifecycle-hook exposure: lockfile review alone may miss dormant import-time execution.

### Trojanized Solana libraries
- Later npm packages shipped Solana-looking JavaScript bundles with malicious code appended after legitimate exports and source-map markers.
- The appended payloads scanned key files and environment variables containing terms such as `KEY`, `SECRET`, `MNEMONIC`, `PRIVATE`, `TOKEN`, `PASSWORD`, `AWS`, `NPM`, `GITHUB`, `CI`, `DEPLOY`, `SOLANA`, `ALCHEMY`, `INFURA`, and `ETHERSCAN`.
- JFrog reports command handling for `/keys`, `/ssh`, `/env`, `/wallet`, `/sh`, `/cmd`, and `/die`, making these variants general backdoors rather than one-shot stealers.
- One variant attempted to drain Solana funds to `D4hGgKKaBFZV1NUTWvYRwbpu8HHr3qmDfHyKCTLqbaE7` and changed Solana RPC settings to `hxxp[:]//104[.]239[.]66[.]223:8899`.

### Fake MEV bot lure
- `solana-mev-bot` used a direct cryptocurrency-scam pattern: it asked the user to paste a Solana private key to start earning from an alleged MEV / sandwich bot.
- JFrog says the package also searched for `.env`, Solana keypair files, SSH keys, AWS credentials, and key-like environment variables.

### CMS-themed Windows loaders
- The campaign also included CMS-themed npm packages uploaded by `thermonuclear`, including `cms-storehub`, `cms-helpgit`, `cms-github`, `to-cms`, and `shopifyto-cms`.
- These packages used npm install-time execution to write and launch hidden PowerShell scripts, install or locate Deno, and run remote JavaScript from `77.90.185.225` with broad permissions.
- JFrog observed repeated fetch/eval behavior, a health endpoint, a registration endpoint, dynamic payload naming, and Windows persistence such as scheduled tasks, Run keys, startup VBS files, PowerShell profile hooks, and a local mutex listener on `127.0.0.1:10092`.

## Affected package names from JFrog
### npm
- `@solana-labs/ancor`
- `@solana-labs/etherjs`
- `@solana-labs/spl-toke`
- `@solana-labs/web3-js`
- `@solana-labs/web3.js`
- `@solana-labs/web3js`
- `cms-github`
- `cms-helpgit`
- `cms-storehub`
- `shopifyto-cms`
- `solana-js-client`
- `solana-mev-bot`
- `solana-rpc-client`
- `solana-web3-community`
- `solana-web3-fixed`
- `solana-web3-fork`
- `solana-web3-lts`
- `solana-web3-patched`
- `solana-web3-stable`
- `solana-web3-v1`
- `to-cms`

### PyPI
- `solana-cli-py`
- `solana-web3`
- `solana-web3-py`
- `spl-token-py`

## Defender heuristics
- Search dependency manifests, lockfiles, local package caches, CI images, and build-worker histories for the affected package names.
- Rebuild developer workstations, CI runners, containers, and build agents from trusted images if any affected package executed; do not rely only on uninstalling the package.
- Rotate Solana keypairs and wallets that may have been present on exposed systems, then move funds from a clean host.
- Rotate SSH keys, AWS keys, GitHub tokens, npm tokens, CI tokens, registry tokens, AI/API keys, and secrets found in `.env` files or environment variables.
- Hunt for npm lifecycle execution followed by Telegram traffic, Deno installation, `deno run -A` remote scripts, hidden PowerShell, and suspicious GitHub issue recommendations to install patched Solana forks.
- On Windows, inspect scheduled tasks, Registry Run keys, startup VBS files, PowerShell profile hooks, and `conhost.exe --headless <deno> -A <hash>.js`-style launches.
- On Unix-like hosts, inspect `crontab @reboot`, shell profile hooks, and macOS LaunchAgents for package-created persistence.
- Treat MEV-bot packages that ask for private keys as credential-harvesting incidents, not failed application installs.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [StegaBin Pastebin-steganography npm campaign](stegabin-pastebin-steganography-npm-campaign.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- [JFrog Security Research](https://research.jfrog.com/post/solana-fakefix/)
