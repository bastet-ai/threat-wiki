# GitHub Actions deployment poisoning

## Summary
Deployment poisoning is a CI/CD abuse pattern in which an attacker uses fork pull-request workflows to create or influence GitHub deployment events, then triggers trusted `deployment_status` workflows that were written as if deployment metadata only came from trusted services.

Boost Security Labs published the technique in April 2026 after disclosure to affected vendors. The pattern matters because it crosses a familiar trust boundary: an untrusted pull request can shape deployment names or URLs, while downstream workflows may run on the default branch with repository secrets.

## Tags
- patterns
- supply-chain
- CI/CD
- GitHub Actions
- deployment_status
- pwn-request
- command-injection
- SSRF
- secrets

## Attack shape
- An attacker opens a pull request from a fork.
- A workflow on that pull request references a crafted environment name or environment URL.
- GitHub can create a new environment automatically when a workflow references one that does not already exist.
- A separate workflow listening on `deployment_status` runs in the base repository context and consumes fields such as `github.event.deployment_status.environment` or `environment_url`.
- If those values are interpolated directly into shell commands, the attacker gets command injection; if the URL is used by an end-to-end test tool with secrets, the attacker may receive tokens or API keys through SSRF-like behavior.

## Why this matters
- Deployment events are often mentally grouped with trusted third-party services such as Vercel, Railway, or other preview-deployment systems.
- The producer and consumer sides are different: one workflow or app may create the deployment, while another workflow consumes the status and runs tests with secrets.
- Fixing shell interpolation alone is not enough if attacker-controlled `environment_url` values are still passed into test clients that authenticate to the target.
- The same trust-assumption failure is adjacent to other CI/CD supply-chain patterns: pwn requests, artifact poisoning, cache poisoning, and trusted-publishing abuse.

## Defender heuristics
- Inventory workflows using `on: deployment_status`.
- Treat `github.event.deployment_status.*` fields as untrusted unless the workflow explicitly verifies the producer and expected environment.
- Avoid direct `${{ }}` interpolation inside `run:` blocks; pass values through environment variables and quote/use them carefully.
- Whitelist expected environment names before executing any secret-bearing step.
- Prefer `github.event.deployment_status.target_url` over `environment_url` where it fits the integration; Boost notes `environment_url` is attacker-controllable in this pattern.
- Set default `GITHUB_TOKEN` permissions to read-only or `permissions: {}` and grant narrower permissions per job.
- Require approval for fork pull-request workflows from all external contributors, not only first-time contributors.
- Add protection rules to secret-bearing environments and monitor for unexpected newly created environments.

## Related pages
- [Supply-chain group profile](supply-chain-actor-profile.md)
- [actions-cool GitHub Actions tag compromise](../ops/actions-cool-github-actions-tag-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- Boost Security Labs: https://labs.boostsecurity.io/articles/deployment_poisoning/
