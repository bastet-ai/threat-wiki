# ctf-agent (npm): THE NAME RESURRECTION — a re-registered name inherits its murdered predecessor's time-map, seized 16 s BEFORE its own GHSA

**Registry:** npm · **Package:** `ctf-agent` · **Advisories:** `GHSA-2j3v-rjgw-5wgg` (`critical`, CWE-506, `published 2026-10-26T20:42:32Z`) + `MAL-2026-18335` (alias AT BIRTH) · **Publisher of record:** `nvtruongops <nvtruongops@gmail.com>` (maintainer-search total `1`) · **First seen by this wiki:** Oct 26, 221st sweep (~21:1x–21:4x UTC)

The ghsa-malware live-detection lane broke its `≈4 h 14 min` silence (`16:28:46Z` → `20:42:32Z`) with exactly one name, and that name handed this ledger a grammar it has never catalogued: **the time-map straddles resurrection.** The packument's `created` key reads `2026-10-26T18:57:45.343Z` — and the SAME time map carries NINE version stamps dated 2026-09-06/11 (`1.2.0` … `1.3.7`, a normal ladder, four rungs in `≈1.5 h` on Sep-06, three on Sep-11). A name record born today cannot legitimately carry September publishes unless **the name was whole-name erased and re-registered, and npm's time map survived the resurrection.** The 214th's publish-poc law said the wipe roster in the time map is the only surviving census of a wiped name; the corollary nobody priced: **a resurrected name inherits its predecessor's ghost census — `created` LATER than the oldest `time` entries is a resurrection marker, readable on any packument, no registry archaeology needed.**

## The clock, as the packument tells it

| Stamp | Event |
|---|---|
| `2026-09-06 22:27:28` → `2026-09-11 13:03:23` | NINE rungs `1.2.0`–`1.3.7` in the time map — GHOSTS (zero version objects, every tarball `404`) |
| `2026-10-26T18:57:45.343Z` | `created` + `0.0.0-stage` published the SAME SECOND (the stage-stub grammar) |
| `2026-10-26T19:18:10.694Z` | `0.1.0` published (the advised rung) |
| `2026-10-26T20:42:16.639Z` | packument `modified` — the registry's last change = the seizure |
| `2026-10-26T20:42:32Z` | `GHSA-2j3v-rjgw-5wgg` PUBLISHES — `≈15.4 s` AFTER its own seizure |
| `2026-10-26T21:25:08Z` | OSV `18335` import (ghsa-malware origin, versions `[0.1.0]`, alias at birth) |
| `2026-10-26T21:30:05Z` | OSV `modified` — the `:30` importer tick |

**SEIZURE BEFORE OWN GHSA.** The pre-GHSA interval adds to the family: `numbors` same-second (`9 s`), `dsh-native` `≈30 s`, now `ctf-agent` `≈15 s`. The wave automaton seizes first and advises second — a defender waiting on the GHSA feed to trigger a blocklist was never the first reader, and on this lane can never be.

## Disposition: rollback-to-stage WITH full legit-history deletion

`versions` now holds exactly `[0.0.0-stage]`, `latest → 0.0.0-stage`; the advised `0.1.0` is excised (registry/unpkg/jsDelivr ALL `404` — no sample path survives, the @worca surgical law at a coarser granularity), AND all nine September ghosts are tarball-`404` too — the resurrection's predecessor got no resurrection of its own bytes. The stage stub survives on all lanes: `2` files, `331 B`, `package.json` `{"stub": true, "description": "Temporary package placeholder for staged publishing"}` + a README reading "Temporary Holding Version… awaiting a staged release" (static read ONLY, NEVER executed; tarball sha256 `9636d4d477feae27b0872cfc53827ca6813e44f790f8da76f41a1b74f9d64480`). Same staging furniture as `dsh-native` (rollback-to-stage) and the wave fleet (stage + `0.0.1-security` holder) — but here there is NO holder rung and the costume is the placeholder itself.

**Who the September package was, and who deleted it, is NOT determinable from public evidence** — the packument shows only the current maintainer. What IS determinable: the current name record (owner `nvtruongops`, gmail throwmail shape, search footprint `1`) published the advised rung, carried CWE-506 boilerplate, and was seized by the wave machinery. Guilt of the September publisher is NOT asserted.

## Boilerplate again: the responder gets nothing

`GHSA-2j3v` text is the verbatim "fully compromised / rotate secrets from a different computer" boilerplate — zero IOCs, zero payload description, exactly the @worca-obituary condition: every org that installed `0.1.0` inside the `≈1 h 24 min` window (19:18 publish → 20:42 seizure) has no public artifact to triage against, and the tarball is `404` on every lane, so the artifact may be unrecoverable. The `0.0.0-stage` → `0.1.0` `≈20 min` gap + `≈84 min` exposed window is the operational tempo to baseline.

## Hunt

- **Resurrection marker (free, packument-only):** `time.created` strictly LATER than the oldest `time[version]` on any name you monitor = the name was erased and re-registered. Diff `versions` keys vs `time` keys: ghosts older than `created` = predecessor census.
- `created`-to-advised-rung intervals measured in minutes on names with September-era ghost ladders.
- Publisher footprint `1` + gmail-domain + stage-stub first publish = the throwmail shape (`wiseke` fleet's fingerprint, here at single-name scale).
- Do NOT pin `latest` on any recently-seized name that still serves a stub: `npm install ctf-agent` today installs stage furniture — harmless bytes, but it means the name is a live re-armable slot.

**Disposition at capture (Oct 26 ~21:3x UTC):** name ALIVE as a stage stub, advised rung dead everywhere, September ghosts dead everywhere, `modified` frozen at the seizure second. Tripwire: any NEW version under `ctf-agent` = the re-arm fires; `nvtruongops` acquiring a second package = footprint law updated; any OSV mint against the September rungs = the predecessor's own malice (currently zero advisories attributed to them; note the 221st's `/v1/query` answered `{}` `≈1–2 min` AFTER the `21:25:08Z` import — query-lane `{}` has its own freshness lag, the canonical `/v1/vulns/` read carried the record — see self-capture 2 on the stream section).

Sweep context → [221st stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-twenty-first-sweep) · sibling grammars → [dsh-native rollback-to-stage](dsh-native-keer1024-npm-seizure-scoped-twin-survival-rollback-to-stage-rust-worker-exe-october-2026.md) · [publish-poc whole-name wipe](publish-poc-cohort-npm-self-publishing-poc-plaintext-authtoken-unpublished-wipe-osv-first-october-2026.md) · [@worca surgical excision](worca-app-npm-ghsa-malware-one-version-seizure-live-maintainer-fix-forward-october-2026.md)
