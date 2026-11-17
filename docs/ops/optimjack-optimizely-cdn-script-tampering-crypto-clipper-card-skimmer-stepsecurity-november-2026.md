# OPTIMJACK: Optimizely-hosted scripts served a crypto clipper and card skimmer to 186 sites

- OPTIMJACK
- Optimizely
- skimming
- crypto-clipper
- card-skimmer
- supply-chain
- CDN-compromise
- iOS-exploit
- Coruna
- DarkSword
- urlscan
- StepSecurity
- November-2026

On November 16, 2026 an attacker gained write access to customer projects on the Optimizely Web experimentation platform and wrote a one-line loader into the per-project custom JavaScript that `cdn.optimizely.com` serves to every visitor of each affected site. Security researcher Scott Helme (Report URI) counted **186 infected sites / 188 infected snippet files** across roughly twenty sectors — public scans recorded requests on CNN, BBC, Fox News, Zoom, Salesforce, GitLab, KLM and others, with later reporting naming brands from HSBC and Equifax to IKEA and Ledger. StepSecurity published the payload anatomy on **November 17** (`OPTIMJACK`, Owais Shaikh; name from Amirul Cyber's earlier write-up), read statically; this wiki re-fetched the post (`200`) and adds the read-time state of the indicators. **The durable read: the trusted-CDN compromise class does not need to breach a single victim site — it edits one field in a vendor SaaS and inherits every site's own script privileges; and the clipper's copy-event hook means the address you pasted into your wallet may never have been the address you copied — verify destinations on your wallet's own screen, never against what you copied.**

## What the payload does (one ~30 KB JavaScript, four modules, read statically)

The tampered snippet adds one script tag: `https://1688360[.]cc/track.js`. From there, four blocks run simultaneously in every visitor's browser:

1. **Crypto address swapper.** Holds replacement addresses for ETH, TRX, BTC, TON, SOL, LTC, BCH, DOGE. Swaps only addresses that pass the chain's checksum (so the replacement is wallet-valid) and only near payment words (`wallet`, `deposit`, `send`). It rewrites addresses in page text, form inputs, link and image attributes, **`copy` events, the clipboard API, `navigator.share`, and the URL and body of `fetch`/XHR** — and it replaces `Function.prototype.call`/`apply`, so a wallet-shaped string is rewritten before any function sees it. A hook on the copy event is why this is a wallet-class threat, not a page-defacement toy: paste-into-wallet gets the attacker's address.
2. **Screenshot + cookie exfil.** After the first swap on a visible element it loads `html2canvas.min.js` from the payload server, captures the visible page as JPEG and POSTs to `/hit.php` with the page URL, up to 8,000 characters of `document.cookie` and up to 20 original addresses. Once per page load, only post-swap; HttpOnly cookies are out of reach.
3. **Card skimmer (added mid-day, ~13:43 UTC).** Wraps `fetch`/XHR, watches form submits for a Luhn-valid card with a known brand prefix + expiry + CVV, and beacons them with the page URL to `/card.php` via `navigator.sendBeacon`. No cardholder name or billing address; **it cannot read card fields inside a cross-origin payment iframe** — hosted fields (Stripe/Adyen) held; the site's own form fields did not. It dedupes captured cards in `sessionStorage` under keys starting `cc_` — which leaves card data in the victim's browser storage as a forensic artifact.
4. **iOS second stage.** iPhone/iPad/iPod user agents are routed to `.icu` domains linked to the **Coruna / DarkSword** iOS exploit kits (StepSecurity did not retrieve those files; chain and versions unconfirmed by them; Censys ARC on-wiki already tracks GHOSTBLADE/DarkSword proliferation).

**The payload was edited live during the exposure window:** urlscan records show `track.js` decoded size growing `28,877 B` (16:02 UTC) → `29,461 B` (16:19) → final `30,430 B` live at `17:56 UTC` — at least four edits in two hours. A campaign that patches its own malware mid-incident is an operator watching telemetry in real time.

## Clock and infrastructure (as published, this wiki's re-quote)

| Fact | Value |
|---|---|
| Payload domain | `1688360[.]cc`, registered **2026-11-16 05:23:08 UTC** (registry WHOIS) |
| A record | `136.113.106.136` (Google Cloud, us-central1); Shodan Nov-5 record shows only SSH |
| SSH host key | ed25519 `5e:7a:7f:b3:d7:22:ba:c7:f5:04:5a:b2:5c:0d:8a:73` (Shodan, Nov-5) — sibling-server pivot |
| iOS-stage domains | `eil786npto9u5bq[.]icu`, `1y69gy2mdzaltz1[.]icu`, `gm38duxoihbmy5o[.]icu` (registered Nov-16 16:38:42 UTC) plus older `.icu` pair registered **Nov-9**, one serving by **Nov-12** = iOS infra pre-dates the campaign |
| First public scan hitting payload server | 08:28 UTC (~3 h after registration) |
| Cleaning reported | ~21:32 UTC, 41 of 188 files still infected → **exposure window ≥ 13 hours** |
| Take | ~`$6,600` on-chain at Nov-16 prices; **4 of 8 attacker wallets received nothing**; cards/cookies/iOS access do not show on-chain |
| Paths | `/track.js`, `/html2canvas.min.js`, `/hit.php`, `/card.php` |
| Browser artifacts | `window._k7`, `window._cc`, `window._qxc`, `window._shot`; `sessionStorage` `cc_*`; non-native `Function.prototype.call`/`apply` |
| Payload digest | urlscan-stored exact file SHA-256 `f7b84b9a…` (17 domains) |

**THIS WIKI READ (Nov-17 ~06:5x UTC):** `1688360[.]cc` (`track.js`, `hit.php`) and the sampled `.icu` iOS-stage hosts all answer **connection timeout (`000`)** from this vantage — quote as lane state, not death: the sink pattern this ledger tracks runs both directions, and StepSecurity explicitly noted the payload server was still live while files were being cleaned. The provider (Optimizely) told press it blocked the vulnerable signup-flow path, deployed a fix, removed injected code, revoked sessions/tokens, and blocked delivery at Cloudflare; the initial-entry mechanism was described by the vendor as a vulnerability in the Experimentation account signup flow, and StepSecurity had not established attribution at publication.

## Defensive read

- **Fetch your own snippets.** Any site loading `cdn.optimizely.com/js/<projectID>.js` (or a first-party CNAME to it) should fetch every snippet it serves and grep for `1688360`, `.icu`, `track.js`; record `Last-Modified`; ask the vendor which project IDs were modified and when. Absence today is not absence during the window — pull your own scan/CSP/telemetry history back to **08:00 UTC Nov-16**.
- **Blocked requests are the victim list.** CSP reports and browser telemetry showing FAILED requests to the payload host mark pages where the loader was present — two sites in early reporting were protected by CSP and only discoverable that way.
- **Payment pages: hosted fields are the control that held.** Cards typed into a site's OWN form fields were captured; cards in a cross-origin hosted-payment iframe were not. Remove third-party tags from checkout paths and use provider hosted fields.
- **Wallet users: trust the device, not the page.** With copy-event swapping, verify the destination address on the wallet/hardware-wallet screen against the intended payee, never against what you copied.
- **iOS triage:** devices on iOS 18.6 or earlier that visited affected sites during the window are exploit-kit candidates for forensic triage; current patch levels sit outside the published kits' range.
- **Forensics:** hunt `sessionStorage` keys `cc_*`, the four `window._*` globals, and non-native `Function.prototype.call`/`apply` in page-context captures; pivot sibling servers on the SSH host-key fingerprint, not the domain (domains here were hours old).
- Feed-absence tripwire: no CVE or KEV entry exists for the Optimizely signup-flow entry path as of this wiki's read — KEV grep `0`.

## Ledger kinship

The web-skimming class is adjacent to, not the same as, the npm/PyPI stealer lanes this ledger tracks: same monetization (wallet keys, cards, sessions), different execution surface (visitor browser vs developer install). The iOS exploit-kit tail (Coruna/DarkSword) joins the ledger's existing Censys ARC watch on GHOSTBLADE panel proliferation. The `webhook.site`/`h1.cx` collector pattern from the registry lanes is the same "attacker rents public inbox services" tradecraft at browser scale.

## Sources

- StepSecurity blog, Owais Shaikh, 2026-11-17: `stepsecurity.io/blog/optimjack-optimizely-hosted-scripts-crypto-clipper-card-skimmer` (fetched `200` by this wiki ~06:5x UTC Nov-17; IOC table quoted with per-row sourcing as published)
- Report URI / Scott Helme infection counts and cleaning timeline (as cited by StepSecurity and press)
- Cointelegraph Nov-17: Optimizely vendor statement (signup-flow vulnerability, fix, token revocation, Cloudflare block); Cointelegraph/CybersecurityNews/SecurityOnline for brand lists and on-chain take figures (secondary, quoted as reporting)
- On-wiki related: [Censys ARC / DarkSword-GHOSTBLADE watch](../notes/source-index.md), [solana-keypair wallet stealer](rubygems-solana-keypair-extconf-build-time-credential-stealer-webhook-site-november-2026.md) (wallet-key monetization kin), [312th sweep stream](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-17-three-hundred-and-twelfth-sweep)
