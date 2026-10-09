# `ig-gox` (PyPI) — a "Gox Secure Runtime Engine for Android Termux" that is really an import-time, anti-analysis, HMAC/XOR/zlib, in-memory-`exec` loader whose real payload NEVER ships in the package: this wiki statically unpacked both layers (no execution) and found device-gated remote fetch from `https://goxtools.shop/api` — a license server that is LIVE and answering structured JSON at check — with zero OSV + zero GHSA coverage on either lane

## Tags
- tools
- supply chain attack
- PyPI
- Python
- Termux
- Android
- in-memory execution
- exec compile
- XOR obfuscation
- zlib
- HMAC gating
- anti-debugging
- anti-frida
- anti-decompiler
- remote payload loader
- license server C2
- kill switch
- device fingerprinting
- goxtools.shop
- HyperGox
- hit bot tooling
- curated lane
- ossf malicious-packages
- zero advisory coverage

## What it is

`ig-gox` is a single-version PyPI package (`1.0.0`, uploaded **2026-10-09T00:29:07Z**, sdist 8,277 B / wheel 8,298 B) sold under the summary *"Gox Secure Runtime Engine for Android Termux."* Its README tells users to `pip install ig-gox`, create a file literally named `ig-hitter.py`, and `import ig_gox`. On that single import, without any function call, the package de-obfuscates and executes an operator-controlled core in memory.

This wiki pulled both artifacts from PyPI files immediately after curated PR #1610 (`ossf/malicious-packages`, reporter `justkorean1681`, opened 2026-10-09T02:53:27Z) filed the name, and de-obfuscated statically — **no execution of any package code, at any point**:

- sdist `ig_gox-1.0.0.tar.gz` sha256 `abbc60f89180a06b6a1a25d8dbf53b41c74eded9a1a78cd1b7933c0e71044146`
- wheel `ig_gox-1.0.0-py3-none-any.whl` sha256 `60c9d54df93424745b88a586d2ee7e0e6bb4eb537c247e4cc60cfd435d67053a`

## The loader anatomy (this wiki's static unpack)

### Layer 0 — `ig_gox/__init__.py` (runs at import)

1. **Anti-analysis gate (`_0x2e7b`, executed unconditionally at import):** exits silently if `sys.gettrace()` is set; exits if `builtins.exec`/`eval`/`compile` have been replaced/instrumented; exits if the lowercase concatenation of `os.getcwd()` + `sys.argv` contains any of `uncompyle`, `pycdc`, `decompyle`, `deobfuscate`, `hook`, `frida`. The payload refuses to run under debuggers, Python decompilers, instrumentation frameworks, and hooking tools — and refuses silently (`sys.exit(0)`), so an analysis box sees a clean no-op instead of a refusal.
2. **Integrity + decryption:** a 5,059-byte base64 blob is HMAC-SHA256-verified under an embedded key (`126f1e31…`) before use — the blob the wiki retrieved verifies (`hmac ok True`); a mismatch exits silently (anti-tamper: a modified copy will not run). The blob is then XOR-decrypted with a 32-byte key (`ca8dd4a1…`) and zlib-decompressed **entirely in memory**.
3. **Execution:** `exec(compile(core, "<gox_core>", "exec"), {...})` under a fake filename with `__name__ = "__main__"` — nothing ever touches disk; stack traces point at `<gox_core>`, not at any file.

### Layer 1 — the `<gox_core>` "GOX SECURE RUNTIME LOADER" (18,207 bytes, this wiki decoded statically)

- Its own header ASCII-art banner: *"Downloads encrypted payload from hosting, decrypts in-memory, and runs without touching storage disk."* — the operator's own description of a second, REMOTE stage.
- **Second obfuscation layer:** the core re-keys everything through another XOR string codec (`_0xds`/`_0xdb`, key `4c4e8273…`) — all sensitive strings (URLs, tokens, handles) exist only as XOR'd byte arrays until runtime. This wiki decoded them statically; see IoCs.
- **Platform gating:** `is_genuine_android()` via `ANDROID_ROOT`/`getprop`, plus emulator detection (`bluestacks`, `bignox`, `droid4x`, `changwan`, `genymotion`, `goldfish`, `google_sdk`, `/dev/qemu_pipe`, `/dev/goldfish_pipe`, `/dev/socket/qemud`, hypervisor cpuinfo) — refuses non-Android/sandbox environments with "Only Andoird Allowed, Contact @HyperGox" (sic). The payload targets real phones under Termux and evades desktop sandboxes/detonators.
- **Device fingerprint:** HWID = `{android_id or 'default_android'}:{model}` — sent to the server on both rails.
- **Two network rails to `https://goxtools.shop/api`:**
  - `GET /admin/licenses.php?action=validate` — license check keyed to the device HWID;
  - `GET /admin/storage.php?action=download&device_name={device_name}` — **fetches an encrypted base64 payload PER-DEVICE**, `X-Admin-Token` in the request headers, fake Chrome-on-Android-14 User-Agent, `requests` with `urllib` fallback "to ensure maximum resilience."
- The fetched stage is then decrypted in memory and executed — **the actual capability of this package is whatever the server returns for your device, at the moment it returns it.**

## Why this matters regardless of intent

The gray-market reading is on the surface: this is sold as a DRM-protected "hitter" (bot/hit) tool for the GoX/Telegram-adjacent economy — license server, Telegram-handle support (`@HyperGox`), admin-key-gated backend. But every property of a commercial DRM spine doubles as attack infrastructure, and none of it is revocable by the person running `pip install`:

1. **The payload is server-side and per-device.** The license endpoint is simultaneously a kill-switch, a targeting system, and a **victim-HWID inventory** — the operator knows exactly which devices ran the tool and can serve different stages to different devices.
2. **The anti-analysis + anti-tamper + silent-exit stack** is there to protect the seller's IP — and is byte-for-byte the same stack commodity malware ships (anti-debug, anti-decompiler, anti-Frida, HMAC'd payload, in-memory exec, fake filename).
3. **A live remote-fetch + exec is a one-server-compromise-from-full-fleet primitive.** Anyone who takes over `goxtools.shop` (or coerces its operator) inherits code execution on every device that ever validates and downloads — with no package change to trigger any scanner.
4. **Zero coverage on both advisory lanes.** At check (~03:5x UTC Oct 9): zero OSV, zero GHSA (name-keyed, both lanes); curated PR #1610 open ~45 min; package LIVE and installable. The same sweep proved OSV-native → GHSA mirror lag runs hours and GHSA version-lags live artifacts (`pxnpm`) — coverage here could be days out while the server keeps answering.

This wiki asserts the **mechanics class** (import-time remote-exec spine under analysis evasion), not espionage-grade intent. Defenders should treat "gray-market Python tool with a live license server" exactly like a malware C2 for hunting purposes: the shape is identical, and only the current server response differs.

## Live infrastructure check (this wiki, Oct 9 ~03:4x–03:5x UTC)

- `goxtools.shop` → Cloudflare (AAAA `2606:4700:3037::ac43:b1fa`, `2606:4700:3031::6815:3358`); site root answers 403 challenge page.
- `GET /api/admin/licenses.php?action=validate` → **HTTP 401**, JSON body: `{"success":false,"error":"Admin API key required. Send via X-Admin-Token header or admin_key param.","error_code":"ADMIN_AUTH_REQUIRED","timestamp":"2026-10-09T03:49:12+00:00"}` — the backend is LIVE, structured, and actively serving within minutes of check. (No admin token used; no payload-fetch attempts against `storage.php` — this wiki does not poke the download endpoint with fabricated credentials beyond the passive read above.)

## IoCs

| IOC | Class | Notes |
|---|---|---|
| `ig-gox` (PyPI) 1.0.0 | package | uploaded 2026-10-09T00:29:07Z, LIVE at check, zero OSV + zero GHSA |
| `abbc60f89180a06b6a1a25d8dbf53b41c74eded9a1a78cd1b7933c0e71044146` | sha256 | sdist |
| `60c9d54df93424745b88a586d2ee7e0e6bb4eb537c247e4cc60cfd435d67053a` | sha256 | wheel |
| `goxtools.shop` / `https://goxtools.shop/api` | C2 domain | Cloudflare-fronted, LIVE, 401 JSON at admin rail |
| `/api/admin/licenses.php?action=validate` | C2 endpoint | HWID license gate |
| `/api/admin/storage.php?action=download&device_name=…` | C2 endpoint | per-device encrypted payload delivery |
| `gox_admin_47f4fad518100e2a711a38ed08d30d16` | embedded admin token | leaked via XOR layer this wiki decoded — reuse NOT tested against the live server |
| `gox_mobile_app` | app id | embedded |
| `@HyperGox` | Telegram handle | support/contact identity |
| `ig-hitter.py` | file name | README's own install recipe; hunt artifacts referencing it |
| `<gox_core>` | in-memory filename | appears in tracebacks/profiling of affected hosts |
| keys `ca8dd4a1…` / `126f1e31…` / `4c4e8273…` | obfuscation keys | layer-0 XOR, layer-0 HMAC, layer-1 XOR |

## Hunt rules

1. **Egress grep:** any non-browser process on Termux/Android hosts calling `*/admin/licenses.php` or `*/admin/storage.php` with an `X-Admin-Token` header is this class (the rails generalize — grep for the endpoint grammar, not the domain, since the shop can re-point).
2. **PyPI/package-approval rule:** a package that executes at bare `import` with zero call site AND phones a license server is an unauditable dependency regardless of category — the executable content is the server's, not the artifact's. Treat as remote-code-execution supply surface in policy terms.
3. **Anti-sandbox tell:** a Python package that exits 0 silently under a detonator but does nothing visible there is NOT benign — check for the `gettrace`/builtins-instrumentation/`frida`-in-argv gate grammar statically (this wiki's decode was ~20 lines of regex + XOR).
4. **Curated-lane watch:** #1610 is the second PyPI filing from `justkorean1681` inside 6 days after #1590 froze at ~122 h unmerged — curated filings for PyPI names can sit unmerged while the name stays live and uncovered; query both lanes by NAME, never by merged-PR status.

## October 9 same-day: OSV arrives naming the crime; PyPI quarantines; the C2 stays alive (this wiki, one-hundred-and-twenty-fourth sweep, ~11:2x–11:4x UTC)

- **`MAL-2026-17712` published 2026-10-09T09:21:11Z** — OSV source is **`kam193`** (`bad-packages.kam193.eu`), a named individual-analyst lane, NOT `ossf-package-analysis`; campaign tag **`2026-10-ig-gox`**. The OSV states the purpose the ledger could only infer from mechanics: **"The remote code is used to abuse Instagram service for mass fake account registration."** The Android/Termux HWID spine described above is therefore an **account-farm botnet backbone** — per-device stage delivery = per-device account credentials — and the `ig` in the name plus the embedded `ig-hitter.py` read accordingly. DRM reading above stands as the mechanics class; the motive read sharpens to platform-abuse farming.
- **GHSA lane: still ZERO** (`affects=ig-gox&type=malware` → 0 records at ~11:3xZ) — monitor whether the kam193 lane EVER mirrors to GitHub; if not, GitHub-side consumers never see this class via any query.
- **PyPI QUARANTINED** ≈6.5 h after curated PR #1610: simple index carries `pypi:project-status quarantined` with an EMPTY file listing, JSON API 404s. Registry death at ~09:5xZ.
- **C2 FOURTH LIVE OBSERVATION:** `goxtools.shop/api/admin/licenses.php` → `401 ADMIN_AUTH_REQUIRED` JSON, server clock `2026-10-09T11:27:55+00:00` = the server has outlived the package by ~6.5 h. The fleet of devices that installed 1.0.0 before quarantine still phones home.

## Related pages

- [algamil7x npm DNS-exfil recon cluster](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-9-one-hundred-and-twenty-first-sweep) — the hundred-twenty-first sweep that captured this unpack
- [kafka-roller / kafka-helmsman PyPI canary pair (hundred-eighteenth section of the same ledger page)](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-8-one-hundred-eighteenth-sweep) — the "advisory feed is a build trigger" + PyPI-native stream rules this name now extends
- [supplychain.local MemTensor worm](../ops/supplychain-local-memtensor-npm-pypi-go-worm-aikido-september-2026.md) — cross-ecosystem precedent for runtime-loaded, token-resolving Python execution paths
