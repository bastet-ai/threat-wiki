# TeamPCP

## Summary
TeamPCP is a supply-chain focused threat actor tracked publicly in connection with multiple operations in 2026, including the **Trivy compromise** and the follow-on **CanisterWorm** NPM campaign. StepSecurity also connects TeamPCP to the broader **HackerBot Claw** GitHub Actions exploitation ecosystem.

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

## Human actors / personas
Public reporting commonly attributes activity to the **TeamPCP** persona itself rather than naming individual humans. I do **not** see a reliable public name for a specific person behind TeamPCP in the sources used here.

## Associated operations
- [Trivy compromise](../ops/trivy-compromise.md)
- [LiteLLM compromise](../ops/litellm-compromise.md)
- [HackerBot Claw GitHub Actions exploitation campaign](../ops/hackerbot-claw-github-actions-exploitation-campaign.md)
- [CanisterWorm](../tools/canisterworm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Nx Console VS Code extension compromise](../ops/nx-console-vscode-extension-compromise.md) (adjacent IDE-extension compromise; attribution remains caveated)

### Operational chain summary
- **Initial trust-boundary break:** compromised Trivy release and related GitHub Actions enabled credential theft.
- **Release abuse:** the attacker leveraged access to move laterally through release/workflow infrastructure and steal additional secrets.
- **NPM-scale propagation:** stolen publish tokens were used to enumerate packages and push malicious patch releases.
- **Persistence:** Linux developer systems were backdoored with a user-level systemd service.
- **C2 rotation:** an ICP canister served as a dead-drop URL source that could be updated remotely.

### Mini Shai-Hulud expansion
- April-May 2026 reporting links TeamPCP-attributed or TeamPCP-linked activity to Mini Shai-Hulud waves affecting SAP, Intercom, TanStack, AntV, Microsoft's `durabletask` PyPI package, Mistral AI, UiPath, OpenSearch, and broader npm/PyPI package ecosystems.
- Key escalation: hijacked legitimate release workflows can produce malicious npm packages with valid provenance/SLSA attestations, so provenance must be paired with workflow/cache integrity checks.
- Later reporting expands the watch area beyond package registries into developer endpoints and IDE extensions: poisoned VS Code extensions can become the path from supply-chain compromise to source-code theft.

## Defender signals
- Moved or force-pushed GitHub Actions tags/refs
- Newly published packages with small patch bumps and preserved READMEs
- `systemd --user` persistence on developer workstations
- Odd package names / masquerading around PostgreSQL-like artifacts
- ICP canister / dead-drop style C2 URLs
- Large-scale package publication shortly after token theft

## Notes
This page is intended as a durable profile based on public reporting. Prefer primary-source reports and investigative writeups over social commentary.

## Sources
- [Aikido](https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise)
- [Wiz](https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack)
- [Wiz Mini Shai-Hulud SAP npm coverage](https://www.wiz.io/blog/mini-shai-hulud-supply-chain-sap-npm)
- [Snyk TanStack Mini Shai-Hulud coverage](https://snyk.io/blog/tanstack-npm-packages-compromised/)
- [Akamai Mini Shai-Hulud analysis](https://www.akamai.com/blog/security-research/mini-shai-hulud-worm-returns-goes-public)
- [StepSecurity](https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation)
- [StepSecurity AntV Mini Shai-Hulud coverage](https://www.stepsecurity.io/blog/shai-hulud-here-we-go-again-mass-npm-supply-chain-attack-hits-the-antv-ecosystem)
- [StepSecurity durabletask coverage](https://www.stepsecurity.io/blog/microsofts-durabletask-pypi-package-compromised-in-supply-chain-attack)
- [StepSecurity Nx Console coverage](https://www.stepsecurity.io/blog/nx-console-vs-code-extension-compromised)
- [Grafana Labs TanStack incident update](https://grafana.com/blog/grafana-labs-security-update-latest-on-tanstack-npm-supply-chain-ransomware-incident/)
- [StepSecurity blog index](https://www.stepsecurity.io/blog)
