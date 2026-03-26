# Dragonfly

## Tags
- groups
- espionage
- critical-infrastructure
- energy-sector
- ICS
- Russia
- watering-hole
- spearphishing

## Summary
Dragonfly is a long-running intrusion group tracked publicly under multiple names, including **Energetic Bear** and **Crouching Yeti**. Public reporting ties the group to repeated targeting of energy and other critical-infrastructure sectors, with staging-target tradecraft that often uses third-party organizations as pivots into intended victims.

## Naming
- **Dragonfly** is the primary title used by [MITRE ATT&CK](https://attack.mitre.org/groups/G0035/).
- **Energetic Bear** and **Crouching Yeti** are common alternate names used in public reporting and vendor writeups.
- MITRE also lists aliases including **TEMP.Isotope**, **DYMALLOY**, **Berserk Bear**, **TG-4192**, **IRON LIBERTY**, **Ghost Blizzard**, and **BROMINE**.

## Scope
This page focuses on the group itself, not on any single campaign.

Confirmed public reporting shows Dragonfly activity against:
- energy-sector organizations
- other critical-infrastructure sectors
- staging targets used to reach intended victims

## Activity and tradecraft
- Uses spearphishing and watering holes as part of multi-stage intrusion campaigns.
- Has used compromised third-party organizations as staging points and malware repositories.
- Has targeted ICS-adjacent information and network access inside victim environments.
- Publicly documented activity includes reconnaissance, credential gathering, lateral movement, and collection of ICS-related information.

## Defender takeaways
- Third-party suppliers can become the initial foothold for a downstream intrusion.
- Energy and ICS-adjacent environments should treat website content, email, and remote access paths as potential staging surfaces.
- Watch for watering-hole infrastructure and spearphishing that leverage trusted relationships.

## Sources
- MITRE ATT&CK group page: https://attack.mitre.org/groups/G0035/
- CISA/FBI alert on Russian government activity targeting energy and other critical infrastructure sectors: https://www.cisa.gov/news-events/alerts/2018/03/15/russian-government-cyber-activity-targeting-energy-and-other-critical-infrastructure-sectors
- Symantec reporting referenced by CISA: https://www.symantec.com/connect/blogs/dragonfly-western-energy-sector-targeted-sophisticated-attack-group
