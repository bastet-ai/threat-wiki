# 3CX desktop app compromise

## Tags
- ops
- operations
- supply-chain
- 3CX
- Trading Technologies
- X_TRADER
- ICONICSTEALER
- Windows
- macOS

## Summary
In late March 2023, [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/), [CISA](https://www.cisa.gov/news-events/alerts/2023/03/30/supply-chain-attack-against-3cxdesktopapp), and multiple incident responders disclosed that signed Windows and macOS builds of `3CXDesktopApp` had been trojanized and distributed to customers from 3CX-controlled infrastructure. [Mandiant's April 20, 2023 investigation](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) and [3CX's April 20, 2023 update](https://www.3cx.com/blog/news/mandiant-security-update2/) later said the operation began earlier, when a 3CX employee installed a malicious `X_TRADER` package downloaded from the legitimate Trading Technologies site in 2022, giving the operators a foothold that they used to compromise 3CX build systems.

This page uses the descriptive title `3CX desktop app compromise` because that is the clearest first-party name for the operation. Public reporting also ties the intrusion to [Mandiant's `UNC4736` cluster](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) and to later vendor branding such as [SentinelOne's `SmoothOperator`](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-in-software-supply-chain-attack/), but those labels describe the suspected operator cluster or a vendor campaign brand rather than the victim-facing operation itself.

## Naming and companion-page assessment
- [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/) and [CISA](https://www.cisa.gov/news-events/alerts/2023/03/30/supply-chain-attack-against-3cxdesktopapp) both use descriptive `3CX DesktopApp` wording for the incident.
- [SentinelOne](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-in-software-supply-chain-attack/) branded the campaign `SmoothOperator`.
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) tracks the responsible activity cluster as `UNC4736` and assesses with moderate confidence that it is related to North Korean `AppleJeus` activity.
- No companion `Groups` or `People` page is published in this pass. The public reporting supports the operation strongly, but the actor-alias boundary across `UNC4736`, `AppleJeus`, Lazarus-related reporting, and vendor labels is still too attribution-dependent to collapse into a single durable profile here.

## Timeline
- **2022:** [3CX](https://www.3cx.com/blog/news/mandiant-security-update2/) says the initial compromise began when a 3CX employee installed a trojanized `X_TRADER` package on a personal computer after downloading it from the legitimate Trading Technologies website.
- **2023-03-22:** [SentinelOne](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-in-software-supply-chain-attack/) says it began seeing a spike in behavioral detections for trojanized `3CXDesktopApp` installers on March 22, 2023.
- **2023-03-30:** [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/) disclosed the incident, listed affected Windows and macOS versions, told customers to uninstall the Electron app, and said it had appointed Mandiant to investigate.
- **2023-03-30:** [CISA](https://www.cisa.gov/news-events/alerts/2023/03/30/supply-chain-attack-against-3cxdesktopapp) published a public alert urging defenders to hunt for indicators tied to the trojanized application.
- **2023-04-11:** [3CX](https://www.3cx.com/blog/news/mandiant-initial-results/) published Mandiant's interim findings, including attribution to `UNC4736`, Windows malware `TAXHAUL` and `COLDCAT`, and the macOS build-server backdoor later clarified as `POOLRAT`.
- **2023-04-20:** [3CX](https://www.3cx.com/blog/news/mandiant-security-update2/) and [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) published the reconstructed intrusion chain from the earlier Trading Technologies compromise into 3CX's Windows and macOS build environments.
- **2023-04-20:** [CISA](https://www.cisa.gov/news-events/analysis-reports/ar23-110a) released a malware analysis report on `ICONICSTEALER`, the Windows information stealer used in the 3CX attack chain.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### 3CX
- [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/) said the affected Windows builds were `18.12.407` and `18.12.416`, and the affected macOS builds were `18.11.1213`, `18.12.402`, `18.12.407`, and `18.12.416`.
- The same March 30, 2023 post said 3CX rebuilt and redistributed clean versions, advised customers to uninstall the Electron app, and pushed users toward the PWA client while the investigation was underway.
- [3CX's April 11, 2023 update](https://www.3cx.com/blog/news/mandiant-initial-results/) said the attacker had compromised both Windows and macOS build environments and had used `TAXHAUL`, `COLDCAT`, and a macOS backdoor first described as `SIMPLESEA` and later aligned to `POOLRAT`.

### Trading Technologies / X_TRADER
- [3CX's April 20, 2023 update](https://www.3cx.com/blog/news/mandiant-security-update2/) says the initial compromise path began with a trojanized `X_TRADER_r7.17.90p608.exe` installer downloaded from `download.tradingtechnologies[.]com`.
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) says the `X_TRADER` package was signed with a valid Trading Technologies certificate, was still downloadable in 2022 even though the product had reportedly been retired in 2020, and deployed the `VEILEDSIGNAL` backdoor.
- Mandiant also says this earlier Trading Technologies compromise is what made the 3CX incident a cascading software supply-chain attack rather than a single isolated vendor breach.

### Incident-response and public-defense reporting
- [CISA's March 30 alert](https://www.cisa.gov/news-events/alerts/2023/03/30/supply-chain-attack-against-3cxdesktopapp) acted as the U.S. public-defense coordination point and linked defenders to vendor and partner analysis.
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) reconstructed the full compromise chain, from the earlier `X_TRADER` infection to lateral movement inside 3CX and abuse of the build environment.
- [CISA's `ICONICSTEALER` analysis report](https://www.cisa.gov/news-events/analysis-reports/ar23-110a) documents the Windows infostealer's browser-targeting behavior against Chrome, Edge, Brave, and Firefox.

## Operational chain
1. A trojanized `X_TRADER` installer was made available from Trading Technologies infrastructure and was downloaded by a 3CX employee in 2022, according to [3CX](https://www.3cx.com/blog/news/mandiant-security-update2/) and [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise).
2. That installer deployed `VEILEDSIGNAL`, which gave the operator administrator-level access and persistence on the employee's personal computer and created a path to steal 3CX corporate credentials.
3. [3CX](https://www.3cx.com/blog/news/mandiant-security-update2/) says the earliest evidence inside the 3CX corporate environment appeared through VPN access using those stolen credentials two days after the personal-device compromise.
4. [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) says the threat actor laterally moved through 3CX using tools such as the Fast Reverse Proxy project, then compromised both the Windows and macOS build environments.
5. The operators inserted malicious logic into signed Windows and macOS `3CXDesktopApp` builds. [SentinelOne](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-in-software-supply-chain-attack/) and [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) describe a staged chain in which the app pulled encrypted data from GitHub-hosted icon files and, on Windows, eventually loaded `ICONICSTEALER`.
6. On compromised Windows endpoints, [CISA](https://www.cisa.gov/news-events/analysis-reports/ar23-110a) says `ICONICSTEALER` harvested host details plus browser history and related sensitive parameters from Chrome, Edge, Brave, and Firefox.
7. Once public reporting and AV detections exposed the issue, [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/) pulled the affected builds, pushed replacement packages, and shifted customers toward the PWA client while incident response continued.

## Evidence and impact
- [3CX](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/) confirms the operation reached real customer distribution channels, not just internal build systems; customers were downloading trojanized signed software from 3CX-managed infrastructure.
- [SentinelOne](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-supply-chain-attack/) says the staged chain used GitHub-hosted icon files to hide encrypted C2 data and, in some cases, delivered a third-stage infostealer.
- [CISA](https://www.cisa.gov/news-events/analysis-reports/ar23-110a) says the Windows infostealer targeted browser history and related parameters, turning a vendor compromise into downstream customer data exposure.
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise) calls this the first software supply-chain compromise it had seen that directly led to another software supply-chain compromise.

## Defender takeaways
- Treat developer and build-engineer personal devices as part of the enterprise attack surface if they are used to access corporate VPNs, build systems, or code-signing workflows.
- Separate build, signing, and release infrastructure aggressively. The 3CX case shows how one stolen employee credential path can become a trusted-software distribution event.
- Hunt not just for the trojanized vendor binary, but also for its follow-on infrastructure, including suspicious GitHub content retrieval, icon-file staging, and browser-data theft activity.
- When a signed application is suspected of compromise, remove the affected builds from every distribution point quickly, publish exact affected version numbers, and give users a lower-risk fallback path.
- If upstream compromise is suspected, keep attribution caveats explicit. In this case, the operational chain is clearer than the exact boundary between `UNC4736`, `AppleJeus`, and later vendor branding.

## Sources
- [3CX DesktopApp Security Alert - Mandiant Appointed to Investigate](https://www.3cx.com/blog/news/desktopapp-security-alert-updates/)
- [3CX Security Update Tuesday 11 April 2023 - Interim Assessment Concluded](https://www.3cx.com/blog/news/mandiant-initial-results/)
- [3CX Security Update Thursday 20 April 2023 - Initial Intrusion Vector Found](https://www.3cx.com/blog/news/mandiant-security-update2/)
- [Mandiant: 3CX Software Supply Chain Compromise Initiated by a Prior Software Supply Chain Compromise](https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise)
- [CISA: Supply Chain Attack Against 3CXDesktopApp](https://www.cisa.gov/news-events/alerts/2023/03/30/supply-chain-attack-against-3cxdesktopapp)
- [CISA: MAR-10435108-1.v1 ICONICSTEALER](https://www.cisa.gov/news-events/analysis-reports/ar23-110a)
- [SentinelOne: 3CX SmoothOperator | 3CXDesktopApp in Supply Chain Attack](https://www.sentinelone.com/blog/smoothoperator-ongoing-campaign-trojanizes-3cx-software-in-software-supply-chain-attack/)
