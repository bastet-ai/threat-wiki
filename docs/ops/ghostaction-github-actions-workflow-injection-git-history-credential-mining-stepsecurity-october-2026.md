## Tags
- ops
- GitHub-Actions
- supply-chain
- workflow-injection
- credential-theft
- secret-exfiltration
- CI-CD
- compromised-accounts
- StepSecurity
- ghostaction

# GhostAction returns: maintainer-account workflow injection sweeps 345 repos, and the October payload mines the ENTIRE git history (StepSecurity, Oct 9, 2026)

**Class:** CI/CD workflow injection via compromised maintainer accounts — exfiltration of named Actions secrets PLUS every credential pattern in the working tree and the full commit history
**First reported:** StepSecurity blog, "GhostAction Returns: Malicious 'Security Audit' Workflows Now Mine Credentials from Entire Git Histories" (Rohan Prabhu, October 9, 2026) — full text captured by this wiki same-day via blog HTML (the RSS route 404s per the ledger's StepSecurity feed mechanic; blog listing walk worked)
**Campaign lineage:** GhostAction, first documented by StepSecurity September 2025 (3,000+ secrets across 817 repos / 327 developers); never stopped — 2025-era payload still deploys alongside the new one

## Why this matters to this wiki's watch

This is the workflow-backdoor cost side of the credential-harvesting story this ledger tracks from the package side (Mini Shai-Hulud / ChainDrop harvest secrets at build time; GhostAction delivers a victim-self-executing harvester INTO the build system). The October upgrade — `git log -p --all` full-history mining — breaks the standard remediation this wiki has repeated for every package compromise: **rotating configured secrets is no longer sufficient; every credential ever committed to the repository must be treated as compromised.**

## The October 8 wave (StepSecurity's facts, captured verbatim)

| Window (UTC, Oct 8) | Compromised account | Repositories | Detail |
|---|---|---|---|
| 13:20–13:44 | `kitao` (Takashi Kitao, pyxel author, 18.4K stars) | 27 | pyxel got three commits: "Add security audit workflow" 13:20:36, updates 13:36:30 / 13:42:33; workflow then run **twice manually via `workflow_dispatch` from the compromised session** = hands-on-keyboard verification |
| 21:10–21:26 | `henrywoo` (Henry Wu, uid 458995, original author of Uber's athenadriver) | 318 (39 source + 279 forks) | uber/athenadriver injected last at 21:25:54, commit `e3c0dfa`, git author `Henry <wufuheng@gmail.com>`, UNSIGNED, straight to master — no PR, bypassing Uber review entirely |

- Injection path assessed as the maintainer's own leaked PAT (infostealer logs / dumps) — every commit carries the victim's legitimate identity, nothing looks anomalous in audit logs unless workflow CONTENT is inspected.
- **Exfiltration confirmed** from run 37846728441 (uber/athenadriver): the C2's HTTP response body `OK` is echoed in the run log at 21:26:04Z, four seconds after run start.
- `typecho-fans/plugins` (compromised `xxyangyoulin`, infected since Sep 5): two commits whose only purpose was re-triggering (an EMPTY commit + a 3-line README edit "Trigger security scan") — both runs STALLED in `action_required` because the repo requires run approval. **A one-setting control broke the kill chain.**

## Payload anatomy (Variant B = the October upgrade)

File names: `.github/workflows/security-audit.yml` ("Security Audit", job `audit`) or `github_actions_security.yml` ("Github Actions Security", job `send-secrets`, step "Prepare Cache Busting"). Triggers: `workflow_dispatch` + UNFILTERED `push` (any branch/tag). Four behaviors:

1. **Named-secrets append** (Variant A carried forward): recon-scanned `${{ secrets.NAME }}` references templated into the POST. pyxel's copy templated its PUBLISHING credentials (`CARGO_REGISTRY_TOKEN`, `PERSONAL_ACCESS_TOKEN`, `PYPI_USERNAME`/`PYPI_PASSWORD`) = direct path to shipping a malicious version of an 18K-star library dual-published to PyPI + crates.io.
2. **Working-tree sweep** for 13 credential patterns: AWS AKIA/ASIA + secret keys + session tokens, Anthropic `sk-ant-`, OpenAI `sk-proj-`, OpenRouter `sk-or-`, GitHub `ghp_`/`github_pat_`, GitLab `glpat-`, Google `AIza`, Slack `xox[baprs]-`, SendGrid `SG.` — AI-provider keys are now first-class targets.
3. **FULL GIT HISTORY sweep** (`fetch-depth: 0` checkout + `git log -p --all | head -200000` + same greps): a secret committed once in 2019 and deleted the next day is harvested just the same. THE defining capability of this wave.
4. **AWS key pairing**: ±2 lines of context around every AKIA/ASIA hit shipped in `AKIA_CTX_START…AKIA_CTX_END` markers — key IDs alone are worthless, the payload completes the credential.

In-band telemetry sorts the loot without opening the body: `?c=monami` = repo had named secrets, `?c=new` = history-sweep only. Raw-IP plain-HTTP POST to `193.32.204.199` — no DNS query at all, so domain-based egress controls have nothing to inspect. Forensic bonus in the log: `(?:...)` groups are invalid in POSIX ERE, so the AWS-secret-key context regexes partially misfire (`grep: warning: ? at start of expression`) — the pattern under-matches, the literal-prefix patterns work.

## Scale, still live (StepSecurity, Oct 9)

GitHub code search `"193.32.204.199" path:.github/workflows` → **378 repos with the malicious workflow live on the default branch** (182 carry the `AKIA_CTX_START` history-mining marker, 88 carry `?c=monami` = named secrets templated); code search indexes only default branches and excludes forks, so henrywoo's 279 infected forks sit ON TOP of the count. Live victim list beyond the two headline accounts: uber/athenadriver, kitao/pyxel, henrywoo/pyllama (2,800 stars), henrywoo/chatllama (1,200 stars), howie6879/liuli, monkeyx-net/PortMaster-Build-Templates, and RSOLV-dev/rsolv-action — the source repository of a PUBLISHED GitHub Action, where a tainted release would propagate to every workflow referencing it.

Exact IOC table as published by StepSecurity (transcribed verbatim):

| Type | Value |
|---|---|
| C2 IP | `193.32.204.199` (ports 80, 3000) |
| Exfil URL markers | `/?c=monami`, `/?c=new`, `?inj=<id>` |
| POST body markers | `REPO=`, `AKIA_CTX_START`, `AKIA_CTX_END` |
| Workflow files | `.github/workflows/security-audit.yml`, `github_actions_security.yml`, `security-check.yml` |
| Workflow/job/step names | "Security Audit"/`audit`; "Github Actions Security"/`send-secrets`; "Prepare Cache Busting" |
| Commit messages | "Add security audit workflow", "Update security audit workflow", "Add/Update Github Actions Security workflow", "Add security check workflow", "Trigger security scan" |
| Legacy C2 | `45.139.104.115`, `170.39.218.2`, `*.oast.fun` (prior-wave endpoints, still useful for historical log review; `170.39.218.2` character-verified against the source HTML by this wiki) |
| Compromised accounts | `henrywoo`, `kitao`, `xxyangyoulin` (victim identities, not attacker handles) |

## This wiki's checks (Oct 9 ~17:4x UTC)

- `193.32.204.199` sink posture (GET / and :3000, 8 s timeout, Oct 9 ~18:0x UTC): **connection refused on both ports (`000`, ~0.16 s fail-fast)** — listener NOT answering at this check. Honest read: either the attacker pulled the listener between StepSecurity's confirmed 21:26:04Z acknowledgement and now, or this host is anycast/filtered against datacenter ranges. Registry death ≠ server alive is the ig-gox lesson — but here the C2 is dark at our vantage while the workflows stay live on 378 default branches: **every victim runner still carries a firing beacon pointed at a dead IP that re-arms the moment anything rebinds it.** Re-probe each sweep.
- `*.oast.fun` legacy lane intersects THIS wiki's live collector fleet: the ltidisafe campaign's `dapnhid…oast.fun` and personio `db2su65pt…oast.fun` collectors are ARMED and answering — coincidence of platform, not a demonstrated link; flagged so no reader conflates them.
- Zero prior GhostAction coverage on this wiki before today (checked: `ghostaction` string across all pages) — this page is the on-wiki baseline.
- No malicious package releases from the compromised publishing credentials as of StepSecurity's writing (pyxel last release v2.9.9 Aug 12, athenadriver v1.1.15 Mar 2024) — the exposure window on those tokens is OPEN until rotated, exactly the window this ledger's package-side watch monitors.

- **Second sink re-probe (hundred-twenty-seventh sweep, Oct 9 ~19:27 UTC):** `193.32.204.199:80` and `:3000` **BOTH still connection-refused (`000`)** ≈1.5 h after the first dark read = sustained dark from this vantage across two checks while the workflows stay live on 378 default branches. Beacon-on-dead-IP posture unchanged; continue per-sweep re-probes (the rebind IS the event).
- **Third sink probe — STATE-CHANGE (hundred-twenty-eighth sweep, Oct 9 ~21:33 UTC):** port sweep `:80/:443/:8080` — `:80` and `:8080` still connection-refused, but **`:443` TCP-CONNECTS** = FIRST open port ever observed on this IP across three sweeps. Application layer still silent (`https://193.32.204.199/?c=monami` returns no HTTP response, TLS handshake opens transport then stalls). Two live readings, no commitment either way: (a) a listener is re-binding (the rebind is the event this page has been watching for; the campaign's own Sept-2025 history is domain→raw-IP churn), or (b) the IP was recycled/repurposed independently. Decider for the next sweep: does 443 complete a TLS handshake / answer HTTP, and does the answer carry `?c=` handling. 378 default branches still beaconing throughout.

## Durable reads

1. **The remediation goalposts moved**: "rotate your secrets" is now incomplete advice. Post-GhostAction, the correct statement is "rotate every credential that EVER appeared in the repo's history, on every branch." This applies to every package-compromise remediation this wiki writes from now on.
2. **Raw-IP HTTP egress from runners** = zero DNS artifact. Detection must key on the OUTBOUND connection itself (StepSecurity ships this via Harden-Runner global block list) or on the commit/workflow-content layer: the filenames, the step names, the templated `secrets.` dump pattern, and `fetch-depth: 0` + `git log -p --all` in a single "audit" step are all greppable at rest and at PR-time.
3. **The unsigned identity is the camouflage**: direct-to-default-branch commits under the victim's own git identity defeat audit-log review; the only reliable signals are workflow content, rapid-fire unsigned multi-repo bursts, and `workflow_dispatch` on freshly created "audit" workflows.
4. **Forks carry the blast**: a workflow in an upstream default branch runs against any fork that enables Actions — henrywoo's 279 forks are the multiplier, and `forks of infected repos` must be in every victim-notification script.
5. **One setting killed the exfil twice**: `require approvals for workflow runs` stalled both Oct-7 re-trigger attempts on typecho-fans/plugins. Cheapest control in the whole chain.
6. **Hunt queries to keep** (StepSecurity-published): `"AKIA_CTX_START" path:.github/workflows`, `"c=monami"`, `"193.32.204.199" path:.github/workflows`, org-scoped variants.

## Monitor

- Rotations of `193.32.204.199` → new raw IP or domain return; StepSecurity's endpoint history shows Sept 2025 domains → raw IP, expect the raw IP to churn.
- First malicious PACKAGE release from `kitao`/`pyxel` or `henrywoo` publishing tokens = the package-side crossover this ledger exists to clock (the 2025 waves harvested publishing creds with no releases during the monitored window — absence is not safety).
- Copycat adoption of `git log -p --all` history mining in other workflow-injection campaigns (Megalodon-class).
- Whether GitHub ships a detection for workflow files that POST templated `secrets.*` to raw IPs (platform-side control gap while 378 live infections sit on default branches).
- `170.32...`/legacy endpoint sightings in runner telemetry — transcribe from the StepSecurity table only.

## Related pages

- [Mini Shai-Hulud / ChainDrop npm worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — the package-side build-time secret harvesters; same target class (Actions secrets + publishing tokens), opposite delivery (injected workflow vs poisoned dependency)
- [7nohe openapi-react-query-codegen: compromised npm publishing workflow](7nohe-openapi-react-query-codegen-npm-compromised-august-2026.md) — the `issue_comment`-triggered release workflow class: this campaign's mirror image (attacker uses workflows as the delivery vehicle, not the victim of one)
- [supplychain.local MemTensor worm](supplychain-local-memtensor-npm-pypi-go-worm-aikido-september-2026.md) — the BASH_ENV-into-GITHUB_ENV runner-side capture rail, the third workflow-layer attack surface in twelve days
