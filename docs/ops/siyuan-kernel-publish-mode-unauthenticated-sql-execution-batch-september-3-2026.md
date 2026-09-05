# SiYuan kernel publish-mode security batch: unauthenticated SQL execution and publish-boundary breakdowns (GHSA-69083/69084/72811 criticals, 2026-09-03)

## Summary
On **September 3, 2026**, GitHub Security Advisories published a coordinated **20-advisory batch** against the **SiYuan** kernel (`github.com/siyuan-note/siyuan`), a popular open-source, local-first knowledge base / note-taking application. The batch discloses **3 critical (CVSS 10.0)** unauthenticated SQL-execution flaws reachable in **publish mode**, **9 high**, and **8 medium** flaws, all stemming from a systemic failure to enforce SiYuan's publish/reader access boundary and, in three cases, from passing **client-supplied SQL directly to a read-write database handle** with no single-statement or read-only guard. All 20 are fixed in the **v3.8.3-alpha.1** release line (hardening commits dated 2026-07-21 through 2026-07-23; the `first_patched_version` for the criticals is the pre-release kernel build `0.0.0-20260721004815-cf42dd5680c8` and siblings).

The durable defender lesson: **a knowledge-base "publish mode" is a read surface, but this implementation made it effectively read-write.** When a product exposes an HTTP API where the "reader" token is gated only by `CheckAuth` (authentication) rather than a per-data authorization check, every data-returning endpoint becomes a candidate for cross-boundary disclosure — and the moment one endpoint accepts a *raw SQL statement* rather than a parameterized query, the boundary collapses into arbitrary read/write against the entire cleartext workspace.

## Why this matters
- **SiYuan is widely self-hosted** as a personal/team knowledge base, and "publish mode" is its primary way to share a notebook with readers over the network. An exposed SiYuan instance is a realistic internet attack surface, and the two most severe classes here require **no credentials** when `Publish.Auth.Enable` is `false` (the default for many self-hosted setups).
- **Unauthenticated SQL execution on a read-write handle** is not merely "SQL injection": the endpoints accept a *full* SQL statement by design and simply fail to restrict who may call them. An attacker can read **and write** across **all cleartext notebooks**, spanning the cross-notebook asset-content store.
- **The localhost-trust admin bypass (CVE-2026-72809, 8.0)** is the second-order amplifier: the kernel grants `RoleAdministrator` to any request whose `RemoteAddr` is loopback on a set of endpoints, and the fixed-port reverse proxy forwards to the kernel over loopback with **no auth token and no `SetTrustedProxies`**, so a proxy bound to a network interface can remote the bypass.
- **Second-order / supply-chain vector (CVE-2026-72807, 8.0):** attribute-view template columns are live-evaluated on render and expose a `queryBlocks` function that runs raw SQL. An attacker can ship a maliciously crafted SiYuan document or AV package that executes arbitrary SQL **when a victim imports it** — a document-delivery primitive, not just a remote one.

## Operational characteristics
- **Affected component:** SiYuan kernel (Go), `github.com/siyuan-note/siyuan/kernel` — the HTTP API service, its search/attribute-view/backlink endpoints, the fixed-port reverse proxy, and the encrypted-notebook key material.
- **Exploit status:** no public PoC, in-the-wild exploitation, or actor attribution reported in the reviewed advisories. This is a **disclosure/publish batch**; treat it as a patch-now, not a hunt-now, item until exploitation telemetry appears.
- **CVSS / severity breakdown (20 GHSAs):**
  - **Critical 10.0 (3):** `CVE-2026-69083` (unauthenticated SQL execution + REGEXP injection via `fullTextSearchAssetContent`, publish mode), `CVE-2026-69084` (unauthenticated arbitrary SQL execution via `searchEmbedBlock`, publish mode), `CVE-2026-72811` (SQL injection in backlink/mention search via unescaped stored + client input, publish mode).
  - **High (9):** `CVE-2026-72804` (8.6, graph endpoints omit publish-password tier), `CVE-2026-72810` (8.6, publish-boundary bypass via WebSocket live broadcast), `CVE-2026-68584` (8.6, anonymous publish-password auth bypass via `getHeading*`), `CVE-2026-68586` (8.6, cross-boundary content disclosure via `getBacklinkDoc`/`getBackmentionDoc`), `CVE-2026-68587` (8.6, full-content disclosure of publish-disabled docs via `getHeading*Transaction`), `CVE-2026-72807` (8.0, second-order SSTI→SQL via AV template `queryBlocks`), `CVE-2026-72809` (8.0, localhost-trust admin bypass via fixed-port proxy), `CVE-2026-69086` (7.7, path traversal via unvalidated `avID` in AV read endpoints), `CVE-2026-72801` (7.5, encrypted-notebook key-derivation + wrapped keys disclosed to anonymous readers).
  - **Medium (8):** `CVE-2026-72812` (6.5, `refreshBacklink` missing authorization), `CVE-2026-72800`/`72803`/`72805`/`72806`/`72808`/`68585` (5.8, various missing publish-access filters disclosing schema/block attributes/breadcrumbs/annotations/metadata), `CVE-2026-72802` (5.3, filesystem path + OS username disclosure via `resolveAssetPath`).
- **Fixed versions:** kernel builds from **2026-07-21 to 2026-07-23**; available in the **v3.8.3-alpha.1** release (published 2026-09-03) and the v3.8.2 → v3.8.3 line. `vulnerable_version_range` is expressed as a Go pseudo-version `< 0.0.0-20260721004815-cf42dd5680c8` (and siblings) — i.e. anything before those hardening commits.
- **Public attribution:** none in the reviewed advisories. No actor, campaign, or malware linkage. Keep attribution unset unless a primary source publishes follow-up.

## Defender heuristics
- **Inventory SiYuan instances** (self-hosted knowledge bases / note servers) and confirm the kernel build. If you are on any build prior to the v3.8.3 hardening commits, **upgrade to v3.8.3-alpha.1 or later** — the criticals require no credentials when publish auth is disabled.
- **Do not expose the kernel to the open internet.** If publish mode must be reachable, set `Publish.Auth.Enable` to `true` (so the anonymous account is off) and enforce the publish-password tier; the high-severity disclosure flaws (CVE-2026-72804/68584/68586/68587) are specifically about the *anonymous* reader bypassing the password tier.
- **Treat "accepts a raw SQL statement" as a design smell.** Any endpoint that takes a full SQL string and runs it on a read-write handle is an arbitrary-data read/write primitive regardless of how it is gated. Audit for this pattern when triaging similar "publish"/"share"/"preview" APIs.
- **Watch for the second-order import vector (CVE-2026-72807).** A shared/forwarded SiYuan document or attribute-view package with a malicious `.action{queryBlocks "..."}` template column is a delivery mechanism; treat unexpected imports of AV packages as potentially hostile.
- **Check the fixed-port proxy (CVE-2026-72809).** If the SiYuan fixed-port reverse proxy is bound to a non-loopback interface, confirm it is not forwarding to the kernel without an auth token and that `SetTrustedProxies` is configured; otherwise the loopback admin bypass is remotely reachable.
- **Encrypted notebooks are only as strong as their key-disclosure surface (CVE-2026-72801).** The Argon2id salt/cost, a password verifier, and the wrapped per-notebook key can be retrieved by an anonymous reader on unpatched builds, reducing every encrypted notebook to an offline-crack problem — rotate the master password and notebook keys after patching if the instance was reachable.
- **Hunt** for unauthorized SQL writes across cleartext notebooks (unexpected block mutations, `pg_authid`-style tampering analogs in the SiYuan `.db`), anomalous `fullTextSearchAssetContent` / `searchEmbedBlock` requests, and import events of AV packages around any disclosure window.

## Related pages
- [CISA KEV September 2, 2026 additions (Artifactory / Kestra / SonicWall / LiteLLM / Starlette / Switchvox)](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md) — the recurring "default-config / publish-mode auth bypass" pattern this batch extends.
- [GitHub Security Advisories August 29, 2026 batch (argocd-mcp / Sigma Forms Pro / Omnivore / Skyvern / BookStack)](github-advisories-argocd-mcp-sigma-forms-omnivore-skyvern-bookstack-august-29-2026.md) — another multi-CVE GHSA disclosure batch for reference on triage hygiene.

## Sources
- GitHub Security Advisories (batch, published 2026-09-03): [siyuan-note/siyuan kernel](https://github.com/siyuan-note/siyuan/security/advisories)
- Critical unauthenticated SQL execution: [GHSA-fph3-ghq9-vw66 / CVE-2026-69083](https://github.com/advisories/GHSA-fph3-ghq9-vw66), [GHSA-vh22-h7hf-www7 / CVE-2026-69084](https://github.com/advisories/GHSA-vh22-h7hf-www7), [GHSA-q2vg-7qgx-x5fc / CVE-2026-72811](https://github.com/advisories/GHSA-q2vg-7qgx-x5fc)
- Localhost-trust admin bypass: [GHSA-3mp7-4rh5-jrv9 / CVE-2026-72809](https://github.com/advisories/GHSA-3mp7-4rh5-jrv9)
- Second-order SSTI→SQL: [GHSA-x67c-8pwr-m8g3 / CVE-2026-72807](https://github.com/advisories/GHSA-x67c-8pwr-m8g3)
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-69083 , https://nvd.nist.gov/vuln/detail/CVE-2026-69084 , https://nvd.nist.gov/vuln/detail/CVE-2026-72811
- Release: [SiYuan v3.8.3-alpha.1](https://github.com/siyuan-note/siyuan/releases)

## Tags
- ops
- operations
- SiYuan
- knowledge base
- SQL injection
- unauthenticated RCE
- publish mode
- access control bypass
- arbitrary SQL execution
- path traversal
- second-order injection
- localhost trust bypass
- patch management
- self-hosted applications
- GitHub Security Advisories
