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

## Sweep ticks

- **Oct 10 one-hundred-and-thirty-first sweep (~05:3x-05:5x UTC):** STILL LIVE `2.2.1`, both releases un-yanked, **ZERO OSV + ZERO GHSA ≈13.5 h** — the beaten ig-gox +9 h mark extended by a third again; no PyPI quarantine marker.
- **Oct 10 one-hundred-and-thirty-third sweep (~09:3x-09:5x UTC):** STILL LIVE `2.2.1`, simple-index `project-status=active`, **ZERO OSV + ZERO GHSA ≈17.5 h**. CONTRAST CLOCK: same-window kam193 RAT pair `agentaix`/`media-manager5` went OSV→GHSA→**PyPI quarantine in ≤~1.5 h** — this curated-lane keystroke-RAT is now at a full day-plus unadvised while two same-day PyPI RATs were killed at hours-scale. The registry-action differential is the sharpest question this ledger holds.
- **Oct 10 one-hundred-and-thirty-seventh sweep (~17:2x-17:5x UTC): VERSION CHANGE — `2.3` published 16:58:01Z, ~25 MIN OLD at first read, ZERO OSV + ZERO GHSA ≈30 h live.** See the 2.3 analysis section below: the release is SELF-HEALING (silent auto re-registration on panel 401/403) and ANTI-INSPECTION (the `python2 config` command — the only surface that showed the linked server + key — is deleted). C2 rails alive: both `space-z.ai` hosts resolve to an **Aliyun Hong Kong ALB** (`alb-1i2q34bllrtyl61zig.cn-hongkong.alb.aliyuncsslbintl.com`), `/api/cli/init` answers `405` GET = POST rail live (first geo/hosting read on the panel).

## <a id="october-10-version-23"></a>October 10: `2.3` — the self-healing re-key + the deleted config command (static diff, no execution)

Wheel `py2ops-2.3-py3-none-any.whl` (8,391 B, sha256 `06a843657663a19b4efb53b4dbfe9082d975dc75f9e9583440c36749682fba40`, uploaded 2026-10-10T16:58:01Z) vs `2.2.1`. Three functional changes, all in `pyops/cli.py`:

1. **`_rekey(cfg, word)` added.** When the pinned panel answers `401`/`403` (its comment: "the pinned server is alive but lost this device — fresh deploy, wiped db"), the client silently calls `_register(server)` for a FRESH apiKey on the SAME server, retries the unlock once with the new key, and only pins the new key if the server accepts the secret. Wired in at BOTH unlock paths (interactive line-based unlock and startup password prompt) with a one-shot `rekeyed` guard. DURABLE: the implant now RE-ENROLLS itself — a panel redeploy that wipes device keys, or a deleted `~/.python2/config.json`, no longer strands the implant; the first `401` fixes it without user action.
2. **`python2 config` REMOVED** (command + help line). That command was the only surface where a victim or responder could see the linked server URL and the masked apiKey. Its removal makes the linkage invisible from inside the tool — detection now requires artifact/traffic hunting (`~/.python2/`, UA `python2/<ver>`, `space-z.ai` registration traffic), which is exactly the hunter's-rule already on this page, now with the self-serve path closed.
3. **First-release pair unchanged otherwise:** `__init__.py`/version strings bump; `python2 -d` uninstall stays.

Reading: an operator shipping resilience + anti-inspection improvements WHILE the package sits at ~30 h zero-OSV/zero-GHSA with a curated ingest PR (#1613, 26 h old) unmerged — release cadence so far: `2.2` 15:02Z Oct 9, `2.2.1` 16:02Z Oct 9 (hot-fix, 1 h), `2.3` 16:58Z Oct 10 (feature, ≈25 h later). The advisory-as-build-trigger rule is INVERTED here: there is no advisory, the clock is the operator's own.

- **Oct 10 one-hundred-and-thirty-eighth sweep (~19:2x-19:5x UTC): VERSION CHANGE AGAIN — `2.3.1` published 18:12:11Z, 81 MIN after `2.3`, ZERO OSV + ZERO GHSA ≈32 h live.** Static diff = `remember_word()`/`recall_word()` persist the unlock word XOR-scrambled under a per-machine key into `~/.python2/state.json` → the self-heal loop is now END-TO-END (re-register + re-unlock with zero user action after any panel wipe); `state.json` key `k` = post-first-success IOC marker. Panel read: `www.space-z.ai` apex flipped **`410 Gone`** on all paths (same ALB) while both baked device subhosts still `405`-GET = POST rails live — tenant-level darkening, probe the baked subhosts not the apex. Full diff → [2.3.1 section](#october-10-version-231).
- **Oct 10 one-hundred-and-thirty-ninth sweep (~21:2x-21:3x UTC): NO NEW RELEASE — `2.3.1` static ~3 h, the FIRST release-gap since the iteration loop opened (cadence was 1 h/25 h/81 min); ZERO OSV + ZERO GHSA ≈34 h, queue `#1613` ~30 h unmerged.** Panel recheck under the 138th's tenant-darkening rule: device subhost `b196q82k8891-d` still `405`-GET (POST rail live), apex `www.` still `410 Gone`; `preview-chat-…` subhost returned `000` on two attempts then `405` on three = ALB-pool IP rotation (`47.83.197.91` ↔ `47.239.88.7`) causing transient connection wobble, NOT darkening spread — DURABLE: retry a `000` from an ALB-fronted subhost across ≥2 resolves before dispositioning, the pool itself churns.

## <a id="october-10-version-231"></a>October 10: `2.3.1` — the word goes persistent (static diff 2.3 → 2.3.1, no execution)

Wheel `py2ops-2.3.1-py3-none-any.whl` (sha256 `f89350b99d217af91ff2e446ddaa010eb9dca95cfa6cbf2d32aa7e058dd9cfa6`, uploaded 2026-10-10T18:12:11Z — **81 min after `2.3`**, second same-day iteration, ZERO OSV + ZERO GHSA ≈32 h). One functional change beyond version strings, all in `pyops/cli.py`:

1. **`remember_word()` / `recall_word()` added.** After ANY successful unlock the passphrase is XOR-scrambled with a per-machine key `md5(nodename|sys.platform|"py2ops")` and written into `~/.python2/state.json` (field `k`, ≤128 B). The code comment is candid about intent: "so a fresh server deploy (which forgets every device) heals invisibly instead of wearing the boring cover. the scramble keeps casual file browsing and `strings`-style peeks unrevealing."
2. **Full self-heal loop closed.** `2.3`'s `_rekey()` re-registers a fresh `apiKey` on panel `401/403` but could not re-unlock without the secret; `2.3.1` supplies it — on `401/403` at payload-fetch the client registers a fresh key, re-unlocks with the RECALLED word, re-pins, retries; plus a new `status==0` path quietly retries the pinned server twice on blips. End-to-end: **panel redeploy / wiped device DB / deleted config no longer breaks a victim machine at all** — the implant re-enrolls and re-authenticates with zero user action, and the operator never re-touches the victim.
3. **IOC consequence (durable):** `~/.python2/state.json` previously held only an unlock timestamp; it now holds a machine-derived ciphertext blob. A `state.json` containing key `k` with a hex value is a POST-FIRST-SUCCESS marker — the box has typed a valid word at least once. The scramble is NOT post-cracked: recovery needs the victim's nodename+platform, so responders keep the whole `~/.python2/` directory, not just the file.

**Panel disposition read at this check:** bare apex `space-z.ai` now fails TLS/connection (`000`), while `www.space-z.ai` — EVERY path including `/api/cli/init` and root — answers **`410 Gone`** on the SAME Aliyun HK ALB (`alb-1i2q34bllrtyl61zig…`, 47.239.88.7/47.239.134.228/47.83.197.91). The two baked DEVICE hosts `preview-chat-960504a9-…` and `b196q82k8891-d` still resolve to the same ALB and still answer `405` on GET `/api/cli/init` = POST rail live. DURABLE: `410` at a shared-ALB apex is the panel tenant being retired/hidden while device rails keep serving — ALB-fronted panel infra goes dark TENANT-by-TENANT, so disposition watches must probe the exact baked subhosts, never the apex domain.

## Monitor

- OSV/GHSA arrival clock vs queue #1613 (filed 16:02:22Z; still zero-advisory at +6 h — vs `ig-gox` OSV at +9 h / PyPI quarantine at +6.5 h).
- PyPI quarantine action; re-registration under sibling names (`pyops` import name, `python2` entry point, "companion shell" phrasing).
- `space-z.ai` slug churn on both rails (the baked `preview-chat-<uuid>` shape is the grep key); any other package shipping `space-z.ai` defaults.
- First artifact that FETCHES an unlocked command set from `/api/cli/*` — that release converts inference into payload.

## Related pages
- [ig-gox (PyPI) — the same-day sibling: license-gated in-memory exec loader](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md)
- [algamil7x ledger — one-hundred-and-twenty-eighth sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-9-one-hundred-and-twenty-eighth-sweep)
