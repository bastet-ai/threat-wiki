# CISA KEV August 27, 2026 additions: ownCloud WebDAV pre-signed URL bypass, Linux kernel IPv6 LPE, and JFrog Artifactory Docker-cache path escape

## Summary
On **August 27, 2026**, CISA added **three** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog:

| CVE | Product | Class | NVD / vendor severity | BOD 26-04 due |
|---|---|---|---|---|
| **CVE-2023-49105** | ownCloud Server (< 10.13.3) | unauthenticated file access/modify/delete via WebDAV pre-signed URLs (improper authentication) | 2023-era CVE; CISA CWE-287 | **2026-08-30** |
| **CVE-2026-53362** | Linux kernel | privilege escalation via the IPv6 networking subsystem | kernel fix commits published 2026-07-04 | **2026-08-30** |
| **CVE-2026-66384** | JFrog Artifactory (< 7.146.35 / 7.161.0–7.161.16) | authenticated write outside the intended Docker cache path under remote-repository conditions (CWE-22) | vendor: Medium (NVD published 2026-08-12) | **2026-09-10** |

All three carry the **BOD 26-04** remediation requirement plus the Forensics Triage requirement for covered federal systems. CISA records **ransomware use as unknown** for all three and names **no actor, infrastructure, or payload** on the catalog entries.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- ownCloud
- WebDAV
- pre-signed URL
- authentication bypass
- CVE-2023-49105
- Linux kernel
- IPv6
- local privilege escalation
- CVE-2026-53362
- JFrog
- Artifactory
- path traversal
- Docker cache
- CVE-2026-66384

## The three entries

### CVE-2023-49105 — ownCloud WebDAV pre-signed URL authentication bypass
CISA's entry: an **improper authentication vulnerability** in ownCloud that "allows an attacker to access, modify, or delete any file **without authentication** if the username of a victim is known, and the victim has **no signing-key configured**." CWE-287 (CISA's catalog record).

- **KEV entry:** added 2026-08-27; **BOD 26-04 due 2026-08-30** (three days out).
- **Vendor posture:** ownCloud's security update page scopes the issue to **ownCloud Server below 10.13.3** (upgrade path; a support patch exists for subscription customers), part of a broader ownCloud 10 security update that also covers GraphAPI, crafted redirect URLs, and unauthorized file access issues (including CVE-2023-49103 / CVE-2023-49104). ownCloud Infinite Scale and managed services are not affected.
- **Mechanism:** the WebDAV API honors **pre-signed URLs** in a way that permits unauthenticated file access/modify/delete when the target victim's username is known and that victim has no signing key configured — a 2023-disclosed flaw now carrying an independent known-exploited determination.
- **Context:** ownCloud is a common on-prem file-collaboration platform in European public-sector and SMB estates; a KEV listing with a three-day deadline makes every unpatched sub-10.13.3 instance a patch-now target. This is a **2023 CVE resurfacing as a 2026 exploitation determination**, not a one-day.

### CVE-2026-53362 — Linux kernel IPv6 privilege escalation
CISA's entry: an unspecified vulnerability in the **Linux kernel** that "can allow for **privilege escalation via IPv6 networking subsystem**," impacting products "including but not limited to Suse, Red Hat, and other products using Linux."

- **KEV entry:** added 2026-08-27; **BOD 26-04 due 2026-08-30**.
- **Upstream:** NVD (published 2026-07-04) links the fix to the kernel commit "ipv6: account for fraggap on the paged allocation path" (`__ip6_append_data()` paged-allocation branch, `MSG_MORE` case); CISA's entry additionally cites six stable-tree backport commits, indicating the fix has already propagated across stable branches and distro kernels since early July.
- **Context:** a kernel LPE in the network path is the classic escalation step *after* any initial access; CISA listing it as exploited means unpatched kernels on internet-reachable hosts should be treated as an active lateral-movement / root-escalation target. No distro-specific unpatched version was stated on the KEV entry; vendor (Red Hat / SUSE) advisories and stable-tree backports define the exact affected builds.

### CVE-2026-66384 — JFrog Artifactory Docker-cache path escape
CISA's entry: an **improper limitation of a pathname to a restricted directory** in JFrog Artifactory that "can allow an **authenticated user** to **write data outside the intended Docker cache path** under specific remote-repository conditions." CWE-22 (path traversal).

- **KEV entry:** added 2026-08-27; **BOD 26-04 due 2026-09-10**.
- **Vendor advisory (JFrog Security Advisories, published 2026-08-12):** Medium severity. Affected: **Artifactory < 7.146.35** (fix 7.146.35) and **7.161.0 → 7.161.16** (fix 7.161.16). **JFrog Cloud environments are already fortified** — the actionable scope is **self-managed (self-hosted) Artifactory**. Same release train also fixes companion flaws (e.g., CVE-2026-66375 low-privilege protected-metadata removal, High).
- **Context:** an authenticated path-traversal write on a build-artifact platform is a high-value primitive: the ability to write outside the Docker cache path is the pre-condition for arbitrary file write → service-account code execution on a host that typically has broad repository/registry and CI credentials. The **authenticated** prerequisite means the realistic kill chain is stolen/low-privilege Artifactory credentials → cache-path escape → host compromise; pair with credential hygiene on the Artifactory instance.

## Defender priorities
1. **Patch the two August 30 deadlines first.** ownCloud Server instances below 10.13.3: upgrade (or apply the subscription patch) and configure signing keys where available; audit for unauthenticated WebDAV access and pre-signed URL abuse. Linux kernels: confirm you are on a stable/distro kernel containing the July 2026 IPv6 backport; treat any initial-access host as an active LPE target until patched.
2. **Self-managed Artifactory:** upgrade to 7.146.35 / 7.161.16 (or later). Cloud instances are already fortified. Hunt for authenticated write attempts outside the Docker cache path and review Artifactory user/role hygiene.
3. **Treat the KEV listing as independent of attribution.** CISA names no actor on any of the three; correlate to your own threat model rather than assuming a named campaign.
4. **Preserve evidence before cleanup** on covered federal systems (BOD 26-04 Forensics Triage requirement applies to all three).
5. **Re-check the catalog.** The August 26 batch added Citrix NetScaler / SQL Server / UAT-10147 CVEs (see the [August 26 page](cisa-kev-citrix-sql-server-august-26-2026.md)); CISA is now adding entries at a multi-per-day cadence, so the catalog is a standing watch item, not a one-time digest.

## Assessment limits
- CISA's entries record **ransomware use as unknown** and identify **no actor, infrastructure, or payload** for all three.
- CVE-2023-49105 is a **2023** disclosure (NVD published 2023-11-21) resurfacing as a 2026 exploitation determination; ownCloud's FAQ is the authoritative affected-version source (Server < 10.13.3).
- For CVE-2026-53362, CISA's entry cites stable-tree commits but no vendor-affected-version matrix; distro advisories define the exact unpatched builds.
- For CVE-2026-66384, the vendor severity is **Medium** with an **authenticated** prerequisite; the KEV listing establishes exploitation, but the KEV entry does not state the exploitation scope (which remote-repository conditions).

## Related pages
- [CISA KEV August 26, 2026 additions: Citrix NetScaler DoS, Microsoft SQL Server RCE, and four UAT-10147 CVEs](cisa-kev-citrix-sql-server-august-26-2026.md)
- [Gitea diffpatch Git-hook RCE in CISA KEV (CVE-2026-60004)](gitea-cve-2026-60004-diffpatch-git-hook-rce-kev-august-25-2026.md)
- [Zimbra SNMP command injection in CISA KEV; Microsoft patches Entra ID deserialization flaw](cisa-kev-microsoft-entra-zimbra-august-21-2026.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (2026-08-27 batch) / [catalog JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- ownCloud security update FAQ: [https://owncloud.org/security](https://owncloud.org/security); advisory: [WebDAV API authentication bypass using pre-signed URLs](https://owncloud.com/security-advisories/webdav-api-authentication-bypass-using-pre-signed-urls/)
- NVD: [CVE-2023-49105](https://nvd.nist.gov/vuln/detail/CVE-2023-49105), [CVE-2026-53362](https://nvd.nist.gov/vuln/detail/CVE-2026-53362), [CVE-2026-66384](https://nvd.nist.gov/vuln/detail/CVE-2026-66384)
- JFrog Security Advisories (CVE-2026-66384): [https://docs.jfrog.com/releases/docs/jfrog-security-advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories)
- Linux kernel fix commit: [https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962](https://git.kernel.org/stable/c/14200d435af9a9eeb444f529fc2f689a236b7962)
- BOD 26-04: [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
