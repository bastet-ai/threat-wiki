# CISA KEV: Microsoft SharePoint / ADFS, FortiSandbox, and SonicWall SMA1000 July 2026 additions

## Summary
On July 14-16, 2026, CISA added seven newly reported exploited vulnerabilities to the Known Exploited Vulnerabilities catalog across Microsoft identity/collaboration software, SonicWall SMA1000 appliances, and Fortinet FortiSandbox. The entries are high-signal because CISA's KEV catalog is an active-exploitation signal and several July 2026 entries carry emergency remediation due dates under BOD 26-04 guidance.

## Tags
- ops
- operations
- active exploitation
- CISA KEV
- Microsoft
- SharePoint
- ADFS
- SonicWall
- SMA1000
- Fortinet
- FortiSandbox
- edge appliance
- identity infrastructure
- authentication bypass
- code injection
- SSRF
- OS command injection

## KEV additions

| CVE | Product | Vulnerability | CISA due date | Public notes |
| --- | --- | --- | --- | --- |
| `CVE-2026-56155` | Microsoft Active Directory Federation Services | Insufficient granularity of access control; CISA describes local privilege escalation by an authorized attacker. | 2026-07-28 | Identity infrastructure: prioritize exposed or high-trust federation servers and preserve auth/audit evidence before rebuilds. |
| `CVE-2026-56164` | Microsoft SharePoint Server | Missing authentication for a critical function; CISA describes unauthenticated network privilege escalation. | 2026-07-17 | Treat internet-exposed or externally reachable SharePoint as urgent; review web, authentication, and file-write telemetry. |
| `CVE-2026-15409` | SonicWall SMA1000 Appliances | Server-side request forgery allowing unauthenticated remote requests to unintended locations. | 2026-07-17 | Edge/VPN appliance exposure makes SSRF useful for internal reachability and appliance-local follow-on probing. |
| `CVE-2026-15410` | SonicWall SMA1000 Appliances | Code injection that can allow a remote authenticated administrator to execute arbitrary OS commands under specific conditions. | 2026-07-17 | Investigate administrator-session abuse and appliance command execution, especially if paired with SSRF or credential exposure. |
| `CVE-2026-58644` | Microsoft SharePoint | Deserialization of untrusted data vulnerability. | 2026-07-19 | CISA's July 16 addition creates a second urgent SharePoint exploitation signal in the same week; prioritize exposed SharePoint estates and preserve IIS/ULS/authentication evidence before cleanup. |
| `CVE-2026-25089` | Fortinet FortiSandbox | OS command injection vulnerability. | 2026-07-19 | Treat internet-exposed malware-analysis/sandbox appliances as high-value control-plane assets; inspect for command execution, new jobs, configuration exports, and outbound staging traffic. |
| `CVE-2026-39808` | Fortinet FortiSandbox | OS command injection vulnerability. | 2026-07-19 | CISA lists this alongside CVE-2026-25089; patch/mitigate both and investigate for chained or repeated command-injection attempts. |

## Why this matters
- **Confirmed exploitation signal:** KEV inclusion means defenders should assume exploitation is occurring in the wild even where actor attribution or exploit-chain details are not yet public.
- **Identity and collaboration blast radius:** ADFS and SharePoint sit near authentication flows, document stores, and internal collaboration data. Compromise can lead to token abuse, lateral movement, or sensitive file access.
- **Security-appliance risk:** SonicWall SMA1000 and FortiSandbox are trusted edge/security appliances. Compromise can provide a durable perimeter or analysis-plane foothold, internal network visibility, and authentication or artifact exposure.
- **Short remediation window:** CISA's July 17 and July 19 due dates make these immediate operational priorities, not normal monthly-patch backlog items.

## Defender guidance
1. Inventory externally reachable SharePoint, ADFS, SonicWall SMA1000, and FortiSandbox assets, including managed-service, lab, disaster-recovery, and evaluation appliances.
2. Apply vendor mitigations or fixed versions according to MSRC, SonicWall PSIRT, and Fortinet PSIRT guidance. Where patching cannot be completed immediately, isolate exposure and apply compensating access controls.
3. Preserve logs before appliance or server rebuilds: web access logs, authentication logs, ADFS audit events, SharePoint ULS/IIS logs, SonicWall appliance logs, FortiSandbox job/admin/system logs, VPN/session history, admin-login history, submitted-sample history, and configuration-change records.
4. Hunt for post-exploitation rather than only vulnerability probes: unexpected SharePoint privilege changes, anomalous ADFS token or claims activity, new administrator sessions on SMA1000 or FortiSandbox, command-execution artifacts, internal-only HTTP requests from appliances, unexpected malware-analysis jobs, unexplained configuration exports, and suspicious outbound connections from security appliances.
5. Rotate credentials and tokens only after isolating suspected compromised hosts or appliances so live malware or web shells cannot capture the rotation process.
6. For internet-facing appliances, treat a successful exploit as a control-plane compromise: rebuild from trusted media/configuration where feasible, review downstream VPN/authentication/logging paths, and inspect for persistent accounts, altered access policy, tampered sample-processing pipelines, or exfiltrated configuration.

## Related pages
- [Microsoft SharePoint CVE-2026-45659 RCE exploitation](microsoft-sharepoint-cve-2026-45659-rce-exploitation.md)
- [FortiBleed Fortinet credential exposure](fortibleed-fortinet-credential-exposure.md)
- [Check Point VPN CVE-2026-50751 exploitation](check-point-vpn-cve-2026-50751-exploitation.md)
- [BeyondTrust RS / PRA CVE-2026-40138 / CVE-2026-40139 authentication bypass](beyondtrust-rs-pra-cve-2026-40138-40139-auth-bypass.md)

## Sources
- CISA Known Exploited Vulnerabilities catalog: [https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- MSRC CVE-2026-56155: [https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-56155](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-56155)
- MSRC CVE-2026-56164: [https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-56164](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-56164)
- MSRC CVE-2026-58644: [https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-58644](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-58644)
- SonicWall PSIRT SNWLID-2026-0008: [https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0008](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0008)
- Fortinet PSIRT CVE-2026-25089: [https://www.fortiguard.com/psirt/FG-IR-26-25089](https://www.fortiguard.com/psirt/FG-IR-26-25089)
- Fortinet PSIRT CVE-2026-39808: [https://www.fortiguard.com/psirt/FG-IR-26-39808](https://www.fortiguard.com/psirt/FG-IR-26-39808)
