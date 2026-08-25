# Mirage2FA PhaaS: 4,500 US and EU companies hit via Microsoft 365 login-flow abuse

## Summary
ANY.RUN research (via The Hacker News, August 25, 2026) documents the scale of the **Mirage2FA** commercial **phishing-as-a-service (PhaaS)** campaign, active from 2024 through 2026 against **Microsoft 365** accounts. Mirage2FA abuses legitimate M365 login flows to bypass two-factor authentication and steal passwords and **session cookies**, letting attackers join authenticated M365 sessions and reach SSO-connected services. ANY.RUN estimates the campaign is linked to **4,532 unique organization email domains**, with **48% of targeted email addresses potentially compromised**. The United States accounts for **63.7%** of victims; the rest span India, Singapore, the UK, Canada, Saudi Arabia, South Africa, and other countries. Technology, manufacturing, and education were among the most targeted industries. ANY.RUN uncovered **more than 9,000 potential compromise events** involving cookie/password theft, SSO logins, and 2FA bypass.

## Tags
- ops
- operations
- Mirage2FA
- phishing-as-a-service
- PhaaS
- Microsoft 365
- M365
- adaptive identity management
- AiTM
- adaptive identity phishing
- session cookie theft
- SSO
- 2FA bypass
- ANY.RUN
- enterprise identity
- enterprise security

## Campaign mechanics
- Mirage2FA is a commercial PhaaS toolkit sold to operators, not a single-actor campaign — treat it as a reusable service rather than one intrusion chain.
- The attack abuses **legitimate M365 login flows** (adaptive-identity / AiTM shape): the victim authenticates through a forged but protocol-valid flow, so the session token/cookie is issued by Microsoft's own infrastructure and carries normal MFA posture.
- Stolen **session cookies** are the primary prize: they let the attacker act as the authenticated user without re-triggering M365 sign-in, and SSO federation extends the foothold to connected enterprise apps.
- ANY.RUN's scoping: ~4,532 organization domains, 63.7% US-based, 9,000+ potential compromise events, 48% of targeted addresses potentially compromised.
- Impact compounds beyond the initial account: follow-on access through SSO-connected apps and internal workflows widens the attack radius and raises containment cost.

## Defender heuristics
1. **Treat session theft as an identity incident, not a password event** — rotating passwords does not kill a live stolen M365 session; force session invalidation / sign-in everywhere and review conditional-access refresh.
2. **Alert on anomalous sign-in flow shapes** in M365 audit: successful MFA + immediate SSO fan-out to apps the user has not recently used, impossible-travel pairs, and access-token reuse across devices.
3. **Enforce the strongest authentication posture possible**: phishing-resistant MFA (FIDO2/passkeys), conditional access that requires device compliance and token freshness, and per-app MFA for the highest-value apps to blunt SSO fan-out.
4. **Hunt for cookie-based access**: correlate M365 sign-in events with downstream SSO app authentications that bypass a fresh sign-in; a session that appears in an SSO app with no preceding interactive M365 sign-in is the session-theft signature.
5. **Scope exposure like ANY.RUN did**: inventory which M365 domains in your org chart appear in public PhaaS victim disclosures, and assume the credential/session classes (password, refresh token, session cookie) are all in scope for rotation and revocation.

## Related pages
- [Marimo CVE-2026-75149: attacker-supplied MCP command runs before cells execute](../tools/marimo-cve-2026-75149-mcp-command-injection.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- The Hacker News: [Mirage2FA Surge Hits 4,500 US and EU Companies, Abusing Microsoft 365 Login Flows](https://thehackernews.com/2026/08/mirage2fa-surge-hits-4500-us-and-eu.html)
- ANY.RUN research (campaign scope, compromise-event counts, and mitigation guidance referenced in the THN coverage)
