## Tags
- ops
- GitHub-Actions
- supply-chain
- workflow-injection
- secret-exfiltration
- compromised-accounts
- CI-CD
- Wiz
- gheist
- megalodon
- polinrider

# Gheist: 13,500+ planted `ci-sync-*` branches across 850+ compromised GitHub accounts dump every repository secret through GitHub's own API — base32 defeats log masking, `permissions: {}` does not gate the `secrets` context, and GitHub's public-repo approval hold is exactly why private repos and GHES burned (Wiz Research, Oct 25, 2026)

**Captured by this wiki at feed+full-text level Oct 25 ~23:4x UTC, ~45 min after publication.** Wiz Research (published `2026-10-25 17:55:33Z`, `wiz.io/blog/gheist-attempted-scaled-abuse-of-stolen-github-tokens-stumbles`) tracks since **Sep 15, 2026** a mass-abuse campaign over compromised GitHub tokens: for every repository each stolen token reaches, the tool creates a branch `ci-sync-` + six random chars, commits `.github/workflows/sync-check.yml` with message `ci: sync config` (unsigned, authored as the token owner), the `push` trigger runs the job, and **the tool then downloads the workflow log via the GitHub API and deletes the run within seconds.** API traffic carries user agent `gheist`. Scale on record: **>13,500 planted branches, >850 compromised accounts** (personal projects → enterprise private orgs); as of Oct 24 the attack is ongoing, evolving, and **≈⅔ of implicated accounts are already gone from GitHub** (Wiz reported the activity to GitHub — response activity, not necessarily takedown of the operator).

## Why the trick works — three durable mechanics

1. **GitHub masks secret values in logs only when they appear verbatim.** The payload prints `env | base32 -w 120` and `echo -n '${{ toJSON(secrets) }}' | base32 -w 120` — a base32-encoded secret never matches the masking token, so **every secret prints in full**. (Same masking-defeat class as this wiki's base64-in-logs precedents; encoding is the universal bypass of string-match redaction.)
2. **`permissions: {}` restricts the job's `GITHUB_TOKEN` — it does NOT restrict the `secrets` context.** An apparently locked-down workflow still hands over everything; the attacker never needs the token, only the log. Defenders who read `permissions: {}` as "harmless" are reading the wrong field.
3. **Exfiltration has no attacker domain.** The secrets leave through GitHub's own logs API and the attacker pulls them down — there is no outbound connection, no egress IOC, no DNS to sinkhole. Detection must be behavioral (branch/commit/log patterns, UA `gheist`), not network-side.
4. **Environment matrix escalates scope:** where a repo has deployment environments, the job matrices over `environment: ${{ matrix.environment }}`, pulling **environment-scoped secrets — often production credentials** — into one run.

## Two tools, one campaign, and a self-hosted-runner pivot

- **Tool A**: hex branch suffix, plain payload. **Tool B**: base36 suffix, added `timeout-minutes: 6` + the environment-matrix within hours of its first run (Sep 28), per-repo payload selection; Oct 19 added `echo X | base32` printing `LAFA====` as a log-parser separator.
- **Oct 19 (Tool B)**: second job `sync-host` with `runs-on: self-hosted`, pushed only at repos with a registered self-hosted runner. Writes `.gdmp_pat`, `.gdmp_patg`, `.gdmp_sweep`; stage headers `===== gdmp-pivot: <stage> =====`; collects host details + crontab; recursive home/workspace/system search for **31 token formats** (incl Anthropic, Hugging Face, Groq, NVIDIA keys), private keys, `.env`, Terraform state, shell history; **every process environment via `/proc/*/environ`**; **through the Docker socket, mounts the host root filesystem in a container and repeats the sweep on the host**; AWS instance-role creds + GCP/Azure metadata; Actions/GitLab runner credential files; the Kubernetes SA token. Wiz notes the job is BUGGY (wrong runner key path, broken URL-credential regex, GCP/Azure collection not wired) — low-discipline tradecraft, high still-lethal reach.
- **The control that worked — and where it doesn't apply:** since **Jul 28, 2026**, GitHub holds potentially-malicious workflow runs in PUBLIC repos at `action_required` until a collaborator approves; every public Gheist run Wiz checked is sitting unexecuted. **The hold does NOT apply to private repos or GitHub Enterprise Server** — there, audit logs show runs completing then being deleted by the `gheist` UA, and **CloudTrail shows org workflows on `ci-sync-*` branches assuming AWS roles** = Actions executed without approval, and cloud creds from the same org enumerated AWS Secrets Manager hours later. Cross-plane detection law for defenders: **CloudTrail role-assumptions whose OIDC subject includes a `ci-sync-` branch prove compromise with ZERO GitHub logs.**

## The credential pool is shared — the campaign map, not just a campaign

Wiz traces token sources to infostealer logs and **tokens exposed in earlier supply-chain compromises (e.g. the March Trivy compromise)** — the compromised-token pool is a reusable ecosystem asset. Same-account overlaps observed:
- **Lure repositories (Oct 6):** 391 accounts renamed ~1,461 repos to cracked-software lures (`fl-studio-crack`, `solana-sniper-lite`); the renames wiped 610 `ci-sync` branches as a side effect; **166 of those accounts never appear in Gheist activity = the stolen-token pool is bigger than any one campaign's footprint.**
- **Free compute (Oct 18):** 25 Gheist accounts each created a "Windows RDP Runner" repo within nine minutes — Actions compute theft.
- **PolinRider (DPRK-linked):** Oct 19–20, three victims re-pushed their Gheist commits with a loader hidden behind hundreds of whitespace chars in `vite.config.js`, two also an `api.js` that `package.json` runs before every `dev`/`build` = a second actor moving onto the same compromised accounts within HOURS.
- **Megalodon:** 57 first-phase Gheist accounts were also May Megalodon victims (this wiki's `megalodon-github-actions-workflow-backdooring` page) — the same GitHub-Actions-as-delivery-surface community, months apart.
- **Explicit disambiguation (Wiz):** Gheist ≠ **GhostAction** (this wiki: Oct-9 workflow-injection page) — different workflow files, GhostAction exfiltrates to `193.32.204[.]199`, Gheist exfiltrates through GitHub's own API.

## Hunt / respond / harden (Wiz IoCs, quotable verbatim)

- Branch regex `^ci-sync-[0-9a-z]{6}$`; commit message `ci: sync config` adding ONLY `.github/workflows/sync-check.yml`; UA `gheist`; payload markers `toJSON(secrets) }}' | base32 -w 120`, `===== gdmp-pivot:`; files `.gdmp_pat`, `.gdmp_patg`, `.gdmp_sweep`.
- **Workflow blob SHAs (git blob hashes, not file hashes):** `f3da2b8b357dcda02fd455d314be2a95007516a6` (plain), `d09535857a741bbb976bdc084a9a021713133291` (timeout), `1dc5af9cce950aad1eb1546ecce8565b117540c4` (separator), `c665b778b2d822453293003e7ca0bbb2cb08e39d` (self-hosted job). Environment-matrix variants differ per repo — blob SHAs are variant-fragile, the branch/commit-message pair is the durable key.
- GitHub audit: runs on `ci-sync-*` branches **deleted within a minute of completing** = the pull-and-erase signature. Cloud audit: OIDC role assumptions with a `ci-sync-` subject. Self-hosted runners: the `.gdmp_*` files + `gdmp-pivot` in job logs.
- Respond: rotate EVERY repo/org/environment secret reachable from an affected repo (deleting the run/branch does NOT undo exposure); revoke the pushing tokens and check owners' devices for infostealers; a `ci-sync` run on a self-hosted runner ⇒ treat host + instance role as compromised; never approve a held `sync-check` run.
- Harden: required reviewers on production-secret environments; OIDC trust scoped to protected branches/environments; GitHub Apps / short-lived fine-grained tokens over PATs; ephemeral self-hosted runners without Docker-socket or unrestricted metadata access.

## What this adds to the lane's laws

1. **The `secrets` context is outside the permission system.** `permissions: {}`, `timeout-minutes`, and a clean-looking name are costume; the only honest review question for an added workflow is *what does the log carry*.
2. **Log masking is a string-matching control and encoding always wins** — base32/base64/`xxd` all defeat it. Treat any encoding pipe around `${{ toJSON(secrets) }}` or bare `env` as hostile on sight.
3. **API-mediated exfil has no network IOC.** "No suspicious egress" is not evidence of no compromise when the attacker downloads GitHub's own logs endpoint.
4. **A control that covers public repos trains the ecosystem into ignoring private/GHES** — the Gheist operator never touched anything GitHub would approve-hold. Detection parity across repo visibility is the fix.
5. **Stolen GitHub tokens are a shared, tradable pool** (Gheist × lure-rename × cryptomining × PolinRider × Megalodon on overlapping accounts, sources incl infostealers and the March Trivy exposure). One actor's incident on your org is an invitation to four others; respond at the credential, not the campaign.

**Related on-wiki:** [GhostAction](ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md) · [Megalodon](megalodon-github-actions-workflow-backdooring.md) · [LiteLLM GitHub dead-drop loader](litellm-1-107-0-wheel-only-privcollect-startup-hook-credential-stealer-hourly-github-dead-drop-loader-jfrog-october-2026.md) · [GlassWorm OVHcloud](glassworm-developer-supply-chain-botnet.md)
