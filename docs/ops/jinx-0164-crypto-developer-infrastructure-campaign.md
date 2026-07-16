# JINX-0164 crypto developer infrastructure campaign

## Summary
Wiz CIRT and Wiz Research reported JINX-0164, a financially motivated threat actor active since at least mid-2025 that targets cryptocurrency organizations through LinkedIn social engineering, fake meeting / troubleshooting flows, custom macOS malware, credential theft, source-repository abuse, and package-supply-chain compromise.

The most important operational lesson is the chain from a single developer laptop to trusted distribution systems: JINX-0164 used endpoint access to steal GitHub, cloud, package, and local secrets, then abused source repositories and CI/CD-adjacent infrastructure to spread the same malware internally. Wiz also linked the actor to the April 2026 trojanized `@velora-dex/sdk@4.9.1` npm package, which delivered MINIRAT through an import-time shell downloader.

## Tags
- ops
- operations
- JINX-0164
- cryptocurrency
- DeFi
- developer-targeting
- supply-chain
- npm
- GitHub
- CI/CD
- macOS
- LinkedIn
- social engineering
- ClickFix
- credential-theft
- infostealer
- RAT
- AUDIOFIX
- MINIRAT
- launchctl
- source-code compromise
- cloud secrets
- financial theft

## Why this matters
- The campaign shows how cryptocurrency-sector social engineering can become a source-code and CI/CD incident rather than only an endpoint compromise.
- Developer laptops exposed GitHub tokens, package credentials, SSH keys, cloud keys, password-manager material, browser data, shell history, crypto-wallet artifacts, and communication-app sessions.
- Internal repository poisoning let the actor turn normal developer build/update behavior into lateral movement.
- The `@velora-dex/sdk` compromise demonstrates that JINX-0164 can also reach downstream users through public package ecosystems.

## Attack chain
### Initial access
- The actor used LinkedIn personas that appeared credible for the cryptocurrency industry, including recruiter or business-partner approaches.
- Victims were moved to fake meeting or troubleshooting pages impersonating services such as Microsoft Teams, Slack, Aircall, driver update portals, or cryptocurrency companies.
- The fake pages delivered a macOS-focused installer or command-line fix for an alleged meeting/audio problem.

### Malware delivery
- Wiz observed a bash script hosted from a fake driver-store domain that downloaded architecture-aware macOS payloads for Intel and Apple Silicon hosts.
- The payload masqueraded as an audio driver or updater, with names such as `coreaudiod` and `ChromeUpdater`, and used `launchctl` for execution/persistence.
- AUDIOFIX is the main reported Python-based macOS infostealer/RAT in the social-engineering cases.

### Credential theft and lateral movement
- AUDIOFIX collected local and cloud-development secrets, including Keychain material, browser credentials, local admin credentials, SSH keys, configuration files, cloud keys, package-manager credentials, console history, cryptocurrency wallet data, and communication-app sessions.
- Wiz reported stolen GitHub tokens being used with `nord-stream` to exfiltrate GitHub Actions secrets from CI/CD pipelines.
- The actor then used access to internal code distribution systems and source repositories, showing relatively little interest in broad traditional cloud pivoting compared with development-infrastructure abuse.

### Repository poisoning
- In affected internal repositories, JINX-0164 injected the same Python RAT into code to infect additional employees when they updated or built projects.
- The actor used deceptive Git tactics: direct-to-main commits in unprotected repositories, branch hijacking when direct main access failed, and modified committer metadata to impersonate other developers.
- Wiz reported that GitHub Vigilant Mode, unverified commit badges, GPG-key/user mismatches, and audit logs tying pushes to the initially compromised endpoint helped identify the malicious commits.

### Public package compromise
- On 2026-04-07, JINX-0164 trojanized `@velora-dex/sdk@4.9.1` on npm.
- The malicious release appended JavaScript to `dist/index.js` that decoded and executed a shell downloader when the package was imported.
- The shell script downloaded MINIRAT, a lightweight Go backdoor with host registration, file upload/download, and command-execution capability.
- Wiz reported the package source on GitHub was not modified, suggesting access to npm publishing credentials rather than a source-repository change for that public package.

## Malware notes
### AUDIOFIX
- Python 3.12-based macOS malware with infostealer and backdoor behavior.
- Supports attacker-directed fake password prompts, broad local secret harvesting, and HTTPS or Dropbox-style exfiltration / command paths depending on variant.
- Reported TCC-prompt abuse attempts include AppleScript-triggered Finder automation prompts paired with distraction UI.

### MINIRAT
- Lightweight Go backdoor used in the Velora supply-chain operation and observed in later activity.
- Shares reported hard-coded C2 domains with AUDIOFIX variants: `datahub.ink`, `cloud-sync.online`, and `byte-io.us`.
- Less automated exfiltration than AUDIOFIX, but sufficient for follow-on file transfer and command execution.

## Infrastructure and evasion notes
- Actor-controlled infrastructure imitated legitimate meeting providers, support pages, driver portals, and cryptocurrency brands, often copying real pages and localizations while placing malicious content on one targeted page.
- Wiz observed VPN use through Mullvad, Astrill, and ExpressVPN for cloud and SaaS activity.
- The campaign is macOS-focused in public reporting, but Wiz noted infrastructure such as Windows-themed driver domains that may indicate broader targeting plans.

## Defender heuristics
- Treat fake-meeting / audio-fix incidents involving developers as potential source-repository, package-registry, and cloud-credential incidents.
- Isolate the developer endpoint before rotating secrets if active malware may still be running; preserve volatile/audit evidence where possible.
- Search macOS endpoints for unexpected `launchctl` jobs, updater/audio-driver masquerading, `ChromeUpdater` / `coreaudiod`-like payload names, suspicious `~/.zsh_cache` password artifacts, and outbound traffic to reported JINX-0164 infrastructure.
- Review GitHub audit logs for pushes, token use, secret access, repository cloning, and Actions-secret exfiltration from the compromised endpoint or unusual VPN egress.
- Enable or enforce signed-commit / vigilant-mode workflows for high-trust repositories, and investigate unverified commits whose author metadata does not match the signing key or push actor.
- Diff internal repositories touched during the exposure window for RAT injections, shell downloaders, install/build hook changes, and branch-only payload insertions.
- For cryptocurrency / DeFi SDK maintainers, compare npm package contents against source tags and alert on import-time shell execution, new lifecycle hooks, or package artifacts that do not match the repository.

## Related pages
- [JINX-0164](../actors/jinx-0164.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- Wiz: <https://www.wiz.io/blog/threat-actors-target-crypto-orgs>
- StepSecurity Velora DEX SDK coverage: <https://www.stepsecurity.io/blog/velora-dex-sdk-compromised-on-npm-malicious-version-drops-macos-backdoor-via-launchctl-persistence>
- iru MINIRAT coverage: <https://www.iru.com/blog/minirat>
