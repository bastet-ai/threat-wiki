# `py2ops` (PyPI) — an "operator-linked companion shell" that ships a REAL Python REPL as cover, reads every console line with terminal echo switched OFF, hands bare single words to a server-side unlock gate, and self-registers the device to a baked C2 panel on first run — LIVE at `latest = 2.2.1`, ZERO OSV, ZERO GHSA, curated queue PR ossf/malicious-packages #1613 only; this wiki statically unpacked the wheel (no execution) and verified BOTH baked registration endpoints answering `200 {"ok":true,"apiKey":…}` to an unauthenticated probe

## Tags
- tools
- supply chain attack
- PyPI
- Python
- keystroke capture
- echo suppression
- termios
- msvcrt
- operator-linked shell
- server-side unlock gate
- hidden mode
- C2 registration panel
- failover C2
- space-z.ai
- console_scripts
- REPL cover
- curated lane
- ossf malicious-packages
- zero advisory coverage

## What it is

Curated queue PR ossf/malicious-packages **#1613** (filed 2026-10-09 16:02:22Z) files PyPI `py2ops`. This wiki's same-day verification: package is **LIVE at `latest = 2.2.1`**, published 16:02:26Z — four seconds AFTER the queue PR was filed — with its first-ever release `2.2` at 15:02:39Z (both releases the same day), and **ZERO OSV + ZERO GHSA at query**. Tarball sha256: `2.2` = `8c44f1ea62d6769e905c3fb070817c82b5bc14599dc06ad671aa8c381cd26509`, `2.2.1` = `fcaf5924e3c051ca2f14f2b7c06768b2346349006948fd7ce8852b7f76ba7208`. Wheel metadata: package `pyops`, console script `python2 = pyops.cli:main`, author field `pyops`, homepage `https://preview-chat-960504a9-b4e0-4b69-bc80-6ac3d4fa4ae0.space-z.ai` — a preview-sandbox URL on an AI-app-hosting platform baked into the metadata itself.

The wheel is 8.5 KB: `pyops/__init__.py`, `pyops/__main__.py`, `pyops/cli.py` (19,651 B, the whole story), plus dist-info. No install hooks — the malware class here is **use-time**, which is why install-hook scanners find nothing.

## Mechanics (static unpack, no execution)

The header comment is unusually candid (quoted verbatim in spirit): "this file is only the CONNECTION LAYER… bare `python2` behaves exactly like the local python interpreter — because it IS one (a real REPL); that is the whole cover. every line is read with the console echo switched off and put back on the record afterwards, so whatever is meant to stay secret never touches the screen."

1. **Silent first-run registration.** `_quiet_config()` bootstraps without user interaction: `POST <server>/api/cli/init` with `{hostname, os}` and `User-Agent: python2/<version>`; the returned `apiKey` is pinned to `~/.python2/config.json`. Two servers are baked: primary `https://preview-chat-960504a9-b4e0-4b69-bc80-6ac3d4fa4ae0.space-z.ai` (env `PY2_SERVER` overrides), fallback `https://b196q82k8891-d.space-z.ai`. `_candidates()` / `_failover()` rotate the pinned home whenever the panel looks stale (status 0/404/≥500; clean denials and 429s count as alive answers — deliberate anti-noise logic).
2. **Echo-off line reading (`_quiet_read`).** POSIX path drops to `termios` raw reads; Windows path uses `msvcrt.getwch()`. Characters never reach the screen; the console layer "writes them back to the record afterwards." A genuine REPL input loop where every typed line passes through a silent capture-then-replay layer — standing keystroke interception, not a targeted password prompt.
3. **Server-side gate with a hidden mode.** A bare single token typed at the prompt (regex-checked, non-keyword, ≤5 tries/session) is POSTed to `/api/cli/unlock` as `{apiKey, password}`. On success the client marks a **24 h unlock window** in `~/.python2/state.json` and raises an internal `_Veil` exception — "silence — that is the entire reply." The unlocked capability is NOT in this wheel: "every working command is served by the linked ops server for operator-authorized devices" = second-stage tooling lives server-side and is fetched only after the passphrase, so the public artifact carries no detectable malicious payload surface.
4. **Invisible-by-design details.** Wrong words are echoed back with an ordinary `NameError` any unknown word would get; real Python expressions (spaces, brackets, dots) are never sent anywhere; `python2 -d` removes the install; `Retry-After`-respecting backoff on 429/502/503.

## This wiki's checks (Oct 9 ~21:4x UTC)

- `POST /api/cli/init` with `{"hostname":"probe","os":"linux"}` (harmless probe, no victim data): **both** baked servers answered `200 {"ok":true,"apiKey":"ptm_…"}` — open, unauthenticated device registration is LIVE on both rails, keys prefixed `ptm_`. The panel is not a parked domain; it is issuing enrollments now.
- Primary host root answers `000` (no plain response) while `/api/cli/init` works — the panel serves only its API routes. Fallback host root answers `307`.
- PyPI registry: both versions live, no quarantine marker (contrast `ig-gox`, quarantined within ~6.5 h of its PR). `py2ops` has now been live-and-unadvised ≈6 h at this write.
- **Hundred-twenty-ninth sweep follow-check (Oct 9 ~23:1x UTC, ≈7 h live):** STILL `latest = 2.2.1`, both releases un-yanked, no quarantine marker; **ZERO OSV (OSV name query empty) + ZERO GHSA (GitHub `ecosystem=pip&affects=py2ops` = 0 records)**. Approaching/past the ig-gox OSV-arrival mark (+9 h); PyPI-action comparison stays the clock that matters.

## Durable reads

- **The "it IS the real interpreter" cover is the ledger's cleanest dual-use camouflage statement**: detection can't come from behavior difference at the prompt, because there is none — hunt must key the artifacts (`~/.python2/config.json`, `state.json`, UA string `python2/<ver>`, `space-z.ai` registration traffic, `console_scripts: python2`).
- Server-gated second stage + echo-off reading + 24 h unlock TTL is a **remote-operator shell delivered through a package index**, functionally the same trust inversion as ig-gox's license-gated loader (same-day sibling) — one gate design, two ecosystems. Cross-link: [ig-gox page](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md).
- Abuse of **AI-app preview hosting** (`*.space-z.ai` "preview-chat-…" slugs) for C2 panels joins the ledger's platform-abuse lane (preview/ephemeral hosts as disposable, trusted-domain-adjacent infrastructure).

## Monitor

- OSV/GHSA arrival clock vs queue #1613 (filed 16:02:22Z; still zero-advisory at +6 h — vs `ig-gox` OSV at +9 h / PyPI quarantine at +6.5 h).
- PyPI quarantine action; re-registration under sibling names (`pyops` import name, `python2` entry point, "companion shell" phrasing).
- `space-z.ai` slug churn on both rails (the baked `preview-chat-<uuid>` shape is the grep key); any other package shipping `space-z.ai` defaults.
- First artifact that FETCHES an unlocked command set from `/api/cli/*` — that release converts inference into payload.

## Related pages
- [ig-gox (PyPI) — the same-day sibling: license-gated in-memory exec loader](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md)
- [algamil7x ledger — one-hundred-and-twenty-eighth sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-9-one-hundred-and-twenty-eighth-sweep)
