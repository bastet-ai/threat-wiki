# actions-cool GitHub Actions tag compromise

## Summary
On May 19, 2026, StepSecurity reported that the GitHub Actions repositories `actions-cool/issues-helper` and `actions-cool/maintain-one-comment` were compromised by tag retargeting. Every existing release tag in both repositories was moved to an imposter commit outside the normal branch history, so workflows that referenced version tags would fetch malicious code on the next run.

The malicious action behavior overlaps with the broader Mini Shai-Hulud / TeamPCP supply-chain cluster: it downloaded Bun, read the GitHub Actions `Runner.Worker` process memory to scrape decrypted workflow secrets, and exfiltrated to `t.m-kosche[.]com`. Only workflows pinned to a previously verified full commit SHA were outside the tag-retargeting blast radius.

## Tags
- ops
- operations
- supply-chain
- GitHub Actions
- CI/CD
- tag tampering
- credential-theft
- Runner.Worker
- Bun
- TeamPCP

## Why this matters
- Version-tag pinning (`@v1`, `@v3`, etc.) is not enough when a maintainer account or repository can move tags after publication.
- The attack reaches CI/CD secrets at runtime rather than relying on static source-code exposure.
- `Runner.Worker` memory scraping bypasses normal log masking and can recover decrypted secrets already loaded into the runner process.
- The same infrastructure (`t.m-kosche[.]com`) and Bun-based runner-memory theft pattern appears across adjacent Mini Shai-Hulud reporting, making GitHub Actions tag integrity part of the same supply-chain watch surface.

## Reported chain
1. An attacker gained the ability to update tags in `actions-cool/issues-helper` and `actions-cool/maintain-one-comment`.
2. Existing tags were repointed to imposter commits not reachable from normal repository branch history.
3. Workflows referencing the actions by tag pulled the malicious commit on their next run.
4. The payload downloaded Bun, executed JavaScript, invoked local tooling such as `gh auth token`, and used Python to read `/proc/.../mem` for the `Runner.Worker` process.
5. Extracted secrets were sent to attacker-controlled infrastructure at `t.m-kosche[.]com`.

## Defender heuristics
- Search all workflows for `actions-cool/issues-helper` and `actions-cool/maintain-one-comment`; treat tag-pinned references as exposed unless pinned to a known-good full SHA.
- Review runs after the suspected tag movement for unexpected Bun downloads, `python3` reading `/proc/*/mem`, `gh auth token` execution, or outbound traffic to `t.m-kosche[.]com`.
- Rotate GitHub, cloud, package-registry, deployment, and application secrets present in affected workflow environments after disabling impacted workflows.
- Prefer full commit SHA pinning for third-party actions and monitor for tag movement, orphan/dangling commits, and release tags outside expected branch ancestry.
- Add egress controls and runtime process telemetry to GitHub-hosted or self-hosted runners; static workflow review alone will not catch memory-scraping payloads at execution time.

## Attribution notes
- StepSecurity's reporting connects the same infrastructure and runner-memory theft motifs to the active Mini Shai-Hulud / TeamPCP ecosystem.
- Keep direct attribution caveated: this page records public infrastructure and technique overlap, not an independent actor determination.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity actions-cool report: [https://www.stepsecurity.io/blog/actions-cool-issues-helper-github-action-compromised-all-tags-point-to-imposter-commit-that-exfiltrates-ci-cd-credentials](https://www.stepsecurity.io/blog/actions-cool-issues-helper-github-action-compromised-all-tags-point-to-imposter-commit-that-exfiltrates-ci-cd-credentials)
- StepSecurity 48-hour supply-chain timeline: [https://www.stepsecurity.io/blog/5-supply-chain-attacks-in-48-hours-why-securing-one-layer-is-not-enough](https://www.stepsecurity.io/blog/5-supply-chain-attacks-in-48-hours-why-securing-one-layer-is-not-enough)
