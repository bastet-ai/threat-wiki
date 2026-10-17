# PyPI `2026-10-emberlytts` cohort: EIGHT simultaneous `*-tts`/`*-asr` "audio-analysis profile" loader names (`driftwavets`, `emberlytts`, `glassbeakasr`, `novalithtts`, `pyrechoasr`, `quasitonnts`, `tonemaptts`, `voltswannts`), all `0.1.0`, one kam193 campaign tag, the whole cohort PyPI-QUARANTINED BEFORE this wiki could pull a single artifact — kam193's own text calls it the continuation of the ledger-tracked `2026-10-voxeval` coin-mining campaign (OSV `MAL-2026-17912`–`17918` + `17920`, Oct 17)

## Summary

- **What landed:** nine OSV records broke a 107-sweep quiet lane in one import tick (`17912`–`17920`, published `16:53:55Z`–`17:06:12Z`). Eight of the nine are ONE campaign: kam193 tag **`2026-10-emberlytts`**, category MALICIOUS, abuse category `remote_script`. The ninth (`17919`) is `ukraine69`, tracked on its [own page](ukraine69-pypi-telegram-vault-deletion-goygram-self-cleaning-queue-1646-october-2026.md).
- **The eight names** (all PyPI, all version `0.1.0`, all `aliases: None` — zero GHSA across the whole cohort): `driftwavets` (`17912`), `emberlytts` (`17913`), `glassbeakasr` (`17914`), `novalithtts` (`17915`), `pyrechoasr` (`17916`), `quasitonnts` (`17917`), `tonemaptts` (`17918`), `voltswannts` (`17920`).
- **kam193's own text (verbatim sense):** the series falsely advertises 'audio-analysis profiles' loaders; the only purpose is to execute remote code, **but the URL is not embedded in the package**; kam193 assesses it is "likely a continuation of the coin-mining campaign `2026-10-voxeval` which used similar wording."
- **Disposition at this wiki's read (~19:3xZ, Oct 17):** ALL EIGHT names serve `/simple/` `200` with `<meta name="pypi:project-status" content="quarantined">` and ZERO links, project JSON `404`. The entire cohort was dead on the registry **before a single tarball could be pulled** — no artifact forensics are possible for this wiki, and the payload stage-2 URL is unknown to everyone (never embedded, never served).
- **OSV import batch clock:** the eight records published inside `123 s` (`17:03:49Z`–`17:06:12Z`), `modified` timestamps all `17:45:03.2xZ` — one scripted import tick, not eight events.

## The voxeval lineage — this ledger watched this operator for two weeks

The kam193 `2026-10-voxeval` campaign is on-wiki history: `voxeval` `0.4.3–0.4.5` (MAL-2026-17457, Oct 2, cryptominer, quarantined within HOURS of advisory) → name-pivot #1 `voxel-tts` `0.5.0/0.5.1` (MAL-2026-17461, Oct 3, version counter survived the pivot) → name-pivot #2 `voxcpmtts3` `0.1.x` (Oct 3, counter RESET — the campaign TAG, not the version series, is the durable cluster key). Every one of those pivots was ONE name at a time, quarantined within hours, GHSA-blind the whole way.

**This cohort is the scale jump:** EIGHT simultaneous names in one import, one campaign tag, audio-modality name grammar (`-tts`, `-asr`, `-wav`/wave/echo/tonemap/volt vocabulary) instead of the single `vox*` pivots. The durable reads:

1. **The operator graduated from sequential name pivots to batch registration.** The Oct 2–3 ledger read was "hunt by campaign tag, treat name grammar as a tell"; batch launch makes the campaign tag the ONLY practical key — name-grammar watches (`vox*`) would have caught none of these eight.
2. **Quarantine-before-read is now the default state on this lane.** The Oct 2–3 pivots quarantined within hours of OSV; this cohort was already dead when the wiki first saw the names. For delete/quarantine-fast campaigns, the OSV record text — not the artifact — is the entire public forensics surface, and the absence of an embedded URL means even the C2 is unknowable pre-execution. The detector value here is the NAME LIST and the quarantine meta, nothing else.
3. **The zero-GHSA-through-everything pattern reproduces at cohort scale:** eight OSV records, zero GHSA aliases at check — Dependabot-blind as all three voxeval-lineage predecessors were.
4. **"URL not embedded" is a design signature, not an omission:** the same choice `voxcpmtts3`'s era implied (stages fetched at runtime). A cohort whose public artifacts contain no IOC string cannot be hunted by content — it is hunted by registry-lane metadata (`project-status` meta) and by name arrival.

## Tags

`pypi` `malware` `kam193` `campaign-2026-10-emberlytts` `voxeval-lineage` `cryptominer-lane` `remote_script` `audio-costume` `quarantined` `zero-ghsa` `batch-registration` `october-2026`

## Monitor

- Re-registration / third-generation pivots: any PyPI name carrying the `2026-10-emberlytts` or `2026-10-voxeval` campaign tag, any `*-tts`/`*-asr` audio-grammar name arriving OSV-side.
- Whether GHSA EVER mirrors any of the eight (all three voxeval pivots stayed GHSA-less through two full pivots — a zero-mirror cohort of eight would be the strongest Dependabot-blindness datapoint on the ledger).
- Whether any vendor (Socket, Snyk, StepSecurity) publishes an artifact teardown — at check no public writeup exists beyond kam193's text; stage-2 is unknowable from public sources.
- Whether quarantined shells get re-upload releases off the shell (the `dedh-devops-automation` / `voxeval` monitor pattern).
- Copycat adoption of the eight-in-one-import cadence by other campaign lanes.

Sweep context → [126th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-17-one-hundred-and-twenty-sixth-sweep).
