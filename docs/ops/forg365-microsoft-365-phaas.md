# Forg365 Microsoft 365 PhaaS

## Summary
ZeroBEC's July 2026 research describes **Forg365**, a Telegram-distributed phishing-as-a-service platform for Microsoft 365 account compromise. The kit combines device-code phishing, adversary-in-the-middle routing, anti-bot filtering, AI-assisted lure generation, SMTP rotation, token vaulting, mailbox/inbox tooling, and a companion browser-extension workflow for persistent Microsoft SSO access.

The durable defender lesson is that device-code authentication and session-transfer workflows need to be treated as identity-risk surfaces. Forg365 can drive victims through legitimate Microsoft authentication surfaces while the operator receives OAuth/session material and then manages post-compromise access through a productized panel.

## Tags
- ops
- phishing
- phishing-as-a-service
- Microsoft 365
- Microsoft Entra ID
- device-code phishing
- OAuth device authorization grant
- adversary-in-the-middle
- AiTM
- session cookie theft
- token theft
- token replay
- mailbox compromise
- Telegram
- AI-assisted phishing
- SMTP abuse
- Amazon SES
- Twilio SendGrid
- Cloudflare
- browser extension
- Forg365
- ForgCookie
- Kali365
- Octopi365
- Freedom365
- Sneaky 2FA
- ZeroBEC
- The Hacker News

## Reported activity
- Forg365 is sold and supported through Telegram, with ZeroBEC observing subscription-style onboarding, trial access, operator invitations, and campaign-management workflows.
- The panel advertises account management, link generation, invitations, OAuth application configuration, redirect-link handling, SVG/lure generation, campaign sending, SMTP profile rotation, AI email generation, token vaulting, account intelligence, keyword alerts, viewer links, inbox sync, and browser-extension support.
- Attack chains use business-document and remittance-approval lures. ZeroBEC and The Hacker News report use of legitimate delivery infrastructure such as Amazon SES and Twilio SendGrid to make the redirect chain look less anomalous before the victim reaches Forg365-controlled infrastructure.
- The device-code branch presents a Microsoft-styled verification-code page and pushes the victim into the legitimate Microsoft Authentication Broker / device-login flow. The victim satisfies real Microsoft authentication, but the resulting authorization benefits the attacker.
- The AiTM branch fits the Sneaky 2FA-style class: Microsoft 365 traffic is proxied or replayed so the operator can capture session material rather than only credentials.
- ZeroBEC reports post-compromise workflows for token/cookie handling, automatic session refresh, inbox access, keyword listeners, and a Manifest V3 browser extension named **ForgCookie** for persistent Microsoft SSO access.
- Observed operator infrastructure included the clearnet panel path `logfriend[.]com/login`; treat this as a point-in-time indicator, not the only infrastructure.

## Why this matters
- **Device-code phishing bypasses the mental model of “fake login page equals phishing.”** The victim may interact with legitimate Microsoft authentication surfaces while authorizing the attacker-controlled session.
- **The kit productizes the full identity intrusion loop.** Lure generation, delivery, token capture, session persistence, mailbox intelligence, and operator workflows are in one service, lowering the skill needed to run campaigns.
- **Legitimate mail and CDN infrastructure blur first-hop telemetry.** Amazon SES, SendGrid-hosted resources, Cloudflare-hosted pages, and similar commodity services should not be treated as sufficient reassurance when the authentication flow is abnormal.
- **Post-authentication controls matter.** Once OAuth/session material is captured, mailbox rules, OAuth grants, refresh-token behavior, and session-cookie reuse become the key incident-response surface.

## Defender guidance
1. Block or narrowly scope Microsoft OAuth device-code flow where it is not business-critical. Use Conditional Access report-only testing before enforcement for legitimate shared devices, Teams rooms, CLI tools, and constrained-device workflows.
2. Hunt Entra sign-in logs for device-code authentication by users, geographies, device types, clients, or user agents that do not normally use it.
3. Alert on suspicious OAuth application consent, refresh-token use, and Microsoft Authentication Broker flows that follow unusual email-click or redirect activity.
4. For suspected compromise, revoke refresh tokens, invalidate sessions, review OAuth grants, inspect mailbox rules/forwarding, search for suspicious inbox keyword access, and review SharePoint/OneDrive/Teams activity.
5. Treat user reports of being asked to visit `microsoft.com/devicelogin`, enter a code, scan a QR code, or approve an Authenticator prompt from an email lure as identity incidents.
6. Add detections for high-risk combinations: legitimate bulk email delivery + URL shortener/redirect chain + Microsoft device-login prompts + new token grants from unfamiliar infrastructure.
7. Where browser extensions are used to preserve sessions, include browser extension inventory and local profile review in post-compromise triage.

## Related pages
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [Evilginx and device-code phishing open-directory cluster](evilginx-device-code-phishing-open-directory.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)

## Sources
- [ZeroBEC](https://zerobec.com/blog/inside-forg365-telegram-distributed-sneaky2fa-style-phaas)
- [The Hacker News](https://thehackernews.com/2026/07/forg365-phaas-targets-microsoft-365.html)
- [Microsoft Storm-2372 device-code phishing report](https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/)
- [Microsoft AI-enabled device-code phishing report](https://www.microsoft.com/en-us/security/blog/2026/04/06/ai-enabled-device-code-phishing-campaign-april-2026/)
- [Microsoft device-code Conditional Access guidance](https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-teams-devices-device-code-flow)
