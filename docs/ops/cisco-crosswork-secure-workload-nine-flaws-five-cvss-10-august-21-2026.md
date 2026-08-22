# Cisco Crosswork and Secure Workload: nine flaws patched, five scoring CVSS 10.0

## Summary
On August 21, 2026, Cisco published a further round of security updates for **Crosswork** platforms and **Secure Workload** as part of a **continued comprehensive internal security review** that has produced "software hardening releases that address multiple internally discovered vulnerabilities." **Four flaws** affect Crosswork Data Gateway, Crosswork Network Controller, and Crosswork Planning **regardless of device configuration** (fixed in Crosswork **7.2.1-SP**, affecting ≤7.2.1), and **five flaws** affect Secure Workload SaaS and on-premises deployments (≤3.10 fixed in **3.10.9.1**; 4.0 fixed in **4.0.4.16**). Five of the nine score **CVSS 10.0**. Cisco stated the flaws "were found during internal testing and are **not known to be actively exploited**." The round follows, roughly two weeks later, the same review's resolution of **12 bugs in Catalyst SD-WAN and IOS XE Software**, and the same month's in-the-wild exploitation of **CVE-2026-20349** (CVSS 8.6) in Secure Firewall ASA/FTD — underscoring that the review's internally found flaws coexist with flaws that *are* being exploited.

## Tags
- ops
- Cisco
- Crosswork
- Crosswork Data Gateway
- Crosswork Network Controller
- Crosswork Planning
- Secure Workload
- internal security review
- SQL injection
- missing authentication
- improper access control
- path traversal
- buffer overflow
- patching
- CVSS 10.0
- no active exploitation

## Affected flaws
**Crosswork (4 flaws; affect Data Gateway / Network Controller / Planning regardless of configuration; release ≤7.2.1, fixed in 7.2.1-SP):**
- **CVE-2026-20030** (CVSS **10.0**) — SQL injection vulnerability
- **CVE-2026-20357** (CVSS **10.0**) — missing authentication for a critical function
- **CVE-2026-20358** (CVSS **10.0**) — external control of file system
- **CVE-2026-20359** (CVSS **9.9**) — insufficiently protected credentials

**Secure Workload (5 flaws; SaaS + on-premises; ≤3.10 fixed in 3.10.9.1, 4.0 fixed in 4.0.4.16):**
- **CVE-2026-20231** (CVSS **9.9**) — improper neutralization of special elements (command, OS, and argument injection)
- **CVE-2026-20315** (CVSS **10.0**) — improper access control (authorization, authentication, privileges, bypasses)
- **CVE-2026-20317** (CVSS **10.0**) — improper authentication (missing authentication, authentication bypass, reliance on untrusted inputs)
- **CVE-2026-20318** (CVSS **9.6**) — improper input validation (input validation, path traversal, external path control)
- **CVE-2026-20319** (CVSS **7.5**) — improper restriction of operations within memory buffer bounds (buffer overflows, out-of-bounds writes)

## Coverage and correlation
- This is the **second round** of the same internal security review, which in early August produced fixes for **12 Catalyst SD-WAN / IOS XE flaws** and is the same review under which Cisco's **CVE-2026-20316** Secure FMC static-credential flaw ([page](../ops/cisco-fmc-cve-2026-20316-static-credential-exploitation.md)) was being actively exploited. The pattern to watch: Cisco's internally-found hardening CVEs are released ahead of exploitation, but the company's product estate also carries actively exploited flaws, so **patch-currency across the whole estate** — not just the flagged products — is the durable control.
- No exploit code, actor, or infrastructure is associated with these nine flaws; they are **not in CISA KEV** as of this scan.

## Defender priorities
- **Patch Crosswork to 7.2.1-SP** and **Secure Workload to 3.10.9.1 / 4.0.4.16** for all SaaS and on-prem deployments; the four Crosswork flaws apply "regardless of device configuration," so no configuration workaround exists.
- Prioritize the **CVSS 10.0** set (20030, 20357, 20358, 20315, 20317) — SQL injection, missing authentication, and access-control flaws on management/control-plane products are the most likely candidates if exploitation emerges.
- Track whether any of these nine enter CISA KEV; if so, reclassify from patch-now to patch-and-hunt.

## Assessment limits
- "Not known to be actively exploited" is Cisco's statement as of the August 21, 2026 release; absence of exploitation is time-bounded.
- No KEV listing, exploit tooling, or actor attribution exists as of this scan.

## Related pages
- [Cisco Secure FMC CVE-2026-20316 static-credential exploitation](../ops/cisco-fmc-cve-2026-20316-static-credential-exploitation.md)

## Sources
- The Hacker News: [Cisco Patches Nine Crosswork and Secure Workload Flaws, Five Scoring CVSS 10.0](https://thehackernews.com/2026/08/cisco-patches-nine-crosswork-and-secure.html) (Ravie Lakshmanan, August 21, 2026)
