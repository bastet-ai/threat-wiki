# Trivy compromise

## Tags
- ops
- operations
- supply-chain
- CI/CD
- GitHub Actions
- release tampering
- credential theft
- developer machines
- persistence
- TeamPCP

## Summary
In March 2026, Aqua Security's Trivy project and related GitHub Actions were compromised. Public reporting ties the incident to **TeamPCP** and describes a combination of credential theft, malicious release tampering, and downstream workflow abuse.

## What happened
- Malicious versions of Trivy and related GitHub Actions were published
- Workflows were modified to steal credentials from GitHub Actions runners and developer environments
- The attacker used a typosquatted domain and fallback infrastructure for exfiltration
- Developer-machine persistence was introduced via a user-level systemd service

## Tooling highlights
- **Trivy binary tampering**
- **GitHub Actions workflow compromise**
- **Systemd user service persistence**
- **Python dropper / backdoor**
- **Cloudflare Tunnel C2**
- **ICP canister dead-drop** for payload rotation
- **Packaging and release automation abuse**

## Why it matters
This incident shows how a single upstream trust break can become a **multi-environment supply-chain event**:
- CI runners
- developer workstations
- package ecosystems
- container registries
- GitHub org credentials

## TeamPCP attribution
Public reporting attributes the campaign to **TeamPCP**. This page intentionally keeps the attribution centered on the operation while linking the actor profile separately.

## Defender takeaways
- Pin actions to full SHAs, not tags
- Treat release pipelines as high-value targets
- Rotate secrets if a build or release system may have been exposed
- Hunt for repository creation / release artifact abuse as a fallback exfil path

## Sources
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
- Aikido: https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise
