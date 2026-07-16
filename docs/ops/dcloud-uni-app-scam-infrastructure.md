# DCloud Uni-App scam infrastructure ecosystem

## Summary
Infoblox Threat Intel reported that **DCloud Uni-App**, a legitimate Chinese cross-platform application framework, has become common scaffolding for a large online fraud ecosystem. Infoblox identified **236,493 distinct second-level domains** since mid-2022 in an investment-scam-specific DCloud population, spanning fake crypto exchanges, pig-butchering flows, WhatsApp-style phishing, fake gambling / "scambling" sites, brand impersonation, and crypto wallet drainers.

Track this as fraud infrastructure rather than as a DCloud product issue. Infoblox explicitly says DCloud is a legitimate framework and that it has no evidence DCloud is involved in fraudulent use; the defender value is the framework and template fingerprints that reveal shared scam kits, centralized control over large swaths of domains, and repeatable DNS / web-content pivots.

## Tags
- ops
- operations
- DCloud Uni-App
- DCloud
- Uni-App
- Infoblox Threat Intel
- scam infrastructure
- investment scam
- pig butchering
- cryptocurrency scam
- wallet drainer
- WhatsApp phishing
- brand impersonation
- fake crypto exchange
- scambling
- fake gambling
- RainbowEx
- Lightning Shared Scooter Co.
- LSSC
- Yuechi Shared Technology
- bulletproof hosting
- Chinese-language fraud ecosystem
- DNS threat intelligence

## Why this matters
- Infoblox's investment-scam-specific collection reached **236,493 second-level domains** from 2022-2026, with the steepest growth after late-2024 public reporting connected RainbowEx to DCloud Uni-App.
- New DCloud-fingerprinted scam-site observations reportedly rose from a few thousand per month before the RainbowEx coverage to roughly **15,000 newly observed sites per month at peak** afterward.
- Infoblox separates legitimate DCloud use from malicious sites by looking for scam-specific layers such as fake brokerage interfaces, wallet-drainer prompts, rigged gambling flows, brand-impersonation storefronts, and template fingerprints.
- The ecosystem is not one actor, but Infoblox says hosting patterns, technical fingerprints, communication methods, and synchronized registration dips point to centralized control over significant portions of the population.
- Some evasive scam sites attempted to strip default DCloud fingerprints and were more concentrated on bulletproof hosting providers, suggesting more sophisticated operators inside the broader kit ecosystem.

## Reported scam families
- **Fake crypto exchanges and deposit-and-trade platforms:** the largest category in Infoblox's sample. These sites impersonate exchanges or invent exchange-like brands, often gate registration with invite codes, take deposits in Tether or other stablecoins, display fake trading activity, and block or condition withdrawals.
- **Crypto wallet drainers:** sites present "verify your wallet" or "connect your wallet" flows, sometimes impersonating BNB Chain, Tether, or other crypto platforms, then drain connected wallets.
- **Prediction-market and gambling clones:** Polymarket-like clones, casinos, and lottery sites where operators can simply refuse payouts; Infoblox references the informal "scambling" label for this pattern.
- **WhatsApp and messaging-platform phishing:** templates impersonate WhatsApp "Security Help Center" / help-center verification flows and related trust prompts.
- **Generic credential and investment templates:** simple login/register sites can still be tied to larger fraud operations. Infoblox cites `lsscol[.]com` as a heavily accessed DCloud-fingerprinted domain used by the Lightning Shared Scooter Co. scam.

## Physical-world fraud crossover
Infoblox connects the same template family to offline or hybrid fraud operations:

- **RainbowEx / San Pedro:** Argentine victims, including local officials, promoted a fake crypto platform that displayed fictional trading activity, accepted stablecoin deposits, and blocked withdrawals after exposure. Infoblox says RainbowEx's exchange interface, registration flow, dashboard, and Telegram-driven price calls were built with DCloud Uni-App.
- **Lightning Shared Scooter Co. (LSSC):** a 2024-2025 U.S. mobility investment scam where public reporting and official warnings tied domains including `lsscol[.]com` / `lsscol[.]vip` to victim recruitment. Infoblox notes Salinas, California police identified more than five dozen local victims with combined losses over $370,700, while FBI-linked estimates put total U.S. losses easily in the millions.
- **Yuechi Shared Technology:** Infoblox describes a currently active bicycle-sharing investment scam using DCloud and real-looking legitimacy props, including a Hong Kong company registration and a FinCEN money-services business registration. Treat such registrations as paperwork, not proof of operational legitimacy.

## Defender notes
- Do not block or label all DCloud Uni-App sites as malicious. Use DCloud framework artifacts as one signal, then require scam-specific content, registration/payment flows, brand impersonation, wallet-connection prompts, invite-code gates, or known kit fingerprints.
- For DNS and proxy hunting, cluster recently registered domains with mobile-optimized DCloud layouts, exchange/gambling/wallet language, WhatsApp/help-center themes, and repeated static assets or route structures.
- Treat fraud infrastructure as multi-channel: domains may be only the web front end while recruitment and victim control happen through Telegram, WhatsApp, local offices, social-media groups, or community promoters.
- For wallet-drainer variants, warn users that "verify asset," "connect wallet," and platform-verification prompts on newly registered or unsolicited domains can directly authorize theft.
- For enterprise controls, block confirmed Infoblox / internal indicator domains at DNS, preserve first-seen timestamps and passive-DNS context, and share clusters with brand-protection, fraud, legal, and abuse teams rather than handling them only as malware IOCs.
- For FinCEN / company-registration legitimacy claims, verify the filing directly and remember that registration pages themselves warn that MSB registration is not an endorsement and can be abused in scams.

## Selected pivots from public reporting
- Framework / artifact family: `DCloud Uni-App`, `Uni-App`.
- Public framework site: `en.uniapp[.]dcloud[.]io`.
- RainbowEx example: `rainbowex[.]cc`.
- Fake exchange / finance examples from Infoblox figures: `hkxiu[.]com`, `nasdaqpro[.]top`.
- Wallet-drainer example from Infoblox: `bepviews[.]com`.
- Prediction/gambling examples from Infoblox: `polymk[.]com`, `mango-cleopatrapg[.]com`.
- WhatsApp-themed examples from Infoblox: `whats-zwp[.]vip`, `whats-zrs[.]vip`, `whats-zef[.]vip`, `whats-zea[.]vip`, `whats-zus[.]vip`, `whats-zei[.]vip`, `whats-zen[.]vip`, `faq-whatsapp-center[.]com`.
- LSSC examples from public reporting: `lsscol[.]com`, `lsscol[.]vip`.
- Yuechi example from Infoblox: `ys904[.]top`.

Use Infoblox's source post and DNS intelligence for active domain sets; this page keeps only representative public pivots because the domain population is large and fast-moving.

## Related pages
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [Outsider Enterprise smishing PhaaS](outsider-enterprise-smishing-phaas.md)
- [GHOST STADIUM FIFA World Cup ticket phishing](ghost-stadium-fifa-world-cup-ticket-phishing.md)
- [Hunt.io global smishing infrastructure campaign](huntio-global-smishing-government-postal-telecom.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)

## Sources
- [Infoblox Threat Intel](https://www.infoblox.com/blog/threat-intelligence/from-san-pedro-to-salinas-how-a-chinese-framework-dcloud-uni-app-powers-a-global-scam-economy/)
- [The Hacker News summary](https://thehackernews.com/2026/06/236000-dcloud-uni-app-sites-used-in.html)
