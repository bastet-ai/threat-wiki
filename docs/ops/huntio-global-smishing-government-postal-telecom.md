# Hunt.io global smishing infrastructure campaign

## Summary
Hunt.io reports a coordinated smishing operation that grew from fraudulent SMS messages impersonating Romania's Ghișeul.ro government payment portal into a broader campaign spanning 19 countries across Europe, the Americas, and the Caucasus.

The durable defender value is the shared infrastructure and page fingerprint: Hunt.io found 1,628 active malicious URLs tied together by a single 128-character metadata hash embedded in each phishing page. The campaign impersonates government payment portals, road-police and tax services, postal and parcel brands, telecoms, toll systems, banking / fine-payment portals, and retail reward flows.

No actor name is publicly established in the report. Treat this as infrastructure-centric cybercrime coverage unless future public sources connect it to a named crew.

## Tags
- ops
- operations
- smishing
- phishing
- credential-theft
- payment-card-theft
- government-impersonation
- postal-impersonation
- telecom-impersonation
- infrastructure
- typosquatting
- cybercrime

## Why this matters
- SMS payment lures against official portals create direct card-theft risk for citizens and reputational risk for impersonated public services.
- The same deployment pattern spans unrelated brands and countries, so blocking by brand name alone will miss follow-on infrastructure.
- A shared HTML metadata hash, repeated JavaScript bundles, URL language patterns, and hosting clusters give defenders better pivots than individual domains.
- The operation is still rotating infrastructure according to Hunt.io, making detection pivots and takedown coordination more useful than static IOC-only blocking.

## Reported chain

### Initial public warning
- In May 2026, Romania's official Ghișeul.ro payment portal warned users that it does not announce payment obligations by SMS or email and advised citizens not to click suspicious links.
- Hunt.io used that Romanian impersonation as the starting point for wider infrastructure pivots.
- Hunt.io says the same cluster also targeted DPD delivery customers in the United Kingdom and Ireland, road police portals in Bulgaria and Armenia, tax authorities in Greece, T-Mobile users in the United States, and other localized services.

### Victim flow
Hunt.io describes a four-stage card-harvesting flow in the Romanian Ghișeul.ro clone:

1. **Trust establishment** — a localized landing page copies official branding, navigation labels, service badges, SSL-trust language, and a three-step verification / details / payment flow.
2. **Urgency creation** — after a vehicle-registration lookup, the page fabricates traffic-fine details, including a process number, violation type, due date, payment status, and amount.
3. **Payment-card collection** — a payment page asks for cardholder name, card number, expiration date, and CVV while showing a realistic card visualization and payment summary.
4. **Processing deception** — a loading screen gives the appearance of payment processing while the submitted card data is sent to attacker infrastructure.

### Infrastructure and campaign pivots
- Hunt.io found **1,628 malicious URLs** across **19 countries** and multiple sectors.
- The report says every phishing page carried the same 128-character hexadecimal metadata identifier in the HTML `<head>` section:
  - `39dabeddef7c2f0806110b305bd8ca7307c13ac987e7c64fc1d46752868a258958eba99f16413f522a4961dfb0956598336fc258794664ccc9f71f25e8f688c5`
- The same operation used two broad template families:
  - A modern Vue.js single-page application used across most domains.
  - A Bootstrap-based clone apparently scraped from the legitimate Ghișeul.ro site.
- Hunt.io also pivoted on identical JavaScript and CSS assets, including `B0cMf6vN.js`, `DNINFtUF.js`, and `Vx8ldEBt.css`.
- A recurring URL shape, `/{language-code}/#/index`, helped expose the multi-country scope.

### Targeting scope reported by Hunt.io
Hunt.io's 1,628-URL cluster included the following country / brand themes:

- United Kingdom: DPD parcel delivery and Tesco rewards.
- Ireland: DPD parcel delivery.
- Spain: SEUR postal / parcel delivery.
- Romania: Ghișeul.ro government services.
- Bulgaria, Armenia, North Macedonia, Estonia, Latvia: road-police, traffic-fine, or road-safety portals.
- Slovenia, Lithuania, Kosovo: government-service impersonation.
- Greece: AADE tax authority.
- Georgia: TBC Pay banking / fine-payment lures.
- Trinidad and Tobago: court-payment system.
- United States: T-Mobile and North Carolina / Ohio DMV lures.
- Albania: Vodafone.
- Montenegro: postal-service impersonation.
- France: toll / motorway lures.
- Generic or multi-country: DSV-branded delivery and shopping-platform lures.

### Hosting footprint
Hunt.io mapped **32 backend IP addresses** across six geographic regions and several hosting models:

- **Tencent Cloud / AS132203** — 15 servers across Singapore, Frankfurt, and Santa Clara.
- **Cloudflare / AS13335** — 14 anycast IPs fronting parts of the operation.
- **Alibaba Cloud / AS45102** — three Frankfurt-based servers.
- **ALEXHOST Moldova / AS200019** — two Chisinau servers with OpenSSH, nginx, and unusual ports `887` / `888` exposed.

Hunt.io notes that the provider spread complicates takedown and cross-border law-enforcement requests. It also warns that two Cloudflare anycast IPs in the broader cluster had unrelated domains flagged with Tactical RMM and Cobalt Strike signatures; do not treat those shared anycast observations as direct attribution to this smishing operation.

## Defender heuristics
- Search web telemetry, proxy logs, crawler data, and brand-protection feeds for the 128-character metadata hash shown above.
- Hunt for the asset names `B0cMf6vN.js`, `DNINFtUF.js`, and `Vx8ldEBt.css` on newly registered or suspiciously branded domains.
- Detect phishing URLs matching `/{two-letter-language-code}/#/index` on non-official domains, especially when paired with government, parcel, telecom, toll, DMV, court, or payment-service branding.
- Monitor typosquat registrations and cheap / abuse-prone TLDs around public-service brands; Hunt.io specifically observed `.lat`, `.shop`, `.cyou`, `.bond`, `.sbs`, `.cfd`, `.icu`, `.cam`, `.one`, `.vip`, `.top`, and related patterns.
- For public-sector portals and high-volume parcel / telecom brands, publish clear user guidance that payment obligations are not sent through unsolicited SMS links and maintain a rapid takedown workflow for lookalike domains.
- Treat Cloudflare anycast IP overlap carefully: use hostname, certificate, page fingerprint, and body-hash evidence rather than blocking broad shared CDN IP ranges.

## Reported indicators and pivots

Campaign fingerprint:

- `39dabeddef7c2f0806110b305bd8ca7307c13ac987e7c64fc1d46752868a258958eba99f16413f522a4961dfb0956598336fc258794664ccc9f71f25e8f688c5`

Repeated asset names:

- `B0cMf6vN.js`
- `DNINFtUF.js`
- `Vx8ldEBt.css`

Example defanged domains from Hunt.io:

- `ghiseal[.]lat`
- `ghiseul[.]eu[.]cc`
- `ghisaul[.]lat`
- `ghizeul[.]lat`
- `hoiatustrahv[.]politsei[.]gov-ee[.]bond`
- `sumin[.]lrv-lt[.]shop`
- `roadpolice-am[.]icu`
- `roadpolice-am[.]shop`
- `mvr-gov-mk[.]cyou`
- `dpd[.]ie-com[.]vip`
- `vodafaone[.]shop`
- `tesco-redeem-check[.]bond`

Selected backend IPs explicitly listed by Hunt.io:

- Tencent Cloud: `43.160.242[.]3`, `43.160.221[.]174`, `43.160.250[.]19`, `43.157.17[.]77`, `43.157.122[.]50`, `43.157.64[.]211`, `43.165.4[.]234`, `43.157.25[.]170`, `43.165.3[.]200`, `43.165.4[.]68`, `43.165.1[.]208`, `43.165.62[.]39`, `43.157.91[.]129`, `43.153.72[.]244`, `43.173.74[.]207`
- Alibaba Cloud: `47.245.142[.]76`, `47.91.88[.]57`, `47.254.147[.]205`
- ALEXHOST Moldova: `80.96.58[.]119`, `80.96.58[.]68`
- Cloudflare anycast examples from the cluster: `104.21.80[.]54`, `172.67.199[.]16`, `172.67.206[.]239`, `104.21.23[.]164`, `104.21.16[.]182`, `104.21.61[.]204`, `172.67.196[.]175`, `104.21.83[.]233`, `104.21.34[.]64`, `104.21.75[.]129`, `172.67.137[.]96`, `172.67.136[.]71`, `104.21.8[.]35`

## Related pages
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [0ktapus phishing campaign](0ktapus-phishing-campaign.md)

## Sources
- Hunt.io: <https://hunt.io/blog/massive-smishing-campaign-governments-postal-telecoms>
