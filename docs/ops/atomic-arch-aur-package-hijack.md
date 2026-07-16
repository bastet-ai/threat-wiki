# Atomic Arch AUR package hijack

## Summary
Sonatype Security Research and StepSecurity reported **Atomic Arch** in June 2026: a supply-chain campaign that abused Arch User Repository (AUR) orphan-package adoption to turn trusted community `PKGBUILD` projects into a malware-delivery path. Attackers reportedly adopted abandoned AUR packages and modified build/install logic to fetch malicious npm dependencies such as `atomic-lockfile`, `js-digest`, and `lockfile-js`.

Track this as an operation because the durable defender lesson is not limited to Arch Linux: package ownership transfer, local build scripts, and cross-ecosystem dependency fetches can become developer-workstation and self-hosted-runner compromise paths.

## Tags
- ops
- operations
- supply-chain
- AUR
- Arch Linux
- npm
- PKGBUILD
- developer-workstations
- CI-CD
- credential-theft
- Rust
- Linux
- eBPF
- rootkit

## Why this matters
- AUR packages execute local build logic on developer machines; malicious `PKGBUILD` or install-hook changes can run before users see a traditional binary package boundary.
- The campaign abused trust inheritance: attackers could adopt orphaned packages with existing reputation instead of building new malicious package names from scratch.
- Sonatype's initial reporting tied the malicious AUR changes to npm dependency installation, making Atomic Arch a cross-ecosystem chain rather than an Arch-only packaging issue.
- StepSecurity reported more than 400 modified AUR packages; Sonatype said follow-on community audits could put impacted packages around 1,500 and that investigation was ongoing.
- Developer and CI impact depends on where AUR is used: Arch / Arch-derived workstations, WSL2 Arch environments, and self-hosted Arch runners are higher-risk than GitHub-hosted runners or non-Arch CI images.

## Reported chain

### Orphan-package adoption
- AUR lets community members maintain `PKGBUILD` recipes for software outside Arch's official repositories.
- When packages become orphaned, another user can request adoption and inherit the package name, history, and user trust.
- Sonatype described Atomic Arch as exploiting this stewardship process: attackers adopted abandoned packages and changed build instructions while the packages still looked like familiar community projects.

### Malicious build dependency
- Sonatype reported `PKGBUILD` changes that introduced post-install logic such as `npm install atomic-lockfile minimist chalk`.
- The malicious dependency was not necessarily present in the AUR package itself; the AUR script pulled it from npm during build/install.
- Sonatype tied the campaign to malicious npm packages including `atomic-lockfile`, `js-digest`, and `lockfile-js`.
- Sonatype also observed at least one wave that appeared to use Bun rather than npm as part of the install path.

### Payload behavior
- Sonatype analyzed `atomic-lockfile` and found a bundled native Linux executable executed during installation.
- The binary included Linux payload functionality tied to credential harvesting, stealth, anti-debugging, archive / multipart upload support, and likely data exfiltration behavior such as references to `POST /upload`.
- StepSecurity described the payload as a Rust credential stealer with optional rootkit-like behavior when it gains elevated privileges.
- Reported target classes include browser cookies and sessions, SSH keys, GitHub / npm / developer tokens, Slack / Discord / Teams sessions, Docker / Podman credentials, and cloud access keys.
- StepSecurity warned that elevated execution can enable eBPF-style persistence or hiding of processes and file activity; treat affected hosts as compromised rather than relying on one-time malware scanning.

## Exposure and triage

### Systems most exposed
- Arch Linux and Arch-derived developer machines such as EndeavourOS or Manjaro when users enable AUR helpers.
- Windows developer workstations using Arch inside WSL2 and installing AUR packages in that environment.
- Self-hosted CI runners or build agents based on Arch that bootstrap from AUR packages during jobs.
- Any build pipeline that treats `PKGBUILD` recipes or AUR helper output as trusted without reviewing fetched secondary dependencies.

### Lower direct exposure
- GitHub-hosted Ubuntu / Windows / macOS runners do not use AUR by default.
- Debian, Ubuntu, RHEL, Rocky, macOS, and Windows hosts are not directly affected by the AUR adoption vector unless they invoke Arch / AUR through containers, WSL, nested virtualization, or custom build steps.

## Defender heuristics

### AUR and package review
- Inventory Arch and Arch-derived endpoints that use AUR helpers, including developer WSL2 environments.
- Review recently installed or upgraded AUR packages for ownership changes, orphan-adoption events, modified `PKGBUILD`, `.install`, `prepare()`, `build()`, `package()`, and post-install logic.
- Flag AUR recipes that invoke `npm`, `bun`, `curl | sh`, remote JavaScript, or other secondary package managers during build/install unless that behavior is expected and pinned.
- For high-value developer hosts, rebuild from a clean image if a malicious AUR package executed, then rotate exposed credentials after containment.

### Endpoint and CI hunting
- Search shell history, package-manager logs, and CI job output for `atomic-lockfile`, `js-digest`, `lockfile-js`, and unexpected `npm install` / Bun execution during AUR package builds.
- Hunt for new native Linux binaries spawned from package build directories or npm cache paths.
- Review access to SSH keys, browser profile stores, Docker / Podman config, cloud credential files, and package-registry tokens from the suspected execution window.
- On Arch self-hosted runners, preserve job logs and filesystem artifacts before rotating secrets so responders can identify which credentials and repositories were reachable.

### Governance lessons
- Treat community package adoption and maintainer transfer as a security event for critical dependencies.
- Require human review for build scripts that fetch executable code from a second ecosystem at install time.
- Prefer pinned, checksummed source artifacts over live package-manager resolution inside packaging recipes.
- Keep developer endpoint detection in scope for open-source supply-chain incidents; package build scripts execute on the machine that holds the credentials attackers want.

## Related pages
- [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md)
- [IronWorm npm Rust infostealer campaign](ironworm-npm-rust-infostealer.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- Sonatype Security Research: [https://www.sonatype.com/blog/atomic-arch-npm-campaign-adds-malicious-dependency](https://www.sonatype.com/blog/atomic-arch-npm-campaign-adds-malicious-dependency)
- Sonatype vulnerability guide entry: [https://guide.sonatype.com/vulnerability/sonatype-2026-003775/sonatype-research](https://guide.sonatype.com/vulnerability/sonatype-2026-003775/sonatype-research)
- StepSecurity: [https://www.stepsecurity.io/blog/400-aur-packages-hijacked-atomic-arch-campaign](https://www.stepsecurity.io/blog/400-aur-packages-hijacked-atomic-arch-campaign)
