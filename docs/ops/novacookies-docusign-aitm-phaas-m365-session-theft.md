# NovaCookies: Docusign-notification-driven AitM PhaaS stealing Microsoft 365 sessions (Sneaky2FA variant)

## Summary
On **August 26, 2026**, Island Security disclosed details (via a report shared with The Hacker News ahead of publication) of **NovaCookies**, an **adversary-in-the-middle (AitM) phishing toolkit** operating as a **$320/month subscription phishing-as-a-service (PhaaS)** platform that relays Microsoft 365 sign-ins through attacker-controlled infrastructure and captures authenticated sessions — including MFA. The kit has been used against **hundreds of organizations across multiple sectors in the U.S., U.K., Canada, Germany, Israel, and the U.A.E.** Proofpoint assesses NovaCookies to be a **variant of the Sneaky 2FA phishing kit**, extending its original Microsoft-account focus with dedicated flows for other identity providers, including **Okta** and **Entra domains federated to GoDaddy**.

The durable tradecraft pattern: campaigns used **genuine Docusign envelopes to carry counterfeit document-share lures**, with some clicks routed through **legitimate Microsoft or Google sign-in endpoints as redirect hops** before reaching the kit — so the message, the document service, and the redirect can each appear trustworthy in isolation until the browser reaches attacker-controlled infrastructure.

## Tags
- ops
- phishing
- AitM
- adversary-in-the-middle
- PhaaS
- phishing-as-a-service
- NovaCookies
- Sneaky 2FA
- Sneaky2FA
- Docusign
- document-share lure
- Microsoft 365
- session theft
- MFA bypass
- pass-the-cookie
- OAuth error redirect
- .vu TLD
- PwPt-sHaRe
- Ms36-AcCeSs
- ClOd-ViEw
- fordmotbvmorcompany.vu
- Telegram
- subscription PhaaS
- Okta
- GoDaddy federation
- Island Security
- Proofpoint
- anti-analysis
- Cloudflare gate
- debugging detection
- cybercrime

## How the campaign works
1. **Genuine Docusign delivery:** the victim receives a *real* Docusign notification (genuine sender-authentication and reputation pass because the email really is a Docusign share notice), styled as an accounting department sharing a "remittance-advice PDF." The malicious destination sits **inside the shared document, below the layer most mail security products inspect**.
2. **Redirect hops:** some clicks are routed through legitimate Microsoft or Google sign-in endpoints before reaching the kit, so each hop looks legitimate on its own — "a trusted delivery service, an identity-provider redirect, then a familiar sign-in page."
3. **OAuth error-redirect into the relay:** the attack uses an **OAuth error-redirect technique previously detailed by Microsoft (March 2026)** to hand the victim to attacker-controlled infrastructure.
4. **Live AitM session capture:** the NovaCookies relay captures credentials and MFA codes and relays them to Microsoft in real time, harvesting the authenticated session — the standard AitM session-theft model.
5. **Anti-analysis:** the kit evades security scanners with a **Cloudflare gate** and a mechanism to detect **debugging-tool execution passes** before serving the bogus login form.

## Observable characteristics (per Island, via THN)
- **Lure domains:** many hosted on **`.vu`**, e.g. `fordmotbvmorcompany[.]vu`.
- **Phishing URLs with alternating-case labels** masquerading as Microsoft services: `PwPt-sHaRe`, `Ms36-AcCeSs`, `ClOd-ViEw`.
- **Distribution/support:** advertised via **Telegram**, which is also used to manage customer profiles, configure redirect services, and contact support — a centrally managed PhaaS operator model rather than per-affiliate hosting.

## Why it matters
- **Trusted-brand notification abuse with the payload inside the document** defeats envelope-level mail filtering: the email is authentic Docusign; the malice is in the content. Document-share lures inside trusted SaaS notifications are a growing pattern (compare Mirage2FA's M365 login-flow abuse).
- **PhaaS economics:** at $320/month with central hosting, non-technical actors can run AitM MFA-bypass campaigns at scale. This is one of several new subscription PhaaS services emerging in recent months (e.g., the AnonyMousKIT AI-vishing service noted in the same report).
- **Multi-IdP scope:** unlike original Sneaky2FA (Microsoft-focused), the NovaCookies variant covers **Okta and GoDaddy-federated Entra** — relevant for SaaS-heavy environments using non-Microsoft IdPs.

## Defender priorities
1. **Treat trusted-SaaS notifications as inspectable content:** Docusign (and similar) share notices are not free from inspection; content-aware inspection of shared-document links is the control, plus user guidance that shared documents inside trusted-service emails can still be malicious.
2. **Hunt the URL patterns:** `.vu`-hosted lures, alternating-case Microsoft-service label strings (`PwPt-sHaRe`, `Ms36-AcCeSs`, `ClOd-ViEw`), and OAuth error-redirect URLs pointing at unfamiliar infrastructure.
3. **Monitor OAuth error-redirect behavior:** the technique Microsoft documented in March 2026 is the hand-off point — alert on OAuth error-redirect flows that terminate at non-corporate infrastructure.
4. **Session-hygiene baseline:** with AitM session capture active at scale, keep conditional-access refresh, token-lifetime controls, and PRT (Primary Refresh Token) revocation runbooks tested — stolen M365 sessions are the direct objective.
5. **Multi-IdP scope:** extend detection beyond M365 to Okta and any GoDaddy-federated Entra flows if present.

## Caveats
- Island's assessment and the Proofpoint variant assessment are as reported by The Hacker News (August 26, 2026); Island's own blog post was not independently reachable at scan time.
- "Hundreds of organizations" is Island's characterization of observed campaigns, not a confirmed victim list.
- No actor attribution beyond the PhaaS operator model; the kit is commercialized tooling, not a named threat group.

## Timeline
- **March 2026** — Microsoft details the OAuth error-redirect technique later used by the campaign.
- **July 2026 (approx.)** — Proofpoint posts its assessment of NovaCookies as a Sneaky2FA variant (X post, "last month" as of the August 26 report).
- **August 26, 2026** — Island report via The Hacker News disclosure.

## Related pages
- [Mirage2FA M365 PhaaS: 4,500 US and EU companies](mirage2fa-m365-phishing-4500-companies-anyrun.md)
- [Forg365 Microsoft 365 PhaaS](forg365-microsoft-365-phaas.md)
- [Kratos Microsoft 365 PhaaS and infrastructure disruption](kratos-microsoft-365-phaas-disruption.md)
- [JWR phishing framework (likely The Outsider variant)](jwr-phaas-phishing-framework-outsider-variant.md)

## Sources
- The Hacker News (Ravie Lakshmanan): [NovaCookies Campaigns Abuse Genuine Docusign Notifications to Steal Microsoft 365 Sessions](https://thehackernews.com/2026/08/novacookies-campaigns-abuse-genuine.html) (August 26, 2026; cites Island Security's pre-publication report and Proofpoint's assessment)
- Island Security blog (referenced in the THN report; blog listing not independently reachable at scan time)
- Proofpoint assessment of NovaCookies as a Sneaky2FA variant (X post, referenced in the THN report)
