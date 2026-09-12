# CISA KEV September 10–11, 2026 additions: six exploited flaws — ConnectWise ScreenConnect client file-execution, two JFrog Artifactory auth flaws, GitLab unauth file read, and two MikroTik RouterOS flaws

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- ConnectWise
- ScreenConnect
- CWE-269
- CWE-862
- CVE-2026-84869
- JFrog
- Artifactory
- authentication bypass
- CWE-287
- CWE-863
- CVE-2026-42016
- CVE-2026-42018
- GitLab
- path traversal
- CWE-22
- CVE-2026-85706
- MikroTik
- RouterOS
- SSH
- command injection
- CWE-88
- CWE-306
- CVE-2026-86060
- CVE-2026-67277

## Summary
On **September 10 and 11, 2026**, CISA added **six** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog (catalog `2026.09.11`, 1,709 entries):

| CVE | Product | Class | CVSS | CWE | Forensics triage | BOD 26-04 due |
|---|---|---|---|---|---|---|
| **CVE-2026-84869** | ConnectWise ScreenConnect (client) | **Improper privilege management / missing authorization** — files transferred and executed through an active remote session without authorization or host confirmation | **9.9 Critical** (CVSS v3.1, S:C) | CWE-269, CWE-862 | **Yes** | **2026-09-14** |
| **CVE-2026-42016** | JFrog Artifactory (self-hosted) | **Incorrect authorization / token-scope validation** — low-privilege token used to perform unauthorized, elevated actions | **8.1 High** (CVSS v3.1) | CWE-863 | **Yes** | **2026-09-25** |
| **CVE-2026-42018** | JFrog Artifactory (self-hosted) | **Improper authentication** — returns the internal anonymous-user token to an unauthenticated caller even when anonymous access is disabled | **7.5 High** (CVSS v3.1) | CWE-287 | **Yes** | **2026-09-25** |
| **CVE-2026-85706** | GitLab CE/EE | **Path traversal** in the repository commits API — unauthenticated arbitrary-file read; improper path confinement + missing authentication enforcement | **10.0 Critical** (CVSS v3.1, S:C) | CWE-22 | **Yes** | **2026-09-14** |
| **CVE-2026-86060** | MikroTik RouterOS | **Argument-delimiter handling flaw in the SSH login path** — username beginning with a prohibited character changes the trusted policy mask, leading to privilege escalation | **9.2 High** (CVSS v4.0) | CWE-88 | **Yes** | **2026-09-13** |
| **CVE-2026-67277** | MikroTik RouterOS | **Missing authentication for critical function** — a "related" btest connection is accepted before the primary session completes authentication; unauthenticated client can start an IPv4 UDP test that transmits an uninitialized kernel-packet-buffer tail and can restart the RouterOS kernel | **8.8 High** (CVSS v4.0) | CWE-306 | **Yes** | **2026-09-13** |

All six carry the **BOD 26-04** remediation requirement. CISA records **ransomware use as unknown** for all six and names **no actor, infrastructure, or payload** on the catalog entries. The two **2026-09-13** MikroTik entries and the **2026-09-14** ConnectWise / GitLab entries are the priority items; the two **2026-09-25** JFrog Artifactory entries are part of an active in-the-wild exploitation chain documented by Wiz (see related page).

## ConnectWise ScreenConnect CVE-2026-84869 (due 2026-09-14)
- **Fixed in ScreenConnect 26.6.5** (security patch dated 09/08/2026; ConnectWise severity "Important," **Priority 1 High** — "either being targeted or have higher risk of being targeted by exploits in the wild").
- ConnectWise: "a condition in the ScreenConnect client that may allow files to be transferred and executed through an active remote session without authorization or Host confirmation in certain circumstances. **ScreenConnect servers are not impacted.**"
- **Cloud:** no action required, but after upgrading reinstall host clients and update access agents. **On-prem:** upgrade to 26.6.5 (requires a valid on-prem license); if out of maintenance, upgrade the license first. Interim mitigation (not a substitute): Administration → Security → Roles → deselect **TransferFiles** (or **TransferFilesInSession** in legacy environments) in each affected session group.
- This is the **CVE + fixed build** that the Huntress Sep 3 rogue-ScreenConnect / guest-file-transfer campaign and ConnectWise's Sep 3 "Guest File Transfer Advisory" had been tracking (the advisory had no CVE ID or fixed build until this Sep 8 bulletin / Sep 11 KEV listing).
- Durable tell (from the Huntress chain): ScreenConnect audit-log **`RunFiles` / `RanFiles` entries executed from `Process: Guest`**.

## JFrog Artifactory CVE-2026-42016 / CVE-2026-42018 (due 2026-09-25)
- Both are **self-hosted** Artifactory flaws. See the dedicated in-the-wild page for the full chained exploitation, `token:anonymous` actor tell, Groovy-plugin / Rust-backdoor post-exploitation, and exposure telemetry.
- **CVE-2026-42018** (CWE-287): unauthenticated caller gets the internal anonymous-user token even with anonymous access disabled. **CVE-2026-42016** (CWE-863): that token is then escalated to admin scope because Artifactory validates the token's signature/issuer but not its scope.
- Fixed in 7.133.11+ (42016) and the corrected JFrog advisory builds (42018, per the Sep 11 change log). CVE-2026-82329 (the default-config auth bypass to admin) has been in KEV since Sep 2 and is the third exploited flaw in ~30 days against this product family.

## GitLab CVE-2026-85706 (due 2026-09-14)
- **Unauthenticated arbitrary-file read** via the **repository commits API**: improper path confinement + missing authentication enforcement. Reported by `s3ntago` via HackerOne.
- **Impacted versions:** all GitLab CE/EE from **18.7 before 19.1.8**, **19.2 before 19.2.6**, and **19.3 before 19.3.2**. Fixed in the **Critical Patch Release 19.3.2 / 19.2.6 / 19.1.8** (released **September 10, 2026**).
- CVSS 10.0 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N`). The same critical patch release also fixed CVE-2026-87719 (insecure deserialization in the GraphQL subscription serializer, EE) and a batch of other flaws; this is the one CISA listed as actively exploited.

## MikroTik RouterOS "MikroTrick" — CVE-2026-86060 / CVE-2026-67277 (due 2026-09-13)
- Reported by **CERT.pl**; issue codename **"MikroTrick"** (the full issue codename covers CVE-2026-67276, CVE-2026-86060, and CVE-2026-67277; CISA listed the two above).
- **Fixed in:** **6.49.21** (long-term), **7.23.4** (long-term), and **7.24.2** (stable).
- **CVE-2026-86060** (CWE-88, 9.2 v4.0): argument-handling flaw in the SSH login path — usernames that begin with a prohibited character let an unauthenticated SSH session change the trusted RouterOS policy mask, leading to privilege escalation.
- **CVE-2026-67277** (CWE-306, 8.8 v4.0): RouterOS accepts a "related" btest connection before the primary session completes authentication; an unauthenticated client can start an IPv4 UDP test, and with `random-data=false` the sender transmits an uninitialized tail from a kernel packet buffer; an unchecked, inverted packet-size interval causes an unsigned integer underflow, anomalously large fragmented output, and can restart the RouterOS kernel.
- **Vendor guidance:** make sure **SSH is not open to untrusted networks** (default blocks it from the internet; use WireGuard / a VPN and do not open management ports). RouterOS will flag a compromised device to **"Flagged" status** (written to the Log); even if not flagged, after upgrading inspect the configuration for **unknown scripts, users, or other unrecognized config**.

## Defender takeaways
- **MikroTik and ScreenConnect are the two with the nearest BOD 26-04 deadlines (2026-09-13 / 2026-09-14)** and the most operational exposure: RouterOS is ubiquitously internet-facing edge gear, and ScreenConnect's client file-execution path is a proven initial-access vector (see the Sep 3 Huntress worm-like propagation chain).
- **JFrog Artifactory:** patch to the corrected builds, then **hunt the `token:anonymous` actor** and remove any persistent admin account / malicious Groovy plugin; treat the host as compromised if the chain was observed.
- **GitLab:** move self-managed CE/EE to 19.1.8 / 19.2.6 / 19.3.2; audit the repository commits API for unauthenticated file-read attempts.
- **MikroTik:** upgrade to 6.49.21 / 7.23.4 / 7.24.2, confirm the device is not in "Flagged" status, and review config for unknown scripts/users; keep SSH out of untrusted networks.
- **ConnectWise:** on-prem ScreenConnect must move to 26.6.5 and clients must be reinstalled; the `TransferFiles` role-permission stopgap is the interim control until the patch lands.

## Related pages
- [Wiz "Artifactory Under Attack": in-the-wild exploitation chains in JFrog Artifactory (CVE-2026-42016 / -42018 / -82329)](wiz-artifactory-in-the-wild-cve-2026-42016-42018-82329-september-2026.md)
- [CISA KEV September 2, 2026: JFrog Artifactory unauth admin access (CVE-2026-82329)](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)
- [Rogue ScreenConnect installations across unrelated hosts: worm-like VBS propagation via guest file transfer (Huntress, Sep 3)](screenconnect-rogue-install-worm-like-vbs-propagation-huntress-september-2026.md)
- [ConnectWise ScreenConnect exploitation wave](connectwise-screenconnect-exploitation-wave.md)

## Sources
- CISA KEV catalog, version **2026.09.11** (1,709 entries): [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- ConnectWise: [ScreenConnect 26.6.5 Security Patch / CVE-2026-84869](https://www.connectwise.com/company/trust/security-bulletins/2026-09-08-screenconnect-bulletin) (dated 09/08/2026)
- JFrog: [Security Advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories)
- GitLab: [Critical Patch Release 19.3.2 / 19.2.6 / 19.1.8](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-3-2-released/) (September 10, 2026)
- MikroTik: [September 2026 Vulnerability — "MikroTrick"](https://mikrotik.com/supportsec/september-2026-vulnerability/)
- NVD: [CVE-2026-84869](https://nvd.nist.gov/vuln/detail/CVE-2026-84869), [CVE-2026-42016](https://nvd.nist.gov/vuln/detail/CVE-2026-42016), [CVE-2026-42018](https://nvd.nist.gov/vuln/detail/CVE-2026-42018), [CVE-2026-85706](https://nvd.nist.gov/vuln/detail/CVE-2026-85706), [CVE-2026-86060](https://nvd.nist.gov/vuln/detail/CVE-2026-86060), [CVE-2026-67277](https://nvd.nist.gov/vuln/detail/CVE-2026-67277)
