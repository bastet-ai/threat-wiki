# CyberAv3ngers

## Summary
**CyberAv3ngers** (also `CyberAveng3rs`, `Cyber Avengers`; `Shahid Kaveh Group` in the 2026 U.S. advisory) is an Iranian state-directed threat actor operating behind a pro-Palestinian hacktivist persona. U.S. government agencies attribute the group to Iran's Islamic Revolutionary Guard Corps **Cyber-Electronic Command (IRGC-CEC)**: CISA, FBI, NSA, EPA and partners in joint advisory [AA23-335A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a) (December 2023, updated December 2024), and again in the six-agency advisory [AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a) (April 2026). MITRE ATT&CK tracks the cluster as [G1027](https://attack.mitre.org/groups/G1027/).

The group's defining activity is opportunistic operational-technology (OT) targeting: compromising internet-exposed programmable logic controllers (PLCs) and IoT/SCADA-adjacent devices, initially with default credentials, later with a custom implant and an unpatchable authentication-bypass exploit. Its impact model is disruption plus defacement and propaganda, not extortion.

## Tags
- actors
- Iran
- IRGC
- IRGC-CEC
- ICS
- OT
- PLC
- water
- energy
- critical infrastructure
- IOCONTROL
- defacement
- faketivism

## Naming and affiliation
- [MITRE ATT&CK G1027](https://attack.mitre.org/groups/G1027/): suspected IRGC-affiliated APT group, active since at least 2020; notes disputed and false early claims of Israeli infrastructure compromise.
- Private-industry names: `Storm-0784` (Microsoft), `Bauxite` (Dragos), `Hydro Kitten`, `UNC5691` (Mandiant), listed as names used for the same or a heavily overlapping cluster in [AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a) context and vendor reporting ([Tenable](https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure), [Orion Policy Institute](https://orionpolicy.org/apt-profile-cyberav3ngers/)).
- [AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a) uses `Shahid Kaveh Group` alongside the CyberAv3ngers name.
- In February 2024 the U.S. Treasury ([OFAC](https://home.treasury.gov/news/press-releases/jy2072)) sanctioned six IRGC-CEC officials for directing or supporting the group's operations: Hamid Reza Lashgarian (IRGC-CEC head), Hamid Homayunfal, Mahdi Lashgarian, Milad Mansuri, Mohammad Amin Saberian, and Mohammad Bagher Shirinkar. The State Department's Rewards for Justice program offers up to $10 million for information on the `Mr. Soul` persona, linked to the group.
- Dragos tracks a heavily overlapping activity cluster as `Bauxite` and links it to the `IOCONTROL` implant while noting the hacktivist persona and the intrusion cluster should not be automatically equated ([IntelFusions summary](https://www.intelfusions.com/threat-actors/cyber-av3ngers)).
- December 2025 leaked internal records reportedly showed structured operational spreadsheets (domain registrations, European VPS hosting, cryptocurrency payments) with administrative overlap to the `Moses Staff` operation ([Tenable](https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure)). Treat the Moses Staff convergence as single-source until independently corroborated.
- Naming caveat: Microsoft's [February 2024 Iran influence report](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/) lists `CyberAvengers` as a distinct Iranian persona from `Handala`/`Moses Staff`. Shared Israel-targeting alone does not merge these clusters; see [Handala](handala.md#naming-and-affiliation).

## Primary motivation
- **Disruption of critical infrastructure**, especially water/wastewater and energy, aligned with Iranian geopolitical objectives, confirmed operational disruption and financial loss at U.S. organizations per [AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a).
- **Propaganda and signaling**: HMI defacement, Telegram claims, and leak-style image drops serve Iranian state messaging; the group presents as hacktivists but is assessed as state-directed.
- Targeting logic has two prongs: Israeli-manufactured technology wherever deployed (Unitronics), and U.S. critical infrastructure as retaliatory targeting ([Orion Policy Institute](https://orionpolicy.org/apt-profile-cyberav3ngers/)).

## Tradecraft
### Access
- Phase 1 (2020-2022): propaganda-heavy persona claiming Israeli power-grid and rail disruptions; [DomainTools-era analysis](https://rss-cybersecurity.ankura.com/cyber-sec-feed-item/threat-profile-cyberavengers) and later reporting found several claims reused imagery from unrelated leaks (including Moses Staff material) to simulate fresh intrusions. Verify claims against victim confirmation.
- Phase 2 (November 2023 - January 2024): mass exploitation of internet-exposed `Unitronics Vision Series` PLCs/HMIs using factory default credentials (`1111`) on default port `20256`. At least 75 devices compromised across the U.S., Israel, UK, and Ireland, at least 34 in the water sector ([AA23-335A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a)).
- Phase 3 (2024): [IOCONTROL](https://claroty.com/team82/research/from-exploits-to-forensics-unraveling-the-unitronics-attack), a custom modular Linux implant for OT/IoT and SCADA-adjacent devices, routers, PLCs, HMIs, firewalls, fuel-management systems (Orpak, Gasboy), IP cameras. Previously tracked as `OrpraCab`/`QueueCat` in 2023.
- Phase 4 (2026): exploitation of `CVE-2021-22681`, a critical authentication bypass in Rockwell Automation Logix controllers with no vendor patch (defense-in-depth mitigations only), across U.S. water, energy, and government facilities ([AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a); [Tenable](https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure)).

### IOCONTROL characteristics
- MQTT over TLS on port `8883` for C2; DNS-over-HTTPS for C2-domain resolution to evade network monitoring
- AES-256-CBC encrypted configuration data
- Persistence via a systemd boot script
- Capabilities include OS command execution, port scanning, and self-deletion
- (per [Rewards for Justice](https://www.state.gov/rewards-for-justice) and Claroty Team82 reporting summarized in [Brandefense](https://brandefense.io/knowledge-hub/apt-groups/cyberav3ngers))

### Proliferation
- CyberAv3ngers' ICS exploitation techniques have proliferated to an estimated 60+ affiliated pro-Iranian hacktivist groups, meaning the technique outlives disruption of the core group ([Tenable, April 2026](https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure)).

## Associated operations
### Confirmed or strongly sourced operations
- **2023-11: Aliquippa, Pennsylvania Municipal Water Authority.** Compromised a Unitronics Vision Series PLC controlling a tank-monitoring booster station; HMI defaced with "You have been hacked, down with Israel. Every equipment 'made in Israel' is CyberAv3ngers legal target." No loss of customer water service ([CISA advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a); [GovTech](https://www.govtech.com/security/bad-password-may-have-led-to-pennsylvania-water-system-hack)).
- **2023-11/12: multi-state Unitronics wave.** 75+ devices across U.S. water, energy, food and beverage, and healthcare sectors plus UK and Ireland victims; one Irish utility left residents without water for several days ([AA23-335A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a)).
- **2023-12: BAZAN Group (Israel) DDoS.** Israel's largest oil refinery operator's website knocked offline; the group leaked claimed SCADA screenshots, which BAZAN and Check Point called fabricated. The incident shows the group's propaganda-to-impact ratio: the DDoS was real, the intrusion claims were not ([BleepingComputer](https://www.bleepingcomputer.com/news/security/israels-largest-oil-refinery-website-offline-after-ddos-attack/)).
- **2024: IOCONTROL campaign** against fuel-management systems and OT/IoT devices across multiple countries (Claroty Team82 / Dragos reporting).
- **2026: Rockwell Logix CVE-2021-22681 campaign** against U.S. government services, water/wastewater, and energy facilities; confirmed operational disruption and financial loss; documented in [AA26-097A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a) (FBI, CISA, NSA, EPA, DOE, U.S. Cyber Command).

### Disputed or unverified claims
- 2020-2021 claims of Israeli power-grid outages (7,500+ interruptions) and railway disruption: no independent corroboration; Israeli officials dismissed them ([Ankura CTIX](https://rss-cybersecurity.ankura.com/cyber-sec-feed-item/threat-profile-cyberavengers)).
- Claimed 2021 Haifa Bay petrochemical fires and 2020 attacks on 28 Israeli railway stations: unverified ([BleepingComputer](https://www.bleepingcomputer.com/news/security/israels-largest-oil-refinery-website-offline-after-ddos-attack/)).

## Defender signals
- Internet-exposed PLCs, HMIs, fuel-management systems, or OT/IoT devices, the group's consistent precondition is reachability, not sophistication
- Unitronics Vision-series devices with default credentials or reachable on TCP `20256`
- Rockwell Automation Logix controllers unmitigated for CVE-2021-22681 (no patch exists; apply defense-in-depth per AA26-097A)
- Outbound MQTT over TLS on port `8883` from OT/IoT hosts; DNS-over-HTTPS from devices that have no business using it
- Unexpected systemd service files on Linux-based OT/IoT devices (IOCONTROL persistence)
- HMI defacement or unexpected content on operator screens, treat as intrusion, not vandalism
- Vendor-agnostic exposure: the group targets Israeli-made equipment anywhere and U.S. infrastructure broadly; device nationality is not a shield

## Notes
- Page title follows MITRE ATT&CK's `CyberAv3ngers` spelling (the leetspeak `3` is standard across CISA advisories and ATT&CK); plain `Cyber Avengers` appears in older reporting.
- Distinguish claimed impact from confirmed impact: the group's early history is propaganda-heavy, and several marquee claims (BAZAN intrusion, grid outages) were fabricated or unverified. Confirmed compromise begins with the November 2023 Unitronics campaign.
- Do not merge with [Handala](handala.md) (MOIS-linked) or Moses Staff despite shared Iran nexus and Israel targeting; IRGC-CEC and MOIS are separate commands. The December 2025 leaked-records overlap claim, if corroborated, would revise this.
- The July 2026 [Iran-linked threat landscape](../notes/iran-linked-threat-landscape-july-2026.md) places this cluster in the "opportunistic OT targeting" mission class alongside `CL-STA-1128`.

## Sources
- CISA/FBI/NSA/EPA/INCD/CCCS/NCSC: IRGC-Affiliated Cyber Actors Exploit PLCs in Multiple Sectors (AA23-335A, Dec 2023, updated Dec 2024): [https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a)
- CISA/FBI/NSA/EPA/DOE/U.S. Cyber Command: Iranian-Affiliated Cyber Actors Exploit Programmable Logic Controllers Across US Critical Infrastructure (AA26-097A, Apr 2026): [https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a)
- U.S. Treasury OFAC: Sanctions on six IRGC-CEC officials (Feb 2024): [https://home.treasury.gov/news/press-releases/jy2072](https://home.treasury.gov/news/press-releases/jy2072)
- MITRE ATT&CK G1027: [https://attack.mitre.org/groups/G1027/](https://attack.mitre.org/groups/G1027/)
- Tenable: What to Know About CyberAv3ngers (2026 campaign context, IOCONTROL detail, proliferation estimate): [https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure](https://tenable.com/blog/what-to-know-about-cyberav3ngers-the-irgc-linked-group-targeting-critical-infrastructure)
- Orion Policy Institute: APT Profile, CyberAv3ngers: [https://orionpolicy.org/apt-profile-cyberav3ngers/](https://orionpolicy.org/apt-profile-cyberav3ngers/)
- Claroty Team82: From Exploits to Forensics, Unraveling the Unitronics Attack (IOCONTROL forensics): [https://claroty.com/team82/research/from-exploits-to-forensics-unraveling-the-unitronics-attack](https://claroty.com/team82/research/from-exploits-to-forensics-unraveling-the-unitronics-attack)
- BleepingComputer: Israel's largest oil refinery website offline after DDoS attack (BAZAN claims/counterclaims): [https://www.bleepingcomputer.com/news/security/israels-largest-oil-refinery-website-offline-after-ddos-attack/](https://www.bleepingcomputer.com/news/security/israels-largest-oil-refinery-website-offline-after-ddos-attack/)
- GovTech/TribLive: Bad Password May Have Led to Pennsylvania Water System Hack (Aliquippa detail): [https://www.govtech.com/security/bad-password-may-have-led-to-pennsylvania-water-system-hack](https://www.govtech.com/security/bad-password-may-have-led-to-pennsylvania-water-system-hack)
- Brandefense: CyberAv3ngers threat group profile (alias crosswalk incl. Shahid Kaveh Group): [https://brandefense.io/knowledge-hub/apt-groups/cyberav3ngers](https://brandefense.io/knowledge-hub/apt-groups/cyberav3ngers)
- Ankura CTIX: Threat Profile, CyberAvengers (early-claims verification history): [https://rss-cybersecurity.ankura.com/cyber-sec-feed-item/threat-profile-cyberavengers](https://rss-cybersecurity.ankura.com/cyber-sec-feed-item/threat-profile-cyberavengers)
