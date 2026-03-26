# TeamPCP

## Summary
TeamPCP is a supply-chain focused group tracked publicly in connection with multiple operations in 2026, including the **Trivy compromise** and the follow-on **CanisterWorm** NPM campaign. The group demonstrates fast operational follow-through: compromise one upstream trust boundary, steal publish credentials, then weaponize them to mass-push malicious packages across entire package scopes.

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

## Named people
Public reporting commonly attributes activity to the **TeamPCP** group or persona rather than naming individual humans. I do **not** see a reliable public source for a specific person behind TeamPCP in the sources used here, so this material belongs under a group page rather than a people page.

## Associated operations
- [Trivy compromise](../ops/trivy-compromise.md)
- [LiteLLM compromise](../ops/litellm-compromise.md)
- [CanisterWorm](../tools/canisterworm.md)

### Operational chain summary
- **Initial trust-boundary break:** compromised Trivy release and related GitHub Actions enabled credential theft.
- **Release abuse:** the attacker leveraged access to move laterally through release/workflow infrastructure and steal additional secrets.
- **NPM-scale propagation:** stolen publish tokens were used to enumerate packages and push malicious patch releases.
- **Persistence:** Linux developer systems were backdoored with a user-level systemd service.
- **C2 rotation:** an ICP canister served as a dead-drop URL source that could be updated remotely.

## Defender signals
- Moved or force-pushed GitHub Actions tags/refs
- Newly published packages with small patch bumps and preserved READMEs
- `systemd --user` persistence on developer workstations
- Odd package names / masquerading around PostgreSQL-like artifacts
- ICP canister / dead-drop style C2 URLs
- Large-scale package publication shortly after token theft

## Notes
This page is intended as a durable group profile based on public reporting. Prefer primary-source reports and investigative writeups over social commentary.

## Sources
- Aikido: https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
- r/netsec discussion: https://www.reddit.com/r/netsec/comments/1s3kjhf/teampcp_deploys_canisterworm_on_npm_following_trivy_compromise/
- r/netsec discussion (LiteLLM-related supply chain): https://www.reddit.com/r/netsec/comments/1s2n2bo/how_a_poisoned_security_scanner_became_the_key_to_backdooring_litellm/
