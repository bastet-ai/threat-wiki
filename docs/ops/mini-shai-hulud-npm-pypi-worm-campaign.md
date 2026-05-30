# Mini Shai-Hulud npm/PyPI worm campaign

## Summary
Mini Shai-Hulud is the 2026 continuation of the Shai-Hulud npm worm tradecraft: malicious package installs execute inside developer or CI/CD environments, steal credentials, and use reachable publishing or repository access to spread into additional packages and repositories.

Public reporting from Wiz, Snyk, Akamai, JFrog, Socket, Unit 42, and Microsoft describes multiple waves in April-May 2026. Several vendors attribute the later waves to **TeamPCP** or describe them as TeamPCP-linked; keep that attribution caveated unless a firsthand operator statement or official source is being cited directly.

## Page role
This is the canonical operation page for the broad Mini Shai-Hulud npm/PyPI campaign. Keep actor-level judgments on [TeamPCP](../actors/teampcp.md) and narrow April 22 Bitwarden/Checkmarx distribution-lane details on [Bitwarden / Checkmarx Shai-Hulud Third Coming campaign](bitwarden-checkmarx-shai-hulud-third-coming.md).

## Tags
- ops
- operations
- supply-chain
- npm
- PyPI
- GitHub Actions
- CI/CD
- OIDC
- SLSA
- credential-theft
- worm
- TeamPCP
- Shai-Hulud

## Why this matters
- The May 2026 TanStack wave showed that a malicious npm release can carry **valid provenance/attestation** when the legitimate release workflow is hijacked before publication.
- The campaign targets the places with the most blast radius: developer laptops, GitHub Actions runners, npm trusted-publishing workflows, cloud credentials, Kubernetes secrets, and package maintainer accounts.
- Removing a compromised package is not enough if the payload already created persistence, poisoned repository files, or extracted tokens that can publish more packages.

## Publicly reported wave sequence

### September-November 2025: original Shai-Hulud waves
- Microsoft and Unit 42 describe the original Shai-Hulud activity as a self-propagating npm worm era shift.
- The campaign pattern: run during package install, steal tokens/secrets, create public exfiltration repositories, and use npm access to republish infected packages.
- Later 2025 waves added more automation and destructive behavior.

### March 2026: TeamPCP / Trivy precursor activity
- Wiz and other researchers reported a TeamPCP-linked Trivy compromise that used GitHub Actions/release infrastructure to steal runner secrets and publish malicious artifacts.
- This established several recurring motifs later seen in Mini Shai-Hulud coverage: runner memory scraping, cloud/Kubernetes credential harvesting, package/release trust abuse, encrypted exfiltration, and fallback GitHub repository exfiltration.
- <a id="2026-05-25-wiz-teampcp-post-compromise"></a>Wiz CIRT's post-compromise reporting shows why stolen-token handling needs to extend beyond package cleanup: observed TeamPCP activity validated cloud and SaaS secrets with TruffleHog-style API calls within hours, enumerated AWS IAM/EC2/Lambda/RDS/Route 53/S3/ECS/Secrets Manager, abused GitHub PATs to create malicious workflow pull requests and delete workflow logs, cloned repositories at scale, used ECS Exec / SSM paths for code execution inside containers, and pulled data from S3, databases, Secrets Manager, and source repositories.
- See also: [Trivy → TeamPCP → CanisterWorm timeline](trivy-lite-llm-compromise-timeline.md).

### April 22, 2026: Bitwarden / Checkmarx "Third Coming" wave
- Unit 42 reported a TeamPCP-attributed wave that included malicious `@bitwarden/cli@2026.4.0` and public GitHub artifacts containing the string `Shai-Hulud: The Third Coming`.
- The same payload family reportedly appeared across Checkmarx distribution lanes: poisoned `checkmarx/kics` Docker Hub images, `checkmarx/ast-github-action`, and Checkmarx VS Code extensions.
- Unit 42's reported `@bitwarden/cli` package used both a `preinstall` hook and a `bw` command-name masquerade path via `bw_setup.js`, giving the malware a secondary execution path even when install scripts were blocked.
- This wave adds a durable defender lesson for later Mini Shai-Hulud triage: package-registry compromise, IDE-extension compromise, Docker image poisoning, and GitHub Actions abuse can all be lanes for the same payload and credential-theft infrastructure.
- See also: [Bitwarden / Checkmarx Shai-Hulud Third Coming campaign](bitwarden-checkmarx-shai-hulud-third-coming.md).

### April 29-30, 2026: SAP / Intercom / PyPI / Packagist expansion
- Wiz reported Mini Shai-Hulud-style malicious versions in SAP ecosystem npm packages including `@cap-js/sqlite`, `@cap-js/postgres`, `@cap-js/db-service`, and `mbt`.
- The same reporting later added `intercom-client` and PyPI `lightning` packages as related compromises under analysis.
- Reported behavior included `preinstall` execution, Bun-based loaders, obfuscated JavaScript payloads, cloud/GitHub/npm/Kubernetes/Vault credential harvesting, Russian locale guardrails, and GitHub-based encrypted exfiltration.
- Wiz assessed TeamPCP responsibility with high confidence based on shared cryptographic material and implementation overlaps, while noting that references to older Shai-Hulud operations do not by themselves prove a single operator across every wave.
- <a id="2026-05-24-socket-sap-cap-details"></a>Socket's SAP CAP / Cloud MTA analysis adds operationally useful detail: `mbt@1.2.48`, `@cap-js/db-service@2.10.1`, `@cap-js/postgres@2.2.2`, and `@cap-js/sqlite@2.2.2` were published in a short April 29 window with injected `package.json`, `setup.mjs`, and large obfuscated `execution.js` files. The loader downloaded Bun `1.3.13` from GitHub Releases when Bun was absent, ran the payload under Bun, and deleted the temporary runtime directory. Socket estimated meaningful SAP ecosystem reach at roughly 52k weekly downloads for `mbt`, 10k for `@cap-js/postgres`, 260k for `@cap-js/db-service`, and 250k for `@cap-js/sqlite`.
- Socket reported the SAP payload family mirrored Bitwarden/Checkmarx cryptographic tooling, including a PBKDF2 / XOR string-protection layer, while generating unique deployment keys per payload. On developer hosts it harvested SSH keys, cloud credentials, Kubernetes config, Docker/Git/npm material, environment files, AI-tool configs such as Claude/Kiro MCP settings, crypto wallets, messaging app data, shell history, GitHub CLI tokens, and cloud metadata credentials; on CI runners it attempted `Runner.Worker` memory scraping to recover masked GitHub Actions secrets.
- Socket reported that `intercom-client@7.0.4` introduced `setup.mjs` plus an 11.7 MB `router_runtime.js` payload, ran during npm `preinstall`, downloaded Bun from GitHub without integrity checks, harvested Kubernetes/Vault/cloud/developer secrets, and exfiltrated through GitHub infrastructure.
- Socket's follow-up expanded the Intercom chain into Packagist: `intercom/intercom-php@5.0.2` was replaced by force-updated tag metadata and converted into a Composer plugin via `composer-plugin-api`, `src/composerPlugin.php`, `post-install-cmd` / `post-update-cmd`, and `setup-intercom.sh`, which downloaded Bun `1.3.13` and executed the same `router_runtime.js`-style payload.
- Intercom told Socket the root cause was a local install of `pyannote-audio` that pulled the compromised PyPI `lightning` dependency, linking a PyPI foothold to the npm `intercom-client` compromise and then to the Packagist `intercom/intercom-php` artifact. This is a durable ecosystem-expansion lesson: Mini Shai-Hulud-style activity can move from a developer endpoint into multiple package registries through local dependency installs, repository access, and mutable package metadata rather than through one registry's native publishing flow alone.

### May 11-12, 2026: TanStack and trusted-publishing abuse
- Snyk reported malicious artifacts across `@tanstack/*` packages published by the legitimate TanStack release pipeline after attacker-controlled code hijacked the runner mid-workflow.
- Unit 42 later quantified the initial TanStack burst as 84 malicious artifacts across 42 `@tanstack/*` packages within six minutes, expanding by end of day to 373 malicious versions across 169 npm packages plus compromised PyPI packages. Unit 42 estimated roughly 520 million cumulative downloads during the affected window.
- Snyk’s key point: SLSA provenance can prove where the artifact was built, but it does not prove the runtime workflow was clean if attacker-controlled code executed before publication. Unit 42 called this the first documented case of a worm publishing malicious npm packages with valid SLSA Build Level 3 provenance.
- Akamai, JFrog, and Unit 42 describe the chain as privileged workflow abuse: a `pull_request_target` workflow checked out fork-controlled code, a poisoned `pnpm` cache was written with a precomputed release cache key, a legitimate release workflow later restored that state, and the payload extracted GitHub Actions OIDC material from `Runner.Worker` memory to obtain npm publishing credentials.
- Unit 42 reported that the malicious TanStack packages used an injected `optionalDependencies` reference to an orphaned commit surfaced under the legitimate fork network, while secondary propagation victims such as UiPath, Mistral AI, and OpenSearch reverted to more familiar `preinstall` execution.
- Unit 42 also warned that the May 11 payload installed a background service that polled `api.github.com/user` with the stolen token and, if the token was revoked while the daemon was active, executed destructive home-directory deletion. This makes containment order especially important: stop active execution and isolate hosts before broad token revocation when this variant may be running.
- Akamai and Unit 42 reported that weaponized Mini Shai-Hulud source code appeared publicly on GitHub after the TanStack wave, increasing copycat risk and weakening attribution based only on worm lineage. Socket separately reported that TeamPCP and BreachForums promoted a Shai-Hulud supply-chain attack contest, creating an explicit incentive for lower-tier copycats to target package ecosystems by download count.
- <a id="2026-05-30-ox-copycat-packages"></a>OX Security reported a concrete copycat cluster after the source-code leak: four typosquatted npm packages (`chalk-tempalte`, `@deadcode09284814/axios-util`, `axois-utils`, and `color-style-utils`) from one publisher, with `chalk-tempalte` described as an almost unmodified Shai-Hulud clone. OX reported infostealer behavior across the set, one DDoS botnet-style `phantom bot` package, C2 / exfiltration endpoints including `87e0bbc636999b[.]lhr[.]life`, `80[.]200[.]28[.]28:2222`, `b94b6bcfa27554[.]lhr[.]life`, and `edcf8b03c84634[.]lhr[.]life`, and GitHub dead-drop repository strings such as `A Mini Sha1-Hulud has Appeared`. This reinforces that copycat triage should not assume TeamPCP authorship merely because the payload lineage or strings match the leaked worm.
- On May 27, CISA added **CVE-2026-45321** to KEV for the TanStack incident, describing malicious `@tanstack/*` releases published under a trusted identity and setting a June 10 remediation due date for covered agencies. Treat this as public exploitation validation for the trusted-publishing / cache-poisoning lane, not as a normal application bug.

### April-May 2026: broader npm/PyPI spread
- JFrog reported a TeamPCP-linked / possible-copycat compromise of the legitimate `xinference` PyPI release line: versions `2.6.0`, `2.6.1`, and `2.6.2` executed from `xinference/__init__.py` on import, spawned a detached Python payload, collected developer/cloud/Kubernetes secrets, and exfiltrated `love.tar.gz` to `whereisitat[.]lucyatemysuperbox[.]space` with header `X-QT-SR: 14`. TeamPCP publicly denied involvement, so keep attribution caveated.
- JFrog reported more than 170 npm packages and 2 PyPI packages affected in its earlier analysis window, with npm payloads using malicious `preinstall` loaders and PyPI payloads using import-time downloaders.
- JFrog's May 19 follow-up counted the AntV wave as 325 legitimate npm packages after identifying `@cap-js/openapi@1.4.1`; the added package used a cleaner-looking `optionalDependencies` reference to `github:cap-js/openapi#d78c25443ec4a0d7f0a85776461f3b1163132537` and delivered the Shai-Hulud payload from fork-resolvable GitHub content rather than embedding malicious code directly in the tarball.
- Socket reported continuing package findings across npm and PyPI ecosystems, including OpenSearch, Mistral AI, Guardrails AI, Squawk, and other artifacts in related coverage. In its May 12 update, Socket named `@opensearch-project/opensearch` npm versions `3.5.3`, `3.6.2`, `3.7.0`, and `3.8.0`, PyPI `mistralai@2.4.6`, PyPI `guardrails-ai@0.10.1`, and additional `@squawk/*` packages such as `@squawk/mcp@0.9.5`, `@squawk/weather@0.5.10`, and `@squawk/flightplan@0.5.6`.
- Socket's `guardrails-ai@0.10.1` analysis is operationally important because it used Python import-time execution rather than npm lifecycle execution: on Linux it downloaded `https://git-tanstack[.]com/transformers.pyz` to `/tmp/transformers.pyz` and executed it with `python3` without integrity verification. Socket reported the `git-tanstack[.]com` host displayed a TeamPCP-signed taunt while the infrastructure was live, giving defenders another infrastructure and import-time-loader pivot for the May 11 wave.
- Socket also reported a separate February 2026 Shai-Hulud-style `SANDWORM_MODE` cluster that used typosquatted npm packages and a malicious GitHub Action to target CI secrets and AI coding toolchains; track it separately because the delivery model and MCP prompt-injection tradecraft differ from the May Mini Shai-Hulud waves.
- StepSecurity, Snyk, and Unit 42 reported an AntV-centered wave involving the `atool` maintainer account, `timeago.js`, `echarts-for-react`, and many `@antv/*` visualization packages. StepSecurity described a two-wave May 19 publish pattern: first using a `preinstall` hook that invoked Bun, then adding Bun as an explicit dependency to improve delivery reliability.
- Unit 42 counted approximately 639 malicious package versions across 323 unique packages in about one hour, calling it the largest single-hour package count of any Shai-Hulud wave observed in its reporting.
- Socket later summarized the same AntV burst as 639 malicious versions across 323 unique packages after the `atool` npm maintainer account was seized, and said npm responded on May 19 by invalidating all granular access tokens with write access that bypass two-factor authentication. Socket's campaign rollup counted 1,055 Mini Shai-Hulud package versions across 502 unique packages at that point: 1,048 npm versions across 498 packages, six PyPI entries across three packages, and one Composer package-version entry.
- <a id="2026-05-26-safedep-antv-details"></a>SafeDep's May 19 AntV / `atool` analysis adds several concrete detection pivots for the same wave: it counted 637 malicious versions across 317 packages in a roughly 22-minute automated burst, reported payload SHA256 `a68dd1e6a6e35ec3771e1f94fe796f55dfe65a2b94560516ff4ac189390dfa1c`, and identified orphan/imposter `antvis/G2` commits `1916faa365f2788b6e193514872d51a242876569`, `7cb42f57561c321ecb09b4552802ae0ac55b3a7a`, and `dc3d62a2181beb9f326952a2d212900c94f2e13d` as redundant payload-delivery paths via `@antv/setup` optional dependencies. SafeDep also described dual exfiltration through GitHub dead-drop repositories and `t.m-kosche[.]com` OpenTelemetry-looking HTTPS posts, Docker-socket host escape attempts, local Node.js project propagation, `.github/workflows/codeql.yml` persistence named `Run Copilot`, AI-assistant SessionStart hooks for Claude Code / Codex, VS Code `runOn: folderOpen` tasks, `kitty-monitor` GitHub commit-search C2 using the `firedalazer` keyword, and a `gh-token-monitor` daemon that repeatedly polled stolen GitHub tokens.
- Wiz's May 19 AntV writeup adds a compact TeamPCP-attribution and persistence pivot set for the same wave: moderate-confidence TeamPCP attribution based on infrastructure, malware behavior, and operational overlap; backup C2 `m-kosche[.]com` / `185.95.159.32`; GitHub commit search for `api.github.com/search/commits?q=firedalazer`; persistent backdoor path `~/.local/share/kitty/cat.py`; macOS LaunchAgent `~/Library/LaunchAgents/com.user.kitty-monitor.plist`; Linux user service `~/.config/systemd/user/kitty-monitor.service`; and backdoor SHA256 `fb5c97557230a27460fdab01fafcfabeaa49590bafd5b6ef30501aa9e0a51142`.
- Treat that npm-wide reset as an incident-response interruption, not a root-cause fix: Socket noted that it burns already stolen bypass-2FA tokens but does not address workflow-level publication paths such as TanStack-style OIDC extraction, cache poisoning, or compromised trusted-publishing pipelines.
- GitHub's May 22 npm changelog made staged publishing generally available in npm CLI `11.15.0` or newer. The feature lets CI upload a prebuilt tarball into a stage queue, then requires a human maintainer to pass a 2FA challenge before the package becomes installable; it can be paired with OIDC trusted publishing and configured so a workflow may only run `npm stage publish`, not direct `npm publish`. This is a meaningful mitigation for unattended CI publication, but not a substitute for cleaning compromised workflows, runners, caches, and maintainer endpoints.
- The same npm release added install-source allowlist controls: `--allow-file`, `--allow-remote`, and `--allow-directory`, complementing `--allow-git`. These flags matter for Mini Shai-Hulud-style defense because several waves used non-registry GitHub/orphan-commit or remote runtime paths instead of obvious malicious code embedded directly in the registry tarball.
- StepSecurity, JFrog, and Unit 42 reported that AntV-wave payloads read GitHub Actions runner process memory to recover masked CI/CD secrets, harvested developer/cloud/Kubernetes/Vault/crypto-tool paths, queried local password-manager CLIs including 1Password, Bitwarden, `pass`, and `gopass`, exfiltrated through a GitHub dead-drop and `t.m-kosche[.]com`, and created public Dune/Shai-Hulud-themed repositories from stolen tokens. JFrog also reported that the npm payload logic could request GitHub Actions OIDC material, exchange it for npm trusted-publishing credentials, and create Sigstore provenance, reinforcing that valid provenance can be produced by a compromised workflow.
- StepSecurity and Snyk reported malicious `durabletask` PyPI versions `1.4.1`, `1.4.2`, and `1.4.3` in Microsoft's official Durable Task Python SDK. Unlike the TanStack trusted-publishing chain, these uploads reportedly bypassed the GitHub release workflow and used real PyPI publishing credentials.
- The `durabletask` payload was reported as a Linux-focused Python zipapp (`rope.pyz`) that harvested AWS, Azure, GCP, Kubernetes, password-manager, and developer-tool secrets, used redundant exfiltration paths, installed fake systemd persistence, attempted lateral movement via AWS SSM and Kubernetes `kubectl exec`, skipped Russian-locale systems, and used TeamPCP-linked infrastructure (`t.m-kosche[.]com`). JFrog reported AWS SSM propagation state under `/tmp/.rope_state/ssm_instances.json`, an SSM marker at `~/.cache/.sys-update-check`, Kubernetes propagation marker `~/.cache/.sys-update-check-k8s`, and attempts to propagate to up to five non-Windows SSM instances or Kubernetes pods where permissions allowed. Wiz additionally reported primary C2 at `check.git-service[.]com`, downloaded payload paths such as `/tmp/managed.pyz` and `/tmp/rope-*.pyz`, and infection markers `~/.cache/.sys-update-check` and `~/.cache/.sys-update-check-k8s`.
- Grafana Labs publicly stated that the TanStack/Mini Shai-Hulud incident led to unauthorized access to its GitHub environment and source-code download after one impacted workflow token was missed during rotation. Grafana reported no evidence of production-system or Grafana Cloud compromise and said its codebase was downloaded but not altered.

### May 2026: adjacent GitHub Actions and IDE-extension lanes
- StepSecurity reported compromised `actions-cool/issues-helper` and `actions-cool/maintain-one-comment` GitHub Actions where all release tags were moved to imposter commits. The malicious action downloaded Bun, read `Runner.Worker` memory for decrypted workflow secrets, and exfiltrated to `t.m-kosche[.]com`, matching infrastructure and runner-memory-theft motifs seen in the broader Mini Shai-Hulud cluster.
- StepSecurity reported a compromised Nx Console VS Code extension (`nrwl.angular-console` `18.95.0`) that fetched an obfuscated payload from an orphan commit in the official `nrwl/nx` repository. This is not the same registry lane as npm/PyPI worming, but it targets the same developer-trust boundary.
- GitHub publicly confirmed a May 18 employee-device compromise involving a poisoned third-party VS Code extension and linked to the Nx Console security advisory; GitHub said the activity involved exfiltration of GitHub-internal repositories only and that the attacker's roughly 3,800-repository claim was directionally consistent with its investigation.
- See also: [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md) and [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md).

## Tradecraft map

### Initial access / publication path
- `pull_request_target` or similar privileged workflow footguns that run fork-controlled code in a privileged repo context.
- GitHub Actions cache poisoning or runner-state poisoning that survives until a legitimate release workflow executes.
- OIDC/trusted-publishing token extraction from runner memory, then exchange for short-lived npm publishing credentials.
- Compromised maintainer/package publisher accounts in some waves.

### Execution and payload staging
- npm lifecycle hooks such as `preinstall`.
- Bun runtime download/execution to run large JavaScript payloads.
- PyPI import-time loader/downloader behavior in related Python packages.
- Composer plugin install/update hooks and mutable Packagist tag metadata in PHP ecosystem compromises.
- Heavy obfuscation and embedded encrypted payload sections.

### Credential harvesting
- GitHub PAT/OAuth tokens and Actions runtime secret material.
- npm tokens and trusted-publishing exchange material.
- AWS, Azure, GCP, Kubernetes, Docker, Vault, Terraform, SSH, Git, shell history, `.npmrc`, cloud config, and generic API secrets.
- Kubernetes API enumeration where service-account permissions allow it.
- Browser/password-store collection reported in later variants.

### Exfiltration and propagation
- Encrypted exfiltration via attacker-controlled infrastructure.
- GitHub fallback/dead-drop repositories created in victim accounts.
- Repo naming/description patterns reported by vendors, including Dune/Shai-Hulud themed descriptions and configuration-storage masquerades.
- Automated enumeration of packages the victim can publish, tarball modification, version bumping, metadata injection, and republishing.
- Repository poisoning through `.claude/`, `.codex/`, and `.vscode/` files in variants that try to reach AI coding agents and IDE automation. JFrog reported SessionStart hook injection for Claude Code/Codex settings and a VS Code `folderOpen` task path in the May 19 wave.
- GitHub commit-search C2/persistence: JFrog reported `kitty-monitor`, which searched GitHub commits for signed command markers such as `firedalazer`; the `@cap-js/openapi` variant used separate markers including `thebeautifulsnadsoftime` and `thebeautifulmarchoftime`.
- GitHub Actions tag retargeting as an adjacent lane: trusted action tags can be moved to imposter commits, allowing malicious runtime code to read runner memory and steal secrets.
- IDE-extension compromise as an adjacent lane: poisoned VS Code extensions can reach developer endpoints even when package lockfiles and build dependencies are clean.

### Persistence / destructive behavior
- Claude Code hooks and VS Code task automation reported as persistence or re-execution paths.
- Background daemon behavior and dead-man-switch style deletion/wiping behavior reported in later Shai-Hulud/Mini Shai-Hulud analysis.
- Developer endpoints and CI runners should be treated as compromised hosts, not just as places where a bad dependency was installed.

## Defender heuristics

### Exposure triage
- Search dependency lockfiles, package-manager caches, CI logs, and artifact repositories for affected package names/versions from vendor advisories.
- Treat any install of affected versions in CI or on a developer machine as credential exposure.
- Prioritize environments with npm publishing permissions, GitHub org/admin tokens, cloud deployment credentials, Kubernetes service-account access, or Vault access.

### GitHub and CI hunting
- Look for `pull_request_target` workflows that check out or execute fork-controlled code.
- Review caches restored by release workflows, especially caches writable by pull-request jobs.
- Hunt workflow logs for unexpected Bun downloads, large obfuscated JavaScript payloads, `preinstall` execution, runner memory scraping, or token/OIDC environment access.
- Search for unexpected repositories created by maintainers/bots with Shai-Hulud/Dune/config-storage descriptions or encrypted blobs; Unit 42 notes that later variants can use both GitHub dead-drop repositories and telemetry-looking HTTPS exfiltration to `t.m-kosche[.]com`. Socket reported AntV-wave dead-drop repositories using reversed markers such as `niagA oG eW ereH :duluH-iahS` / `niaga og ew ereh :duluh-iahs`, Dune-themed names like `sayyadina-stillsuit-852`, and `results/results-*.json` paths.
- Audit newly added `.claude/`, `.codex/`, and `.vscode/` files, especially `settings.json`, `tasks.json`, `setup.mjs`, copied payload scripts, Claude Code/Codex SessionStart hooks, and VS Code `folderOpen` tasks.
- Search for SafeDep-reported AntV indicators where applicable: payload hash `a68dd1e6a6e35ec3771e1f94fe796f55dfe65a2b94560516ff4ac189390dfa1c`, `@antv/setup` GitHub optional-dependency references to orphan `antvis/G2` commits, `.github/workflows/codeql.yml` workflows named `Run Copilot`, `~/.local/bin/gh-token-monitor.sh`, `~/.local/share/kitty/cat.py`, `kitty-monitor.service`, `com.user.kitty-monitor.plist`, `/var/tmp/.gh_update_state`, and GitHub commits containing `firedalazer` command markers.
- Search GitHub audit logs and repositories for suspicious workflow commits matching reported Mini Shai-Hulud patterns such as branch `chore/add-codeql-static-analysis`, commit message `fix: ci`, and unexpected `.github/workflows/codeql.yml` content labelled `Run Copilot`.
- Hunt for post-theft GitHub activity such as many `git.clone` events, malicious workflow pull requests, workflow-log deletion, or activity from VPN / VPS ASNs not normally used by maintainers.
- Inventory IDE extensions on developer machines; treat a malicious editor extension as an endpoint compromise capable of reading source, secrets, shell history, and authenticated GitHub sessions.

### Package and registry hunting
- Diff newly published package tarballs against prior clean versions.
- Flag new lifecycle hooks, new Bun/runtime downloaders, large minified/obfuscated payload files, or sudden patch releases from unusual automation.
- For Composer/Packagist, flag packages that unexpectedly become `composer-plugin` packages, add `composer-plugin-api`, introduce `post-install-cmd` / `post-update-cmd` execution paths, or move an existing version tag to a new commit.
- Do not trust provenance alone; correlate attestations with clean workflow inputs, clean cache state, and expected release commits.
- Add release-age/cooldown controls for package ingestion when operationally possible.
- For npm maintainers, prefer staged publishing for high-blast-radius packages: CI should stage the tarball and a separate human 2FA approval should release it from a trusted device. Where available, configure trusted-publisher bindings as stage-only so direct CI `npm publish` is rejected.
- In npm consumers, consider setting non-registry install sources to deny-by-default (`--allow-git=none`, `--allow-remote=none`, `--allow-file=none`, `--allow-directory=none`) and only allow exceptions after review; this specifically reduces exposure to GitHub/orphan-commit and remote-tarball dependency paths used in recent supply-chain waves.
- After registry-wide token resets, explicitly inventory and replace automation tokens that stopped working, but do not assume new tokens are safe until affected runners, developer endpoints, caches, and release workflows have been cleaned.

### Containment
- Stop affected workflows, isolate affected hosts, and package publication paths before rotating secrets if persistence or active exfiltration may still be running; Unit 42 specifically warns that some May 11 payloads used token-revocation-triggered destructive behavior while the daemon was active.
- Remove malicious packages and poisoned repo files, then rotate all reachable credentials: GitHub, npm, cloud, Kubernetes, Vault, SSH, Docker, CI, and any app secrets present on the host.
- Invalidate GitHub Actions caches and rebuild release infrastructure from known-clean commits.
- Prefer short-lived scoped credentials, protected environments, least-privilege OIDC subjects, pinned action SHAs, and separate untrusted PR workflows from release workflows.

## Monitoring notes
- High-priority sources for this campaign: StepSecurity, Wiz Research, Socket, Snyk, JFrog Security Research, Akamai Security Research, Unit 42, Microsoft Security Blog, CISA alerts, GitHub Security Advisories, npm advisories/security notices, and maintainer postmortems from affected projects.
- Durable updates worth adding here: new affected package families, new propagation primitives, new persistence paths, new infrastructure/naming patterns, official advisories, or postmortems that explain the initial access path.
- Avoid duplicating every package name from vendor appendices unless it changes the operational picture; link the vendor-maintained affected-package lists instead.

## Related pages
- [TeamPCP](../actors/teampcp.md)
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [Bitwarden / Checkmarx Shai-Hulud Third Coming campaign](bitwarden-checkmarx-shai-hulud-third-coming.md)
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)
- [Trivy → TeamPCP → CanisterWorm timeline](trivy-lite-llm-compromise-timeline.md)
- [Trivy compromise](trivy-compromise.md)
- [CanisterWorm](../tools/canisterworm.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Wiz: https://www.wiz.io/blog/mini-shai-hulud-supply-chain-sap-npm
- Wiz: https://www.wiz.io/blog/durabletask-teampcp-supply-chain-attack
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
- Wiz TeamPCP post-compromise activity: https://www.wiz.io/blog/tracking-teampcp-investigating-post-compromise-attacks-seen-in-the-wild
- Snyk: https://snyk.io/blog/tanstack-npm-packages-compromised/
- Akamai: https://www.akamai.com/blog/security-research/mini-shai-hulud-worm-returns-goes-public
- JFrog: https://research.jfrog.com/post/shai-hulud-here-we-go-again/
- JFrog May 19 follow-up: https://research.jfrog.com/post/shai-hulud-here-we-go-again-may19/
- JFrog Xinference compromise: https://research.jfrog.com/post/xinference-compromise/
- Microsoft: https://www.microsoft.com/en-us/security/blog/2025/12/09/shai-hulud-2-0-guidance-for-detecting-investigating-and-defending-against-the-supply-chain-attack/
- Unit 42: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
- Socket TanStack / OpenSearch / Guardrails AI update: https://socket.dev/blog/tanstack-npm-packages-compromised-mini-shai-hulud-supply-chain-attack
- StepSecurity AntV wave: https://www.stepsecurity.io/blog/shai-hulud-here-we-go-again-mass-npm-supply-chain-attack-hits-the-antv-ecosystem
- StepSecurity durabletask: https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack
- Snyk AntV wave: https://snyk.io/blog/mini-shai-hulud-antv-npm-supply-chain-attack/
- Snyk durabletask: https://snyk.io/blog/durabletask-pypi-supply-chain-attack/
- Grafana Labs: https://grafana.com/blog/grafana-labs-security-update-latest-on-tanstack-npm-supply-chain-ransomware-incident/
- StepSecurity actions-cool: https://www.stepsecurity.io/blog/actions-cool-issues-helper-github-action-compromised-all-tags-point-to-imposter-commit-that-exfiltrates-ci-cd-credentials
- StepSecurity 48-hour timeline: https://www.stepsecurity.io/blog/5-supply-chain-attacks-in-48-hours-why-securing-one-layer-is-not-enough
- StepSecurity Nx Console: https://www.stepsecurity.io/blog/nx-console-vs-code-extension-compromised
- GitHub Blog Nx Console incident note: https://github.blog/security/investigating-unauthorized-access-to-githubs-internal-repositories/
- Socket npm token reset / Mini Shai-Hulud registry response: https://socket.dev/blog/npm-invalidates-tokens-mini-shai-hulud
- Socket AntV package wave: https://socket.dev/blog/antv-packages-compromised
- SafeDep AntV / atool wave analysis: https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/
- Wiz AntV / TeamPCP wave analysis: https://www.wiz.io/blog/mini-shai-hulud-teampcp-hits-antv-supply-chain
- GitHub npm staged publishing / install source controls: https://github.blog/changelog/2026-05-22-staged-publishing-and-new-install-time-controls-for-npm/
- Socket Intercom npm compromise: https://socket.dev/blog/intercom-s-npm-package-compromised-in-supply-chain-attack
- Socket SAP CAP / Cloud MTA compromise: https://socket.dev/blog/sap-cap-npm-packages-supply-chain-attack
- Socket Intercom Packagist compromise: https://socket.dev/blog/mini-shai-hulud-packagist-malicious-intercom-php-package-compromise
- Socket TeamPCP contest reporting: https://socket.dev/blog/teampcp-supply-chain-attack-contest
- OX Security TeamPCP copycat package cluster: https://www.ox.security/blog/new-actors-deploy-shai-hulud-clones-teampcp-copycats-are-here/
- Socket SANDWORM_MODE reporting: https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning
- CISA: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
