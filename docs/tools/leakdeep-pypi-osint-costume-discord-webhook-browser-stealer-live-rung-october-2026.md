---
title: "LEAKDEEP (PyPI): 'OSINT / Credential Leak Intelligence' costume wrapping a Windows browser+Discord stealer — LIVE after advisories, with an out-of-scope served rung (2.6.2) and a plaintext webhook behind a fake-XOR decoy"
---

# LEAKDEEP (PyPI) — OSINT-costume Windows stealer, advised fast, still installable, one served rung out of scope

**First wiki capture: October 18, 2026 (one-hundred-and-twenty-ninth sweep, ~03:2x–03:4x UTC).** OSV `MAL-2026-17921` (`leakdeep`, PyPI) is the first record to break the `17920` high-water after the 126th's nine-record tick — published `01:45:23Z`, imported `01:52:23Z` (amazon-inspector lane, origins `IN-MAL-2026-021510`–`021514`), with `GHSA-4pw5-gqh4-v2pj` (critical) following `03:31:13Z` — a `≈1 h 46 m` OSV→GHSA mirror clock measured live INSIDE this sweep. No press at capture: the analyst lanes are ahead of the news cycle on this name.

## What it is

Five rungs advised — `2.5.0`, `2.5.2`, `2.6.0`, `2.6.4`, `2.6.6` — every one the SAME code (this wiki sha256-verified the evidence files identical across the `2.6.4` and `2.6.6` wheels: `config.py` `fe0752ff…`, `cli.py` `abae927c…`, `core/system.py` `0634ec69…`; `2.6.4` wheel `bb0853ea…` matches the OSV `package_integrity` entry byte-for-byte). PyPI `Author: LeakDeep Intelligence`, summary *"Professional OSINT & Credential Leak Intelligence Framework"* — the costume:

- `cli.py` exposes a console script `leakdeep` (console_scripts entry point) with `-q/--query`; every invocation — ANY invocation — calls `SystemInfo.initialize_background_process()` BEFORE the fake search.
- `core/search.py` `SearchEngine.search()` is a stub: `time.sleep(0.5); return []`. The advertised product does not exist. Interactive mode prints *"Querying breached databases…"* then *"No records found"* forever.
- `core/system.py` spawns a daemon thread: copies Chrome/Edge/Brave `Login Data`/`Cookies`/`Web Data` SQLite files via `win32file.CreateFile` share-delete forcing, decrypts DPAPI-unwrapped AES-GCM keys from the `Local State` `os_crypt.encrypted_key` (`crypt.py`: strip 5-byte `DPAPI` prefix, `CryptUnprotectData`, AES-GCM `val[3:15]` IV), scans `%APPDATA%\discord*\Local Storage\leveldb` for Discord token/MFA regexes, screenshots (`Pillow ImageGrab`), wmic system inventory, `api.ipify.org` public IP, zips to `%TEMP%\ld_<epoch>\export_<user>.zip` and POSTs it to `get_webhook()`, then `shutil.rmtree` self-clean. Windows-only by import (`pywin32` in deps); `requests` dep for the exfil.
- **Exfil endpoint (IOC):** `https://discord.com/api/webhooks/1561071611430572052/fURAoSTpoCHWmZWij9W7kys2Lx7GlgM27F82eWPvvj45Tw7hR2-BW7iH5s95uY0oNejY`

## SELF-CAPTURE — the "XOR-obfuscated webhook" is a decoy; the real one is plaintext

The OSV/amazon-inspector source text says the webhook "is stored in `config.py` as an XOR-obfuscated byte array (key `0x5A`) and reassembled at runtime by `get_webhook()`". This wiki decoded `_ENC_HOOK` with key `0x5A` directly: the 366-byte array decodes to gibberish (`ljhfiad33ojiijho3iojah…`) — NOT the webhook, not any URL. `get_webhook()` returns the Discord webhook as a PLAINTEXT string literal; the array is never referenced. **Durable: fake-obfuscation is anti-analysis theatre — a decoder analyst who trusts the source-text framing spends the hunt on the decoy. Check what the function actually returns before chasing the array; and treat automated-source prose describing a mechanism as a lead to verify, not a fact to copy.**

## Registry state at capture (~03:3xZ, ~2 h after OSV, ~5 min after GHSA) — STILL FULLY LIVE

- simple index `200`, NO `project-status` quarantine meta, serves FIVE files: `2.5.2`, `2.6.0`, **`2.6.2`**, `2.6.4`, `2.6.6`.
- project JSON `200`, `latest = 2.6.6` (advised, still installable).
- **THE OUT-OF-SCOPE RUNG, LIVE AND SERVED: `2.6.2` appears in NEITHER OSV version list NOR the GHSA scope (GHSA lists exactly the five `= 2.5.0/2.5.2/2.6.0/2.6.4/2.6.6`), yet the registry serves its wheel (`ea/f2/24eb…`, `7,274 B`, uploaded `01:20:54Z`) and it is byte-different code territory from the advised rungs (unpulled — declared payload inferred same-lane, honestly recorded).** Set-difference at capture: advised FIVE (`2.5.0` + four served) vs served FIVE (`2.6.2` + four advised) — the intersection is FOUR. `2.5.0` is advised-but-not-served (dropped from the index between the `01:05:51Z`-era uploads and this read — the first rung vanished while the rest stayed), `2.6.2` is served-but-unadvised. The publish→advisory fast clock RANGS-COUNTED WRONG: uploads `01:05:51Z`→`01:34:48Z` ladder, OSV origins `01:45:23–55Z`, import `01:52:23Z` — the importer enumerated five rungs in `≈9 min` yet `2.6.2`, uploaded `01:20:54Z` BEFORE the origin stamps, is absent from both lanes. The out-of-scope-live-rung class (this ledger's `kmf`/`npp-ml`/`function-flag 4.0.0` lineage) reproduces on the FAST machine lane, not just the slow curated lane.
- Alias lane: `17921` `aliases None` at the ~5-min-post-GHSA read; `v1/vulns/GHSA-4pw5-gqh4-v2pj` GET `404` = never-join model v3 holds for this record too (one datapoint, edge-cache rule applies).

## Publish mechanics

All five upload times sit in a `28 m 57 s` window Oct-18 `01:05:51Z`–`01:34:49Z`, sdists+ wheels both uploaded per rung, version numbers skip `2.6.2` in the advisory but not the registry — the ladder reads scripted (version inflation + rapid re-upload, the `0.0.0-stage`-adjacent grammar without the stub). No project URLs, no homepage — costume-only metadata. No OSV/GHSA history under adjacent names at capture; monitor for sibling names (OSINT/leak/breach vocabulary).

## Defender notes

- Hunt: any `leakdeep` install (pip metadata, site-packages) on Windows hosts = credential-compromise triage (browser passwords/cookies/autofill + Discord tokens exfil), same posture as the `webreader`/`pafer` PyPI RAT class.
- Network: Discord webhook POSTs with `multipart/form-data` file fields named `export_<user>.zip` from python parent processes.
- The `2.6.2` rung and `latest 2.6.6` resolve to ADVISORY-INVISIBLE or installable states: version-pinning against "advised list" scanners under-reports here; treat ANY `leakdeep` version as hostile.

## Monitor

- npm/PyPI re-registration or sibling OSINT-costume names off the same author pattern; whether `2.6.2` (or a `2.6.8`) appears in either advisory later; quarantine clock vs the ukraine69 `≈2 h` registry-first fast path (leakdeep was live ~2 h at this read — compare at next sweep); alias join on `17921` (expect none, model v3); press arrival; webhook deletion state (not probed — webhook GET would signal the operator; left unread by choice, record-only posture).

Sweep context → [129th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-twenty-ninth-sweep).

## <a id="october-18-second-read"></a>October 18 one-hundred-and-thirtieth sweep: SECOND READ — STILL LIVE, PAST EVERY BENCHMARK

`simple/` serves `200` with `pypi:project-status` **`active`** and ten links — NOT quarantined `≈3.5 h` post-OSV, `≈2 h` post-GHSA — already past `ukraine69`'s `≈2 h` registry-first fast path; the remaining clock comparison is marocolor's slow-rung `≈42 h`. Served set UNCHANGED `{2.5.2, 2.6.0, 2.6.2, 2.6.4, 2.6.6}`: rung `2.6.2` served-but-unadvised holds in both lanes, advised `2.5.0` still absent from the index, JSON `latest 2.6.6` installable. Alias lane: `MAL-2026-17921` `aliases None` at `≈2 h 30 m` post-GHSA with `modified` frozen `02:00:13Z` = the FIRST over-`2 h` never-join datapoint on a GHSA-mirrored record — the lag-window excuse expires here; if the record stays `None` into tomorrow the 17900/marocolor permanent-never-join precedent extends to inspector-origin records too. Full sweep context → [130th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-thirtieth-sweep).

## <a id="october-18-third-read"></a>October 18 one-hundred-and-thirty-first sweep: THIRD READ — STILL LIVE AT `≈5 h 45 m` POST-OSV

`simple/` `200` `project-status active` — not quarantined `≈5 h 45 m` post-OSV / `≈4 h` post-GHSA = now DOUBLE ukraine69's `≈2 h` registry-first fast-path benchmark; served set unchanged `{2.5.2, 2.6.0, 2.6.2, 2.6.4, 2.6.6}` with `2.6.2` served-but-unadvised + `2.5.0` vanished, JSON `latest 2.6.6` installable. `MAL-2026-17921` `aliases None` at `≈4 h` post-GHSA, `modified` frozen `02:00:13Z` — the never-join datapoint doubles; marocolor's `≈42 h` slow-rung remains the only slower lane on the ledger. Full sweep context → [131st stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-thirty-first-sweep).

## <a id="october-18-fourth-read"></a>October 18 one-hundred-and-thirty-second sweep: FOURTH READ — STILL LIVE AT `≈6.5 h` POST-OSV, CLOCK-CROSSING CAVEAT RECORDED

`simple/` `200` `project-status active` — not quarantined `≈6.5 h` post-OSV / `≈5.8 h` post-GHSA; served set STILL `{2.5.2, 2.6.0, 2.6.2, 2.6.4, 2.6.6}` with `2.6.2` served-but-unadvised, JSON `latest 2.6.6` installable. `MAL-2026-17921` `aliases None` + `modified` frozen `02:00:13Z` = never-join `≈6.5 h`, triple the ukraine69 `≈2 h` benchmark. **Self-capture on the ledger's own comparison: leakdeep's open span has NOT yet crossed marocolor's `≈42 h` slow-rung benchmark — the marocolor asset-open span at this read is `≈31 h` on a name-DEAD lane, and spans across different lane classes are compared with the class difference stated.** Full sweep context → [132nd stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-18-one-hundred-and-thirty-second-sweep).
