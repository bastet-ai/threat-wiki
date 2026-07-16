# TrapDoor crypto-stealer cross-ecosystem campaign

## Summary
Socket reported TrapDoor, an active supply-chain campaign spanning npm, PyPI, and Crates.io packages that impersonate developer, crypto, AI, DeFi, Solidity, Sui, and Move tooling.

Socket observed more than 34 malicious package names and 384+ related versions or artifacts across the three registries. The earliest package it identified was `eth-security-auditor@0.1.0` on PyPI, uploaded on 2026-05-22 at 20:20:18 UTC, followed by waves of npm, PyPI, and Crates.io publications through the weekend.

## Tags
- ops
- operations
- supply-chain
- npm
- PyPI
- Crates.io
- Rust
- crypto
- DeFi
- AI tooling
- credential-theft
- wallet-theft
- lateral-movement
- persistence
- prompt-injection

## Why this matters
- TrapDoor crosses three package ecosystems and targets developer machines where crypto wallets, GitHub tokens, cloud credentials, SSH keys, and AI-tool configuration are likely to coexist.
- The campaign is not only a one-shot stealer: the npm payload validates AWS and GitHub credentials, attempts SSH-based lateral movement, and plants several persistence mechanisms.
- It uses AI-assistant instruction files such as `.cursorrules` and `CLAUDE.md` as an attempted persistence and social-engineering layer, showing attackers are adapting supply-chain malware for agentic development workflows.
- Crates.io `build.rs`, PyPI import-time execution, and npm `postinstall` hooks create multiple automatic execution paths during normal install, import, and build workflows.

## Reported package sets

### npm packages
Socket listed the following npm packages in the campaign:

- `async-pipeline-builder`
- `build-scripts-utils`
- `chain-key-validator`
- `crypto-credential-scanner`
- `defi-env-auditor`
- `defi-threat-scanner`
- `deployment-key-auditor`
- `dev-env-bootstrapper`
- `eth-wallet-sentinel`
- `llm-context-compressor`
- `mnemonic-safety-check`
- `model-switch-router`
- `node-setup-helpers`
- `project-init-tools`
- `prompt-engineering-toolkit`
- `solidity-deploy-guard`
- `token-usage-tracker`
- `wallet-backup-verifier`
- `wallet-security-checker`
- `web3-secrets-detector`
- `workspace-config-loader`

### PyPI packages
- `cryptowallet-safety`
- `data-pipeline-check`
- `defi-risk-scanner`
- `env-loader-cli`
- `eth-security-auditor`
- `git-config-sync`
- `solidity-build-guard`

### Crates.io packages
- `move-analyzer-build`
- `move-compiler-tools`
- `move-project-builder`
- `sui-framework-helpers`
- `sui-move-build-helper`
- `sui-sdk-build-utils`

## Execution and payload behavior

### npm path
- Malicious npm packages were published by npm user `asdxzxc`.
- Packages used `postinstall` execution.
- A shared `trap-core.js` payload scanned for credentials and developer secrets.
- The payload validated stolen AWS and GitHub credentials via API calls.
- Socket reported persistence and propagation attempts through `.cursorrules`, `CLAUDE.md`, Git hooks, shell hooks, systemd services, cron jobs, and SSH-based movement.
- `dev-env-bootstrapper` is notable as both malware and a delivery vector for malicious developer-environment configuration.

### PyPI path
- PyPI packages auto-executed on import.
- They downloaded JavaScript from the attacker-controlled GitHub Pages domain and executed it with `node -e`.
- Socket associated PyPI publishing activity with accounts including `asdmini67` and `dae5411`.
- Remote JavaScript hosting lets the operator alter behavior after package publication.

### Crates.io path
- Rust packages targeted Sui and Move developers.
- Malicious `build.rs` scripts executed during compilation.
- The build scripts searched for wallet keystores, encrypted data with the XOR key `cargo-build-helper-2026`, and exfiltrated data to GitHub Gists.

## Data targeted
Socket reported collection logic for:

- SSH keys
- Sui, Solana, and Aptos wallet data
- AWS credentials
- GitHub tokens and credentials
- browser profile data and login databases
- crypto wallet extension data
- environment variables
- API keys
- local development configuration files

## AI-tooling abuse
TrapDoor attempts to plant hidden AI-facing instructions in `.cursorrules` and `CLAUDE.md`, including zero-width Unicode characters. The apparent goal is to make future AI coding-assistant sessions treat malicious credential discovery and exfiltration as a benign "security scan" or development-standard workflow.

The attacker-controlled GitHub Pages repository also contained an `AUDIT-MATRIX.md` document describing a "Universal AI Agent Extraction Framework." Socket cautioned that this document should not be treated as a full list of confirmed runtime behavior, but many themes match observed payload behavior: filesystem scanning, environment harvesting, credential discovery, AI-facing disguise language, `.cursorrules` persistence, and remote configuration.

## Infrastructure and campaign markers
- GitHub account: `ddjidd564`.
- GitHub Pages host: `ddjidd564[.]github[.]io/defi-security-best-practices/`.
- Campaign marker: `P-2024-001`.
- Shared npm payload: `trap-core.js`.
- Crates.io XOR key: `cargo-build-helper-2026`.

Socket also observed the same GitHub account opening pull requests against AI and developer-tooling projects such as `browser-use/browser-use`, `langchain-ai/langchain`, `langflow-ai/langflow`, `run-llama/llama_index`, `FoundationAgents/MetaGPT`, and `OpenHands/OpenHands`. The PRs attempted to add `.cursorrules` or `CLAUDE.md` files under benign documentation or build-verification language.

## Defender heuristics
- Treat new developer-helper packages in crypto, DeFi, AI, Solidity, Sui, and Move contexts as high risk until provenance is confirmed.
- Block or review lifecycle execution paths: npm `postinstall`, PyPI import-time side effects, and Rust `build.rs` scripts.
- Hunt for unexpected `.cursorrules`, `CLAUDE.md`, Git hooks, shell hooks, systemd units, cron jobs, and SSH authorized-key changes after package installation.
- Alert on packages that fetch and execute remote JavaScript through `node -e`, especially from GitHub Pages.
- Search developer workstations and CI runners for the listed package names, `trap-core.js`, `P-2024-001`, `ddjidd564`, and `ddjidd564.github.io` references.
- If affected packages were installed or built, isolate before rotating secrets. Assume wallet keys, SSH keys, GitHub tokens, cloud credentials, browser data, and environment variables may have been exposed.

## Attribution notes
Public reporting attributes the campaign to an attacker-controlled package and GitHub infrastructure cluster that Socket tracks as TrapDoor. It is not currently tied here to a named threat group such as TeamPCP or Mini Shai-Hulud without stronger sourcing.

## Related pages
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [js-logger-pack Hugging Face exfiltration campaign](js-logger-pack-hugging-face-exfiltration.md)
- [BufferZoneCorp RubyGems / Go module CI poisoning](bufferzonecorp-ruby-go-ci-poisoning.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)

## Sources
- Socket: [https://socket.dev/blog/trapdoor-crypto-stealer-npm-pypi-crates](https://socket.dev/blog/trapdoor-crypto-stealer-npm-pypi-crates)
