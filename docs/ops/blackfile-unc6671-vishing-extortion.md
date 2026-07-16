# BlackFile / UNC6671 vishing extortion operation

## Summary
Google Threat Intelligence Group reported **UNC6671**, operating under the **BlackFile** brand, as an active extortion cluster that uses voice phishing, adversary-in-the-middle credential capture, and SSO / SaaS compromise rather than a product vulnerability. The group targets Microsoft 365 and Okta environments, persists by registering attacker-controlled MFA devices, exfiltrates data from SaaS platforms, and pressures victims through BlackFile-branded data-leak and direct-extortion workflows.

## Tags
- ops
- operations
- vishing
- social-engineering
- identity
- AiTM
- MFA-bypass
- SaaS
- Microsoft 365
- Okta
- SharePoint
- OneDrive
- Salesforce
- Zendesk
- extortion
- BlackFile
- UNC6671

## Why this matters
- This is an identity-first extortion chain: no exploited CVE is required if help-desk impersonation can defeat MFA enrollment and SSO controls.
- Personal-cell vishing bypasses many enterprise email and endpoint controls, while real-time AiTM workflows can turn a victim's MFA response into immediate account control.
- The actor's data theft includes programmatic API and direct HTTP access patterns that may log as `FileAccessed` rather than obvious `FileDownloaded` events.
- The campaign reinforces phishing-resistant MFA, MFA-device enrollment controls, and SaaS audit-log coverage as tier-0 defenses.

## Reported chain
1. Callers contact targeted employees, often on personal phones, while impersonating internal IT or help-desk staff.
2. Pretexts include mandatory passkey migration, SSO enrollment, or MFA updates.
3. The victim is directed to a victim-branded SSO lookalike hosted on actor-controlled infrastructure.
4. The actor captures username and password in real time and submits them to the legitimate identity provider.
5. The actor relays MFA prompts or codes, then immediately registers an attacker-controlled MFA device for persistence.
6. With SSO access, the actor pivots into Microsoft 365, Okta-connected SaaS applications, SharePoint, OneDrive, Zendesk, Salesforce, and related repositories.
7. Operators search for terms such as `confidential` and `SSN`, enumerate corporate directories, and collect high-value business, HR, support, CRM, and mailbox data.
8. Exfiltration uses Python, PowerShell, Microsoft Graph, direct HTTP GET requests, and captured session cookies such as `FedAuth`.
9. Victims receive direct extortion messages under the BlackFile brand, commonly with 72-hour deadlines and Tox or Session contact identifiers.

## Infrastructure and tradecraft notes
Google reports that UNC6671 shifted from unique organization-tailored phishing domains to a subdomain model. Recent themes referenced passkey or enrollment language and used domains such as:

- `.enrollms[.]com`
- `.passkeyms[.]com`
- `.setupsso[.]com`

GTIG assesses UNC6671 as distinct from ShinyHunters / UNC6240 despite overlap in SaaS data-theft techniques and at least one case where UNC6671 co-opted the ShinyHunters brand for perceived credibility. The distinction is based on separate Tox communication channels, unique domain-registration patterns, and the dedicated BlackFile data leak site.

## Indicators and hunt pivots
- Vishing reports involving passkey migration, SSO setup, or MFA enrollment calls to personal phones.
- New MFA device registrations immediately after suspicious interactive sign-ins.
- SSO sign-ins followed by rapid access to SharePoint, OneDrive, Zendesk, Salesforce, ServiceNow, or corporate directory exports.
- Microsoft 365 file activity that appears as `FileAccessed` with high-volume direct resource URL access rather than only `FileDownloaded`.
- Python `requests`, PowerShell, Microsoft Graph, or browser-cookie reuse against document repositories from unusual hosts or user agents.
- Internal SaaS searches for strings such as `confidential`, `SSN`, `NDA`, `HR`, `billing`, or customer-support exports.
- Extortion email subjects resembling `[COMPANY NAME] DATA BREACH 72 HOURS TO CONTACT US`.
- Tox or Session contact IDs embedded in post-theft negotiation messages.

## Defender heuristics
- Prefer phishing-resistant MFA and passkeys with strong enrollment ceremonies over push/SMS/TOTP flows that can be relayed in real time.
- Require step-up verification and alerting for new MFA-device registration, especially after high-risk sign-ins or help-desk initiated changes.
- Train help desks and employees that passkey or MFA migration should never be driven by ad hoc calls to personal phones.
- Monitor SaaS access at the API and direct-resource level; do not rely only on explicit download events.
- Preserve identity-provider, M365, Okta, SaaS, endpoint, and help-desk telemetry together during response, because the intrusion path crosses identity, browser sessions, and cloud data stores.
- When BlackFile-style extortion arrives, assume SaaS/identity compromise until ruled out and prioritize token revocation, MFA-device review, session invalidation, and cloud-data access scoping before broad credential rotation.

## Related pages
- [0ktapus phishing campaign](0ktapus-phishing-campaign.md)
- [Cloudflare Okta token theft incident](cloudflare-okta-token-theft-incident.md)
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- [Google Cloud / GTIG](https://cloud.google.com/blog/topics/threat-intelligence/blackfile-vishing-extortion-operation)
