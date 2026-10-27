# The `mw` trio — the queue name eaten alive: `mw-test-utils`, `mw-communication-client`, `mui-wrapper-x-date-pickers` (npm, ossf `#1673`, unpublished `+21 min` after the queue PR, zero OSV / zero GHSA, collector `38.242.235.206/depconf/` LIVE)

**Captured Oct 27, 2026 (232nd sweep, ~19:2x–19:5x UTC) by this wiki. Static analysis only — no package was ever executed. Attribution and authorization claims NOT asserted.**

## What happened

Three npm names — `mw-test-utils`, `mw-communication-client`, `mui-wrapper-x-date-pickers` — were created by account `amahrou1w` on 2026-10-27 at `06:54:28.875Z` / `06:54:34.131Z` / `06:54:41.531Z`, each with a `0.0.0-stage` rung at its own creation second, then malicious rungs published one minute after each stage inside the `06:55–07:03Z` window (the stage-born ladder grammar; `1.0.0/10.0.0/10.0.1`, `1.0.1/10.0.0`, `1.0.0/10.0.0` respectively).

ossf/malicious-packages **PR `#1673` opened `18:34:45Z`** reporting all three (curator writeup, tarball sha256s attached, static-only). **npm's abuse lane unpublished every rung of all three names at `18:55:46/48/49Z` — `+21 min` after the PR opened, `≈12 h` after the rungs went live** — while `#1673` was still OPEN. Zero OSV records (query `{}` ×3 at `19:46Z`), zero GHSA (`affects=` `[]` ×3), ever.

## The payload (reporter static text, corroborated by surviving time blocks only)

Per the report: each tarball carries three files and no functional code; `package.json` declares `preinstall` and `postinstall` scripts that POST the installing machine's **username, hostname, and working directory over plain HTTP to `38.242.235.206` under `/depconf/<name>/<hook>`**. The README self-labels the set as a dependency-confusion proof of concept for a bug bounty program. Bug-bounty costume; intent NOT asserted.

## Registry forensic state (this wiki, first fetch)

- All three packuments: `versions []`, `dist-tags` absent, `maintainers []` — whole-rung unpublish including each `0.0.0-stage`.
- **Surviving `unpublished` blocks** `2026-10-27T18:55:46.624Z` / `18:55:48.181Z` / `18:55:49.751Z` naming every erased rung = the only registry-side durable artifact (Sep-21 time-block law).
- jsDelivr AND unpkg versioned probes `404` — **no CDN afterimage this time** (afterimages are cache-luck, not a lane property — contrast `@azure-growth`, whose pinned jsDelivr rung still serves `200` through its death).
- Maintainer search `maintainer:amahrou1w` `total: 0`, profile `~amahrou1w` `404` (footprint 0 after the hop — but search totals are phantoms per the 230th scope-search law; the packument is ground truth).
- **THE COLLECTOR IS ALIVE: `http://38.242.235.206/` → `200`, `/depconf/` → `200`** (GET-only probes, `≈19:3xZ`). Bare-IP endpoint-outlives-package class (nodetokyo / `eslint-config-compact-utils` lineage). Hunt template: `/depconf/<pkg>/<hook>` + identity triple in cleartext HTTP.

## Why it is durable

1. **TAKEDOWN ≠ ADVISORY, second instance with a queue clock.** The `css-nesting-transform` precedent (Sep 17, unpublished unadvised via `#1602`) reproduces at ×3-name scale. A name can enter, be flagged, be erased, and leave **zero advisory-lane trace** — advisory-keyed consumers (Dependabot class) were blind the entire `≈12 h` live window AND stay blind forever after. The durable public record is only: the open PR + the `unpublished` time block + collector IOCs.
2. **The queue is an enforcement trigger, not just a ledger.** The 228th–229th law said queue-only names are enforcement-INVISIBLE; the 231st–232nd pair corrects it precisely: invisible to the ADVISORY machinery (no OSV/GHSA ever), never invisible to the ABUSE machinery. PR-open-to-unpublish clock `≈21 min`. Whether npm reads the queue or a shared reporter path triggered it is NOT asserted — either way, **the ossf queue is now demonstrably upstream of registry enforcement, which makes report-shape poisoning of the queue a live attack surface.**
3. **Three bare, delete-only names are re-registerable right now.** Tripwire block: any new packument on `mw-test-utils`, `mw-communication-client`, or `mui-wrapper-x-date-pickers` = the operator returning; and the `38.242.235.206` collector answers today whether or not the names come back.

## Monitor

- Re-registration on any of the three names (holder seal? resurrection marker? the trio has NO prior OSV row, so the 230th death-on-arrival law has nothing to enforce against — a return here would be **advisory-invisible a second time**).
- Collector liveness / path grammar growth on `38.242.235.206` (other `/depconf/` siblings from sightings).
- `#1673` merge outcome (if it merges, the trio finally gets OSV rows — watch whether they arrive `MAL-0000-`-draft-minted or at merge).
- Whether the abuse lane's queue-reading clock (`+21 min`) holds on the next curated PR (`#1672` `cache-helper` is the live candidate — different: it is worm-shaped and STILL live).

Sweep context → [232nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-thirty-second-sweep)
