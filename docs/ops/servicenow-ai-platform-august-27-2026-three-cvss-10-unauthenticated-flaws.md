# ServiceNow AI Platform August 27, 2026 advisory: three CVSS 10.0 unauthenticated flaws and a sandbox escape (CVE-2026-18885 / CVE-2026-18886 / CVE-2026-74820 / CVE-2026-6876)

## Summary
ServiceNow's **August 27, 2026** security advisory addresses **four** flaws in the **ServiceNow AI Platform / Now Platform**, three rated **CVSS 10.0** and exploitable in certain circumstances by an **unauthenticated** attacker. ServiceNow deployed the update to **hosted instances** and provided it to partners and self-hosted customers (who must apply it themselves). The batch follows the July 2026 pre-authentication sandbox escape **CVE-2026-6875** and the June 2026 hosted-instance unauthenticated table-query incident.

| CVE | CVSS 4.0 | Class |
|---|---|---|
| **CVE-2026-18885** | 10.0 | code injection in the **GraphQL Composite Data API** — unauthenticated arbitrary code execution / instance-data access and modification |
| **CVE-2026-18886** | 10.0 | improper access control in the **system configuration image upload processor** — unauthenticated create/modify of instance data → privilege escalation |
| **CVE-2026-74820** | 10.0 | **SQL injection** reachable through a dynamic-schema `ORDER BY` clause — unauthenticated arbitrary SQL against the underlying database |
| **CVE-2026-6876** | 8.7 | **sandbox escape** in the Now Platform — unauthenticated arbitrary code execution |

The three 10.0 flaws share the vector `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H`: network-reachable, low complexity, **no privileges, no user interaction**, high impact across the component and connected systems.

## Tags
- ops
- operations
- ServiceNow
- ServiceNow AI Platform
- Now Platform
- CVSS 10.0
- unauthenticated
- code injection
- GraphQL Composite Data API
- SQL injection
- improper access control
- sandbox escape
- CVE-2026-18885
- CVE-2026-18886
- CVE-2026-74820
- CVE-2026-6876
- enterprise application
- SaaS

## Why this matters
- Three **unauthenticated, network-reachable** 10.0-rated flaws in a high-value enterprise control plane (workflow, CMDB, ticketing, identity, integrations, automation) make any unpatched self-hosted instance an immediate patch target.
- ServiceNow is the CVE Numbering Authority for its products; the 10.0 ratings are **ServiceNow's own** — as of **August 28, 2026**, none of the four appeared in CISA's KEV catalog, so these ratings are the only severity assessment on record (NIST has enriched only KEV-listed / federal / EO-14028-critical CVEs since April 15, 2026).
- This is a rapid repeat of the July sandbox-escape pattern: **CVE-2026-6875** (pre-auth sandbox escape, publicly reported exploited in July after Defused flagged activity that ServiceNow later attributed to Searchlight Cyber's public PoC) is followed here by another sandbox escape (**CVE-2026-6876**) plus a broader set of unauthenticated primitives.

## Affected releases (ServiceNow August advisory)
- **Xanadu** — any version before Patch 11 Hot Fix 7a
- **Yokohama** — before Patch 12 Hot Fix 3, and before Patch 13 Hot Fix 4
- **Zurich** — before Patch 7b Hot Fix 3, Patch 8 Hot Fix 5, Patch 9 Hot Fix 6, Patch 10 Hot Fix 2m (m-branch), Patch 10 Hot Fix 3 (standard), Patch 11, or Patch 12
- **Australia** — before Patch 2 Hot Fix 3, Patch 3 Hot Fix 2, Patch 3m, Patch 4, or Patch 5

Notes on the affected-version records:
- **CVE-2026-18886** marks "any version before Australia Patch 5" with status **unknown**, whereas the other three mark it **affected**.
- All four default to **unaffected** status, so a release not named in the list falls outside the affected set.
- **CVE-2026-6876** is described as allowing an **unauthenticated** user to execute arbitrary code, yet ServiceNow's CVSS vector specifies **`PR:L`** (low privileges required) — an internal inconsistency in the vendor's own record.

## Relation to the July CVE-2026-6875 exploitation
The advisory follows **CVE-2026-6875**, a pre-authentication sandbox escape in the same platform reported by Searchlight Cyber on **April 1, 2026** and published by ServiceNow on **July 13, 2026**. Days later, **Defused** reported in-the-wild exploitation of CVE-2026-6875, then issued a correction stating the captured payload matched Searchlight Cyber's published PoC. A ServiceNow spokesperson said they "have not observed evidence that this activity is related to instances that ServiceNow hosts" and urged self-hosted and hosted customers to apply patches. ServiceNow rated CVE-2026-6875 at **9.5** under the same scoring version — every metric identical to the three 10.0 flaws **except attack complexity, which it set to high**.

## Detection and response
1. **Confirm your release against the affected-version list above** and apply the vendor patch immediately (self-hosted: apply now; hosted: confirm the update has been deployed by ServiceNow).
2. Restrict internet access to AI execution and administrative surfaces where business requirements permit; enforce identity-aware access and network allow-listing.
3. Review reverse-proxy, WAF, and platform telemetry for **unauthenticated** requests to the GraphQL Composite Data API, configuration-image upload paths, and dynamic-schema query endpoints, followed by code execution, SQL execution, child-process creation, or instance-data modification.
4. Scope integration credentials, OAuth applications, MID servers, service accounts, and downstream automation reachable from the platform.
5. Preserve request, platform, audit, process, and network evidence before remediation; on credible exploitation, isolate affected components and rotate exposed credentials.
6. Keep this batch distinct from the July CVE-2026-6875 exploitation and the June table-query incident so patch validation and compromise windows are not conflated.

## Assessment limits
- No public **in-the-wild exploitation** has been reported for the four August CVEs as of this page's last update; none were in CISA KEV as of August 28, 2026.
- Severity ratings are **ServiceNow's own** (CNA for its products); NVD enrichment has not yet been applied.
- The CVE-2026-6876 "unauthenticated" description vs. `PR:L` vector is an internal inconsistency worth monitoring as the record is clarified.

## Related pages
- [ServiceNow AI Platform CVE-2026-6875 exploitation](servicenow-ai-platform-cve-2026-6875-exploitation.md)
- [ServiceNow instance unauthenticated table-query exploitation](servicenow-instance-unauthenticated-table-query-exploitation.md)
- [City Forum Salesforce/ServiceNow guest-access scraping](city-forum-salesforce-servicenow-guest-access-scraping.md)

## Sources
- The Hacker News: [Three CVSS 10.0 ServiceNow Flaws Could Let Unauthenticated Attackers Execute Code and SQL](https://thehackernews.com/2026/08/three-cvss-100-servicenow-flaws-could.html) (Aug 28, 2026)
- ServiceNow August 27, 2026 advisory (affected-version list and CVSS vectors as reported above)
- Prior context: [ServiceNow AI Platform CVE-2026-6875 exploitation](servicenow-ai-platform-cve-2026-6875-exploitation.md)
