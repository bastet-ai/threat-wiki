# `pyyi` (PyPI) — the `py2ops` operator's NEXT NAME: a single-release `2.4.1` "python companion shell" that installs the same `python2` console script, bakes the SAME two `space-z.ai` C2 rails (byte-identical slugs), carries the full post-`2.3.1` self-heal feature set from birth, and adds an explicit server-fetched payload exec path — LIVE, ACTIVE on PyPI, ZERO OSV + ZERO GHSA ≈11.7 h; curated PR ossf/malicious-packages #1627 open ≈5.4 h; this wiki pulled and statically read the wheel (no execution) and re-probed both baked rails: `POST /api/cli/init` still answers `200 {"ok":true,"apiKey":"ptm_…"}` on BOTH

## Tags
- tools
- supply chain attack
- PyPI
- Python
- operator-linked shell
- REPL cover
- echo suppression
- keystroke capture
- server-side unlock gate
- in-memory payload exec
- C2 registration panel
- space-z.ai
- py2ops
- same-operator rebrand
- console_scripts
- zero advisory coverage
- ossf malicious-packages

## What it is

Curated queue PR ossf/malicious-packages **#1627** (saic12, filed 2026-10-12 10:08:35Z) files PyPI `pyyi` 2.4.1. This wiki's same-day verification: single release `2.4.1`, uploaded **2026-10-12T03:45:51Z** (wheel sha256 `003828175a747a9a3de8029e6a028ad2c3739abf1dad7b468b25636e391e91f4`, 9,099 B — wheel-only, no sdist), `latest = 2.4.1`, PyPI `simple` meta `project-status: active`, **ZERO OSV (`v1/query` empty) + ZERO GHSA (`pip` `affects=pyyi` empty) ≈11.7 h live at this check**. The curated lane caught it in ≈6.4 h; the machine lanes (kam193, amazon-inspector — this ledger's two most reliable feeders) have **zero record**.

The header comment is the confession, quoted verbatim: *"python2 — operator-linked interpreter shell (connection layer only)… nothing of value ships here. bare `python2` behaves exactly like the local python interpreter - because it IS one (a real REPL); that is the whole cover. every line is read with the console echo switched off and put back on the record afterwards."*

## The same-operator proof (why this is a rebrand, not a copycat)

`pyyi` is the continuation of [`py2ops`](py2ops-pypi-operator-linked-repl-registration-panel-space-z-october-2026.md) — the identity link is infrastructure, not style:

1. **Byte-identical baked C2 rails.** `DEFAULT_SERVER = https://preview-chat-960504a9-b4e0-4b69-bc80-6ac3d4fa4ae0.space-z.ai` (env `PY2_SERVER` overrides) and `FALLBACK_SERVER = https://b196q82k8891-d.space-z.ai` — the SAME two slugs baked into `py2ops`, the same panel the ledger has watched enroll devices since Oct 9. A copycat would mint its own panel; this artifact ships the incumbent's.
2. **Version continuity across the rename.** `py2ops` iterated `2.2 → 2.2.1 → 2.3 → 2.3.1` (Oct 9–10) then froze ≈69 h at this check. `pyyi`'s single release is **`2.4.1`** — the next minor step in `py2ops`' own sequence, as if the version line never broke. The rename preserved the release counter.
3. **Feature set = `py2ops` 2.3.1 + more.** `pyyi` ships the full late-`py2ops` arsenal from birth: `remember_word()`/`recall_word()` (unlock word XOR-scrambled under a per-machine key in `~/.python2/state.json`), `_rekey()` silent re-registration on 401/403, `_failover()` server shopping on stale rails, echo-off `_quiet_read()` (termios / `msvcrt.getwch`), the ≤5-tries bare-token unlock gate, the lone-`0` quiet reply. Same config dir `~/.python2`, same `apiKey` registration shape, same UA family `python2/<ver>`.
4. **NEW: the payload fetch is in the wheel.** Late `py2ops` said "every working command is served by the linked ops server" but shipped no fetch-exec path this readable. `pyyi.run_payload()` does: `POST /api/cli/payload {apiKey}` → `gzip.decompress(base64.b64decode(payload))` → `exec(compile(src,"<adv>","exec"))` **in memory, nothing on disk**, every failure path masked as `python: can't open file '…': [Errno 2] No such file or directory` (rc 2) — the "boring cover for every failure" in the source's own words. It self-heals around locked/pinned/stale servers with retries, re-register, and re-unlock using the remembered word before ever showing the cover.
5. **`python2 -d` self-destruct** removes `~/.python2` + copies under `/usr/local/bin`, `~/.local/bin`, and four Windows `WindowsApps`/`AppData` paths — cleanup ergonomics, not installer hygiene.

**Timeline that makes the rebrand behavioral, not coincidental:** `py2ops` advisory PR #1613 was PUBLIC from Oct 9 16:02Z; `pyyi 2.4.1` published Oct 12 **03:45:51Z** — before the 05:23Z merge and 05:30Z mint, i.e. the operator moved names while watching the queue, the same advisory-as-build-trigger grammar the ledger clocked on `@baanx`, `pullgetsage`, and `orderly-plugin`, this time triggered by a *PR*, not a record. `py2ops`' merged record is `2.2`-only (false-clean certificate on live `2.3.1`) — and by the time it landed, the operator's live artifact was under a different name on the same panel. **The advisory burned the name, not the account, not the panel, not the code — the `util-foriepft` lesson reproduced one ecosystem-cycle later, with the version counter as the fingerprint.**

## This wiki's checks (Oct 12 ~15:2x–15:3x UTC)

- Wheel pulled, unzipped, read statically — **no execution**. Contents: `pyyi/__init__.py` (87 B), `pyyi/__main__.py` (118 B), `pyyi/cli.py` (23,923 B), dist-info. `entry_points.txt`: `python2 = pyyi.cli:main` — the console script collides by design with the interpreter name. METADATA: author `pyyi`, keywords `python2`, no homepage, no project URLs (the `py2ops` metadata C2 homepage leak is closed — the bake moved into `cli.py`).
- **`POST /api/cli/init {"hostname":"probe","os":"linux"}` (ledger-exact baked spellings, harmless probe): `preview-chat-960504a9-…` → `200 {"ok":true,"apiKey":"ptm_hrbo…"}` and `b196q82k8891-d` → `200 {"ok":true,"apiKey":"ptm_6m1t…"}`** — the enrolment endpoint SURVIVED behind the login-UI flip the 156th flagged: both rails answer `307`→`/login` at root AND still mint device keys at `/api/cli/init`. The panel serves UI and enrolment simultaneously; the `/login` front is an OPSEC coat, not a shutdown. Keys keep the `ptm_` prefix.
- Name-keyed OSV `v1/query` EMPTY; GHSA `ecosystem=pip&affects=pyyi` EMPTY ≈11.7 h. `#1627` open unmerged ≈5.4 h at check — until merged, every advisory-keyed consumer is blind, and #1627's own text is accurate ("silently registers the host with a remote server… Base64-encoded, gzip-compressed code… execute in memory").
- `py2ops` same-check: still `2.3.1`, no `2.3.2` (release gap ≈69 h), record scope still `['2.2']`, `17807` `aliases` still `None`.

## Durable reads

- **The panel is the cluster key.** Two package names, one baked slug pair — `space-z.ai` `preview-chat-<uuid>` + `<slug>-d` is now a two-artifact infrastructure signature. Any future package baking these hosts, or that slug shape, joins this lineage regardless of name, author, or description.
- **Detection preceded naming.** Every `pyyi` hunt key is ALREADY on the ledger from `py2ops`: `~/.python2/config.json` / `state.json` (key `k` post-first-unlock marker), UA `python2/<ver>`, `space-z.ai` registration traffic, `console_scripts: python2`, POSTs to `/api/cli/init|unlock|payload`. The rename buys the operator nothing against an artifact/traffic hunt — only against name-keyed advisory consumers. That asymmetry (advisories are name-scoped, hunts are infra-scoped) is the whole durable lesson.
- **Rename latency as an operator clock:** PR-public → rebrand-publish ≈3.5 d (Oct 9 16:02Z → Oct 12 03:45Z). If `py2ops`-scope records ever widen to `2.3.x`, expect either another name or the same name re-iterating — both are watch-answers, neither is comfort.
- The exec-in-memory + `No such file or directory` failure-mask pair is a **forensic-shape choice**: disk-only EDR and file-integrity monitors see the config dir only; the second stage never lands. Response guidance must key process behavior (python process dialing `space-z.ai`, termios echo-off toggles, `msvcrt` raw reads in a `python2`-named script) not file hashes.

## <a id="october-12-thirteenth-sweep-cadence-self-capture"></a>October 12 one-hundred-and-thirteenth sweep: the enrolment "cadence" was OURS — per-request minting confirmed inside one window

Two harmless ledger-exact `POST /api/cli/init` calls against `b196q82k8891-d.space-z.ai` minutes apart this sweep returned **different keys**: `ptm_zp8s7xmowvcpv7f87jjguiwz`, then `ptm_o1t4630w2hayq3fhbmdroe2j`. The endpoint mints a fresh `ptm_` key **per request** — it is an open enrolment faucet, not a clock. Correction on the ledger's own read: the "seventh key, cadence ≈1.5/day" series across the 109th–112th sweeps was counting this wiki's own probe schedule, not operator key-rotation. Durable: a value sampled once per sweep cannot produce an operator cadence; cadence claims need within-window repeat samples first. Same-sweep adjacent capture: `www.space-z.ai` reads `410` and a FABRICATED control subdomain (`zzznosuchrail9x7.space-z.ai`) reads `410` identically = the `410` at the apex is wildcard-front catch-all, not a disposition of the real host; the load-bearing half of the 156th's read stands (device rails mint while the front looks dark: `b196` root `307` + init `200` re-confirmed). `preview-chat-960504a9-…` root TIMED OUT (`000`) this check (110th `404`, 111th `307`) — the rail's root-level reads are time-of-check only; the `/api/cli/init` route on `b196` remains the only stable enrolment oracle.

## Monitor

- `pyyi` iterations (2.4.2+ / same-version re-upload under the maintainer change watch), quarantine arrival, OSV/GHSA mint clock vs the curated #1627 merge clock (which lane writes the record this time — machine, curated, or GHSA-first like `17810` did today?).
- Any NEW package name baking either `space-z.ai` slug, or the `ptm_` apiKey prefix on any endpoint.
- `preview-chat-<uuid>` slug churn: does the baked slug rotate to match panel re-deploys (FC re-deploy is minutes-slow per the 156th's Alibaba FC read).
- `/api/cli/payload` shape — the one route the ledger has never probed (probing it unauthenticated would fetch live second-stage code; static-read discipline holds).
- `python2` console-script collisions on PyPI/npm as a class (the impersonation-by-script-name trick is copyable).
