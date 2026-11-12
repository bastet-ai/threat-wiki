## Tags
- ops
- GitHub-Actions
- supply-chain
- CI-CD
- secret-exfiltration
- compromised-accounts
- runner-memory-scraping
- cloud-credential-abuse
- StepSecurity
- wfx
- ghostaction-adjacent

# WFX Phantom CI secret stealer

**Class:** CI/CD secret stealer pushed through stolen GitHub tokens (a subset issued to the Fly.io GitHub App), executed by the victim's own GitHub Actions runner, with automated evidence cleanup (revert + workflow-run deletion)
**First reported:** StepSecurity blog, "WFX Phantom: The GitHub Actions Secret Stealer That Deletes Its Tracks" (Owais Shaikh, November 12, 2026), full text captured by this wiki same-day via blog HTML
**Campaign start:** November 10, 2026 (first HTTP-exfil copies); exfil transport pivoted to Telegram-only during November 12

## Why this matters to this wiki's watch

This is the CI lane's answer to what the registry lane keeps measuring: the credential is the package. WFX Phantom does not exploit GitHub Actions — it *uses* it, with valid tokens for real developer and bot accounts, exactly the way a developer would. Its evidence-deletion step (revert plus workflow-run deletion, usually inside a minute) makes the Actions **run-number gap** the primary forensic artifact, and its same-day transport pivot (HTTP → Telegram) makes any blocklist built from the first published IPs stale within hours. Three of the sampled repositories were also hit by the October GhostAction wave, and one commit carries a hidden VS Code task in the PolinRider style: the re-infection-of-previously-compromised-accounts law this wiki stated on the GhostAction page lands with fresh specimens three days later. Overlap is quoted, single-actor identity NOT asserted — stolen token pools are shared goods.

## The three-step play (StepSecurity's facts, captured at read)

1. **Probe:** open a pull request titled `docs: dependency audit notes` (body "Routine dependency audit notes") from branch `wfx-docs`, adding a byte-identical `docs/wfx-audit.md` (git blob `ee6e5addfe591923fc385553cb66cf0d25634a6b`). The PR does nothing — it tells the attacker the token can write. **A probe PR means the opening account is compromised even if nothing else happened.** At 07:40Z Nov-12, GitHub search returned **63,000+ probe PRs, ~90% still open**, new ones arriving every few minutes.
2. **Payload:** push a ~1,500-line shell stealer via one of FOUR hiding places: (a) append two steps to an existing workflow (`ci: refresh build cache`, >21,000 commits Nov-10→12), one step handing the job's internal tokens to the next, the step named `Restore cache x9xx` carrying the script; (b) APPEND the script to an ordinary shell script CI already runs (`nextcloud/docker update.sh` line 211 sets the collection server; `tests/retry_env.sh` variants) — no workflow-file change at all; (c) `chore: add dependency audit workflow` adding `.github/workflows/build-audit-<6>.yml` on a throwaway `chore/<8>` branch; (d) `chore: add ci helper`: hidden `.ci-<6>.sh` at repo root + a `package.json` hook (`postinstall` 11×, `build` 2×, `test` 1× in samples) so **npm install fires the stealer** — the registry/CI boundary crossing that puts this page in the package ledger.
3. **Cleanup:** revert commit (`ci: restore`, sometimes `ci: cleanup`) + DELETE the workflow run and its logs, usually within a minute. **A missing run number in the Actions tab right after such a commit means the stealer probably ran: treat every secret and cloud role that workflow could reach as stolen.**

## The stealer's four stages

- **Collect:** every repo secret and variable (`toJSON(secrets)`/`toJSON(vars)`), the job's `GITHUB_TOKEN` + cloud sign-in token capability, **the Runner.Worker process memory in decrypted form** (secrets the workflow never asked for — this is how the shell-script and npm-hook placements steal without touching a workflow file), every process environment, credential files (AWS/Azure/GCP/Docker/Kubernetes/npm/PyPI/SSH/Vault), AI-provider and coding-agent API keys, and on self-hosted runners the cloud instance-metadata credentials, plus a repo snapshot with recent history and workflow artifacts.
- **Escalate:** the job's OIDC cloud sign-in token opens AWS/GCP/Azure sessions, chains into further AWS roles named in the repo, impersonates GCP service accounts, and replays cached Azure CLI refresh tokens into Microsoft Graph + Key Vault.
- **Persist (designed to outlast rotation):** (a) built-in but UNACTIVATED required-check-passing switch (off in all 101 copies examined); (b) AWS: rewrite an assumed role's trust policy to `"Principal": {"AWS": "*"}` + attempt `iam:CreateAccessKey` = long-lived keys surviving rotation; (c) Azure: add a federated identity credential `wfx-ci-<n>` to AD apps so the attacker's workflows sign in with NO stored secret.
- **Exfiltrate:** one gzipped archive. GitHub-native channels exist in code (Actions cache, step summary between `<!--WFX-BEGIN-->` markers, `wfx-loot-<run>` artifact) but were OFF in every copy. Delivery in 101 copies: 57 × HTTP POST to `194.150.166[.]244:8080/exfil`, 3 × `18.143.168[.]96:8080/exfil`, 1 × HTTP + Telegram backup (third server `153.75.82[.]159:8080/exfil`, first seen 01:10Z Nov-12), and **43 × Telegram-ONLY from ~05:30Z Nov-12** (`api.telegram.org` `sendDocument`, chat `-1004340163187`, five bot tokens; callback IP hard-set to `127.0.0.1`; in-script comment: "no callback IP anywhere in the payload"). **The pivot means IP blocklists built from the Nov-10 addresses miss every newest copy; an egress allowlist stops both, since neither a bare IP nor `api.telegram.org` belongs in a normal build.**

## The Fly.io GitHub App vector (first disclosed 2026-11-12 by StepSecurity)

On 173 probe PRs opened from 19 accounts, GitHub's own API records `performed_via_github_app` = the **Fly.io GitHub App** (`fly-io`, app ID 34557, permissions: write to contents/actions/pull-requests) while the PR still shows the account owner as author = the attacker held **user-granted app tokens** and acted AS the user. PR bursts (Nov-11 10:02-10:36Z, Nov-12 06:20-06:30Z) opened PRs for 4-7 unrelated accounts within the same one-to-two seconds = one operator parallelizing across a token pool. Token acquisition method NOT established; **no evidence of a breach of Fly.io's own infrastructure**; most campaign activity uses other credential classes (PATs). Durable read: **the token that mattered was issued by an OAuth grant the user made to a third-party app — app-token sprawl is now a CI blast-radius input, same family as this wiki's trusted-integration law (Qubole, Railway).**

## Bot-account economics

The stealer was pushed as **bot accounts** in two sampled cases: `drubot` committed to `drunomics/nuxtjs-drupal-ce` default branch (run #1964 then deleted between #1963 and #1965, revert 12 s after the payload), and `wdio-bot` pushed 56 `chore: add ci helper` commits across 28 WebdriverIO repos **with branch-protection bypass rights** (a contributor spotted them in 20 minutes; no WebdriverIO package release was affected). Durable: **automation accounts with write + bypass rights are as valuable to this attacker as maintainers** — audit bot-token grants the same way you audit human ones.

## The surviving run (nextcloud/docker, run #2675)

The stealer appended to `update.sh` ran three seconds after the commit and the run was NEVER deleted (revert came 27 minutes later, by a Nextcloud developer). The public log reads itself: `memscan_files 3`, `gcp_live`, `token=0 projects=0 gcloud=0`, `selfhosted_collected` (the runner was Nextcloud's OWN server, so metadata + machine-wide collection fired), `az_graph_token_fail`, `oidc_discovery arn=none gcp=none azure=none`, `archive_bytes 8971`, `exfil_no_runtime_vars` — no upload-retry message anywhere, so **the first upload to `194.150.166[.]244` succeeded and the job finished green**. Self-hosted runners widen collection scope silently; the green checkmark is not a clean bill.

## Releases that carried it (supply-chain tail)

Where a repository publishes automatically on push, the stealer reached a release: `digitalelvis/neuronai-studio 3.14.3` (Packagist — ships the `.ci-*.sh` + `postinstall` hook; `composer install` does not fire it, `npm install` inside the package directory does — pin ≤3.14.2); `github.com/onuragtas/docker-env v1.0.278/v1.0.280` and `github.com/vkuznet/gocurl v0.0.0-20261111095532-8d5aad0cb0da` (Go — stealer only in a workflow file inside the tags; Go builds never run workflow files, but **the module proxy keeps serving the pseudo-version after the commit was reverted** — `vkuznet/gocurl` was still live at publication). Check `composer.lock`/`go.sum`; rebuild any package published between a malicious commit and its `ci: cleanup` revert from a clean commit. **The Go module proxy law is this wiki's CDN-outlives-the-package law (jsDelivr/radio-player-theme) re-landed on the Go lane: a revert does not revoke a pseudo-version.**

## Indicators (per-read, quote source and time)

- Collection servers: `194.150.166[.]244:8080/exfil`, `18.143.168[.]96:8080/exfil`, `153.75.82[.]159:8080/exfil`
- Callback tokens (sent as `t=`): `b42d70a7aab9140ca19e8249`, `15f44heehnax8jdf41yx`
- Telegram: `api.telegram.org` `sendDocument`, chat `-1004340163187`, bot IDs `8708988906`, `9196217635`, `9180059428`, `8902935164`, `8876515636`
- PR grammar: title `docs: dependency audit notes`, branch `wfx-docs`, file `docs/wfx-audit.md` (blob `ee6e5addfe591923fc385553cb66cf0d25634a6b`)
- Commit messages: `ci: refresh build cache`, `ci: restore`, `ci: cleanup`, `chore: add ci helper`, `chore: add dependency audit workflow`, `chore: initial commit before the workflow` (empty repos)
- Branch/file grammar: `chore/[a-z0-9]{8}`, `ci-check-[0-9]{4}`, `.ci-[a-z0-9]{6}.sh`, `.github/workflows/build-audit-[a-z0-9]{6}.yml`
- Script markers: steps `Pass runtime`, `Restore cache <4>`, `Run audit`; vars `WF_CALLBACK`, `WF_CTOKEN`, `WF_EXFIL_*`, `WF_TG_BOTS`; staging dir `.wfx-$$`; log notes `memscan_files`, `selfhosted_collected`, `archive_bytes`, `exfil_no_runtime_vars`
- Fly.io GitHub App: `fly-io`, app ID `34557` (`performed_via_github_app` in probe-PR API records)
- Third-party artifact: 19 files named `SECURITY_INCIDENT_2026-11-10.md` = one developer's own per-repo incident write-ups, useful as a victim census

## What to do

Search your org for the PR/commit grammar above on or after November 10; then check the Actions tab for **missing run numbers** adjacent to those commits. A gap = assume the stealer ran: rotate every repo secret/variable, the job-reachable cloud roles, and everything the Runner.Worker memory could hold; audit AWS trust policies for `"AWS": "*"` and AD apps for `wfx-ci-*` federated credentials; check bot-account token grants for write/bypass rights; review third-party GitHub App grants as blast-radius inputs. Egress-allowlist the build fleet (kills both HTTP and Telegram exfil). If you were hit in the October GhostAction wave, check for this wave too — previously-compromised accounts get re-fished from shared token pools.

## Overlaps quoted, kinship NOT asserted

Three samples were injected into `security-audit.yml` files left behind by GhostAction, still pointing at the October collection server `193.32.204[.]199`; one commit additionally planted a hidden VS Code task running a Node.js file on folder open (PolinRider technique). Stolen-token reuse across campaigns is the parsimonious reading; no single-actor claim. See [GhostAction page](ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md).

## Monitor forward

- Does GitHub ship detection for deleted workflow runs (run-number-gap telemetry is currently a manual hunt)?
- `wfx-docs` probe-PR growth curve vs the 63k/07:40Z census; does the Telegram-only share keep climbing; new bot tokens?
- Fly.io response + any second app-ID cohort (app-token laundering spreading beyond Fly.io)?
- Whether the `wfx-ci-*` Azure persistence or the AWS `"AWS":"*"` rewrite gets confirmed in the wild (StepSecurity saw switches armed in zero of 101 copies);
- The activated-but-unused required-check-passing switch (first field use = new ATT&CK-visible primitive);
- `vkuznet/gocurl` pseudo-version lifecycle (proxy purge precedent for post-revert Go supply chain);
- Attribution: any actor naming, and whether the token pool links to GhostAction/PolinRider infrastructure reuse.
