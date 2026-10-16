# `marocolor` (PyPI) — a color-palette costume that at IMPORT time spawns two daemon threads: `steal()` walks the victim's home directory for nine sensitive extensions and POSTs every match to a hardcoded Telegram bot `sendDocument`, while `crash()` runs a thread-fork-bomb plus a `127.0.0.1:80` connect-loop DoS; Arabic operator-addressed comments mark it in the LLM-authored tell class; `MAL-2026-17900` (kam193 lane, campaign `2026-10-marocolor`) is the ledger's live NEVER-JOIN control — it arrived OSV-first, got its `GHSA-m6jr-rmfr-29w4` mirror `1 h 52 m` later, and still reads `aliases: None` at `+59 min`

## Tags
- ops
- supply chain attack
- PyPI
- malicious-package
- infostealer
- file-exfiltration
- telegram-bot-c2
- denial-of-service
- fork-bomb
- kam193-lane
- OSV-first
- alias-lane
- never-join-test
- LLM-authored-tell
- October 2026

## Summary

`marocolor 1.0.0` (single version; upload `2026-10-14T23:15:32Z`; costume summary "Enhanced color palette utilities for terminal UI"; homepage `marocolor[.]net`; sole dependency `requests`; author string `MarocoColor Dev`) was flagged by the kam193 / bad-packages lane as campaign `2026-10-marocolor` (`files-exfiltration`, `uses-telegram-bot`, `destructive-actions`), imported to OSV as `MAL-2026-17900` at the `11:17:07Z` tick (`published` backdated to the kam193 flag second `10:38:53Z`), mirrored as `GHSA-m6jr-rmfr-29w4` (critical) at `12:31:16Z` — and STILL SERVES on PyPI at this wiki's `≈13:4xZ` check (`≈38.5 h` after upload, no quarantine).

This wiki pulled both artifacts without execution (wheel sha256 `575afa75f14b07fd0f183e033e855cf2c159420ddb568202e2b3193b202d5110`, sdist sha256 `3709dd05c82403b06a26e5a0e35257fc44eae3624afac8edb8702ffa6eb00ded`) and read the full source. The mechanics are a two-thread import-time payload:

- `__init__.py` — `from .core import steal, crash` then `threading.Thread(target=steal, daemon=True).start()` and the same for `crash`. **Mere `import marocolor` executes both lanes — no function call, no CLI, no hook needed.** The comment above them (Arabic) reads "execute the malicious operations immediately upon invocation in the system background" — an operator-addressed note, the same generation-artifact tell class this ledger logged on CL-UNK-1211's reasoning comments.
- `steal()` — `os.walk` over `os.path.expanduser("~")`; every file ending `.txt .pdf .docx .jpg .png .key .env .config .sql` is POSTed, one at a time, to `https://api.telegram.org/bot<TOKEN>/sendDocument` with `chat_id` — **bot token `8534701940:AAFcc26hUmwzkTrFWbbeZQ4QE01l3B6J4lk`, chat `1785091570` are durable egress hunt keys** (search proxy/egress logs for `api.telegram.org/bot8534701940` and the chat id; the token is also a report-to-Telegram abuse handle — request revocation, do not probe the bot from infra you care about).
- `crash()` — an unbounded `while True` that spawns a new `crash` thread each iteration AND opens/closes a TCP socket to `127.0.0.1:80`: a local resource-DOS (thread bomb + port-80 connect loop), matching kam193's "performing a DoS on the victim's machine." The `127.0.0.1:80` target is local-only — self-harm, not C2: read it as destructive filler or a sandbox-frustration device, not a network hunt key.
- Every exfil/network call is bare `except: pass` — the package fails silently on any error, keeping the color-palette illusion intact for the victim.

**Why this matters (durable reads):**

1. **`17900` is the cleanest NEVER-JOIN control the ledger has ever held.** The record is FRESH (born `11:17Z`), its mirror exists (`12:31:16Z`), and `aliases` was still `None` at `+59 min`. Model v3 (alias join is machine-lane-birth-only; a GHSA minted later never attaches) predicts: never joins, permanent. The Oct-9 precedent (ghsa-malware importer mirrors kam193-sourced OSV records at retro-lag, join follows) predicts: joins within days. This single record settles the model boundary at the `+2 h` / `+24 h` re-reads — no other configuration separates the two hypotheses this cleanly.
2. **The kam193 quarantine clock is per-package, and `marocolor` is a slow rung.** Upload→check `≈38.5 h` LIVE after a flagged kam193 record with a GHSA mirror already minted. Ledger bracket now: sysdiagd `≈25 min` / fromthehotel-poems `≤1.5 h` / fontcase `≈75 min` / minecraftaccfinder `≈2 h` / npp-ml `≈25 h 20 m` / **marocolor `≥38.5 h` still live**. Hunt rule unchanged: never treat an advisory as removal on PyPI; verify the JSON API.
3. **Duplicate-origin = analyst-revision signal.** `17900` carries TWO `malicious-packages-origins` entries for the SAME version `1.0.0` with DIFFERENT source shas, imported `24 min` apart (`11:17:07Z` sha `38b0fa2e…`, `11:41:03Z` sha `84922797…`), `modified` `11:45:05Z`. kam193 re-published the campaign record within the same hour and the importer consumed both. `modified` movement with unchanged versions list can mean "the analyst updated the writeup," a useful early tell that record text is about to change.
4. **The Telegram-bot-as-drop-house pattern keeps working.** Bot-token + chat-id in plaintext with `sendDocument` is trivially revocable and trivially hunt-able — yet the lane keeps shipping it (`ig-gox`, proxyrubika spellings, and a Telegram `chat_id 1064260758` recon fleet on-wiki since September). Defender action is cheap here: block/monitor `api.telegram.org/bot*` from developer egress as a class, and IoC-match the two literals above.

## Confirmed mechanics (verified by this wiki, no execution)

- Registry state `≈13:4xZ` Oct 16: `pypi.org/pypi/marocolor/json` `200` (NOT quarantined), single release `1.0.0`, both wheel and sdist served (`files.pythonhosted.org` `302`→asset).
- Wheel contents: `marocolor/__init__.py`, `marocolor/core.py`, dist-info only. No entry points, no console scripts — the import-time threads ARE the activation.
- OSV record: `published 10:38:53Z` (kam193 flag second), `modified 11:45:05Z`, references `bad-packages.kam193.eu/pypi/package/marocolor`, credits kam193 reporter+analyst, `aliases: None` at `+59 min` post-GHSA (the watch item).
- GHSA `GHSA-m6jr-rmfr-29w4` critical, scope `= 1.0.0` exactly, published `12:31:16Z`, description = kam193 source text verbatim = mirror, not independent research.
- The 111th sweep read `17900` as `404` inside a window that opened AFTER the `11:17Z` import — edge-cache or query-position. Self-capture: with `published` backdating standard on this lane, a resume-id `404` inside a live window proves nothing; extend the probe window past the tick, not to it.

## Disposition

- PyPI: LIVE at check. Monitor quarantine clock (rung watch vs the npp-ml `25 h 20 m` slow-rung record).
- Registry-side: monitor re-registration of the campaign under a costume sibling (`marocolor` + adjective/noun grammar), Telegram token/chat reuse in other packages (the literal hunt keys above), and whether the campaign gets curated-PR coverage.
- Advisory-graph-side: the aliases join-vs-never decision at `+2 h`/`+24 h` — feeds the model-v3 boundary for every OSV-first record class (curated `17893`–`17896`, machine `17898`/`17899`, kam193 `17900`).

## Related pages
- [robdotty / @flexmr creditslib cohort](../tools/robdotty-flexmr-offregistry-url-deps-creditslib-npm-october-2026.md#october-16-sixth-day-repull) — same-sweep sixth-day registry re-check + the never-join test handoff
- [algamil7x stream page, 112th sweep](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-twelfth-sweep)
- [CL-UNK-1211 AI-generated payloads](cl-unk-1211-ai-generated-payloads-linux-government-espionage-unit42-october-2026.md) — the operator-addressed AI-comment tell class
- [Telegram chat_id dependency-confusion recon cluster](telegram-chatid-1064260758-dependency-confusion-recon-cluster-september-2026.md) — the Telegram-bot-literal hunt-key precedent

## Sources
- OSV `MAL-2026-17900` (kam193 source, campaign `2026-10-marocolor`): <https://osv.dev/vulnerability/MAL-2026-17900>
- GHSA `GHSA-m6jr-rmfr-29w4`: <https://github.com/advisories/GHSA-m6jr-rmfr-29w4>
- kam193 bad-packages entry: <https://bad-packages.kam193.eu/pypi/package/marocolor>
- PyPI project page: <https://pypi.org/project/marocolor/> (LIVE at check)

## <a id="october-16-quarantine-third-origin"></a>October 16 one-hundred-and-fifteenth sweep: THE QUARANTINE CLOCK STOPS AT `≈42–43 h` — **`pypi.org/pypi/marocolor/json` `404` + `/simple/marocolor/` `404` = REMOVED FROM THE INDEX (was `200` LIVE at the 113th's `≈15:4xZ` read) — BUT `files.pythonhosted.org` STILL SERVES THE SDIST (`302`→`200`, `1,895 B`, bytes match the recorded `3709dd05…` family) = PARTIAL ENFORCEMENT SHAPE: index removed, asset alive** — AND the record itself moved for the first time: OSV `modified` broke its `11:45:05Z` freeze with a THIRD ORIGIN, `amazon-inspector` (`IN-MAL-2026-021507`, import `15:40:45.925Z`, modified-time `15:25:33Z`) carrying its own independent payload write-up; `aliases` STILL `None` at `+5 h 59 m`; and the GHSA mirror re-stamped `updated_at 18:30:33Z` WITHOUT taking the third-source text into its description = **mirror updates are partial-metadata, not wholesale syncs**.

**Registry state `≈19:3xZ` Oct 16:** `https://pypi.org/pypi/marocolor/json` `404`, `https://pypi.org/simple/marocolor/` `404` (`404 Not Found` body), while `https://files.pythonhosted.org/packages/source/m/marocolor/marocolor-1.0.0.tar.gz` `302`→`200` serving the real `1,895 B` gzip. The human project page returns a `Client Challenge` interstitial at this wiki's check — honest record, the `404`s are the JSON-API + simple-index canonical surfaces this ledger's quarantine rule keys on. **Quarantine clock: `≈42 h 20 m`–`43 h` post-flag — NEW SLOWEST kam193 RUNG, bracket closed at sysdiagd `≈25 min` / fromthehotel-poems `≤1.5 h` / fontcase `≈75 min` / minecraftaccfinder `≈2 h` / npp-ml `≈25 h 20 m` / marocolor `≈42–43 h` — and the hunt rule gains a corollary: after quarantine, the simple-index `404` is the removal signal, but tarball URLs can outlive it — a pinned direct-URL consumer is still installing.**

**Third-origin read (advisory-lane durable):** `database_specific.malicious-packages-origins` now carries THREE entries for one version — kam193 `38b0fa2e…` (import `11:17:07Z`), kam193 `8492279…` (`11:41:03Z`, the analyst-revision pair), and `amazon-inspector` `8206a6d3…` (`15:40:45Z`, id `IN-MAL-2026-021507`) — the first independent-house confirmation of this campaign on the OSV record itself, and the `modified` field proves the never-join rule does NOT mean the record is frozen: origins join at any age, aliases never do. GHSA-side at the same read: `severity critical`, `github_reviewed_at = published_at 12:31:16Z`, `updated_at 18:30:33Z`, description STILL the kam193-only text, `withdrawn_at` null, range `= 1.0.0`, no CVE. Monitor: whether the GHSA description ever absorbs the amazon-inspector detail; `marocolor`-sibling names in campaign `2026-10-marocolor`; whether the pythonhosted asset is eventually purged. Full sweep context → [115th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-fifteenth-sweep).

## <a id="october-16-plus2h-checkpoint"></a>October 16 one-hundred-and-thirteenth sweep: THE `+2 h` NEVER-JOIN CHECKPOINT PASSES — `MAL-2026-17900` reads `aliases: None` at `+2 h 53 m` behind `GHSA-m6jr-rmfr-29w4` (re-verified via API: critical, `published_at 12:31:16Z`) with OSV `modified` frozen `11:45:05Z` — no third origin, `published` still `10:38:53Z`. The importer batchers ran TWICE inside the gap (the `13:27:21Z`/`13:30:04Z` ticks minted `17901`/`17902` and touched their `modified`, never `17900`'s) = this is not sleep, it is design: **model v3 (alias join = machine-lane birth-only) holds on the ledger's own fresh controlled record; the Oct-9 kam193 retro-join precedent retires as a query-route artifact**. `aliases`-keyed consumers stay blind to a mirror that has existed for nearly three hours. `marocolor` `200` LIVE on PyPI (JSON + simple-index, `1.0.0` wheel+sdist) = `≈40 h 10 m` installable since flag, slowest kam193 rung still growing. Final `+24 h` checkpoint Oct 17 `≈12:31Z`. Full sweep context → [113th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-thirteenth-sweep).
