# Handala

## Summary
Handala is the current public-facing persona used in operations that public reporting and U.S. government action tie to the Iranian Ministry of Intelligence and Security (`MOIS`) cluster tracked as `Void Manticore`, `Storm-0842`, `Banished Kitten`, and `Red Sandstorm`. The group pairs destructive intrusions with hack-and-leak publication, doxxing, intimidation, and propaganda. As of [March 19, 2026](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations), the U.S. Justice Department said the `MOIS` used `Handala-Hack[.]to`, `Handala-Redwanted[.]to`, `Karmabelow80[.]org`, and `Justicehomeland[.]org` as part of one shared operational playbook, directly tying Handala to the earlier `Karma` and `Homeland Justice` personas.

This page uses `Handala` as the title because it is the operator-chosen current persona and the clearest durable public name for the cluster's recent Israel- and U.S.-focused activity. Vendor names and older personas are kept inside the page as sourced attribution.

## Tags
- Iran
- MOIS
- faketivism
- wiper
- hack-and-leak
- psychological operations
- transnational repression
- Israel
- Albania
- sabotage

## Primary motivation
- **Disruption / sabotage** against adversary organizations, especially Israeli targets and, by March 2026, at least one U.S.-based medical technologies firm
- **Espionage** and access retention before impact; the cluster steals data, maintains access, and only later wipes or leaks
- **Credential theft** and service-provider compromise to gain repeatable access into victim environments
- Psychological pressure is central to the operation: leak sites, doxxing, threats, and public personas are part of the attack chain rather than mere publicity

## Naming and affiliation
- [Check Point Research](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/) says Handala is an online persona operated by `Void Manticore`, a threat actor affiliated with `MOIS`.
- [Microsoft](https://learn.microsoft.com/en-us/unified-secops/microsoft-threat-actor-naming) maps `Storm-0842` to `Red Sandstorm`, `Banished Kitten`, and `Void Manticore`.
- The [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations) says the seized `Handala`, `Karma`, and `Justicehomeland` domains were all used by `MOIS` and linked through shared leak sites, Iranian IP ranges, and a common operational playbook.
- [Check Point's May 2024 research](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/) says the older Israel-focused persona `Karma` and the Albania-focused persona `Homeland Justice` showed overlapping victims and tradecraft with `Void Manticore`.
- Naming caveat: [Microsoft's February 2024 report](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/) describes separate Iranian personas such as `CyberAvengers` and `Moses Staff`; they should not be merged into Handala just because they also targeted Israel.

## Core tooling and tradecraft
### Access and target development
- Compromised VPN accounts and repeated VPN logon or brute-force attempts against organizations, including IT and service providers, according to [Check Point's March 2026 Handala report](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/)
- Possible target handoff from `Scarred Manticore` / `Storm-0861` into `Void Manticore` destructive phases, per [Check Point](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/) and Microsoft's Albania/Israel context in its [February 2024 report](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/)
- Manual, hands-on intrusion activity rather than heavy custom post-exploitation frameworks

### Lateral movement and control
- Heavy `RDP` use inside victim networks, per [Check Point](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/)
- `NetBird` mesh tunneling in recent intrusions, per [Check Point's March 2026 report](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/)
- Group Policy and scheduled tasks to fan out destructive payloads across the environment

### Impact and intimidation
- Custom Windows and Linux wipers, including the `BiBi` family and later `Handala`-branded components, according to [Microsoft](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/), [CISA/FBI](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-264a), and [Check Point](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/)
- PowerShell-based wiping and file deletion, including one script [Check Point](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/) assesses was likely AI-assisted
- Leak sites, public persona websites, social channels, bulk messaging, doxxing, and direct death threats, as described by the [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations)

## Team dynamics / operating style
- State-aligned but deniable `faketivist` packaging: hacktivist branding wraps state-directed objectives, as described by the [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations)
- Not stealth-first: the cluster often keeps access long enough to steal data, then shifts into noisy leak or wipe phases
- Relatively simple tooling, but coordinated sequencing: initial access, credential use, data theft, destructive deployment, and public intimidation
- Growing willingness to mix state activity with criminal tooling and underground services, according to [Check Point's March 2026 cyber-crime overlap report](https://research.checkpoint.com/2026/iranian-mois-actors-the-cyber-crime-connection/)

## Associated operations
### Confirmed or strongly sourced operations
- **2022-07 / 2022-09: Albania government attacks under `Homeland Justice`.** [CISA and FBI](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-264a) say Iranian state actors identifying as `HomeLand Justice` launched destructive attacks against Albanian government networks after maintaining access for about 14 months.
- **2023-10: `BiBi` wiper attack in Israel.** [Microsoft](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/) says `Storm-0842` deployed the `BiBi` wiper at an Israeli organization in late October 2023, amid collaboration with other `MOIS`-linked groups.
- **2023-11 onward: `Karma` leak-and-wipe campaign against Israeli organizations.** [Check Point](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/) says `Karma` emerged soon after the war began, posed as "anti-Zionist Jewish hackers," and overlapped heavily with `Void Manticore` and `Scarred Manticore` victim sets.
- **Late 2023 onward: `Handala` becomes the dominant public persona.** [Check Point](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/) says Handala was used extensively from late 2023 and likely replaced `Karma` as the main Israel-facing brand.
- **2026-03: U.S.-based medical technologies attack plus doxxing and death threats.** The [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations) says `Handala-Hack[.]to` was used to claim credit for a March 2026 destructive malware attack on a U.S.-based multinational medical technologies firm, while `Handala` sites and email accounts were also used to publish personally identifiable information, threaten IDF- and Israeli-government-linked individuals, and send bounty-backed death threats to dissidents and journalists.

### Publicly claimed activity that should be treated cautiously
- **2024-04: radar-system and mass-text claims.** Public reporting on Handala's claim to have hacked Israeli radar systems and sent large numbers of threatening SMS messages also noted problems in the screenshots the group published, including default coordinates, so this is better treated as a psychological-operation claim than a confirmed infrastructure compromise. See [Cyber Daily's April 15, 2024 report](https://www.cyberdaily.au/security/10427-iranian-hackers-claim-israeli-radar-hack-sends-citizens-text-threats).
- **2025-01: kindergarten emergency-button / PA disruption.** Reporting quoting Israel's National Cyber Directorate said a breached private supplier's system was used to broadcast alarm sounds and terror-supporting audio in several kindergartens; Handala claimed responsibility. This looks like a real downstream impact via a supplier compromise, but public sourcing is still thinner than the Albania, `BiBi`, and March 2026 cases. See [The Jerusalem Post's January 27, 2025 report](https://www.jpost.com/israel-news/article-839386).

## Affiliations and operational relationships
- **`MOIS` / Iranian state nexus:** supported by the [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations), [Check Point](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/), and Microsoft's `Storm-0842` mapping in [Microsoft Learn](https://learn.microsoft.com/en-us/unified-secops/microsoft-threat-actor-naming)
- **`Scarred Manticore` / `Storm-0861`:** [Check Point](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/) describes apparent victim handoff from the more access-oriented actor into `Void Manticore` destructive phases; Microsoft's [Albania and Israel reporting](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/) is consistent with that division of labor
- **Possible overlap with other `MOIS` actors:** [Microsoft](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/) says `Storm-1084` may also have had access in one Israeli case where `Storm-0842` deployed `BiBi`
- **Criminal ecosystem ties:** [Check Point](https://research.checkpoint.com/2026/iranian-mois-actors-the-cyber-crime-connection/) says `Void Manticore` increasingly relies on criminal tooling, services, and operational models to support state aims

## Motivations and messaging
- The cluster's public messaging frames attacks as retaliation for Israeli actions and as support for the "Axis of Resistance"; the [Justice Department](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations) quotes a March 11, 2026 Handala claim saying the U.S. medtech attack was retaliation for "ongoing cyber assaults against the infrastructure of the Axis of Resistance."
- The observed behavior goes beyond protest branding. The combination of wipers, leak sites, doxxing, and death threats fits a coercive state-backed campaign focused on disruption, fear, and reputational pressure.
- Unlike financially motivated ransomware groups, Handala's public operations are not centered on payment collection. Even when it borrows criminal tradecraft or underground tooling, the operational effect is political coercion and intimidation.

## Named people
Public reporting names possible supervisors and individual officials behind related `MOIS` activity, but the sourcing in hand is still better suited to a group page than to a standalone `People` page. No `People` companion page is published in this pass.

## Defender signals
- Sudden VPN logon or brute-force noise from commercial VPN nodes or unusual residential or Starlink egress points
- Hands-on `RDP` activity across multiple hosts at once
- `NetBird` installation on compromised systems without a business reason
- Group Policy logon scripts or scheduled tasks distributing wipe components
- Simultaneous use of multiple deletion and wiping mechanisms to maximize impact
- Leak-site publication and direct email threats timed around destructive activity
- Hacktivist-style branding that tries to disguise a state-backed intrusion

## Notes
- Use `Handala` as the page title for current activity because it is the operator-chosen public persona.
- Keep older personas `Karma` and `Homeland Justice` inside the same lineage only when the source explicitly supports that linkage.
- Do not collapse `Handala` into unrelated Iranian personas such as `CyberAvengers`; shared targeting alone is not enough.

## Sources
- [U.S. Department of Justice: Justice Department Disrupts Iranian Cyber Enabled Psychological Operations](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations)
- [Microsoft: Iran surges cyber-enabled influence operations in support of Hamas](https://www.microsoft.com/en-sg/security/security-insider/intelligence-reports/iran-surges-cyber-enabled-influence-operations-in-support-of-hamas/)
- [Microsoft Learn: How Microsoft names threat actors](https://learn.microsoft.com/en-us/unified-secops/microsoft-threat-actor-naming)
- [Check Point Research: Bad Karma, No Justice: Void Manticore Destructive Activities in Israel](https://research.checkpoint.com/2024/bad-karma-no-justice-void-manticore-destructive-activities-in-israel/)
- [Check Point Research: "Handala Hack" - Unveiling Group's Modus Operandi](https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/)
- [Check Point Research: Iranian MOIS Actors & the Cyber Crime Connection](https://research.checkpoint.com/2026/iranian-mois-actors-the-cyber-crime-connection/)
- [CISA/FBI: Iranian State Actors Conduct Cyber Operations Against the Government of Albania](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-264a)
- [Cyber Daily: Iranian hackers claim Israeli radar hack, send citizens text threats](https://www.cyberdaily.au/security/10427-iranian-hackers-claim-israeli-radar-hack-sends-citizens-text-threats)
- [The Jerusalem Post: Iranian hackers broadcast rocket sirens, pro-terror songs at 20 kindergartens](https://www.jpost.com/israel-news/article-839386)
