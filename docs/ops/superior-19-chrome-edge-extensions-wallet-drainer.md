# "Superior": 19 Chrome/Edge extensions delivering a wallet drainer and credential-stealing framework (Socket)

## Summary
Socket's threat research team identified **18 Chrome extensions and 1 Edge extension** sharing a single, modular malware framework that **drains crypto wallets and steals credentials**. The malicious versions were published over the last six months, but code and operational similarities tie the campaign to a dual-function Chrome-extension threat first reported by **DomainTools in February 2024** and later described by **Secure Annex** ("Pixel Perfect"). Socket tracks the actor under the name **"Superior"**, based on tags in the names of the malicious JavaScript modules.

The most significant tactic is **acquiring established, legitimate extensions** with an existing user base and then weaponizing them. Five of the 19 were bought from legitimate authors; fourteen were created by the actor. The extension with the largest blast radius — **"Enable Right Click & Copy — Smart Unlock + OCR"** (original author **PreppHint**, ~70,000 Chrome users plus ~10,000 Edge users) — had its malware introduced by the new owner; the Chrome version was removed from the store, but the Edge version was still serving malware at publication, with a new C2 domain published August 14, 2026.

## Tags
- ops
- operations
- Socket
- Chrome extension
- Edge extension
- browser extension malware
- supply-chain risk
- trusted extension risk
- wallet drainer
- wallet-theft
- credential theft
- command and control
- WebSocket C2
- CSP stripping
- XSS injection
- crypto draining
- hardware wallet
- seed phrase
- ClickFix
- fake update
- extension takeover
- dual-function malware
- DomainTools
- Secure Annex
- PreppHint

## Why this matters
- **The trusted-extension takeover is the core risk.** The actor publishes a clean first version, builds base trust and a user base, then pushes a malicious update. Chrome's default extension update settings auto-update to the latest version at startup and every few hours, so the malicious version reaches existing users without any user action. Buyers of extensions are not notified when ownership changes.
- **The impact surface is large and real.** 80,000+ users on the PreppHint extension alone; the campaign has been operational for two-plus years and is described as advanced and well-consolidated, with deliberate separation of the malware-loading framework from the payload modules to reduce detection risk.
- **The framework is modular and evolving.** Payloads are downloaded from C2 as encrypted JavaScript "nodes" and are pluggable; the observed set of 16 modules (drainers, seed-phrase phishing, session stealers, click-fix lures) is explicitly "not exhaustive nor final."
- **The campaign has expanded to Microsoft Edge**, not just Chrome.

## Architecture and shared techniques
All identified extensions share the same design patterns, which are recognizable across the code:

- **Covert C2 channel.** The background service worker maintains a **persistent WebSocket** connection to a C2 endpoint, with a 25-second ping and a 5-minute heartbeat; errors are silently swallowed. Per-victim `userId` and downloaded code modules ("nodes") are stored via `chrome.storage.local`. The loading framework supports **C2 endpoint rotation** on instruction from the initial server — observed in the wild — enabling distribution of victims to different C2 groups and reducing detection risk. Data-exfiltration endpoints are also received dynamically from C2.
- **Encryption.** Incoming WebSocket messages deliver malicious JavaScript modules that are **AES-GCM encrypted** with a key derived from **SHA-256 of `extensionId-installUUID`**.
- **CSP stripping.** On startup the background worker registers a **declarativeNetRequest** dynamic rule that removes `Content-Security-Policy` (and report-only / `x-webkit-csp` / `x-content-security-policy`) headers on **every page, all frames, and every site** the user visits — required to enable the injection technique below.
- **Main-world JavaScript injection.** Content scripts create hidden DOM elements (`<img>`, `<input>`, `<form>`) on visited pages, attach the downloaded module as an event handler, and dispatch a synthetic event to force execution in the page's **main world**, then remove the element to avoid leaving evidence. Newer versions trigger injection dynamically via `chrome.scripting.executeScript` rather than static manifest content scripts (less noisy, harder to spot).

## Observed payload modules
Modules are the pluggable payloads delivered from C2. The observed list (from the PreppHint extension's C2) includes 16 modules grouped as:

1. **Multi-chain wallet drainer** — detects EVM, Solana, and Tron wallets; loads a chain-specific second stage from a dedicated domain (`cookie-whitelist.top`, `whale-alert.art`), then **hijacks the site's real "Connect Wallet" / "Swap" buttons** — cloning the button to strip the site's own handlers, attaching actor-defined handlers, dismissing the genuine wallet dialog, and driving the connect/approve flow to authorize theft.
2. **Hardware-wallet seed-phrase phishing (superior-trezor / superior-ledger)** — on `trezor.io` and `ledger.com`, performs a full-page DOM takeover, serving a pixel-accurate fake "Ledger Live / Trezor" update-and-restore wizard from `ggle-analytics.com`, then capturing and exfiltrating the 12/18/24-word recovery phrase.
3. **Exchange & wallet account harvesters** — session-riding modules that read balances and authenticated session material (cookies, bearer/authorization tokens, account/profile data) from logged-in tabs. Targeted services: OKX, MEXC, Kraken, KuCoin, Coinbase, Binance, Bybit, and MetaMask.
4. **Universal credential/form grabber (superior-grabber)** — hooks focus/input/change/blur/mutation events on every text, password, and email input (including same-origin iframes), batching and exfiltrating captured values on a timer with page-fingerprint data.
5. **Social-media theft** — a Facebook module harvesting access tokens, business, billing, and dashboard data; a LinkedIn module registering a rogue in-page service worker to strip anti-CSRF headers and abuse the logged-in session.
6. **Browser-history exfiltration (superior-history)**.
7. **ClickFix fake-update lures (superior-updater)** — injects a fake browser-update page/modal/bar from `ggle-analytics.com` with decoy behavior; one lure shows a fake "Chrome — Update available" page that copies an attacker-supplied command to the clipboard, then uses OS-specific screenshots to instruct the victim to paste and run it.

## Campaign history
Socket traces the campaign to **February 2024** based on overlap with DomainTools' dual-function-malware-in-Chrome-extensions research: shared techniques, operational methods, heavy use of the `.top` TLD for primary C2, and near-identical domain naming (e.g., `cookie-whitelist[.]top`/`whale-alert[.]art` here vs `cookie-whitelist[.]com`/`whale-alert[.]life` in the DomainTools dataset).

## Outlook and recommendations
- **Users:** review installed extensions regularly and remove anything unneeded or suspicious; think hard before adding a new extension (is it really necessary?). Assume a previously trustworthy extension can change instantly, and note that ownership changes are not notified.
- **Defenders:** monitor for the CSP-stripping declarativeNetRequest pattern, main-world injection of downloaded modules, and WebSocket C2 to the domains below; treat extension ownership changes as a supply-chain event. The Edge variant means non-Chrome browsers are now in scope.

## Indicators of compromise
### Primary C2 domains
`active-enable-right-click[.]top`, `api[.]enable-right-click[.]click`, `enable-right-click[.]click`, `payload[.]siteinsight[.]bond`, `api[.]extensionanalyticspro[.]top`, `password-protect-pdf[.]com`, `privatecryptonewsreader[.]pro`, `cryptoratesfiatconverter[.]pro`, `cryptopricebadgequickglance[.]pro`, `ws[.]site-signal[.]top`, `content[.]resonanceweb[.]top`, `api[.]creativelibrary[.]top`, `api[.]codefilearc[.]net`, `ws[.]seopulsepro[.]sbs`, `relay[.]seopulsepro[.]sbs`, `defipulsetracker[.]pro`, `blockfolioaddressmonitor[.]pro`, `pricealarmsvolatilitywarnings[.]pro`, `extension[.]io-safe[.]icu`, `feedback[.]feedx-ray[.]top`

### Additional domains
`lucky-random[.]sbs` (secondary C2); `pipi[.]saghirmohamed19[.]workers[.]dev` and `mimi[.]saghirmohamed19[.]workers[.]dev` (Cloudflare Worker exfiltration sinks); `cookie-whitelist[.]top` and `whale-alert[.]art` (wallet-drainer script hosting); `ggle-analytics[.]com` (fake-update page hosting).

### Extension IDs
**Bought by the threat actor** (legitimate extensions later weaponized):
- `pkoccklolohdacbfooifnpebakpbeipc` — Enable Right Click & Copy — Smart Unlock + OCR (PreppHint)
- `fegckejpfnlmfgkfjpinlbgmeeijjkel` — RapidLens - Google Lens for Screen Search & Images
- `kdenlnncndfnhkognokgfpabgkgehodd` — QuickLens - Search Screen with Google Lens
- `jamminefolhgepgihbmcjjhgldbfcikp` — Password Protect PDF
- `inmkjedjdhgpknjogbjomhnbgdccckkg` — Allow Copy - Select & Enable Right Click (Edge)

**Created by the threat actor:**
- `fcgdejjichpgfaaafflplhfijcnieopb` — PixelCheck
- `cfpnjdbpojpcongfaefcamjbaolpelcd` — Creative Library - Ad Spy Tool
- `aapdalkmclfaahehnmicbglkohkldhne` — Website Traffic Checker: MirrorSphere SEO Stats
- `dkdadldmiefjldmegbjbnhhfddnkhlhm` — Site Signal - Website Traffic & SEO Checker
- `fjmlhlkccegopebcllcmafahkmeejpph` — SEO Pulse Pro - Website Traffic & SEO Analyzer
- `iekoapohahgmogbagegmcgplbkikcgke` — Private Crypto News Reader
- `ahpnnnjbnfbhoikhohglpohnoocjcoco` — Blockfolio: Address Monitor
- `oeacadlaclegkkkdehjmiifnjhcekclj` — Crypto Rates & Fiat Converter
- `jmlgannjlbliikgcaieomgmcnfplglea` — Crypto Alerter: Price Alarms & Volatility Warnings
- `lhmcajhgadanidbopgaoobjlldegjmke` — DeFi Pulse Tracker
- `gfackggoapepdmnjnkblogdcjpgcjiak` — Crypto Price Badge: Quick Glance
- `hfijkbdkpidafdbeebnnkhfccildbcle` — Multi-Chain Explorer
- `pcngchfbfgejllcbhmeadjhiebebiome` — LedgerLook: Wallet Checker
- `aodkjdeghbjiaienipfjkbpcikkacbcp` — Meta & Facebook Ad Library Spy — Save Ads, Finder, Downloader | FeedX-Ray

Related domain set: see DomainTools' [DualFunction-Malware-Chrome-Extensions](https://github.com/DomainTools/SecuritySnacks/blob/main/2025/DualFunction-Malware-Chrome-Extensions).

## Source
- Socket: [19 Chrome and Edge Extensions Deliver a Wallet Drainer and Credential-Stealing Payloads](https://socket.dev/blog/chrome-edge-extension-wallet-drainer) — August 27, 2026. Related: DomainTools, [Hidden Threats of Dual-Function Malware Found in Chrome Extensions](https://dti.domaintools.com/research/hidden-threats-of-dual-function-malware-found-in-chrome-extensions) (February 2024); Secure Annex, [Pixel Perfect](https://annex.security/blog/pixel-perfect/).
