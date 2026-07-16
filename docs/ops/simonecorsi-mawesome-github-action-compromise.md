# simonecorsi/mawesome GitHub Action compromise

## Summary
StepSecurity reported that on June 24, 2026 an attacker compromised the `simonecorsi/mawesome` GitHub repository, force-pushed malicious commits, and repointed several version tags to attacker-controlled code. Workflows that resolved those tags after the tag movement executed the attacker's code inside GitHub Actions runners.

StepSecurity explicitly compares the method to the same-day [`codfish/semantic-release-action` compromise](codfish-semantic-release-action-tag-compromise.md): repository compromise, force-pushed malicious commits, and mutable version tags moved to the malicious commit. The public writeup is still marked as a developing story and does not yet publish payload internals, exfiltration infrastructure, a malicious commit hash, or a named actor attribution.

A live GitHub API check during this wiki update showed the repository `pushed_at` timestamp as `2026-06-25T00:35:56Z` and current tag refs resolving to ordinary-looking release commits such as `v2.2.0` / `v2` at `e339407b8e34dc1540290d1d310bccafbc6028ca`, `v2.1.0` at `6e26314c306ed5ea744eb90ebc6f3f70298abcb5`, and `v2.0.0` at `7a59a7d02b1fdf6432ea9467b8e31357217288f7`. Treat those current refs only as a point-in-time sanity check; historical workflow runs may still have fetched malicious tag targets during the compromise window.

## Tags
- ops
- operations
- supply-chain
- GitHub Actions
- CI/CD
- tag tampering
- mutable tags
- credential-theft
- release automation
- mawesome

## Why this matters
- `simonecorsi/mawesome` is a third-party GitHub Action, so consumers often reference it from privileged CI/CD workflows rather than reviewing and vendoring the code.
- Mutable Git tags create an exposure window even when maintainers later restore the tags. Current tag state does not prove that earlier workflow runs were clean.
- The incident landed hours after StepSecurity's `codfish/semantic-release-action` report, making GitHub Actions tag integrity a high-priority watch surface for the current supply-chain wave.
- The public report is intentionally sparse while analysis continues; defenders should preserve workflow logs, resolved action SHAs, runner telemetry, and network records before routine retention windows expire.

## Reported chain
1. An attacker gained write capability over `simonecorsi/mawesome`.
2. On June 24, 2026, the attacker force-pushed malicious commits.
3. The attacker repointed several version tags to the malicious commit or commits.
4. GitHub Actions workflows using those tags fetched and executed attacker-controlled action code on their next run.
5. StepSecurity published the incident as a developing story and noted similarity to the `codfish/semantic-release-action` compromise earlier the same day.

## Exposure triage
Search current workflow files, reusable workflows, workflow templates, and historical workflow run metadata for references such as:

- `uses: simonecorsi/mawesome@v2`
- `uses: simonecorsi/mawesome@v2.2.0`
- `uses: simonecorsi/mawesome@v2.1.0`
- `uses: simonecorsi/mawesome@v2.0.0`
- any other `uses: simonecorsi/mawesome@v*` tag reference

Treat a workflow run as exposed if it resolved `simonecorsi/mawesome` by mutable tag after the June 24 compromise began and before the consuming workflow was disabled, pinned to a reviewed full SHA, or rerun against a known-clean action commit.

## Hunt pivots
- GitHub Actions runs that fetched `simonecorsi/mawesome` after June 24, 2026.
- Resolved action SHAs that differ from expected release history or are not reachable from the repository's normal branch ancestry.
- Force-push / tag-update events for `simonecorsi/mawesome` in dependency-review, GitHub audit, or third-party CI inventory telemetry.
- Unexpected extra steps, shell execution, package-manager bootstrap, or network egress inside jobs that historically only used `simonecorsi/mawesome` for its normal action behavior.
- Credential, token, package-registry, cloud, or release-automation activity shortly after affected workflow runs.

## Defender heuristics
- Disable or pin affected workflows before rotating credentials; otherwise a rerun can expose newly rotated secrets.
- Rotate GitHub, cloud, package-registry, release, signing, deployment, and application secrets reachable from impacted jobs.
- Pull workflow run metadata through the GitHub API while logs are still retained, including the resolved action commit SHA when available.
- Prefer full-length commit SHA pinning for third-party actions and pair pins with automated update review.
- Monitor third-party action tags for force updates, orphan commits, commits outside expected branch ancestry, and sudden Docker/composite/JavaScript action-type changes.
- Add runner egress and process telemetry where possible; a compromised action executes after workflow YAML review has already passed.

## Attribution notes
StepSecurity's public post does not attribute the `simonecorsi/mawesome` compromise to Mini Shai-Hulud, TeamPCP, or another named actor. Keep it separate from attributed campaign pages unless a later public source establishes infrastructure, payload, or actor overlap.

## Related pages
- [codfish semantic-release-action tag compromise](codfish-semantic-release-action-tag-compromise.md)
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- [StepSecurity](https://www.stepsecurity.io/blog/simonecorsi-mawesome-github-action-has-been-compromised)
- [GitHub repository](https://github.com/simonecorsi/mawesome)
