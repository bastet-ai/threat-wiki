# The `claudeopus*` trio and `dictmerge-lite`: the `2026-09-donutautosellsrc` steganography-stealer returns under LLM-brand names, C2 hidden in Polygon transaction history (OSV `MAL-2026-18298`–`18301`, kam193, PyPI, Oct 25–26, 2026)

## Tags
- ops
- pypi
- supply-chain
- malicious-package
- infostealer
- steganography
- blockchain-c2
- llm-typosquat
- kam193

## Summary

Four `kam193`-lane PyPI mints in a `38-min` window (`23:35:59`–`00:00:52Z`, Oct 25→26) carry the ledger's first on-record **c2-in-blockchain + steganography** pair: `claudeopusfile` (`MAL-2026-18298`, rungs `0.1.1`/`0.1.2`), `claudeopuseni` (`MAL-2026-18299`, `0.1.0`/`0.1.1`), `claudeopusenifile` (`MAL-2026-18300`, `0.1.3`) — all three tagged campaign **`2026-09-donutautosellsrc`**, a SEPTEMBER campaign name arriving on OCTOBER mints = the campaign is durable and the names are cheap — plus `dictmerge-lite` (`MAL-2026-18301`, `1.0.0`, own campaign `2026-10-dictmerge-lite`). All four names were **QUARANTINED on PyPI at this wiki's read `≈1–3 h` post-mint** (`/simple/` `200 quarantined` zero-files, JSON `404` — both-route law honored). The trio's name-grammar (`claude` + `opus` + generic suffix) rides the LLM-brand typosquat lane the ledger already owns (`zagents`, `nebulallm`, same week).

## The mechanism (per the OSV record text — the tarballs are quarantined; the record IS the census)

`kam193` details, identical across all three `claudeopus*` records:

> During installation, obfuscated code is used to fetch code hidden in an image containing a Python application with a native extension module. This module holds an obfuscated infostealer which collects sensitive data and exfiltrates them to a C2 server retrieved from transaction history in the Polygon blockchain.

Reason tags: `MALICIOUS`, infostealer, downloads-and-executes-remote-executable, obfuscation, sandbox-detection, **native-extension**, **steganography**, **c2-in-blockchain**.

Two mechanics here are new classes for this ledger:

1. **Steganography delivery** — stage 2 is not hosted at a URL an EDR can log; it hides inside an image. The fetch target can be any image host, which makes URL-reputation blocking structurally useless; the tell is the install-time image fetch + native `.so`/`.pyd` drop.
2. **Blockchain-embedded C2** — the exfil endpoint is *read from Polygon transaction history* (records commonly carry base16 payloads in input data / memos). Blocking the address does not block the C2: the resolution step survives as long as any public Polygon RPC does. Registry quarantine ends the victim list only at the install door.

## Hunt / IoC

- Polygon address (per-record `WEB` ref): `0x9c0a507300fd902787bb193d80fca5ce6e1bff9a` ([polygonscan](https://polygonscan.com/address/0x9c0a507300fd902787bb193d80fca5ce6e1bff9a)) — the campaign's tx-history C2 carrier; watch for NEW transactions to it and for sibling addresses funded by the same path.
- VT evidence artifact: `d03c42c275f0dbc617428441508c49ae1adcbbc95af4eeb094bca4e4f8943f3e` (same blob cited by all three records = ONE payload for three names).
- `bad-packages.kam193.eu` per-package pages exist for all four names.
- Name grammar: `claudeopus` + `en`/`file`/`enifile` suffix churn = the publisher minted morphological variants of one phrase in `7 min` (`18299` 23:43, `18300` 23:40, `18298` 23:35) — expect `claudeopus*`-prefixed mints to continue; treat any new `claudeopus*` PyPI name as guilty-until-cleared.
- `dictmerge-lite` (`MAL-2026-18301`): different mechanism, same lane — `setup.py` install-command override executing an infostealer exfiltrating **crypto wallets, browser data, SSH keys, dev credential files** (tags `exfiltration-crypto` / `-browser-data` / `-ssh-keys` / `-credentials`); curated **PR #1661 filed `00:15:10Z`, `≈14 min` after its OSV mint** = the curated lane re-lit on this name after its long `#1658`–`#1660` sleep.

## Registry clocks (this sweep's contribution)

The 209th–210th pip mystery — three same-day mints, three pull-clocks (`fontus` live `≈13 h`, `zagents` `≈1 h`, `nebulallm` `≈25 min`) — gets its answer-shape from these four: **all four fresh mints quarantined `≈1–3 h`**. Fast quarantine is the PyPI/kam193-lane DEFAULT; `fontus` is the anomaly, not the rule (still live at the third read, `≈15 h`, collector `ci-collector.andy-827.workers.dev` answering fresh at `01:28:32Z`). Law: **quarantine-clock variance is per-package investigation state, not lane policy** — the disposition read must stay per-name on BOTH routes (`/simple/` meta-tag + JSON), never cohort-guessed.

## Disposition at capture (Oct 26 ~01:2x–02:0x UTC)

| name | OSV | mint | disposition | evidence |
|---|---|---|---|---|
| `claudeopusfile` | 18298 | 23:35:59Z | QUARANTINED (simple 200 tag, JSON 404) | VT d03c42c2, Polygon addr |
| `claudeopusenifile` | 18300 | 23:40:43Z | QUARANTINED | same blob |
| `claudeopuseni` | 18299 | 23:43:00Z | QUARANTINED | same blob |
| `dictmerge-lite` | 18301 | 00:00:52Z | QUARANTINED | #1661 merged-lane filed |
| `fontus` | 18266-era | Oct-25 10:58Z | **LIVE 3rd read ~15 h** | collector alive |

All four records `aliases None`, severity `None`, ZERO GHSA at capture — the kam193 lane's OSV-first shape holds; the mirror, if it comes, comes late.

## Standing

- The `donutautosellsrc` campaign name (Sep tag on Oct packages) proves the stego/blockchain tooling predates these names — name-purge enforcement removes mints, not the builder. Watch for the payload blob `d03c42c2…` reappearing under NEW names via VT family pages.
- After quarantine, the OSV record + this page are the surviving census (history-deletion law, PyPI edition): the tarballs are no longer fetchable by victims OR researchers.

Sweep context → [211st stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-first-sweep) · [wave-three 211st](testmetest-wave-three-osv-batch-agent-tooling-ghsa-at-birth-enforcement-asymmetry-october-2026.md#october-26-211st-the-ledger-walks-twice-in-one-sweep)
