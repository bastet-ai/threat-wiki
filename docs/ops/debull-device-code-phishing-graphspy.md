# DEBULL device-code phishing and GraphSpy post-exploitation

## Summary

ZeroBEC reported a late-June to early-July 2026 Microsoft 365 device-code phishing campaign using a reusable tooling layer it tracks as **DEBULL**. The campaign used collaboration-themed lures and legitimate Microsoft device-login flows rather than fake password pages: a compromised first-stage site generated Microsoft Authentication Broker device codes through a DEBULL backend, pushed the victim to `microsoft.com/devicelogin`, polled for token completion, and handed the attacker a Microsoft 365 session after the victim completed MFA.

ZeroBEC does **not** directly attribute the activity to Microsoft-tracked Storm-2372, but assesses strong Storm-2372-style tradecraft: Teams/messaging-style lures, Microsoft Authentication Broker device-code flow abuse, geo-plausible infrastructure, and follow-on device-registration behavior. A post-authentication device object named `GraphSpy-Device` led ZeroBEC to assess with high probability that DEBULL uses GraphSpy or a GraphSpy-derived workflow for Microsoft 365 / Entra post-exploitation.

## Tags

- ops
- operations
- phishing
- PhaaS
- device-code phishing
- OAuth
- Entra ID
- Microsoft 365
- Microsoft Authentication Broker
- Storm-2372
- DEBULL
- GraphSpy
- token theft
- cloud identity
- MFA bypass
- phishing infrastructure
- ZeroBEC

## Why this matters

- Device-code phishing produces real Microsoft sign-ins and valid OAuth tokens; successful MFA is part of the compromise path, not proof of safety.
- DEBULL appears to package the chain into reusable PhaaS-style infrastructure with page templates, analytics, custom-domain publishing, and Cloudflare Workers deployment support.
- The observed `GraphSpy-Device` artifact gives defenders a concrete post-authentication pivot for tenant hunts.
- The chain used a legitimate compromised website as first-stage delivery, making domain-age and basic reputation checks less reliable.

## Reported chain

ZeroBEC describes the observed campaign as follows:

1. A minimal payment / shared-folder lure reached the victim mailbox with a `Team_Meets` URL path and no attachment to detonate.
2. The victim opened a compromised Croatian rental website path: `hxxps://trogir-rental[.]com/Team_Meets/`.
3. The landing page presented a fake encrypted secure-message UI and called the DEBULL broker at `hxxps://frenksv[.]sbs/user/email/office_poll.php?uid=4`.
4. The broker generated a Microsoft Authentication Broker device-code challenge with `tenant_id: common`.
5. The victim was sent to Microsoft's legitimate `hxxps://www.microsoft[.]com/devicelogin` page and entered the attacker-supplied code.
6. The landing page polled `poll_auth_broker_token` until the device-code flow completed.
7. The attacker-side session was created from `162.35.167[.]138` and later continued from `96.126.176[.]130` through OfficeHome / Outlook Web.
8. A `GraphSpy-Device` object appeared after authentication.
9. The victim was redirected to `hxxps://outlook.office[.]com/`, reducing user-visible suspicion.

## DEBULL backend exposure

ZeroBEC pivoted from the attacker-side Authentication Broker session IP to a directly exposed DEBULL login panel on `162.35.167[.]138` over HTTP and HTTPS. Additional exposed material reportedly showed:

- `phpinfo` exposure with document root `/var/www/token`.
- A virtual-host hint of `debull[.]app:0`.
- Apache 2.4.66 on Ubuntu, PHP 8.5.4, cURL, MySQL support, and OPcache.
- A compact PHP / Composer application.
- `/user/email/deploy.php`, suggesting a PhaaS deployment layer with phishing page creation, reusable templates, analytics, custom-domain publishing, and Cloudflare Workers deployment.
- Broader profile-routing and notification capabilities referencing Office, Gmail, IMAP, chat, file-transfer, voice-message, Telegram, and email-notification workflows.

ZeroBEC also found Turkish-language code-lineage markers in separate components: `Code'u otomatik kopyala` in the landing page and `SAYAÇ` in the DEBULL header component. Treat those as codebase or template lineage signals, not as standalone attribution.

## Defender heuristics

### Entra ID / Microsoft 365 hunts

- Hunt for device-code sign-ins using Microsoft Authentication Broker where the user was not actively enrolling or configuring a device.
- Review sign-ins followed by unusual OfficeHome, Outlook Web, Graph API, mailbox, OneDrive, SharePoint, or Teams access from a different IP or geography than the victim's normal session.
- Search Entra ID device inventory and audit logs for `GraphSpy-Device` or similarly suspicious newly registered device names.
- Correlate `deviceCode` / Authentication Broker events with mail lures that ask users to enter or copy a code into a Microsoft page.
- Revoke refresh tokens and sessions for affected users; password reset alone is insufficient when OAuth tokens have already been minted.

### Email and web controls

- Flag unsolicited collaboration or secure-message lures that send users to `microsoft.com/devicelogin`, especially when the initial URL path resembles Teams / meeting / shared-folder language.
- Do not trust domain age or sender authentication alone. ZeroBEC's sample inherited legitimate mail-authentication signals and used a compromised first-stage website.
- Monitor for `office_poll.php`, `get_auth_broker_device_code`, `poll_auth_broker_token`, `Team_Meets`, and secure-message pages that open `microsoft.com/devicelogin` then redirect to Outlook.

### Incident response

- Preserve original messages, URLs, redirect chains, browser history, proxy logs, Entra sign-in logs, audit logs, device-registration events, application-consent events, and mailbox/Graph activity after the device-code timestamp.
- Review mailbox rules, delegated permissions, OAuth consents, outbound mail, OneDrive downloads, SharePoint file access, Teams access, and newly registered devices.
- If `GraphSpy-Device` or GraphSpy-like behavior appears, assume the actor attempted Microsoft Graph post-exploitation and scope beyond email alone.

## Related pages

- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [GraphSpy](../tools/graphspy.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources

- ZeroBEC, DEBULL: Storm-2372-Style Microsoft Device-Code Phishing With GraphSpy Post-Exploitation: [https://zerobec.com/blog/debull-storm-2372-microsoft-device-code-phishing-graphspy](https://zerobec.com/blog/debull-storm-2372-microsoft-device-code-phishing-graphspy)
- The Hacker News summary: [https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html](https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html)
- Microsoft OAuth 2.0 device authorization grant documentation: [https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code)
