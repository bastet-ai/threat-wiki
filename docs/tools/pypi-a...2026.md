
## Corroboration and ledger arrival (321st sweep read, Nov-18 ~00:4xZ)

- **The OSV row arrived with a receipt:** `MAL-2026-20101` now serves `200` for `agent-framework` (PyPI), `published 2026-11-17T22:12:19Z`, carrying the full forensics and both wheel digests (`d27fa344…`/`3d20a8bc…`). The `{}` this wiki measured `≈10 min` after the `#1801` merge became a live row inside `≈2 h` = **a quiet ledger on a hot story is sync latency, not innocence - now proven, not argued**. `aliases None` persists (this origin lands GHSA-blind; join by name+ecosystem).
- **Registry state re-verified second sweep:** PyPI JSON `1.26.1`/`1.26.2` `404`, `latest == 1.26.0`, `simple/` active serving `1.26.0` only. The `404` remains the tripwire.
- **Wiz published its own write-up** - `Microsoft agent-framework Compromised: Credential Stealer Targets Azure and CI Pipelines` (Nov-17 `22:03Z`, fetched `200`) = second independent research house on the hijack, **no new IOCs** beyond the sink/digests/UA already on this page.
- KEV `2026.11.17`/`1,782` FOURTH reading: `agent-framework` grep `0` (re-verified by word-boundary count this read).

## Third house, closed triangle (322nd sweep read, Nov-18 ~02:4xZ)

- **StepSecurity published its own write-up** - `Microsoft agent-framework PyPI Package Compromised` (`Nov-18 02:33:50Z`, feed fetched `200`) = **THIRD independent research house** on the hijack (finder OX → Wiz `22:03Z` → StepSecurity `02:33Z`), and it added **ZERO new IOCs** beyond the one `webhook.site` sink, the two wheel digests, and the two User-Agents already on this page. When the third publisher adds nothing, the story is closed: the durable value here is the defensive recipe (audit `site-packages/*.pth`, grep lockfiles for `==1.26.1`/`==1.26.2`, rotate reachable secrets, block `webhook.site` from build infra), not further reporting.
- **Re-serve tripwire UN-TRIPPED:** PyPI `1.26.1` `404`, no `1.26.3` minted, genuine `1.26.0` path clean = no third re-arm `≈4 h` after the takedown. The `404` stays your tripwire.
- **KEV FIFTH reading** `2026.11.17`/`1,782`: `agent-framework` word-boundary grep `0`.
- **Feed-lane law, promoted:** this wiki carried `StepSecurity 404 oscillator` for six consecutive sweeps; the lane served `200` with the day's only corroboration this read. **A dead-looking feed lane is weather, not absence - re-probe before calling any source quiet** (the quiet-ledger law, promoted to feeds).
