# GHOST STADIUM FIFA World Cup ticket phishing

## Summary
Hunt.io reported a June 2026 infrastructure hunt for FIFA World Cup 2026 ticketing lookalikes that builds on Group-IB's earlier **GHOST STADIUM** reporting. The campaign cloned FIFA's real ticketing portal across many cheap lookalike domains to steal FIFA account credentials and payment-card details from fans searching for tickets, resale seats, or hospitality packages.

Track this as an operation because the durable value is the phishing-kit fingerprint: the operators reused a cloned React build, a Chinese UI framework, same-origin credential-harvesting routes, and shared favicon / origin-hosting pivots that defenders can hunt across rotating domains.

## Tags
- ops
- operations
- phishing
- brand impersonation
- fraud
- credential theft
- payment-card theft
- World Cup
- FIFA
- China-linked
- Chinese-speaking
- infrastructure
- Cloudflare
- Hunt.io

## Why this matters
- The sites are visually close to FIFA's real ticketing portal, so user education based only on page appearance is weak.
- The kit captures more than a single ticket payment: Hunt.io says it is designed to collect FIFA account credentials, buyer details, and payment data, creating downstream account-takeover and card-fraud risk.
- Reputation feeds can miss fresh domains during the short window when victim traffic peaks; structural kit features are more durable than domain age or blocklist status.
- Cloudflare fronting hides much of the hosting layer, but leaked suspected origins and reverse-DNS patterns provide better expansion pivots than any single domain.

## Reported chain
1. Group-IB first documented the largest FIFA World Cup 2026 ticketing impersonation cluster as GHOST STADIUM and noted Chinese-language artifacts in the kit.
2. Hunt.io's crawler observations from May 14 through June 2, 2026 found fake ticketing sites built from a shared toolkit and deployed across lookalike domains.
3. The operators cloned FIFA's real ticketing application rather than writing a custom page, then re-hosted it under non-FIFA domains.
4. Victims who reached the fake ticket shop encountered FIFA-branded login and registration flows on attacker-controlled hosts.
5. Hunt.io reports same-origin `/as/authorize` and `/register` routes as the credential-harvesting path.
6. The fleet used Cloudflare fronting for most domains while a smaller set exposed suspected origin hosting.

## Infrastructure and attribution caveats
- Hunt.io assesses the operation as Chinese-speaking based on multiple independent indicators: Simplified Chinese comments in operator JavaScript, use of the Chinese Layui UI framework, Chinese-locale handling, China-oriented hosting, and Chinese registrars for much of the fleet.
- Treat this as a language / operator-environment assessment, not proof of state sponsorship or a specific named group.
- Most domains resolved through Cloudflare `AS13335`; do not use Cloudflare front IPs alone as attribution or clustering proof.
- Hunt.io identifies suspected origin pivots on `AS25820` / Cluster Logic Inc and reverse DNS under `16clouds[.]com`; these are stronger pivots when combined with FIFA-specific structural filters.

## Defender heuristics
### User and brand response
- Direct users to FIFA ticketing only through `fifa.com`, the official app, or a known bookmark.
- Treat any FIFA login, registration, or payment flow hosted on a non-`fifa.com` domain as fraudulent until proven otherwise.
- Prioritize takedown for domains with live payment flows and submit in batches by registrar / hosting provider rather than one at a time.
- Consider public advisories before ticket-sale milestones, when search traffic and forwarded-link exposure are likely to spike.

### Structural web hunting
Hunt on kit features that the operator must keep for the fraud to work:

- FIFA-branded ticketing pages served from non-`fifa.com` hosts.
- Re-hosted React build paths such as `/fifa/main.<hash>.css` rather than FIFA's legitimate `/static/` paths.
- `/layui/layui/layui.js` on FIFA-themed pages.
- `/fifa/common_main.js` operator script.
- `embedded.js` / Flourish usage across the cloned sites.
- `/fifa/host.html?id=` templated payload pages.
- `fifaindexopen` "BUY NOW" pop-up element ID.
- Same-origin `/as/authorize` and `/register` paths on lookalike domains.

### Clustering pivots
Use these to expand and prioritize, not as standalone detection:

- Favicon perceptual hash `c79a386d396664c9` and favicon MD5 `1ea068c804e8ba88b84f6e9598e3172d`; Hunt.io notes these are copied from real FIFA, so they need a non-`fifa.com` and structural-kit guardrail.
- Build CSS hash `main.c56d670b.css`.
- Suspected origins `104[.]225[.]235[.]49`, `89[.]208[.]250[.]38`, and `65[.]49[.]223[.]138` when paired with FIFA hostnames.
- `AS25820` / Cluster Logic Inc and reverse-DNS pattern `16clouds[.]com` as origin-hosting expansion pivots.
- Registrars Beijing Lanhai Jiye Technology Co., Ltd, Alibaba Cloud / HiChina (`www[.]net[.]cn`), and GoDaddy as supporting context for batches of lookalikes.
- Registration waves around 2025-11-17 for premium-TLD brand domains and 2026-03-20 through 2026-03-31 for `fifa-com` and prefix lookalikes.

## Reported domain patterns
Hunt.io's listed domains include these examples; keep them defanged in notes and refang only inside controlled security tooling:

- Brand plus TLD: `fifa[.]center`, `fifa[.]cash`, `fifa[.]gold`, `fifa[.]sale`, `fifa[.]shopping`, `fifa[.]black`, `fifa[.]cafe`, `fifa[.]city`, `fifa[.]fund`, `fifa[.]market`, `fifa[.]red`, `fifa[.]ski`, `fifa[.]website`.
- `fifa-com` variants: `fifa-com[.]com`, `fifa-com[.]id`, `fifa-com[.]services`, `fifa-com[.]vip`, `fifa-com[.]xyz`, `fifa-com-26[.]shop`.
- Prefix lookalikes: `ww-fifa[.]com`, `ww-fifa[.]vip`, `ww-fifaweb[.]cn`, `www-fifa[.]co`, `www-fifa[.]me`, `www-fifa[.]website`, `www-fifa-com[.]vip`, `https-fifa[.]cn`.
- Ticket / host themes: `dt-fifa26[.]shop`, `fc-fifa26[.]shop`, `lg-fifa26[.]shop`, `fifaofficial[.]help`, `fifa-online[.]me`, `fifa-web[.]co`, `fifawebsite[.]cn`, `fifawebsite[.]net`.

## Related pages
- [Hunt.io global smishing infrastructure campaign](huntio-global-smishing-government-postal-telecom.md)
- [Outsider Enterprise smishing PhaaS](outsider-enterprise-smishing-phaas.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Hunt.io: [https://hunt.io/blog/fifa-world-cup-2026-ticket-phishing-kit](https://hunt.io/blog/fifa-world-cup-2026-ticket-phishing-kit)
