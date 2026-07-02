# Trivy → TeamPCP → CanisterWorm: compromise timeline

## Tags
- ops
- operations
- supply-chain
- CI/CD
- GitHub Actions
- npm
- persistence
- worm
- tooling

## Purpose
This page is the canonical timeline for the Trivy → TeamPCP → CanisterWorm chain. It complements the shorter [Trivy compromise](trivy-compromise.md) operation overview by preserving event order, follow-on propagation, and defender lessons across the related activity.

## Timeline

### February 2026: initial runner-memory secret theft
- Public reporting describes an earlier compromise of the Trivy CI pipeline.
- Attackers used **GitHub Actions runner memory dumping** to exfiltrate secrets.
- The incident set up the later March activity by exposing highly privileged credentials.

### Early March 2026: retained access and staging
- Reporting indicates the attacker retained access after incomplete containment.
- A service account / org-scoped token path appears to have enabled later release and workflow abuse.
- The attacker staged impersonated commits and workflow changes before the main release event.

### March 19, 2026: poisoned Trivy release and GitHub Actions compromise
- Poisoned **v0.69.4** Trivy releases were published.
- Related GitHub Actions tags were force-updated to malicious commits.
- The payload stole runner secrets and used fallback exfiltration paths.
- Public reporting ties the campaign to **TeamPCP**.
- StepSecurity's July 2026 retrospective identifies the second Trivy compromise as **CVE-2026-33634** and says **76 of 77** `aquasecurity/trivy-action` version tags were injected with the credential stealer.
- The same retrospective puts the compromise timestamp at **March 19, 2026 17:43 UTC** for incident-response scoping.

### March 20, 2026: NPM worming / CanisterWorm
- The same campaign expanded into the npm ecosystem.
- The worm used stolen npm publish tokens to mass-publish malicious package updates.
- A persistent Python backdoor and a systemd user service provided Linux persistence.
- An ICP canister served as a dead-drop C2 for payload rotation.

### March 22, 2026 and beyond: continued iteration
- Reporting indicates the group continued evolving payloads and infrastructure.
- The campaign added more package compromise and additional payload variants.
- The group maintained the ability to rotate binaries without changing the implant on victim hosts.

## Operational chain
1. **Secret extraction** from CI runner memory
2. **Credential retention** / reuse after incomplete cleanup
3. **Impersonated commits** and **tag force-pushes**
4. **Malicious release publication** across CI and registries
5. **Follow-on npm worming** via stolen publish tokens
6. **Persistence + remote payload rotation** on developer hosts

## July 2026 StepSecurity retrospective
StepSecurity's July 2 defender retrospective adds more concrete CI/CD detection pivots for the Trivy wave and the later Checkmarx KICS action compromise:

- The Trivy action compromise used **imposter commits**: tags resolved to commits reachable by SHA in GitHub's repository object storage but not present on a normal branch of the source repository.
- The malware attempted to read secrets from `/proc/pid/mem` for the GitHub Actions `Runner.Worker` process, a behavior that should be rare enough to alert or terminate in CI runners.
- Exfiltration attempted to POST to the typosquatted domain `scan.aquasecurtiy[.]org`, which StepSecurity says resolved to `45.148.10[.]212`.
- The KICS action compromise followed the same broad playbook, reinforcing that action-tag integrity, branch ancestry checks, and runtime network/process controls should be treated as general CI/CD supply-chain detections rather than Trivy-only cleanup.
- For exposure scoping, defenders should enumerate every `aquasecurity/trivy-action` reference, distinguish mutable tags from full commit SHAs, and review runs during the March 19 compromise window.

## Tooling
### CI / release abuse
- GitHub Actions
- release tag force-pushes
- workflow file tampering
- org-scoped token abuse

### Malware / propagation
- Bash / shell postinstall loader
- Python backdoor
- systemd user units
- npm token harvesting
- publish automation
- ICP canister dead-drop C2

## Key defender lessons
- Treat **CI runner secrets** as instantly sensitive if a pipeline is compromised.
- Pinning to tags is insufficient if tags can be force-updated.
- Look for **release-history anomalies**: unexpected patch releases, deleted tags, and rapid tag rewrites.
- Hunt for **user-level persistence** on developer workstations after package installs.
- Rotate **all** exposed secrets, not just the obvious ones.

## Sources
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
- Socket: https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise
- Boost Security: https://labs.boostsecurity.io/articles/20-days-later-trivy-compromise-act-ii/
- Aikido: https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise
- StepSecurity: https://www.stepsecurity.io/blog/10-layers-deep-how-stepsecurity-stops-teampcps-trivy-supply-chain-attack-on-github-actions
