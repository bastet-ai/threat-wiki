# CISA KEV August 4 additions: N-central, Tomcat, and Langflow

## Summary
On August 4, 2026, CISA added three vulnerabilities to the Known Exploited Vulnerabilities catalog:

- **N-able N-central CVE-2026-18556**, the original authentication-bypass flaw in an actively exploited remote-monitoring and management platform;
- **Apache Tomcat CVE-2026-34486**, a bypass of the earlier CVE-2026-29146 fix for `EncryptInterceptor`; and
- **IBM Langflow CVE-2026-9198**, an unauthenticated token-minting and Python code-execution chain affecting default deployments.

All three have a **2026-08-07** federal remediation deadline under BOD 26-04. CISA records ransomware use as unknown and does not identify actors, exploitation infrastructure, payloads, or victim scope for these entries.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- CVE-2026-18556
- CVE-2026-34486
- CVE-2026-9198
- N-able
- N-central
- Apache Tomcat
- EncryptInterceptor
- IBM
- Langflow
- authentication bypass
- code execution
- RMM
- AI application infrastructure

## CVE-2026-18556 — N-able N-central
CISA describes CVE-2026-18556 as an authentication bypass using an alternate path or channel. The August 4 addition complements the catalog's August 3 addition of **CVE-2026-18577**, the alternate path left by the incomplete first fix. The two entries have different deadlines: August 7 for CVE-2026-18556 and August 6 for CVE-2026-18577.

Operators should not interpret the second KEV entry as a separate patch target. N-able's emergency guidance remains to upgrade N-central to **2026.3.1.7** and then investigate the management server and downstream endpoints for activity conducted through Take Control, including Cloudflare Tunnel persistence. See the [N-central incident page](n-able-n-central-cve-2026-18556-18577-exploitation.md) for campaign detail and public indicators.

## CVE-2026-34486 — Apache Tomcat EncryptInterceptor bypass
Apache rates CVE-2026-34486 **Important**. An error in the CVE-2026-29146 fix allowed Tomcat's `EncryptInterceptor` to be bypassed. Apache lists these specific affected releases and fixed versions:

| Affected release | Upgrade target |
|---|---|
| Tomcat `11.0.20` | `11.0.21` or later |
| Tomcat `10.1.53` | `10.1.54` or later |
| Tomcat `9.0.116` | `9.0.117` or later |

`EncryptInterceptor` protects Tomcat cluster traffic; exploitation relevance therefore depends on use and exposure of the affected clustering path. CISA's KEV addition confirms exploitation but does not publish request patterns, infrastructure, payloads, or victim details. Inventory exact Tomcat versions and cluster configuration, upgrade affected nodes, and review cluster-member and network telemetry for unexpected peers or unencrypted/suspicious replication traffic.

## CVE-2026-9198 — Langflow unauthenticated RCE
IBM scores CVE-2026-9198 **9.8 CVSS 3.1** and lists Langflow OSS `1.0.0` through `1.10.0` as affected. The default-deployment chain combines:

1. unauthenticated access to `/api/v1/auto_login`, which can mint a superuser bearer token for a network caller; and
2. authenticated submission to `/api/v1/validate/code`, where Python `exec()` evaluates attacker-controlled code, including decorators, default arguments, and annotations at function-definition time.

IBM recommends upgrading to **Langflow OSS 1.10.1** and lists no workaround. Because the chain yields host-level Python execution, responders should treat a reachable affected instance as a potential initial-access path: preserve reverse-proxy and application logs, review requests to both endpoints in sequence, inspect Langflow/Python process descendants and outbound traffic, rotate secrets available to the service after containment, and rebuild where execution cannot be ruled out.

Do not conflate CVE-2026-9198 with the several other Langflow vulnerabilities and campaigns already tracked on threat.wiki. The CISA entry establishes exploitation of this specific auto-login-plus-validation chain but does not link it to JADEPUFFER, cryptomining, SSH worming, or another named operator.

## Defender priorities
1. **Patch on exposure, not on the August 7 outer bound.** Upgrade N-central to `2026.3.1.7`, affected Tomcat branches to the fixed releases above, and Langflow to `1.10.1`.
2. **Scope post-exploitation separately from patching.** N-central can project authority into managed endpoints; Langflow can expose host and cloud credentials; Tomcat cluster trust may cross nodes.
3. **Preserve evidence before destructive cleanup.** Collect application, reverse-proxy, identity, process, network, and management-plane records while they remain available.
4. **Avoid unsupported attribution.** KEV inclusion confirms exploitation, not a shared campaign or actor across the three products.

## Related pages
- [N-able N-central CVE-2026-18556 / CVE-2026-18577 exploitation](n-able-n-central-cve-2026-18556-18577-exploitation.md)
- [Langflow CVE-2026-0770 exploitation](langflow-cve-2026-0770-exploitation.md)
- [Langflow CVE-2026-33017 cryptominer / SSH worm](langflow-cve-2026-33017-cryptominer-ssh-worm.md)
- [Langflow CVE-2026-55255 flow authorization bypass](langflow-cve-2026-55255-flow-authorization-bypass.md)
- [JADEPUFFER Langflow agentic ransomware](jadepuffer-langflow-agentic-ransomware.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- CISA: [August 4, 2026 alert — CISA Adds Three Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/08/04/cisa-adds-three-known-exploited-vulnerabilities-catalog)
- Apache Tomcat: [CVE-2026-34486 security advisory](https://lists.apache.org/thread/9510k5p5zdvt9pkkgtyp85mvwxo2qrly)
- IBM: [Security Bulletin: Unauthenticated Remote Code Execution via Auto-Login Bypass and Code Validation](https://www.ibm.com/support/pages/node/7278927)
- N-able: [N-central security update](https://www.n-able.com/blog/n-central-security-update-august-2-2026)
