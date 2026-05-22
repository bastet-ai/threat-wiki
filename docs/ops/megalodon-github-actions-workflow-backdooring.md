# Megalodon GitHub Actions workflow backdooring

## Summary
SafeDep reported a mass GitHub repository backdooring campaign it calls **Megalodon**. On May 18, 2026, the campaign pushed 5,718 malicious commits to 5,561 repositories in roughly six hours, using throwaway accounts and forged CI-looking author identities such as `build-bot`, `auto-ci`, `ci-bot`, and `pipeline-bot`.

The payload lived in GitHub Actions workflow files rather than application runtime code. The workflows decoded and executed base64-encoded bash that exfiltrated CI environment variables, cloud credentials, SSH keys, source-code secrets, GitHub Actions OIDC tokens, and other runner-accessible material to `216.126.225[.]129:8443`. StepSecurity's May 22 analysis frames the campaign as direct poisoned pipeline execution (`d-PPE`): the attacker used repository write paths and weak branch-protection defaults to land workflow changes directly on default branches, avoiding pull-request review entirely.

## Tags
- ops
- operations
- supply-chain
- GitHub Actions
- CI/CD
- credential-theft
- OIDC
- workflow backdoor
- npm

## Why this matters
- The campaign demonstrates direct repository write access abuse at scale: malicious commits were pushed into many repositories without relying on pull-request review paths.
- CI workflow files are high-impact backdoor locations because a small YAML change can run in a secret-bearing environment, request `id-token: write`, mint short-lived cloud OIDC credentials, and reach metadata services.
- The `workflow_dispatch` variant is especially stealthy: it can sit dormant with no immediate failed run or obvious Actions-tab noise until the attacker triggers it through the GitHub API.
- The Tiledesk case shows a second-order package risk: `@tiledesk/tiledesk-server` versions `2.18.6` through `2.18.12` reportedly carried a poisoned workflow because legitimate npm publishes were made from the already-compromised GitHub repository.
- Branch protection is the key structural boundary: mandatory pull-request review and workflow-change review convert this direct-push `d-PPE` path into a harder indirect PPE problem where an attacker must convince a maintainer to merge malicious CI changes.

## Reported chain
1. The attacker obtained repository write paths, likely via compromised personal access tokens or deploy keys, then pushed directly to default branches.
2. Commits used CI-like author names, generic noreply-style identities, and routine-looking messages such as `ci: add build optimization step`, `build: improve ci performance`, and `chore: update ci/cd pipeline`.
3. The mass variant added `.github/workflows/ci.yml` named `SysDiag`, triggered by `push` and `pull_request_target`.
4. The targeted variant replaced existing workflow content with `Optimize-Build`, used `workflow_dispatch`, and requested `id-token: write` plus `actions: read`.
5. The decoded bash harvested environment, cloud, source, container, Kubernetes, Vault, Terraform, shell-history, SSH, npm, netrc, and CI tokens, then exfiltrated to `216.126.225[.]129:8443`.

## Notable affected repositories and package propagation
SafeDep says `@tiledesk/tiledesk-server` versions `2.18.6` through `2.18.12` contained the targeted workflow variant. The malicious change replaced `.github/workflows/docker-community-worker-push-latest.yml` with a dormant `workflow_dispatch` workflow, while application code remained otherwise identical. This means npm consumers were not the direct execution target; CI/CD runners in repositories using the poisoned source workflow were.

StepSecurity lists nine affected Tiledesk repositories, including `tiledesk/tiledesk-server`, `tiledesk/tiledesk-dashboard`, `tiledesk/tiledesk-telegram-connector`, `tiledesk/tiledesk-llm`, `tiledesk/tiledesk-docker-proxy`, `tiledesk/tiledesk-community-app`, `tiledesk/tiledesk-campaign-dahboard`, `tiledesk/tiledesk-helpcenter-template`, and `tiledesk/tiledesk-ai`. It also calls out Black-Iron-Project and WISE-Community as additional confirmed affected repository clusters.

## Indicators and hunt pivots
- Campaign name/string: `megalodon`.
- C2: `hxxp://216[.]126[.]225[.]129:8443`.
- Workflow names: `SysDiag`, `Optimize-Build`.
- Workflow paths: newly added `.github/workflows/ci.yml`, filenames such as `SysDiag.yml` or `Optimize-Build.yml`, or unexpected replacement of existing build/publish workflows.
- Permissions: unexpected `id-token: write` and `actions: read` on workflows that previously did not need them.
- Triggers: `pull_request_target` on broad workflows; unexpected `workflow_dispatch` replacing normal push/build triggers.
- Author names: `build-bot`, `auto-ci`, `ci-bot`, `pipeline-bot`.
- Author-email pivots reported by StepSecurity: `build-bot@github-ci.com`, `ci-pipeline@actions-bot.com`.
- Commit messages: `ci: add build optimization step`, `build: improve ci performance`, `chore: optimize pipeline runtime`, `chore: sync ci configuration`, `chore: update ci/cd pipeline`, `ci: update build config`, `fix: correct build workflow`.
- Tiledesk commit: `acac5a9`; package versions: `@tiledesk/tiledesk-server` `2.18.6` through `2.18.12`.

## Defender heuristics
- Search recent default-branch commits for CI-looking author names, generic automation messages, and unlinked author/committer identities.
- Diff `.github/workflows/` from a known-good baseline, not just application source files.
- Treat added `id-token: write`, `pull_request_target`, base64 decode-and-execute one-liners, broad secret collection, or metadata-service probes as high severity.
- Require branch protection and human review for workflow-file changes on default branches; workflow YAML is security-sensitive code, not routine build plumbing.
- Restrict CI runner egress where possible; StepSecurity notes the payload depended on normal outbound HTTPS access to reach `216.126.225[.]129:8443` and exit cleanly.
- Disable suspicious workflows before rotating credentials; otherwise manual dispatch or future push events can re-steal newly issued secrets.
- Rotate GitHub, cloud, package-registry, Docker, Kubernetes, Vault, Terraform, SSH, and application secrets that were reachable from affected runners.
- Review audit logs for workflow dispatch events, direct pushes by deploy keys/PATs, new fine-grained tokens, and unexpected repository write access around May 18, 2026.

## Attribution notes
SafeDep describes Megalodon as an automated campaign but does not publicly tie it to a named actor in the report used here. Keep it separate from TeamPCP / Mini Shai-Hulud unless stronger sourcing links them.

## Related pages
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- SafeDep: https://safedep.io/megalodon-mass-github-repo-backdooring-ci-workflows/
- StepSecurity: https://www.stepsecurity.io/blog/megalodon-mass-github-actions-secret-exfiltration-across-5-500-public-repositories
- The Hacker News: https://thehackernews.com/2026/05/megalodon-github-attack-targets-5561.html
