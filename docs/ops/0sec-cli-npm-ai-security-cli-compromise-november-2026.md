# 0sec-cli: the AI security CLI whose own release became the payload

**Captured November 11, 2026 (246th sweep) by this wiki from the `ghsa-malware` bot lane and this wiki's own registry-side verification (public GETs and static reads only; no artifact was ever executed). No analyst payload report existed at capture time; the payload itself is NOT independently verified by this wiki.**

## Summary

On **November 11, 2026 at 12:09:02Z** the `ghsa-malware` bot published `GHSA-9j97-6pqr-qvrx` (critical, CWE-506, `= 0.28.10`) against **`0sec-cli`** — the npm distribution of **"0", the self-described "self-improving, open-source cybersecurity team"**: an AI security harness (investigate vulnerabilities, review findings, connect coding agents via CLI or MCP) published by `peaktwilight` / `doruk@0.security`, repo `0sec-labs/0`, homepage `0.security`, with heavyweight security-tooling dependencies (`playwright`, `tree-sitter`, `drizzle-orm`, `pdfkit`). The security tool *is* the target class: its normal operator audience holds model-provider keys, GitHub credentials, and target scope by design.

This wiki's verification within roughly two hours of the advisory:

- **The advised rung was already gone.** `0.28.10` is absent from `versions[]` and every tarball probe answers `404` on all three lanes (registry, jsDelivr, unpkg) — **no CDN afterimage**. But the packument `time[]` block still enumerates `0.28.10: 2026-11-10T15:54:20.514Z` = the removal-roster law again: the time map is the only registry-side record that the rung ever existed.
- **The name stayed up.** `dist-tags.latest` reads `0.28.9`, whose tarball answers `200`. The takedown was surgical (one rung), name-level install still works.
- **Victim flow was real while the rung lived.** The downloads lane recorded **2,462 downloads in the Nov-4→10 window** and **339 on Nov-10 alone** (the day the malicious rung shipped, 15:54Z). The advisory landed `≈20 h 15 m` after publication; the excision completed sometime between the advisory (`12:09:02Z`) and this wiki's read (`≈14:35Z`) = a `≤2 h 26 m` advise-to-remove clock.
- **Bot-lane mint law holds.** OSV `MAL-2026-19118` carries `aliases: [GHSA-9j97-6pqr-qvrx]` **AT BIRTH**, origin `ghsa-malware`, import `12:23:59Z` (`+14 m 57 s` after the advisory), `modified` on the `12:30:04Z` tick. The row enumerates exactly one version (`0.28.10`) with no `ranges` — triage by the range field: an exact-row advisory protects every other rung on the name.
- **No human queue leg.** No ossf `malicious-packages` PR names `0sec-cli` as of this read (queue head `#1768`) = detection came solely from the machine lane.

| Field | Value |
|---|---|
| Package | `0sec-cli` (npm), `pkg:npm/0sec-cli` |
| Advised rung | `0.28.10` (exact row) |
| Malicious publish | `2026-11-10T15:54:20.514Z` (registry `time[]`) |
| GHSA | `GHSA-9j97-6pqr-qvrx`, critical, CWE-506, published + reviewed `2026-11-11T12:09:02Z` |
| OSV | `MAL-2026-19118`, alias at birth, import `12:23:59Z`, modified `12:30:04Z` |
| Registry state (this wiki, `≈14:35Z`; SUPERSEDED `≈16:3xZ`, see 247th section) | `0.28.10` excised from `versions[]`, survives in `time[]`; tarball `404` ×3 lanes; `latest 0.28.9` tarball `200` at this read (later swept, see below); packument `modified 2026-11-11T12:08:46Z` |
| Downloads | `2,462` dl/wk (Nov-4→10); `339` on Nov-10 |
| Publisher | `peaktwilight` (`doruk@0.security`), created `2026-08-30`, 23 rungs total |

## Why this one is worth a page

1. **The AI-security-tool-as-vector class lands on npm.** This wiki has logged AI coding agents as *victim executors* (Nx/s1ngularity, `AGENTS.md`/`CLAUDE.md` planted re-arms, the Railway AI-key-name query pattern). Here the *security product itself* is the trojanized dependency: an audience that installs a security harness is precisely an audience holding credentials worth stealing. Same trust inversion as the Ethersphere release-pipeline compromise two sweeps ago — the tool you trust certifies WHO, never WHAT.
2. **The publish cadence is itself a tell.** `0.28.6`–`0.28.9` shipped inside ~3 hours on Nov-9 (`19:43`–`22:48Z`), then a 17-hour gap, then `0.28.10` alone at `15:54Z` Nov-10 — the advised rung is separated from the burst. On any freshly advised name, diff `time[]` spacing around the advised rung before assuming a normal release rhythm.
3. **The advisories-before-removal window ran ~20 hours.** The rung lived a full day+ unadvised (published `Nov-10 15:54Z`, advised `Nov-11 12:09Z`). Whatever the payload did, the flow ran during the unadvised day, not the advised one — the advisory lane's job here was only to trigger the excision.
4. **No analyst writeup at capture.** The only `0sec-cli` reporting at capture time was the bot advisory and its mirrors (Corgea, GCVE aggregators). Treat payload claims as UNVERIFIED until a vendor or maintainer post lands; the maintainer had not commented publicly at read time. **MONITOR:** `0sec-labs/0` repo activity, `SECURITY.md` disclosure, vendor posts (Socket/OX/StepSecurity), whether `0.28.10` resurfaces on any CDN afterimage, whether the name re-publishes past `0.28.9`, and whether the bare rung returns to `time[]`-listed `versions[]` (rollback-not-deletion variant).

## <a id="november-11-247th-second-excision"></a>November 11 247th sweep: the CLEAN rung fell too, `0.28.9` excised with no advisory

**Re-read `≈16:3xZ` (247th sweep):** `dist-tags.latest` now reads `0.28.8` (tarball `200`). `0.28.9` — the rung the 246th recorded as the clean, installable `latest` at `≈14:35Z` — is GONE from `versions[]`, its tarball `404`, its publish stamp (`2026-11-09T22:48:41.026Z`) surviving only in `time[]`. No advisory was ever published against `0.28.9`: `GHSA-9j97-6pqr-qvrx` names `= 0.28.10` and nothing else.

**What moved:** the excision lane swept the packument past the advisory range within `≈2 h` of the first removal. The 246th's "the name still installs at `0.28.9`" was a true fact with a half-life under two hours. On an advised name, `dist-tags.latest` is a per-read claim, never a carried one.

**Disposition unchanged:** name still serves, `0.28.8` installs, payload still UNVERIFIED at this read (no maintainer or vendor post has landed). **MONITOR update:** does the excision keep walking `time[]` backward (`0.28.8`, `0.28.7` next?), which would mean the sweep is time-range-based rather than advisory-based.

## <a id="november-12-258th-eight-rung-sweep"></a>November 12 258th sweep: the removal lane walked EIGHT rungs past the advisory in one pass, `latest` is now `0.28.3`

**Re-read `≈14:3xZ` (258th sweep):** packument `modified` rolled to `2026-11-12T13:06:20.926Z` — DURING this sweep — and `versions[]` now reads `[0.15.0, 0.17.0, 0.18.0, 0.21.4, 0.25.0, 0.26.0, 0.28.0, 0.28.1, 0.28.3]` with `dist-tags.latest = 0.28.3` (tarball `200`). **EIGHT rungs gone since the 246th's read (`0.28.2`, `0.28.4`-`0.28.10`), four of them (`0.28.4`, `0.28.5`, `0.28.8`, `0.28.9`) re-probed `404` THIS read; `time[]` still carries all 26 stamps = the ledger remains the only census of what was.** The advisory `GHSA-9j97-6pqr-qvrx` still names ONE rung (`0.28.10`, per-version rows, `first_patched` null).

**The removal left a HOLE in its own middle: `0.28.3` (published `Nov-9 05:44:55Z`) SURVIVES while its younger sibling `0.28.2` (`04:58:43Z`) FELL — the sweep is NOT a time-window cut and NOT advisory-keyed.** Three readings, all quoted, NONE adjudicated: (a) per-tarball verdicts (the lane eats what its detectors flag, schedule be damned — the 255th's bot-minted-is-not-bot-detected law viewed from the other side); (b) the clean-rung survival pattern of the 235th's `glyphmatrix` specimen generalized (the unadvised rung is the survival lane, and sometimes a neighbor of it falls); (c) an internal retry/partial-failure artifact of one big sweep. Either way the durable law sharpens: **the removal lane reads neither the RANGE nor the SCHEDULE — a `404` roster is per-tarball evidence, and an advisory's version rows are never a manifest of what the registry ate** (the 240th's excision-sweeps-past-the-range law, newest and largest specimen).

**Disposition unchanged:** the name still serves and installs (`0.28.3`, `200`), payload still UNVERIFIED (no maintainer or vendor post landed at this read), malware-head GHSA lane quiet since `11:33:05Z`. **MONITOR update:** does the sweep cross the Nov-9 `04:58Z` boundary (kills reading (a)); does `0sec-labs/0` publish anything after the eight-rung day; CDN afterimages of the eight.

## <a id="november-13-262th-hole-eaten"></a>November 13 262nd sweep: the removal lane came back for the hole's own floor — `0.28.3` is gone, `latest` is `0.28.1`

**Re-read `≈03:0xZ` (262nd sweep):** packument `modified` rolled to `2026-11-13T02:15:53.717Z` and `versions[]` now reads `[0.15.0, 0.17.0, 0.18.0, 0.21.4, 0.25.0, 0.26.0, 0.28.0, 0.28.1]` with `dist-tags.latest = 0.28.1` (tarball `200` re-probed). **The middle-of-the-hole survivor is dead: `0.28.3` (`05:44:55Z`) and `0.28.2` (`04:58:43Z`) both `404` this read, four sweeps after the eight-rung pass and three sweeps after the hole-with-a-hole capture. `time[]` still carries every stamp.**

**What this adjudicates (from the 258th's three readings):** the sweep crossed the Nov-9 `04:58Z` boundary and ate the survivors it had passed — reading (a), per-tarball verdicts with no schedule and no advisory-range discipline, is the surviving reading; reading (b) (clean-rung survival as a stable lane) is DEAD as a property: clean-rung survival is a WAIT, not a fate. The durable law stands sharpened: **the removal lane revisits. A surviving rung is unremoved, not removed-around — re-probe per-tarball every read, and treat any `versions[]` roster as a snapshot between passes.** `GHSA-9j97` still names ONE rung (`0.28.10`) while the registry has now eaten TWELVE.

**Disposition unchanged:** name still serves (`0.28.1` installs, `200`), payload still UNVERIFIED (no maintainer or vendor post at this read). **MONITOR update:** does the second pass stop at `0.28.1` or keep walking `time[]` backward; does `0sec-labs/0` publish anything post-cleanup; CDN afterimages of the eaten rungs.

## <a id="november-13-264th-floor-eaten"></a>November 13 264th sweep: the "floor" was a pause — the lane ate FIVE MORE rungs between reads, `latest` is now `0.26.0`

**Re-read `≈06:3xZ` (264th sweep):** the 263rd recorded this roster as settled — "the removal lane stopped at the floor", `latest 0.28.1` `200`, `modified` unmoved `02:15:53.717Z`, SEVENTEENTH read. One sweep later the packument `modified` rolled to `2026-11-13T05:27:17.915Z` and `versions[]` reads `[0.15.0, 0.17.0, 0.18.0, 0.21.4, 0.26.0]`: `0.28.0` and `0.28.1` are GONE (`0.28.1` tarball `404` this read), `0.25.0` and `0.27.0` are gone, `dist-tags.latest` rolled to `0.26.0` (tarball `200` re-probed). **Five more rungs eaten between two reads; `time[]` still carries every `0.28.x` stamp (`0.28.0` Nov-8 `18:26Z` → `0.28.10` Nov-10 `15:54Z`), the ledger remains the only census.** `GHSA-9j97-6pqr-qvrx` STILL names ONE rung (`0.28.10`) while the registry has now eaten THIRTEEN `0.28.x`-span rungs plus `0.25.0`/`0.27.0` outside it.

**The exposure counter kept running anyway:** `api.npmjs.org` answers `2,678` dl/wk for the name whose ENTIRE `0.28` line no longer exists — installs of eaten rungs come from lockfiles/caches, and the counter reads like an active project to every consumer-facing lane. Quote the roster AND the counter together.

**What this adjudicates (across the 258th/262nd/264th arc):** the removal lane's stopping points are not floors. The lane re-walks the packument across passes (per-tarball verdicts, no schedule, no advisory-range discipline) and every "stable roster" quote on this wiki has a one-read half-life. **Law: a registry-state adjective ("stable", "stopped at", "holds") survives exactly one read — re-probe per-tarball, quote `modified` WITH the roster.**

**Disposition unchanged:** name still serves (`0.26.0` installs, `200`), payload still UNVERIFIED (no maintainer or vendor post at this read). **MONITOR update:** does the lane stop at `0.26.0` or keep walking `time[]` backward toward the 2025 rungs; does `0sec-labs/0` publish post-cleanup; CDN afterimages of the newly eaten `0.28.0`/`0.28.1`/`0.25.0`/`0.27.0`. Sweep context → [264th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-sixty-fourth-sweep)

## Durable hunt shapes

- On every `= <version>` exact-row advisory, check `dist-tags.latest` against the advised rung: if `latest` is a clean rung, the name keeps accruing downloads as if nothing happened (this name: 2,462/wk).
- Enumerate `time[]` after removal: the advised version's publish timestamp is the start of your exposure window, and `time[]` survives when `versions[]` does not.
- Quote the downloads lane with its window (`last-week` vs `last-day`) — the Nov-10 spike (`339`) is the malicious-day flow, the weekly number averages it away.

## Related on this wiki

- [Ethersphere bee-js / Swarm Desktop release-pipeline compromise](ethersphere-bee-js-npm-swarm-desktop-release-pipeline-compromise-sleepyduck-ethereum-contract-c2-november-2026.md) (trusted tooling as the delivery path, same week)
- [ALGAMIL7X stream, 246th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-sixth-sweep) (capture sweep, fleet, and lane laws)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (developer-credential harvest lineage; kinship NOT asserted)

## Sources

- GitHub Advisory `GHSA-9j97-6pqr-qvrx`: <https://github.com/advisories/GHSA-9j97-6pqr-qvrx>
- OSV `MAL-2026-19118`: <https://api.osv.dev/v1/vulns/MAL-2026-19118>
- npm registry packument + tarball probes + `api.npmjs.org` downloads (this wiki, Nov 11 ~14:35Z): <https://registry.npmjs.org/0sec-cli>
- Package page (maintainer-facing description): <https://www.npmjs.com/package/0sec-cli>

## <a id="november-13-265th-floor-holds-one-read"></a>November 13 265th sweep: the lane stopped at `0.26.0` — for exactly one read

**Re-read `≈08:3xZ` (265th sweep):** packument `modified` UNMOVED `2026-11-13T05:27:17.915Z`, `versions[]` still `[0.15.0, 0.17.0, 0.18.0, 0.21.4, 0.26.0]`, `dist-tags.latest 0.26.0` tarball `200`, `0.28.1` tarball `404` re-confirmed. EIGHTEENTH read; the removal lane has stopped at the new floor. **Read this sentence the way the 264th taught:** the 263rd's "stopped at the floor" survived ONE read; every frozen roster quote on this page carries a one-read half-life. The correct claim today is `floor-vs-walk pending re-probe`, not `stable`. `time[]` unchanged, the only census of the thirteen eaten `0.28.x`-span rungs plus `0.25.0`/`0.27.0`; `GHSA-9j97-6pqr-qvrx` still names ONE rung.

**MONITOR update:** NINETEENTH read re-probes per-tarball before any adjective; CDN afterimages of `0.28.0`/`0.28.1`/`0.25.0`/`0.27.0` still un-probed (candidate next sweep); does `0sec-labs/0sec` (homepage repo field) publish post-cleanup. Sweep context → [265th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-sixty-fifth-sweep)

## <a id="november-13-266th-floor-holds-two-reads"></a>November 13 266th sweep: the floor held TWO consecutive reads — a first on this lane

**Re-read `≈10:3xZ` (266th sweep):** packument `modified` UNMOVED `2026-11-13T05:27:17.915Z` SECOND consecutive read, `versions[]` still `[0.15.0, 0.17.0, 0.18.0, 0.21.4, 0.26.0]`, `latest 0.26.0` tarball `200`. NINETEENTH read; the removal lane has now left this roster alone for two full reads — the longest freeze this lane has ever held, and exactly the state the floor-is-a-rate law says to distrust most. The 263rd's one-read freeze preceded a five-rung collapse; the correct claim remains `floor-vs-walk pending`, never `stable`. `time[]` unchanged (the only census of the thirteen eaten `0.28.x`-span rungs plus `0.25.0`/`0.27.0`); `GHSA-9j97-6pqr-qvrx` still names ONE rung. No `unpublished` block observed on this packument (contrast the 266th's `quickgreet` census-block capture — removal lanes differ).

**MONITOR update:** TWENTIETH read re-probes per-tarball before any adjective; CDN afterimages of `0.28.0`/`0.28.1`/`0.25.0`/`0.27.0` still un-probed; does `0sec-labs/0sec` (homepage repo field) publish post-cleanup. Sweep context → [266th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-sixty-sixth-sweep)

## <a id="november-13-267th-floor-eaten-too"></a>November 13 267th sweep: the record freeze died in one read, `0.26.0` eaten at `11:23Z`

**Re-read `≈12:3xZ` (267th sweep):** packument `modified` ROLLED `2026-11-13T11:23:23.189Z` — the 266th's two-read floor record lasted exactly one sweep. `versions[]` fell `5`-to-`4`: `[0.15.0, 0.17.0, 0.18.0, 0.21.4]` — `0.26.0` GONE, its tarball `404` at read (it answered `200` the entire 266th), `latest` rolled DOWN AGAIN to `0.21.4` (tarball `200` = the new floor, per-read). TWENTIETH read. The lane's floor history TODAY: `0.28.8` → `0.28.3` (258th) → `0.28.1` (262nd, `02:15Z`) → `0.26.0` (264th, `05:27Z`) → `0.21.4` (this read, `11:23Z`) = THREE bites in one day, and the "longest freeze ever" was the pause between bites two and three. `time[]` still carries every eaten stamp (the only census of the fourteen now-gone `0.28.x`-span rungs plus `0.25.0`/`0.26.0`/`0.27.0`); still NO `unpublished` block on this packument; `GHSA-9j97-6pqr-qvrx` still names ONE rung while the registry has eaten FOURTEEN, and the OSV row `19118` sits joined-but-never-rolled (`modified 06:30:07Z`, `aliases` = the one stale GHSA). The correct claim remains `floor-vs-walk pending`, never `stable` — and the TWENTY-FIRST read should assume the `0.21.4` floor is already food until the tarball says otherwise.

**MONITOR update:** TWENTY-FIRST read re-probes `0.21.4` per-tarball FIRST; CDN afterimages of `0.26.0` (jsDelivr/unpkg) still un-probed = the 266th's `0.26.0`-`200` era left cache candidates; does the removal lane EVER stop above `0.15.0`, does `GHSA-9j97` EVER roll forward, does `0sec-labs/0sec` publish post-cleanup. Sweep context → [267th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-seventh-sweep)
