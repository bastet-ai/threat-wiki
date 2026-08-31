# QTFY: FBI/DoJ seizure of QScan and QTRouter PRC infrastructure targeting U.S. critical infrastructure

## Summary

On August 26, 2026, the U.S. Department of Justice and FBI announced **court-authorized domain seizures** (Southern District of California) of two complementary hacking platforms, **QScan** and **QTRouter**, operated by a PRC state-sponsored group known as **QTFY**. Court documents describe QTFY as being employed by **Nanjing Xinjiuwei Network Technology Company** and offering computer hacking services to paying customers that include the **PRC Ministry of State Security (MSS)** and the **People's Liberation Army (PLA)**.

Named among the **targets** of QTFY computer intrusion activity are the **NASA, Federal Reserve, Department of Energy, Department of Justice, Department of Health and Human Services, National Institutes of Health, and the U.S. Senate**. (The DoJ initially listed these agencies as *victims* in its August 26 press release; the corrected release, reported by Reuters on August 29–31, 2026, now describes them as "among the targets of QTFY," with DoJ noting edits were made "to ensure this press release accurately reflects the government's allegations in the affidavit in support of the domain seizures." The distinction matters: the broader organization set was *targeted*, but confirmed compromise extends only to a subset.) Lumen Black Lotus Labs, which has tracked the operation for over 18 months and collaborated with the FBI on it for roughly a year, assessed QTFY as active since **May 2018** and targeted across "the western world and beyond," with heavy emphasis on academia and research communities.

The seizure is a *disruption of the enablement layer*, not an indictment of named individuals in this announcement: the seized domains were hard-coded into both QScan and QTRouter malware and used for essential communication and authentication, so seizure functionally degrades the platforms.

## Tags
- ops
- operation
- campaign
- disruption
- infrastructure seizure
- QTFY
- QScan
- QTRouter
- QTBotnet
- China-nexus
- PRC
- Nanjing Xinjiuwei
- Ministry of State Security
- PLA
- critical infrastructure
- government targeting
- academia
- IoT botnet
- proxy obfuscation
- OpenWrt
- Clash proxy
- DDoS
- Lumen Black Lotus Labs
- FBI
- DOJ

## Why this matters
- **State-nexus enablement infrastructure with named high-value targets.** The target list (NASA, Federal Reserve, DOE, DOJ, HHS, NIH, Senate) makes this one of the most explicit PRC critical-infrastructure/government-targeting disruption announcements of 2026. Preserve the corrected targets-not-victims framing: the DoJ's own edit downgraded these agencies from "victims" to "targets," so treat confirmed compromise as a subset of the named set until victim-organization or affidavit detail clarifies scope.
- **The durable artifact is the obfuscation model, not the domains.** QTRouter's architecture (compromised IoT + commercial proxy nodes + leased VPS, custom OpenWrt, Clash node chaining, traffic mixed with legitimate commercial-proxy traffic) is a reusable PRC attribution-evasion pattern. Expect reconstitution under new domains and continued use of commercial proxy services.
- **Hard-coded C2 domains are a double-edged sword for defenders.** Seizure worked *because* the domains were hard-coded; operators will rotate. Monitoring the platform's admin/authentication domains and the `qt-proxy` / `qtproxy` naming family is the right watch, not a static blocklist.
- **QScan's CVE inventory documents the PRC exploitation surface.** The announced exploit list (Ivanti CSA CVE-2024-8190/8963/9380, Fortinet SSL-VPN CVE-2018-13379, Citrix ADC CVE-2019-19781, Exchange CVE-2021-26855, F5 BIG-IP CVE-2020-5902, Kentico CMS CVE-2019-10068, Log4j CVE-2021-44228, Confluence CVE-2023-22515) is a concrete reminder that N-day edge-device and remote-access vulnerabilities remain the primary entry path for this class of actor.

## Platforms and tooling
- **QScan** — IoT scanning and automatic infection platform; adds compromised devices to the QTRouter network and identifies victim-network vulnerabilities.
  - Scanning-task pool: `mq-task.qt-proxy[.]org` (previously `mq-task.qt-team[.]com`)
  - Task results: `mq-result.qt-proxy[.]org` (previously `mq-result.qt-team[.]com`)
  - Worker nodes primarily housed on leased servers located outside China.
- **QTRouter** — obfuscation/proxy network composed of QScan-compromised IoT devices plus commercial proxy service devices and leased VPSs.
  - Runs on routers with custom **OpenWrt** software.
  - Authenticates to administration servers at `www.qtproxy[.]xyz` and `securelink.qtproxy[.]xyz`.
  - Uses **Clash** to establish proxy connections; supports viewing available nodes and chaining nodes together to obfuscate the actor behind malicious activity.
  - Mixes malicious traffic with legitimate traffic on commercial proxy services and uses compromised IoT locations to make communications appear geolocated outside China and possibly local to the target.
- **Management planes** — Proxy Platform Management, Proxy Pool Management System, and **QTBotnet** (controller server, secondary-level control servers, compromised devices). The controller server can launch DDoS attacks and run commands on infected nodes.
- **Exploitation (per court documents / FBI):** zero-days in Ivanti Connect Secure (CVE-2024-8190, CVE-2024-8963, CVE-2024-9380) and N-days in Fortinet SSL-VPN (CVE-2018-13379), Citrix ADC (CVE-2019-19781), Microsoft Exchange Server (CVE-2021-26855), F5 BIG-IP (CVE-2020-5902), Kentico CMS (CVE-2019-10068), Apache Log4j (CVE-2021-44228), Atlassian Confluence (CVE-2023-22515).
- **Named intrusion attempt:** in a 2019 case, QTFY is said to have attempted to break into NASA by exploiting **CVE-2019-11510** (Pulse Secure VPN critical vulnerability) (per THN's coverage of the affidavit; attempt-only, not confirmed compromise).

## Victimology and attribution framing
- Named targets (DoJ-corrected framing, August 29–31, 2026): NASA, Federal Reserve, DOE, DOJ, HHS, NIH, U.S. Senate — listed as "among the targets of QTFY," not confirmed victims.
- Operator: QTFY, employed by Nanjing Xinjiuwei Network Technology Company; paying customers assessed to include MSS and PLA.
- Lumen Black Lotus Labs: active since May 2018; targeting across the western world and beyond, especially academia/research communities.
- Preserve the framing: the DoJ names QTFY as a PRC state-sponsored *group* under court documents; the MSS/PLA customer relationship is from the same filing. No individual indictments are described in the public press release as of this page.

## Defender priorities
1. **Hunt the naming family, not just the seized domains:** `qt-proxy` / `qt-team` / `qtproxy` hostnames, `mq-task` / `mq-result` task/result paths, and `www.` / `securelink.` admin pairs.
2. **IoT and edge exposure review:** QScan-style botnets grow through vulnerable IoT/edge devices. Prioritize remote-access appliances (VPN, SD-WAN, CPE routers) and patch the listed N-day set.
3. **Commercial-proxy noise is the detection problem:** operator traffic blends with legitimate proxy services. Egress filtering, per-service allowlists, and outbound-connection baselining on internal endpoints matter more than static domain blocks.
4. **Academia and research-community targeting:** expect recruitment/collaboration-themed initial access and data theft from research environments; scope email and identity telemetry accordingly.
5. **DDoS capability:** QTBotnet controller-side DDoS capability means the platform could pivot from espionage to disruption; monitor for large-scale DDoS from residential/IoT address ranges correlated with the other indicators.

## Indicators
- `mq-task.qt-proxy[.]org`, `mq-result.qt-proxy[.]org`
- `mq-task.qt-team[.]com`, `mq-result.qt-team[.]com` (historical)
- `www.qtproxy[.]xyz`, `securelink.qtproxy[.]xyz`
- Platform names: QScan, QTRouter, QTBotnet, Proxy Platform Management, Proxy Pool Management System
- Actor/group name: QTFY (PRC state-sponsored); employer: Nanjing Xinjiuwei Network Technology Company
- Router firmware fingerprint: custom OpenWrt on proxy nodes; Clash proxy configuration
- Exploited CVEs: CVE-2024-8190, CVE-2024-8963, CVE-2024-9380 (Ivanti CSA); CVE-2018-13379, CVE-2019-19781, CVE-2021-26855, CVE-2020-5902, CVE-2019-10068, CVE-2021-44228, CVE-2023-22515; CVE-2019-11510 (Pulse Secure, named 2019 NASA intrusion attempt)

## Context
- **Separate from the Kaspersky/Group-IB Mirage Kitten (Nimbus Manticore / UNC1549) Iran-nexus line.** Both operations use proxy/tunnel obfuscation; Group-IB's August 26, 2026 Tortoiseshell reporting names `172.86.98[.]113` as the SSH tunnel destination, which also appears in Kaspersky's NightLedger infrastructure list. That IP is a *coincidence-level overlap candidate* between the two unrelated actor lines and is not asserted as shared infrastructure here; see the [Mirage Kitten campaign page](mirage-kitten-nightledger-bridgehead-arcbridge.md).
- **QTFY is not previously tracked on this wiki.** No prior actor page exists; this ops page is the first entry. If QTFY tooling appears in additional reporting (e.g., Lumen's "digital quartermaster" enablement-model post), link it here.

## Related pages
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [Lumen Black Lotus Labs enablement-model post](https://www.lumen.com/blog/en-us/the-infrastructure-quartermaster-inside-a-china-nexus-state-enablement-model) (external)

## Update log
- **2026-08-31:** DoJ corrected its August 26 press release: NASA, Federal Reserve, DOE, DOJ, HHS, NIH, and the U.S. Senate are now described as "among the **targets** of QTFY" rather than victims (DoJ: edits made "to ensure this press release accurately reflects the government's allegations in the affidavit in support of the domain seizures"; correction reported by Reuters over the Aug 29–31 window and by THN on Aug 31). Affected sections of this page updated to the targets framing. THN also names a 2019 QTFY attempt to intrude into NASA via **CVE-2019-11510** (Pulse Secure VPN), attempt-only with no confirmed compromise. Monitor: victim-organization confirmation, affidavit detail naming confirmed victims, and whether the DoJ release adds or removes any agencies.

## Sources
- U.S. Department of Justice / FBI press release, "Justice Department and FBI Seize Platforms Operated and Used by China State-Sponsored Hackers to Target U.S. Critical Infrastructure," August 26, 2026 (as corrected August 29–31, 2026 — "Among the targets of QTFY are..." now replaces the earlier "victims" wording): [https://www.justice.gov/opa/pr/justice-department-and-fbi-seize-platforms-operated-and-used-china-state-sponsored-hackers](https://www.justice.gov/opa/pr/justice-department-and-fbi-seize-platforms-operated-and-used-china-state-sponsored-hackers)
- The Hacker News, "FBI Disrupts China-Linked QTFY Infrastructure Used to Steal Data From U.S. Organizations" (Ravie Lakshmanan, August 26, 2026): [https://thehackernews.com/2026/08/fbi-disrupts-china-linked-qtfy.html](https://thehackernews.com/2026/08/fbi-disrupts-china-linked-qtfy.html)
- The Hacker News, "DoJ Corrects China Hacking Claim, Says U.S. Agencies Were Targets, Not Victims" (Ravie Lakshmanan, August 31, 2026): [https://thehackernews.com/2026/08/doj-corrects-china-hacking-claim-says.html](https://thehackernews.com/2026/08/doj-corrects-china-hacking-claim-says.html)
- Lumen Black Lotus Labs, "The Infrastructure Quartermaster: Inside a China-Nexus State Enablement Model": [https://www.lumen.com/blog/en-us/the-infrastructure-quartermaster-inside-a-china-nexus-state-enablement-model](https://www.lumen.com/blog/en-us/the-infrastructure-quartermaster-inside-a-china-nexus-state-enablement-model)
