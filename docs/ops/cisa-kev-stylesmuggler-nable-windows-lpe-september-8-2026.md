# CISA KEV September 8, 2026 additions: four exploited flaws — Adobe/Magento StyleSmuggler RCE, N-able N-central pre-auth RCE, and two Windows local privilege escalations

## Summary
On **September 8, 2026**, CISA added **four** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog:

| CVE | Product | Class | CVSS / severity | CWE | Forensics triage | BOD 26-04 due |
|---|---|---|---|---|---|---|
| **CVE-2026-75650** | Adobe Commerce and Magento (Open Source 2.4.4–2.4.9, B2B 1.3.3–1.5.3) | **Improper Neutralization of Special Elements Used in a Template Engine** — the **StyleSmuggler** unauthenticated RCE 0-day under active attack | **10.0 Critical** (S:C) | CWE-1336 | **Yes** | **2026-09-11** |
| **CVE-2026-86218** | N-able N-central | **Static Code Injection** — pre-authentication remote-code-execution zero-day exploited in the wild (fixed in Hotfix 4, build 2026.3.1.14) | **10.0 Critical** | CWE-96 | **Yes** | **2026-09-11** |
| **CVE-2026-81963** | Microsoft Windows Update Stack | **Link Following Vulnerability** — an authorized attacker can escalate privileges **locally to SYSTEM** | 7.8 High | CWE-59, CWE-284 | No | **2026-09-22** |
| **CVE-2026-85880** | Microsoft Windows ALPC | **Heap-Based Buffer Overflow** — an authorized attacker can escalate privileges **locally** | 7.8 High | CWE-122, CWE-908 | No | **2026-09-22** |

All four carry the **BOD 26-04** remediation requirement. CISA records **ransomware use as unknown** for all four and names **no actor, infrastructure, or payload** on the catalog entries. The two entries with **2026-09-11** deadlines (Adobe/Magento and N-able N-central) are the priority items — both are **pre-authentication remote-code-execution** flaws already under active exploitation; the two Windows LPEs (due **2026-09-22**) are local privilege escalations that become critical when chained after any initial foothold.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- Adobe
- Magento
- Adobe Commerce
- template injection
- RCE
- CVE-2026-75650
- APSB26-146
- VULN-39341
- N-able
- N-central
- pre-authentication RCE
- zero-day
- CVE-2026-86218
- Hotfix 4
- RMM
- remote monitoring and management
- Microsoft
- Windows
- local privilege escalation
- Windows Update Stack
- ALPC
- CVE-2026-81963
- CVE-2026-85880

## The four entries

### CVE-2026-75650 — Adobe Commerce / Magento StyleSmuggler unauthenticated RCE
CISA's entry: an **Improper Neutralization of Special Elements Used in a Template Engine** vulnerability in Adobe Commerce and Magento that "could allow an attacker to execute arbitrary code." This is the **StyleSmuggler** zero-day that Sansec disclosed on September 5: an unauthenticated two-stage chain (GraphQL `styles` injection into a Magento-generated file, executed server-side at "Payment Transaction Failed Reminder" email render) affecting **every current version**. Adobe published the **APSB26-146** emergency advisory (priority 1) on September 7 with the fix shipped as the **`VULN-39341`** composer hotfix.

- **KEV entry:** added 2026-09-08; **BOD 26-04 due 2026-09-11**; Forensics Triage **Yes**; CWE-1336.
- **Vendor:** Adobe, "Commerce and Magento." CVE published 2026-09-07T21:17Z; **CVSS 3.1 10.0** (scope Changed — e-commerce scope impact).
- **Affected:** Adobe Commerce 2.4.4–2.4.9, Magento Open Source 2.4.4–2.4.9, Adobe Commerce B2B 1.3.3–1.5.3 (older in-branch versions affected but unverified by the hotfix).
- **Context:** stores were exploited for **three days before the hotfix existed** (attacks began Sep 4 22:40 UTC). See the [StyleSmuggler page](stylesmuggler-magento-adobe-commerce-unauth-rce-zero-day-sansec-september-2026.md) for the full chain, Rust backdoor IoCs, and rotation checklist. **Patching does not clean a compromised store** — patch + rotate + hunt.

### CVE-2026-86218 — N-able N-central pre-authentication RCE
CISA's entry: a **Static Code Injection Vulnerability** in N-able N-central enabling **pre-authentication remote-code-execution**. This is the CVSS 10.0 zero-day fixed in **Hotfix 4, build 2026.3.1.14** (September 6), reported by a third independent researcher as **exploited in the wild**.

- **KEV entry:** added 2026-09-08; **BOD 26-04 due 2026-09-11**; Forensics Triage **Yes**; CWE-96.
- **Vendor:** N-able, "N-central."
- **Context:** part of the September escalation of the N-central management-plane incident (a fully-patched customer was compromised September 4). On-prem N-central must move to **2026.3.1.14**; hosted NCOD is already patched. See the [N-able N-central page](n-able-n-central-cve-2026-18556-18577-exploitation.md) for the full exploit chain, Hotfix 3/4 history, and tradecraft. Note: the two Hotfix 3 auth-bypass flaws (**CVE-2026-86206 / CVE-2026-86207**) are **not** in the KEV catalog.

### CVE-2026-81963 — Microsoft Windows Update Stack link-following LPE
CISA's entry: a **Link Following Vulnerability** in the **Windows Update Stack**. NVD: "Improper link resolution before file access ('link following') in Windows Update Stack allows an authorized attacker to elevate privileges locally."

- **KEV entry:** added 2026-09-08; **BOD 26-04 due 2026-09-22**; Forensics Triage **No**; CWE-59 (Symbolic Link) + CWE-284.
- **Vendor:** Microsoft, "Windows." NVD CVSS 3.1 **7.8 High**.
- **Affected (fixed at these versions):** Windows 11 23H2 `10.0.22631.7582`, 24H2 / 25H2 `10.0.26100.9445` / `10.0.26200.9445`, 26H1 `10.0.28000.2954`, Windows Server 2025 `10.0.26100.33438` (per NVD CPE `versionEndExcluding`).
- **Context:** a local, authorized-attacker LPE — the practical risk is post-initial-access privilege escalation to SYSTEM via the Windows Update Stack. Patch in the next regular Windows update cycle; prioritize internet-exposed and domain-joined hosts.

### CVE-2026-85880 — Microsoft Windows ALPC heap-based buffer overflow LPE
CISA's entry: a **Heap-Based Buffer Overflow Vulnerability** in **Windows ALPC** (Advanced Local Procedure Call). NVD: "Heap-based buffer overflow in Windows ALPC allows an authorized attacker to elevate privileges locally."

- **KEV entry:** added 2026-09-08; **BOD 26-04 due 2026-09-22**; Forensics Triage **No**; CWE-122 + CWE-908.
- **Vendor:** Microsoft, "Windows." NVD CVSS 3.1 **7.8 High**.
- **Affected (fixed at these versions):** Windows 10 1607 / Server 2016 `10.0.14393.9512`, 1809 / Server 2019 `10.0.17763.9245`, 21H2 `10.0.19044.7725`, 22H2 `10.0.19045.7725`, Server 2022 `10.0.20348.5622` (per NVD CPE `versionEndExcluding`).
- **Context:** a local, authorized-attacker LPE in the kernel ALPC primitive. Same post-initial-access posture as CVE-2026-81963 — patch with the next regular Windows update and prioritize hosts that already carry an untrusted local foothold.

## Defender priorities
1. **Patch the two 2026-09-11 pre-auth RCE items first.** Adobe/Magento: apply the **`VULN-39341`** composer hotfix under **APSB26-146** and **rotate the encryption key plus every credential it protected** (the hotfix does not clean an already-compromised store). N-able N-central: upgrade every on-prem instance to **build 2026.3.1.14** (Hotfix 4) immediately.
2. **Hunt before trusting the patch.** Both pre-auth RCEs have been exploited in the wild: hunt the Rust backdoor process names / NTP-shaped UDP/123 C2 and `pub/media/**/*.php` web shells for Magento, and the N-central account-name / API-route / Cloudflare-Tunnel pivots on N-central.
3. **Fold the two Windows LPEs into the September 2026 patch cycle** (due 2026-09-22). They are local, authorized-attacker escalations — treat them as the "what an intruder does next" step. Prioritize domain-joined and internet-exposed Windows hosts, especially any already showing signs of a foothold.
4. **Preserve evidence before cleanup** on covered federal systems (Forensics Triage requirement applies to CVE-2026-75650 and CVE-2026-86218).
5. **Re-check the catalog.** This is the sixth CISA batch within six weeks; CISA is adding entries at a multi-per-day cadence, so the catalog is a standing watch item.

## Assessment limits
- CISA's entries record **ransomware use as unknown** and identify **no actor, infrastructure, or payload** for all four.
- The Windows affected-version list is derived from NVD CPE `versionEndExcluding` values; verify against the Microsoft September 2026 Security Update Guide / relevant KB for your specific builds before declaring a host patched.
- The two Windows LPEs have **no** Microsoft Security Blog write-up published as of capture (latest blog post Sep 4); the KEV + NVD records are the primary public source.
- CVE-2026-86206 / CVE-2026-86207 (N-central Hotfix 3 auth-bypass flaws) are **not** in the KEV catalog; only CVE-2026-86218 was added on September 8.

## Related pages
- [StyleSmuggler: Magento / Adobe Commerce unauthenticated RCE zero-day under active attack — Adobe emergency hotfix VULN-39341 / APSB26-146](stylesmuggler-magento-adobe-commerce-unauth-rce-zero-day-sansec-september-2026.md)
- [N-able N-central CVE-2026-18556 / CVE-2026-18577 exploitation (through CVE-2026-86206 / -86207 / -86218)](n-able-n-central-cve-2026-18556-18577-exploitation.md)
- [CISA KEV September 2, 2026 additions: seven exploited flaws across Artifactory, Kestra, SonicWall SMA1000, LiteLLM, Starlette, and Switchvox](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (2026-09-08 batch) / [catalog JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- NVD: [CVE-2026-75650](https://nvd.nist.gov/vuln/detail/CVE-2026-75650), [CVE-2026-86218](https://nvd.nist.gov/vuln/detail/CVE-2026-86218), [CVE-2026-81963](https://nvd.nist.gov/vuln/detail/CVE-2026-81963), [CVE-2026-85880](https://nvd.nist.gov/vuln/detail/CVE-2026-85880)
- Microsoft Update Guide: [CVE-2026-81963](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-81963), [CVE-2026-85880](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-85880)
- Adobe Security Bulletin APSB26-146 (2026-09-07): [https://helpx.adobe.com/security/products/magento/apsb26-146.html](https://helpx.adobe.com/security/products/magento/apsb26-146.html)
- BOD 26-04: [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
