# ShinyHunters Salesforce OAuth abuse

## Summary

Microsoft's July 13, 2026 report describes ShinyHunters-associated SaaS intrusion activity observed between mid-2025 and mid-2026 across Salesforce customer environments. Microsoft did not frame the activity as a Salesforce vulnerability; the durable defender point is that the actor abused trusted OAuth relationships, third-party SaaS integrations, and misconfigured guest access to query and exfiltrate CRM data while blending into legitimate API workflows.

Microsoft grouped the activity into three intrusion paths: vishing users into approving attacker-controlled Salesforce connected apps, abusing compromised credentials or connection secrets from trusted integrations such as Salesloft Drift, Gainsight-published applications, and Klue, and exploiting overly permissive Salesforce Experience Cloud guest-user access through Aura / GraphQL request chains.

## Tags

- ops
- ShinyHunters
- SaaS
- Salesforce
- OAuth
- connected apps
- non-human identity
- vishing
- supply chain
- Salesloft Drift
- Gainsight
- Klue
- Storm-3138
- CRM data theft
- guest access
- Aura framework
- GraphQL
- data exfiltration
- Microsoft

## Why this matters

- The access path is identity and application-trust abuse, not malware. A compromised or malicious OAuth app can inherit user/application privileges and call APIs in ways that do not look like suspicious sign-ins.
- Microsoft observed activity across retail, education, manufacturing, and other tenants, with abuse leading to persistent access and large-scale CRM record extraction.
- Trusted SaaS integrations become a blast-radius multiplier: connection secrets or OAuth tokens held by a vendor or integration can give an attacker access into multiple downstream customer Salesforce instances.
- Guest-user misconfiguration can expose data without an authenticated user session when Aura / GraphQL functionality is reachable with overly broad object or field permissions.

## Intrusion paths

### Vishing-driven OAuth consent abuse

Beginning in mid-2025, actors impersonated IT support and guided employees through Salesforce OAuth consent flows. In confirmed cases, victims authorized an attacker-controlled connected app disguised as a legitimate Salesforce Data Loader tool.

After consent, the app could make API calls as the victim user, enabling:

- enumeration of Salesforce instances belonging to targeted organizations;
- persistent access to Salesforce CRM data;
- possible lateral movement into other SaaS environments if discovered records or credentials supported it;
- exfiltration through sanctioned application access rather than credential replay or endpoint malware.

### Trusted-integration and SaaS supply-chain abuse

Microsoft says the actor also used trusted workflow/integration paths that already had Salesforce access:

- In August 2025, compromised Salesloft Drift credentials let attackers obtain connection secrets used by downstream SaaS applications and use OAuth tokens across multiple customer Salesforce instances.
- In November 2025, a campaign targeted Gainsight-published applications integrated with Salesforce, allowing persistent API access through trusted external connections.
- In June 2026, Klue disclosed an incident in which Storm-3138 accessed Klue systems; Microsoft says credentials used to access Salesforce customer instances were then used to discover, query, and exfiltrate data.

The important detection lesson is that these flows can look like normal integration behavior: API queries, report access, and bulk CRM object reads from a known connected application.

### Guest access and Aura / GraphQL exfiltration

Microsoft observed suspicious guest-user activity against Salesforce Aura endpoints across multiple organizations. The activity used unauthenticated access to Aura framework functionality and chained GraphQL-based Aura requests to query and retrieve data.

Microsoft states this was not exploitation of a Salesforce software vulnerability. The exposure came from misconfigured guest-user permissions that allowed actors to retrieve more data than a guest should be able to access.

## Reported indicators

| Type | Value | Notes |
| --- | --- | --- |
| IP address | `138.226.246.94` | Used by the Klue integration to call Salesforce API and perform CRM queries on 2026-06-11; previously disclosed by Klue according to Microsoft. |
| IP address | `212.86.125.24` | Used to target Aura framework guest access from 2026-06-19 to 2026-06-22. |
| IP address | `213.111.148.90` | Used to target Aura framework guest access from 2026-06-19 to 2026-06-22. |
| IP address | `94.154.32.160` | Used to target Aura framework guest access from 2026-06-19 to 2026-06-22. |
| IP address | `103.75.11.78` | Used to target Aura framework guest access from 2026-06-19 to 2026-06-22. |
| IP address | `103.75.11.110` | Used to target Aura framework guest access from 2026-06-19 to 2026-06-22. |

## Defender heuristics

- Inventory Salesforce connected apps and external client apps. Prioritize apps with high-risk OAuth scopes, administrative access, broad object permissions, or no recent legitimate use.
- Treat new or rarely used connected-app API activity from unusual IPs, new endpoints, or uncommon user/app pairings as a high-severity data-access event.
- Hunt for Salesforce `ApiTotalUsage`, `API Event`, `ReportExport`, and object-query activity tied to connected apps, especially when the activity is API-heavy, report-heavy, or associated with user/app/IP combinations uncommon for the tenant.
- Review OAuth consent events and connected-app creation/authorization after helpdesk calls, support chats, or suspicious vishing reports. A fake Data Loader-style app should be treated as possible SaaS compromise.
- Validate third-party SaaS integrations with Salesforce. Rotate and revoke OAuth tokens or connection secrets after vendor incidents, not only after direct tenant sign-in anomalies.
- Enable and retain Salesforce Shield Event Monitoring / Real-Time Event Monitoring or equivalent telemetry. Traditional authentication logs are not enough when the actor operates through approved integrations.
- Lock down Salesforce Experience Cloud guest users: remove unnecessary object and field permissions, validate sharing rules, and test that Aura / GraphQL endpoints cannot retrieve sensitive CRM records unauthenticated.
- Alert on guest-user Aura activity, anomalous guest-user data access, and GraphQL/Aura request chains from infrastructure Microsoft identified or from ASN/geography patterns that do not match expected customers.
- For confirmed exposure, scope all records queried or exported by the connected app, integration, guest user, and associated user identities before revoking access so legal/privacy notification decisions are evidence-based.

## MITRE ATT&CK mapping

| Tactic | Technique | Notes |
| --- | --- | --- |
| Initial Access | T1566.004 Phishing: Voice Phishing | IT-support impersonation to drive OAuth consent. |
| Credential Access | T1528 Steal Application Access Token | Use of stolen OAuth tokens from trusted integrations such as Salesloft and Gainsight. |
| Persistence | T1671 Cloud Application Integration | Connected apps and integrations provide durable SaaS access. |
| Collection | T1213.004 Data from Information Repositories: CRM Software | Salesforce CRM records queried and exported. |
| Exfiltration | T1567 Exfiltration Over Web Service | Data Loader-style application and API access used for exfiltration. |

## Related pages

- [ShinyHunters](../actors/shinyhunters.md)
- [Oracle PeopleSoft CVE-2026-35273 ShinyHunters exploitation](oracle-peoplesoft-cve-2026-35273-shinyhunters.md)
- [Klue Salesforce OAuth token abuse](klue-salesforce-oauth-token-abuse.md)
- [GitHub API enumeration and access-token abuse](../patterns/github-api-enumeration-token-abuse.md)

## Sources

- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/07/13/defending-saas-based-applications-against-shinyhunters-oauth-abuse/
