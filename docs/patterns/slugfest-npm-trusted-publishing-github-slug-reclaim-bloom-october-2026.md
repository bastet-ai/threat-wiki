# SlugFest: npm Trusted Publishing bound to reclaimable GitHub slugs — zero-credential package takeover, 1,500+ packages exposed, AI agents as the distribution layer (Bloom Security, October 13, 2026)

## Summary
Bloom Security's `SlugFest` disclosure (blog Oct 13, 2026; Golan Myers) demonstrates that npm's Trusted Publishing records its GitHub trusted-publisher binding as the mutable `owner/repo` **slug string** — plus the workflow-file basename and optional environment — and stores the immutable `repository_id`/`repository_owner_id` claims **only after the binding's first successful publish**. Until that first publish, the OIDC exchange succeeds if the token's `repository` claim string-matches the stored slug and the workflow filename matches — nothing checks the numeric IDs, because there is nothing stored to check them against. A maintainer rename, transfer, or deletion of the bound repository (or a rename/deletion of the bound owner account) frees the slug; anyone can claim it, add a matching workflow file, trigger it, mint an OIDC token carrying the reclaimed slug, and exchange it at npm for a **valid, time-limited publish credential for a package they do not own**. No maintainer npm account, GitHub account, or credential is touched. The attack was run end-to-end against a researcher-controlled package, publishing a new version from a second repository belonging to a different organization. Registry-wide, Bloom found **1,500+ vulnerable packages, 10M+ total downloads, 1M+ per month**, and declines to publish the affected list because the residual exposure persists. This is the demonstrated npm-side proof of the "a name is not an identity" thesis this wiki recorded for GitHub's own OIDC subject claims ([Sleeper Squats page](github-actions-oidc-subject-claim-collisions.md)) — same root cause (trust anchored to human-readable mutable namespace strings), now exploited through a registry's trusted-publishing exchange rather than a cloud IAM policy.

## Tags
- patterns
- npm
- Trusted Publishing
- OIDC
- GitHub Actions
- slug reclaim
- supply chain
- AI agents
- provenance

## Attack shape
- Maintainer runs `npm trust add github --allow-publish`: the CLI sends ONLY `repository` (owner/repo string), `workflow_ref.file` (YAML basename), optional `environment`. The immutable `repository_id`/`repository_owner_id` are in GitHub's OIDC token but npm never receives them at binding time and stores them only after a first successful publish from that repository.
- Precondition: a trusted-publisher binding that has **never published** + the bound GitHub slug becoming claimable (repo renamed/transferred/deleted, or owner account renamed/deleted). Once any version publishes from the bound repo, the immutable ID is recorded and this variant of the attack closes.
- Mechanical steps: create a repo at the freed slug (GitHub mints a FRESH `repository_id`); add a workflow file matching the bound basename; trigger it; the minted OIDC token carries the reclaimed slug in its `repository` claim; submit to npm's exchange endpoint; slug + workflow-basename match → publish credential issued.
- Blast radius: publish a malicious version under the legitimate name, inheriting reputation, download counts, dependents, and a **valid Sigstore provenance attestation signed against the attacker's repository** — downstream tooling that checks only "is it signed?" passes it. A malicious `postinstall` fires on every `npm install` behind it, and the transitive dependency cone multiplies reach.
- The AI-agent amplifier (measured across dozens of orgs): agents install `0.3–1.2` packages/day per agent, `2–3`/day on developer machines, `~3` agents per typical endpoint (`5+` on dev machines) → **~70 agent-installed packages/month per endpoint, ~350 on developer machines** (direct installs only). Bloom caught a customer's agent attempting to install one of the exposed packages. "A hijacked package doesn't need to fool a developer anymore. It only needs to be the package an agent chooses."

## Disclosure timeline (per Bloom)
- Reported to GitHub via HackerOne Jun 6, 2026; triaged/validated Jun 9; last substantive team response Jul 8 ("working on fixing…"); 6 unanswered enquiries including a HackerOne mediation request.
- Fix shipped Oct 2, 2026 — discovered by Bloom re-running the test before publication: **>120 days disclosure-to-fix**. GitHub changelog: unvalidated npm Trusted Publishing configurations now expire.
- Mechanism of the fix: npm still creates the ID binding at first publish, but **invalidates any trust binding with no publish event within 48 hours** — a mitigation-window clamp, NOT the clean fix. The clean fix Bloom specifies (and credits PyPI/Warehouse with implementing since launch): resolve owner/repo → `repository_id`/`repository_owner_id` at TRUST-CREATION time and require exact equality against the OIDC token claims at exchange time.
- Same weakness stated to exist in npm's GitLab trusted-publishing integration.

## Defensive lessons
- Treat every registry trust binding keyed on a mutable namespace string (GitHub slug, workflow basename) as a **revocation-tracking problem**: renaming, transferring, or deleting the bound repository is a revocation event — delete the binding BEFORE the repo goes, and re-create it on the current slug.
- Audit with `npm trust list` per package: confirm each listed slug still resolves to a repository YOU control, under the account you control. Re-create any binding pointing at a renamed/transferred repo.
- Provenance verification must check the attestation SOURCE repository against the project's expected repository — a signature alone is not an identity check. The attacker's publish is correctly signed, by the attacker.
- The pre-first-publish window is the exposed window: newly configured bindings carry the risk until the first ID-recording publish (npm's fix caps it at 48 h for unvalidated configs, but pre-Oct-2 unvalidated bindings' retroactive status is unconfirmed — GitHub's changelog does not say existing configurations were bound retroactively).
- For registry/CI trust design generally: immutable numeric IDs resolve at authorization time, not after the fact. This is the third on-wiki instance of the class (Sleeper Squats subject-claim collisions; Aikido's GitLab incoming-email token-as-address; now SlugFest).
- Agent-era perimeter: dependency installers are no longer only humans. Egress/install controls must cover agent-driven installs (~70/endpoint/month observed), which arrive with no review step and take `latest` by default.

## Current status
- npm fix live since Oct 2, 2026 (48-h expiry on unvalidated bindings); no evidence of in-the-wild exploitation reported by Bloom.
- Bloom is NOT releasing the vulnerable-package list (issue still prevalent for pre-existing unvalidated bindings); users of npm packages can only self-verify via provenance-attestation source checks.
- Adoption context: npm Trusted Publishing GA July 2025, still <20% of active packages — the exposed set is large RELATIVE to the configured population, not the registry.
- HackerOne program conduct under criticism: >120 days silence, mediation requested; final GitHub reply arrived with the apology + fix confirmation.

## Related pages
- [GitHub Actions OIDC subject-claim collisions](github-actions-oidc-subject-claim-collisions.md) — Boost "Sleeper Squats": the same name-vs-identity root cause on GitHub's own subject claims
- [GitLab incoming-email token account-wide credential bypass](gitlab-incoming-email-token-account-wide-credential-ip-allowlist-bypass-aikido-september-2026.md) — mutable address strings as unrevocable credentials
- [npm publish-time malware scanning](npm-publish-time-malware-scanning.md) — what registry-side detection can and cannot catch for a legitimately-published malicious version
- [npm install explicit trust controls](npm-install-explicit-trust-controls.md) — installer-side controls for the agent-distribution path
