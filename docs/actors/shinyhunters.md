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

### September 2026: post-betrayal extortion escalation — refuse-to-pay publication confirmed at state scale
- Google GTG's LABScon disclosure (Sep 18) had already established that ShinyHunters went rogue from its TeamPCP revenue-share arrangement ~mid-2026, extorting with TeamPCP's stolen credentials and leaking its own chat log to Google in the process; September's public incidents show the resulting operation's extortion-at-refusal pattern executing at scale:
- **Florida FLHSMV DAVID breach (disclosed Sep 4, records published ~Sep 16-17, 2026):** after the State of Florida declined to pay, the ShinyHunters extortion group published claimed **200,000+ records** from Florida's **Driver and Vehicle Information Database (DAVID)** — a law-enforcement/government system, not a public portal — to its dark-web leak site. FLHSMV attributed the intrusion to a **single Plant City Police Department user whose login had been improperly stored on a personal electronic device**; the state described the attacker only as an "international cybercriminal organization" and has not named ShinyHunters or confirmed the 200k figure. ShinyHunters separately told BleepingComputer it entered via a **password-reset flaw affecting multiple DAVID accounts, including DMV employees and an FBI agent** — an account Florida has not corroborated. TechCrunch's review of the leak: hundreds of thousands of vehicle-ownership certificates (names, addresses, VINs) plus a smaller set with SSNs and government documents including non-U.S. passports/immigration papers; no driver's-license photos apparent. Earlier proof-of-access included a record tied to the late Jeffrey Epstein. Defender read: **a single poorly-stored law-enforcement credential on a personal device reached a statewide LE query system** — inventory and vault-store shared/government logins on out-of-policy devices, and treat password-reset flows on LE systems as Tier-1 attack surface (TechCrunch Sep 16, SOFX Sep 17, 2026).
- **McKesson (August disclosure, Sep 10-19 scope updates):** ShinyHunters claimed theft from the medical-supply giant (claims of up to **284 million patient records**); McKesson confirmed a **third-party-application-mediated** cyberattack, and The Register / HIPAA Journal reported **6.4 million unique email addresses** in exposed data as of Sep 19 — the SaaS/third-party-app OAuth abuse lane already documented on this page, now with healthcare-scale victim numbers.
- Keep sourcing narrow per page policy: FLHSMV has not named ShinyHunters; the FBI-account entry claim is a single one-party account; the McKesson record counts are attacker-claimed pending company validation.

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
- Microsoft Security Blog: [https://www.microsoft.com/en-us/security/blog/2026/07/13/defending-saas-based-applications-against-shinyhunters-oauth-abuse/](https://www.microsoft.com/en-us/security/blog/2026/07/13/defending-saas-based-applications-against-shinyhunters-oauth-abuse/)
- Google Cloud / Mandiant: [https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-targets-education-sector-oracle-exploit/](https://cloud.google.com/blog/topics/threat-intelligence/shinyhunters-targets-education-sector-oracle-exploit/)
- Oracle security alert for CVE-2026-35273: [https://www.oracle.com/security-alerts/alert-cve-2026-35273.html](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html)
- TechCrunch — "Hackers publish thousands of drivers' data after breaching Florida motor vehicle database" (Sep 16, 2026): [https://techcrunch.com/2026/09/16/hackers-publish-thousands-of-drivers-data-after-breaching-florida-motor-vehicle-database/](https://techcrunch.com/2026/09/16/hackers-publish-thousands-of-drivers-data-after-breaching-florida-motor-vehicle-database/)
- SOFX — "Hackers Dump Florida Driver Records Stolen Through a Police Login" (Sep 17, 2026, summarizes FLHSMV statement + BleepingComputer ShinyHunters claims): [https://www.sofx.com/hackers-dump-florida-driver-records-stolen-through-a-police-login/](https://www.sofx.com/hackers-dump-florida-driver-records-stolen-through-a-police-login/)
- The Register — "ShinyHunters expose 6.4M in attack on medical supplier McKesson" (Sep 10, 2026, headline confirmed via Google News aggregation, article URL not independently verified). Scope update: The HIPAA Journal, "McKesson Cyberattack: Stolen Data Includes 6.4 Million Unique Email Addresses" (Sep 19, 2026, also via Google News aggregation).
