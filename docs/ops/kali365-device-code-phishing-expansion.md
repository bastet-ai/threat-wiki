# Kali365 device-code phishing expansion

## Summary
Arctic Wolf Labs reports that **Kali365** is a phishing-as-a-service operation abusing OAuth device authorization flows for token theft and expanding beyond Microsoft 365 lures into a multi-brand phishing cluster.

The April 2026 activity used Microsoft device-code phishing: victims were socially engineered to enter an attacker-provided code at Microsoft's legitimate device login page, causing Microsoft to issue access and refresh tokens to an attacker-controlled application. Arctic Wolf's June 2026 follow-up connected the same operator to 126 malicious hosts, a live token-capture panel, Microsoft Outlook / Live, Okta SSO, Xerox DocuShare, AWS-themed, GMX, Mail.ru, Odnoklassniki, Yandex Disk, and MAX Messenger impersonation.

Kaspersky's July 6, 2026 Securelist writeup adds a separate real-world device-code phishing cluster active from early April to mid-May 2026 and continuing in modified regional campaigns. That chain used law-firm-themed email, a password-protected PDF, Microsoft redirector parameters, CAPTCHA-gated fake legal-portal pages, clipboard-copy behavior for the attacker-generated `user_code`, and Microsoft's real device-login page to collect OAuth tokens after the victim completed MFA.

ZeroBEC's July 2026 DEBULL report adds another device-code phishing cluster active in late June and early July: collaboration-themed lures used a compromised first-stage site, a DEBULL broker endpoint, Microsoft Authentication Broker device-code flows, attacker-side sessions from `162.35.167[.]138` and `96.126.176[.]130`, and a `GraphSpy-Device` post-authentication artifact.

Treat this as an identity-compromise operation, not a password-only phishing kit. Successful victims may have valid OAuth tokens issued by the real identity provider, so MFA success in the logs does not prove the session is benign.

## Tags
- ops
- operations
- phishing
- PhaaS
- device-code phishing
- OAuth
- Entra ID
- Microsoft 365
- Okta
- credential-theft
- token-theft
- social-engineering
- cloud identity
- Kaspersky Securelist
- Microsoft Identity Platform
- refresh token theft
- OneDrive access
- Teams access
- DEBULL
- GraphSpy
- Microsoft Authentication Broker

## Why this matters
- Device-code phishing routes the victim through a legitimate identity-provider page, which can bypass user training and MFA assumptions built around fake login forms.
- The actor receives OAuth tokens rather than just passwords, so response needs token/session revocation, application consent review, and mailbox/SaaS activity review.
- The June 2026 expansion shows one PhaaS operator can reuse infrastructure and panels across enterprise identity targets and consumer messaging or cloud-service brands.
- The MAX Messenger lure matters because account takeover in a large messaging platform can become both monetization and propagation, while the same infrastructure still targets enterprise services.

## Reported chain

### Microsoft device-code flow abuse
- The attacker initiates an OAuth 2.0 device authorization request against an attacker-controlled application and receives a legitimate `user_code`.
- A lure page frames the code as a secure document, OneDrive, or SharePoint-style workflow and directs the victim to Microsoft's real device login endpoint.
- If the victim enters the code and completes authentication, Microsoft issues OAuth access and refresh tokens to the attacker-controlled application.
- Arctic Wolf's April report tied this to Kali365 Live affiliate infrastructure and observed activity across manufacturing, education, government, insurance, financial, healthcare, North American, and EMEA targets.

### Kali365 platform and infrastructure
- Arctic Wolf describes Kali365 / K365 as an emerging PhaaS platform first seen in April 2026.
- The April campaign centered on `kali365[.]xyz`, `v2.kali365[.]xyz`, and `api.kali365[.]xyz`, plus TLS-pivot sibling infrastructure.
- Arctic Wolf's follow-up found the June cluster using a backend under `securehubcloud[.]com` and a primary phishing zone under `attachedfile[.]com`.
- A still-live phishing page polled `panel[.]securehubcloud[.]com` every three seconds to check token-capture status.

### Multi-brand expansion
Arctic Wolf's June 2026 follow-up says the operator expanded into a 126-host cluster impersonating:

- Microsoft Outlook and Microsoft Live.
- Okta SSO.
- Xerox DocuShare.
- LiveDrive.
- AWS-looking naming patterns such as `vpce.` and `apm.`.
- GMX.
- Russian internet services including Mail.ru, Odnoklassniki, and Yandex Disk.
- MAX Messenger, using a prize-claim flow and Telegram bot exfiltration for the takeover variant.

Arctic Wolf assesses this as the same operator behind the earlier OneDrive device-code phish, now running a broader multi-brand phishing operation with both Western enterprise targets and Russian-service targeting.

### Kaspersky legal-portal / Microsoft Identity Platform chain
Kaspersky's July 2026 Securelist analysis describes a separate device-code phishing campaign observed from early April through mid-May 2026, with later adaptations toward Brazil and other regional targeting.

Reported sequence:

1. The victim received a law-firm-themed email with a password-protected PDF attachment.
2. The PDF led to a document-listing page and then through a Microsoft URL whose parameters redirected the user to an attacker-controlled fake corporate legal portal.
3. The phishing site presented multiple CAPTCHAs to filter scanners and then showed a one-time code.
4. Clicking the displayed code copied the attacker-generated `user_code` to the clipboard and redirected the victim to Microsoft's legitimate device-login page.
5. The victim entered the code and completed MFA on Microsoft's real page, causing Microsoft to issue `access_token`, `refresh_token`, and `id_token` material to the attacker-controlled app polling the device-code flow.
6. Kaspersky says the resulting access enabled mailbox read/send activity, OneDrive file exfiltration, and Teams conversation access.

This update reinforces the core defensive point: legitimate Microsoft URLs and successful MFA are not sufficient proof that the authenticated session belongs to the user-intended device or application.

### ZeroBEC DEBULL / GraphSpy chain
ZeroBEC's July 2026 report describes a late-June to early-July Microsoft 365 campaign it tracks as DEBULL. This appears separate from Kali365, but it belongs on this watch page because it exercises the same defensive failure mode: legitimate Microsoft device-code authentication converts a social-engineering lure into attacker-held OAuth tokens.

Reported DEBULL sequence:

1. A payment / shared-folder lure pointed the victim to a compromised website path, `hxxps://trogir-rental[.]com/Team_Meets/`.
2. The landing page called a DEBULL broker endpoint at `hxxps://frenksv[.]sbs/user/email/office_poll.php?uid=4` with `get_auth_broker_device_code`.
3. The victim was pushed to `hxxps://www.microsoft[.]com/devicelogin` and saw a Microsoft Authentication Broker prompt.
4. The page polled `poll_auth_broker_token` until the user completed the legitimate Microsoft flow.
5. Attacker-side Microsoft 365 sessions were observed from `162.35.167[.]138` and `96.126.176[.]130`.
6. A post-authentication device object named `GraphSpy-Device` appeared, which ZeroBEC ties with high confidence to GraphSpy or a GraphSpy-derived Microsoft Graph post-exploitation workflow.

ZeroBEC found a directly exposed DEBULL panel on `162.35.167[.]138`, `phpinfo` leakage with document root `/var/www/token`, a `debull[.]app:0` vhost hint, and `/user/email/deploy.php` functionality consistent with a PhaaS deployment layer for templates, analytics, custom-domain publishing, and Cloudflare Workers deployment. Turkish-language code markers appeared in separate components, but ZeroBEC treats those as lineage markers rather than direct attribution.

## Defender heuristics

### Identity triage
- Hunt for successful Microsoft device-code sign-ins followed by unusual mailbox, SharePoint, OneDrive, Graph API, or OAuth-client activity.
- Review Entra ID sign-in logs for device-code authentication flows, unfamiliar application IDs, suspicious consent grants, and impossible or unusual geolocation after the user authenticated successfully. Include successful MFA events where the initiating workflow was an unsolicited document, legal notice, QR code, or copy/paste code prompt.
- Search Entra ID device-registration and audit logs for `GraphSpy-Device` or other newly registered devices immediately after Microsoft Authentication Broker / device-code sign-ins.
- Revoke refresh tokens and active sessions for confirmed victims; password reset alone is insufficient if OAuth tokens remain valid.
- Review mailbox rules, forwarding, delegated app permissions, Graph API usage, SharePoint/OneDrive downloads, Teams access, and SaaS sessions established after the device-code event.

### User and workflow controls
- Train users that Microsoft device-login prompts should only be completed from a device they are physically configuring.
- Where possible, restrict or monitor device-code authentication for users and applications that do not need it.
- Alert on secure-document lures that ask users to copy a code into a legitimate identity-provider page.
- Treat MFA-completed sessions as suspicious when the authentication context started from an unsolicited code or document workflow.

### Network and infrastructure pivots
- Monitor for domains and subdomains in Arctic Wolf's IOC package, especially `securehubcloud[.]com`, `attachedfile[.]com`, and the `kali365[.]xyz` panel family.
- Use the content string `Preparing your secure document...` as a hunting pivot where web-proxy, email-sandbox, or VirusTotal-style content search is available.
- Treat PDF attachments or web pages that ask users to copy a code and then open `microsoft.com/devicelogin` or `login.microsoftonline.com` as high-risk, even if the final authentication page is legitimate.
- Hunt for DEBULL pivots from ZeroBEC's July 2026 report: `frenksv[.]sbs`, `trogir-rental[.]com/Team_Meets/`, `162.35.167[.]138`, `96.126.176[.]130`, `office_poll.php`, `get_auth_broker_device_code`, `poll_auth_broker_token`, and `GraphSpy-Device`.
- For MAX Messenger-themed incidents, review Telegram bot and chat identifiers from Arctic Wolf's IOC repository in addition to web infrastructure.

## Related pages
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [GraphSpy](../tools/graphspy.md)
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [BlackFile / UNC6671 vishing extortion operation](blackfile-unc6671-vishing-extortion.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- Arctic Wolf Labs, April 2026 Kali365 / Token Bingo report: <https://arcticwolf.com/resources/blog/token-bingo-dont-let-your-code-be-the-winner/>
- Arctic Wolf Labs, June 2026 Kali365 expansion report: <https://arcticwolf.com/resources/blog/kali365-expands-into-aws-microsoft-okta-xerox-max-messenger/>
- Arctic Wolf public IOC repository: <https://github.com/rtkwlf/wolf-tools/tree/main/threat-intelligence/kali365-expands-into-aws-microsoft-okta-xerox-max-messenger>
- Kaspersky Securelist, July 2026 device-code phishing report: <https://securelist.com/microsoft-device-code-phishing-attack/120350/>
- ZeroBEC, DEBULL / GraphSpy Microsoft device-code phishing report: <https://zerobec.com/blog/debull-storm-2372-microsoft-device-code-phishing-graphspy>
- The Hacker News DEBULL summary: <https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html>
- Microsoft OAuth 2.0 device authorization grant documentation: <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code>
