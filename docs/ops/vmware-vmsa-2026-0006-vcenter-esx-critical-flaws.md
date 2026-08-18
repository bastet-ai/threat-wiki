# VMware VMSA-2026-0006 vCenter and ESX critical flaws

## Summary
Broadcom's **VMSA-2026-0006**, published July 29, 2026, fixes five vulnerabilities across VMware vCenter, ESX, Workstation, Fusion, Cloud Foundation, vSphere Foundation, and related Telco products. The highest-risk issues are two network-reachable vCenter flaws rated CVSS 9.8 and an ESX VMXNET3 guest-to-host escape rated CVSS 9.3.

- **CVE-2026-59309:** VMware Directory Service authentication bypass; a network attacker can gain unauthorized vCenter access.
- **CVE-2026-59310:** vCenter Syslog server directory traversal leading to arbitrary code execution by a network attacker.
- **CVE-2026-47876:** VMXNET3 out-of-bounds write; an attacker with local administrator rights inside a VM using VMXNET3 can execute code on the ESX host.
- **CVE-2026-41703:** ESX, Workstation, and Fusion out-of-bounds read causing information disclosure or host-process denial of service.
- **CVE-2026-41709:** ESX logging gap allowing a malicious administrator to perform some operations without logging.

Broadcom reports no evidence of exploitation in the wild and provides no workaround. This page is urgent vulnerability intelligence, not an active-exploitation claim.

## Tags
- ops
- operations
- VMware
- Broadcom
- VMSA-2026-0006
- vCenter
- ESX
- ESXi
- Cloud Foundation
- vSphere Foundation
- VMXNET3
- authentication bypass
- directory traversal
- remote code execution
- virtual machine escape
- information disclosure
- denial of service
- logging impairment
- CVE-2026-59309
- CVE-2026-59310
- CVE-2026-47876
- CVE-2026-41703
- CVE-2026-41709

## Why this matters
- vCenter is a virtualization control plane. Network-level authentication bypass or code execution can expose host, VM, credential, backup, snapshot, and management authority well beyond one server.
- CVE-2026-47876 crosses the guest-to-host boundary. Its prerequisite is already-high privilege inside a VM and use of the VMXNET3 adapter, but successful exploitation reaches the ESX host.
- Broadcom lists **no workaround** for the five issues. Network isolation can reduce reachability, but patching is the remediation.
- The affected matrix spans 8.x, 9.x, Cloud Foundation 5.x, and Telco products; fixed builds differ by product and branch.

## Key fixed versions
Consult the live Broadcom response matrix before deployment. The July 29 initial advisory lists:

- **vCenter 9.1:** 9.1.0.0300 for CVE-2026-59309 and CVE-2026-59310. The authentication-bypass fix first appeared in 9.1.0.0200, but 9.1.0.0300 is the current cumulative release.
- **vCenter 9.0:** 9.0.2.0100.
- **vCenter 8.0:** 8.0 U3k.
- **ESX 9.1 VMXNET3 escape:** ESXi-9.1.0.0200-25557999.
- **ESX 9.0 VMXNET3 escape:** ESXi-9.0.2.0100-25595025.
- **ESX 8.0 VMXNET3 escape:** ESXi80U3k-25595708.
- **Workstation and Fusion CVE-2026-41703:** 26H1.
- **Cloud Foundation and Telco products:** use the async-patch or knowledge-base path named in VMSA-2026-0006; do not infer coverage from a component version alone.

## Defender actions
1. Inventory every vCenter, ESX/ESXi, Cloud Foundation, vSphere Foundation, Workstation, Fusion, and Telco deployment, including isolated management environments and disaster-recovery sites.
2. Apply the exact fixed build or asynchronous patch in Broadcom's product matrix. Because there is no workaround, do not defer remediation based only on perimeter controls.
3. Until patched, restrict vCenter management access to dedicated administration networks and strongly authenticated jump paths. Remove direct internet reachability and unnecessary cross-tenant or workload-network routes.
4. Prioritize vCenter first where network reachability is broad, then ESX hosts running attacker-reachable VMs with VMXNET3. Verify adapter use rather than assuming all guests have the same virtual NIC.
5. Preserve vCenter, VMware Directory Service, Syslog, SSO, API, task/event, hostd, vpxa, shell, VM, and network telemetry if compromise is suspected. CVE-2026-41709 means absence of some ESX audit records cannot by itself rule out malicious administrator activity.
6. Hunt for unexplained vCenter authentication or account changes, new permissions, unusual Syslog requests or filesystem writes, unexpected vCenter child processes or egress, host configuration changes, VM lifecycle operations, and abnormal ESX host-process crashes.
7. If control-plane compromise is plausible, scope all managed hosts and VMs, rotate vCenter and automation credentials, review trust relationships and backup systems, and restore management components from known-good media where integrity cannot be established.

## Exploitation-status caveat
The initial Broadcom advisory says the issues were privately reported and that Broadcom had found no evidence of in-the-wild exploitation. Public discussion of a VM escape or unauthenticated vCenter path does not establish exploitation. Reassess if Broadcom, CISA, incident responders, or credible telemetry later changes that status.

## August 18 update: CISA KEV confirms exploitation of CVE-2026-59310
On August 18, 2026, CISA added **CVE-2026-59310** (the vCenter Syslog-server path traversal) to the Known Exploited Vulnerabilities catalog with a **2026-08-21** BOD 26-04 remediation deadline. This upgrades the flaw from "no evidence of exploitation" to confirmed known exploitation. The remaining four vulnerabilities in VMSA-2026-0006 (CVE-2026-59309, CVE-2026-47876, CVE-2026-41703, CVE-2026-41709) are not yet in KEV. See the [CISA KEV August 17–18 additions page](cisa-kev-microsoft-ray-vmware-macos-august-17-2026.md#cve-2026-59310-vmware-vcenter-syslog-path-traversal) for the full entry. Treat the VMSA-2026-0006 fixed-build matrix as urgent for all network-reachable vCenter deployments.

## Related pages
- [Januscape KVM CVE-2026-53359 guest-to-host escape](januscape-kvm-cve-2026-53359-guest-to-host-escape.md)
- [VerdantBamboo appliance BRICKSTORM operation](verdantbamboo-appliance-brickstorm-operation.md)
- [Operation Highland Velvet Ant authentication-stack backdoors](operation-highland-velvet-ant-authentication-stack-backdoors.md)

## Sources
- Broadcom security advisory: [VMSA-2026-0006](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017)
- Broadcom supplemental FAQ: [VMSA-2026-0006 FAQ](https://brcm.tech/vmsa-2026-0006)
- The Hacker News summary: [Three critical VMware flaws allow auth bypass, code execution, and VM escape](https://thehackernews.com/2026/07/three-critical-vmware-flaws-allow-auth.html)
