# APT29 / Cozy Bear / Midnight Blizzard

## Tags
- groups
- espionage
- state-linked
- Russia
- cloud
- email
- supply-chain
- credential-theft

## Summary
APT29 is a long-running, publicly tracked espionage group associated with Russian state-linked operations. Public reporting and defensive guidance most often use **APT29**, **Cozy Bear**, and **Midnight Blizzard** as the durable names for this cluster.

## Naming
- **APT29** is the canonical MITRE ATT&CK group label: [G0016](https://attack.mitre.org/groups/G0016/).
- **Cozy Bear** is a common public alias used across vendor and press reporting.
- **Midnight Blizzard** is Microsoft’s recent public label for the same activity cluster.
- MITRE ATT&CK lists additional aliases including **NOBELIUM**, **UNC2452**, **YTTRIUM**, **The Dukes**, **CozyDuke**, **SolarStorm**, **Blue Kitsune**, and **UNC3524**.

## Scope
This page covers the group itself, not any single operation.

Confirmed public reporting ties APT29 to:
- cloud and email compromise
- long-dwell espionage operations
- credential theft and account abuse
- supply-chain-enabled intrusion paths, including the SolarWinds compromise

## Activity and tradecraft
- Uses patient, low-noise intrusion tradecraft with long dwell times.
- Has abused cloud identity and mailbox controls to access target communications.
- Has used compromised accounts, service principals, and device-registration paths to expand access.
- Has relied on supply-chain access and downstream credential abuse in major campaigns.

## Related ops
- [Microsoft Midnight Blizzard mailbox theft from Microsoft](../ops/microsoft-midnight-blizzard-mailbox-theft-from-microsoft.md)
- [Cloudflare / Okta token theft incident](../ops/cloudflare-okta-token-theft-incident.md)
- [0ktapus phishing campaign](../ops/0ktapus-phishing-campaign.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Defender takeaways
- Watch for mailbox-rule abuse, delegated permissions, and unexpected device-registration changes in cloud tenants.
- Treat dormant accounts, service principals, and identity provider controls as high-value intrusion surfaces.
- Supply-chain incidents can become cloud follow-on incidents when attackers reuse stolen access.

## Sources
- MITRE ATT&CK group page: https://attack.mitre.org/groups/G0016/
- CISA AA20-352A: Advanced Persistent Threat Compromise of Government Agencies, Critical Infrastructure, and Private Sector Organizations: https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a
- Microsoft Security Response Center guidance on nation-state activity and SolarWinds-related compromise: https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-0688
- Volexity on Dark Halo / SolarWinds mailbox abuse: https://www.volexity.com/blog/2020/12/14/dark-halo-leverages-solarwinds-compromise-to-breach-organizations/
