# Klue Salesforce OAuth token abuse

## Summary
In June 2026, Klue disclosed that an attacker used a compromised legacy credential tied to an integration service to access Klue integration infrastructure, obtain customer OAuth tokens, and access data in connected third-party platforms including Salesforce. Huntress, one impacted customer, said the actor pushed code capable of collecting OAuth tokens that Klue customers used to connect Klue to their own systems, then used those tokens to query customer CRM data directly.

Salesforce disabled the Klue Battlecards app integration while the incident was investigated and emphasized that the issue was limited to Klue's app connection, not a Salesforce platform vulnerability. Treat this as a durable SaaS supply-chain lesson: a vendor integration token can become a cross-tenant data-access path even when the customer's own SaaS tenant and the SaaS provider platform are not directly exploited.

## Tags
- ops
- operations
- SaaS
- Salesforce
- Klue
- OAuth
- OAuth tokens
- third-party integrations
- vendor compromise
- supply-chain
- stale credentials
- CRM data theft
- extortion
- incident response

## Why this matters
- SaaS integrations often hold long-lived OAuth grants with broad read access to CRM, sales, support, collaboration, and document systems.
- A single vendor-side credential can become a token-theft foothold across many connected customer environments.
- Disabling or revoking the vendor's app connection may be necessary even when there is no vulnerability in the underlying SaaS platform.
- Customer exposure can include business contacts, quotes, messages, sales records, and other data reachable through the integration's delegated permissions.
- The incident reinforces that vendor offboarding, abandoned integration prototypes, and service credentials need the same lifecycle controls as production identities.

## Reported chain
1. Klue said it detected unauthorized activity affecting part of its integration infrastructure on June 12, 2026.
2. Klue's investigation found that the attacker gained access through a compromised legacy credential associated with an integration service.
3. The attacker used that access to obtain OAuth tokens used to connect Klue to third-party platforms, including Salesforce.
4. Huntress said Klue's compromise began on June 11 when anomalous behavior occurred in a system that connects to multiple integrations. The actor reportedly pushed a code update capable of collecting customer OAuth tokens.
5. Huntress said the actor then pivoted through Klue infrastructure, stole tokens used by Klue customers, queried customer CRM tools directly, and exfiltrated data.
6. Klue revoked affected credentials and tokens, removed unauthorized code, disabled potentially impacted integrations, launched an investigation, and notified law enforcement.
7. Salesforce disabled the Klue Battlecards app integration, preventing organizations from connecting to Salesforce through the app until further notice.
8. Huntress reported extortion emails with the subject `top secret email` beginning June 16, 2026, after Salesforce data tied to Huntress was copied.

## Scope and caveats
- Klue said the incident affected Klue, customers, and integration partners, and that attackers subsequently accessed data in a number of connected customer environments.
- Klue said there was no evidence, as of its public update, that customer content stored within the Klue platform was impacted.
- Huntress said copied data from its Salesforce account included business contacts, price quotes, and other sales-related data and messaging. Huntress said threat data, passwords, payment-card information, engineering data, Huntress-agent data, and telemetry were not affected.
- Salesforce said the unusual activity may have resulted in unauthorized access to a subset of customer data through the app's Salesforce connection and did not arise from a Salesforce platform vulnerability.
- The Hacker News reported that an extortion group using the name `Icarus` claimed involvement, but public reporting available during this scan provides limited durable actor history. Keep actor attribution caveated until stronger primary reporting emerges.

## Defender heuristics
### Immediate triage
- Inventory SaaS applications connected to Klue, especially Salesforce, HubSpot, SharePoint, Zoom, Slack, Google Workspace, Microsoft 365, and other integrations exposed through Klue support communications or tenant audit logs.
- Revoke and re-consent Klue OAuth grants only after confirming Klue and the downstream SaaS provider have restored trusted integration paths.
- Search Salesforce setup and Event Monitoring logs for access by Klue-connected OAuth clients around and after June 11, 2026.
- Review CRM export, report, API, bulk query, and unusual object-access events associated with Klue app users, connected-app identities, and integration IP ranges.
- Preserve audit logs before revocation or app disablement removes useful context.

### Token and integration controls
- Require least-privilege OAuth scopes for vendor apps; avoid broad CRM read access when the workflow only needs a narrow object set.
- Prefer short-lived tokens, refresh-token rotation, app-specific conditional access, and explicit publisher verification for SaaS integrations.
- Monitor connected-app changes, new callback URLs, unusual refresh-token use, and sudden API spikes by integration clients.
- Maintain a vendor-integration inventory with owner, business justification, approved scopes, last use, data classes reachable, and revocation playbook.
- Remove abandoned prototype integrations and legacy service credentials during vendor and employee offboarding.

### Incident response
- Treat confirmed malicious OAuth-token use as SaaS tenant compromise for the reachable data plane.
- Rotate or revoke any downstream credentials, API tokens, session exports, or business-process secrets exposed through copied CRM records.
- Review extortion emails for recipient targeting and evidence of copied data, but avoid clicking links or replying outside approved legal/IR channels.
- Notify affected business owners whose accounts, contacts, quotes, or sales messages were exposed.
- After containment, compare vendor-app permissions against actual business need and add detections for future delegated-token abuse.

## Related pages
- [Cloudflare / Okta support-system compromise](cloudflare-okta-token-theft-incident.md)
- [BlackFile / UNC6671 vishing extortion operation](blackfile-unc6671-vishing-extortion.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [UNC3753 law-firm vishing extortion campaign](../actors/unc3753.md)

## Sources
- Klue: https://klue.com/blog/an-update-on-recent-klue-security-incident
- Huntress: https://www.huntress.com/blog/klue-breach-investigation
- Salesforce Trust status message: https://status.salesforce.com/generalmessages/20000257
- The Hacker News: https://thehackernews.com/2026/06/salesforce-disables-klue-app.html
