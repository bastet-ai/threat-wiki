# GitHub Actions OIDC subject-claim collisions

## Summary
GitHub Actions OIDC tokens let workflows exchange a GitHub-signed JWT for cloud, registry, or vault credentials. Boost Security Labs' June 2026 "Sleeper Squats" disclosure is a useful reminder that relying parties should not treat human-readable `sub` strings as stable identity unless the identity provider uses unambiguous delimiters and the relying party understands the immutable claims behind them.

In April 2026, GitHub briefly exposed an immutable subject-claim format that appended owner and repository IDs with hyphens, for example `repo:octo-org-123456/octo-repo-456789:ref:refs/heads/main`. Because hyphens are valid in GitHub organization and repository names, an attacker could pre-register a legacy organization such as `octo-org-123456` and mint a legacy `sub` value that string-matched the victim's future immutable-form trust policy. Boost reported the issue to GitHub; GitHub disabled the feature and later reshipped it with `@` as the delimiter.

## Tags
- patterns
- GitHub Actions
- OIDC
- CI/CD
- supply-chain
- cloud IAM
- trusted publishing
- subject claim
- namespace recycling

## Attack shape
- GitHub's original immutable-claim preview used a hyphen between mutable names and immutable IDs: `OWNER-OWNER_ID` and `REPO-REPO_ID`.
- Existing repositories and attacker-created repositories still emitted legacy `sub` values based on names alone.
- An attacker could register a lookalike namespace whose literal name included the victim's future immutable suffix, such as `<target>-<target_id>`.
- If the victim opted in and copied the previewed string into AWS IAM, Azure Entra ID, GCP Workload Identity Federation, Vault, OctoSTS, or a package-registry trusted-publishing configuration, the attacker's legacy `sub` could become an exact string collision.
- Org-wide patterns such as `repo:octo-org-123456/*` are especially dangerous because the attacker may not need to squat every repository name.

## Defensive lessons
- Treat GitHub Actions OIDC `sub` strings as protocol inputs, not as arbitrary parseable text.
- Prefer provider- or registry-side checks that evaluate immutable numeric claims such as `repository_owner_id` and repository IDs instead of authorizing only on human-readable owner/repository strings.
- Avoid broad org-wide `sub` trust patterns where a repo-scoped trust policy is feasible.
- Review OIDC trust policies for string patterns that could match unexpected namespaces, especially wildcard forms and old copy-pasted examples.
- During identity-format migrations, verify that delimiters cannot appear in the namespace alphabet. GitHub's current `@` delimiter is not valid in GitHub organization or repository names, which closes the exact collision described by Boost.
- For package trusted publishing, confirm whether the registry resolves configured owner/repository strings to immutable IDs internally. Boost says PyPI is designed to evaluate integer `repository_owner_id`; public npm, RubyGems, and crates.io flows appeared string-oriented unless their backend performs an additional resolution.

## Current status
- Boost says the constructible collision was reported through HackerOne on 2026-04-24, disabled roughly an hour after the report, and published after GitHub approved disclosure.
- GitHub's changelog and documentation now use `@` between name and ID, for example `repo:octo-org@123456/octo-repo@456789:ref:refs/heads/main`.
- GitHub says repositories created after 2026-07-15 use the immutable default subject format; older repositories keep the previous format unless explicitly opted in. GitHub Enterprise Server is not included in that rollout per the current docs.
- Boost states there is no evidence of compromise from the short-lived hyphen format.

## Related pages
- [GitHub Actions deployment poisoning](deployment-poisoning-github-actions.md)
- [binding.gyp npm CI/CD worm](../ops/binding-gyp-npm-cicd-worm.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- [Boost Security Labs](https://labs.boostsecurity.io/articles/sleeper-squats-github-oidc-immutable-subject-claim/)
- [GitHub Changelog](https://github.blog/changelog/2026-04-23-immutable-subject-claims-for-github-actions-oidc-tokens/)
- [GitHub Docs](https://docs.github.com/en/actions/reference/security/oidc)
