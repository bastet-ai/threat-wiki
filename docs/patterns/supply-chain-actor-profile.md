# Supply-chain actor profile pattern

Use this page for actors whose value comes from abusing software distribution, CI/CD, package publishing, or developer trust.

## What to capture
- **Motivation**: credential theft, monetization, access expansion, sabotage, espionage, or blend
- **Tooling**: CI compromise, package manager abuse, malware stage design, persistence, C2, exfil
- **Team structure**: solo operator vs crew vs “operator + loader + infrastructure” split
- **Iteration speed**: how quickly they adapt tooling and replace infrastructure
- **Defender actions**: package pinning, token rotation, workflow SHA pinning, build provenance, runner hygiene

## Examples
- TeamPCP: Trivy compromise → CanisterWorm NPM worming, systemd persistence, ICP dead-drop C2

## Heuristics
- If the actor can turn one package token into many publish rights, assume **blast radius is the objective**.
- If payloads preserve READMEs and version bumps look routine, assume **deception is part of the tradecraft**.
- If infrastructure is rotated remotely, expect **continuous campaign maintenance**, not one-off malware.
