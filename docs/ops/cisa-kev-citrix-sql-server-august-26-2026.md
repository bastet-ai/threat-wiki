# CISA KEV August 26, 2026 additions: Citrix NetScaler DoS, Microsoft SQL Server RCE, and four UAT-10147 exploitation CVEs

## Summary
On **August 26, 2026**, CISA added **six** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog. Two are new to this wiki: **Citrix NetScaler ADC / NetScaler Gateway CVE-2026-8452** (a memory-overflow denial-of-service in Gateway / AAA virtual servers, NVD CVSS 9.8 Critical) and **Microsoft SQL Server CVE-2019-1068** (an authenticated remote-code-execution flaw, NVD CVSS 8.8 High). The other four — **Ajax.NET Professional CVE-2021-23758** (deserialization RCE), **Linux kernel CVE-2022-0995** (watch_queue out-of-bounds write), **ABRT CVE-2015-5287**, and **libuser CVE-2015-3246** — are the **exact initial-access and Linux-privilege-escalation CVE set documented in the UAT-10147 / SPECTRE / BadIIS campaign**. CISA formally listing them is a durable signal: these are no longer just "the CVEs UAT-10147 uses" but independently confirmed known-exploited vulnerabilities with their own BOD 26-04 federal deadlines.

All six entries carry **BOD 26-04** remediation deadlines (the two new edge/identity-flavor flaws due **2026-08-29**; the four UAT-10147 CVEs due **2026-09-09**) and a Forensics Triage requirement. CISA records **ransomware use as unknown** for all six and identifies **no actor, infrastructure, or payload** on the catalog entries themselves.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- Citrix
- NetScaler
- NetScaler ADC
- NetScaler Gateway
- AAA virtual server
- denial of service
- CVE-2026-8452
- Microsoft
- SQL Server
- remote code execution
- CVE-2019-1068
- UAT-10147
- SPECTRE
- BadIIS
- Ajax.NET Professional
- AjaxPro
- deserialization
- CVE-2021-23758
- Linux kernel
- watch_queue
- out-of-bounds write
- CVE-2022-0995
- ABRT
- CVE-2015-5287
- libuser
- CVE-2015-3246
- local privilege escalation

## The two new CVEs

### CVE-2026-8452 — Citrix NetScaler ADC / Gateway denial of service
CISA's entry describes an **improper restriction of operations within the bounds of a memory buffer** (CWE-119) in **Citrix NetScaler ADC and NetScaler Gateway** that "could lead to denial of service." NVD scores it **CVSS 3.1 9.8 Critical** (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) and **CVSS 4.0 8.8**, network-reachable with **no privileges and no user interaction**. Citrix's advisory (**CTX696604**) scopes the affected configuration: the flaw is exploitable **when the appliance is configured as a Gateway (SSL VPN, ICA Proxy, CVPN, RDP Proxy) or an AAA virtual server** — the same remote-access edge surface that has repeatedly driven CitrixBleed-class incidents.

- **KEV entry:** added 2026-08-26; **BOD 26-04 due 2026-08-29**.
- **CWE:** CWE-119 (buffer memory overflow).
- **Ransomware use:** unknown; no actor, infrastructure, or payload identified.
- **Context:** this is a **DoS** determination, not code execution — but on an internet-facing VPN/AAA edge appliance, availability loss is a remote-access incident in its own right, and it lands days after **CVE-2026-8451** (the June 30, 2026 NetScaler memory-overread in the SAML IdP path, see the [dedicated page](citrix-netscaler-cve-2026-8451-memory-overread.md)) on the same product. Repeated edge-appliance disclosure cycles justify treating NetScaler exposure as a standing credential/session and availability control, not a one-off patch.

### CVE-2019-1068 — Microsoft SQL Server remote code execution
CISA's entry names a **remote-code-execution** vulnerability in **Microsoft SQL Server** that "could allow an attacker to execute code in the context of the SQL Server Database Engine service account." NVD scores it **CVSS 3.1 8.8 High** (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`) — **authenticated** (low privilege), network-reachable, no user interaction. This is a 2019-era flaw surfacing as a KEV entry in 2026, so the durable defender takeaway is that **legacy and unpatched SQL Server builds** remain actively targeted; it is not a one-day.

- **KEV entry:** added 2026-08-26; **BOD 26-04 due 2026-08-29**.
- **Required action:** apply mitigations per Microsoft's advisory (portal.msrc.microsoft.com …/CVE-2019-1068), follow BOD 26-04 and the Forensics Triage requirement.
- **Ransomware use:** unknown; no actor, infrastructure, or payload identified.

## The four UAT-10147 CVEs now in KEV
CISA's August 26, 2026 batch adds four CVEs that map one-to-one onto the initial-access and Linux-privilege-escalation chains documented on the [UAT-10147 campaign page](uat-10147-spectre-badiis-ai-augmented-web-server-campaign.md):

| CVE | Product | Class | UAT-10147 role | CWE | BOD 26-04 due |
|-----|---------|-------|----------------|-----|----------------|
| CVE-2021-23758 | Ajax.NET Professional | deserialization RCE | initial access (web-server RCE) | CWE-502 | 2026-09-09 |
| CVE-2022-0995 | Linux kernel | out-of-bounds write | Linux LPE (watch_queue) | CWE-787 | 2026-09-09 |
| CVE-2015-5287 | Automatic Bug Reporting Tool | memory-safety | Linux LPE (ABRT sosreport) | — | 2026-09-09 |
| CVE-2015-3246 | libuser | memory-safety | Linux LPE (libuser roothelper) | — | 2026-09-09 |

CISA cites the upstream kernel commit (`93ce93587d36493f2f86921fa79921b3cba63fbb`) for CVE-2022-0995, the upstream ABRT commit for CVE-2015-5287, and the AjaxPro fix commit for CVE-2021-23758. None of the four carry a named actor on the KEV entry; the actor linkage is Talos' UAT-10147 attribution, not CISA's. The practical signal: any internet-exposed web server running **AjaxPro**, and any Linux host running a kernel older than the CVE-2022-0995 fix, is now a **patch-now** target under both BOD 26-04 and the UAT-10147 threat model.

## Defender priorities
1. **Patch the two new flaws now.** NetScaler appliances configured as a **Gateway (SSL VPN / ICA / CVPN / RDP Proxy) or AAA virtual server** are the CVE-2026-8452 blast radius — apply Citrix's CTX696604 fix or mitigate availability exposure, and treat it alongside CVE-2026-8451 in a single NetScaler edge review. SQL Server deployments: confirm the service is on a current build and hunt for anomalous execution in the Database Engine service account.
2. **Fold the four UAT-10147 CVEs into your patch-and-hunt scope.** AjaxPro is the highest-leverage initial-access primitive; the three Linux LPEs (watch_queue / ABRT / libuser) are the escalation ladder Talos documented. If you run exposed web servers or long-lived Linux hosts, patch or disable the unused surfaces.
3. **Treat KEV listings as independent of campaign attribution.** CISA adds a CVE because it is known-exploited; it does not name UAT-10147 on these entries. Do not use the KEV listing as a UAT-10147 attribution source — the campaign linkage is Talos' assessment.
4. **Preserve evidence before destructive cleanup.** All six entries carry the BOD 26-04 Forensics Triage requirement for federal systems.
5. **Re-check the catalog.** If CISA adds more UAT-10147 CVEs or names infrastructure later, update this page and the campaign page together.

## Assessment limits
- CISA's catalog entries for all six CVEs record **ransomware use as unknown** and identify **no actor, infrastructure, or payload**. The UAT-10147 linkage for the four CVEs is Talos' separate attribution, not CISA's.
- CVE-2026-8452 is a **denial-of-service** determination (CVSS 9.8 on the availability axis); there is no public code-execution claim on the KEV entry. Citrix's full advisory text was not directly retrievable at capture time; the NVD description and CVSS vector are the authoritative public fields used here.
- CVE-2019-1068 is a **2019** flaw; the KEV addition is a 2026 exploitation determination. Its authenticated prerequisite (PR:L) means it is not an unauthenticated edge exposure, but a high-value follow-on after initial access.

## Related pages
- [Citrix NetScaler CVE-2026-8451 memory overread](citrix-netscaler-cve-2026-8451-memory-overread.md)
- [UAT-10147 SPECTRE / BadIIS / agentic-AI web-server campaign](uat-10147-spectre-badiis-ai-augmented-web-server-campaign.md)
- [UAT-10147](../actors/uat-10147.md)
- [Zimbra SNMP command injection in CISA KEV; Microsoft patches Entra ID deserialization flaw](cisa-kev-microsoft-entra-zimbra-august-21-2026.md)
- [Gitea diffpatch Git-hook RCE in CISA KEV (CVE-2026-60004)](gitea-cve-2026-60004-diffpatch-git-hook-rce-kev-august-25-2026.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (2026-08-26 batch)
- Citrix advisory CTX696604: [https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604)
- NVD: [CVE-2026-8452](https://nvd.nist.gov/vuln/detail/CVE-2026-8452)
- NVD: [CVE-2019-1068](https://nvd.nist.gov/vuln/detail/CVE-2019-1068)
- Microsoft MSRC: [CVE-2019-1068](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-1068)
- BOD 26-04: [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
- Cisco Talos: [UAT-10147: Chinese-speaking adversary integrates agentic AI into post-compromise operations](https://blog.talosintelligence.com/uat-10147-chinese-speaking-adversary-integrates-agentic-ai-into-post-compromise-operations/) (Joey Chen, August 20, 2026)
