# Pakistani law enforcement espionage convergence

## Summary
SentinelOne's July 9, 2026 report describes sustained cyberespionage against Pakistani law enforcement organizations from February 2024 through April 2026. The durable signal is not just one intrusion: multiple suspected China- and India-nexus operations converged on the same victim class, with Balochistan Police appearing across PlugX, ShadowPad, Cobalt Strike, and Remcos-linked activity windows.

The most sensitive exposure reported by SentinelOne was at Balochistan Police, where affected assets included network appliances and web applications handling biometric records, hotel and tenant registrations tied to national identity records, criminal case files, personnel records, and citizen-facing complaint workflows. SentinelOne also reports a suspected China-nexus compromise of a Complaint Management System portal that hosted `cms_plugin.exe` implants in a `/client scripts/` path, turning a public/police digital-services portal into a malware-delivery surface.

## Tags
- ops
- espionage
- Pakistan
- Balochistan Police
- law enforcement targeting
- China-nexus
- India-nexus
- TAG-179
- Mysterious Elephant
- APT-C-08
- Bitter
- PlugX
- ShadowPad
- Cobalt Strike
- Remcos
- AsyncRAT
- web application compromise
- police digital services
- citizen portal compromise
- biometric records
- national identity records
- SentinelOne

## Why this matters
- Domestic security and police platforms can become foreign-intelligence targets when they hold case, identity, personnel, and citizen-interaction data that reveals internal security posture.
- The same police organization attracting both partner-state and adversary-state collection is a warning sign for agencies that support national-security, immigration, biometric, or critical-infrastructure protection workflows.
- Hosting implants from a police web portal expands blast radius beyond server compromise: police personnel and citizens using the portal can become downstream malware targets.
- Commodity or shared tooling such as Cobalt Strike and Remcos can coexist with China-nexus staples such as PlugX and ShadowPad; defenders should separate tooling-based clusters from attribution claims.

## Reported activity windows
SentinelOne grouped command-and-control traffic to Pakistani law enforcement infrastructure into four tooling clusters:

| Cluster | C2 servers | First seen | Last seen |
| --- | --- | --- | --- |
| PlugX | `172.111.233[.]36`, `172.111.233[.]96`, `172.111.233[.]12`, `172.111.233[.]105`, `172.111.233[.]26`, `172.94.9[.]49`, `172.94.9[.]43`, `172.94.9[.]19`, `45.74.6[.]17` | 2024-02-27 | 2024-09-28 |
| ShadowPad | `45.125.32[.]218` | 2024-11-05 | 2024-11-29 |
| Cobalt Strike | `142.171.183[.]8`, `193.42.25[.]65` | 2024-10-12 | 2025-12-05 |
| Remcos | `89.31.121[.]220` | 2026-01-13 | 2026-04-09 |

SentinelOne assesses the PlugX and ShadowPad victimology as consistent with China-aligned collection across government, foreign-affairs, defense, NGO, and research entities in South, Southeast, Central, and East Asia, the Arabian Peninsula, and Southeast Europe. The Remcos cluster is attributed to a suspected India-nexus actor tracked by Recorded Future as **TAG-179**, with overlap to clusters Kaspersky tracks as **Mysterious Elephant** and Qihoo 360 tracks as **APT-C-08 / Bitter**.

## Portal implant activity
SentinelOne reports three notable `cms_plugin.exe` findings around the Balochistan Police Complaint Management System:

- Two `cms_plugin.exe` samples were uploaded to `cms.balochistanpolice[.]gov[.]pk/client%20scripts/` in late 2024.
- One Rust stager downloaded a next stage from `193.42.25[.]65` and executed it; SentinelOne could not retrieve the next stage at analysis time.
- One .NET executable masqueraded as `360Safe.exe`, reflectively loaded an AsyncRAT client, and used `41.216.188[.]140` as C2.
- The AsyncRAT assembly contained the PDB path `D:\codedome\case\six\Client\Client2\obj\Debug\Client2.pdb`.
- SentinelOne's pivots on the `D:\codedome` prefix found related samples with shared implementation patterns, pinyin terms in PDB paths, and simplified-Chinese log messages, supporting the Chinese-speaking developer assessment for that sample set.
- A third similar `cms_plugin.exe` stager also downloaded from `193.42.25[.]65`.
- The stagers displayed `Update Complete! Please refresh the page`, consistent with a fake portal-update prompt aimed at police users, citizen complainants, or both.

## Defender guidance
- Treat law-enforcement, immigration, court, public-safety, biometric, and citizen-service portals as high-value national-security systems even when they look like ordinary web applications.
- Hunt web roots and upload directories for executable content, especially paths resembling static assets or client scripts that should not host PE, .NET, Rust, archive, or script payloads.
- Review web-server, proxy, EDR, and download telemetry for access to `cms_plugin.exe`, `360Safe.exe` masquerading, `Update Complete! Please refresh the page` prompts, and unusual downloads from police or government portals.
- Correlate inbound portal exploitation with outbound C2 to the PlugX, ShadowPad, Cobalt Strike, Remcos, and AsyncRAT infrastructure listed by SentinelOne.
- Preserve portal access logs, filesystem timestamps, deployment records, IAM changes, web-shell traces, and reverse-proxy logs before remediation; citizen-facing malware delivery needs downstream victim-notification analysis.
- For police and government environments, separate public web applications from biometric, criminal-case, personnel, and national-identity systems with explicit network segmentation and monitored service accounts.
- Do not collapse the activity into one actor solely because it hit the same target. Track China-nexus, India-nexus, and commodity-tool clusters independently unless infrastructure, malware, or operational evidence links them.

## Indicators
### IP addresses
- `142.171.183[.]8` — Cobalt Strike C2
- `172.111.233[.]105` — PlugX C2
- `172.111.233[.]12` — PlugX C2
- `172.111.233[.]26` — PlugX C2
- `172.111.233[.]36` — PlugX C2
- `172.111.233[.]96` — PlugX C2
- `172.94.9[.]19` — PlugX C2
- `172.94.9[.]43` — PlugX C2
- `172.94.9[.]49` — PlugX C2
- `193.42.25[.]65` — Cobalt Strike C2 / `cms_plugin.exe` staging
- `41.216.188[.]140` — AsyncRAT C2
- `45.125.32[.]218` — ShadowPad C2
- `45.74.6[.]17` — PlugX C2
- `89.31.121[.]220` — Remcos C2

### SHA-1 hashes
- `000fad96a85dd6933c22d3dbec9aed47b7f1f066` — TAG-179 backdoor launcher
- `08570471f39bb6725f07b8cddbea99ed48c22686` — TAG-179 backdoor launcher
- `23f4766c011d193f076dfc735dc460e2a41ead79` — TAG-179 backdoor launcher
- `23f6781919a50b118d8d4e6a7e9ae63b71ecc885` — `cms_plugin.exe`
- `2bab40c55637398f0497cff9c8cbea564d595c7f` — TAG-179 lure file
- `4039454c9189e64285e93fc075a30b93f814b5b5` — `cms_plugin.exe`
- `47f8cb0c2dcf62702f58cfc1603d6325755f6820` — TAG-179 backdoor launcher
- `539bd79fbb684edea94eb37518134b97e94b9dd8` — TAG-179 lure file
- `58cb2d95063b9df807b7aa8dc106b74ce988a491` — `cms_plugin.exe`
- `5d60ff36ff519c2e13e7f66cfa0bb46be79592a7` — TAG-179 backdoor
- `63b88d00331de88af696dfb7a896935d830e485f` — TAG-179 backdoor
- `6fe2e74d009abbd56de01fd7404a1245e9b47c79` — TAG-179 lure file
- `71757adba833b46f961e840d0f055bcce0b529c4` — TAG-179 lure file
- `8c329db96e093fa25268e078405a33c518dbb5c9` — TAG-179 backdoor
- `c6c197e61079a0a33108c2c87b5e3c7056a138ec` — TAG-179 lure file
- `d66ab0cd2e44dc8389c111b7ed34c7bcb0b35311` — TAG-179 backdoor

### URL
- `https[://]cms.balochistanpolice[.]gov[.]pk/client%20scripts/cms_plugin.exe` — implant-hosting URL on the Balochistan Police CMS portal

## Related pages
- [UAT-7810 LONGLEASH ORB network expansion](uat-7810-longleash-orb-network.md)
- [Operation DragonReturn India tax-season DcRAT campaign](operation-dragonreturn-india-tax-dcrat.md)
- [Operation GriefLure Southeast Asia LNK dropper](operation-grieflure-southeast-asia-lnk-dropper.md)
- [Stock exchange executive mailbox espionage](stock-exchange-executive-mailbox-espionage.md)

## Sources
- SentinelOne SentinelLABS: <https://www.sentinelone.com/labs/one-target-china-india-espionage-converge-on-pakistani-law-enforcement/>
