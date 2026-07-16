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

## Cordyceps CI/CD composition flaws
Novee Security published a related CI/CD weakness class under the name `Cordyceps` in June 2026. The Hacker News summarized Novee's findings and reported that a scan of roughly 30,000 high-impact repositories found more than 300 fully exploitable cases where untrusted pull-request input could cross into privileged automation.

Reported examples included:

- A Microsoft Azure Sentinel pull-request comment path that Novee said could run attacker code in Microsoft's CI and expose a non-expiring GitHub App key.
- Google's `adk-samples` repository, where a pull request could reportedly execute attacker code in Google's CI and gain authority over a Google Cloud repository.
- Apache Doris, where Novee reported zero-click paths from comments or fork pull requests into attacker code execution and CI credential or write-token exfiltration.
- Cloudflare Workers SDK, where a crafted branch name could reportedly execute arbitrary commands on Cloudflare CI runners.
- Python Software Foundation's Black, where a pull request could reportedly execute attacker code on build systems and steal an automation token usable for pull-request approval.

The durable lesson is not that one GitHub Actions trigger is uniquely unsafe. The risk is composition: untrusted pull-request metadata, comments, branch names, artifacts, deployment fields, or generated workflow state are later consumed by higher-trust jobs with secrets, write tokens, approvals, or cloud credentials.

## GitHub hardening updates
- On 2026-06-18, GitHub published `actions/checkout` v7 with default refusal logic for common pwn-request patterns in `pull_request_target` workflows and in `workflow_run` workflows when the triggering workflow was a pull-request event.
- The protection blocks checkout patterns that resolve to fork pull-request code through a fork `repository`, `refs/pull/<number>/head`, `refs/pull/<number>/merge`, or a fork pull request head / merge commit SHA.
- GitHub says the enforcement will be backported on 2026-07-16 to supported major versions such as floating `actions/checkout@v4`; workflows pinned to a SHA, minor, or patch release need an explicit upgrade path.
- GitHub also introduced workflow execution protections in public preview for enterprises, organizations, and repositories. The control lets administrators define rulesets that allow-list who can trigger workflows and which events are allowed, so approval logic does not live only inside mutable workflow YAML.
- These platform changes do not make deployment metadata safe by default: `deployment_status` consumers should still validate the producer, event type, environment name, and URL before any secret-bearing step.

## Defender heuristics
- Inventory workflows using `on: deployment_status`.
- Inventory workflows using `pull_request_target` or `workflow_run` and confirm they are not checking out unreviewed fork code with privileged tokens or secrets.
- Inventory all privileged workflows that react to pull-request comments, labels, branch names, artifacts, check results, deployment events, or generated files from lower-trust workflows.
- Treat PR comments, branch names, titles, labels, artifact contents, and deployment metadata as attacker-controlled even when a downstream workflow runs on the default branch.
- Prefer floating supported `actions/checkout` majors or planned upgrade automation where that is operationally acceptable; if you pin by SHA for supply-chain control, deliberately roll to a version that includes GitHub's June 2026 pwn-request refusal logic.
- For GitHub Enterprise / organization environments, evaluate workflow execution protections to restrict workflow runs by actor and event outside the workflow file itself.
- Treat `github.event.deployment_status.*` fields as untrusted unless the workflow explicitly verifies the producer and expected environment.
- Do not let comments or labels directly approve, merge, release, or publish without binding the request to a trusted actor, immutable reviewed commit, and expected workflow producer.
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
- Boost Security Labs: [https://labs.boostsecurity.io/articles/deployment_poisoning/](https://labs.boostsecurity.io/articles/deployment_poisoning/)
- GitHub Changelog, safer `pull_request_target` defaults for `actions/checkout`: [https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout)
- GitHub Changelog, workflow execution protections: [https://github.blog/changelog/2026-06-18-control-who-and-what-triggers-github-actions-workflows](https://github.blog/changelog/2026-06-18-control-who-and-what-triggers-github-actions-workflows)
- Novee Security, Cordyceps: [https://novee.security/blog/cordyceps/](https://novee.security/blog/cordyceps/)
- The Hacker News, Cordyceps CI/CD flaws: [https://thehackernews.com/2026/06/cordyceps-cicd-flaws-expose-300-github.html](https://thehackernews.com/2026/06/cordyceps-cicd-flaws-expose-300-github.html)
