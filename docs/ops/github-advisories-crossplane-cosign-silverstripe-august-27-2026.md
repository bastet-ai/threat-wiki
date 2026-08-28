# GitHub Security Advisories August 27, 2026: Crossplane cosign signature-verification bypass and Silverstripe RCE batch

## Summary
On **August 27, 2026**, four GitHub Security Advisories were published with durable defender value: one **Crossplane** supply-chain / signature-verification bypass and a three-CVE **Silverstripe** batch (two high-severity RCEs and one medium XSS).

| Advisory | Product | Class | Severity | Fix |
|---|---|---|---|---|
| **GHSA-mf7q-r4rv-jv94** | Crossplane / `crossplane-runtime/v2` | cosign signature-verification TOCTOU bypass on tag-based package install | **High** (no CVE) | v2.3.3 / v2.2.3 (main) ; rc.1 for the 2.4.0-rc.0 range |
| **GHSA-39mm-rwm3-29jp / CVE-2026-54718** | `symbiote/silverstripe-advancedworkflow` | RCE via advanced-workflow **email template** | **High** | 6.4.5 / 7.1.3 / 7.2.1 |
| **GHSA-g8wr-r2v2-vqc6 / CVE-2026-54721** | `silverstripe/userforms` | RCE via **email subject** | **High** | 6.4.9 / 7.0.7 / 7.1.1 |
| **GHSA-gvrw-qqp5-jgc5 / CVE-2026-54720** | `silverstripe/framework` | **XSS** via media embed | **Medium** | 6.2.2 |

No exploitation, actor, infrastructure, or payload detail is named in any of the four advisories.

## Tags
- ops
- supply chain
- signature verification
- cosign
- OCI registry
- TOCTOU
- time-of-check time-of-use
- tag-based install
- Crossplane
- crossplane-runtime
- GHSA-mf7q-r4rv-jv94
- Silverstripe
- RCE
- email template
- email subject
- XSS
- media embed
- CVE-2026-54718
- CVE-2026-54721
- CVE-2026-54720
- GitHub Security Advisories

## Crossplane cosign signature-verification bypass (GHSA-mf7q-r4rv-jv94)
Crossplane can be configured to verify that packages are signed before pulling and installing them, using **cosign**. The bypass is a **time-of-check / time-of-use (TOCTOU)** flaw in `xpkg.CachedClient`:

- When a package is installed using a **tag reference** (a semantic version) rather than a **digest**, Crossplane resolves the tag reference **separately for each step** — once for signature verification, again for the actual image fetch.
- A **malicious or compromised OCI registry** can therefore serve a **correctly signed image for verification**, then serve a **different, unsigned (or attacker-controlled) image for installation**. The signature check passes on content that is not the content that gets installed.

**Relevant only when all three hold:**
1. Package signature verification is configured.
2. Packages are installed using **tag references, not digests**.
3. Packages are pulled from **registries the operator does not control**.

**Affected:** `github.com/crossplane/crossplane-runtime/v2` — `= 2.4.0-rc.0` (patched `2.4.0-rc.1`) and `>= 2.3.0, <= 2.3.2` (patched `2.3.3`). The fix was applied to `main` and backported to the v2.3 and v2.2 release branches (releasing as **v2.3.3** and **v2.2.3**).

**Mitigation without the patch:** install packages **by image digest** rather than by tag, so the content that is verified is the content that is installed.

**CWE:** CWE-345 (Insufficient Verification of Data Authenticity), CWE-367 (TOCTOU Race Condition). Independently reported by `@bugbunny-research` and `@tonghuaroot`. **No CVE has been assigned** as of publication.

**Why it matters:** Crossplane is a control-plane for Kubernetes-native infrastructure; a signature-verification control that can be silently defeated at install time converts a trusted registry relationship into a supply-chain injection vector. The durable pattern — *the signed artifact and the installed artifact need not be the same object when resolution is not pinned* — is the same trust-boundary failure class seen in package-manager tag-vs-digest handling across ecosystems.

## Silverstripe RCE batch (CVE-2026-54718 / -54721 / -54720)
Silverstripe published coordinated security releases on August 27, 2026. The two high-severity items are **remote code execution** reachable through the email-processing paths of two common add-ons:

- **CVE-2026-54718** (GHSA-39mm-rwm3-29jp, **High**) — `symbiote/silverstripe-advancedworkflow`: RCE via the advanced-workflow **email template**. Affected: `< 6.4.5` (fix 6.4.5), `>= 7.0.0, < 7.1.3` (fix 7.1.3), `>= 7.2.0, < 7.2.1` (fix 7.2.1).
- **CVE-2026-54721** (GHSA-g8wr-r2v2-vqc6, **High**) — `silverstripe/userforms`: RCE via the **email subject** of a user form. Affected: `< 6.4.9` (fix 6.4.9), `>= 7.0.0, < 7.0.7` (fix 7.0.7), `>= 7.1.0, < 7.1.1` (fix 7.1.1).
- **CVE-2026-54720** (GHSA-gvrw-qqp5-jgc5, **Medium**) — `silverstripe/framework`: **XSS** through the **media embed** component. Affected: `< 6.2.2` (fix 6.2.2).

**Why it matters:** Silverstripe is a widely deployed PHP content-management framework; the advancedworkflow and userforms modules are extremely common in production sites. Email-subject and email-template RCE means an attacker who can influence a workflow-triggered or form-submitted email can reach code execution on the host running the CMS. Patch all three on any Silverstripe site; prioritize the two RCEs.

## Defender priorities
1. **Crossplane:** if you verify package signatures *and* install by tag *and* pull from registries you do not control, upgrade `crossplane-runtime/v2` to **v2.3.3 / v2.2.3** (or `2.4.0-rc.1` for the RC range), or pin installs **by digest**. Inventory whether signature verification is enabled and whether installs use tags vs. digests.
2. **Silverstripe:** on every Silverstripe site, update `silverstripe/framework` to **≥ 6.2.2**, `symbiote/silverstripe-advancedworkflow` to the applicable fixed release (6.4.5 / 7.1.3 / 7.2.1), and `silverstripe/userforms` to the applicable fixed release (6.4.9 / 7.0.7 / 7.1.1). The two RCEs are the priority; the XSS is lower urgency but in the same release train.
3. **Treat as unattributed.** None of the four advisories names an actor, infrastructure, payload, or exploitation. Correlate to your own exposure model rather than assuming a campaign.
4. **Watch for CVE backfill** on the Crossplane advisory (currently no CVE) and for exploitation telemetry on the Silverstripe email-path RCEs.

## Assessment limits
- GHSA-mf7q-r4rv-jv94 is rated **High** with **no CVSS vector / score and no CVE** at publication; the three prerequisite conditions (signature verification enabled + tag-based install + untrusted registry) gate real-world impact.
- The Crossplane fix is confirmed in `main` and backported; v2.3.3 / v2.2.3 are the named release targets.
- The Silverstripe advisories carry no in-the-wild exploitation indicator; severity is from the advisories' own classification.

## Related pages
- [npm `bin`-entry dependency confusion](../patterns/npm-bin-entry-dependency-confusion.md)
- [Chainlit MCP unauthenticated RCE/SSRF (CVE-2026-45018 / -45019)](../tools/chainlit-mcp-cve-2026-45018-45019-mcp-rce-ssrf.md)
- [CISA KEV August 27, 2026 additions (ownCloud / Linux kernel / JFrog Artifactory)](cisa-kev-owncloud-linux-artifactory-august-27-2026.md)

## Sources
- GitHub Security Advisory: [GHSA-mf7q-r4rv-jv94 — Crossplane cosign signature-verification bypass](https://github.com/advisories/GHSA-mf7q-r4rv-jv94)
- GitHub Security Advisory: [GHSA-39mm-rwm3-29jp — silverstripe-advancedworkflow RCE (CVE-2026-54718)](https://github.com/advisories/GHSA-39mm-rwm3-29jp)
- GitHub Security Advisory: [GHSA-g8wr-r2v2-vqc6 — silverstripe/userforms RCE (CVE-2026-54721)](https://github.com/advisories/GHSA-g8wr-r2v2-vqc6)
- GitHub Security Advisory: [GHSA-gvrw-qqp5-jgc5 — Silverstripe Framework XSS (CVE-2026-54720)](https://github.com/advisories/GHSA-gvrw-qqp5-jgc5)
- Silverstripe security releases: [CVE-2026-54718](https://www.silverstripe.org/download/security-releases/cve-2026-54718), [CVE-2026-54721](https://www.silverstripe.org/download/security-releases/cve-2026-54721), [CVE-2026-54720](https://www.silverstripe.org/download/security-releases/cve-2026-54720)
