# Screening Serpens

## Summary
**Screening Serpens** is an Iran-nexus cyberespionage actor also tracked publicly as **UNC1549**, **Smoke Sandstorm**, and **Iranian Dream Job**. Unit 42's May 2026 reporting says the group targeted technology-sector professionals and organizations tied to aerospace, defense manufacturing, telecommunications, and adjacent high-value sectors, using highly tailored recruitment and meeting lures.

Unit 42 observed a February-April 2026 activity surge after the regional conflict that began on February 28, 2026. The campaign included six newly discovered RAT variants grouped into **MiniUpdate** and **MiniJunk V2**, with suspected targeting in the U.S., Israel, the United Arab Emirates, and other Middle Eastern entities.

## Tags
- Iran
- APT
- espionage
- social engineering
- recruitment lures
- DLL sideloading
- AppDomainManager
- RAT
- MiniUpdate
- MiniJunk

## Primary motivation
- **Espionage** against high-value technology, aerospace, defense, telecommunications, and regional strategic targets.
- **Credential and data theft** through targeted malware delivery rather than broad commodity infection.
- **Operational resilience** through per-target infrastructure segmentation and rapidly adjusted payload variants.

## Naming and affiliation
- Unit 42 names the cluster `Screening Serpens` and maps aliases including `UNC1549`, `Smoke Sandstorm`, and `Iranian Dream Job`.
- Check Point previously reported related activity as a Western Europe expansion under the `Nimbus Manticore` naming context.
- Keep this page distinct from other Iranian personas such as Handala / Void Manticore unless a source explicitly links the operations.

## Core tooling and tradecraft
### Social engineering
- Personalized recruitment lures and job-requisition PDFs aimed at technical personnel.
- Fake application portals or technical assessments, including nested archives such as `Hiring Portal.zip`.
- Video-conferencing or meeting-themed lures in some March 2026 activity.
- Brand impersonation without necessarily compromising the impersonated company's infrastructure.

### Execution and defense evasion
- DLL sideloading remains a core execution path.
- Unit 42 highlights first-seen fusion of Screening Serpens' DLL sideloading playbook with **AppDomainManager hijacking**, manipulating .NET initialization through legitimate configuration files so payloads can run early and interfere with application security mechanisms.
- C2 is segmented by target or variant, often using three to five unique domains per victim set and cloud-hosted infrastructure such as Azure-hosted domains.

### Malware families
- **MiniUpdate:** named from the internal `UpdateChecker.dll` file name. Unit 42 observed March 2026 U.S. and Israel samples and April 2026 UAE / Middle East samples. Later variants added capabilities such as chunked file exfiltration while rotating C2 domains.
- **MiniJunk V2:** an evolved iteration of the MiniJunk family previously reported in Screening Serpens activity, observed in February and March 2026 samples.

## 2026 campaign timeline
- **Late 2025:** public reporting described expansion into Western European targets.
- **Mid-February 2026:** Unit 42 found indications of payload delivery to a Middle Eastern target.
- **March 26-27, 2026:** Unit 42 identified samples uploaded from U.S. and Israeli contexts, including MiniUpdate and MiniJunk V2 activity.
- **April 15-17, 2026:** additional MiniUpdate samples appeared from UAE and another Middle Eastern context.
- **May 22, 2026:** Unit 42 published consolidated analysis of MiniUpdate, MiniJunk V2, per-target infrastructure, and AppDomainManager hijacking.

## Defender signals
- Recruitment-themed archives containing nested payload archives and role-specific PDFs.
- Unexpected execution of signed or legitimate Windows binaries loading nearby unsigned DLLs.
- `.config` files or AppDomainManager-related settings appearing beside .NET executables where they are not expected.
- Azure App Service, OnlyOffice, Filemail, or lookalike business-domain traffic from endpoints that just opened recruiting, meeting, or assessment artifacts.
- RAT C2 segmentation: multiple low-volume domains per suspected target rather than one high-volume commodity C2 endpoint.
- File names and components surfaced by Unit 42, including `UpdateChecker.dll`, `uevmonitor.dll`, `unbcl.dll`, `Connection.dll`, and lure names such as `Hiring Portal.zip`.

## Notes
- Treat the Unit 42 campaign as durable actor intelligence because it adds new malware-family names, execution tradecraft, regional targeting, and defensive pivots.
- Avoid over-indexing on single IOCs: Unit 42's main defensive lesson is behavioral detection for DLL sideloading plus AppDomainManager hijacking.

## Related pages
- [Handala](handala.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/tracking-iran-apt-screening-serpens/](https://unit42.paloaltonetworks.com/tracking-iran-apt-screening-serpens/)
- Check Point: [https://research.checkpoint.com/2025/nimbus-manticore-deploys-new-malware-targeting-europe/](https://research.checkpoint.com/2025/nimbus-manticore-deploys-new-malware-targeting-europe/)
- Google Cloud: [https://cloud.google.com/blog/topics/threat-intelligence/unc1549-iranian-threat-actor-targets-aerospace-defense](https://cloud.google.com/blog/topics/threat-intelligence/unc1549-iranian-threat-actor-targets-aerospace-defense)
- Microsoft Security Insider: [https://www.microsoft.com/en-us/security/security-insider/threat-actors/smoke-sandstorm](https://www.microsoft.com/en-us/security/security-insider/threat-actors/smoke-sandstorm)
