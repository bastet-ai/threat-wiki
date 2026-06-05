# Kali365 device-code phishing expansion

## Summary
Arctic Wolf Labs reports that **Kali365** is a phishing-as-a-service operation abusing OAuth device authorization flows for token theft and expanding beyond Microsoft 365 lures into a multi-brand phishing cluster.

The April 2026 activity used Microsoft device-code phishing: victims were socially engineered to enter an attacker-provided code at Microsoft's legitimate device login page, causing Microsoft to issue access and refresh tokens to an attacker-controlled application. Arctic Wolf's June 2026 follow-up connected the same operator to 126 malicious hosts, a live token-capture panel, Microsoft Outlook / Live, Okta SSO, Xerox DocuShare, AWS-themed, GMX, Mail.ru, Odnoklassniki, Yandex Disk, and MAX Messenger impersonation.

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

## Defender heuristics

### Identity triage
- Hunt for successful Microsoft device-code sign-ins followed by unusual mailbox, SharePoint, OneDrive, Graph API, or OAuth-client activity.
- Review Entra ID sign-in logs for device-code authentication flows, unfamiliar application IDs, suspicious consent grants, and impossible or unusual geolocation after the user authenticated successfully.
- Revoke refresh tokens and active sessions for confirmed victims; password reset alone is insufficient if OAuth tokens remain valid.
- Review mailbox rules, forwarding, delegated app permissions, SharePoint/OneDrive downloads, and SaaS sessions established after the device-code event.

### User and workflow controls
- Train users that Microsoft device-login prompts should only be completed from a device they are physically configuring.
- Where possible, restrict or monitor device-code authentication for users and applications that do not need it.
- Alert on secure-document lures that ask users to copy a code into a legitimate identity-provider page.
- Treat MFA-completed sessions as suspicious when the authentication context started from an unsolicited code or document workflow.

### Network and infrastructure pivots
- Monitor for domains and subdomains in Arctic Wolf's IOC package, especially `securehubcloud[.]com`, `attachedfile[.]com`, and the `kali365[.]xyz` panel family.
- Use the content string `Preparing your secure document...` as a hunting pivot where web-proxy, email-sandbox, or VirusTotal-style content search is available.
- For MAX Messenger-themed incidents, review Telegram bot and chat identifiers from Arctic Wolf's IOC repository in addition to web infrastructure.

## Related pages
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [BlackFile / UNC6671 vishing extortion operation](blackfile-unc6671-vishing-extortion.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- Arctic Wolf Labs, April 2026 Kali365 / Token Bingo report: https://arcticwolf.com/resources/blog/token-bingo-dont-let-your-code-be-the-winner/
- Arctic Wolf Labs, June 2026 Kali365 expansion report: https://arcticwolf.com/resources/blog/kali365-expands-into-aws-microsoft-okta-xerox-max-messenger/
- Arctic Wolf public IOC repository: https://github.com/rtkwlf/wolf-tools/tree/main/threat-intelligence/kali365-expands-into-aws-microsoft-okta-xerox-max-messenger
- Microsoft OAuth 2.0 device authorization grant documentation: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code
