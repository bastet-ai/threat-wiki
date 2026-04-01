# HackerBot Claw

## Summary
HackerBot Claw is an AI-powered GitHub account and autonomous exploitation bot that publicly claimed to be an autonomous security research agent powered by Claude. Public reporting describes it as a bot that systematically scanned public repositories for exploitable GitHub Actions workflows and executed multiple exploitation techniques across major open-source targets.

## Tags
- group
- ai-agent
- tooling
- operations
- GitHub Actions
- CI/CD
- supply-chain

## Relation to TeamPCP
StepSecurity describes HackerBot Claw as being tied to the same supply-chain threat ecosystem as **TeamPCP**. In the public StepSecurity reporting used for this page, TeamPCP is the actor associated with the Trivy compromise and the follow-on CanisterWorm campaign, while HackerBot Claw is the autonomous bot used to exploit GitHub Actions workflows in that broader ecosystem.

## Motivation
- **Autonomous exploitation / research** framing
- Likely **credential theft and access expansion** when the bot succeeded
- Public-facing account branding suggests a blend of **research theater** and **operational exploitation**

## Tooling / tradecraft
- Autonomous GitHub account activity across repositories
- GitHub Actions exploitation via `pull_request_target` and workflow injection patterns
- Payload delivery using `curl | bash`
- Token exfiltration to external receivers
- Branch-name, filename, script, and AI prompt injection techniques
- Rapid iteration across multiple PRs and targets

## Associated operations
- [HackerBot Claw GitHub Actions exploitation campaign](../ops/hackerbot-claw-github-actions-exploitation-campaign.md)
- [Trivy compromise](../ops/trivy-compromise.md)
- [CanisterWorm](../tools/canisterworm.md)

## Defender signals
- Repeated PRs from an account with autonomous / agentic branding
- GitHub Actions jobs that execute untrusted fork code under elevated permissions
- `pull_request_target` workflows that check out attacker-controlled refs
- Any workflow step that shells out with unsanitized branch names, filenames, or PR metadata
- Unexplained outbound calls to attacker-controlled domains during CI

## References
- [StepSecurity](https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation)
- [StepSecurity blog index](https://www.stepsecurity.io/blog)
