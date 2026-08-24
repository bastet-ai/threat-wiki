# CISA KEV August 11 additions: Windows WinSock zero-day, Metabase, and Cisco ASA/FTD

## Summary
On August 11, 2026, CISA added three vulnerabilities to the Known Exploited Vulnerabilities catalog:

- **Microsoft Windows Ancillary Function Driver for WinSock CVE-2026-68820**, a use-after-free flaw that lets a locally authenticated attacker elevate privileges to SYSTEM, added August 11. This was the exploited zero-day in Microsoft's August 2026 Patch Tuesday release and the entry this scan promotes;
- **Metabase CVE-2026-72898**, an unauthenticated SQL-injection flaw in the password-reset API that yields administrator access and connected-database credential exposure, added August 11; and
- **Cisco Secure Firewall ASA/FTD CVE-2026-20349**, a heap-inspection flaw that lets an unauthenticated remote attacker force the device to reload, causing a denial of service, added August 11.

The WinSock entry has a **2026-08-25** BOD 26-04 remediation deadline; the Metabase and Cisco ASA/FTD entries carry a **2026-08-14** deadline. CISA records ransomware use as unknown for all three and does not identify actors, exploitation infrastructure, payloads, or victim scope.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- zero-day
- CVE-2026-68820
- CVE-2026-72898
- CVE-2026-20349
- Microsoft
- Windows
- WinSock
- Ancillary Function Driver
- use-after-free
- local privilege escalation
- BOD 26-04
- Metabase
- SQL injection
- Cisco
- Secure Firewall
- ASA
- FTD
- denial of service

## CVE-2026-68820 — Microsoft Windows WinSock use-after-free (the exploited zero-day)
CISA describes CVE-2026-68820 as a **use-after-free** (CWE-416) vulnerability in the Windows Ancillary Function Driver for WinSock (AFD) that allows an authorized, locally authenticated attacker to elevate privileges. Microsoft's NVD-recorded CVSS is **7.0 (High)**, `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` — local vector, high attack complexity, low privileges required, full impact on confidentiality, integrity, and availability. CISA's SSVC assessment marks exploitation **active**, technical impact **total**, and not automatable.

This was the single exploited zero-day in Microsoft's **August 2026 Patch Tuesday** (415 CVEs, of which 62 were rated critical). CrowdStrike's Patch Tuesday analysis identified it as the one actively exploited 0-day in the batch. The driver-level location (AFD is the kernel-mode network I/O path under `winsock2`) means a successful local escalation reaches SYSTEM on a wide base of Windows hosts — a post-compromise primitive an attacker who already has foothold access on an endpoint can use to break out of a lower-privilege context, bypass user-mode protections, and reach credential and token material.

Operators should treat this as patch-now for internet-adjacent Windows fleets and any host where a lower-privilege foothold is plausible. Confirm the specific KB from Microsoft's update guide is applied, and where exploitation is suspected, preserve host and process telemetry before destructive cleanup. The BOD 26-04 outer bound is 2026-08-25, but an endpoint that is likely compromised is not a schedule.

## CVE-2026-72898 — Metabase unauthenticated SQL injection
CISA describes CVE-2026-72898 as a SQL-injection vulnerability in Metabase that lets an unauthenticated remote attacker inject arbitrary SQL into the application database through the password-reset API, enabling administrator access and exposure of connected-database credentials. The wiki already tracks this in detail on the [Metabase unauthenticated SQL-injection zero-day page](metabase-unauthenticated-sql-injection-zero-day.md), which carries the fixed point-release matrix, the `/api/session/reset_password` blocking workaround, and downstream customer-data findings. This KEV addition upgrades it to confirmed known exploitation with an 2026-08-14 BOD 26-04 deadline.

## CVE-2026-20349 — Cisco Secure Firewall ASA/FTD heap inspection DoS
CISA describes CVE-2026-20349 as a **heap inspection** vulnerability in Cisco Secure Firewall ASA and FTD that could allow an unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service. The Cisco advisory is `cisco-sa-asaftd-vpn-dos-dzv4mQFF`. Because the device reloads on the affected path, this is an availability impact on a network perimeter appliance: a single unauthenticated request pattern can drop the firewall, taking the protected segment with it. The wiki's [Cisco Crosswork and Secure Workload page](cisco-crosswork-secure-workload-nine-flaws-five-cvss-10-august-21-2026.md) references this in-the-wild exploitation as context; this KEV entry is the formal known-exploited determination. Patch ASA/FTD to a fixed release per the Cisco advisory, and if a perimeter appliance is internet-facing, treat the 2026-08-14 deadline as urgent.

## Defender priorities
1. **WinSock first.** CVE-2026-68820 is the exploited zero-day with the broadest blast radius: any Windows host with a plausible local foothold. Patch to the specific KB, not the deadline; an internet-facing or likely-compromised endpoint is a patch-now decision.
2. **Scope the three separately.** WinSock is a post-compromise local escalation; Metabase is an unauthenticated application-admin path to connected data; ASA/FTD is an unauthenticated perimeter DoS. Each has a distinct detection and containment posture.
3. **Preserve evidence before destructive cleanup.** Collect host, process, application, and network records while available. CISA's BOD 26-04 forensics-triage requirement applies to federal systems.
4. **Avoid cross-entry attribution.** Three KEV additions across three vendors do not establish a shared campaign or operator; each is an independent known-exploited determination.

## Related pages
- [Metabase unauthenticated SQL-injection zero-day](metabase-unauthenticated-sql-injection-zero-day.md)
- [Cisco Crosswork and Secure Workload: nine flaws patched, five scoring CVSS 10.0](cisco-crosswork-secure-workload-nine-flaws-five-cvss-10-august-21-2026.md)
- [CISA KEV August 17–18 additions: Microsoft IKE, Ray, VMware vCenter, SharePoint, macOS](cisa-kev-microsoft-ray-vmware-macos-august-17-2026.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- Microsoft: [CVE-2026-68820 advisory](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2026-68820)
- NVD: [CVE-2026-68820](https://nvd.nist.gov/vuln/detail/CVE-2026-68820)
- CrowdStrike: [August 2026 Patch Tuesday: Updates and Analysis](https://www.crowdstrike.com/en-us/blog/patch-tuesday-analysis-august-2026/)
- Metabase: [security update](https://www.metabase.com/blog/security-update), [GHSA-vwf4-m7j8-wcjf](https://github.com/metabase/metabase/security/advisories/GHSA-vwf4-m7j8-wcjf)
- Cisco: [ASA/FTD VPN DoS advisory (cisco-sa-asaftd-vpn-dos-dzv4mQFF)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-vpn-dos-dzv4mQFF)
