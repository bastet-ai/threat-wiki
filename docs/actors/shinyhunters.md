# ShinyHunters

## Summary
**ShinyHunters** is a public extortion and data-theft persona tracked by Google Mandiant / GTIG as **UNC6240** in the June 2026 Oracle PeopleSoft campaign. Mandiant reported that UNC6240 exploited Oracle PeopleSoft **CVE-2026-35273** as a zero-day against PeopleSoft application infrastructure, with stolen organization data later published on the ShinyHunters data-leak site.

This page is intentionally narrow: it records durable, sourced operational facts for threat.wiki and should not be used to merge unrelated public ShinyHunters ecosystem claims without additional primary sourcing.

## Tags
- group
- actor
- ShinyHunters
- UNC6240
- OAuth abuse
- SaaS
- Salesforce
- connected apps
- vishing
- extortion
- data theft
- data leak site
- Oracle PeopleSoft
- CVE-2026-35273
- higher education
- MeshCentral

## Known activity

### 2025-2026 Salesforce OAuth and trusted-integration abuse
- Microsoft reported ShinyHunters-associated SaaS intrusion activity observed between mid-2025 and mid-2026 against Salesforce customer environments.
- Microsoft grouped the activity into three trust-abuse paths: vishing users into consenting to attacker-controlled Salesforce connected apps, abusing trusted SaaS integrations and OAuth tokens from Salesloft Drift / Gainsight / Klue-style workflows, and using misconfigured Salesforce Experience Cloud guest access through Aura / GraphQL requests.
- Microsoft explicitly framed the activity as abuse of OAuth relationships, integrations, and guest-user permissions rather than a Salesforce product vulnerability.
- The impact pattern is CRM enumeration, bulk data querying, and exfiltration through legitimate-looking API and connected-app activity that may evade authentication-centric detections.

### 2026 Oracle PeopleSoft zero-day exploitation
- Google Mandiant and GTIG attribute an Oracle PeopleSoft exploitation and extortion campaign to **UNC6240 (ShinyHunters)**.
- Activity was observed from 2026-05-27 through 2026-06-09 and aligned with exploitation of **CVE-2026-35273**, a critical unauthenticated PeopleSoft PeopleTools remote-code-execution vulnerability.
- Mandiant reported that the actor targeted Environment Management Hub (`PSEMHUB`) endpoints and used staging servers with customized MeshCentral agents, command histories, and a victim-specific fanout script.
- GTIG notified more than 100 organizations whose IP addresses correlated with potentially vulnerable endpoints; 68% were higher-education institutions.
- Mandiant tied the campaign to stolen organization data published on the ShinyHunters data-leak site on 2026-06-09.

## Defender focus
- Treat ShinyHunters / UNC6240 reporting as extortion-driven intrusion activity, not just credential resale or leak-site branding.
- For Salesforce and adjacent SaaS environments, inventory connected apps, review OAuth scopes, revoke stale or unneeded integrations, monitor API-heavy connected-app behavior, and validate Experience Cloud guest-user permissions.
- For PeopleSoft environments, prioritize the operational page's endpoint restrictions, WebLogic log review, PSEMHUB filesystem inspection, and outbound SMB monitoring.
- Preserve staging, web-tier, process-scheduler, and outbound network evidence before removing web shells or remote-management agents.

## Related pages
- [ShinyHunters Salesforce OAuth abuse](../ops/shinyhunters-salesforce-oauth-abuse.md)
- [Oracle PeopleSoft CVE-2026-35273 ShinyHunters exploitation](../ops/oracle-peoplesoft-cve-2026-35273-shinyhunters.md)
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md)

## Sources
- [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/13/defending-saas-based-applications-against-shinyhunters-oauth-abuse/)
- [Google Cloud / Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-targets-education-sector-oracle-exploit/)
- [Oracle security alert for CVE-2026-35273](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html)
