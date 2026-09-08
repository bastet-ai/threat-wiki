# 13 malicious Packagist themes deliver iOS spyware and crypto-wallet seed theft (Socket / FUNNULL)

## Summary
Socket's Threat Research Team confirmed that **13 malicious Composer theme packages across five Packagist vendor namespaces** inject JavaScript into every page of the Vietnamese movie/comic streaming sites that install them. The injected code runs two operations against a site's visitors: a **mobile ad-fraud and gambling-redirect chain**, and, on iPhones, a **WebKit-to-kernel exploit chain that installs spyware**. Socket reported the iOS chain to Apple and coordinated disclosure; Apple confirmed the kernel escape was already fixed in iOS and macOS 26.1 before the report, and the two WebKit entry points are public and listed in CISA's Known Exploited Vulnerabilities catalog.

This expands Socket's earlier March 2026 coverage of six themes under a single vendor (`ophimcms`) to **13 packages across five vendors**, and follows the chain through to the iOS payload and its most recent redeployment. The campaign sits on the same **FUNNULL** infrastructure that QiAnXin XLab documented for the RingH23 / MacCMS supply-chain activity — Socket notes the theme loader pulls its second stage from FUNNULL-hosted infrastructure.

The 13 packages:
- `vsmov`: `theme-dy`, `theme-rrdyw`, `theme-motchill`, `theme-vsmov`
- `vsphim`: `theme-heovl`, `theme-thempho`
- `haiau009`: `kkphim-legend`, `kkphim-motchill`
- `chilltvcms`: `theme-legend`
- `ophimcms`: `theme-dy`, `theme-motchill`, `theme-pcc`, `theme-rrdyw`

OphimCMS and KKPhim are open-source PHP content-management systems (Laravel-based) used to run Vietnamese-language movie and comic streaming sites. A site operator installs a core package plus a theme with `composer require`. The threat actors fork these projects under their own vendor namespaces, keep the scaffolding intact, and trojanize the shipped front-end assets — a site operator who installs one of these themes serves malicious JavaScript to every visitor. The upstream author handle remains inside the forks, so these are hostile republishes.

## Tags
- ops
- operations
- Socket
- Packagist
- Composer
- OphimCMS
- KKPhim
- Funnull
- supply chain
- web supply chain
- JavaScript injection
- iOS exploit chain
- WebKit
- zero-day
- n-day
- spyware
- crypto wallet theft
- seed phrase theft
- gambling redirect
- ad fraud
- CISA KEV
- malicious theme
- Vietnamese CMS

## Why this matters
- **A supply-chain theme becomes a client-side exploit host.** The malicious code ships in the theme's shipped JavaScript and is gated on platform and referrer so mobile visitors (not desktops, bots, or direct visits) are targeted — the CMS itself is not the target, but the theme is the delivery vehicle.
- **Two distinct payloads ride one injection.** A mobile gambling/ad-fraud redirect (monetization) and, on iPhones, a full WebKit-to-kernel exploit chain ending in spyware and crypto-wallet seed theft. The spyware branch is the higher-severity outcome.
- **The iOS chain is an n-day used against unpatched devices.** Apple confirmed the kernel escape was already fixed in iOS and macOS 26.1; the two WebKit entry points (CVE-2025-31277, CVE-2025-43529) are public, patched, and on CISA KEV. The exploit only targets devices that have not updated past iOS 18.6.x.
- **The campaign has been active for months with repeated redeployment.** The initial FUNNULL campaign was reported March 2026 (six `ophimcms` themes); the iOS payload was redeployed on 2026-08-12 under fresh filenames, and the second-stage loader rotated again on 2026-08-17.
- **The crypto-wallet escalation is direct financial theft.** The redeployed payload added an iOS-keychain crypto-wallet seed and mnemonic stealer covering seven wallet apps (Bitget, BitKeep, Bitpie, Phantom, Tonkeeper, Trust Wallet, OKX), extending the campaign from device-data collection to direct financial exfiltration.

## Operational characteristics
- **Delivery mechanism.** The malicious code ships in the theme JavaScript. Loaders gate on platform and referrer so mobile visitors are targeted while desktop browsers, bots, and direct visits are passed over.
- **Branch one: mobile gambling and ad-fraud.** `indexbottom.js` and the `ADTOPLB` plugin in `topinfo.js` (`theme-rrdyw`) inject a fixed banner for mobile visitors that links to a redirect host and loads ad images from `im[.]ue8im[.]com`. The banner is built only when the user agent matches iPhone, iPod, Android, or iOS; it links to `23[.]225[.]52[.]67:4466/vip344.html`, which meta-refreshes to `23[.]225[.]48[.]20:4466/vip/index.php`, sets a session cookie, and forwards to a randomized-subdomain `.vip` gambling landing page on port 7740. The campaign identifier `vip344` rides the chain.
- **Branch two: the iOS WebKit-to-kernel chain.** `theme-dy` appends a loader after the shipped jQuery. The loader uses a custom base64 decoder (avoiding the native `atob`) and fires on non-desktop platforms arriving with an external referrer. It pulls a second stage from FUNNULL infrastructure; the base64 argument decodes to `union[.]macoms[.]la/jquery.min-3.6.8.js`. That injects `cdn[.]data-2920[.]com/app.vue.js`, which redirects to `www[.]cloudfareintcdn[.]com/in-static.js` (a Cloudflare-impersonating domain). That injects a hidden iframe to `start-view.html`, which reads the iOS version and loads a version-specific WebKit exploit.
- **Renderer stage.** Weaponizes two WebKit vulnerabilities: **CVE-2025-31277** (iOS 18.4 to 18.5) and **CVE-2025-43529** (iOS 18.6 and later). Both are public, patched, and on CISA KEV; Apple has acknowledged CVE-2025-43529 was exploited in a targeted attack. The chain carries per-build, per-chipset offset tables for iOS 18.4 through 18.6.x and iPhone XS through the iPhone 16 family. The exploit builds arbitrary read and write inside the WebContent renderer using JavaScriptCore corruption primitives (object-address disclosure, fake objects, a corrupted typed array). The renderer stage reads the iPhone OS version from the user agent and fetches a payload matched to it. The renderer CVEs and staging pattern overlap with the publicly documented **DarkSword** iOS exploit kit.
- **GPU process pivot.** A first escape stage moves from the renderer into the GPU process, building a cross-process memory primitive with IOSurface and mach messaging and forging pointer-authentication signed pointers.
- **Kernel escape.** A second stage reaches the kernel through the **AppleM2ScalerCSCDriver** IOKit user client, opened from a sandboxed context by pivoting through a `mediaplaybackd` XPC service. The code opens the driver (IOServiceOpen type 0) and calls external method selector 1 (the "transform") with a 432-byte input struct carrying two IOSurface IDs. The same driver/interface is publicly disclosed as **CVE-2026-43655** (an AppleM2ScalerCSCDriver use-after-free fixed in iOS 26.5), but the FUNNULL chain's kernel bug is a **distinct primitive**: the public CVE-2026-43655 PoC is a connection-teardown use-after-free on the scaler's shared scheduler objects, whereas the FUNNULL chain races the IOSurface backing store to obtain a kernel read and write. Apple Product Security confirmed to Socket that this kernel escape was already addressed in iOS and macOS 26.1 — so this stage is an n-day used against devices that have not updated.
- **Spyware payload.** On success, the final payload uses the kernel read to collect keychain databases, Wi-Fi passwords, the SMS database, the address book, Photos, browser cookies, call history, location history, and account databases; encrypts them with AES; and uploads over HTTPS `POST /upload` to a rotating pool of C2 domains. The worker beacons exploitation progress to `cloudfareintcdn[.]com/wd-status.html`. The payload reads each sensitive store from a hardcoded path (keychain, Wi-Fi, messages, contacts, cookies, browsing/call history, location, health, accounts, notes, calendar, photos) and its configuration carries a hardcoded AES key, a per-build channel identifier, and the rotating C2 pool.
- **Redeployment and crypto-wallet escalation.** On 2026-08-12 the operators redeployed the entire iOS chain under fresh filenames (a new orchestrator, stager, renderer, workers, kernel stage, and payload) and rotated the second-stage loader again on 2026-08-17; previous filenames continue to return content in parallel. The renderer still weaponizes only CVE-2025-31277 and CVE-2025-43529, and the offset tables still cover only iOS 18.4 through 18.6.x (no tables for iOS 18.7 or iOS 26), so operators target unpatched devices. The redeployed payload roughly doubled in size and added an iOS-keychain crypto-wallet seed and mnemonic stealer, querying the keychain for wallet material from Bitget, BitKeep, Bitpie, Phantom, Tonkeeper, Trust Wallet, and OKX (`keychain_query_bitget`, `keychain_query_bitpie`, `keychain_query_phantom`, `keychain_query_tonkeeper`, `keychain_query_trust`, `mnemonics_vault_`), with five keychain query routines covering seven wallet apps.
- **Staged, admin-activated payloads.** `theme-motchill` and `theme-vsmov` ship `functions.js` containing an `MPAd` class that builds a `<script>` element pointed at a config-supplied URL and appends it to the page (executing arbitrary remote JavaScript) plus a full-viewport `mp-preload-popup-overlay` interstitial ad. `theme-dy` ships pre-declared ad-injection hooks (`indextop`, `content_zaixian`, `play_diyi`, and others). These wire to activate from the fetched second stage or from the theme's own admin "Custom JS" settings fields, which the themes render into every page unescaped via Blade `{!! !!}`.
- **Disguised cryptography.** `theme-motchill` ships `jquery.core.min.js`, a renamed CryptoJS bundle (the `JQMP` namespace) providing AES and PBKDF2, used by a `jquery_beauty()` routine keyed off `document.referrer` and the episode id to sign ad-network requests.
- **Encrypted server-side code.** `theme-thempho` is malicious through its shipped JavaScript (the `jquery_beauty` injection in `js.cookie.js`) and additionally ships its ServiceProvider, route table, controller, and migrations as ionCube-encrypted PHP bytecode — the encrypted code is the theme's entire account system (email/password login, Google OAuth, registration, password change).

## MITRE ATT&CK
- T1195.001 — Supply Chain Compromise: Compromise Software Dependencies and Development Tools
- T1608.001 — Stage Capabilities: Upload Malware
- T1608.004 — Stage Capabilities: Drive-by Target
- T1102 — Web Service (npm registry as a dead-drop resolver, related tenant)
- T1189 — Drive-by Compromise
- T1203 — Exploitation for Client Execution
- T1068 — Exploitation for Privilege Escalation
- T1027 — Obfuscated Files or Information
- T1140 — Deobfuscate/Decode Files or Information
- T1480 — Execution Guardrails
- T1497 — Virtualization/Sandbox Evasion
- T1552.001 — Unsecured Credentials: Credentials In Files (keychain wallet theft)
- T1041 — Exfiltration Over C2 Channel
- T1071.001 — Application Layer Protocol: Web Protocols

## Indicators of Compromise
**Malicious Packagist packages:** `vsmov/theme-dy`, `vsmov/theme-rrdyw`, `vsmov/theme-motchill`, `vsmov/theme-vsmov`, `vsphim/theme-heovl`, `vsphim/theme-thempho`, `haiau009/kkphim-legend`, `haiau009/kkphim-motchill`, `chilltvcms/theme-legend`, `ophimcms/theme-dy`, `ophimcms/theme-motchill`, `ophimcms/theme-pcc`, `ophimcms/theme-rrdyw`.

**Threat-actor handles and emails.** Packagist vendors: `vsmov`, `vsphim`, `haiau009`, `chilltvcms`, `ophimcms`. GitHub source account: `vsphim`. Committer emails: `clemenciajohn74@gmail[.]com`, `dev.cuongnguyen@gmail[.]com`, `nguyenhai.tran.009@gmail[.]com`, `xuxuthoi01@gmail[.]com`, `tuwibu2021@gmail[.]com`.

**Delivery and exploit infrastructure.** `union[.]macoms[.]la/jquery.min-3.6.8.js`, `cdn[.]data-2920[.]com`, `cdn[.]data-2919[.]com`, `www[.]cloudfareintcdn[.]com`, `yunray[.]ai`, `cdn1[.]ai`, `nqsaaskw[.]com`, `abfedgecanme[.]com`, `abfdns[.]com`, `galedns[.]com`.

**Exfiltration C2 (rotating pool).** `www[.]0liwevrhxdc3s2xk00[.]com`, `www[.]39rwcybep-20pwozhvdrzzy[.]net`, `www[.]5wg3w278e3oamlohmcinrkh[.]live`, `www[.]dlosdekr1u18msmov51[.]net`, `www[.]ex0x40vmi8qyccxq[.]net`, `www[.]ioa7xqmhiz26fv5e[.]info`, `www[.]isbo31w1o7xk3fztvmgpbv[.]app`, `www[.]jhflt6l0dwminsl494836rb[.]org`, `www[.]kp2-3ur6pe4r8i2hj5[.]com`, `www[.]ljot1cem6jhzfu53yb9aj3h[.]app`, `www[.]ncalb1rzb2rq5-3zdx1[.]app`, `www[.]ov86ayb0fe4ep2b92-645o[.]com`, `www[.]qdh71-y6j7vxgw046v4cvgga[.]live`, `www[.]sx3cjniwo1bmtqs0vlj-va2f[.]app`, `www[.]sx8vuz4smtdol7pg[.]com`, `www[.]t9ffxu6zhf915fadjv1[.]app`, `www[.]vutjsf0sd9sdqt2rkzvgzv9a[.]org`, `www[.]w4iunvbdvjof39q-3[.]net`, `www[.]xtpj2bzxip6iq7n3bnz[.]info`, `www[.]zfu4n4kxgmx32hsqg[.]cc`.

**Gambling and ad-fraud.** `23[.]225[.]52[.]67:4466`, `23[.]225[.]48[.]20:4466`, `im[.]ue8im[.]com`, `xl0ph4qz[.]vip:7740`, `cre-ads[.]com`.

**Exploit-stage files (SHA-256).** `start-view.html` `60b6771958cb7e553994ba6752f108575ba70e02d24affb51d8936a17eb0bf5e`; `a4tt4g37f36gdd7q7kdc.js` (renderer loader, CVE annotations) `d9530e8cd79ac7b3d02b04e05426653afca7075fcf7424eec4d59c6e95745933`; `a84snnb6pknt3aflt01r.js` (iOS 18.4 to 18.5 RCE) `92c7d246d2c163c076f783dcc19f87f5b9b9ac301b106b87a7aaea9346ce0052`; `921w48jmeqvt3ygn0wwx.js` (kernel escape) `f2fdfddbc436acc24a654092f5205b2c5bd3208b126b2c2754ac63e7aea22298`; `4ap5xpu18z70wwslqybu.js` (spyware payload) `9d6b58886189c0e23f706c32d3d8dda97b0b6d927ece6de07270813f070295b5`; `qljbd9a1h4a83gw8lxcj.js` (iOS 18.6+ worker) `de539a63cbe27bbd4a7db30fc796cd6dc5309c02ef5e60a3c5cf0835e5601283`. A parallel chain redeployed on 2026-08-12 serves the same stages under fresh filenames (orchestrator `98jgbibyeep2qfkvcq.html`, kernel stage `pf2zdl2b4i4cxggjg9s7.js`, spyware payload `sejpbqlu090u7lz0z6ax.js`, among others). The exploit is version-gated at runtime, so per-iOS-version RCE payloads are served conditionally.

**Crypto-wallet spyware.** Hardcoded AES key `9_X1<yW,DC>M=<;5`; channel identifier `22c75b2ee026dbbf7001cfdc2bb47855`.

## Defender heuristics
- **Audit Packagist/Composer theme supply chains on CMS estates.** Any theme installed via `composer require` is Tier-0 for public-web integrity; verify the vendor namespace against the upstream author and treat forked namespaces that keep the upstream handle intact as hostile republishes.
- **Hunt for platform-gated, referrer-gated script injection.** A shipped theme script that builds a `<script>` element from a config-supplied URL and appends it to the page (arbitrary remote-JS execution) plus a full-viewport interstitial ad is a strong tell; so is a loader that fires only on non-Desktop platforms with an external referrer.
- **Trace FUNNULL-hosted second stages.** The loader's base64 argument decoding to a "jQuery-like" host on FUNNULL infrastructure (`union[.]macoms[.]la`, `cdn[.]data-29xx[.]com`, `www[.]cloudfareintcdn[.]com`) and a Cloudflare-impersonating domain is the campaign's structural signature.
- **Treat iOS exploit-stage hashes as hunting pivots**, not just block content — the operators redeploy under fresh filenames and rotate the second-stage loader (2026-08-12 / 2026-08-17), so structure and C2 rotation matter more than static filenames.
- **For iPhone victims, assume full keychain + credential + wallet compromise.** The payload harvests keychain, Wi-Fi, SMS, contacts, cookies, browsing/call history, location, health, accounts, notes, calendar, and photos, and (after the August 12 redeployment) crypto-wallet seeds/mnemonics for Bitget, BitKeep, Bitpie, Phantom, Tonkeeper, Trust Wallet, and OKX. Rotate wallet seeds, 2FA, and session credentials on any affected device and update to current iOS.
- **Keep iOS/macOS current.** The renderer CVEs (CVE-2025-31277, CVE-2025-43529) and the AppleM2ScalerCSCDriver kernel escape are all patched (the latter in iOS/macOS 26.1, hardened further in 26.5 under CVE-2026-43655); the campaign explicitly targets devices not updated past iOS 18.6.x.

## Related pages
- [Funnull RingH23 and MacCMS supply-chain attacks](funnull-ringh23-maccms-supply-chain.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- ["Superior": 19 Chrome/Edge extensions wallet-drainer and credential-stealing framework](superior-19-chrome-edge-extensions-wallet-drainer.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)

## Sources
- Socket Threat Research, "13 Malicious Packagist Themes Deliver iOS Spyware That Steals Crypto Wallet Seeds" (published 2026-08-31T14:25:35Z): [https://socket.dev/blog/packagist-themes-ios-spyware](https://socket.dev/blog/packagist-themes-ios-spyware)
- Apple Product Security disclosure coordination (Socket, August 2026).
- CISA Known Exploited Vulnerabilities catalog (CVE-2025-31277, CVE-2025-43529): [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
