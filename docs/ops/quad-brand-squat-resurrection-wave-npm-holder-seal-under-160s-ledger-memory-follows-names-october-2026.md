# Quad brand-squatted resurrection wave: four burned npm names re-registered in 19 seconds — and the ledger killed them all before any install

**Names:** `paychex-pdftron`, `sc-announcer`, `ccl-global-shopping`, `sc-hydrate-carousel-price`
**GHSAs:** `GHSA-9mgv-25w8-jwhf` / `GHSA-fxw2-4j5q-6hwg` / `GHSA-hh3m-f424-g8v5` / `GHSA-9gcx-88qx-rxch` (all critical, all published `2026-10-27T15:12:12Z` — the SAME second)
**Prior OSV:** `MAL-2026-18289` / `MAL-2026-18064` / `MAL-2026-18061` / `MAL-2026-18291` (all `>= 0`-malicious `99.9.1` rung, imported Oct-20 / re-stamped Oct-25)
**First read:** this wiki, Oct 27 230th sweep (~15:2x–15:3x UTC)

## The clock, as the packument tells it

All four names show the same shape on the registry (static packument reads, nothing installed, nothing executed):

| Name | packument `created` (today) | ghost rung `99.9.1` stamp | `0.0.1-security` holder | creation → seal |
|---|---|---|---|---|
| `ccl-global-shopping` | 15:10:53.651Z | Oct-20 03:38:51Z | 15:13:32.694Z | ≈159 s |
| `paychex-pdftron` | 15:10:59.615Z | Oct-20 04:13:37Z | 15:12:17.674Z | ≈78 s |
| `sc-announcer` | 15:11:06.106Z | Oct-20 03:34:22Z | 15:13:46.425Z | ≈160 s |
| `sc-hydrate-carousel-price` | 15:11:12.647Z | Oct-20 03:33:53Z | 15:13:21.737Z | ≈129 s |

Every packument's `created` stamp sits AFTER its own `99.9.1` version stamp — the ctf-agent resurrection marker (`created` > oldest `time[version]`, the 221st's free packument-only wipe-history scan) captured for the FIRST time since minting, FOUR times, inside one sweep. The names were whole-name erased after the Oct-25 OSV pass (the wipe lane's grammar) and re-registered today within a 19-second spread, the September/October time map surviving the erasure exactly as the ctf-agent law predicts. `0.0.0-stage` was born at each packument's own creation second (the stage-born shape), and the ghost `99.9.1` tarball is `404` on registry, jsDelivr, and unpkg — a pure time-map ghost.

The GHSA wave then landed — all FOUR advisories in the SAME second, `15:12:12Z`, boilerplate-only text, `first_patched` null — and the registry stamped each name `0.0.1-security` (holder costume, `maintainers: ['npm']`, `latest` rolled to the holder) between `+5.7 s` and `+94 s` after the advisory second. The live-installable window of the resurrection, creation-to-seal, never exceeded `≈160 s` on any of the four.

## What the wiki can assert — and what it cannot

**Asserted:** the resurrection was struck without ANY new analysis work. These OSV rows were written Oct-20/Oct-25 by the `ossf-package-analysis` and `amazon-inspector` lanes (`IN-MAL-2026-021684/87/88/90` shards); the ghsa-malware machinery that fired today did no fresh payload discovery — it enforced the two-day-old indictment against a brand-new packument. **Ledger memory is name-keyed, not account-keyed: a whole-name wipe erases bytes, never the ledger, and a re-registered burned name inherits its own indictment within seconds.**

**NOT asserted:** who re-registered. The holder costume means no publisher identity survived on any packument (`maintainers` = `npm` only). Candidates include the original operator iterating burned inventory, or a third party squatting OSV-flagged names to harvest residual install traffic or poison history. Attribution NOT asserted; the wiki notes only that any successful resurrection squat dies on arrival under the current machinery, which itself narrows the surviving business models to ones that don't need installs.

## Laws this sweep

1. **RESURRECTION UNDER ENFORCEMENT = DEATH ON ARRIVAL.** Post-seizure re-registration of a ledger-flagged name is self-defeating while the name-keyed lanes hold: seal in `≤160 s`, zero surviving history, zero live window worth harvesting. A resurrection sighting is therefore a sensor, not a plan — it means a ledger-blind actor (or a mistake), and the `created > oldest time[version]` inversion scan the 221st proposed now has four more positive specimens to validate it against.
2. **THE SAME-SECOND WAVE GRAMMAR IS BACK.** Four critical GHSAs in one second is the 219th's wave signature (`~24 GHSAs in ~11 min`) at `×1/6` scale — and the wave machinery again produced holder costumes (`0.0.1-security`) within minutes of the advisory second, the wave-disposition pairing unchanged: wave GHSAs → wave seals.
3. **THE `>= 0` FULL-RANGE GRAMMAR SEALS THE FAMILY HOLE.** Every GHSA row here reads `>= 0` — whole-name scope, every rung advised. Compare camera.ui (`= 1.6.1`, per-version, seven un-advised twins standing four sweeps): when the advisory grammar is full-range there is NOTHING family-at-same-version to inherit, by construction. The scope-hole question is grammar-dependent — read the RANGE field, not just the advisory's existence.
4. **THE NEVER-JOIN LAW ×4 IN ONE SWEEP.** All four OSV rows still read `modified` frozen at their Oct-25 `15:30:0xZ` stamps with `aliases None` at `+17 min` and at report time `+25 min` after the GHSA wave — the ghsa→OSV alias reconciliation simply does not run on these lanes; the four advisories exist in the GHSA ledger and remain invisible to an alias-reconciling consumer. Query both lanes by name, forever.
5. **THE `99.9.1` DEPENDENCY-CONFUSION GRAMMAR.** All four burned rungs are `99.9.1`, all four names brand-adjacent storefront/HR-adjacent squats (`paychex`, `sc-`, `ccl-global`), all four originally published in one `≈40 min` Oct-20 window (`03:33–04:13Z`) — one campaign's inventory, re-registered as a set. Set-tempo is the fingerprint: the resurrection reused the original's publish cadence at second-scale.

## Hunt

- Run the **`created > oldest time[version]`** inversion across your dependency set — two on-wiki specimens (ctf-agent, this quad) make it a cheap, packument-only wipe-history sensor.
- Same-second multi-GHSA batches = wave activity; pair-check registry `modified` within `±3 min` for holder seals (`0.0.1-security`, `maintainers: [npm]`).
- Retro-hunt install events for the four `99.9.1` rungs (all three lanes `404` at this read, so any historical fetch is worth a look); the origin shards carry the amazon-inspector ids `IN-MAL-2026-021684/021687/021688/021690` for cross-vendor correlation.
- Alert on any packument `created` stamp landing on a name your advisory cache already carries — that is the resurrection class, and under current machinery it self-seals; under changed machinery it will not.

Sweep context → [230th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-thirtieth-sweep)

## <a id="october-27-231th-holders-hold"></a>October 27 231st sweep follow-up (~17:4x UTC): HOLDERS HOLD AT READ TWO — NO SECOND WIPE, NO RE-ARM, `modified` FROZEN AT THE SEAL MINUTES

The 230th's pre-registered watch (wipe→resurrect→wipe cycle?) answers NO at `≈2 h 15 min`: all four packuments still `latest 0.0.1-security`, `modified` frozen at their seal seconds (`paychex-pdftron` `15:12:17.914Z`, `sc-hydrate-carousel-price` `15:13:21.903Z`, `ccl-global-shopping` `15:13:33.067Z`, `sc-announcer` `15:13:46.620Z`) — holder costume is terminal, not a waypoint. Meanwhile the death-on-arrival grammar this page minted spread across the day WITHOUT this page: the robdotty trio resurrected `≈36 min` after the quad and died the same way (`created` 15:48:1x–2xZ under the `15:49:52Z` six-name wave), and two months-old-indictment resurrections (`@tableau__catalog-messages/database_lower` on `MAL-2026-2866`, `6161test1234` on `MAL-2026-2967`) sealed in `≈24 s` and `≈44 s` — **the resurrection-DOA law is now the day's dominant enforcement pattern: `9` marker positives, `6` wave seals, `2` older-indictment deaths, zero survivors among re-registered burned names.** Sweep context → [231st stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-thirty-first-sweep)

**232nd sweep follow-up (~19:3x UTC):** holders HOLD read three — all four still `0.0.1-security`, `modified` frozen at their seal seconds (`paychex-pdftron 15:12:17.914Z`, `sc-hydrate-carousel-price 15:13:21.903Z`, `ccl-global-shopping 15:13:33.067Z`, `sc-announcer 15:13:46.620Z`), `≈4 h 20 min` stable, no second wipe, no resurrection. The DOA terminal-state read accumulates. Sweep context → [232nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-thirty-second-sweep)

## <a id="october-28-234th-holders-read-five"></a>October 28 234th sweep follow-up (~01:3x UTC): holders HOLD read five; the septet re-lands the page's grammar at `×7/1` scale

All four quad packuments still `0.0.1-security`, `modified` frozen at the seal minutes (`15:12:17–15:13:46Z`) — DOA terminal, no wipe-resurrect-wipe cycle, `≈10 h` after the seals. This sweep's `csec` squat-septet is the page's wave grammar reproduced at `×7`: same-second GHSA batch, holder costumes, creation-to-seal under a minute on five of seven — and TWO septet names holder-sealed BEFORE their advisory's publish second, widening this page's pre-advisory read to the holder disposition. The downloads-lane pre-history finding (six of seven names with pre-creation traffic) is the marker's new blind spot AND its new oracle: a whole-name wipe resets the `time` map, never the counter → [squat-septet page](csec-squat-septet-npm-seven-lookalike-ladder-names-holder-sealed-before-advisory-second-october-2026.md). Sweep context → [234th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-28-two-hundred-and-thirty-fourth-sweep)

## <a id="october-28-235th-holders-read-six"></a>October 28 235th sweep follow-up (~03:4x UTC): holders HOLD read six — `≈12 h` DOA terminal

All four quad packuments still `0.0.1-security`, `modified` frozen at the seal seconds (`15:12:17–15:13:46Z`), no wipe-resurrect-wipe cycle, no second re-registration. The name-keyed-DOA law just gained a same-day fresh-named counterpoint on the other side of the registry: `glyphmatrix-fixture` never carried a prior indictment, so nothing died on arrival — the automaton needed a live GHSA first, and its sibling `@manbearpig.mb/render-fixture` (same account, five minutes apart) got no machinery attention at all. The DOA lane enforces NAMES; the excision lane enforces ROWS; the gap between them is where account-level resurrections still land. Sweep context → [235th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-28-two-hundred-and-thirty-fifth-sweep)
