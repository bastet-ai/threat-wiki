# supplychain.local: a novel cross-ecosystem Go worm published into MemTensor's MemOS agent-memory ecosystem (npm `@memtensor/memos-cloud-openclaw-plugin` + PyPI `MemoryOS`), carrying a secret-stealing regex, direct registry re-publishing, and a GitHub Actions push-trigger self-propagation template — both packages LIVE as `latest` with ZERO OSV and ZERO GHSA at this wiki's check (Sep 23, 2026)

## Tags
- ops
- supply-chain
- worm
- go
- npm
- pypi
- github-actions
- memtensor
- memos
- openclaw
- ai-agent-supply-chain
- secret-stealing
- cross-ecosystem
- skyleen.fr
- sckit
- self-propagation
- aikido
- zero-ghsa
- live-packages

## Summary

Aikido Security Research published on **September 23, 2026 (~07:41 UTC)** that a **novel supply-chain worm** — tracked by Aikido as **`supplychain.local`** after the threat actor's own Go module name — was published the same day into **MemTensor's MemOS ecosystem** in two ecosystems at once:

| Ecosystem | Package | Malicious versions | State at this wiki's check (~09:30–10:10 UTC Sep 23) |
| --- | --- | --- | --- |
| npm | `@memtensor/memos-cloud-openclaw-plugin` | `>=0.1.21` (0.1.21, 0.1.23, 0.1.25 carry the payload; 0.1.22/0.1.24 are clean alternates) | **LIVE, `latest` = 0.1.25 (malicious)** |
| PyPI | `MemoryOS` | `>=2.0.34` | **LIVE, `latest` = 2.0.34 (malicious)** |

Both accounts have **substantial benign publishing history** and appear **compromised** (Aikido's preliminary assessment, which this wiki's registry forensics corroborates). The worm is a **multi-platform Go binary** with functionality to **self-propagate through other packages via direct npm/PyPI publishing and via compromised GitHub Actions**.

**Zero OSV records and zero GHSA advisories existed for either package at this wiki's check** — the packages sit on `latest` in both registries with the public advisory pipeline entirely silent. This is the highest-stakes window the intake pipeline has ever shown on this wiki: a live, `latest`-tagged, cross-ecosystem worm in an **AI-agent memory stack** with no machine-readable signal yet.

## This wiki's independent verification (all live pulls, this sweep)

- **All six `sckit` binaries in the live npm tarball SHA-256-match Aikido's published IoC set exactly** — the wiki's pulls of `0.1.23` reproduce `65faf8cc…32c31` (darwin-amd64), `f8ccdd1d…53fce` (darwin-arm64), `381ac6dc…2cc18` (linux-amd64), `e077c387…44b26` (linux-arm64), `56cd3416…8f14be` (windows-amd64), `d6b3e77c…b38a26` (windows-arm64). The IoCs are confirmed against registry-served bytes, not a report.
- **The Go module path is embedded in every binary**: `strings` shows `mod supplychain.local/campaign` and symbols `supplychain.local/campaign/cmd/implant`, `/internal/wire.Marshal`, `/internal/wire.SealBound`, `/internal/wire.GenerateX25519`, `/internal/wire.Signed.Verify`, `/internal/wire.ParseManifest`, `/internal/presentation.Resolve` — a clean compiled Go project with an **X25519 + AEAD sealed-envelope wire protocol and signed-manifest parsing** (tasking that is authenticated, not just encrypted).
- **The loader is wired into genuine product code, not an install hook.** In `0.1.23`, `package/lib/sckit.js` exports `launchStageZero()`, called from `index.js` in two places: at **gateway runtime startup** (`if (isGatewayRuntimeStartup()) launchStageZero();`) and **on every agent user-prompt in the recall hook** (`launchStageZero(userPrompt)` — fired BEFORE the plugin's own recall logic). The plugin is a lifecycle hook in an agent gateway, so **every conversation through a host running it passes the victim's prompt text to the implant as `SCKIT_EVENT_TEXT`**. No `postinstall`, no `npm install` execution — `npm install` is clean and inert; execution needs the package to be *used* (Aikido concurs: "executes on any invocation… does not appear to attempt to execute at install time"). This is the post-npm-12 runtime-loader class, aimed at exactly the AI-agent plugin surface this wiki has been tracking.
- **The config blob decoded from the live tarball** (base64 `--config64` argument, identical in 0.1.23 and 0.1.25):
  - `campaign_id: cloud-openclaw-semi-nuclear`, `product: cloud-openclaw`, `profile: semi-nuclear`
  - `channel: "exact-ref-one-use-NPM_TOKEN,@memtensor/memos-cloud-openclaw-plugin"` — the channel string names the credential the stage-0 run is fed: `collectStageZero()` deliberately passes `NPM_TOKEN: process.env.NPM_TOKEN || process.env.NODE_AUTH_TOKEN` into the child environment = **the loader hands the victim's live npm publishing token to the implant at every invocation**.
  - `root_public: 9Nh4ESrIQgorJMDr58sBII7Y9B7fjrHFmNhWPqphUns` (Ed25519-style root key for manifest verification), `stage0_digest: dZjBrB1q7fG9Qaw5YDEfcbFT7ibQooRuNHjdauzcJgs` (self-verification of the binary)
  - `state_dir: $HOME/.openclaw/.cache/runtime`, `inventory_roots: ["$HOME"]` — the whole home directory is the inventory surface
  - Three `fronts` (per-front unique 24-hex path prefix, `config`/`status`/`batch` endpoints) on `8a8acaf167b3.skyleen.fr`, `0b48fafd6fbe.skyleen.fr`, `266297c6df27.skyleen.fr`; Aikido's IoCs add `c747d139e7e9`, `73376a079d87`, `d4f77a3a8cb0` subdomains and origin IP `139.84.223.178`
  - `not_after: 1792714982` = **2026-10-23 00:23 UTC** — a built-in kill date, one month out.
- **`skyleen.fr` DNS has gone to null since Aikido's publication**: at this wiki's check **ALL subdomains resolve (via local resolver AND Google DoH) to `127.0.0.1`** — including random-test wildcards — and the apex has no A record (MX = ProtonMail). Aikido reported live resolution to `139.84.223.178`. `*.skyleen.fr` resolving to loopback is either an actor-side null-route or a registrar/hosting sinkhole; **the wildcard-to-127.0.0.1 pattern is itself now the detection artifact** — no real C2 answers at those URLs anymore (HTTPS connections fail). If the C2 is being re-pointed, monitor for the fronts re-resolving to non-loopback IPs.
- **Clean-version alternation**: registry `time` blocks show 0.1.21 (02:23 UTC) → 0.1.22 (03:45) → 0.1.23 (03:49) → 0.1.24 (04:33) → 0.1.25 (04:36), a ~2-hour publish sprint with malicious/clean pairs, and **pre-existing dist-tags `clean-inverse-0-1-23` → 0.1.22 and `clean-inverse-0-1-25` → 0.1.24**. Those tags are either maintainer remediation bookkeeping or actor-side staging artifacts — their provenance is unknown at capture, but they are the cleanest registry-level tell in the document: read them as "someone is marking which versions are clean," which implies someone knows which are not.
- **Scope sweep (this wiki)**: of eight `@memtensor/*` packages plus the third-party mirror `@steven-stack-s/dsh-memos-local`, **only `memos-cloud-openclaw-plugin` carries `.sckit`** at `latest` — the compromise is one package, not the scope. On PyPI, `MemoryOS` 2.0.32/2.0.33 are clean and **2.0.34 jumps from ~1 MB to 19 MB** (both wheel and sdist) — the size delta alone is a hunting heuristic.
- **PyPI artifact detail Aikido's post doesn't include**: the MemoryOS 2.0.34 sdist carries the same six `.sckit` binaries under `memos/.sckit/` plus **two Python loaders**: `memos/_stage0.py` (locates the platform binary and `Popen(..., start_new_session=True)`) and `memos/_initial_ci_delivery.py` — a **wire-protocol CI delivery client** (indexed/selector domains `sckit/initial-ci/delivery-index/v2`, `SCKIT_CI_RESULT_V2` base64 wire payloads, `execution_context_sha256`, `runner_nonce`, a `SCKIT_CI_OBSERVATION_V2` stdout protocol) = the same worm is designed to run **inside CI** and pull its second stage through the sealed wire, not just beacon.
- **Zero OSV, zero GHSA** for both packages at check (OSV query returns `{}` for both names; GHSA anonymous search endpoint unavailable — OSV is the authoritative negative).

## What the worm does (Aikido, full text captured by this wiki)

1. **Stage 0** executes the platform `sckit` binary with `stage0 --config64 <blob>`, detached, stdio ignored; writes state to `state_dir`.
2. **Secret hunting**: a compiled Go regex sweeps for generic JWTs (`eyJ…`), AWS access keys (`AKIA/ASIA…`), GitHub tokens (`github_pat_`, `gh[opusr]_`), GitLab (`glpat-`), **npm tokens (`npm_…`)**, **PyPI tokens (`pypi-…`)**, Hugging Face (`hf_`), Vault (`hvs.`), Slack (`xox*`), Stripe live keys (`sk_live_`), SendGrid (`SG.`), plus a broad secret/keyword context regex covering DB/Redis/Mongo/AMQP connection URIs — and reads publishing-credential environment variables.
3. **Self-propagation, three rails**: (a) **direct re-publishing** via `npm publish` + `npm version patch` and `twine upload` using stolen registry tokens; (b) a **GitHub Actions workflow template** embedded in the binary — `on: [push]`, checkout@v6, then `./<dir>/linux-amd64/sckit stage0 --config64 <blob>` = any pushed-to compromised repo re-executes the worm on every future push, on GitHub's runners; (c) **drop-in loader stubs** — a JS stub written to `bootstrap.cjs` and wired as a `postinstall` script, and a Python stub, for implanting into other repositories/packages on the infected host. (Aikido: no compromised public workflow files or repositories containing the stubs had been identified at publication — the rails are armed, not yet observed firing.)
4. **C2**: three-front HTTPS with per-front unique path prefixes and config/status/batch endpoints; wire protocol is X25519 + AEAD with signed manifests (verified above from symbol names), so tasking authenticity is enforced at the protocol layer.

## Why this is above the bar (analysis)

- **Target class**: MemOS/MemTensor is an **AI-agent memory layer** (MemOS = "Memory Operating System"; the plugin is an OpenClaw lifecycle hook). Its users are precisely the population running authenticated agent gateways with `NPM_TOKEN` in the environment, GitHub credentials on the workstation, and home-directory-wide agent state. The worm was published *into an agent runtime's plugin path* and is fed the user's prompts. This is the same thesis as the on-wiki `my-company-device` entry (agent-dispatch-as-payload) but industrialized: a worm, not a single package.
- **The `channel` field names the credential**: `exact-ref-one-use-NPM_TOKEN` is the first on-wiki sample where the operator's config field tells you, in their own vocabulary, exactly which stolen credential the stage exists to consume.
- **Pipeline silence**: zero OSV/GHSA for a live `latest` cross-ecosystem worm with six confirmed binary hashes — the sixth-plus confirmation on this wiki that GHSA/OSV-keyed consumers must not be the only detection path; vendor malware feeds (Aikido Intel's own feed caught this same-day) and `latest`-tag size deltas are doing the actual catching.
- **Family positioning**: cross-ecosystem worms with Actions-propagation belong beside the on-wiki **Mini Shai-Hulud** worm class and the **SANDWORM_MODE** AI-toolchain worm, and the runtime-loader/post-npm-12 migration class (`indexed-btree`, Graphalgo). The sealed/signed wire + signed-manifest + kill-date + per-front path-prefix design is closer to ChainDrop/Equation-of-Compromise sophistication than to the beacon-fleet clusters this wiki's daily sweeps track.

## Hunt and disposition

- **Immediate**: any host that installed `@memtensor/memos-cloud-openclaw-plugin` ≥0.1.21 or `MemoryOS` 2.0.34 = treat as compromised at agent-gateway privilege level. Remove the package, then **rotate every credential in the regex set from that host** (npm, PyPI, GitHub, GitLab, HF, Vault, Slack, Stripe, SendGrid, AWS, JWTs, DB URIs) — the stealing regex is the rotation checklist. Check for `$HOME/.openclaw/.cache/runtime` (or the config's `state_dir`) and `_stage0.py` / `_initial_ci_delivery.py` / `bootstrap.cjs` postinstall artifacts in other repos.
- **Network**: DNS/proxy logs for ANY `*.skyleen.fr` query — the wildcard now answers 127.0.0.1, so historical resolution to `139.84.223.178` (or any non-loopback address) marks infections; HTTPS to any `skyleen.fr` subdomain with a 24-hex path prefix.
- **Registry**: any new `@memtensor/*` version carrying `.sckit/`; any PyPI `memoryos` release whose size jumps ~1 MB → 19 MB class; any package whose tarball contains a hidden `.sckit/` directory or a `sckit`/`stage0`/`--config64` string; any npm/PyPI publish from a workstation with the worm present (the direct re-publish rail will look like a maintainer's own account).
- **GitHub**: workflow files containing `on: [push]` + a `sckit stage0 --config64` run step; unexpected `bootstrap.cjs` appearing as a postinstall entry in `package.json` diffs.
- **Takedown posture**: both packages still LIVE at check; monitor OSV/GHSA for the advisory wave (first sighting cadence will be informative given both finders have had hours), npm/PyPI holder actions, and whether the `clean-inverse-*` dist-tags become `0.0.1-security` holders (npm's neutralization signature).

## Watch

- OSV/GHSA advisories for the two names (absent at check — expect arrival; record the lag).
- npm/PyPI takedown or holder state of both packages; whether `latest` is moved to a clean version.
- Additional `supplychain.local` artifacts: other packages carrying `.sckit`, `sckit.initial-ci-delivery-index.v2` strings, or the `9Nh4ESrIQgor…` root key; other campaigns reusing `semi-nuclear` profile naming.
- `skyleen.fr` front re-resolution (C2 resurrection), and any second domain.
- Whether the GitHub Actions push-trigger rail fires anywhere in public (Aikido found none fired yet — a compromised public repo suddenly running a `sckit stage0` workflow would be the first ITW observation).
- MemTensor's own disclosure/disposition (account compromise confirmation, republish of clean versions).
- `not_after` 2026-10-23: absence of beacon activity after that date is by design, not remediation.

## Sources

- Aikido Security Research, "Novel supplychain.local Go worm appears" (Oliver Smith), Sep 23, 2026 — <https://www.aikido.dev/blog/supplychain-local-memtensor-npm-pypi> (full text captured by this wiki; IoC set embedded in post)
- This wiki (Sep 23, 2026, ~09:30–10:15 UTC): npm registry documents + tarball pulls (0.1.21–0.1.25); loader read (`lib/sckit.js`, `index.js` call sites); config blob base64 decode; `strings` verification of Go module path + wire-protocol symbols; SHA-256 of all six binaries vs Aikido IoCs (all six match); scope sweep of eight `@memtensor/*` packages + mirror scope; PyPI `MemoryOS` JSON + 2.0.34 sdist read (six `.sckit` binaries + `_stage0.py` + `_initial_ci_delivery.py`), 2.0.32/2.0.33 verified clean; OSV queries (empty); DoH + local resolution of all six `skyleen.fr` fronts (all `127.0.0.1`, apex no A record)
