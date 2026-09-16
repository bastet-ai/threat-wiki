# CISA KEV September 16, 2026 (second and third additions): Cisco ISE CVSS 10.0 unauthenticated management-interface bypass with Cisco confirming active exploitation, and Acronis Backup cPanel/Plesk local privilege escalation under limited targeted exploitation

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- Cisco
- Cisco ISE
- Identity Services Engine
- ISE-PIC
- authentication bypass
- CWE-648
- CVE-2026-76460
- network access control
- Acronis
- Acronis Backup
- cPanel
- WHM
- Plesk
- shared hosting
- privilege escalation
- incorrect default permissions
- CWE-276
- CVE-2026-87886

## Summary

CISA's September 16, 2026 KEV batch is **three** additions, not one (catalog `2026.09.16`, now **1,713 entries**). The Google Pixel cellular-modem entry has its own page; this page covers the two that arrived after it:

| CVE | Product | Class | CVSS | CWE | BOD 26-04 due | Forensics triage |
|---|---|---|---|---|---|---|
| **CVE-2026-76460** | Cisco Identity Services Engine (ISE) + ISE Passive Identity Connector (ISE-PIC) | **Incorrect use of privileged APIs — unauthenticated remote authentication bypass of the web management interface**; Cisco states successful exploitation may yield **command execution with root privileges** | **10.0 Critical** (CVSS v3.1, `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`) | CWE-648 | **2026-09-19** | **Yes** |
| **CVE-2026-87886** | Acronis Backup plugin for cPanel & WHM + extension for Plesk | **Incorrect default permissions → local privilege escalation** on Linux hosting servers | **7.8 High** (Acronis-assigned) | CWE-276 | **2026-09-19** | **Yes** |

Both carry **BOD 26-04**, **ransomware use unknown**, and **no actor named** on the catalog entry. Both are exploitation-confirmed: **Cisco PSIRT "is aware of active exploitation of this vulnerability"**, and **Acronis disclosed "limited, targeted exploitation in the wild"** ahead of its patch.

## Cisco ISE / ISE-PIC CVE-2026-76460 (due 2026-09-19)

- **Advisory:** `cisco-sa-ISE-ABP-VNSW7Tn5`, first published **2026 September 16 16:00 GMT, Version 1.0 Final**, Cisco Bug ID **CSCww39530**. Found during the resolution of a **Cisco TAC support case**. Part of a group of September 16 advisories, published alongside a dedicated **Cisco ISE Security Hardening Release: September 2026**.
- **Mechanics:** insufficient authentication control on an API endpoint lets an **unauthenticated, remote attacker send a crafted request** to **bypass authentication on the web-based management interface** and gain unauthorized access to the device. Cisco's own IoC section warns that **upon successful exploitation, threat actors may obtain command execution with root privileges** — an auth bypass that is really a path to root.
- **Scope:** ISE and ISE-PIC affected **regardless of device configuration**.
- **Workarounds:** none. The only **mitigation** is infrastructure access control lists (iACLs) restricting the management interface to required management sources.
- **Fixed releases:** **3.1 Patch 12, 3.2 Patch 11, 3.3 Patch 12, 3.4 Patch 7, 3.5 Patch 4**. **Release 3.0 is End of Software Maintenance** — migrate to a supported fixed branch; there is no fix for it.
- **Cisco-published hunt:** review `access.log` on **every node** of a distributed deployment for **suspicious usernames**, e.g. `admin#show logging application ise-kong/access.log | include dummyuser`; additional access logs live in a support bundle (with debug logs) at `./ise/logs/apigateway/access.log*.gz`. Cisco states an attacker with root **may remove or hide local evidence**, and **strongly recommends re-imaging** affected nodes (restore from configuration backup) rather than trusting in-place cleanup.
- **Sibling advisories the same day** (GitHub Advisory mirror): CVE-2026-20307 (`GHSA-phj9-35hx-q9cr`, 9.9, **authenticated** web-management-interface escalation) and CVE-2026-20306 (`GHSA-m8gm-7wx7-cf56`, 9.1, **authenticated** REST API flaw on ISE/ISE-PIC) — treat the September 16 ISE hardening release as a full attack-surface trim, not a single-CVE patch.
- **Why this one matters disproportionately:** ISE is the **network admission control brain** — policy, identity, profiling, and RADIUS/TACACS+ authority over which device gets on the network and at what privilege. A root-level foothold on ISE is a pivot primitive against every downstream authenticated network, not just the appliance. It is the **fourth September 2026 root-class flaw against network/security management planes** after Cisco Secure FMC CVE-2026-20079, Secure Email Gateway CVE-2026-76461, and Check Point Security Management Server CVE-2026-91843.

## Acronis Backup for cPanel & WHM / Plesk CVE-2026-87886 (due 2026-09-19)

- **Advisory:** Acronis `SEC-10986`. **CWE-276 (Incorrect Default Permissions)**; Acronis assigns CVSS **7.8** (local attack vector, low privileges required, no user interaction). The KEV/NVD record was still sparse at scan time (no NVD entry yet).
- **Mechanics:** insecure default file permissions in the Linux backup component let a **local low-privileged user** access resources / execute actions beyond their level — i.e. **privilege escalation on the hosting server itself**.
- **Exploitation status:** Acronis reported **limited, targeted exploitation in the wild** and shipped fixes **before** the KEV listing.
- **Fixed in:** **Backup plugin for cPanel & WHM 1.9.3 HF3**; **Backup extension for Plesk 1.8.11**.
- **Blast radius:** these components run on **shared hosting / MSP servers consolidating many customer accounts**. The realistic kill chain is: phished/weak hosting account or webshell (initial access at account level) → **Acronis LPE to server-level privileges** → access to **backup data (which contains every tenant's files and credentials), system files, control-panel resources, and other customers' workloads**. One compromised site becomes a whole-server compromise.
- **Durable read:** backup software on multi-tenant hosts is a **credentials-to-all-tenants concentration point**; a backup agent that any customer account can influence is part of the trust boundary, and default-permission bugs in it convert account-level footholds into platform compromise.

## Defender takeaways

- **Cisco ISE/ISE-PIC is the urgent item: CVSS 10.0, unauthenticated, vendor-confirmed active exploitation, no workaround, BOD deadline 2026-09-19.** Patch to the fixed patches above, apply iACLs to the management interface now, hunt the access-log username tell on every deployment node, and if anything surfaces — **re-image, rotate ISE-integrated credentials (AD, RADIUS secrets, TACACS+, integrated identity sources), audit admin accounts**, and treat network admission policy as potentially attacker-edited.
- **ISE on 3.0 has no fix path** — migration is the only remediation; an EoS ISE on a reachable management network should be treated as an open door.
- **cPanel/Plesk hosting operators:** move Acronis plugin/extension to 1.9.3 HF3 / 1.8.11, then audit for local accounts with anomalous sudo/setuid artifacts and any backup-job tampering. Assume post-exploitation from account-level footholds — the LPE only matters because something already got a local shell.
- **Pattern:** September 2026's KEV cadence keeps hitting **management and concentration-plane software** (firewall management, email gateways, NAC, backup-on-shared-hosting). Inventory where management interfaces are reachable from, and put every one of them behind strict access control regardless of CVE status.

## Related pages

- [Google Pixel cellular-modem CVE-2026-58704 KEV page](google-pixel-cellular-modem-cve-2026-58704-kev-targeted-exploitation-september-2026.md) — the first addition to the same 2026.09.16 catalog batch
- [Check Point Security Management Server CVE-2026-91843 login stack overflow root RCE](../tools/check-point-security-management-server-cve-2026-91843-login-stack-overflow-root-rce-september-2026.md) — same-week management-plane root flaw (not yet KEV at scan time)
- [Cisco Secure Email Gateway CVE-2026-76461 SQL injection root KEV](cisco-secure-email-gateway-cve-2026-76461-sql-injection-root-kev-september-2026.md) — September's second Cisco appliance root flaw
- [Cisco Secure FMC CVE-2026-20316 static-credential exploitation](cisco-fmc-cve-2026-20316-static-credential-exploitation.md) — the September FMC cluster
- [Talos: three actor clusters exploiting Cisco FMC](talos-fmc-ongoing-exploitation-cve-2026-20079-cve-2026-20316-actor-clusters-september-2026.md)
- [CISA KEV September 10-11, 2026 batch](cisa-kev-screenconnect-artifactory-gitlab-mikrotik-september-10-11-2026.md)

## Sources

- CISA KEV catalog, version **2026.09.16** (1,713 entries): [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- Cisco advisory: [cisco-sa-ISE-ABP-VNSW7Tn5 — Cisco Identity Services Engine Incorrect Use of Privileged APIs Vulnerability](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ISE-ABP-VNSW7Tn5) (Sep 16, 2026, Version 1.0 Final; CVSS 10.0; PSIRT aware of active exploitation; access.log hunt + re-image guidance; fixed patch table)
- Cisco sibling advisories via GitHub Advisory mirror: [CVE-2026-20307 / GHSA-phj9-35hx-q9cr](https://github.com/advisories/GHSA-phj9-35hx-q9cr), [CVE-2026-20306 / GHSA-m8gm-7wx7-cf56](https://github.com/advisories/GHSA-m8gm-7wx7-cf56)
- Acronis advisory: [SEC-10986](https://security-advisory.acronis.com/advisories/SEC-10986) (JS-gated at scan time; KEV row cites it directly)
- NVD: [CVE-2026-76460](https://nvd.nist.gov/vuln/detail/CVE-2026-76460); CVE-2026-87886 not yet enriched at scan time
