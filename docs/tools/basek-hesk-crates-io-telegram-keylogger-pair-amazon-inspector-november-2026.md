# basek and hesk: two crates.io keyloggers born advised, one already gone

## Summary

- **What landed:** the first two `crates.io` rows since the `sharpnes` era arrived in the OSV lane at the `21:47Z` Nov-12 import, BOTH from **amazon-inspector** origins, in adjacent seconds: `MAL-2026-19200` `basek 0.1.0` (`21:47:36Z`) and `MAL-2026-19201` `hesk 0.1.0` (`21:47:28Z`). Zero GHSA either side (`affects=` zero-test `0` on both, controls must-hit), `aliases None`, no RUSTSEC entries.
- **basek is GONE, hesk is INSTALLABLE:** `basek` answers crates.io API `404`, sparse index `404`, download `404` = whole-name gone at read (~22:4xZ, `≈1 h` post-advisory). `hesk` answers `200` everywhere: crate API live, `created_at = updated_at = 2026-11-12T16:36:40Z` (single version, `9` downloads at read), tarball `200` `41,406 B`, sha256 `09bc0f16645e5dcc64f9a73d93e032bf4d347192ed541b9aeddfba7c87e68419`, sparse index `200` = **advised and installable right now**.
- **basek per amazon-inspector (row text):** Windows keylogger as a Rust LIBRARY — `get_data()` polls key states, batches keystrokes with the local username, POSTs to `api.telegram.org/bot<token>/sendMessage` with the token XOR-`0xAA` obfuscated and reassembled via a `ut!` macro, hardcoded `chat_id 7304091279`; secondary exfil `https://keylogger.nullsect0r.tech/log`. Full persistence kit: copy to `%LOCALAPPDATA%\WindowsSystemUtility\WinSysUtils.exe`, `HKCU\...\Run` value `WinSysUtils`, watchdog clone under a random 12-digit filename, `cmd.exe timeout+del` self-delete; `30 s` sleep + `20 s` observation-only warmup + polling jitter = deliberate sandbox evasion. The description's "educational cybersecurity project" framing is contradicted by every mechanism in the crate.
- **hesk per amazon-inspector, CONFIRMED on this wiki's own bytes:** two reachable async payloads (`dat` in `src/test.rs`, `bs` in `src/parse.rs`, both imported from `src/lib.rs`) walk `$HOME` with `walkdir`, zip via `ZipWriter` (wallet artefacts incl. `exodus.wallet`), upload via `reqwest` multipart to a hardcoded Telegram bot endpoint with embedded `API_` token + `chat_id`. The tarball read here shows the camouflage first-hand: `lib.rs` opens with the Russian comment `Это учебный проект для тестирования кибербезопасности` ("this is an educational project for cybersecurity testing") and the public surface is ~100 invented-name filler items (`Modemir65`, `apply_twice_torvak_78`, `shuffle_zelkvak_73`, `score_felrim_69`, `wexhesk_74`) around the two payload files (`parse.rs` ~40 KB, `test.rs` ~60 KB). Dependency set extends to cross-platform keylogging: `evdev`/`rdev`, `winreg` + `winapi` (winuser/processthreadsapi/memoryapi), `walkdir`, `zip`, `reqwest[multipart]`.
- **The naming law:** both names are squat-adjacent (hesk = Rust's flagship HTTP client crate name family; `basek` a one-letter mutation). Same-day, same-second-pair, same-inspector-origin = one publisher or one reporting sweep, NOT adjudicated.

## Durable hunt shapes

- **crates.io seizure lane is per-name, same as npm:** basek deleted within ~1 h of its advisory while hesk sits fully served — quarantine-before-read remains a DIFFERENTIAL, the advised-and-installable class is the base rate (the 256th/261st law re-attested on a fourth registry).
- **The filler-identifier camouflage is detectable pre-payload:** an `== 0 downloads`, single-version crate whose `lib.rs` re-exports exactly two async fns buried under ~100 nonsense identifiers is a shape a registry-side lint could catch at publish; watch for the grammar (`[A-Z][a-z]+[0-9]+` enum names + `verb_noun_[0-9]+` fns) in new crates.
- **Telegram-Bot-API-as-C2 keeps crossing registries** (the `sharpnes` tdata stealer used the same `api.telegram.org/bot<token>/sendMessage` shape with XOR-`0xAA`, Oct 9): the XOR-`0xAA` byte-array token encoding is now a recurring family tell across crates.io specimens.
- **amazon-inspector mints crates.io rows with forensic detail AT BIRTH** (chat IDs, endpoints, persistence keys) — unlike the PyPI kam193 rows one lane over, these advisories are the whole public forensics surface and they landed complete.

## Related on this wiki

- [sharpnes crates.io Telegram tdata stealer](sharpnes-crates-io-telegram-tdata-chrome-extension-stealer-crows7781-glitch-october-2026.md) — the XOR-`0xAA`/Telegram family precedent on this registry.
- [PyPI voice-synthesis wave two](pypi-voice-synthesis-wave-two-sixteen-advised-loaders-installable-kam193-november-2026.md) — the sixteen rows minted minutes before these two.
- [algamil7x stream, 261st sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-12-two-hundred-and-sixty-first-sweep) — full sweep record.

## Sources

- OSV API rows `MAL-2026-19200`/`19201` (reads ~22:4x-23:0xZ Nov 12); amazon-inspector origin hashes `f82b1f07...`/`83716a1c...` quoted from `details`.
- crates.io API `crates.io/api/v1/crates/basek|hesk`, download lane `.../hesk/0.1.0/download`, sparse index `index.crates.io/ba/se/basek` (`404`) + `he/sk/hesk` (`200`).
- Tarball bytes: `static.crates.io/crates/hesk/hesk-0.1.0.crate` `200 41,406 B`, sha256 `09bc0f16645e5dcc64f9a73d93e032bf4d347192ed541b9aeddfba7c87e68419`, contents + `lib.rs` read locally.
- RustSec advisory-db raw path for both names: `404` at read.
