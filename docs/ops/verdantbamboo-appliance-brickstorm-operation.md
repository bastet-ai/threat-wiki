# VerdantBamboo appliance BRICKSTORM operation

## Summary
Volexity reported a VerdantBamboo incident-response case in which the China-nexus actor maintained long-running access on proprietary and edge appliances that often lack normal EDR coverage. The operation centered on BRICKSTORM implants on Linux and FreeBSD appliances, plus PLENET / GRIMBOLT and AGENTPSD fallback malware, and included a likely managed service provider pivot.

Google Cloud / Mandiant separately published vSphere-focused BRICKSTORM defender guidance on June 8, 2026, emphasizing that this activity is not simply a product-vulnerability story: adversaries exploit weak management-plane architecture, flat networks, identity design gaps, enabled shell access, and limited telemetry at the virtualization layer.

## Tags
- ops
- operations
- espionage
- China-nexus
- edge appliances
- MSP
- Linux
- FreeBSD
- pfSense
- Synology
- Egnyte
- VMware
- vSphere
- BRICKSTORM
- PLENET
- AGENTPSD

## Why this matters
- Appliance persistence can sit below normal endpoint visibility. Volexity found BRICKSTORM on Egnyte Storage Sync, pfSense, and legacy Linux systems, and PLENET on a Synology NAS.
- The MSP angle expands incident scope: customer remediation can fail if the service provider still holds compromised credentials, topology knowledge, or appliance access.
- Cloud and SaaS access can be proxied through victim infrastructure. Volexity says VerdantBamboo used BRICKSTORM proxying and compromised credentials to access Microsoft 365 while blending in with expected traffic and bypassing Conditional Access assumptions.
- Mandiant's vSphere guide highlights the same control-plane gap for vCenter Server Appliance and ESXi: compromise of the virtualization layer can undermine every VM it manages, including domain controllers, PAM systems, and backup / recovery tooling.

## Reported chain

### Egnyte Storage Sync appliance
- Volexity began investigating suspicious traffic from a Linux-based Egnyte Storage Sync virtual appliance in September 2025.
- The appliance connected to actor-controlled infrastructure behind Cloudflare and made TLS connections to Google's public DNS service; Volexity later confirmed DNS-over-HTTPS-style behavior.
- VerdantBamboo reportedly accessed the appliance through IP addresses assigned by the victim organization's web SSL VPN.
- Volexity determined the threat actor used valid SSH credentials for the default `egnyteservice` account. The MSP had changed the default password, so Volexity assessed the actor likely obtained the credentials from the MSP.
- The actor abused sudo permissions for vendor-approved commands, including `tee`, to write files that normally required root-level permission.
- BRICKSTORM was launched manually when needed rather than through a long-term persistence mechanism on that appliance.
- VerdantBamboo also modified the Egnyte host-monitor path to establish AGENTPSD as a fallback command-and-control channel if BRICKSTORM stopped working.

### MSP pfSense firewall
- Volexity investigated the victim organization's managed service provider and found suspicious traffic from the MSP network.
- The MSP's pfSense firewall had web shells, cryptocurrency miners, alternate VPN configurations, and a FreeBSD-compatible BRICKSTORM implant.
- Volexity says the pfSense BRICKSTORM implant had persisted through a modified cron file and that compromise evidence went back at least 18 months.
- Volexity assessed with high confidence that VerdantBamboo had root-level compromise of a critical MSP system and with medium confidence that the customer compromise may have happened through the MSP.

### Firewall re-entry and Synology NAS PLENET deployment
- After initial remediation removed the Storage Sync appliance and web SSL VPN path, VerdantBamboo regained access.
- Volexity traced the source to the victim firewall, whose administrative interface was exposed to the internet after the older SSL VPN device was retired.
- VerdantBamboo used stolen administrative credentials without MFA, configured a web SSL VPN network, connected through it, and pivoted internally.
- The actor used administrative credentials to enable SSH on a Synology NAS and deployed PLENET / GRIMBOLT, a Native AOT .NET Core backdoor.
- Volexity found the actor had administrative-level VMware infrastructure credentials and validated them through web logins, but did not observe malware installation on ESXi or vCenter systems in this case.

## Malware and infrastructure notes
- **BRICKSTORM** was VerdantBamboo's primary implant. Volexity describes modular task-based construction, WebSocket / proxy capabilities, and Linux plus FreeBSD variants customized per appliance.
- **PLENET / GRIMBOLT** is a cross-platform .NET Core backdoor compiled with Native AOT, likely selected in part because static analysis tooling for that format is less mature.
- **AGENTPSD** is a Python backdoor compiled to a binary and used as a fallback persistence path.
- Volexity developed a Censys pivot for BRICKSTORM C2 infrastructure based on a small service count, a TLS banner hash, Cloudflare issuer metadata, OpenBSD SSH, and a zero-length HTTP response. Treat the Volexity indicator page as the live reference rather than copying transient infrastructure wholesale.

## Defender heuristics

### Appliance and edge response
- Include appliances, firewalls, NAS, storage-sync systems, and legacy Linux systems in containment scope when suspicious SaaS or VPN access appears to originate from "trusted" infrastructure.
- Review local accounts that bypass MFA, particularly break-glass, service, and vendor-default accounts.
- Hunt for recent SSH enablement, custom VPN profile creation, unexpected cron changes, modified vendor monitor scripts, and binaries written through vendor service accounts.
- Preserve appliance snapshots and logs before rebuilding; many appliances lack full EDR telemetry and local evidence can disappear quickly.
- During customer incident response, validate MSP-controlled credentials, access paths, and appliance management interfaces before declaring eviction complete.

### vSphere control-plane hardening
- Treat vCenter and ESXi as Tier-0 systems when they host domain controllers, PAM tooling, backups, or other privileged workloads.
- Restrict VCSA VAMI (`5480`), SSH (`22`), vSphere Client / API, and ESXi management interfaces to hardened administrative workstations and management networks.
- Enforce phishing-resistant MFA for vCenter web access and limit who can pivot from vCenter administration into the underlying Photon OS shell.
- Disable unnecessary shell access, including ESXi management-account shell paths where supported.
- Forward VCSA, ESXi, auditd, and firewall logs off-host with reliable time sync; do not depend on local appliance logs that an attacker can purge.
- Alert on local account creation and deletion, SSH service enablement, VAMI changes, VM clone/export events, VIB installation, firewall-rule changes, and unexpected outbound C2-like traffic from management appliances.
- Encrypt Tier-0 VMs such as domain controllers, certificate authorities, password vaults, and backup-management systems to reduce silent vSphere-level data exfiltration.

## Related pages
- [VerdantBamboo](../actors/verdantbamboo.md)

## Sources
- Volexity: [https://www.volexity.com/blog/2026/06/04/verdantbamboo-just-another-brickstorm-in-the-firewall/](https://www.volexity.com/blog/2026/06/04/verdantbamboo-just-another-brickstorm-in-the-firewall/)
- Google Cloud / Mandiant vSphere BRICKSTORM defender guide: [https://cloud.google.com/blog/topics/threat-intelligence/vsphere-brickstorm-defender-guide](https://cloud.google.com/blog/topics/threat-intelligence/vsphere-brickstorm-defender-guide)
- The Hacker News summary: [https://thehackernews.com/2026/06/verdantbamboo-deploys-bsd-variant-of.html](https://thehackernews.com/2026/06/verdantbamboo-deploys-bsd-variant-of.html)
