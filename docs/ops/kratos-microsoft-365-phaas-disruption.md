# Kratos Microsoft 365 PhaaS and infrastructure disruption

## Summary
German and Indonesian authorities announced the disruption of **Kratos**, a subscription phishing-as-a-service operation built primarily to steal Microsoft 365 credentials and, in one operating mode, authenticated sessions. Germany's Federal Criminal Police Office (BKA) says Indonesian authorities arrested the service's developer and technical administrator while investigators disabled central infrastructure and took more than 200 servers offline.

The BKA estimates that more than 1,800 criminal customers used Kratos to run roughly 15,000 phishing campaigns per month. Authorities assess that the service reached hundreds of thousands of victims in more than 30 countries and earned more than €300,000 since 2024. The takedown interrupts the central service, but it does not by itself revoke stolen Microsoft 365 sessions, clean compromised WordPress hosts, or remove kit copies and access already held by customers.

## Tags
- ops
- operations
- phishing
- phishing-as-a-service
- Kratos
- Microsoft 365
- adversary-in-the-middle
- AiTM
- credential theft
- session cookie theft
- account takeover
- business email compromise
- QR code
- anti-bot
- Telegram
- WordPress
- Cloudflare
- infrastructure disruption
- law enforcement
- BKA
- Germany
- Indonesia
- ANY.RUN

## Reported scale and disruption
- The BKA described Kratos as a criminal franchise model sold through a dedicated website and Telegram shop, with cryptocurrency payments and centralized campaign-management infrastructure.
- German investigators estimate more than **1,800 customers**, approximately **15,000 campaigns each month**, and campaigns capable of reaching thousands of recipients apiece.
- Public reporting based on the law-enforcement action places victim exposure in the hundreds of thousands across more than 30 countries, concentrated in Europe and the United States.
- Indonesian authorities arrested the alleged developer and technical administrator. German authorities reported disabling central components and more than 200 servers.
- The BKA says the central infrastructure is no longer usable for Kratos-supported campaigns. Treat that as service disruption, not proof that every affiliate deployment, stolen credential, live session, or copied kit has been neutralized.

## Service and attack chain
1. A customer configures a campaign through the Kratos panel, selecting deployment, delivery, geographic filtering, anti-bot behavior, and a credential-only or relay-capable phishing flow.
2. Lures commonly impersonate Microsoft 365 document, invoice, tax, SharePoint, or file-sharing workflows. ANY.RUN observed submissions that had passed corporate email filtering and campaigns using recipient-specific QR codes.
3. Redirects and anti-bot checks lead to a Microsoft-styled page. Compromised WordPress sites, disposable domains, Cloudflare-fronted infrastructure, and ordinary cloud hosting all appeared in the ecosystem.
4. In the simpler PHP branch, the page posts credentials to endpoints such as `next.php`, `save.php`, or generation-specific paths.
5. In the Node.js reverse-proxy branch, the service can relay authentication to Microsoft and capture resulting session material. Password reset alone is therefore insufficient where session theft is suspected.
6. Stolen access can support mailbox and SharePoint/OneDrive access, further phishing from a trusted account, business email compromise, fraud, data theft, or resale to other criminals.

## Durable detection pivots
- ANY.RUN found that requests for both `*/assets/img/barr.svg` and `*/assets/img/lg.svg` in the same browser session identify the principal Kratos V1 family with about **90% recall** and a near-zero false-positive rate in its negative-control testing.
- ANY.RUN published a SHA-256 for `barr.svg`: `949895df17148c5ea29f190d2619a14b3ec648425b9cc3c5a1423553c16f3898`.
- V2 pages use a different cluster: `dsa.svg`, `sid.gif`, and `imag.jpg`. V0 used `*/PTT/SOft/` paths and a blurred-invoice “Secure File Access” presentation.
- Credential posts or related page logic may reference `next.php`, `save.php`, `/SOft/mini.php`, `di`, `pr`, `submitData()`, `#pass-err`, or a three-attempt password flow followed by an Office redirect.
- A distinctive animated envelope and “Loading in progress…” interstitial appeared before the Microsoft login imitation in observed versions.
- Asset pairing is more durable than blocking every co-hosted IP or domain. ANY.RUN cautions that shared hosting also carried Tycoon, Flowerstorm, Sneaky2FA, EvilProxy, and unrelated pages; co-location alone is not Kratos attribution.

## Defender guidance
### Email, web, and endpoint controls
- Retrospectively hunt proxy, DNS, browser, secure-email-gateway, and sandbox telemetry for paired `barr.svg` / `lg.svg` requests and the V2 asset cluster. Correlate those with Microsoft-themed login pages, QR-code lures, and credential-post endpoints.
- Search compromised web estates, especially WordPress sites, for unexpected phishing subdirectories, recently written PHP/JavaScript/assets, unauthorized administrator changes, and web-server requests for the published asset names.
- Do not bulk-block a cloud provider, Cloudflare address, shared VPS, or legitimate compromised domain solely because it co-hosted a Kratos page. Require the family asset or behavior pattern where possible.
- Train users to report document or invoice links that lead to Microsoft authentication after QR scans, unusual redirects, anti-bot gates, or animated loading interstitials.

### Identity response
- Treat a confirmed Kratos page visit with submitted credentials as an identity incident. Reset the password, verify MFA methods, and review Entra sign-ins, mailbox rules, OAuth grants, SharePoint/OneDrive access, and outbound mail.
- If reverse proxying, session relay, suspicious Microsoft sign-ins, or cookie theft cannot be excluded, revoke active sessions and refresh tokens in addition to resetting the password.
- Move high-value accounts to phishing-resistant authentication such as passkeys/FIDO2 and enforce Conditional Access appropriate to the organization.
- Search for successful sign-ins from unfamiliar infrastructure, new device/browser characteristics, token reuse after password reset, inbox access followed by internal phishing, and suspicious finance-thread manipulation.

### Post-takedown handling
- Preserve suspicious messages, QR images, redirect chains, page assets, authentication logs, session identifiers, and browser/proxy evidence before cleanup.
- Do not close incidents only because central Kratos infrastructure was disabled. Affiliates may retain victim data, deployed pages, alternate infrastructure, or reusable code.
- Use the disruption window to reset exposed identity material and remove compromised web content before surviving customers migrate to another service or name.

## Confidence and caveats
- The arrest, central-infrastructure disruption, and customer/campaign estimates are law-enforcement reporting, not a public judicial finding against every suspected user.
- ANY.RUN's victim and deployment measurements are based on its sandbox and OSINT visibility; they are not a complete census of the operation.
- A WebSocket observed on a phishing page may support live relay, but a WebSocket alone does not prove session theft. Escalate based on the complete authentication and network sequence.
- Shared infrastructure is not actor attribution. Apply the Kratos label only when family-specific assets or behavior are present.

## Related pages
- [Forg365 Microsoft 365 PhaaS](forg365-microsoft-365-phaas.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [Evilginx and device-code phishing open-directory cluster](evilginx-device-code-phishing-open-directory.md)
- [O-UNC-066 Entra passkey vishing](o-unc-066-entra-passkey-vishing.md)

## Sources
- German Federal Criminal Police Office (BKA): [https://www.bka.de/SharedDocs/Kurzmeldungen/DE/Kurzmeldungen/260720_Schlag_gegen_Phishing_Gruppierung_Kratos.html](https://www.bka.de/SharedDocs/Kurzmeldungen/DE/Kurzmeldungen/260720_Schlag_gegen_Phishing_Gruppierung_Kratos.html)
- ANY.RUN: [https://any.run/cybersecurity-blog/kratos-phaas-account-takeover/](https://any.run/cybersecurity-blog/kratos-phaas-account-takeover/)
- Microsoft tax-season campaign context: [https://www.microsoft.com/en-us/security/blog/2026/03/19/when-tax-season-becomes-cyberattack-season-phishing-and-malware-campaigns-using-tax-related-lures/](https://www.microsoft.com/en-us/security/blog/2026/03/19/when-tax-season-becomes-cyberattack-season-phishing-and-malware-campaigns-using-tax-related-lures/)
- The Hacker News summary: [https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html](https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html)
