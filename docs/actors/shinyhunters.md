# ShinyHunters

## Summary
**ShinyHunters** is a public extortion and data-theft persona tracked by Google Mandiant / GTIG as **UNC6240** in the June 2026 Oracle PeopleSoft campaign. Mandiant reported that UNC6240 exploited Oracle PeopleSoft **CVE-2026-35273** as a zero-day against PeopleSoft application infrastructure, with stolen organization data later published on the ShinyHunters data-leak site.

This page is intentionally narrow: it records durable, sourced operational facts for threat.wiki and should not be used to merge unrelated public ShinyHunters ecosystem claims without additional primary sourcing.

## Tags
- group
- actor
- ShinyHunters
- UNC6240
- extortion
- data theft
- data leak site
- Oracle PeopleSoft
- CVE-2026-35273
- higher education
- MeshCentral

## Known activity

### 2026 Oracle PeopleSoft zero-day exploitation
- Google Mandiant and GTIG attribute an Oracle PeopleSoft exploitation and extortion campaign to **UNC6240 (ShinyHunters)**.
- Activity was observed from 2026-05-27 through 2026-06-09 and aligned with exploitation of **CVE-2026-35273**, a critical unauthenticated PeopleSoft PeopleTools remote-code-execution vulnerability.
- Mandiant reported that the actor targeted Environment Management Hub (`PSEMHUB`) endpoints and used staging servers with customized MeshCentral agents, command histories, and a victim-specific fanout script.
- GTIG notified more than 100 organizations whose IP addresses correlated with potentially vulnerable endpoints; 68% were higher-education institutions.
- Mandiant tied the campaign to stolen organization data published on the ShinyHunters data-leak site on 2026-06-09.

## Defender focus
- Treat ShinyHunters / UNC6240 reporting as extortion-driven intrusion activity, not just credential resale or leak-site branding.
- For PeopleSoft environments, prioritize the operational page's endpoint restrictions, WebLogic log review, PSEMHUB filesystem inspection, and outbound SMB monitoring.
- Preserve staging, web-tier, process-scheduler, and outbound network evidence before removing web shells or remote-management agents.

## Related pages
- [Oracle PeopleSoft CVE-2026-35273 ShinyHunters exploitation](../ops/oracle-peoplesoft-cve-2026-35273-shinyhunters.md)
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md)

## Sources
- Google Cloud / Mandiant: https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-targets-education-sector-oracle-exploit/
- Oracle security alert for CVE-2026-35273: https://www.oracle.com/security-alerts/alert-cve-2026-35273.html
