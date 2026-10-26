# dsh-native / @keer1024/dsh-native — the seizure took the bare name; the maintainer's scoped twin was born 53 minutes before the advisory and lives

## Tags
- ops
- npm
- supply-chain
- malicious-package
- seizure
- scoped-name
- grammar-drift
- native-binary
- infostealer-ambiguity
- this-wiki-forensics

## Summary

`MAL-2026-18315` / `GHSA-x94m-hxm5-m298` (`critical`, `Malware in dsh-native`) minted `2026-10-26T02:17:08Z` — alias AT BIRTH — advising npm `dsh-native` **exactly one version `1.4.1`** (`ranges None`). At capture the bare name is seized in a disposition grammar this ledger has not previously catalogued: **ROLLBACK-TO-STAGE** — `latest` points at the `0.0.0-stage` stub, there is NO `0.0.1-security` holder rung, the `1.4.1` version object is deleted while its `time`-map entry survives, and the `1.4.1` tarball `404`s (jsDelivr versioned `404`, stage rung `200`). This is a THIRD disposition shape: holder-costume (the CSS/Tailwind trio), rollback-to-legit (`w-mousekey 1.0.40`), and now rollback-to-stage.

The sweep headline is not the seizure — it is what the seizure left alive. **`@keer1024/dsh-native`** — same maintainer `keer1024 <keer_mail@163.com>`, same staging grammar — was **created `2026-10-26T01:23:54Z`, `0.0.0-stage` the same second, `1.6.1` published `01:26:03Z`**: the scope was born `≈53 min` BEFORE the bare name's GHSA, carries a HIGHER version (`1.6.1 > 1.4.1`), its tarball answers `200` (`1,082,590 B`), and OSV-query returns `{}` — ZERO advisories of any kind. npm `maintainer:keer1024` search total `2` = both twins visible on the public search lane.

## The two packuments, side by side

| | `dsh-native` (seized) | `@keer1024/dsh-native` (live) |
|---|---|---|
| created | `2026-10-22T08:05:17Z` | `2026-10-26T01:23:54Z` |
| rungs | `0.0.0-stage` + `1.4.1` (`08:06:16Z`) | `0.0.0-stage` + `1.6.1` (`01:26:03Z`) |
| dist-tags | `latest = 0.0.0-stage` | `latest = 1.6.1` |
| `1.x` tarball | `404` (21 B) | `200`, `1,082,590 B`, sha256 head `88300be7…` (static read ONLY, NEVER executed) |
| jsDelivr `1.x` | `404` | not probed this sweep |
| advisories | `GHSA-x94m-hxm5-m298` + `MAL-2026-18315`, critical, `= 1.4.1` only | none — OSV query `{}`, ZERO GHSAs |
| modified | `02:16:38Z` (seizure minute, `−30 s` before the GHSA) | `01:26:04Z` (publish second) |

GitHub `users/keer1024` answers `200` (the account is NOT gone, unlike the `@s4yhiitestpoc` case one sweep prior); npm doc route `~keer1024` answers `403` under the standing doc-route blanket — doc verdicts VOID, packuments are ground truth.

## Static extract of the live scoped tarball (NEVER executed)

Eleven files, `type: module`, zero dependencies, ZERO lifecycle hooks (scripts are `check` + `pack:check` only). The artifact ships a **Windows native binary `bin/dsh-rust-worker.exe` (`2,276,864 B`)** and a `144 KB` `index.js` with `37` `child_process`-family call sites; the only URL in either JS file is `http://127.0.0.1`. `exe` strings advertise a shell-execution engine: `DSH_RUST_SHELL` env override, full `pwsh.exe`/`powershell.exe` path ladder, `cmd.exe /e:ON /v:OFF /d /c`, and a defensive-looking `Get-CimInstance Win32_Process … -EncodedCommand … Stop-Process` cleaner. The manifest is a `dsh`/cordis plugin (`@deepseek-ai/dsh-client-*` inject slots, `cordis.patch.yml`) — a "resident Rust worker" tool for a DeepSeek-family chat client. **No obfuscation, no external collector, no install hooks were found statically** — this reads as a plausibly-legit tool, and this wiki asserts NOTHING about operator guilt.

What is asserted is the GRAMMAR coincidence and the clock overlap: `0.0.0-stage`-then-instant-rung staging (the era's ladder signature), version-jump succession (`1.4.1 → 1.6.1`), scope birth inside the same importer-active window (`01:23:54Z` sits between the `01:34Z` seizure burst's staging minutes — the scope was created `10 min` before the `util-foriepft` burst and `53 min` before its own bare twin's GHSA), one throwmail-pattern maintainer across both names.

## Why it matters (durable reads)

- **Enforcement seizes NAMES, not FAMILIES.** When a bare name dies, enumerate `maintainer:<name>` on the search lane and check every scoped sibling — the successor can be born before the advisory that buries its predecessor and inherit the userbase by name-similarity while carrying ZERO machine record. Consumers keyed to the GHSA/OSV name never see the migration.
- **ROLLBACK-TO-STAGE is now a named disposition**: `latest` → `0.0.0-stage`, no holder rung, version object deleted, time-map entry surviving, tarball `404`. Registry-state vocabularies that only know holder-costume and rollback-to-legit will misfile this as "weird empty package" and miss the seizure entirely. The `0.0.0-stage` stub survives as enforcement's own leftover grammar (law holds, second sweep since its naming).
- **A scoped name bearing a native `.exe` + a shell-exec engine + zero advisories is a blind spot in every advisory-keyed blocker**: there is nothing to block on until someone advises it. Detection must key on publisher-adjacency and staging-grammar, not verdicts.
- Ambiguity is reported, not resolved: legitimate rename-away-from-trouble and campaign re-arm produce byte-identical registry states — the same absent-operator/armed-automaton ambiguity class, one level up (name-level → family-level).

## Hunt guidance

- `npm view` / maintainer enumeration on ANY newly-seized name: `search?text=maintainer%3A<name>` — flag scoped rungs created within `≈24 h` of a sibling seizure.
- Scope names shipping `bin/*.exe` with zero advisories + `child_process` density: verdict-free native executables are the class URL-reputation and advisory-blocking both miss.
- Strings hunt on this family: `DSH_RUST_SHELL`, `dsh-rust-worker`, `cordis.patch.yml`, `dsh-plugin` keyword.
- Tripwire (re-arm watch): does `dsh-native` 1.4.x reappear under either name; does the scoped name ever mint an advisory (its twin's critical GHSA now PREDICTS it on the join-lane law); does `@keer1024/dsh-native` `modified` move off `01:26:04Z`.

## Disposition at capture (Oct 26 ~03:2x–03:5x UTC, 212nd sweep)

- Bare `dsh-native`: seized, rollback-to-stage, all payload `404` (registry + jsDelivr versioned), stage stub `200`, GHSA+OSV both live, `= 1.4.1` scope only — rungs BELOW `1.4.1`: packument shows none other than stage. `modified 02:16:38Z` = seizure `≈30 s` BEFORE the GHSA mint (`02:17:08Z`) — publish→seizure again outruns the advisory lane.
- Scoped `@keer1024/dsh-native`: LIVE, `latest 1.6.1`, tarball `200`, ZERO advisories, `aliases`-lane empty, untouched at second read `≈2.2 h` post-publish.

Sweep context → [212nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-second-sweep) · [wave-two 212nd](testmetest-wave-two-shadow-registry-gist-loader-oast-beacon-october-2026.md#october-26-212nd-the-plane-holds-and-the-window-arrives)
