# PolinRider cross-ecosystem supply-chain campaign

## Summary
Socket Threat Research reported on July 1, 2026 that **PolinRider**, a North Korea-linked developer-targeting supply-chain campaign associated with the broader Contagious Interview / Famous Chollima cluster, had expanded across npm, Packagist, Go modules, and a Chrome extension. Socket identified **162 malicious release artifacts across 108 packages and extensions**, including compromise traces in **80 Go modules**, **10 Packagist packages**, and **one Chrome extension**.

The durable defender lesson is that PolinRider is not only a package-name problem. The campaign repeatedly abuses legitimate GitHub repositories and maintainer identities, hides JavaScript loaders inside source trees, rewrites Git history to make malicious commits look older, and uses developer tooling such as VS Code folder-open tasks or executable build configuration as the trigger.

## Tags
- ops
- operations
- supply-chain
- GitHub
- npm
- Packagist
- Composer
- Go modules
- Chrome extension
- VS Code
- developer machines
- credential theft
- source-repository poisoning
- blockchain C2
- DPRK
- North Korea
- Contagious Interview
- Famous Chollima
- PolinRider

## Why this matters
- Socket describes PolinRider as active and likely to continue producing newly confirmed packages, versions, repositories, and extensions.
- GitHub repository landing pages and normal commit views can be misleading because the actor has used force-push / history-rewrite behavior and anti-dated commits.
- The loader is cross-ecosystem: the same operational model can reach developers through npm packages, Packagist/Composer packages, Go module source archives, browser extensions, and repository-local IDE tasks.
- The campaign targets developer environments where package-registry credentials, GitHub tokens, cloud keys, Kubernetes material, CI/CD secrets, SSH keys, browser data, and wallets may be reachable.

## Reported campaign shape
1. Threat actors compromise or obtain access to legitimate maintainer GitHub accounts or organizations.
2. Multiple repositories under the same account are modified in a narrow time window, indicating account-level compromise rather than ordinary per-project maintenance.
3. Malicious code is inserted as an obfuscated JavaScript loader, often hidden by long horizontal whitespace in config files or embedded in fake `.woff2` font files.
4. In newer variants, `.vscode/tasks.json` defines a folder-open task that executes the fake `.woff2` file with Node.js, converting an apparent static asset into an execution path.
5. Where the actor also has registry access, modified repositories can propagate into published package artifacts; Socket specifically flagged a malicious `Xpos587/git2md` Go module release.
6. Where registry access is absent or blocked, the repository can still remain a trap for developers, CI jobs, preview builders, or AI/IDE agents that open or build the source tree.

## July 2026 Socket expansion
Socket's July 1 report adds several operationally useful pivots:

- **Scale:** 162 malicious release artifacts across 108 unique packages/extensions.
- **Ecosystems:** npm, Packagist, Go modules, and Chrome extensions, with compromise traces in 80 Go modules and 10 Packagist packages.
- **GitHub account / repository pivots:** `Xpos587`, `Xpos587/git2md`, `Xpos587/markfetch`, and `Artiffusion-Inc/mirofish`.
- **Packagist / organization pivots:** `sevenspan`, `7span`, and `7span/react-list`.
- **Observed hiding methods:** long-line whitespace padding in executable configuration files such as `vite.config.js`, plus fake `.woff2` font files executed through `.vscode/tasks.json`.
- **History manipulation:** force pushes and anti-dated commits that can make malicious changes appear to be old routine maintenance.
- **Payload family:** obfuscated JavaScript loaders that can retrieve encrypted second stages from public blockchain/RPC infrastructure.
- **Reported follow-on payloads:** DEV#POPPER and OmniStealer.

## Payload behavior
After deobfuscation, Socket reported that PolinRider loaders reach out to public blockchain and RPC infrastructure, including **TRON**, **Aptos**, and **BNB Smart Chain** services. The loaders retrieve encrypted second-stage material, decrypt it with embedded XOR keys, and execute the resulting JavaScript with `eval()`.

Observed follow-on payload capabilities include command execution, `socket.io-client`-based C2 communication, credential theft, browser-data theft, and wallet exfiltration. Because the first stage is a loader, defenders should treat the campaign as capable of delivering additional malware even when a specific artifact has only been linked publicly to DEV#POPPER or OmniStealer.

## Defender heuristics

### Repository and code review
- Review GitHub **Activity** and audit logs, not only the repository landing page or latest visible commit metadata.
- Treat recent force pushes that rewrite older commits as high-risk, especially when followed by package releases.
- Search source trees for long-line whitespace padding in executable files and configuration files, including `config.js`, `vite.config.js`, `eslint.config.js`, `astro.config.mjs`, package-manager scripts, CI YAML, and IDE task files.
- Hunt for fake static assets executed by Node.js, especially `.woff2` files referenced from `.vscode/tasks.json` with `"runOn": "folderOpen"`.
- Review repositories under a shared maintainer account for synchronized modification timestamps; bulk edits across unrelated projects can indicate account-level compromise.

### Endpoint and CI triage
- Treat any developer machine or CI runner that installed affected artifacts or opened/build trusted source trees as potentially compromised.
- Preserve evidence before cleanup where possible, then rebuild from known-good lockfiles and known-clean repository history.
- Rotate reachable GitHub, npm, PyPI, RubyGems, Packagist/Composer, Go proxy, cloud, Vault, Kubernetes, Docker, SSH, Slack, Twilio, and CI/CD credentials from a clean machine.
- Inventory VS Code workspace tasks and other IDE/agent auto-execution surfaces, not just dependency manifests.
- Correlate package install timestamps with browser-data theft, wallet access, source-code cloning, unexpected package publishes, GitHub workflow changes, and cloud control-plane activity.

### Package and registry controls
- Diff new package releases against prior clean versions before adoption, especially after maintainer account recovery events or unusual Git history changes.
- Flag packages that unexpectedly add `composer-plugin` behavior, lifecycle hooks, folder-open tasks, fake assets, or large obfuscated JavaScript.
- Prefer release cooldowns, maintainer MFA/passkey enforcement, registry token scoping, and protected publishing workflows for high-blast-radius packages.
- Do not assume that absence of a malicious release in one registry means the repository is clean; Socket reported cases where repository compromise did not produce corresponding npm or PyPI publishes.

## Related pages
- [Astro config blockchain C2 PR injection](astro-config-blockchain-c2-pr-injection.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [UNK_DeadDrop developer repository phishing](unk-deaddrop-developer-repository-phishing.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Famous Chollima Packagist dev-branch loader](famous-chollima-packagist-dev-branch-loader.md)

## Sources
- [Socket](https://socket.dev/blog/polinrider-north-korea-linked-supply-chain-campaign-expands)
- [Socket live campaign tracker](https://socket.dev/supply-chain-attacks/polinrider)
