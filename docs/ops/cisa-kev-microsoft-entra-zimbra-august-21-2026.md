# Zimbra SNMP command injection in CISA KEV; Microsoft patches Entra ID deserialization flaw (August 21, 2026)

## Summary
On August 21, 2026, CISA added **Synacor Zimbra Collaboration Suite (ZCS) CVE-2026-73570** (CVSS 8.9, High) to the Known Exploited Vulnerabilities catalog, with a **2026-08-24** BOD 26-04 remediation deadline. The flaw is an **OS command injection** (CWE-78) in the optional `zimbra-snmp` monitoring component that an unauthenticated attacker can reach by sending crafted SMTP requests when SNMP notifications are enabled. CISA lists ransomware use as unknown and identifies no actor, infrastructure, payload, or victim scope.

The same day, Microsoft patched and disclosed **Microsoft Entra ID CVE-2026-69836** (CVSS 10.0, Critical), a **deserialization of untrusted data** (CWE-502) flaw in the cloud identity service (formerly Azure Active Directory) that could allow an unauthorized, network-based attacker to execute code. As of the catalog's 2026.08.21 release (17:46 UTC), **CVE-2026-69836 is not in the KEV catalog** and Microsoft states it was not exploited in the wild — it is covered here for the combined incident timeline and the disputed exploitation status, not as a CISA known-exploited determination.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- CVE-2026-69836
- CVE-2026-73570
- Microsoft
- Entra ID
- Azure Active Directory
- Synacor
- Zimbra
- Zimbra Collaboration Suite
- ZCS
- deserialization
- OS command injection
- remote code execution
- SNMP
- unauthenticated
- CERT Polska
- BOD 26-04

## CVE-2026-69836 — Microsoft Entra ID deserialization RCE
Microsoft describes the flaw as "deserialization of untrusted data in Microsoft Entra ID that allows an unauthorized attacker to execute code over a network." NVD scores it **10.0 Critical** with vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` — network-reachable, no privileges or user interaction, scope changed (the identity platform is the blast radius).

Entra ID is Microsoft's central cloud identity and access-management service; a deserialization RCE here is a platform-level primitive rather than a single-app bug. The vulnerability was discovered and reported by Microsoft principal security engineer Robert Fitzpatrick.

**Exploitation status:** Microsoft's initial August 21 security bulletin marked the "Exploited" field as "Yes" and said the issue had "already been fully mitigated by Microsoft" with "no action for users of this service to take." After The Hacker News contacted Microsoft for comment, Microsoft **corrected the Exploited status to "No"** on August 21, 2026, stating "this vulnerability was not exploited in the wild." No CISA KEV listing followed as of the catalog's 2026.08.21 release. Treat the "exploited" question as closed in Microsoft's favor, and do not let "fully mitigated, no action required" displace a review of whether any unpatched or self-hosted identity surfaces (e.g., on-premises AD federation, legacy AAD connectors, or third-party SSO that fronts Entra) remain reachable.

## CVE-2026-73570 — Zimbra SNMP command injection
Zimbra describes the flaw as a **command injection in the SNMP monitoring component** exploitable **when the optional `zimbra-snmp` package is installed and SNMP notifications are enabled**. NVD describes it as: "A remote code execution vulnerability exists in Zimbra Collaboration (ZCS) before 10.1.20 when the optional zimbra-snmp package is installed and SNMP notifications are enabled. Due to improper sanitization of untrusted input during SNMP notification processing, an unauthenticated attacker can send specially crafted SMTP requests that may result in execution of arbitrary operating system commands as the Zimbra user," scored **8.9 High** with vector `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L`.

The unauthenticated, network-reachable, arbitrary-OS-command-execution primitive is the high-signal part: any ZCS deployment that has enabled SNMP notifications and is reachable from untrusted networks is a patch-now target. This is a **permanent fix for the critical SNMP vulnerability Zimbra disclosed in its June 26, 2026 security advisory**, shipped in **Zimbra 10.1.20** (July 20, 2026). Zimbra 10.1.20 also fixes a stored XSS cluster in the Classic Web Client, an EWS access-control issue (CVE-2026-10631), a mail-forwarding-restriction bypass (CVE-2026-50055), a mailbox-delegation authorization issue (CVE-2026-50054), and a Nextcloud-integration SSRF.

The KEV addition corroborates the August 20, 2026 The Hacker News report of active exploitation of the Zimbra SNMP flaw for unauthenticated remote code execution.

## Defender priorities
1. **Zimbra:** Upgrade any ZCS deployment with `zimbra-snmp` installed and SNMP notifications enabled to **10.1.20**, and disable the optional SNMP-notifications feature where it is not required. Verify the Zimbra user account and its host for signs of arbitrary command execution around the exposure window; the KEV entry carries a 2026-08-24 BOD 26-04 bound, so an internet-reachable SNMP-enabled ZCS is a patch-now decision.
2. **Entra / identity:** CVE-2026-69836 is a CVSS 10.0 cloud-identity deserialization primitive that Microsoft reports as fully mitigated and not exploited in the wild. Confirm no on-premises or federated identity surface fronting Entra remains unpatched — inventory SSO, legacy AAD Connect / Entra Connect, and any third-party IdP that proxies Entra — and preserve identity-signing and protocol telemetry for the disclosure window.
3. **Preserve evidence before destructive cleanup.** CISA's BOD 26-04 forensics-triage requirement applies to federal systems for the Zimbra KEV entry.
4. **Avoid cross-entry attribution.** A CISA KEV listing for Zimbra and a Microsoft vendor patch for Entra ID on the same day do not establish a shared campaign or operator; each is an independent determination.
5. **Re-check the KEV catalog.** If CISA adds CVE-2026-69836 in a later release, reclassify the Entra section as a known-exploited determination and update this page's title and tags.

## Assessment limits
- CVE-2026-69836 exploitation status was initially disputed inside Microsoft's own bulletin ("Exploited: Yes," then corrected to "No" — "not exploited in the wild"). No public PoC, exploit, or actor linkage is available, and the catalog's 2026.08.21 release contains no KEV entry for it.
- CVE-2026-73570 active exploitation was reported by CERT Polska via The Hacker News (August 20, 2026); Zimbra's 10.1.20 permanent fix and the CISA KEV entry corroborate it. No CISA-published victim scope.
- CISA records ransomware use as unknown for the Zimbra entry and identifies no infrastructure or payload.

## Related pages
- [CISA KEV August 17–18 additions](cisa-kev-microsoft-ray-vmware-macos-august-17-2026.md)
- [CISA KEV August 4 additions: N-central, Tomcat, and Langflow](cisa-kev-n-central-tomcat-langflow-august-4-2026.md)
- [GitLab GraphQL CVE-2026-19478 / CVE-2026-19650 critical patch](gitlab-graphql-cve-2026-19478-19650-critical-patch.md)
- [CL-STA-1114 Zimbra webmail espionage](cl-sta-1114-zimbra-webmail-espionage.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- Microsoft: [CVE-2026-69836 update guidance](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-69836)
- NVD: [CVE-2026-69836](https://nvd.nist.gov/vuln/detail/CVE-2026-69836)
- Zimbra: [Zimbra Security Advisories](https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories)
- Zimbra: [Patch Release Update: Zimbra 10.1.20](https://blog.zimbra.com/2026/07/patch-release-update-zimbra-10-1-20/)
- NVD: [CVE-2026-73570](https://nvd.nist.gov/vuln/detail/CVE-2026-73570)
- The Hacker News: [Microsoft Patches Severe Entra ID Flaw (CVSS 10.0) Allowing Remote Code Execution](https://thehackernews.com/2026/08/microsoft-entra-id-flaw-cvss-100.html)
- The Hacker News: [Attackers Exploit Zimbra SNMP Flaw for Unauthenticated Remote Code Execution](https://thehackernews.com/2026/08/attackers-exploit-zimbra-snmp-flaw-for.html)
