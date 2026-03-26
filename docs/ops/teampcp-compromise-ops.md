# TeamPCP compromise operations

## Overview
This page focuses on the **operational chain** behind TeamPCP’s supply-chain activity: how one compromise led to another, which tooling enabled the campaign, and how the actor turned initial access into repeated downstream publication and persistence.

## Tags
- ops
- operations
- tooling
- supply-chain
- CI/CD
- npm
- GitHub Actions
- persistence
- worm

## Sequence of operations

### 1) Initial trust-boundary break: Trivy compromise
- Public reporting ties the campaign to a compromised **Trivy** release and related GitHub Actions.
- The attacker used the compromise to steal credentials and interact with trusted automation paths.
- Actions and release tags were abused to make malicious artifacts look legitimate.

### 2) Follow-on release abuse and credential theft
- The attacker leveraged access to move laterally through release and workflow infrastructure.
- Stolen secrets included developer and CI credentials.
- Exfiltration used both direct network C2 and fallback paths.

### 3) NPM-scale propagation: CanisterWorm
- The campaign then expanded into the npm ecosystem.
- Stolen publish tokens were used to enumerate publishable packages and push malicious patch releases.
- The worm preserved READMEs and used ordinary-looking patch bumps to blend in.

### 4) Persistence on developer systems
- For Linux developer machines, the payload wrote a **user-level systemd service**.
- That service was configured to restart automatically and survive reboots.
- Payload execution stayed quiet and delayed to reduce immediate detection.

### 5) C2 and payload rotation
- The implant used an **ICP canister dead-drop** to fetch a binary URL.
- That meant the attacker could rotate payloads remotely without touching the infected host.
- The canister’s output could be switched between dormant and active payloads.

## Tooling
### CI/CD and release tooling abuse
- GitHub Actions workflows
- GitHub release / tag manipulation
- npm tokens and registry publishing
- patch-version automation

### Malware components
- Node.js postinstall loader
- Python second-stage backdoor
- systemd user units
- canister-based dead-drop C2
- typosquatted / rotating infrastructure

### Operational tradecraft
- README preservation
- PostgreSQL-themed masquerading (`pgmon`, `pglog`)
- sandbox delay and quiet try/catch wrappers
- multi-step payload chain with fallback delivery

## Team structure / dynamics
The public reporting suggests a **small, coordinated team** with multiple roles:
- **access operators**: break into CI/release trust boundaries
- **package operators**: convert token access into broad package compromise
- **malware operators**: maintain the worm/backdoor and rotate payloads
- **infrastructure operators**: manage canister / exfil / hosting paths

## Motivation
Likely priorities based on observable behavior:
- **credential theft**
- **access expansion**
- **blast-radius maximization**
- **repeatable monetization or resale potential**

## Defender implications
- Treat release and package publishing systems as high-value targets
- Pin actions and critical build dependencies to immutable refs
- Hunt for automated patch releases with preserved READMEs
- Rotate npm / GitHub tokens after any suspected trust-boundary compromise
- Watch for user-level persistence on developer machines

## Sources
- Aikido: https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
