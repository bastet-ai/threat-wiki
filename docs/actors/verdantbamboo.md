# VerdantBamboo

## Summary
VerdantBamboo is Volexity's name for a China-nexus espionage actor that targets edge and appliance systems where endpoint detection and response coverage is limited or unavailable. Volexity maps the cluster to **WARP PANDA** and **UNC5221**; The Hacker News notes overlap with Microsoft's **Clay Typhoon** naming.

Volexity's June 2026 incident-response writeup describes VerdantBamboo maintaining access for at least 18 months across Linux and BSD appliances, including Egnyte Storage Sync, pfSense firewall, Synology NAS, and legacy Linux email infrastructure. The actor used BRICKSTORM as its primary implant and deployed PLENET / GRIMBOLT plus AGENTPSD as additional appliance backdoors.

## Tags
- groups
- China-nexus
- espionage
- edge appliances
- Linux
- FreeBSD
- VMware
- vSphere
- MSP
- BRICKSTORM
- PLENET
- AGENTPSD

## Reported operations and tradecraft

### 2025--2026 appliance persistence and MSP pivot
- Volexity discovered the activity in September 2025 during incident response to suspicious traffic from an Egnyte Storage Sync Linux virtual appliance.
- The appliance contacted actor-controlled infrastructure hidden behind Cloudflare and made TLS connections to Google's public DNS service, which Volexity later confirmed was DNS-over-HTTPS behavior.
- Volexity says VerdantBamboo accessed the appliance through IP addresses assigned by the victim's web SSL VPN and used BRICKSTORM's proxying capability plus compromised credentials to access the victim's Microsoft 365 environment while blending with expected network traffic.
- The investigation found the victim organization's managed service provider had also been compromised. Volexity found a FreeBSD-compatible BRICKSTORM implant on the MSP's pfSense firewall and assessed with medium confidence that the victim may have been compromised through the MSP breach.
- After initial remediation, VerdantBamboo returned by using stolen administrative credentials against the victim firewall, configuring web SSL VPN access, pivoting internally, and deploying PLENET to a Synology NAS.

## Malware families reported by Volexity
- **BRICKSTORM** — primary VerdantBamboo implant observed on Linux and FreeBSD appliances, including a pfSense firewall sample. Volexity describes modular task-based construction, WebSocket / proxying behavior, and customized appliance persistence.
- **PLENET / GRIMBOLT** — cross-platform .NET Core backdoor compiled with Native AOT; Volexity observed it on a Linux-based Synology NAS and Google had previously used the GRIMBOLT name in UNC6201 reporting.
- **AGENTPSD** — Python backdoor compiled to a binary with limited functionality; Volexity assesses with high confidence that it served as a fallback if BRICKSTORM stopped functioning.

## Defender notes
- Treat internet-facing and management-plane appliances as Tier-0 intrusion surfaces when they can proxy into identity, cloud, or virtualization environments.
- Require MFA and network restrictions for local and administrative appliance accounts, not just domain-integrated identities.
- Review managed service provider access paths and appliance credentials during incident response; Volexity's case suggests an MSP compromise may provide the credentials and topology needed to re-enter a customer environment.
- Add appliance-specific persistence review for pfSense cron changes, Synology SSH enablement, modified vendor monitor scripts, unexpected binaries under service-user home directories, and outbound WebSocket / DNS-over-HTTPS traffic to non-vendor destinations.
- For VMware estates, pair this actor profile with Mandiant's vSphere hardening guidance: restrict VAMI / SSH access, forward logs off-host, monitor local account creation and service enablement, and treat vCenter / ESXi logs as Tier-0 evidence.

## Related pages
- [VerdantBamboo appliance BRICKSTORM operation](../ops/verdantbamboo-appliance-brickstorm-operation.md)

## Sources
- Volexity: https://www.volexity.com/blog/2026/06/04/verdantbamboo-just-another-brickstorm-in-the-firewall/
- Google Cloud / Mandiant vSphere BRICKSTORM defender guide: https://cloud.google.com/blog/topics/threat-intelligence/vsphere-brickstorm-defender-guide
- The Hacker News summary: https://thehackernews.com/2026/06/verdantbamboo-deploys-bsd-variant-of.html
