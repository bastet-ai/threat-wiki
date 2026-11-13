# PyPI voice-synthesis wave two: sixteen advised loaders still installing

## Summary

- **What landed:** twenty-four OSV rows in one ~3.5 h lane (`MAL-2026-19178`-`19201`), of which SIXTEEN are one kam193 campaign: tag **`2026-10-voice-synthesis-profiles`**, category MALICIOUS, abuse reason "Downloads and executes a remote malicious script." The sixteen (`19179`-`19193` + `19199`): `eulaliatts`, `evalometer`, `ferrotts`, `flowmetry`, `garviscope`, `garvisuite`, `inframetric`, `lumitts`, `melstagen`, `phoneliasr`, `spectrova`, `stackvane`, `voxgramasr`, `voxrelitts`, `wavforge`, `acustoviasr` — all PyPI, all version `0.1.0`, all `aliases: None`, **zero GHSA across the whole sixteen** (per-name `affects=` zero-test, controls must-hit).
- **The registry ignored every advisory:** fifteen of sixteen answer `simple/` `200` `project-status: active` WITH live file links, and `pypi.org/pypi/<name>/0.1.0/json` `200`; only `inframetric` sits `quarantined`/zero-links = a 15:1 advised-and-installable differential at read (~22:3xZ Nov 12), the 256th differential law re-attested at cohort scale.
- **The artifacts are the SAME binary-identical template as the Oct-21 wave one:** `__init__.py` 2,899-2,911 B across all names (name-substitution only), wheel ~4.0-4.1 KB, docstring *"a tiny, standard-library-only runner for remote profiles"*, `_fetch` with `attempts=8` and `_RETRY_STATUS (408,425,429,500,502,503,504,530)`, per-name `<NAME>_CACHE` env in `tempfile.gettempdir()`, zero dependencies, `requires_python >=3.8`. The docstring's only URL is the `example.com` placeholder: **the URL is not embedded**, same design signature as the `emberlytts`/`voxeval` lineage — hunted by name list and campaign tag, not by content.
- **The birth split is new and forensic-grade:** upload stamps cluster in TWO batches, Oct-6 `17:29`-`18:15Z` (8 names: `melstagen`,`voxgramasr`,`voxrelitts`,`garviscope`,`flowmetry`,`eulaliatts`,`phoneliasr`,`garvisuite`,`lumitts`,`spectrova`,`stackvane` = eleven names actually) and Oct-9 `14:22`-`14:23Z` (5 names: `acustoviasr`,`wavforge`,`evalometer`,`ferrotts` in a 21-second window) — the same campaign tag, two upload sittings, and every OSV row minted TONIGHT (`20:35:05Z`-`21:04:04Z`), `≈37-38 days` after birth. The wave-one correction law ("the advised-and-installable class is the kam193 base rate") is now the measured base rate: 15/16.

## <a id="the-paper-arrives-november-13"></a>The paper arrives (November 13, 262nd sweep): GHSA mirrors landed inside the 2 h bracket, PyPI ate one name and kept the live tail

The 261st's `GHSA 0`/16 was a lane-lag statement with an expiry time. Direct `type=malware&sort=published` reads (`~03:0xZ`) show the pip GHSA lane carrying the wave-two names as critical `= 0.1.0` exact rows minted at the `2026-11-12 21:30:32Z` second - `GHSA-q6vp` (`stackvane`), `GHSA-3825` (`phoneliasr`), `GHSA-c2cg` (`voxgramasr`), `GHSA-qmvr` (`voxrelitts`), `GHSA-2w2f` (`spectrova`), `GHSA-rgqq` (`wavforge`), `GHSA-26j8` (`garvisuite`), `GHSA-vpj7` (`melstagen`), `GHSA-p2pc` (`inframetric`), `GHSA-c475` (`flowmetry`) + cohort - i.e. `~25-55 min` after the OSV mints, inside the emberlytts lineage's `~2 h` mirror bracket; `GHSA-79gc` (`acustoviasr`) and `GHSA-fwqr` (`dashloom`) followed at the `2026-11-13 00:31:29Z` second. The earlier zero was the SILENT PARAMETER DROP (`advisories?package=` served the same unrelated 30 rows for three different names, echo-checked - the `affects=`-style zero must be confirmed on the direct head).

**Registry dispositions between reads:** `dashloom` (a same-lane pip cousin minted `19202`, not in the sixteen) went WHOLE-NAME `404` on `simple/` + JSON `~4 h` after `GHSA-fwqr` minted; the sixteen hold at `simple/` `200` across the spot re-checks (three read this sweep: `eulaliatts`, `voxgramasr`, `spectrova`), `inframetric` still the sole quarantine (`project-status: quarantined`, zero links, `SERIAL 43574484`, JSON `404`).

**The tail (`MAL-2026-19206`-`19208`, `garvisometerui`/`qwen3ttsui`/`voxcpmttslora`):** same kam193 loader family ("provide executing code from a given URL... no payload in-package", Category MALICIOUS), all `simple/` `200` `project-status: active`, all single `0.1.0`, all `aliases None` at first read. Their artifact clocks read **Oct-3 `22:41Z` / Oct-4 `00:52Z` / Oct-5 `09:48Z`** - a third birth sitting, `~40 days` before the rows - extending the two-sitting law to three. **The counter control:** `pypistats` answers NON-uniform `7`/`30`/`11` dl/wk on the tail vs the sixteen's `1,309`-`2,203` - uniformity was the tell; per-package counters across a cohort need a same-cohort spread check before any of them is read as demand.

## The counter trap (self-capture)

`pypistats` `last_week` answers a suspiciously UNIFORM `1,309`-`2,203` downloads/week on all sixteen names (sum `≈29,232` dl/wk) — near-identical counters across sixteen zero-dependency, days-old loader stubs are NOT organic popularity. Mirror/probe traffic on `simple/` lanes can dominate per-package counters for names no human installs. **A uniform cohort counter is a mirror signal, not a demand signal; do not quote PyPI download counters across a cohort as victim census the way npm `dl/wk` was quoted for the `baileys` forks (npm counts registry pulls, and those names had real pre-advisory ladders).** Per-read traffic claims need a same-source control.

## Durable hunt shapes

- **Campaign tag is the only key that works on this lane:** wave one (21 names, `18134`-`18154`) + wave two (16 names) share tag `2026-10-voice-synthesis-profiles`; name grammar (`-atts`/`-tts`/`-asr`/`-vtt`/`-liatts` tails) drifted again — hunt the tag, not the tails.
- **Template byte-stability is a fingerprint:** 2,899-2,911 B `__init__.py` + identical retry table + `<NAME>_CACHE` naming = same generator; byte-length windows over PyPI arrivals catch the cohort at birth even with no embedded URL.
- **GHSA never mirrors the kam193 lane at cohort scale:** sixteen rows, per-name `affects=` zero-test `0/16` at `≈30 min` post-mint; the emberlytts cohort's mirrors arrived ~2 h late, so treat zero-at-read as a lag class with a re-read obligation, not blindness.
- **OSV `modified` stamps cluster on the `:15`/`:30`/`:45` import ticks** (`21:15:13-14Z` bulk of the wave) while `published` spreads `20:35`-`21:04Z` = the row was authored then SERVED at the next tick; a 30-minute "quiet lane" can be a queue, not an absence.

## Related on this wiki

- [Emberlytts eight-name cohort + voice-synthesis wave one](emberlytts-pypi-eight-name-audio-analysis-loader-cohort-voxeval-lineage-kam193-october-2026.md) — the lineage: `voxeval` → `voxel-tts` → `voxcpmtts3` → emberlytts ×8 → wave one ×21 → **wave two ×16**.
- [basek and hesk, the crates.io keylogger pair](basek-hesk-crates-io-telegram-keylogger-pair-amazon-inspector-november-2026.md) — the two rows minted in the same lane minutes after this cohort.
- [algamil7x stream, 261st sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-12-two-hundred-and-sixty-first-sweep) — full sweep record.

## Sources

- OSV API rows `MAL-2026-19179`-`19193`, `19199` (reads ~22:2x-23:0xZ Nov 12), `api.osv.dev/v1/vulns/` + `v1/query`; campaign tag `2026-10-voice-synthesis-profiles` quoted verbatim from the kam193 source block in each row's `details`.
- PyPI reads: `pypi.org/simple/<name>/` (`project-status` meta + link count), `pypi.org/pypi/<name>[/0.1.0]/json` (upload stamps, sizes), wheel downloads + unzip (all 16 names, sample full-read 5: `eulaliatts`,`phoneliasr`,`spectrova`,`wavforge`,`stackvane`).
- `pypistats.org/api/packages/<name>/recent` (all 16).
- GitHub Advisory API `GET /advisories?affects=<name>` (all 16 zero; `express`/`requests` controls must-hit).
