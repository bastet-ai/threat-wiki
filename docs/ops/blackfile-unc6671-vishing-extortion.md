# UNC6671 / BlackFile multi-brand vishing extortion operation

## Summary
Google Threat Intelligence Group reported **UNC6671** as an active extortion cluster that uses voice phishing, adversary-in-the-middle credential capture, and SSO / SaaS compromise rather than a product vulnerability. After the **BlackFile** brand announced its May 2026 retirement, GTIG linked continued UNC6671 activity to **REDACT**, **PINK**, **HELIX**, and **FALCON** extortion fronts. The cluster targets Microsoft 365 and Okta environments, persists through identity changes, exfiltrates data from SaaS platforms, and pressures victims through multiple data-leak and direct-extortion workflows.

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
- REDACT
- PINK
- HELIX
- FALCON
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

## August 2026 multi-brand follow-up
GTIG's August 6 follow-up found that UNC6671 did not stop when BlackFile announced its retirement in May. The cluster diversified across REDACT, PINK, HELIX, and FALCON while retaining the same help-desk vishing, AiTM panels, SaaS theft, and extortion baseline. Shared root domains, identical phishing templates, overlapping victim targeting, and intermediate victim-specific subdomains connect the brands. Examples include:

- `passkeyhelpdesk[.]com`, which targeted organizations later extorted under both FALCON and HELIX;
- `passkeydeploy[.]com`, linked through overlapping targeting to PINK and BlackFile infrastructure;
- `oskeysync[.]com` and `keysyncos[.]com`, associated with HELIX targeting;
- `portalpasskey[.]com`, `addssopasskey[.]com`, `mysecurepasskey[.]com`, `idokta[.]com`, and `passkeyuser[.]com`.

Target selection shifted from broad enterprise verticals in April and May toward technology, transportation, and hospitality in June, then financial services, private equity, legal, and professional services in July. GTIG measured a June-July provisioning cadence of roughly one domain every 1.6 days, including seven domains operationalized during July 20-22. Because seven of eight still-resolving phishing domains did not use wildcard DNS at publication, passive-DNS subdomains were likely deliberate targets rather than automatically valid names.

Recent intrusions added help-desk caller-ID spoofing and account-level defense evasion. Operators used compromised mailboxes to reset passwords for non-SSO applications, then deleted password-reset confirmations, security notifications, company-wide alerts, and messages generated by account-security changes. Hunts should therefore include deleted-message and recovery-setting activity, not only successful IdP authentication and bulk SaaS access.

GTIG reviewed 18 BlackFile Bitcoin addresses that received **141.65 BTC**, approximately **$10.69 million** at transaction time, from January 7 through May 12, 2026. Payments and cash-outs continued after the announced shutdown. Initial demands were commonly $1 million to more than $3 million; in over 53% of tracked cases, negotiated final payments averaged about $750,000. These figures describe the reviewed wallets and cases, not a complete UNC6671 revenue estimate.

GTIG assesses that one coordinated cluster operating multiple brands is the most likely explanation, but explicitly preserves alternatives: actor splintering, shared phishing/caller infrastructure, or outsourced extortion and negotiation. Brand overlap should not be treated as proof that every REDACT, PINK, HELIX, or FALCON claim is controlled by one operator.

## Indicators and hunt pivots
- Vishing reports involving passkey migration, SSO setup, or MFA enrollment calls to personal phones.
- New MFA device registrations immediately after suspicious interactive sign-ins.
- Password resets for non-SSO applications followed by deletion of confirmation, security-alert, or account-change messages from compromised mailboxes.
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
- Google Cloud / GTIG: [https://cloud.google.com/blog/topics/threat-intelligence/blackfile-vishing-extortion-operation](https://cloud.google.com/blog/topics/threat-intelligence/blackfile-vishing-extortion-operation)
- Google Cloud / GTIG: [https://cloud.google.com/blog/topics/threat-intelligence/unc6671-targets-financial-services-and-enterprise-cloud-environments/](https://cloud.google.com/blog/topics/threat-intelligence/unc6671-targets-financial-services-and-enterprise-cloud-environments/)
