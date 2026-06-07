# TeamPCP

## Summary
TeamPCP is a supply-chain focused threat actor tracked publicly in connection with multiple operations in 2026, including the **Trivy compromise**, the follow-on **CanisterWorm** NPM campaign, and Python package compromises such as LiteLLM and Telnyx. StepSecurity also connects TeamPCP to the broader **HackerBot Claw** GitHub Actions exploitation ecosystem.

## Page role
This actor page should stay focused on TeamPCP identity, motivation, tradecraft, and associated operations. Keep detailed timelines and wave-specific indicators on the operation pages, especially [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md), [Bitwarden / Checkmarx Shai-Hulud Third Coming campaign](../ops/bitwarden-checkmarx-shai-hulud-third-coming.md), and [Trivy → TeamPCP → CanisterWorm timeline](../ops/trivy-lite-llm-compromise-timeline.md).

## Tags
- supply-chain
- CI/CD
- npm
- GitHub Actions
- persistence
- worm
- malware
- tooling
- operations

## Primary motivation
- **Access monetization through supply-chain abuse**
- **Credential theft and secondary compromise** of developer environments
- **Rapid blast-radius expansion** by turning one foothold into many downstream victims
- Likely opportunistic but highly operationalized; the behavior looks profit-driven and/or access-driven rather than stealth-only espionage

## Core tooling and infrastructure
### Initial compromise / release abuse
- **GitHub Actions / CI workflow compromise**
- **npm token theft** and package publication abuse
- **Trivy / trivy-action / setup-trivy** as a prior compromise surface
- **HackerBot Claw** as an autonomous exploitation bot in the same ecosystem

### CanisterWorm components
- **Node.js postinstall loader**
- **Python second-stage backdoor**
- **systemd user service persistence** (`Restart=always`, user-level, survives reboots)
- **ICP canister dead-drop C2** for payload rotation
- **Typosquatted / rotating infrastructure** for payload hosting
- **PostgreSQL-themed masquerading**: names like `pgmon`, `pglog`, `.pg_state`

### Collection / exfiltration behavior
- Harvests secrets from developer machines and runners
- Collects SSH, cloud, and K8s secrets
- Uses encrypted exfiltration and fallback delivery paths
- Preserves original READMEs to keep tampered packages looking normal

## Team dynamics / operating style
- Appears to operate like a **small, coordinated crew** rather than a single noisy opportunist
- Strong evidence of **division of labor**:
  - one portion of the operation handled CI/release compromise
  - another portion turned that access into package-level worming
- Uses **rapid iteration**: operations were followed quickly by propagation campaigns, and payloads were updated over time
- Comfort with both **attack tooling** and **operational logistics** (repo access, npm publishing, persistence, and C2 rotation)

## Post-compromise operating style
Wiz CIRT's March 2026 incident-response reporting adds a useful view of what happens after TeamPCP-style supply-chain malware steals credentials. Stolen secrets were validated within hours with TruffleHog-style live API checks, then used for AWS discovery across IAM, EC2, Lambda, RDS, Route 53, S3, ECS, and Secrets Manager.

The same reporting observed GitHub PAT abuse for malicious workflow pull requests, workflow-log deletion, repository cloning at scale, ECS Exec / SSM-based command execution in running containers, and bulk exfiltration from S3, databases, Secrets Manager, and source repositories. Wiz characterized the activity as fast, high-volume, and not especially stealthy, with open-source tools, conspicuous resource names such as `pawn` or `massive-exfil`, Mullvad VPN exit nodes, and InterServer-hosted VPS infrastructure appearing in observed cases.

## Python toolkit / FIRESCALE fallback
Hunt.io's June 2026 TeamPCP toolkit analysis fills in the post-delivery stage behind Mini Shai-Hulud-style npm and PyPI compromises. Hunt describes a 13-file Python second-stage toolkit with a hardcoded primary C2 at `83.142.209[.]194`, broad cloud/developer credential collection, persistence, optional destructive behavior, and multiple fallback exfiltration paths.

The most durable tradecraft is **FIRESCALE**, a GitHub commit-search dead drop. If the primary C2 is unavailable, the malware queries `api.github[.]com/search/commits?q=FIRESCALE`, looks for commit messages containing a keyword plus two base64 segments, decodes a replacement server URL, and verifies the URL with an embedded 4096-bit RSA public key before using it. Because the signed redirect can be posted from any public GitHub account, taking down one repository or one C2 host does not break the fallback path.

Hunt also documents a third exfiltration tier that abuses the victim's own GitHub account. The toolkit collects GitHub CLI credentials and token-bearing environment variables; if direct C2 and FIRESCALE fail, it can create a public repository under the victim account, name it with Slavic folklore terms plus digits, set the description `PUSH UR T3MPRR`, commit the credential harvest as JSON, and later clean up with the same stolen token. This turns normal GitHub API traffic and victim-owned infrastructure into the final delivery path.

Credential collection is broader than package-registry theft. Hunt reports collection of every visible environment variable, SSH keys/config, dotenv files across the home directory, Docker container environment variables, Tailscale and WireGuard configs, Terraform state, AWS credentials across profiles and 19 regions including GovCloud, Kubernetes kubeconfigs and service-account material, Azure CLI / managed-identity / certificate paths, GCP service-account and metadata paths, and Vault tokens/secrets. Collected data is compressed, encrypted with AES-256-GCM, and wrapped with RSA-OAEP.

Hunt attributes the toolkit to TeamPCP through multiple public anchors: the shared `83.142.209[.]194` C2 seen in prior Orca / TanStack reporting, the `voicproducoes` supply-chain operator account linkage, recurring endpoint naming patterns, Russian-locale exit behavior, and Israel / Iran wiper targeting logic. The infrastructure pivots also add a Google Cloud node, `35.192.220[.]222`, that shared an HTTP-header fingerprint with the primary C2 in April 2026, plus certificate-linked leads Hunt treats as less confirmed.

## Extortion ecosystem role
Unit 42's May 27, 2026 cyber-extortion economy analysis adds an important monetization layer for TeamPCP / TGR-CRI-1135. Unit 42 says the actor has moved beyond credential theft and package compromise into data-theft monetization by partnering with extortion and ransomware operators.

The reported partnerships include collaboration with LAPSUS$ Group operators for extortion through a data-leak site and communications on BreachForums around work with Vect ransomware operators. Unit 42 also noted claims from a Vect affiliate, the Rostova Organization, that it was partnering with TGR-CRI-1135, while caveating that Vect was later removed from BreachForums and the operational impact of that removal was unclear.

Two defender implications follow from that update:
- Treat TeamPCP-style supply-chain incidents as potential **data-extortion precursors**, not only package-registry or developer-endpoint events. Cloud, source-code, SaaS, and CI/CD secret exposure can become leverage even when no ransomware is deployed.
- Attribution may become noisier because Unit 42 observed a May 13, 2026 BreachForums announcement claiming an open-source release of Shai-Hulud. Public or leaked tooling can let copycats mimic TeamPCP tradecraft while still feeding the same extortion economy.

## PCPJack adjacency caveat
SentinelOne's May 2026 PCPJack reporting describes a separate cloud credential-theft framework that deliberately removes artifacts associated with TeamPCP / PCPcat-style infections. Hunt.io's June 2026 follow-up recovered PCPJack infrastructure used to convert 230 compromised AWS, Google Cloud, and Azure Linux servers into a Chisel-backed SMTP relay network.

Track PCPJack as **TeamPCP-adjacent but not confirmed TeamPCP-controlled**: public evidence supports overlap and rivalry/removal behavior, not shared operators. The useful defender takeaway for this page is that TeamPCP-linked cloud and supply-chain compromises now sit in an ecosystem where other crimeware operators may evict, reuse, or monetize the same exposed cloud hosts.

## Human actors / personas
Public reporting commonly attributes activity to the **TeamPCP** persona itself rather than naming individual humans. I do **not** see a reliable public name for a specific person behind TeamPCP in the sources used here.

## Associated operations
- [Trivy compromise](../ops/trivy-compromise.md)
- [LiteLLM compromise](../ops/litellm-compromise.md)
- [Telnyx PyPI TeamPCP compromise](../ops/telnyx-pypi-teampcp-compromise.md)
- [Xinference PyPI compromise](../ops/xinference-pypi-compromise.md)
- [HackerBot Claw GitHub Actions exploitation campaign](../ops/hackerbot-claw-github-actions-exploitation-campaign.md)
- [CanisterWorm](../tools/canisterworm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Bitwarden / Checkmarx Shai-Hulud Third Coming campaign](../ops/bitwarden-checkmarx-shai-hulud-third-coming.md)
- [actions-cool GitHub Actions tag compromise](../ops/actions-cool-github-actions-tag-compromise.md) (adjacent action-tag compromise; attribution remains caveated)
- [Nx Console VS Code extension compromise](../ops/nx-console-vscode-extension-compromise.md) (adjacent IDE-extension compromise; attribution remains caveated)
- [PCPJack cloud SMTP relay network](../ops/pcpjack-cloud-smtp-relay-network.md) (TeamPCP-adjacent cloud crimeware; public reporting describes TeamPCP artifact removal, not TeamPCP control)

### Operational chain summary
- **Initial trust-boundary break:** compromised Trivy release and related GitHub Actions enabled credential theft.
- **Release abuse:** the attacker leveraged access to move laterally through release/workflow infrastructure and steal additional secrets.
- **NPM-scale propagation:** stolen publish tokens were used to enumerate packages and push malicious patch releases.
- **Persistence:** Linux developer systems were backdoored with a user-level systemd service.
- **C2 rotation:** an ICP canister served as a dead-drop URL source that could be updated remotely.

### Mini Shai-Hulud expansion
- Unit 42's May 20 threat-landscape update ties the April 22 `@bitwarden/cli@2026.4.0` / Checkmarx distribution-channel compromise to TeamPCP and to the `Shai-Hulud: The Third Coming` string. The same wave reportedly crossed npm, Docker Hub, GitHub Actions, and VS Code extension channels, reinforcing that TeamPCP-style operations target the whole developer trust pipeline rather than a single registry.
- April-May 2026 reporting links TeamPCP-attributed or TeamPCP-linked activity to Mini Shai-Hulud waves affecting SAP, Intercom, TanStack, AntV, Microsoft's `durabletask` PyPI package, Mistral AI, UiPath, OpenSearch, and broader npm/PyPI package ecosystems.
- Unit 42's May 20 update describes two important May-wave escalations: TanStack trusted-publishing abuse produced malicious packages with valid SLSA Build Level 3 provenance, while the AntV wave produced roughly 639 malicious package versions across 323 packages in about one hour.
- Socket's May 21 registry-response coverage says the AntV burst triggered npm to invalidate all granular write tokens that bypass 2FA. That is a useful disruption signal, but TeamPCP/Mini Shai-Hulud operators have also shown paths that do not require long-lived bypass-2FA tokens.
- Key escalation: hijacked legitimate release workflows can produce malicious npm packages with valid provenance/SLSA attestations, so provenance must be paired with workflow/cache integrity checks.
- Later reporting expands the watch area beyond package registries into GitHub Actions tag integrity, developer endpoints, and IDE extensions: retargeted action tags can expose CI/CD secrets, while poisoned VS Code extensions can become the path from supply-chain compromise to source-code theft. GitHub's May 20 incident note confirmed a poisoned Nx Console extension was involved in employee-device compromise and GitHub-internal repository exfiltration; StepSecurity's May 21 technical update assesses TeamPCP as responsible for that GitHub breach while GitHub's own note did not publicly name the actor.
- Socket reported that TeamPCP and BreachForums promoted a Shai-Hulud supply-chain attack contest with a small Monero prize for the biggest package compromise. Treat this as a copycat/recruitment signal: it incentivizes broad package compromise by download count and may increase noisy attempts by lower-tier actors using leaked/open Shai-Hulud tooling.
- Socket separately tracks `SANDWORM_MODE` as a Shai-Hulud-like npm worm rather than a confirmed TeamPCP operation; use it as lineage/copycat context unless stronger attribution emerges.
- JFrog's May 19 AntV follow-up adds two durable TeamPCP/Mini Shai-Hulud escalations to monitor: optional-dependency delivery from fork-resolvable GitHub commits that leaves the npm tarball itself looking clean, and post-compromise persistence through AI-tool hooks (`~/.claude/`, `~/.codex/`), VS Code `folderOpen` tasks, and GitHub commit-search C2 (`kitty-monitor`).
- Boost Security's LiteLLM writeup reinforces the Trivy-to-second-order-victim model but keeps causality appropriately caveated: the poisoned Trivy APT/Homebrew/action paths they could inspect did not explain BerriAI, leaving GitHub Release binaries, Docker images, force-pushed action tags, or another unobserved credential path as live hypotheses. The same report adds the `litellm_init.pth` Python-startup execution pattern, `models.litellm.cloud` exfiltration, and GitHub repository exposure/destruction behavior to TeamPCP hunting.
- OX Security's Telnyx writeup adds a same-week PyPI follow-on pattern: malicious `telnyx` releases `4.87.1` and `4.87.2` reportedly used compromised publishing access, added obfuscated logic to `_client.py`, downloaded an XOR-obfuscated WAV-like payload as `temp.wav`, and reused LiteLLM-style cloud/developer credential theft. Telnyx told OX the compromise was limited to the Python package, not Telnyx service infrastructure.
- JFrog's Xinference writeup adds another TeamPCP-linked / possible-copycat PyPI pattern: legitimate `xinference` versions `2.6.0`-`2.6.2` ran import-time code from `xinference/__init__.py`, spawned detached Python execution, collected cloud/Kubernetes/developer secrets, and exfiltrated `love.tar.gz` to `whereisitat[.]lucyatemysuperbox[.]space`. JFrog noted TeamPCP denied responsibility, so track it as reported TeamPCP-family activity with attribution caveats.
- Socket's Intercom reporting adds a cross-ecosystem pivot pattern to watch: a compromised PyPI dependency (`lightning`, pulled locally through `pyannote-audio`) was linked to Intercom npm compromise, followed by a malicious Packagist artifact (`intercom/intercom-php@5.0.2`) that abused Composer plugin install/update execution and mutable tag metadata. Treat future TeamPCP/Mini Shai-Hulud triage as multi-registry by default, especially when one compromised developer account or endpoint has GitHub organization write access.
- Socket's SAP CAP / Cloud MTA analysis reinforces that TeamPCP-linked Mini Shai-Hulud waves target high-blast-radius enterprise developer ecosystems, not just generic npm packages: SAP CAP packages added Bun runtime bootstrappers, large obfuscated payloads, developer/CI credential harvesting, and GitHub Actions runner-memory scraping in artifacts with hundreds of thousands of combined weekly downloads.
- Socket's May 12-May 19 Mini Shai-Hulud updates add two TeamPCP-family watch points: AI/security packages can be compromised through import-time PyPI loaders (`guardrails-ai@0.10.1` downloading `transformers.pyz` from `git-tanstack[.]com`), and high-volume maintainer-account compromise can now be measured in hundreds of versions per hour (Socket counted the AntV wave at 639 versions across 323 packages, with 1,055 versions across 502 packages campaign-wide at that point).
- Unit 42's May 27 cyber-extortion economy analysis adds that TGR-CRI-1135 / TeamPCP has collaborated with LAPSUS$ Group operators for data-leak-site extortion and with Vect ransomware operators or affiliates in BreachForums-advertised arrangements. That makes stolen developer, cloud, SaaS, and repository data a direct extortion risk even without encryptor deployment.
- The same Unit 42 update reported a May 13 BreachForums post announcing an open-source Shai-Hulud release, increasing the chance of copycat operations that reuse TeamPCP/Mini Shai-Hulud methods without clean actor attribution.
- Wiz and StepSecurity's June 1, 2026 Miasma reporting adds a concrete example of this attribution problem: compromised `@redhat-cloud-services` npm packages used Mini Shai-Hulud-derived code and TeamPCP-like cloud/GitHub credential theft, but Wiz explicitly cautioned that the public Mini Shai-Hulud release means a copycat actor could be reusing the tooling. Keep Miasma on the Mini Shai-Hulud operation page unless stronger public attribution emerges.

## Defender signals
- Moved or force-pushed GitHub Actions tags/refs, especially tags pointing to commits outside normal branch ancestry
- Newly published packages with small patch bumps and preserved READMEs
- `systemd --user` persistence on developer workstations
- Odd package names / masquerading around PostgreSQL-like artifacts
- ICP canister / dead-drop style C2 URLs
- Large-scale package publication shortly after token theft
- Valid provenance/SLSA attestations on malicious packages when a legitimate trusted-publishing workflow was poisoned before publication
- npm automation-token churn after registry-wide resets, especially newly minted bypass-2FA write tokens stored back into still-contaminated CI systems
- Token-revocation-triggered destructive behavior on affected developer hosts in variants that keep polling GitHub with stolen credentials
- Copycat contest/recruitment chatter that rewards high-download package compromise, especially when paired with public Shai-Hulud tooling leaks
- New optional dependencies pointing at GitHub commits outside normal branch ancestry, especially setup-themed names such as `@antv/setup` or `@sap/setup`
- Claude Code/Codex SessionStart hooks, VS Code `folderOpen` tasks, and GitHub commit-search C2 markers such as `firedalazer`, `thebeautifulsnadsoftime`, or `thebeautifulmarchoftime`
- Composer packages that unexpectedly add `composer-plugin-api`, plugin classes, or install/update hooks, especially when an existing Packagist version tag moves to a new commit
- PyPI packages that add Linux-only import-time downloaders for `.pyz` payloads, especially AI/security packages and hosts resembling legitimate project infrastructure such as `git-tanstack[.]com`
- Leak-site, BreachForums, or victim-communication references that appear after TeamPCP-linked credential theft, especially claims involving LAPSUS$ Group, Vect, Rostova Organization, or copycat Shai-Hulud operators
- Cloud-host compromise where tools remove TeamPCP / PCPcat-named artifacts before installing unrelated credential-theft, Sliver, Chisel, or SMTP relay components; keep this as adjacency/rivalry evidence, not attribution by itself
- TeamPCP Python-toolkit fallback behavior: GitHub commit search for `FIRESCALE`, unexpected GitHub repository creation from developer accounts with description `PUSH UR T3MPRR`, Slavic-folklore repository names, and outbound attempts to `83.142.209[.]194` or fingerprint-related backup infrastructure such as `35.192.220[.]222`
- Broad credential sweeps that read all environment variables, SSH material, Docker container env vars, Terraform state, Tailscale/WireGuard configs, Vault stores, AWS GovCloud regions, Azure Key Vault, GCP metadata/service-account flows, and Kubernetes credentials from the same short-lived Python process tree

## Notes
This page is intended as a durable profile based on public reporting. Prefer primary-source reports and investigative writeups over social commentary.

## Sources
- [Aikido](https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise)
- [Wiz](https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack)
- [Wiz TeamPCP post-compromise activity](https://www.wiz.io/blog/tracking-teampcp-investigating-post-compromise-attacks-seen-in-the-wild)
- [Wiz Mini Shai-Hulud SAP npm coverage](https://www.wiz.io/blog/mini-shai-hulud-supply-chain-sap-npm)
- [Snyk TanStack Mini Shai-Hulud coverage](https://snyk.io/blog/tanstack-npm-packages-compromised/)
- [Akamai Mini Shai-Hulud analysis](https://www.akamai.com/blog/security-research/mini-shai-hulud-worm-returns-goes-public)
- [StepSecurity](https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation)
- [StepSecurity AntV Mini Shai-Hulud coverage](https://www.stepsecurity.io/blog/shai-hulud-here-we-go-again-mass-npm-supply-chain-attack-hits-the-antv-ecosystem)
- [StepSecurity durabletask coverage](https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack)
- [StepSecurity actions-cool GitHub Actions coverage](https://www.stepsecurity.io/blog/actions-cool-issues-helper-github-action-compromised-all-tags-point-to-imposter-commit-that-exfiltrates-ci-cd-credentials)
- [StepSecurity Nx Console coverage](https://www.stepsecurity.io/blog/nx-console-vs-code-extension-compromised)
- [GitHub Nx Console incident note](https://github.blog/security/investigating-unauthorized-access-to-githubs-internal-repositories/)
- [Socket npm token reset / Mini Shai-Hulud registry response](https://socket.dev/blog/npm-invalidates-tokens-mini-shai-hulud)
- [Socket TeamPCP supply-chain attack contest reporting](https://socket.dev/blog/teampcp-supply-chain-attack-contest)
- [Socket SANDWORM_MODE reporting](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning)
- [Grafana Labs TanStack incident update](https://grafana.com/blog/grafana-labs-security-update-latest-on-tanstack-npm-supply-chain-ransomware-incident/)
- [Unit 42 npm threat landscape May 20 update](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)
- [JFrog May 19 Shai-Hulud follow-up](https://research.jfrog.com/post/shai-hulud-here-we-go-again-may19/)
- [JFrog Xinference PyPI compromise](https://research.jfrog.com/post/xinference-compromise/)
- [Socket Intercom npm compromise](https://socket.dev/blog/intercom-s-npm-package-compromised-in-supply-chain-attack)
- [Socket Intercom Packagist compromise](https://socket.dev/blog/mini-shai-hulud-packagist-malicious-intercom-php-package-compromise)
- [Socket SAP CAP / Cloud MTA compromise](https://socket.dev/blog/sap-cap-npm-packages-supply-chain-attack)
- [Socket TanStack / OpenSearch / Guardrails AI update](https://socket.dev/blog/tanstack-npm-packages-compromised-mini-shai-hulud-supply-chain-attack)
- [Socket AntV Mini Shai-Hulud wave](https://socket.dev/blog/antv-packages-compromised)
- [StepSecurity blog index](https://www.stepsecurity.io/blog)
- [Unit 42 cyber-extortion economy analysis](https://unit42.paloaltonetworks.com/cyber-extortion-economy/)
- [Wiz Miasma / RedHat npm coverage](https://www.wiz.io/blog/miasma-supply-chain-attack-targeting-redhat-npm-packages)
- [StepSecurity RedHat Cloud Services npm coverage](https://www.stepsecurity.io/blog/multiple-redhat-cloud-services-npm-packages-compromised)
- [SentinelOne PCPJack cloud worm reporting](https://www.sentinelone.com/labs/cloud-worm-evicts-teampcp-and-steals-credentials-at-scale/)
- [Hunt.io PCPJack SMTP relay network reporting](https://hunt.io/blog/pcpjack-230-cloud-servers-smtp-proxy-network-sliver-chisel)
- [Hunt.io TeamPCP Python toolkit / FIRESCALE analysis](https://hunt.io/blog/teampcp-python-toolkit-firescale-github-c2-takedown)
- [OX Security Telnyx PyPI compromise](https://www.ox.security/blog/telnyx-malware-teampcp-strikes-again-following-litellm-compromise/)
