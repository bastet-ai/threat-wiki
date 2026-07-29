# CISA KEV: Check Point SmartConsole and Microsoft SharePoint July 22, 2026 additions

## Summary
On 2026-07-22, CISA added `CVE-2026-16232` in Check Point security-management servers and `CVE-2026-50522` in Microsoft SharePoint Server to the Known Exploited Vulnerabilities catalog. Both entries have a 2026-07-25 remediation due date under CISA's accelerated BOD 26-04 process.

The Check Point issue is the more operationally detailed disclosure: Check Point says an unauthenticated attacker can obtain an application login token, authenticate through SmartConsole with full administrative privileges, and change security policy or configuration. The vendor says exploitation has affected a very small number of customers. A July 23 Rapid7 follow-up records a sixth published attacker IP, two companion flaws fixed by the same emergency hotfixes, audit-log guidance, exposure conditions, and the fixed Jumbo Hotfix Accumulator takes.

The SharePoint issue is a critical deserialization vulnerability that can lead to remote code execution. CISA describes an unauthorized network attacker, while Microsoft's public FAQ says exploitation requires an attacker authenticated as at least a Site Owner. Microsoft's CVSS vector nevertheless records `PR:N`, and the MSRC API still displayed `exploited: No` when checked after CISA's KEV publication. Treat CISA's catalog entry as the active-exploitation signal and do not delay patching while the public descriptions are reconciled.

## Tags
- ops
- operations
- active exploitation
- CISA KEV
- Check Point
- SmartConsole
- Security Management Server
- Multi-Domain Security Management
- authentication bypass
- application token
- firewall management
- Microsoft
- SharePoint
- deserialization
- remote code execution
- CVE-2026-16232
- CVE-2026-62144
- CVE-2026-62145
- GaiaOS WebUI
- CVE-2026-50522

## Check Point CVE-2026-16232

### Impact and exposed conditions
Check Point's advisory covers Security Management Server and Multi-Domain Security Management Server releases `R77.30`, `R80`, `R80.10`, `R80.20`, `R80.30`, `R81`, `R81.10`, `R81.20`, `R82`, and `R82.10`; several older branches are already end of support.

The vendor says successful remote exploitation requires:

- internet access to the management-server IP address; and
- no effective Trusted Clients restriction for GUI clients, such as a Trusted Client type of `Any`.

A successful attacker receives full administrative access through the SmartConsole login path and can modify firewall security policy and management configuration. That makes this a control-plane compromise, not merely a console-account event.

### Companion vulnerabilities in the emergency update
Rapid7's July 23 synthesis of the Check Point advisory identifies two additional flaws addressed by the same July 22 Jumbo Hotfix release:

| CVE | Severity | Impact | Affected product families | Exploitation status reported July 23 |
| --- | --- | --- | --- | --- |
| `CVE-2026-62144` | Critical; vendor CVSS 9.3 | Management authentication bypass and privilege escalation | Security Management and Multi-Domain Management | No known exploitation |
| `CVE-2026-62145` | High; CVSS 7.5 | Local privilege escalation in GaiaOS WebUI | Firewall, Multi-Domain Management, and Multi-Domain Log Server | No known exploitation |

These companion flaws do not expand CISA's July 22 KEV entry, which names only `CVE-2026-16232`. They do matter for remediation scope: the emergency hotfix is a three-vulnerability update, and defenders should validate the applicable management, firewall, and log-server estate rather than treating it as a SmartConsole-only patch. Rapid7 says `CVE-2026-62144` and `CVE-2026-62145` affect the `R81.10`, `R81.20`, `R82`, and `R82.10` families; consult the current Check Point advisory for release-specific takes.

### Vendor fixes
Check Point says the fix is included in:

| Release | Fixed Jumbo Hotfix Accumulator |
| --- | --- |
| `R82.10` | Take 36 or later |
| `R82` | Take 118 or later |
| `R81.20` | Take 158 or later |

For unsupported or unlisted releases, follow Check Point support guidance and move to a supported fixed branch. Restrict management access and Trusted Clients immediately; those controls reduce exposure but are not substitutes for applying the vendor fix.

Check Point reports that Smart-1 Cloud customers are already protected. Where an on-premises hotfix cannot be installed immediately, restrict GUI Trusted Clients and management access to explicit trusted IP addresses or subnets and verify that implied control-connection rules are enabled. Continue with emergency patching and compromise assessment; these are exposure reductions, not fixes.

### Published infrastructure and hunt pivots
Check Point published these attacker IP addresses:

```text
151.241.99.207
151.241.99.233
158.62.198.182
192.142.10.99
139.28.37.250
194.213.18.137
```

Use them as investigation pivots, not as a complete blocklist or attribution set. Check Point recommends searching SmartConsole Logs & Events for the IPs as source or destination and searching Audit Logs for:

```text
Authentication method: application token
```

Also review newly created or changed administrators, policy installations, object and rule changes, Trusted Client changes, management API activity, exports or backups, and outbound connections from the management server. Preserve audit and policy history before remediation.

### Rapid7 root-cause and public-PoC follow-up
On 2026-07-29, Rapid7 published a technical analysis and proof-of-concept validator after reproducing the flaw against `R81.20` and `R82.10`. The root cause is a broken identity-binding boundary: the remote application-authentication path trusted an attacker-supplied Secure Internal Communication distinguished name instead of binding it to the authenticated peer certificate's DN. An unauthenticated client could learn the management server's own SIC DN during bootstrap, replay it during an application bind, obtain an application token, and exchange that token through the legacy management service for a SmartConsole SSO ticket.

Rapid7 compared `R81.20` Jumbo Hotfix Take 146 with fixed Take 158. The patched path accepts a supplied DN only for loopback traffic and otherwise requires the supplied identity to match the authenticated peer certificate and expected remote IP context. Rapid7 confirmed that the public validator succeeds against its vulnerable test systems and fails after the vendor hotfix.

The new public PoC increases the likelihood of scanning and copycat exploitation but does not itself establish new victims. Do not run it against systems you do not own or have explicit permission to test. Defenders should prioritize patch verification, restrict management-plane reachability, and hunt for the existing audit event `Authentication method: application token`; a successful ticket redemption uses the normal SmartConsole SOAP login path and can therefore look like a privileged console session after the initial bind.

## Microsoft SharePoint CVE-2026-50522

### Affected products and fixes
Microsoft rates the issue Critical with CVSS 3.1 base score 9.8. The July 2026 security updates cover:

| Product | Security update | Fixed build |
| --- | --- | --- |
| SharePoint Server Subscription Edition | KB5002882 | `16.0.19725.20434` |
| SharePoint Server 2019 | KB5002883 | `16.0.10417.20175` |
| SharePoint Enterprise Server 2016 / SharePoint Server 2016 | KB5002891 | `16.0.5561.1001` |

Microsoft says the flaw is deserialization of untrusted data in SharePoint and can produce network-reachable remote code execution. A reboot may be required for each listed update.

### Public-description discrepancy
The currently published sources do not agree on the privilege prerequisite:

- CISA says an unauthorized attacker can execute code over a network.
- Microsoft's vulnerability description and CVSS vector indicate network exploitation with no privileges or user interaction.
- Microsoft's FAQ says the attacker must be authenticated as at least a Site Owner and can then inject and execute arbitrary code.
- Microsoft's API had not yet changed its own exploited flag to `Yes` after KEV inclusion.

This discrepancy should lower confidence in the exact initial-access precondition, not in the need to respond. Internet-facing SharePoint servers and servers reachable by untrusted or lightly privileged users should receive the July fix first.

### Hunt and response guidance
1. Inventory all SharePoint farms, including test, disaster-recovery, extranet, and externally published systems, and verify the installed build rather than relying only on patch-management status.
2. Preserve IIS, ULS, Windows event, authentication, EDR, and file-integrity telemetry before cleanup.
3. Review anomalous requests and exceptions around deserialization or object-state processing, unexpected child processes from SharePoint/IIS service processes, suspicious assembly or script writes, newly modified web content, web-shell behavior, and unusual outbound connections.
4. Investigate newly used Site Owner accounts and unexpected privilege or site-membership changes because Microsoft's FAQ identifies Site Owner access as one possible prerequisite.
5. If exploitation is suspected, isolate before rotating farm, service-account, application-pool, database, and integration credentials; otherwise an active foothold may capture replacements.

## Priority actions
1. **Check Point:** remove internet exposure from management servers where possible, restrict Trusted Clients to explicit trusted IPs/subnets, apply the fixed Jumbo Hotfix take across the applicable management/firewall estate, preserve management audit logs, and investigate application-token authentications and the six published IP addresses.
2. **SharePoint:** apply the July 2026 security update and verify the resulting fixed build across every server in each farm.
3. Treat confirmed Check Point exploitation as a firewall-management-plane incident: review policy/configuration integrity and downstream trust, then rebuild from trusted media or known-good configuration where evidence supports compromise.
4. Treat suspected SharePoint exploitation as server compromise, not only a patching event; hunt for post-exploitation and credential use, and preserve evidence before rebuilding.
5. Do not infer actor or ransomware attribution from KEV inclusion. CISA lists ransomware use as unknown for both entries.

## Related pages
- [CISA KEV: Microsoft SharePoint / ADFS, FortiSandbox, and SonicWall SMA1000 July 2026 additions](cisa-kev-microsoft-sharepoint-adfs-sonicwall-sma1000-july-2026.md)
- [Microsoft SharePoint CVE-2026-45659 RCE exploitation](microsoft-sharepoint-cve-2026-45659-rce-exploitation.md)
- [Check Point VPN CVE-2026-50751 exploitation](check-point-vpn-cve-2026-50751-exploitation.md)
- [UTA0533 SonicWall SMA1000 zero-day compromise](uta0533-sonicwall-sma1000-zero-day-compromise.md)

## Sources
- CISA Known Exploited Vulnerabilities catalog: [https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- Check Point `sk185169`, CVE-2026-16232: [https://support.checkpoint.com/results/sk/sk185169](https://support.checkpoint.com/results/sk/sk185169)
- Rapid7, “CVE-2026-16232: Critical Check Point SmartConsole Authentication Bypass Exploited in the Wild,” 2026-07-23: [https://www.rapid7.com/blog/post/etr-cve-2026-16232-critical-check-point-smartconsole-authentication-bypass-exploited-in-the-wild/](https://www.rapid7.com/blog/post/etr-cve-2026-16232-critical-check-point-smartconsole-authentication-bypass-exploited-in-the-wild/)
- Rapid7, “Check Point SmartConsole Authentication Bypass Technical Analysis (CVE-2026-16232),” 2026-07-29: [https://www.rapid7.com/blog/post/ra-check-point-smartconsole-authentication-bypass-technical-analysis-cve-2026-16232/](https://www.rapid7.com/blog/post/ra-check-point-smartconsole-authentication-bypass-technical-analysis-cve-2026-16232/)
- Rapid7 public validator repository: [https://github.com/sfewer-r7/CVE-2026-16232](https://github.com/sfewer-r7/CVE-2026-16232)
- MSRC CVE-2026-50522: [https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50522](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50522)
- MSRC Security Update Guide API, CVE-2026-50522: [https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability/CVE-2026-50522](https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability/CVE-2026-50522)
- MSRC affected-product API query, CVE-2026-50522: [https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$filter=cveNumber%20eq%20%27CVE-2026-50522%27](https://api.msrc.microsoft.com/sug/v2.0/en-US/affectedProduct?$filter=cveNumber%20eq%20%27CVE-2026-50522%27)
