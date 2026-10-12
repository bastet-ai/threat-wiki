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

## Monitor

- OSV/GHSA arrival for the pair (first measured machine-lane clock on a URL-pinned-delivery artifact?), #1624 merge-or-rot (≈10 h unmerged at check).
- `limbomail.com` attachment-path disposition + whether the GCS object mutates (the loader's `.v` size-gate proves the operator re-signs new stages in place).
- Second-stage (`all.js`, sha256 `23c9d188…`) deobfuscation follow-up; whether its capabilities re-qualify this as stealer-class.
- Sibling names from `kingsize`/`ozturkxdd@gmail.com`; any other package citing `lunexindonesia` repos or `node-net-pool` spelling.
- Registry action: npm untouched at ≈42 h; `0.0.0-stage` grammar + twin-clone pattern makes more names likely.
