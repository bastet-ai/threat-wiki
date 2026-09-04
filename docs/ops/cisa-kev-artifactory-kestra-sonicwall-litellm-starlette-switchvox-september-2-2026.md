# CISA KEV September 2, 2026 additions: seven exploited flaws across Artifactory, Kestra, SonicWall SMA1000, LiteLLM, Starlette, and Switchvox

## Summary
On **September 2, 2026**, CISA added **seven** vulnerabilities to the Known Exploited Vulnerabilities (KEV) catalog:

| CVE | Product | Class | NVD severity | BOD 26-04 due |
|---|---|---|---|---|
| **CVE-2026-82329** | JFrog Artifactory (self-managed; 7.111.4–7.117.27 / 7.125.0–7.125.19 / 7.133.0–7.133.28 / 7.146.0–7.146.36 / 7.161.0–7.161.19) | authentication weakness; unauthenticated attacker with network access may obtain **administrative privileges under default configuration** | **9.8 Critical** | **2026-09-05** |
| **CVE-2026-49869** | Kestra OSS (< 1.0.45 / < 1.3.21) | OS command injection via auth-filter path suffix-match bypass → unauthenticated arbitrary workflow execution → **RCE as root in the worker container** (script plugins enabled by default) | **10.0 Critical** | **2026-09-05** |
| **CVE-2026-83548** | SonicWall SMA1000 (SNWLID-2026-0016) | **pre-authentication SSRF** in the SMA1000 Appliance Work Place interface via an unintended alternate access path | **10.0 Critical** | **2026-09-05** |
| **CVE-2026-83549** | SonicWall SMA1000 (SNWLID-2026-0016) | post-authentication OS command injection in the Appliance Management Console (AMC); authenticated attacker as administrator → arbitrary OS commands / RCE | 7.8 High | **2026-09-05** |
| **CVE-2026-59822** | BerriAI LiteLLM (pip; < 1.84.0) | improper authentication — MCP gateway OAuth2-passthrough fallback replaces failed key validation with an empty `UserAPIKeyAuth()`; any Bearer token grants full MCP access | High | **2026-09-16** |
| **CVE-2026-48710** | Kludex Starlette (pip; ≤ 1.0.0) | HTTP request/response smuggling — unvalidated `Host` header poisons `request.url.path`, bypassing path-based security checks | 6.5 Medium | **2026-09-16** |
| **CVE-2026-9586** | Sangoma Switchvox SMB Edition 8.3 (104997) | **unauthenticated SQL injection** at `/pa`: `<PolycomIPPhone>` XML `PhoneIP` concatenated unsanitized into PostgreSQL queries → arbitrary SQL / RCE | 9.3 Critical | **2026-09-05** |

All seven carry the **BOD 26-04** remediation requirement plus the Forensics Triage requirement for covered federal systems. CISA records **ransomware use as unknown** for all seven and names **no actor, infrastructure, or payload** on the catalog entries.

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- JFrog
- Artifactory
- authentication bypass
- CVE-2026-82329
- Kestra
- workflow orchestration
- command injection
- CVE-2026-49869
- SonicWall
- SMA1000
- SSRF
- SNWLID-2026-0016
- CVE-2026-83548
- CVE-2026-83549
- LiteLLM
- MCP
- CVE-2026-59822
- Starlette
- request smuggling
- CVE-2026-48710
- Sangoma
- Switchvox
- SQL injection
- CVE-2026-9586

## The seven entries

### CVE-2026-82329 — JFrog Artifactory unauthenticated administrative access
CISA's entry: an **authentication weakness** in JFrog Artifactory that "under default configuration, may allow an **unauthenticated attacker with network access to obtain administrative privileges**." JFrog's security advisory (published **2026-08-28**, Critical) confirms: "Potential authentication bypass leading to administrative access in Artifactory."

- **KEV entry:** added 2026-09-02; **BOD 26-04 due 2026-09-05**.
- **Affected (self-managed):** 7.111.4–7.117.27, 7.125.0–7.125.19, 7.133.0–7.133.28, 7.146.0–7.146.36, 7.161.0–7.161.19.
- **Context:** this is the **second exploited Artifactory flaw in a month** after CVE-2026-66384 (Docker-cache path escape, KEV August 27 — see the [August 27 page](cisa-kev-owncloud-linux-artifactory-august-27-2026.md)). An unauthenticated admin-takeover primitive on the build-artifact platform that holds repository and registry credentials is a first-stage foothold into the build supply chain.

### CVE-2026-49869 — Kestra OSS unauthenticated workflow execution → root RCE
CISA's entry: **OS command injection** in Kestra OSS. The NVD record details: `AuthenticationFilter` whitelists the public configuration endpoint with a **suffix match** — `request.getPath().endsWith("/configs")` — so **any API path whose last segment is `configs` bypasses Basic Auth entirely**. An unauthenticated remote attacker can create and execute arbitrary workflows; because Kestra ships with script-execution plugins (`plugin-script-shell`, `plugin-script-python`, …) **enabled by default**, this is unauthenticated RCE **as root inside the Kestra worker container**. Fixed in **1.0.45** and **1.3.21**.

- **KEV entry:** added 2026-09-02; **BOD 26-04 due 2026-09-05** (the tightest deadline in this batch).
- **Context:** Kestra is an open-source event-driven orchestration platform in the same trust-boundary class as the other workflow/CI systems hit in 2026; the suffix-match auth-filter bypass is a reusable code smell worth auditing for in any router that whitelists paths by `endsWith`-style matching.

### CVE-2026-83548 / CVE-2026-83549 — SonicWall SMA1000 pre-auth SSRF + post-auth command injection
CISA's entries (both under **SNWLID-2026-0016**, published 2026-09-02, **BOD 26-04 due 2026-09-05**):

- **CVE-2026-83548** — **pre-authentication SSRF** in the SMA1000 Appliance Work Place interface due to an unintended alternate access path; a remote unauthenticated attacker could reach sensitive functionality. NVD scores it **10.0**.
- **CVE-2026-83549** — **post-authentication OS command injection** in the Appliance Management Console (AMC); in specific conditions a remote authenticated attacker **as administrator** can execute arbitrary OS commands (RCE). NVD scores it 7.8.

- **Context:** the SMA1000 is a WAN-optimization / secure-remote-access appliance at the network edge. This follows the **UTA0533** cluster that exploited the SMA1000's earlier zero-days (CVE-2026-15409 / CVE-2026-15410, KEV July 2026 — see the [UTA0533 page](uta0533-sonicwall-sma1000-zero-day-compromise.md)): the appliance is now on its **second exploited-flaw wave**, so unpatched SMA1000 fleet instances should be treated as actively targeted. SonicWall's fixed hotfixes are on the [SNWLID-2026-0016 advisory](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0016).

### CVE-2026-59822 — LiteLLM MCP gateway authentication bypass
CISA's entry: an **improper authentication vulnerability** in BerriAI LiteLLM (pip). GHSA-7488-6r32-c95q (published 2026-07-22): the MCP Streamable HTTP endpoint's OAuth2-passthrough fallback could replace failed LiteLLM key validation with an **empty `UserAPIKeyAuth()` object** — any fabricated Bearer token (even a single character) established a fully authenticated MCP session, able to list and call configured MCP tools and reach connected services. Fixed in **1.84.0**; workaround is disabling MCP routes or blocking `/mcp/`.

- **KEV entry:** added 2026-09-02; **BOD 26-04 due 2026-09-16**.
- **Context:** this flaw was already observed in the wild in [Wiz's 90-day AI-infrastructure honeypot telemetry](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md) (requests with `Authorization: Bearer ***` probing `GET /v1/models`); the KEV listing formalizes the in-the-wild status.

### CVE-2026-48710 — Starlette Host-header validation bypass
CISA's entry: an **HTTP request/response smuggling vulnerability** in Kludex Starlette (pip). GHSA-86qp-5c8j-p5mr: the HTTP `Host` request header was not validated before being used to reconstruct `request.url`; because routing uses the raw path while `request.url` is rebuilt from the `Host` header, a malformed header makes `request.url.path` differ from the requested path, letting middleware/endpoints that gate on `request.url` be bypassed. Fixed in **1.0.1**.

- **KEV entry:** added 2026-09-02; **BOD 26-04 due 2026-09-16**.
- **Context:** Starlette is a core ASGI building block for a large installed base of FastAPI/agent applications; in [Wiz's honeypot telemetry](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md) this CVE was **chained with CVE-2026-42271** (LiteLLM MCP stdio command injection, in KEV since June 2026) to achieve fully unauthenticated RCE, and external researchers have linked the chain to the **Qilin ransomware group** (third-party attribution, not confirmed by Wiz).

### CVE-2026-9586 — Sangoma Switchvox unauthenticated SQL injection
CISA's entry: an **SQL injection vulnerability** in Sangoma Switchvox SMB Edition 8.3 (104997). The NVD record: the `/pa` endpoint processes XML content beginning with `<PolycomIPPhone>` and **directly concatenates the user-controlled `PhoneIP` value into PostgreSQL queries without sanitization or parameterization** — an unauthenticated remote attacker executes arbitrary SQL statements against the backend database with a single crafted request, including database operations and remote code execution.

- **KEV entry:** added 2026-09-02; **BOD 26-04 due 2026-09-05**.
- **Vendor posture:** fixed in **Switchvox 8.4.0.2** (released July 14, 2026 per Sangoma's release notes, the reference on the KEV entry). Third-party analyses (SRA Labs, Horizon3.ai) documented the RCE chain.
- **Context:** Switchvox/Polycom PBX appliances are frequently internet-exposed for remote telephony; an unauthenticated SQLi with a single-request RCE path is a classic perimeter-breach primitive.

## Defender priorities
1. **Patch the five September 5 BOD 26-04 deadlines first.** Self-managed Artifactory: upgrade off the affected 7.111–7.161 release ranges. Kestra OSS: upgrade to 1.0.45 / 1.3.21. SonicWall SMA1000: apply the SNWLID-2026-0016 hotfix. LiteLLM: 1.84.0 (September 16). Starlette: 1.0.1 (September 16). Switchvox: 8.4.0.2.
2. **Treat unpatched SMA1000 and Artifactory as actively targeted** — both products have two exploited flaws in the public record within ~30 days (SMA1000: UTA0533 zero-days in July, this pair in September; Artifactory: CVE-2026-66384 in August, this CVE in September). Hunt for unauthorized admin sessions, anomalous workflow executions, and SMB/SSH pivots from the appliance.
3. **AI-infrastructure estates:** upgrade LiteLLM ≥ 1.84.0 and audit Starlette ≥ 1.0.1; hunt the `Bearer x` / single-character-token MCP probing pattern and host-header anomalies in ASGI access logs.
4. **Preserve evidence before cleanup** on covered federal systems (BOD 26-04 Forensics Triage requirement applies to all seven).
5. **Re-check the catalog.** This is the fourth batch in as many weeks (Aug 26, Aug 27, Aug 31, Sep 2); CISA is adding entries at a multi-per-day cadence, so the catalog is a standing watch item, not a one-time digest.

## Assessment limits
- CISA's entries record **ransomware use as unknown** and identify **no actor, infrastructure, or payload** for all seven.
- SonicWall's PSIRT advisory page is JavaScript-rendered; the fixed-hotfix matrix is on the live [SNWLID-2026-0016 page](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0016) — consult it for current affected hotfixes rather than treating this summary as a version authority.
- The JFrog affected-version ranges are from JFrog's security-advisory page (captured 2026-09-04); JFrog Cloud environments should be verified against JFrog's current advisory matrix.
- For CVE-2026-49869, the NVD description (suffix-match auth-filter bypass) is the authoritative mechanism; Kestra's own GHSA (GHSA-5vc5-wxxq-3fjx) is cited by CISA.

## Related pages
- [CISA KEV August 27, 2026 additions: ownCloud WebDAV pre-signed URL bypass, Linux kernel IPv6 LPE, and JFrog Artifactory Docker-cache path escape](cisa-kev-owncloud-linux-artifactory-august-27-2026.md)
- [UTA0533 SonicWall SMA1000 zero-day compromise](uta0533-sonicwall-sma1000-zero-day-compromise.md)
- [Wiz Threat Research: 90 days of honeypot telemetry on AI-infrastructure attacks](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md)
- [PaperCut NG/MF zero-day: active exploitation of an unauthenticated admin-trigger → unsafe class-loading chain (CVE-2026-81578 / CVE-2026-82078)](papercut-ng-mf-zero-day-active-exploitation-cve-2026-81578-cve-2026-82078.md)

## Sources
- CISA: [Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (2026-09-02 batch) / [catalog JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- NVD: [CVE-2026-82329](https://nvd.nist.gov/vuln/detail/CVE-2026-82329), [CVE-2026-49869](https://nvd.nist.gov/vuln/detail/CVE-2026-49869), [CVE-2026-83548](https://nvd.nist.gov/vuln/detail/CVE-2026-83548), [CVE-2026-83549](https://nvd.nist.gov/vuln/detail/CVE-2026-83549), [CVE-2026-59822](https://nvd.nist.gov/vuln/detail/CVE-2026-59822), [CVE-2026-48710](https://nvd.nist.gov/vuln/detail/CVE-2026-48710), [CVE-2026-9586](https://nvd.nist.gov/vuln/detail/CVE-2026-9586)
- JFrog Security Advisories (CVE-2026-82329, published 2026-08-28): [https://docs.jfrog.com/releases/docs/jfrog-security-advisories](https://docs.jfrog.com/releases/docs/jfrog-security-advisories)
- SonicWall PSIRT: [SNWLID-2026-0016](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0016)
- GitHub Advisories: [GHSA-7488-6r32-c95q (LiteLLM)](https://github.com/BerriAI/litellm/security/advisories/GHSA-7488-6r32-c95q), [GHSA-86qp-5c8j-p5mr (Starlette)](https://github.com/Kludex/starlette/security/advisories/GHSA-86qp-5c8j-p5mr), [GHSA-5vc5-wxxq-3fjx (Kestra)](https://github.com/kestra-io/kestra/security/advisories/GHSA-5vc5-wxxq-3fjx)
- Sangoma Switchvox 8.4.0.2 release notes (2026-07-14): [https://sangomakb.atlassian.net/wiki/spaces/Switchvox/pages/1802371073](https://sangomakb.atlassian.net/wiki/spaces/Switchvox/pages/1802371073/Switchvox+-+Release+Notes+Version+8.4.0.2+July+14+2026)
- BOD 26-04: [https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
