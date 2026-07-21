# Iran-linked threat landscape: access optionality and evidence quality

## Summary
SentinelLABS' July 21, 2026 midyear assessment reframes the Iran-linked cyber threat around **access plus mission plus dependency**, rather than public personas or claim volume. Its central judgment is that the near-term base case remains persistent espionage and access development, accompanied by persona-led coercion and lower-impact opportunistic activity—not a synchronized national-scale destructive campaign.

The durable defender lesson is **access optionality**: a compromised identity, cloud account, service provider, remote monitoring and management (`RMM`) agent, or trusted administrator can support collection today and selective disruption later as tasking changes. Existing access does not by itself prove pre-positioning or a software supply-chain compromise; downstream builds, updates, customers, or distribution must be shown to be affected before applying that label.

## Tags
- Iran
- threat landscape
- access optionality
- espionage
- destructive operations
- hack-and-leak
- persona operations
- identity compromise
- cloud compromise
- RMM abuse
- service providers
- supply-chain attribution
- OT
- ICS
- evidence quality
- incident response
- MOIS
- IRGC
- Void Manticore
- Handala
- MuddyWater
- Seedworm
- Screening Serpens
- APT42
- Cavern Manticore
- CyberAv3ngers
- TAG-182
- MarkiRAT

## Mission-based working taxonomy
SentinelLABS explicitly presents this as a working crosswalk, not proof that every name is a one-to-one alias or that every organizational relationship is settled.

| Public cluster or labels | Assessed mission / relationship |
|---|---|
| Void Manticore; Red Sandstorm; Storm-0842; Banished Kitten; TAG-145; personas Handala, Homeland Justice, and Karma/KarmaBelow80 | MOIS-linked destructive, hack-and-leak, coercive, and influence operations through public personas |
| MuddyWater / Seedworm / Boggy Serpens / Mango Sandstorm | MOIS-subordinate espionage and access enablement |
| APT34 / OilRig / Hazel Sandstorm / Evasive Serpens | Persistent regional espionage commonly associated with MOIS |
| Screening Serpens / UNC1549 / Smoke Sandstorm / Nimbus Manticore; Iranian Dream Job campaign | Recruitment-themed espionage aligned with IRGC strategic priorities |
| APT42; cross-referenced as Agent Serpens and Educated Manticore | IRGC Intelligence Organization-linked high-trust social engineering and cloud collection |
| Cavern Manticore | Service-provider and RMM-enabled espionage; MOIS relationship remains a moderate-confidence, single-vendor assessment |
| TAG-182 | Surveillance of dissidents and diaspora; Ferocious Kitten, Domestic Kitten/GreenEcho, and Rampant Kitten are related reporting contexts, not aliases |
| CyberAv3ngers / Storm-0784 / CL-STA-1128 | IRGC Cyber-Electronic Command-affiliated opportunistic OT targeting |
| Predatory Sparrow / Gonjeshke Darande | Comparison case only: destructive anti-Iran operations widely reported as Israel-linked, not an Iran-linked cluster |

Mission is the safer organizing principle: persistent espionage and access enablement; destructive or coercive persona operations; high-trust social engineering and cloud compromise; dissident surveillance; and opportunistic OT targeting.

## Access optionality
Public 2026 cases illustrate why existing authority is often more important than a novel exploit:

- **Seedworm / MuddyWater** obtained access before the wider conflict to organizations including a U.S. bank, airport, nonprofits, and the Israeli operation of a U.S. software supplier. Public reporting showed backdoors and attempted commercial-cloud exfiltration, but not downstream build or update compromise.
- **Screening Serpens** continued tailored recruitment operations while introducing new RAT variants and AppDomainManager hijacking. Increased tempo does not mean the conflict created the actor's espionage mission.
- **APT42** targeting of journalists, researchers, NGOs, academics, activists, and government-linked individuals demonstrates that high-trust people and their cloud accounts are part of the enterprise perimeter.
- **Cavern Manticore** reporting shows how already-authorized RMM and service-provider pathways can become intrusion paths. SentinelLABS emphasizes that SysAid itself was not compromised and no SysAid vulnerability was involved in that activity.

Do not infer original intent from later geopolitical use. Ask what authority the foothold grants now: intelligence collection, impersonation, downstream targeting, broad administrative action, or disruption.

## Persona operations are infrastructure
Handala, Homeland Justice, and Karma are better modeled as related fronts in a common MOIS-linked persona system than as interchangeable strict aliases. Public personas can provide:

- attribution masking and deniable branding;
- leak and doxxing infrastructure;
- coercion, threats, and direct approaches to employees;
- narrative control while responders are still scoping impact; and
- amplification of technical effects or unverified claims.

Direction, alignment, collaboration, access brokerage, and claim amplification are not synonyms. A persona can amplify another party's claim without proving shared organization. Technical findings and actor-claimed device, data-loss, or operational-impact numbers should remain separate in incident reporting.

## OT evidence ladder
SentinelLABS recommends increasing the evidentiary threshold as a cyber-physical claim becomes stronger:

1. **Provenance and target validation:** establish organization, system, location, and timeframe.
2. **Interface visibility:** confirm that the actor can display an interface.
3. **Authenticated interaction:** show live navigation or current-value queries.
4. **Write or control capability:** prove a setting, logic file, mode, or command can be changed.
5. **Process effect:** verify an operational change outside the interface.
6. **Physical or safety consequence:** independently verify real-world impact.

A screenshot of an HMI or PLC page is not evidence of process manipulation. Logs, engineering review, process data, timestamps, configuration changes, operator testimony, and independently confirmed outcomes should support stronger claims. This analytic caution does not reduce the urgency of closing exposed control paths.

## Defender priorities
### Enterprise and identity
- Inventory old access that predates escalation: privileged identities, service accounts, cloud sessions, RMM agents, identity providers, support organizations, and third-party administrators.
- Use phishing-resistant MFA and conditional access for high-trust people and administrative paths; revoke stale sessions and credentials rather than only changing passwords.
- Review RMM deployment authority and alert on unexpected packages, scripts, or child processes delivered through legitimate management systems.
- Map shared dependencies. Determine which nominally separate services and recovery paths rely on the same identity provider, carrier, administrator, management plane, or service provider.
- Preserve identity, cloud, RMM, service-provider, endpoint, and egress telemetry before containment removes the evidence needed to distinguish access from impact.

### Persona-led incident response
- Run technical response, legal review, communications, executive protection, and employee physical-safety support in parallel; publication and doxxing may begin before scoping is complete.
- Record separately what the victim, responders, government sources, and actor persona each confirm or claim.
- Do not let a public logo or claimed affiliation replace intrusion-level attribution evidence.

### OT and recovery
- Remove direct internet exposure from PLCs, HMIs, and engineering services.
- Put remote access behind authenticated gateways with phishing-resistant MFA, source/time restrictions, and explicit vendor approval.
- Restrict programming-mode and logic changes; monitor engineering workstations and industrial protocols.
- Maintain offline project files and known-good configurations.
- Test whether recovery depends on the same identity, virtualization, management, communications, or administrative environment as production.

## Outlook and analytic boundaries
SentinelLABS assesses with high confidence that continued espionage, credential theft, mailbox and cloud compromise, recruitment lures, trusted-service abuse, and inflated public claims are the near-term base case. It assesses with moderate confidence that selective disruption becomes more likely when usable access, political or symbolic value, and achievable effects coincide.

The report treats a coordinated campaign to disable the U.S. power grid or multiple critical sectors simultaneously as a lower-likelihood, high-impact contingency. It identified no public evidence, as of July 21, of the synchronized access, specialized preparation, and cross-sector execution needed to support claims of an imminent nationwide grid-down operation.

## Related pages
- [Handala](../actors/handala.md)
- [Seedworm / MuddyWater](../actors/seedworm-muddywater.md)
- [Screening Serpens](../actors/screening-serpens.md)
- [Cavern Manticore](../actors/cavern-manticore.md)
- [Cavern](../tools/cavern.md)
- [Oman government Iranian-nexus webshell C2](../ops/oman-government-iranian-nexus-webshell-c2.md)

## Sources
- SentinelLABS: [https://www.sentinelone.com/labs/iran-war-cyber-threat-landscape-a-midyear-assessment-on-what-matters/](https://www.sentinelone.com/labs/iran-war-cyber-threat-landscape-a-midyear-assessment-on-what-matters/)
- U.S. Department of Justice: [https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations](https://www.justice.gov/opa/pr/justice-department-disrupts-iranian-cyber-enabled-psychological-operations)
