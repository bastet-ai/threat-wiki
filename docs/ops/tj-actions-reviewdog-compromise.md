# tj-actions and reviewdog compromise

## Tags
- ops
- operations
- supply-chain
- GitHub Actions
- CI/CD
- secret exposure
- tag tampering
- Coinbase
- reviewdog
- tj-actions

## Summary
In March 2025, attackers compromised the third-party GitHub Actions [`reviewdog/action-setup@v1`](https://github.com/advisories/ghsa-qmg3-hpqr-gqvc) and [`tj-actions/changed-files`](https://github.com/tj-actions/changed-files/issues/2463), turning routine CI workflows into a credential-exposure path. Public reporting from [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised), [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/), and [CISA](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) shows a chained operation: first abuse access around `reviewdog`, then use that access to poison `tj-actions`, and finally expose secrets from downstream workflow runs by forcing tags to point at malicious code.

This page treats the incident as a single operation because the public evidence ties the two compromises together. Public sources do **not** clearly support a named group or public human identity for this campaign, so this material belongs under `Ops`, not `Groups` or `People`.

## Timeline
- **November 28, 2024:** [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) reports that a SpotBugs maintainer PAT was added to `spotbugs/sonar-findbugs`, creating an access path later abused in the campaign.
- **December 6, 2024:** [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) says the attacker leaked that SpotBugs maintainer PAT from `spotbugs/sonar-findbugs`.
- **March 11, 2025, 18:42-20:31 UTC:** [`reviewdog/action-setup@v1`](https://github.com/advisories/ghsa-qmg3-hpqr-gqvc) was compromised; both GitHub's advisory and the [reviewdog maintainer notice](https://github.com/reviewdog/reviewdog/issues/2079) describe this as the confirmed compromise window.
- **March 12-14, 2025:** [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) observed attacker preparation around forks tied to `coinbase/agentkit`, `coinbase/onchainkit`, `coinbase/x402`, and `tj-actions/changed-files`.
- **March 14, 2025, around 16:00 UTC:** [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised) says the `tj-actions/changed-files` compromise was active by this point and exposed secrets in workflow logs.
- **March 14, 2025:** A public [GitHub issue](https://github.com/tj-actions/changed-files/issues/2463) documented that multiple `tj-actions/changed-files` tags had been retroactively moved to malicious code.
- **March 15, 2025, 14:00 UTC:** [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised) reports that GitHub removed the compromised `tj-actions/changed-files` Action.
- **March 15, 2025, 22:00 UTC:** [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised) reports the repository was restored after the malicious code was removed.
- **March 18-26, 2025:** [CISA](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) published and revised its alert for the linked `tj-actions` and `reviewdog` compromises, and later added both CVEs to the KEV catalog.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here:

### reviewdog
- GitHub's [advisory](https://github.com/advisories/ghsa-qmg3-hpqr-gqvc) says `reviewdog/action-setup@v1` was compromised on March 11, 2025, between 18:42 and 20:31 UTC.
- The [reviewdog maintainer](https://github.com/reviewdog/reviewdog/issues/2079) publicly stated that automatically invited contributors had write access to `reviewdog/action-*` repositories, creating a broader attack surface than intended.
- The maintainer disabled the automated inviter flow, removed broad write access, pinned internal dependencies to commit SHAs, and rotated or deleted relevant PATs.

### tj-actions
- [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised) reported that `tj-actions/changed-files` was used in more than 23,000 repositories when it was compromised.
- Public reporting describes attackers retroactively moving many version tags to a malicious commit so downstream workflows would execute the payload even when users thought they were pinned to a stable tag.
- [CISA's March 26, 2025 alert revision](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) says the compromise was patched in `v46.0.1`.

### Coinbase and SpotBugs
- [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) describes the campaign as initially targeting Coinbase-managed open-source repositories, especially `coinbase/agentkit`, before expanding to wider `tj-actions` consumers.
- [Unit 42](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) also traces the earliest known access path through `spotbugs/sonar-findbugs` and `spotbugs/spotbugs`, where maintainer PAT exposure enabled later movement into `reviewdog`.

## Operational chain
1. A workflow in `spotbugs/sonar-findbugs` was abused to leak a maintainer PAT, according to Unit 42.
2. The attacker used that access to reach `spotbugs/spotbugs`, trigger another malicious workflow run, and leak a PAT belonging to a maintainer with access to `reviewdog/action-setup`.
3. With that PAT, the attacker repointed the `reviewdog/action-setup@v1` tag to malicious code stored in a fork.
4. `tj-actions/changed-files` depended on `tj-actions/eslint-changed-files`, which in turn depended on `reviewdog/action-setup`; when that CI path ran, it exposed a write-capable token for `tj-actions/changed-files`.
5. Unit 42 says the attacker first used the poisoned `tj-actions` path against `coinbase/agentkit`, then force-moved more `tj-actions/changed-files` tags so many downstream users would execute the same malicious code.
6. The payload read secrets from runner memory and wrote them into GitHub Actions workflow logs, turning normal CI output into a leak surface.

## Evidence and impact
- [StepSecurity](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised) says the malicious `tj-actions` payload exposed CI/CD secrets in build logs and that public repositories were especially dangerous because anyone able to read the logs could recover the leaked values.
- [CISA](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) warned that exposed material could include access keys, GitHub PATs, npm tokens, and private RSA keys.
- GitHub's [advisory](https://github.com/advisories/ghsa-qmg3-hpqr-gqvc) says these additional actions were affected through the shared dependency path: `reviewdog/action-shellcheck`, `reviewdog/action-composite-template`, `reviewdog/action-staticcheck`, `reviewdog/action-ast-grep`, and `reviewdog/action-typos`.
- Public reporting ties the operation to mutable tag abuse, transitive GitHub Action dependencies, and insufficient separation between maintainer convenience and release-security boundaries.

## Defender takeaways
- Pin third-party GitHub Actions to full commit SHAs, and inspect transitive action dependencies instead of assuming top-level pinning is enough.
- Treat any affected workflow logs as sensitive evidence. If a run happened in the compromise windows, assume the exposed secrets are compromised and rotate them.
- Review historical workflow runs, not just current workflow files. This operation relied on retroactive tag movement and short-lived malicious windows.
- Reduce maintainer blast radius by limiting broad write access, avoiding automatic org invitations with repository-write permissions, and rotating PATs aggressively after CI or repo compromise.

## Audit windows
- [CISA](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction) advised organizations to audit use of `tj-actions/changed-files` between **2025-03-12 00:00 UTC** and **2025-03-15 12:00 UTC**.
- GitHub's [reviewdog advisory](https://github.com/advisories/ghsa-qmg3-hpqr-gqvc) and the [maintainer notice](https://github.com/reviewdog/reviewdog/issues/2079) place the `reviewdog/action-setup@v1` compromise window at **2025-03-11 18:42-20:31 UTC**.

## Sources
- CISA alert: https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction
- StepSecurity incident writeup: https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised
- GitHub issue for `tj-actions/changed-files`: https://github.com/tj-actions/changed-files/issues/2463
- GitHub advisory for `reviewdog/action-setup@v1`: https://github.com/advisories/ghsa-qmg3-hpqr-gqvc
- reviewdog maintainer advisory issue: https://github.com/reviewdog/reviewdog/issues/2079
- Unit 42 attack-chain analysis: https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/
