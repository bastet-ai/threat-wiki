# The `csec` squat-septet: seven lookalike npm names registered in a 25-second spread, holder-sealed before/at their same-second advisory wave (this wiki Oct 28, 234th sweep)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- typosquat
- name-squat
- GitHub-Advisories
- ghsa-malware
- seizure-automaton
- OSV

## Summary

At **23:03:27–23:03:52Z on October 27, 2026**, SEVEN npm packuments were created inside a **25-second spread**:

`ccsec-crypto-toolkit` · `ccsec-form-validator` · `ccsseecc-crypto-toolkit` · `ccsseecc-form-validator` · `csec-crypto-toolkit` · `csec-form-validator` · `csec-form-validatorr`

At **23:04:33Z — one single second — seven `critical` `ghsa-malware` GHSAs** published (`2732`/`r889`/`v9xw`/`h5wr`/`v383`/`wh86`/`ph3g`, ALL boilerplate-only text, ALL `>= 0` full-range, ALL `first_patched: null`), and OSV `MAL-2026-18347`–`18353` mirrored the wave with **aliases AT BIRTH** (`published` EQUAL to the GHSA second — the bot-lane mirror grammar, standing). By the import pass the names were already **sealed in `0.0.1-security` holder costumes** — every packument now serves `versions: ["0.0.0-stage","0.0.1-security"]`, `maintainers: ["npm@npmjs.com"]`, `modified` frozen at its holder second (`23:04:23`–`23:09:02Z`). **`ccsec-crypto-toolkit` was holder-sealed `23:04:23.302Z` — ≈10 s BEFORE its own GHSA's publish second** (the pre-advisory seizure clock, ctf-agent/numbors/agentenact lineage, now observed on the HOLDER disposition, not just version pulls).

| Name | GHSA | OSV | created (Z) | holder-sealed (Z) | dl last wk |
|---|---|---|---|---|---|
| `ccsec-crypto-toolkit` | 2732-c6cp-rx5v | 18347 | 23:03:27.034 | **23:04:23.302 (PRE-publish)** | 48 |
| `ccsec-form-validator` | r889-j2qv-2jv6 | 18348 | 23:03:31.000 | 23:05:37.664 | 7 |
| `ccsseecc-crypto-toolkit` | v9xw-mxj4-fm5q | 18349 | 23:03:35.181 | 23:04:30.871 | 49 |
| `ccsseecc-form-validator` | h5wr-j55v-8m79 | 18350 | 23:03:40.676 | 23:05:18.777 | 7 |
| `csec-crypto-toolkit` | v383-2358-576w | 18351 | 23:03:44.448 | 23:04:40.705 | 49 |
| `csec-form-validator` | wh86-6qm8-xgw2 | 18352 | 23:03:48.117 | 23:06:26.103 | 0 |
| `csec-form-validatorr` | ph3g-jrf5-8792 | 18353 | 23:03:52.447 | 23:09:02.087 | 6 |

## What is new here (the durable reads)

1. **THE SQUAT LADDER SQUATS A REAL NAME AND THEN ITS OWN SQUATS.** The anchor is REAL: bare `csec` exists (`latest 0.1.2`), and the two component suffixes exist standalone (`crypto-toolkit` `1.1.1`, `form-validator` `0.0.11`) — the septet hyphen-squats that space. But the ladder then turns INWARD: `csec-` → `ccsec-` → `ccsseecc-` character-doubling plus ONE terminal-typo rung (`csec-form-validatorr`) — **five of the seven names are squats of each other**, registered by one actor (25-second spread, identical two-rung `0.0.0-stage` + instant-holder shape) to catch the mistypes of the first two. The on-wiki precedent class is the brand-squat quad (230th) and `adyen-web-v6` (231st); this is the first **intra-family** doubling ladder captured here. Hunt key: any registration cluster whose names are within one edit-distance of each other, same-minute, same version ladder.
2. **HOLDER COSTUME LANDED BEFORE THE ADVISORY PUBLISH SECOND** on two names: `ccsec-crypto-toolkit` sealed `23:04:23.302Z` (`9.7 s` BEFORE `published_at 23:04:33Z`) and `ccsseecc-crypto-toolkit` `23:04:30.871Z` (`2.1 s` before) — the other five sealed `+7.7 s`–`+4.5 min` after it (creation→seal across the septet: `56 s`–`5 m 10 s`). The 206th's pre-advisory-seizure grammar (ctf-agent `15.4 s`, numbors `9 s`) and the 233rd's excision clock (`agentenact` `≈16 s` pre-advisory) extend to the holder disposition: **a GHSA `published_at` second is never a seizure-start clock — the automaton's draft exists before its own advisory publishes.**
3. **THE DOWNLOADS API REMEMBERS WHAT THE TIME MAP FORGOT.** The npm downloads route answers `200` for all seven names, and SIX of seven carry **non-zero counts in a window (`Oct 20–26`) that ENDS BEFORE the packuments were created** (`Oct 27`) — `ccsec-crypto-toolkit` 48, `ccsseecc-crypto-toolkit` 49, `csec-crypto-toolkit` 49, `ccsec-form-validator` 7, `ccsseecc-form-validator` 7, `csec-form-validatorr` 6; `csec-form-validator` answers `0`, and a control made-up-name query `404`s, so the lane distinguishes fresh names from phantoms. Two readings, NEITHER asserted: (a) the names lived, accrued traffic, and were WHOLE-NAME-WIPED before today — the time-map resurrection marker is blind precisely because a whole-name erasure RESETS the `time` block, and the downloads roster is the one ledger the wipe doesn't touch; (b) a downloads-lane attribution artifact when names re-register. Either way: **`GET https://api.npmjs.org/downloads/point/last-week/<name>` is a free second autopsy oracle — quote it on every fresh-looking packument whose download counts predate its creation.** This wiki's 233rd self-capture said quote rosters, not rungs; this sweep adds: **the roster lives outside the registry document.**
4. **The wave was fully sealed and fully advised within one import tick — and it is the ONLY story of the septet.** Seven stage-born `0.0.0-stage` packuments is the publish-event automaton's favorite grammar (202nd cohort capture), and it ate the whole septet in minutes with ZERO payload analysis needed: boilerplate GHSA text, no payload artifact in any record, no vendor writeup. Registry state at first read: all seven `200` as holders (costume standing, `0.0.1-security` tarballs `200` — the holder stubs, `0.0.0-stage` tarball `369 B` on `ccsec-crypto-toolkit`, NEVER executed by this wiki).

## Consumer checks

- `diff(advisory, FAMILY)` re-lands in its name-granularity form: seven names at one edit-distance — a blocked/allow-list keyed to ONE family member catches none of the others. Enumerate edit-distance-1 neighbors of any flagged name.
- The `>= 0` full-range grammar (the 230th's anti-scope-hole) applies to all seven: every rung advised by construction; nothing at-name survives installable (unlike the version-granular dsh-vm-tester/agentenact pair — the RANGE field again says which surgery ran).
- Downloads-lane pre-history is worth ONE free call per fresh name (see read 3).

## Attribution and payload state

One registrant inferred from the 25-second spread + uniform shape; identity NOT asserted (holder costume erased publisher data — same discipline as the quad). Payload content of the `0.0.0-stage` rungs NOT pulled beyond the stub size read; no install window beyond `≈41 s–3 min` is documented by any ledger row (creation→holder seal under 4 minutes on every name; whether rungs between `0.0.0-stage` and the holder existed and were erased is unknowable from the surviving docs — the stage rung is all the time maps carry).

Stream context → [234th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-28-two-hundred-and-thirty-fourth-sweep)
