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

## October 15 one-hundred-and-thirty-sixth sweep: `2.4.2` published ≈17 h BEHIND THE MERGED ADVISORY, ZERO RECORDS, AND THE WHEEL-DIFF IS A C2 TENANCY MIGRATION

`pyyi 2.4.2` published `2026-10-14T17:16:43Z` — `≈17 h` AFTER curated PR `#1627` MERGED (`00:03:13Z` Oct 14) and after OSV `MAL-2026-17866` went live — with **zero OSV and zero GHSA coverage on `2.4.2`** at check (`affects=pyyi` = `0`, `17866` scope still `['2.4.1']`). This is the post-advisory out-of-scope iteration class in its sharpest observed form: unlike the `@myorder-frontend-commons` (112th) or `npp-ml` cases, the advisory here is neither queue-stale nor scope-drifting — the merged record is CORRECT for `2.4.1`, and the code simply moved past it. Advisory-keyed consumers are blind to the live rung no matter which lane writes the record. The infra-scoped hunt (baked `space-z.ai` slug pair, `ptm_` key prefix, `/api/cli/*` routes) is the only consumer class that covers the iteration.

**Wheel-diff (both wheels pulled, unzipped, diffed statically — no execution; 45 changed lines):**
- `DEFAULT_SERVER` RE-BAKED from `https://preview-chat-960504a9-b4e0-4b69-bc80-6ac3d4fa4ae0.space-z.ai` to `https://b196q82k8891-d.space-z.ai` (`FALLBACK_SERVER` unchanged — both defaults now converge on `b196`). This directly answers this page's own monitor question: YES, the baked `preview-chat-<uuid>` slug rotated with the panel re-deploy.
- New functions `_homed()` + `_home_stale_pin()`: **silent victim re-pinning.** Any installed host whose `~/.python2/config.json` pins a stale server re-registers against the baked servers and re-pins ONLY if registration succeeds AND the remembered unlock word still unlocks the new home; the stale pin is kept on any failure ("nothing breaks, nothing is asked twice" — operator's own comment; new device rows arrive `vip`; pushes to a stale pin "land in a database the operator's answering surface can never see"). That is a C2 tenancy-migration tool shipped as a point release: the operator moved panels and needed existing implants to follow invisibly.
- `VERSION` bump; `run_payload` fetch-exec path byte-for-byte identical (`exec(compile(...))` still at `cli.py:640`); `PY2_SERVER` env override unchanged.
- Artifact: `pyyi-2.4.2-py3-none-any.whl` 9,498 B, `sha256 6248e67aa2d1755c9844f299f71948904eaa92fd4bfea324a4ef3ac938603fec` vs `2.4.1` 9,099 B `00382817…`.

**Registry state at check (~03:3x UTC Oct 15):** both `2.4.1` and `2.4.2` served, NOT yanked, PyPI NOT quarantined `≈41.5 h` post-OSV — slower than the `npp-ml` `≈25 h 20 m` bound that already closed on this ledger = pyyi is now the slowest advise-to-action clock measured here. `#1627` merged; GHSA mirror still absent (OSV-only since birth, `17866` `aliases: None`).

**Durable addition:** a point release can be *infrastructure* churn, not feature churn — when a malicious package's version bump diffs to server-bake rotation + pin-migration logic, the operator's panel moved and every installed host is being herded to the new one. Diffing consecutive wheels of an advised name is a free read on the C2's lifecycle; do it before the next version lands, while both artifacts are still on the index.

## <a id="october-15-one-hundred-and-thirty-seventh-sweep-osv-blesses-the-cluster-key-seapy-ops-carries-both-rails"></a>October 15 one-hundred-and-thirty-seventh sweep follow-up: `MAL-2026-17880` (`seapy-ops`) BAKES BOTH RAILS INTO AN OSV — THE CLUSTER KEY IS NOW ADVISORY-GRADE

The curated queue drained at `04:02:07Z` (`#1636` merged) and `seapy-ops` got `MAL-2026-17880` (npm lane n/a; PyPI, scope `1.0.0`–`1.1.2`+`1.2.1`+`1.2.2`). Its `database_specific.iocs.domains` list names **`preview-chat-960504a9-b4e0-4b69-bc80-6ac3d4fa4ae0.space-z.ai` AND `b196q82k8891-d.space-z.ai`** — the exact pair this page treats as the operator's cluster key, including the `b196` slug that this wiki first read off the `pyyi 2.4.2` wheel-diff ~6 h earlier (`Oct 15` 136th sweep). Independent confirmation from a second package: (1) the same operator runs at least three names (`py2ops` → `pyyi` → `seapy-ops`); (2) the `seapy-ops` advisory text independently describes the same grammar family (unlock-gated collection/upload; a REPL mode that ships single-token input to the unlock endpoint and executes a fetched `Base64/gzip` payload IN MEMORY, disguised as `FileNotFoundError`); (3) hunt-string value: the two slugs are now queryable inside OSV `IoCs`, not just off this wiki's page.

Two fleet-relevant reads at check: `seapy-ops` was **advised and NOT quarantined** (`project-status` active, JSON `200`, latest `1.2.2` serving) — the pyyi slow-class non-action reproduces on the operator's third name, supporting the lane-level-coverage read over per-name oversight; and the advisory's scope **misses live rung `1.2.0`** (present on the simple index, absent from the enumerated list) = the post-/pre-advisory out-of-scope rung class on this operator too. GHSA mirror still absent at `≈2 h` post-birth (`affects=seapy-ops&ecosystem=pip` = `[]`) — until it mints, GHSA-keyed quarantine automation (the ledger's established quarantine trigger) sees nothing. Full sweep record: [137th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-thirty-seventh-sweep).

## <a id="october-15-one-hundred-and-thirty-eighth-sweep-the-lane-level-non-enforcement-read-gets-its-mechanistic-proof"></a>October 15 one-hundred-and-thirty-eighth sweep follow-up: The Lane-Level Non-Enforcement Read Gets Its Mechanistic Proof — The `06:30:33Z` Mirror Wave Fired ZERO Seizures

`seapy-ops`'s GHSA mirror `GHSA-5j6r-jv3q-c93f` minted `2026-10-15T06:30:33Z` (same second as the `util-foriepft` + `@flexmr/ui` mirrors — the bot batches curated imports), and `GHSA-5j6r` inherits the OSV's scope gap verbatim: eight rungs `1.0.0`–`1.1.2`+`1.2.1`+`1.2.2`, live `1.2.0` absent on BOTH advisory surfaces. One hour after the mint: `seapy-ops` PyPI NOT quarantined (`project-status` absent, `latest 1.2.2` serving, simple index `15` links), `util-foriepft` serving with no security-holder recreate, `pyyi` still `latest 2.4.2` unquarantined `≈45 h` post-OSV. The ledger's established GHSA-mint→seizure interlock (`+57 s`/`+78 s`/`+123 s` on the August names and the Oct-14 costume) demonstrably did NOT fire on curated-born names. This page's slowest-advise-to-action clock is therefore not an oversight story: the automation that seizes machine-lane names simply has no path to this operator's names — `py2ops`/`pyyi`/`seapy-ops` sit in the lane where neither alias-join consumers nor mint-interlock automation can ever see them. Enforcement here requires a human/abuse action, which makes the infra-scoped hunt (baked `space-z.ai` slug pair) the only reliable defense for installed hosts. Full sweep record: [138th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-thirty-eighth-sweep).
