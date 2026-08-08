# Metabase unauthenticated SQL-injection zero-day

## Summary
On August 8, 2026, Metabase disclosed active exploitation of a previously unknown vulnerability in self-hosted and cloud releases **1.58 / 0.58 and later**. The flaw, tracked as **GHSA-vwf4-m7j8-wcjf** but not yet assigned a CVE, lets an unauthenticated remote attacker inject SQL into the Metabase application database through the password-reset API. Successful exploitation can produce Metabase administrator access and expose connected-database credentials and all data those connections can read.

Metabase says it detected the zero-day in an attack against Metabase Cloud, blocked the abused endpoints, and patched its hosted service. Self-hosted operators must upgrade to a fixed point release. Blocking `/api/session/reset_password` is only a temporary workaround; an exposed vulnerable instance should also be investigated for compromise.

## Tags
- ops
- operations
- active exploitation
- zero-day
- Metabase
- business intelligence
- data analytics
- GHSA-vwf4-m7j8-wcjf
- SQL injection
- authentication bypass
- unauthenticated admin access
- credential theft
- data theft
- application database
- /api/session/reset_password
- incident response

## What is confirmed
- Metabase says an attacker used an unknown zero-day against Metabase Cloud and that the company patched the hosted service after identifying the vulnerability.
- The GitHub advisory rates the issue **Critical, CVSS 10.0** and confirms active exploitation.
- The vulnerable endpoint is `/api/session/reset_password`. The vendor says the observed compromise pattern is a `POST` to that path returning HTTP `400`, followed by `GET /api/user/current` returning HTTP `200`.
- The SQL injection targets the **Metabase application database**. Administrator access obtained through that path can be used to change application configuration, retrieve stored credentials for connected databases, query data available through those connections, and export data.
- Releases before the 0.58 / 1.58 line are not affected according to Metabase. Cloud customers have already been patched; self-hosted customers need to upgrade.
- Metabase has not publicly identified the operator, initial target set, exploit request body, source infrastructure, or complete victim scope.

## Fixed-version matrix
Metabase lists the following as the minimum safe point releases for supported branches:

| Branch | Minimum safe release |
| --- | --- |
| 0.58 / 1.58 | `0.58.24` / `1.58.24` |
| 0.59 / 1.59 | `0.59.21` / `1.59.21` |
| 0.60 / 1.60 | `0.60.17` / `1.60.17` |
| 0.61 / 1.61 | `0.61.11` / `1.61.11` |
| 0.62 / 1.62 | `0.62.9` / `1.62.9` |
| 0.63 / 1.63 | `0.63.5` / `1.63.5` |

Use the vendor advisory and release channel as the source of truth for later branches. Verify the running version after deployment rather than relying only on an image tag or rollout status.

## Detection and scoping
1. Search Metabase application, ingress, reverse-proxy, WAF, and load-balancer logs for `POST /api/session/reset_password`, especially HTTP `400` responses followed from the same source or session by a successful `GET /api/user/current`.
2. Treat the vendor's two-request sequence as a high-confidence compromise lead, not the only possible exploit signature. Preserve request bodies, headers, source addresses, timestamps, and upstream proxy context before cleanup.
3. Review administrator-account creation and changes, API-key creation, permission and group changes, authentication settings, application configuration, exports, downloads, subscriptions, and unusual query activity.
4. Review the Metabase application database for unexpected changes to users, sessions, API keys, permissions, database connections, and configuration. Preserve a forensic copy before deleting records.
5. Correlate Metabase query history with connected data-warehouse and database audit logs. Look for unusual schemas, bulk reads, exports, credential tests, and access outside normal user or service-account patterns.
6. Inventory every credential stored in or reachable from Metabase, including database passwords, cloud warehouse keys, SSH tunnel material, API credentials, and secrets used by plugins or integrations.
7. Scope downstream data according to what each configured Metabase connection could read. Administrator access to Metabase is not automatically database-server administrator access, but it can expose broad application-level query authority and stored credentials.

## Response guidance
1. **Upgrade immediately** to the fixed point release for the deployed branch. Metabase Cloud customers are already patched; self-hosted deployments require operator action.
2. If an immediate upgrade is impossible, block `/api/session/reset_password` at the reverse proxy, WAF, or ingress. Keep the service inaccessible from untrusted networks until patching and initial scoping are complete.
3. After upgrading, revoke all Metabase user sessions. Metabase specifically directs operators to delete all rows from the application database's `core_session` table; preserve evidence first when compromise is suspected.
4. Remove unrecognized API keys and administrator accounts, and reverse unauthorized permission or configuration changes.
5. Rotate credentials for every connected database and other secret reachable from the instance after containment. Review downstream logs before rotation so the old credential identifiers can be used for scoping.
6. Review Metabase activity, query history, exports, and the connected data stores for unauthorized access. Do not treat patching or a clean administrator list as proof that no data was read.
7. Rebuild from a known-good deployment and restore reviewed configuration if application-database integrity cannot be established.

## Attribution and scope caveats
The public record confirms exploitation but does not identify an actor or quantify affected self-hosted instances. A vulnerable internet-reachable deployment is exposure, not proof of compromise. Conversely, absence of the exact published request sequence does not rule compromise out because attackers can change request flow or logs can be incomplete.

The vulnerability directly affects Metabase's application database and authorization state. Claims about theft from a connected database should be tied to Metabase query history, database audit logs, exports, or another victim-side artifact rather than inferred solely from successful exploitation.

## Related pages
- [ServiceNow hosted-instance table-query exploitation](servicenow-instance-unauthenticated-table-query-exploitation.md)
- [CosmosEscape Azure Cosmos DB cross-tenant takeover](cosmosescape-azure-cosmos-db-cross-tenant-takeover.md)
- [Progress Kemp LoadMaster CVE-2026-8037 pre-auth RCE](progress-kemp-loadmaster-cve-2026-8037-preauth-rce.md)

## Sources
- Metabase, “Security update available for Metabase — Please upgrade now,” 2026-08-08: [https://www.metabase.com/blog/security-update](https://www.metabase.com/blog/security-update)
- GitHub Security Advisory, GHSA-vwf4-m7j8-wcjf, “SQL injection using an unauthenticated endpoint leading to admin access,” 2026-08-08: [https://github.com/metabase/metabase/security/advisories/GHSA-vwf4-m7j8-wcjf](https://github.com/metabase/metabase/security/advisories/GHSA-vwf4-m7j8-wcjf)
