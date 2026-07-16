# codfish semantic-release-action tag compromise

## Summary
StepSecurity reported that on June 24, 2026 an attacker compromised the `codfish/semantic-release-action` GitHub repository and force-pushed a malicious commit, `6b9501e1889cc45c91726729610cf69c2442b8c5` (`6b9501e`). StepSecurity says seven existing version tags — `v1.6.1`, `v1.6.2`, `v1.7.0`, `v1.8.0`, `v1.9.0`, `v2.0.0`, and `v2.2.1` — were repointed to that commit at `2026-06-24 15:39:06 UTC`, so downstream workflows using those mutable tags executed attacker-controlled code on their next run.

The payload converted the action from a Docker action to a composite action that installed Bun with `oven-sh/setup-bun@v2` and ran a heavily obfuscated JavaScript payload with `if: always()`. StepSecurity's initial analysis says the payload targeted GitHub Actions OIDC tokens and GitHub personal access tokens, encrypted collected material with AES-128-GCM, and attempted to propagate a backdoor into repositories reachable with stolen credentials.

As of a live GitHub API check during this wiki update, `refs/tags/v2.2.1` resolved to `5792aba0e2180b9b80b77644370a6889d5817456`, so treat the highest-risk exposure as workflow runs that resolved one of the affected tags during the malicious tag window rather than current tag state alone.

## Tags
- ops
- operations
- supply-chain
- GitHub Actions
- CI/CD
- tag tampering
- mutable tags
- credential-theft
- OIDC
- GitHub tokens
- Bun
- semantic-release

## Why this matters
- Release automation actions often run with package-registry, GitHub, and cloud publish credentials; compromising the release action can turn routine release jobs into secret-theft and propagation events.
- The incident repeats the core mutable-tag lesson from prior GitHub Actions compromises: `uses: owner/action@v2` is only as stable as the repository's tag-protection and maintainer-account controls.
- `if: always()` on injected steps means the malicious payload still runs when the legitimate release step fails, reducing the chance that broken release behavior prevents compromise.
- Bun installation is a useful CI hunt pivot: StepSecurity notes the attacker selected Bun partly because many Node.js security controls rely on `--require`-style interception that does not apply to Bun.
- Current clean tag resolution does not clear historical exposure. Review workflow runs in the malicious window, not just present-day repository refs.

## Reported chain
1. The attacker gained the ability to write to `codfish/semantic-release-action` and force-update release tags.
2. At `2026-06-24 15:39:06 UTC`, StepSecurity says the attacker introduced commit `6b9501e1889cc45c91726729610cf69c2442b8c5` and repointed `v1.6.1`, `v1.6.2`, `v1.7.0`, `v1.8.0`, `v1.9.0`, `v2.0.0`, and `v2.2.1` to it.
3. The malicious `action.yml` changed the runner type from Docker to composite.
4. The composite action preserved a semantic-release-looking step, then added `oven-sh/setup-bun@v2` and `bun run ${{ github.action_path }}/index.js`, both guarded with `if: always()`.
5. The injected `index.js` was roughly 512 KB of single-line obfuscated JavaScript.
6. StepSecurity's static analysis identified patterns for GitHub OIDC token theft, GitHub PAT harvesting using known token formats, AES-128-GCM encryption of collected material, and repository backdoor propagation attempts.
7. StepSecurity reported that the exfiltration endpoint remained encoded at publication time and said it would update the post after deeper deobfuscation.

## Exposure triage
Search GitHub Actions workflow history, not only current workflow files:

- `uses: codfish/semantic-release-action@v1.6.1`
- `uses: codfish/semantic-release-action@v1.6.2`
- `uses: codfish/semantic-release-action@v1.7.0`
- `uses: codfish/semantic-release-action@v1.8.0`
- `uses: codfish/semantic-release-action@v1.9.0`
- `uses: codfish/semantic-release-action@v2.0.0`
- `uses: codfish/semantic-release-action@v2.2.1`

Treat runs as exposed if they executed after `2026-06-24 15:39:06 UTC` and before the tag was restored or replaced with a reviewed pinned SHA. Also review reusable workflows, composite actions, release templates, and organization-wide workflow generators that may reference the action indirectly.

## Hunt pivots
- Unexpected `oven-sh/setup-bun@v2` execution in release workflows that previously used only `codfish/semantic-release-action`.
- `bun run` execution from a GitHub action path, especially `bun run ${{ github.action_path }}/index.js`.
- A sudden Docker-to-composite diff in `codfish/semantic-release-action/action.yml`.
- Commit `6b9501e1889cc45c91726729610cf69c2442b8c5` / short SHA `6b9501e` resolving under older release tags.
- Large obfuscated single-line JavaScript near `index.js` in the action checkout.
- GitHub OIDC token minting, `ACTIONS_ID_TOKEN_REQUEST_URL` / `ACTIONS_ID_TOKEN_REQUEST_TOKEN` access, or unusual calls to cloud federation endpoints from release jobs.
- GitHub PAT-shaped strings found in runner memory, environment snapshots, action debug output, or exfiltration telemetry.
- New branches, workflow files, release changes, or commits made by automation identities shortly after an affected run.

## Defender heuristics
- Disable or pin affected release workflows before rotating credentials; otherwise a rerun can re-steal fresh secrets.
- Rotate GitHub, npm, container-registry, cloud, package-signing, and release-automation credentials that were reachable from affected runners.
- For GitHub Enterprise environments, GitHub's June 24, 2026 changelog adds incident-response options that can revoke SSO authorizations for personal access tokens, SSH keys, and OAuth tokens across an enterprise or organization, and can delete user tokens / SSH keys for Enterprise Managed Users. Use those controls as bulk containment aids when release-runner compromise may have exposed user credentials.
- Review GitHub audit logs for workflow runs, OIDC token requests, repository writes, tag updates, branch creations, package publishes, and secret access after the affected workflow ran.
- Prefer full-length commit SHA pinning for third-party GitHub Actions, paired with automation that periodically reviews and advances pins.
- Enable tag protection / rulesets for maintained actions and monitor release tags for forced updates, orphan commits, or commits outside expected branch ancestry.
- Treat action code as executable supply-chain input: diff the resolved action commit during incident response, not only the consuming repository's workflow YAML.
- Consider egress restrictions and runtime telemetry for release runners; release jobs often need broad credentials but rarely need arbitrary outbound destinations.

## Attribution notes
StepSecurity's public post does not attribute the `codfish/semantic-release-action` compromise to a named actor. Keep it separate from Mini Shai-Hulud / TeamPCP unless a later public source establishes overlap. The technique overlaps with earlier GitHub Actions tag-retargeting incidents, but overlap is not attribution.

## Related pages
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [GitHub Actions OIDC subject-claim collisions](../patterns/github-actions-oidc-subject-claim-collisions.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity: <https://www.stepsecurity.io/blog/supply-chain-compromise-codfish-semantic-release-action>
- GitHub repository: <https://github.com/codfish/semantic-release-action>
- GitHub Changelog: <https://github.blog/changelog/2026-06-24-self-service-credential-revocation-for-incident-response>
