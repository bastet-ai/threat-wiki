# CISA KEV September 22, 2026: a security-product batch — F5 BIG-IP APM OAuth RCE under active exploitation, the Check Point pair (Gateway VPN cert-validation RCE + Management zero-day), and the VeloCloud row landing

**Category:** ops
**First seen:** 2026-09-22
**Last verified:** 2026-09-22 (this wiki, KEV JSON pulled ~20:41 UTC)

## What happened

CISA moved the KEV catalog for the first time since September 21 — **catalog 2026.09.22, 1,721 entries (+4)** — and the entire batch is **network security products with exploitation evidence**: F5 BIG-IP APM, two Check Point products, and Arista VeloCloud Orchestrator. All four carry compressed **due dates of 2026-09-25** (three-day BOD clock, same compressed posture as the September 18 kernel trio). The Zyxel GS1900 row (Sep 21, due Sep 24) remains the nearest deadline in the catalog.

This batch also **partially clears this wiki's KEV lag queue**: CVE-2026-93952 (VCO) and the Check Point pair were all publicly disclosed/confirmed-exploited before or on the listing date, so the "vendor says exploited, CISA silent" backlog (now just Veeam CVE-2026-32996 + the attribution-less kernel trio) started draining the same day it was recorded here.

## The four rows

| CVE | Product | Mechanism (per vendor) | KEV due | Ransomware |
|---|---|---|---|---|
| CVE-2026-94127 | F5 BIG-IP APM | Heap-based buffer overflow in TMM data plane when an access policy **and an OAuth profile** are configured on a virtual server → unauthenticated RCE | 2026-09-25 | Unknown |
| CVE-2026-93616 | Check Point Security Management (+ MDMS, Log Server, MD Log Server, SmartEvent) | Pre-auth **path traversal → arbitrary-path script execution + arbitrary Java class load** in the management web service — a **zero-day** (first attacks observed July 23, 2026; fix shipped with the advisory) | 2026-09-25 | Unknown |
| CVE-2026-85102 | Check Point Security Gateway / Spark Firewall (Site-to-Site + Remote Access VPN) | **Improper certificate validation during VPN negotiation** → unauthenticated RCE; patched Sep 9, then exploited anyway = **one-day exploitation** | 2026-09-25 | Unknown |
| CVE-2026-93952 | Arista VeloCloud Orchestrator (on-prem) | Improper input validation → privileged internal function access, CVSS 10.0, cert-auth-mode-gated (see [VCO page](arista-velocloud-orchestrator-cve-2026-16812-exploitation.md#september-22-second-vco-flaw-cve-2026-93952)) | 2026-09-25 | Unknown |

NVD status at this wiki's check: **all four "Awaiting Analysis"** — the KEV row is again the earliest authoritative public artifact; patch triggers come from vendor advisories, not the CVE feed.

## F5 CVE-2026-94127 (K000162605)

- CVSS v3.1 **9.8** per F5; **unauthenticated** attacker sends crafted traffic to an exposed virtual server that has an APM access policy + OAuth profile configured; overflow occurs in the **Traffic Management Microkernel (data plane)** — F5 explicitly scopes: "This is a data plane issue; there is no control plane exposure." Appliance mode remains vulnerable.
- **F5 confirms in-the-wild exploitation** in the bulletin ("We have learned that this vulnerability has been exploited"). No public PoC at this wiki's check.
- Affected: BIG-IP 21.1.0, 17.5.0–17.5.1, 17.1.0–17.1.3. Fixes are **engineering hotfixes only** as of Sep 22: `Hotfix-BIGIP-21.1.0.2.0.30.22-ENG`, `Hotfix-BIGIP-17.5.1.9.0.160.12-ENG`, `Hotfix-BIGIP-17.1.3.5.0.41.14-ENG`; an emergency **iRule mitigation** is available from F5 Support for systems that cannot take a hotfix immediately.
- Hunt: repeated OAuth authentication failures in APM logs (F5's own guidance); any APM virtual server exposing an OAuth profile is the exposure inventory question — that config combination, not the version alone, is the triage split.

## Check Point pair (sk1000117 + sk1000171, blog advisory full text captured by this wiki)

Check Point Research published a combined advisory describing **active exploitation of both flaws** — unusual enough to note: a vendor confirming a zero-day AND its own patched flaw being exploited in the same notice.

**CVE-2026-85102 (Security Gateway / Spark, CVSS 9.8, sk1000117):** pre-auth RCE via improper validation of certificate data during **VPN negotiation**. Disclosed and fixed **September 9, 2026 with no evidence of exploitation at the time**; Check Point now observes a **wave of exploitation attempts against Spark customers globally starting September 12** — three days after the fix shipped = textbook one-day window, originating from anonymization infrastructure (VPN services and proxies). **Certificate-subject IoCs observed in attacks** (non-exhaustive by Check Point's own caveat):

- `CN=vpn,OU=users,O=global`
- `CN=vpn-user,OU=users,O=global`
- `CN=vpnuser,OU=users,O=global`

Hunt guidance: anomalous **certificate-based Mobile Access logins** (do not limit to these subjects), then second-stage internal port/service scanning by suspicious logged-in Mobile Access users. Affected trains: R81 (EOS), R81.10 (EOS), R81.10.X, R81.20, R82, R82.00.X, R82.10.

**CVE-2026-93616 (Security Management, CVSS 9.8, sk1000171):** pre-auth path traversal in the management web service → execute a script from an arbitrary path and load an arbitrary Java class. **Zero-day**: "a handful of pinpointed exploitation" observed on **July 23, 2026** — ~two months before the fix shipped — a management-plane vulnerability quietly exploited while unpatched. Affected: R82.20; R82.10 Jumbo ≤ Take 44; R82 Jumbo ≤ Take 126; R81.20 Jumbo ≤ Take 166; R81.10 Jumbo ≤ Take 190 (EoS); R80–R81 (EoS). **Check Point explicitly warns LivePatch Take 28/29 does NOT address this issue** — the second on-wiki case this month (after VCO's fixed-versions-sitting-inside-the-new-range inversion) where the obvious hotfix path leaves you exposed; validate the actual take/build, not the patch level.

**Lineage note:** this is Check Point Security Management's **second actively-exploited KEV-class flaw in one week** — CVE-2026-91843 (login stack overflow → root, sk1000155) was emergency-disclosed September 16 ([page](../tools/check-point-security-management-server-cve-2026-91843-login-stack-overflow-root-rce-september-2026.md)). Two independent pre-auth RCE classes on the same product surface within eight days changes the posture answer for Security Management from "patch promptly" to "assume targeted and manage the exposure" (internet-exposed management interfaces should not exist; check the actual network ACL, not the intent).

## Durable reads

1. **One-day and zero-day exploitation of security appliances is now routine, not exceptional.** Check Point's own timeline (patched flaw exploited three days after fix; unpatched flaw quietly exploited ~two months before fix) shows both ends of the exploitation clock firing in the same week.
2. **Certificate subjects are cheap, durable IoCs** — the `CN=vpn*,OU=users,O=global` set costs the attacker nothing to change but retroactively grades every Mobile Access login log; index certificate-subject fields from VPN appliances now, before the next set lands.
3. **The exposure unit is the configuration combination, not the version**: APM policy + OAuth profile (F5), certificate-auth Edge mode (Arista), management-web-service reachability (Check Point). Inventory by config.
4. **"Fixed" is per-CVE and per-take, not per-product** — VCO's July fixes sit inside September's affected range; Check Point's LivePatch Take 28/29 explicitly does not carry this fix. Re-read affected/take tables per incident.

## State at this wiki's check (Sep 22 ~20:41 UTC)

- KEV JSON: 2026.09.22, **1,721** rows; the four Sep 22 rows all due **2026-09-25**; Zyxel CVE-2026-7273 due 2026-09-24 remains the nearest deadline.
- Lag queue remaining: **Veeam CVE-2026-32996** (Arctic Wolf confirmed active exploitation, no KEV row) and the **Sep 18 kernel trio** (attribution-less, day six).
- No actor attribution on any of the four rows; ransomware flag Unknown on all four.

## Sources

- CISA KEV JSON (this wiki pull, Sep 22 ~20:41 UTC): <https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>
- Check Point Research advisory (full text captured by this wiki, Sep 22): <https://blog.checkpoint.com/security/security-advisory-action-required-active-exploitation-of-cve-2026-85102-and-a-management-pre-authentication-vulnerability-cve-2026-93616/>
- Check Point SKs: <https://support.checkpoint.com/results/sk/sk1000117> (CVE-2026-85102), <https://support.checkpoint.com/results/sk/sk1000171> (CVE-2026-93616)
- F5 K-series: <https://my.f5.com/manage/s/article/K000162605> (SPA — not retrievable at capture; hotfix/affected detail via SecurityOnline.info Sep 22 secondary, full text captured: <https://securityonline.info/big-ip-apm-vulnerability-cve-2026-94127/>)
- NVD records (all "Awaiting Analysis"): CVE-2026-94127, CVE-2026-93616, CVE-2026-85102, CVE-2026-93952
- Arista advisory 0144: <https://www.arista.com/en/support/advisories-notices/security-advisory/24364-security-advisory-0144>
- Canadian Cyber Centre AL26-022 (F5 APM): <https://www.cyber.gc.ca/en/alerts-advisories/al26-022-vulnerability-impacting-f5>

## Related pages

- [Arista VeloCloud Orchestrator CVE-2026-16812 + Sep 22 CVE-2026-93952 page](arista-velocloud-orchestrator-cve-2026-16812-exploitation.md)
- [Check Point Security Management CVE-2026-91843 (September 16)](../tools/check-point-security-management-server-cve-2026-91843-login-stack-overflow-root-rce-september-2026.md)
- [September 18 KEV Linux kernel trio](cisa-kev-linux-kernel-af-alg-ebtables-september-18-2026.md)
- [Veeam Agent CVE-2026-32996 (KEV queue, active exploitation)](../tools/veeam-agent-windows-cve-2026-32996-session-uid-log-leak-system-lpe-active-exploitation-arcticwolf-september-2026.md)
