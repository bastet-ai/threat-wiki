---
title: "sharpnes — crates.io Telegram tdata + Chrome extension-settings stealer (crows7781-glitch, Oct 9 2026)"
---

# sharpnes — crates.io Telegram tdata + Chrome extension-settings stealer

**Class:** malicious Rust crate (infostealer) — first crates.io name this ledger has carried end-to-end (publish → curated filing → OSV → GHSA → post-advisory iteration, all inside ~5 hours).
**Crate:** `sharpnes` 0.1.0–0.1.5 on crates.io · repository `github.com/crows7781-glitch/shortneer` (public at capture) · publisher `crows7781-glitch` (fresh account, no prior ledger history) · description: "The sharpnes project is a learn."
**Records:** curated [ossf/malicious-packages PR #1611](https://github.com/ossf/malicious-packages/pull/1611) (KunalSin9h, filed 09:59:33Z, **merged 12:19:17Z** — first merge since #1603) → OSV `MAL-2026-17713` (source **SafeDep**, modified 12:30:05Z, scope `introduced: 0` = ALL versions, CWE-506) → `GHSA-qq2r-xp7w-5r55` (published 12:31:16Z, ≈71 s after the OSV, blanket `> 0`).
**Status at this wiki's 13:2x–13:4x UTC check:** all five versions LIVE, none yanked, sparse index `sh/ar/sharpnes` 200, `static.crates.io` downloads 200. **crates.io has taken ZERO action ~1 h after dual-lane advisories.**

## Timeline (this wiki's verified registry/API clock, 2026-10-09 UTC)

| Time | Event |
|---|---|
| 08:43:04Z | 0.1.0 published (Chrome stealer present, not wired) |
| 08:52:03Z | 0.1.1 published — wires Chrome stealer into `shortname()` |
| 09:59:33Z | curated PR #1611 filed |
| 12:19:17Z | **PR #1611 merged** |
| 12:21:34Z | **0.1.2 published — 117 s AFTER the merge** |
| 12:30:05Z | OSV MAL-2026-17713 (SafeDep) |
| 12:31:16Z | GHSA-qq2r-xp7w-5r55 + GHSA-rhpj-mr3r-r4gg (ig-gox) in the SAME one-second batch |
| 12:31:57Z | **0.1.3 published — 41 s AFTER its own GHSA** |
| 12:42:40Z | 0.1.4 published — wires `func11()` into `shortname()` |
| 13:18:42Z | 0.1.5 published — ~47 min post-advisory, still live at check |

**This is the kafka-roller "advisory feed is a build trigger, not a stop signal" rule, first measured on crates.io.** The publish cadence accelerates THROUGH the advisory window (117 s after merge, 41 s after GHSA) and function names churn per release (`send_tg_trt` → `fghjikr0tyhu5`; Chrome path dead → wired as `func11`), which reads as active iteration against takedown pressure, not idle republish.

## Static unpack (this wiki, no execution; tarballs pulled from static.crates.io)

Tarball SHA-256 (first 16): 0.1.0 — · 0.1.1 `88ba6b69…` · 0.1.2 `58eb4ad2…` · 0.1.3 `871281ef…` · 0.1.4 `1ff14d96…` · 0.1.5 `85869522…`.

Call surface: everything runs ONLY when the exported `pub async fn shortname()` is called — no proc-macro, no build.rs, no install hook. In Rust this means the crate is inert until a consuming program calls it: dependency-graph presence is not execution; hunt consumers, not just the crate.

- `src/teleg.rs` (commented "telegram stealer", Windows-only paths): collects Telegram Desktop session data from `%USERPROFILE%\AppData\Roaming\Telegram Desktop\tdata` and `<drive>:\Telegram Desktop\tdata` across drives C–J, zips to `tdata_backup.zip`, uploads via Telegram Bot API `sendDocument` — bot ID `8775554963`, chat `-1003869029825` (bot auth secret not reproduced here; present verbatim in the crate source and the OSV IOC block).
- `src/data.rs` (commented "chrome stealer", cross-OS): locates Chrome `Default/Local Extension Settings` (extension state — the container for crypto-wallet extension vaults) on Windows/Linux/macOS via **XOR key `0xAA`-obfuscated strings with Chinese identifiers**; strings for `LOCALAPPDATA`/`HOME`/`USERS` decode cleanly under the key (this wiki verified); zips in memory and sends as `文件.zip` via a second bot (`8898886905`) to the SAME chat `-1003869029825`. In 0.1.5 the second bot token exists only in XOR-encoded byte-array form (this wiki re-encoded the known prefix and matched) — the OSV's two-token disclosure predates the crate's own self-concealment, i.e. the author is iterating against the exact analysis that produced the advisory.
- Dependency grammar (`Cargo.toml`): `teloxide` (Telegram bot framework) + `reqwest` + `dirs` + `zip` — the exfil stack, visible in the sparse index without downloading anything.
- Function-rename churn across versions (0.1.1 `send_tg_trt` → 0.1.3+ `fghjikr0tyhu5`, `gfhrt0jhu60x0rg`, `jk697uth`, `t6us`, `dfdrfhu0ytxzakr`, filename `fghjj5.zip`) = keyboard-mash identifiers, same class as the payload-name noise in npm campaigns on this ledger; the constant across ALL five versions is the chat ID.

## Durable rules

1. **Chat ID `-1003869029825` and bot IDs `8775554963` / `8898886905` are permanent grep IoCs** — the chat survives bot-token rotation; the same pattern that made the telegram-bot grammar durable on the Baileys/PhantomSub waves applies to Rust artifacts now.
2. **crates.io dual advisories do not stop publishing.** OSV blanket `introduced: 0` + GHSA blanket `> 0` mean Dependabot-class consumers DO see all five versions (the version-lag defect that bit `pxnpm` is absent here — blanket scope is the fix shape the npm lane should copy). The gap is the opposite kind: **advisory ≠ yank** — every version stayed installable at check; Rust consumers get a warning, not a wall.
3. **Rust-specific hunt note:** unlike npm import-time execution, this class needs an explicit `shortname()` call site; flag crates whose exported API is one meaningless-named async function with `teloxide`/`reqwest`/`zip` deps and zero documented use (description "The sharpnes project is a learn." = the tell).
4. **Same-day crate mortality check:** crates.io has no quarantine concept observed here (contrast PyPI's `ig-gox` quarantine the same morning, ~6.5 h post-PR) — expect Rust equivalents of delete-before-advise or, as today, advised-and-still-serving. Re-check yank state; a future yank is retro-coverage evidence, not safety.

## Monitor

- Yank/ deletion action on 0.1.0–0.1.5; whether 0.1.6+ keeps publishing advised. **State at the hundred-twenty-seventh sweep (~19:3xZ, ≈6 h post-dual-advisory): ZERO yanks, `max_version` still `0.1.5`, downloads 15→52 since the 125th — every Rust install path advised-and-serving for six hours and counting.**
- Re-registration under new crate names by `crows7781-glitch` / the `shortneer` repo grammar (`learn` description, mash identifiers, chat `-1003869029825`).
- Whether the second bot token's XOR form stays concealed in any future OSV re-issues.
- First sighting of `shortname()` call sites in downstream Rust projects (the actual victim path).

## Related pages

- [ig-gox PyPI loader page](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md) — the same-morning PyPI name whose kam193 OSV mirrored to GitHub in the identical 12:31:16Z GHSA batch
- [algamil7x ledger, one-hundred-and-twenty-fifth sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-9-one-hundred-and-twenty-fifth-sweep) — the sweep that caught the full advisory→publish race
- [kafka-roller / kafka-helmsman section (hundred-eighteenth)](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-8-one-hundred-eighteenth-sweep) — the advisory-as-build-trigger rule this crate replicates on its third registry
