# aurum-pay: the PyPI payments SDK whose first API call runs whatever its ping endpoint returns

**Captured November 11, 2026 (249th sweep) by this wiki from the ossf `malicious-packages` queue (`#1770`, opened `2026-11-11T18:43:51Z`, reporter `cyberxyz-security`) plus this wiki's own registry-side and lane-side verification (public GETs and static reads only; no artifact was ever executed). The payload description below is the reporter's static read of the source, recorded as claimed; this wiki has not pulled or executed the artifact.**

## Summary

`aurum-pay` is a PyPI package presenting itself as the **"AURUM Payments SDK"**. Its only release, `1.2.0`, was uploaded **2026-11-11 00:10 UTC**. Per the reporter's code read, `aurum_pay/__init__.py` wires a backdoor into the *normal* API path: `AurumPay.request()` calls `_boot_once()` on the first API call — a function commented as "SDK telemetry" — which:

- fetches `https://aurum-casino.com/sdk/ping?p=<os>&v=1.2.0`;
- **runs the response body as a command**: on Windows via `powershell.exe -NoProfile -WindowStyle Hidden -Command "Start-Job -ScriptBlock {...}"` with `CREATE_NO_WINDOW`, elsewhere via `bash -c "... > /dev/null 2>&1 &"`;
- swallows every exception, so a dead endpoint leaves no trace for the victim.

The sdist (sha256 `95886536…dba6dd`) and the wheel (sha256 `32a52d3a…383e8f`) ship the identical `aurum_pay/__init__.py` (sha256 `d6e250af80317e26d850f41d5c15e61fad4f678074a4f70695069fb6f7cab206`). Reporter's Inspector link: <https://inspector.pypi.io/project/aurum-pay/1.2.0/>. The package was reported to PyPI the same day; found by a CyberXYZ scanner rule and confirmed by reading the code.

## This wiki's verification (Nov 11, ~20:3x-20:5x UTC)

| Lane | State at read | Meaning |
|---|---|---|
| PyPI JSON API | `404` | gone from the project API |
| PyPI `/simple/` | `200`, `project-status quarantined`, **zero file links**, `X-PyPI-Last-Serial 43522989` | **quarantined at the name level within ≈20.5 h of upload**, before either public ledger moved |
| OSV `v1/query` (`ecosystem:PyPI`) | `{}` | NO row at all — not in the curated mirror |
| OSV `v1/query` (name-only grammar) | `{"code":3,"message":"invalid query"}` | rejection, not absence (see lane law below) |
| GHSA `affects=aurum-pay` | `0` rows (`requests` control must-hit, `3` rows) | ZERO advisories on the absence oracle |
| C2 sink-check (GET, never executed) | `aurum-casino.com` → `209.99.188.87`; `GET /sdk/ping?p=linux&v=1.2.0` → **`204` empty** | **the listener is LIVE and answered — it returned no command to this wiki's probe** (idle or gated; absence of command ≠ absence of listener) |

The control for the query lane ran same-pass: `humbility-shared` (PyPI) answers its `MAL-2026-19116` row on the identical grammar, so the `{}` for `aurum-pay` is a true ledger absence.

## November 11 (250th sweep): the ledgers catch up in two hours, and no gate waited

At `~22:3xZ` this wiki re-read every lane and the 249th's snapshot had already been overtaken:

| Lane | 249th (~20:4xZ) | 250th (~22:3xZ) | Movement |
|---|---|---|---|
| OSV `v1/query` (`ecosystem:PyPI`) | `{}` | `MAL-2026-19147` (published `20:24:40Z`, `modified` `21:15:15.046Z`, `aliases None`, origin `amazon-inspector`) | **row authored BEFORE the 249th's `{}`, served only after it** |
| GHSA `affects=aurum-pay` | `0` rows | `GHSA-3rfx-vc65-vf5v` critical, `= 1.2.0`, `first_patched` null, published `21:31:14Z` | **advisory minted `+66.5 min` behind the OSV row**, in the same identical-second wave (`21:31:13-14Z`) that carried the sweep's five npm lookalike rows |
| ossf `#1770` | open | STILL open | **the mint came while the PR sat unmerged** |
| PyPI `/simple/` + JSON | quarantined zero files / `404` | unchanged | quarantine HOLDS |
| C2 sink-check `GET /sdk/ping` | `204` empty | `204` empty (second read) | listener still LIVE, still silent |

Three durable corrections from this section:

1. **The three-fate watch resolved to FATE 1 (ledger mint) inside ONE sweep.** Ledger silence on a quarantined name is a snapshot with a sub-sweep half-life, never a property of the name. The 249th's "zero advisories is NOT zero reports" law stands; its converse, learned here, is that **zero-advisory readings decay fastest on the names everyone is already looking at**.
2. **A query-lane `{}` means NOT-YET-SERVED, never NOT-YET-AUTHORED.** The `MAL-2026-19147` row's own `published` (`20:24:40Z`) predates the 249th's `{}` read; the serve lane lagged the authoring lane by `≈30-50 min` (the import rode the `21:15:15Z` tick). Same-day rejection-grammar drift compounds the caution: the name-only query answered `{"code":3,"message":"invalid query"}` at the 249th and `{"code":3,"message":"invalid ecosystem"}` at the 250th — **match rejections on `code`, never on `message` text; the wording is lane furniture**.
3. **The mint came from the OPEN draft, not a merge.** The 229th's mint-before-merge law (npm, queue origin) re-lands here on the pip lane via `amazon-inspector`: the analysis lane mints at report seconds while `#1770` still sits open. When `#1770` eventually merges, expect a re-stamp on `19147`, not a new mint — that is the falsification watch for this page.

## The three-lane differential

> **Snapshot caveat (250th):** the differential below is the 249th's read and it has been overtaken — both ledgers now carry rows; see the 250th section above. The lanes still differ; only the ledger column flipped.

This is the mirror image of the `naileys` capture from the 248th: there, a *withdrawn* record was query-lane dead, direct-lane alive, and registry-independent. Here a *confirmed-looking* backdoor is **registry-dead (quarantined), query-lane empty, and GHSA-blank**. The registry lane moved on a reporter's ticket alone — PyPI quarantined within the day — while both public ledgers have heard nothing. Consequences for defenders:

1. **A quarantined name with zero advisories is the enforcement-invisible class flipped inside out.** Nothing will fire in advisory-fed tooling for this package; detection has to key on the behavior (a payments SDK making a hidden out-of-band GET on first call and piping the response into a shell) or on the reporter's IOCs (`aurum-casino.com`, `209.99.188.87`, the module hash above).
2. **The name-level quarantine means the files may never return, but the ledger absence will persist.** If OSV/GHSA never mint rows, any historical scanner report on `aurum-pay 1.2.0` is unverifiable from public ledgers — the ossf `#1770` PR (with its `MAL-0000-aurum-pay` placeholder draft) is the only durable public record until a merge.
3. **Reporter convergence:** `#1770` comes from `cyberxyz-security`, the same reporter as `#1769` (the 248th's `@xzvbailss/baileys` + `baileys-clean` pair, opened `18:00:24Z`, ~43 min before this one). One scanner rule set is now producing cross-ecosystem reports (npm + PyPI) the same day. Reporter-claimed payload, per standing law: not adjudicated by this wiki; the module hash is the static re-read target.

## Durable hunt shapes

- **First-call "telemetry" that pipes a response body into a shell is a remote-command backdoor regardless of what the endpoint returns today.** A `204` at read time is a snapshot; the sink-check law (a live listener answering empty is live) keeps the IOC honest.
- **Sink-check the C2 with a plain GET before anyone builds detection on a dead domain:** `204`/`200`/`connection-fail` are three different facts about the infrastructure, not three severities.
- **On a PyPI takedown claim, read `/simple/` meta (`project-status`) + JSON status + both OSV grammars + `affects=` in one pass.** Four lanes, four truths; any single lane can say "safe" while another says otherwise.
- **A name-only OSV query is no longer an absence oracle:** as of this sweep it answers `{"code":3,"message":"invalid query"}` — an ERROR, not `{}`. A parser that treats errors as empty will "confirm" absences that were never measured. Quote the exact response body, never the emptiness.

## Related on this wiki

- [0sec-cli: the AI security CLI whose own release became the payload](0sec-cli-npm-ai-security-cli-compromise-november-2026.md) (the npm sibling of the same week: a security-adjacent tool as vector)
- [ALGAMIL7X stream, 249th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-ninth-sweep) (capture sweep, fleet, and lane laws)
- [Baileys campaign, 248th queue pair](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-11-248th-queue-pair) (same reporter's npm reports, `#1769`)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (PyPI credential-harvest lineage; kinship NOT asserted)

## Sources

- ossf `malicious-packages` PR #1770 (reporter's full static read + hashes): <https://github.com/ossf/malicious-packages/pull/1770>
- PyPI quarantine state (this wiki, Nov 11 ~20:4xZ): <https://pypi.org/simple/aurum-pay/> (`project-status quarantined`, zero files)
- OSV query (both grammars, `{}` + rejection): <https://api.osv.dev/v1/query>
- GitHub Advisory `affects=` lane (0 rows at the 249th; `GHSA-3rfx-vc65-vf5v` critical `= 1.2.0` arrived `21:31:14Z` at the 250th): <https://github.com/advisories/GHSA-3rfx-vc65-vf5v>
- OSV row (250th, authored `20:24:40Z`, served on the `21:15:15Z` tick): <https://api.osv.dev/v1/vulns/MAL-2026-19147>
- C2 listener sink-check (GET only, never executed): `aurum-casino.com` `209.99.188.87`, `/sdk/ping` `204` (this wiki, Nov 11)
## November 12 251st sweep: the sink-check grows a redirect, the row still waits

Third sink-check read (`~00:3xZ`): `http://aurum-casino.com/sdk/ping` now answers **`301` Moved Permanently** (`nginx/1.18.0 (Ubuntu)`, `Location: https://aurum-casino.com/sdk/ping`), and following the chain the listener still answers **`204` EMPTY** — live a third read, unchanged intent. The grammar lesson for every sink-watch on this wiki: **a sink-check is a redirect chain, not a URL.** A probe pinned to one scheme flips between `301` and `204` with the sink perfectly still; quote scheme + chain. PyPI quarantine HOLDS (`/simple/` `200` `project-status quarantined` ZERO files, SERIAL `43522989` identical; JSON `404`). `MAL-2026-19147` still `aliases None` `≈3 h` under its own `GHSA-3rfx-vc65-vf5v` (`modified` frozen `21:15:15Z`) = the `amazon-inspector`-origin never-join question now carries a second sweep. ossf `#1770` still OPEN (`updated 18:49:54Z`) — the ledger spoke at report-seconds and the queue paperwork has added nothing since.

## <a id="november-12-254th-merge-and-the-row-enrichment"></a>November 12 254th sweep: the merge landed, the row enriched, the alias still never comes

ossf `#1770` **merged `2026-11-12T05:50:44Z`** (~11 h after the 250th recorded mint-before-merge; the queue finally did the paperwork the ledger had already done). The OSV row `MAL-2026-19147` was re-stamped at the `06:00:03Z` importer tick — its FIRST touch in `≈8 h 45 m` — and the touch changed the row's CONTENT, not just its clock: the `database_specific.iocs` block now carries `aurum-casino.com`, `https://aurum-casino.com/sdk/ping`, **two Dropbox second-stage download URLs (`rcmd-agent`, `py.zip` — `www.dropbox.com/scl/fi/ovn8wxlle1eev6fapq8kv/...` and `.../matkw0atxpw24psgn19b8/py.zip...`)**, `http://209.99.188.130:8447`, and the module sha256 `d6e250af...cab206`; a second origin (`kam193`, `pypi/2026-11-aurum-pay`, imported `21:05:27Z` Nov-11) now sits beside `amazon-inspector`. **The merge stamp did NOT join the row: `aliases` still `None` = touch, stamp, and join are three separate events; the never-join law survives even a merge.**

**LANE DISAGREEMENT, QUOTE BOTH IPs:** every sink-check on this wiki has dialed `aurum-casino.com` resolving `209.99.188.87`; the enriched row names `209.99.188.130` (and a `:8447` listener). Same `/24`, NOT adjudicated — the sixth sink-check read (`204` EMPTY direct-https, `301`-then-`204` behind the http chain, listener live SIXTH consecutive read) is only about `.87`. The `:8447` endpoint and both Dropbox URLs get a first liveness read next sweep (second-stage availability is a per-read claim). PyPI quarantine HOLDS (seventh read: `/simple/` `200` zero files, JSON `404`).

**AND THE `affects=` ORACLE MISSED THIS NAME'S OWN CRITICAL:** `api.github.com/advisories?ecosystem=pip&affects=aurum-pay` answered `0` rows TWICE this sweep while the direct lane serves `GHSA-3rfx-vc65-vf5v` (critical, `= 1.2.0`) fine by ID, with controls must-hitting on the same API (`requests` pip control `1` row, `express` npm control `1`). **`affects=` absence is NOT row absence — the index has holes even for advisories this wiki recorded by ID; confirm hot-name absences on the direct lane before claiming them.** Sweep context → [254th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-12-two-hundred-and-fifty-fourth-sweep)
