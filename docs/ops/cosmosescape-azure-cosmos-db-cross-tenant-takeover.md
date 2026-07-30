# CosmosEscape Azure Cosmos DB cross-tenant takeover

## Summary
On 2026-07-30, Wiz Research disclosed **CosmosEscape**, a now-remediated Azure Cosmos DB vulnerability chain that crossed the service's tenant-isolation boundary through the Gremlin API. A malicious customer could escape the .NET-based Gremlin query sandbox on infrastructure serving its own database, execute code on a multi-tenant DB Gateway, obtain a platform-wide signing secret dubbed the **Cosmos Master Key**, enumerate Cosmos DB accounts, and retrieve any account's primary key for full database read and write access.

The chain reportedly worked across tenants, regions, and Cosmos DB API flavors, including SQL, MongoDB, Cassandra, and Gremlin. It also reached private and network-isolated accounts because the compromised DB Gateway was the component enforcing network restrictions. Microsoft deployed an entry-point hot fix within 48 hours of Wiz's 2025-11-20 report, eliminated the platform-wide key through a longer architectural migration completed across all regions in July 2026, and added authentication, network, monitoring, and detection guardrails.

Microsoft and Wiz say no customer action is required. Microsoft reported no unauthorized activity beyond Wiz's testing and no customer-data access. No CVE, public exploit, customer indicator, or evidence of in-the-wild exploitation was published with the disclosure.

## Tags
- ops
- operations
- CosmosEscape
- Azure Cosmos DB
- Microsoft Azure
- cloud security
- managed database
- multi-tenant cloud
- cross-tenant access
- tenant isolation
- sandbox escape
- Gremlin API
- .NET reflection
- remote code execution
- credential exposure
- primary keys
- network isolation bypass
- control plane
- responsible disclosure

## Reported vulnerability chain
1. The researcher created and queried its own Cosmos DB account through the public Gremlin API.
2. Cosmos DB translated Gremlin queries into .NET code. Restrictions around that code did not sufficiently constrain .NET reflection, enabling file read, file write, and ultimately command execution on the DB Gateway.
3. The DB Gateway ran on multi-tenant Service Fabric clusters and used account primary keys to reach customer databases.
4. Credentials available to the gateway exposed a signing key that could request a primary key for any Cosmos DB account. The key was not scoped to the initiating account, tenant, region, or API flavor.
5. The same platform-wide capability exposed the regional Config Store, a Cosmos DB-backed directory containing account names, subscription and tenant IDs, network configuration, tags, and other account metadata.
6. An attacker could query the Config Store to enumerate accounts or select a target by tenant or subscription ID, then use the platform-wide signing path to obtain that target's primary key.
7. A Cosmos DB primary key grants full read and write access to the account's databases. Because access originated through the trusted gateway, private-endpoint and network-isolation controls did not block the path.

Wiz said Microsoft services including Entra ID, Teams, and Copilot use Cosmos DB, so Microsoft-internal databases were potentially inside the vulnerable population. This describes technical reachability, not confirmed access or impact.

## Why this matters
- **A tenant-controlled query crossed into a shared privileged tier.** The gateway combined executable customer input, multi-tenant placement, service-wide credentials, account discovery, and data-plane access in one trust zone.
- **A platform key collapsed all narrower boundaries.** Per-account primary keys and API, region, subscription, tenant, and network boundaries did not protect databases once the service-wide signing path was exposed.
- **Private networking was not an independent isolation layer.** The component compromised by the query was also responsible for enforcing network policy and already had a trusted route to private databases.
- **Managed-service remediation is provider-led.** Customers could not patch the gateway or rotate the Cosmos Master Key. Provider investigation and architectural key elimination were the decisive controls.
- **Potential blast radius is not observed compromise.** The chain could theoretically reach every Cosmos DB account, but the public record says only researcher testing occurred. Defenders should not convert architectural exposure into an unsupported breach claim.

## Defender actions
1. **Record the provider's conclusion and preserve tenant evidence.** Retain Azure Activity Logs, Cosmos DB data-plane diagnostics, Entra sign-in and service-principal events, network-flow telemetry, and application audit records covering at least 2025-11-20 through the July 2026 architectural rollout, subject to local retention and legal requirements.
2. **Review for unexplained data-plane activity rather than an unpublished exploit signature.** Look for anomalous reads, writes, key use, account or collection enumeration, and application-visible data changes. The public disclosure does not provide a customer-side CosmosEscape IOC or query signature.
3. **Do not perform precautionary primary-key rotation without impact analysis.** Microsoft says no customer action is required. If independent evidence suggests key misuse, coordinate application failover and rotate keys through the normal two-key process so emergency rotation does not cause avoidable outages.
4. **Use identity-based access where supported.** Prefer Microsoft Entra identities, managed identities, narrow Cosmos DB data-plane roles, and short-lived authorization over distributing account primary keys to workloads. This does not remediate the historical provider flaw, but it reduces the ordinary blast radius of customer-managed secret exposure.
5. **Constrain applications even when the database is managed.** Separate sensitive datasets and workloads by account and identity where practical, validate writes at application boundaries, maintain tested backups, and detect high-volume or cross-workload access.
6. **Treat provider control planes as part of threat models.** Private endpoints, firewalls, and public-network disablement remain useful, but document that a compromise inside the trusted managed-service gateway may bypass them.
7. **Request provider evidence proportionate to risk.** Highly regulated or high-impact users can ask Microsoft through established support channels for tenant-specific assurance, applicable log coverage, and the completed-remediation scope rather than relying on third-party scanning or attempting to reproduce the chain.

## Evidence and exploitation caveats
The public technical account comes from Wiz, the reporting researcher, with an embedded Microsoft statement. Microsoft says it reviewed access logs, found no activity outside the researcher's tests, and observed no customer-data access. Wiz withheld the full query pending its Black Hat USA presentation, and neither source published a CVE, exploit, affected regional build list, customer-visible indicator, or evidence of malicious exploitation. The absence of observed exploitation is not mathematically equivalent to proof that no access occurred, but there is currently no public basis to describe CosmosEscape as an active campaign or customer breach.

The 2025-11-22 hot fix blocked the reported Gremlin entry point; the July 2026 milestone was completion of a broader architectural migration and elimination of the Cosmos Master Key. These are distinct remediation stages and should not be represented as an eight-month period of known unmitigated exposure.

## Disclosure timeline
- **2025-11-20:** Wiz reported the issue; Microsoft acknowledged it the same day.
- **2025-11-22:** Microsoft deployed a hot fix blocking the reported entry point and began longer-term architectural work.
- **July 2026:** Microsoft completed the architectural fix across all regions and eliminated the Cosmos Master Key.
- **2026-07-30:** Wiz and Microsoft publicly disclosed the research and no-observed-exploitation conclusion.

## Related pages
- [Internet-exposed unauthenticated MCP servers](../patterns/internet-exposed-unauthenticated-mcp-servers.md)
- [Cloud logging control-plane tampering](../patterns/cloud-logging-control-plane-tampering.md)
- [Cloud bucket namespace hijacking](../patterns/cloud-bucket-namespace-hijacking.md)

## Sources
- Wiz Research, “CosmosEscape: Taking Over Every Database in Azure Cosmos DB,” 2026-07-30: [https://www.wiz.io/blog/cosmosescape-taking-over-every-database-in-azure-cosmos-db](https://www.wiz.io/blog/cosmosescape-taking-over-every-database-in-azure-cosmos-db)
- Microsoft statement reproduced in the coordinated disclosure above, including remediation, log-review, and customer-action conclusions.