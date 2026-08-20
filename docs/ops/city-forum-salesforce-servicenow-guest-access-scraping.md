# City Forum: single-IP Salesforce and ServiceNow guest-access scraping

## Summary
Reco (agent-security platform) named a long-running scraping operation the **City Forum campaign**: a single server, **158.220.87.79** on a Contabo VPS, has been pulling records from **both Salesforce and ServiceNow customer portals since at least March 2025**. Every request carries the default Go `net/http` user agent, indicating a compiled, purpose-built tool rather than a browser. The campaign spans telecoms, banks and other financial services, enterprise software vendors (including security and data-privacy companies), and public-sector portals. The unifying root cause is a **guest identity granted more access than the site needed to serve the public**: on Salesforce, the Experience Cloud guest profile can read objects that are then reachable via the Aura framework *and* the newer Lightning Web Runtime (LWR) UI-API; on ServiceNow, the persistent Service Portal guest user reaches the anonymous `POST /api/now/sp/search` endpoint. Reco has not attributed the campaign to a named group; it is distinguished from the widely reported ShinyHunters Salesforce abuse mainly by the *range* of surfaces it touches.

## Tags
- ops
- operations
- City Forum
- Salesforce
- ServiceNow
- guest access abuse
- SaaS exposure
- Aura
- Lightning Web Runtime
- UI-API
- Service Portal
- data scraping
- Experience Cloud
- ShinyHunters-adjacent
- Reco
- Go net/http user agent
- 158.220.87.79

## Why this matters
- **One misconfigured guest profile, two platforms, two years of access.** The campaign shows that guest-access hygiene is the control, not endpoint-level blocking: both the Salesforce UI-API and the ServiceNow search endpoint are working as designed and simply return what the guest can read.
- **The newer surface has no public tooling or write-ups yet.** Aura guest abuse is well documented; the same tool also walks the Lightning Web Runtime UI-API sequentially across API versions **v56.0 → v66.0**, a data layer Reco says has no public scanning tools. Defenders should not treat "we aren't on Aura" as coverage.
- **Volume scale:** one target logged over **560,000 Aura events** from the same IP; the infrastructure is still active and climbing.
- **Differentiator from ShinyHunters:** that operation leaned on high-volume Aura guest enumeration; City Forum combines Aura bulk paging *plus* LWR UI-API traversal *plus* a third, almost-undocumented endpoint (ServiceNow `sp/search`).

## Reported technique
1. A single Go binary (default `Go-http-client` user agent on every request) sends high-volume guest requests.
2. **Salesforce:** Aura guest requests enumerate objects and page through records (bulk of traffic), plus LWR UI-API calls across API versions v56.0–v66.0 on Experience Cloud sites.
3. **ServiceNow:** repeated `POST /api/now/sp/search` against native Service Portal search, harvesting what the portal's guest-facing search criteria return.
4. Passive DNS ties the `City Forum` domain to 158.220.87.79 back to at least **March 2025**; the server has not moved since.

## Detection
### Salesforce (Event Monitoring / Shield)
- Pull `AuraRequest` and `Sites` log events; look for:
  - the Go `net/http` default user agent,
  - source IP **158.220.87.79** (or your own equivalents of single-source, high-volume guest traffic),
  - request paths containing `/webruntime/api/services/data`,
  - spikes in self-registration attempts at `/SiteRegister` and `/CommunitiesSelfReg`.
### ServiceNow
- Filter `syslog_transaction` by source IP and URLs beginning with `/api/now/sp/search`.
- The clearest live-sweep signals: guest-created rows and unusual output length in search responses.

## Remediation
- **Salesforce:** review guest sharing rules; strip object/field-level access the guest does not need; disable self-registration where not required; turn off the Experience Builder setting that lets guest users reach public APIs.
- **ServiceNow:** map which search sources are exposed on public-facing portals; audit the Knowledge Base read criteria that determine what anonymous search returns.
- Both fixes target the **guest profile**, not the endpoints — the endpoints are behaving correctly relative to their configuration.

## Confidence and attribution
- Reco has not attributed the campaign to a named group; treat "City Forum" as Reco's operational label (from a domain tied to the attacker IP).
- Victim organizations are not named; sector scope is as above.
- The activity is ongoing per Reco at publication; indicator freshness should be re-checked.

## Related pages
- [ShinyHunters Salesforce OAuth abuse](shinyhunters-salesforce-oauth-abuse.md)
- [ServiceNow instance unauthenticated table-query exploitation](servicenow-instance-unauthenticated-table-query-exploitation.md)
- [ServiceNow AI Platform CVE-2026-6875 exploitation](servicenow-ai-platform-cve-2026-6875-exploitation.md)

## Sources
- Reco: [City Forum campaign — Salesforce and ServiceNow guest-access scraping](https://www.reco.ai/blog/city-forum-campaign-salesforce-servicenow)
- The Hacker News: [One Attacker Has Scraped Both Salesforce and ServiceNow Portals Since 2025](https://thehackernews.com/2026/08/one-attacker-has-scraped-both.html) — August 18, 2026
