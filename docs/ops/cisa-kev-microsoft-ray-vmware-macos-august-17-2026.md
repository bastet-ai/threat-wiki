# CISA KEV August 17–18 additions: Microsoft IKE, Ray, VMware vCenter, SharePoint, and macOS

## Summary
On August 17–18, 2026, CISA added five vulnerabilities to the Known Exploited Vulnerabilities catalog:

- **Microsoft Internet Key Exchange (IKE) Service Extensions CVE-2026-33824**, a double-free flaw enabling remote code execution, added August 18;
- **Broadcom VMware vCenter CVE-2026-59310**, a path traversal in the vCenter Syslog service allowing a network attacker to execute arbitrary code, added August 18;
- **Microsoft SharePoint CVE-2026-55040**, a weak-authentication flaw allowing an over-the-network security-feature bypass, added August 18;
- **Apple macOS CVE-2026-65400**, an improper-authentication flaw that lets a network attacker authenticate to Screen Sharing without valid credentials, added August 18; and
- **Ray-Project Ray CVE-2025-62593**, a code-injection flaw exploitable through Firefox and Safari that enables remote code execution against developers using Ray as a development tool, added August 17.

The four August 18 entries share a **2026-08-21** federal remediation deadline under BOD 26-04; Ray has a **2026-08-20** deadline. CISA records ransomware use as unknown for all five and does not identify actors, exploitation infrastructure, payloads, or victim scope.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- CVE-2026-33824
- CVE-2026-59310
- CVE-2026-55040
- CVE-2026-65400
- CVE-2025-62593
- Microsoft
- IKE
- Broadcom
- VMware
- vCenter
- SharePoint
- Apple
- macOS
- Screen Sharing
- Ray
- double free
- path traversal
- weak authentication
- improper authentication
- code injection
- DNS rebinding
- remote code execution
- BOD 26-04

## CVE-2026-33824 — Microsoft IKE Service Extensions
CISA describes CVE-2026-33824 as a **double-free** (CWE-415) vulnerability in the Internet Key Exchange Service Extensions that could enable remote code execution. Double-free RCE in a network-protocol service is an unauthenticated-reachability problem when IKE endpoints face untrusted networks. Microsoft's update guidance is to apply the vendor mitigation; CISA's BOD 26-04 and forensics-triage requirements apply. Inventory IKE/IPsec gateways and VPN concentrators, confirm the patch level from Microsoft's update guide, and preserve protocol and host telemetry where exploitation is suspected. The entry is a known-exploited determination and does not publish exploitation request patterns, infrastructure, or victims.

## CVE-2026-59310 — VMware vCenter Syslog path traversal
CISA describes CVE-2026-59310 as a **path traversal** (CWE-22) in the VMware vCenter Syslog server that a network attacker can use to execute arbitrary code. This is one of the two network-reachable vCenter flaws in **VMSA-2026-0006**; the wiki's [VMware vCenter and ESX critical flaws page](vmware-vmsa-2026-0006-vcenter-esx-critical-flaws.md) carries the full fixed-build matrix. The KEV addition upgrades that vulnerability from "no evidence of exploitation" to confirmed known exploitation. Operators should treat the VMSA-2026-0006 remediation as urgent and, because vCenter is a virtualization control plane, scope managed hosts and VMs if compromise is plausible. Fixed builds: vCenter 9.1 → 9.1.0.0300, 9.0 → 9.0.2.0100, 8.0 → 8.0 U3k.

## CVE-2026-55040 — Microsoft SharePoint weak authentication
CISA describes CVE-2026-55040 as a **weak-authentication** (CWE-1390) vulnerability in SharePoint that allows an unauthorized attacker to bypass a security feature over a network. SharePoint is a recurring exploitation target and already has several KEV entries on this wiki. The entry establishes known exploitation of this specific flaw without identifying a shared campaign across the multiple SharePoint vulnerabilities tracked here. Patch from Microsoft's update guide, inventory all SharePoint farm components and front-end proxies, and review access logs for unauthorized or out-of-band authentication attempts. **Update (August 24, 2026):** VulnCheck published a full unauthenticated-RCE chain combining this auth bypass with **CVE-2026-63520** (unsafe .NET type instantiation in BCS, fixed in KB5002893) — see the [SharePoint CVE-2026-55040 + CVE-2026-63520 RCE chain page](microsoft-sharepoint-cve-2026-55040-cve-2026-63520-rce-chain-vulncheck.md).

## CVE-2026-65400 — Apple macOS Screen Sharing improper authentication
CISA describes CVE-2026-65400 as an **improper-authentication** (CWE-287) vulnerability in macOS that could allow an attacker on the network to authenticate to Screen Sharing without valid credentials. Apple addressed it in a macOS security update; CISA lists three Apple support references. This is a lateral-movement and post-compromise access path: an attacker already positioned on the network can reach the remote-desktop service without credentials. Apply the macOS update, and where remote-desktop/Screen Sharing is exposed beyond the trusted network, enforce it behind VPN or restrict source addresses. Confirm the installed macOS build against Apple's advisory after patching.

## CVE-2025-62593 — Ray code injection via browser
CISA describes CVE-2025-62593 as a **code-injection** (CWE-94, CWE-352) vulnerability in Ray-Project Ray that could allow remote code execution. The developer-facing angle matters: GitHub's advisory (GHSA-q279-jhrf-cc6v, rated **Critical**) describes the flaw as a DNS-rebinding-adjacent browser attack exploitable through **Firefox and Safari** that targets developers using Ray as a development tool. Ray's own advisory lists affected versions **< 2.52.0** and patched version **2.52.0**. The wiki tracks Ray-cluster exploitation in the [TeamPCP / ShadowRay 2.0 lineage](../actors/teampcp.md#shadowray-20-and-ta-natalstatus-lineage); this KEV entry is a separate browser-to-developer-machine vector and CISA does not link it to that campaign. Upgrading Ray to 2.52.0 or later removes the described vector; treat an affected development environment as a potential initial-access path and preserve browser, network, and process telemetry if exploitation is suspected.

## Defender priorities
1. **Patch to the specific fixed builds, not the deadline.** The outer BOD 26-04 bound is 2026-08-20/21; an internet-reachable IKE gateway, vCenter, SharePoint, or macOS host is a patch-now decision, not a schedule.
2. **Scope post-exploitation separately from patching.** vCenter and SharePoint can reach broader control planes and data stores; macOS Screen Sharing is a lateral-movement surface; Ray is a developer-machine and cluster target.
3. **Preserve evidence before destructive cleanup.** Collect protocol, access-log, application, host, and network records while available. CISA's BOD 26-04 forensics-triage requirement applies to federal systems.
4. **Avoid cross-entry attribution.** Five KEV additions across five vendors do not establish a shared campaign or operator; each is an independent known-exploited determination.

## Related pages
- [Exploiting SharePoint: CVE-2026-55040 and CVE-2026-63520 RCE chain (VulnCheck)](microsoft-sharepoint-cve-2026-55040-cve-2026-63520-rce-chain-vulncheck.md)
- [VMware VMSA-2026-0006 vCenter and ESX critical flaws](vmware-vmsa-2026-0006-vcenter-esx-critical-flaws.md)
- [CISA KEV August 4 additions: N-central, Tomcat, and Langflow](cisa-kev-n-central-tomcat-langflow-august-4-2026.md)
- [CISA KEV: Check Point SmartConsole and Microsoft SharePoint July 22 additions](cisa-kev-check-point-smartconsole-sharepoint-july-22-2026.md)
- [TeamPCP group profile](../actors/teampcp.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- Microsoft: [CVE-2026-33824 update guidance](https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2026-33824)
- Microsoft: [CVE-2026-55040 update guidance](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-55040)
- Broadcom: [VMware security advisory 38017 (CVE-2026-59310)](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017)
- Apple: [macOS security update 148170](https://support.apple.com/en-us/148170)
- Ray-Project: [GHSA-q279-jhrf-cc6v advisory](https://github.com/ray-project/ray/security/advisories/GHSA-q279-jhrf-cc6v)
