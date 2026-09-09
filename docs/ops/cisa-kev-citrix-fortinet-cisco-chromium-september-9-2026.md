# CISA KEV September 9, 2026 additions: four exploited flaws — Citrix NetScaler auth bypass, Fortinet heap overflow, Cisco FMC auth bypass, and an in-the-wild Chrome V8 out-of-bounds write

## Summary
On **September 9, 2026**, CISA added **four** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog:

| CVE | Product | Class | CVSS / severity | CWE | Forensics triage | BOD 26-04 due |
|---|---|---|---|---|---|---|
| **CVE-2026-19490** | Citrix NetScaler ADC / Gateway | **Authentication Bypass Using an Alternate Path or Channel** — unauthenticated auth bypass on an AAA virtual server or Gateway (SSL VPN / ICA Proxy / CVPN / RDP Proxy) | **9.3 Critical** (CVSS v4.0) | CWE-288 | **Yes** | **2026-09-12** |
| **CVE-2025-25249** | Fortinet FortiOS / FortiSwitchManager / FortiSASE | **Heap-based Buffer Overflow** — unauthorized code/commands via specially crafted packets | **8.1 High** (CVSS v3.1) | CWE-122, CWE-787 | **Yes** | **2026-09-12** |
| **CVE-2026-20079** | Cisco Secure FMC / SCC Firewall Management | **Authentication Bypass Using an Alternate Path or Channel** — unauthenticated root on the FMC web interface | **10.0 Critical** (CVSS v3.1, S:C) | CWE-288 | **Yes** | **2026-09-12** |
| **CVE-2026-87491** | Google Chromium V8 | **Out-of-Bounds Write** — remote attacker executes arbitrary code inside the sandbox via a crafted HTML page; Google confirms an exploit exists in the wild | **8.8 High** (CVSS v3.1) | CWE-787 | No | **2026-09-23** |

All four carry the **BOD 26-04** remediation requirement. CISA records **ransomware use as unknown** for all four and names **no actor, infrastructure, or payload** on the catalog entries. The three entries with **2026-09-12** deadlines (Citrix NetScaler, Fortinet, Cisco FMC) are the priority items — all are **unauthenticated, remote, pre-authentication** flaws against edge/management appliances, and two of them (Citrix and Cisco FMC) are **CWE-288 authentication bypasses that yield full control** of the appliance. The Chrome V8 entry (due **2026-09-23**) is the seventh actively-exploited Chromium zero-day tracked by CISA this cycle and is confirmed **exploited in the wild**.

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
- authentication bypass
- CWE-288
- CVE-2026-19490
- Fortinet
- FortiOS
- FortiSwitchManager
- FortiSASE
- heap-based buffer overflow
- CVE-2025-25249
- Cisco
- Cisco Secure FMC
- Security Cloud Control
- root access
- CVE-2026-20079
- Google
- Chromium
- V8
- out-of-bounds write
- browser zero-day
- client-side exploitation
- CVE-2026-87491

## The four entries

### CVE-2026-19490 — Citrix NetScaler ADC / Gateway authentication bypass
CISA's entry: a **Citrix NetScaler Authentication Bypass Using an Alternate Path or Channel Vulnerability** in NetScaler ADC and NetScaler Gateway. When the appliance is configured as an AAA virtual server or as a Gateway (SSL VPN, ICA Proxy, CVPN, or RDP Proxy), an unauthenticated remote threat actor may be able to bypass authentication.

- **KEV entry:** added 2026-09-09; **BOD 26-04 due 2026-09-12**; Forensics Triage **Yes**; CWE-288.
- **Vendor:** Citrix. NVD CVSS **v4.0 9.3 Critical** (`AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L`).
- **Affected / preconditions (per Citrix bulletin CTX696939, published with sibling CVE-2026-19489):** 14.1 before 14.1-73.32 and 13.1 before 13.1-63.21 (14.1-FIPS before 14.1-73.32 FIPS; 13.1-FIPS/NDcPP before 13.1-37.277). Applicable when configured as a Gateway (SSL VPN, ICA Proxy, CVPN, RDP Proxy) or AAA vserver; on 14.1-43.56+ / 13.1-61.28+ only when a **SAML action** is configured. Secure Private Access Hybrid deployments using NetScaler are also affected.
- **Fix:** upgrade to NetScaler ADC / Gateway **14.1-73.32+** or **13.1-63.21+** (FIPS: 14.1-73.32 FIPS / 13.1-37.277+). The sibling **CVE-2026-19489** (memory overflow → DoS, CVSS v4.0 8.8, CWE-119, on LSN-group SIP-ALG configs) is fixed in the same builds.
- **Hunt:** config recon for `add authentication samlAction.*`, `add authentication vserver .*`, and `add vpn vserver .*`.

### CVE-2025-25249 — Fortinet FortiOS / FortiSwitchManager / FortiSASE heap-based buffer overflow
CISA's entry: a **heap-based buffer overflow vulnerability** in Fortinet FortiOS, FortiSwitchManager, and FortiSASE that allows an attacker to execute unauthorized code or commands via specially crafted packets.

- **KEV entry:** added 2026-09-09; **BOD 26-04 due 2026-09-12**; Forensics Triage **Yes**; CWE-122 / CWE-787.
- **Vendor:** Fortinet. NVD CVSS **v3.1 8.1 High** (`AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H`).
- **Affected (per NVD):** FortiOS 7.6.0–7.6.3, 7.4.0–7.4.8, 7.2.0–7.2.11, 7.0.0–7.0.17, FortiOS 6.4 (all versions), FortiSwitchManager 7.2.0–7.2.6 and 7.0.0–7.0.5 (FortiSASE listed in the KEV entry).
- **Context:** this is the same Fortinet PSIRT record (FG-IR-25-084) that has sat on the Fortinet advisory since early 2026; its promotion to KEV on September 9 marks confirmed in-the-wild exploitation. Patch to the Fortinet-recommended fixed builds and verify internet-exposed edge devices.

### CVE-2026-20079 — Cisco Secure FMC / SCC Firewall Management authentication bypass (root)
CISA's entry: a **Cisco Firewall Management Center Authentication Bypass Using an Alternate Path or Channel Vulnerability** in Cisco Secure FMC Software and Cisco Security Cloud Control (SCC) Firewall Management that could allow an unauthenticated, remote attacker to bypass authentication and execute script files to obtain **root access** to the underlying operating system.

- **KEV entry:** added 2026-09-09; **BOD 26-04 due 2026-09-12**; Forensics Triage **Yes**; CWE-288.
- **Vendor:** Cisco, advisory **cisco-sa-onprem-fmc-authbypass-5JPp45V2** (CVSS **v3.1 10.0 Critical**, `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`). Root cause: an improper system process created at boot; crafted HTTP requests to the FMC web interface reach script execution as root. No workarounds.
- **Affected:** Cisco Secure FMC Software and SCC Firewall Management, regardless of device configuration. (FDM, ASA, FTD, and SCC core are confirmed not vulnerable.) The SCC SaaS offering is already patched by Cisco — no user action there.
- **Fix (on-prem hotfixes):** 7.0 → `7.0.9.1-3`, 7.2 → `7.2.11.1-4`, 7.4 → `7.4.7.1-3`, 7.6 → `7.6.5.1-2`, 7.7 → `7.7.12.1-2`, 10.0 → `10.0.1.1-2` (from the Cisco Software Center).
- **IoC:** `zgrep "package_info.*license" /var/log/messages*` in expert mode — a log line referencing `/var/tmp/license.tmp` (e.g. `COMMAND=/usr/local/sf/bin/package_info.pl /var/tmp/license.tmp --lsm`) indicates possible exploitation. If found, contact Cisco TAC; hotfixes only prevent future exploitation and do not clean an existing compromise.

### CVE-2026-87491 — Google Chromium V8 out-of-bounds write
CISA's entry: an **Out-of-Bounds Write Vulnerability** in Google Chromium V8 that allows a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. Affects Chromium-based browsers including Google Chrome, Microsoft Edge, and Opera.

- **KEV entry:** added 2026-09-09; **BOD 26-04 due 2026-09-23**; Forensics Triage **No**; CWE-787.
- **Vendor:** Google. NVD CVSS **v3.1 8.8 High** (`AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H`).
- **Exploit status:** the **Chrome 153 stable-channel update (Sep 8, 2026 — 153.0.8010.36 / .37)** explicitly states that **an exploit for CVE-2026-87491 exists in the wild**. That makes it the next actively-exploited Chromium zero-day after CVE-2026-85046 (patched Sep 4) — the seventh tracked in this cycle.
- **Discovery / disclosure:** reported by Jihyeon Jeong (Compsec Lab, Seoul National University / research intern) on 2026-08-06; $2,500 bug bounty. The 153 update shipped **230 security fixes** in total.
- **Public attribution:** none in the reviewed public sources. Keep actor, lure, and target-sector attribution unset unless Google or CISA publishes follow-up.

## Defender priorities
1. **Treat the three 2026-09-12 edge/management pre-auth items as urgent.** Citrix NetScaler: upgrade to 14.1-73.32+ / 13.1-63.21+ (fixes CVE-2026-19490 and CVE-2026-19489) and check SAML / AAA / VPN vserver configs. Cisco FMC: deploy the matching per-release hotfix and hunt the `/var/tmp/license.tmp` IoC; on-prem only (SCC SaaS is patched). Fortinet: move every in-range FortiOS / FortiSwitchManager / FortiSASE device to the recommended fixed build.
2. **Push Chrome 153.0.8010.36+ across all endpoints** and verify Chromium-derived browsers (Edge, Brave, Opera, Vivaldi, embedded runtimes) separately. The in-the-wild V8 OOB-write is a client-side initial-access primitive — prioritize hosts that browse the open web, open mail/web links, or run privileged SaaS sessions.
3. **Preserve evidence before cleanup** on covered federal systems — Forensics Triage applies to CVE-2026-19490, CVE-2025-25249, and CVE-2026-20079.
4. **Assume appliance compromise, not just vulnerability.** All three edge flaws yield full control (two auth bypasses to root/admin, one heap overflow to code execution); after patching, hunt for persistence, lateral movement, and credential theft from the appliance's vantage point.
5. **Re-check the catalog.** This is the seventh CISA batch within seven weeks; CISA is adding entries at a multi-per-day cadence, so the catalog is a standing watch item.

## Assessment limits
- CISA's entries record **ransomware use as unknown** and identify **no actor, infrastructure, or payload** for all four.
- The Citrix precondition (SAML action / AAA vserver) and the CVE-2026-19489 pairing are from Citrix bulletin CTX696939; verify your specific NetScaler build against the full affected matrix.
- The Fortinet affected-version list is derived from the NVD description; confirm exact fixed builds against Fortinet advisory FG-IR-25-084 and your release branch before declaring a device patched.
- The Cisco FMC IoC (`/var/tmp/license.tmp`) is a strong signal but not definitive; follow Cisco TAC guidance when it is present.
- No Microsoft Security Blog write-up was found for the four KEV entries as of capture; the KEV + NVD + vendor advisories are the primary public source.

## Related pages
- [CISA KEV September 8, 2026 additions: four exploited flaws — Adobe/Magento StyleSmuggler, N-able N-central, and two Windows LPEs](cisa-kev-stylesmuggler-nable-windows-lpe-september-8-2026.md)
- [CISA KEV September 2, 2026 additions: seven exploited flaws across Artifactory, Kestra, SonicWall, LiteLLM, Starlette, and Switchvox](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)
- [Chrome V8 CVE-2026-85046 type-confusion exploitation](chrome-v8-cve-2026-85046-type-confusion-exploitation-september-2026.md)
- [Microsoft: passkey-themed social engineering leads to identity and cloud compromise (Storm-3121 / Storm-3032)](microsoft-passkey-social-engineering-identity-cloud-compromise-september-9-2026.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (2026-09-09 batch) / [catalog JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- NVD: [CVE-2026-19490](https://nvd.nist.gov/vuln/detail/CVE-2026-19490), [CVE-2025-25249](https://nvd.nist.gov/vuln/detail/CVE-2025-25249), [CVE-2026-87491](https://nvd.nist.gov/vuln/detail/CVE-2026-87491), [CVE-2026-20079](https://nvd.nist.gov/vuln/detail/CVE-2026-20079)
- Citrix: [NetScaler ADC and NetScaler Gateway Security Bulletin CTX696939 (CVE-2026-19489 / CVE-2026-19490)](https://support.citrix.com/external/article/CTX696939/netscaler-adc-and-netscaler-gateway-secu.html)
- Fortinet: [PSIRT advisory FG-IR-25-084](https://fortiguard.fortinet.com/psirt/FG-IR-25-084)
- Cisco: [Security Advisory cisco-sa-onprem-fmc-authbypass-5JPp45V2](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2)
- Google Chrome Releases: [Stable Channel Update for Desktop — Sep 8, 2026](https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_0808145027.html)
- BOD 26-04: [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
