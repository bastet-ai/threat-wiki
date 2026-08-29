# GitHub Security Advisories August 29, 2026: argocd-mcp auth bypass, Sigma Forms Pro RCE, Omnivore Apple-Sign-In bypass, and a 6-item batch

## Summary
On **August 29, 2026**, a batch of GitHub Security Advisories was published with durable defender value. The six highest-impact, and the three additional criticals are:

| Advisory | Product | Class | Severity | Fix |
|---|---|---|---|---|
| **GHSA-p2x5-x87w-v2xj / CVE-2026-82456** | `argocd-mcp` 0.8.0 | **Unauth RCE-equivalent**: HTTP transport binds to all interfaces, accepts MCP sessions with no caller credentials, and invokes the full tool surface with the operator's stored `ARGOCD_API_TOKEN` | **Critical** (CVSS 10.0) | n/a — config (rebind + require caller creds) |
| **GHSA-vgff-mr3q-h6mh / CVE-2026-14494** | Sigma Forms Pro (WordPress) | **Unauth RCE** via `handle_form_submission`: dynamically grants `unfiltered_upload` to all users + bypasses MIME validation when `allowed_file_types` unset | **Critical** (CVSS 9.8) | n/a at publication |
| **GHSA-hc3c-8h8r-vcg7 / CVE-2026-82452** | rust-iot-platform ≤ 5df942ab | **Unauth auth bypass**: most REST routes lack auth guards in handler signatures | **Critical** (CVSS 9.8) | n/a at publication |
| **GHSA-4v5f-2v2r-748m / CVE-2026-82448** | Shinobi < 5a76c74f | **Unauth arbitrary DB queries** via hardcoded child-node connection key | **Critical** (CVSS 9.8) | 5a76c74f |
| **GHSA-8fpq-5wcx-76h3 / CVE-2026-82454** | Omnivore API (packages/api) < abf53d6 | **Auth bypass** in Apple sign-in: JWT `alg` from attacker header passed as sole allowed algorithm; `alg=HS256` signed with Apple's public RSA key as HMAC secret | **Critical** (CVSS 9.1) | abf53d6 |
| **GHSA-57gg-9j2p-5v4x / CVE-2026-82447** | Skyvern < 1.0.45 | **Sandbox escape**: `TextPromptBlock` renders prompts twice (sandboxed then unsandboxed Jinja) → arbitrary code | **High** (CVSS 8.8) | 1.0.45 |
| **GHSA-jgmr-x24h-q8jj / CVE-2026-82450** | BookStack < 26.05.4 | **RCE** in portable ZIP import: PHP polyglot uploaded as book cover, stored in public web root | **High** (CVSS 8.8) | 26.05.4 |
| **GHSA-xfj7-7fp8-rhvp / CVE-2026-80192** | @better-auth/sso < 1.6.27 / < 1.4.8 / < 1.7.0-rc.5 | **Domain-ownership bypass** (two paths): unverified-provider auto org-assignment + DNS-proof race | **High** (CVSS 8.1) | 1.6.27 |

No exploitation, actor, infrastructure, or payload detail is named in any of the advisories. The batch also included ~20 WordPress-plugin advisories (all "unknown" severity, routine) and a second wave of high-severity items (IBM ARE for i CVE-2026-18527 9.9, getgrav/grav-plugin-api CVE-2026-80203 9.8, Kimai CVE-2026-80198 / CVE-2026-80193, StarRocks CVE-2026-80346, su-exec CVE-2026-82457, cohttp CVE-2026-82481, RubyGems CVE-2026-82455).

## Tags
- ops
- GitHub Security Advisories
- authentication bypass
- unauthenticated RCE
- MCP
- Argo CD
- argocd-mcp
- Sigma Forms Pro
- WordPress
- unfiltered_upload
- Omnivore
- Apple Sign-In
- JWT
- algorithm confusion
- HS256
- Skyvern
- Jinja
- sandbox escape
- BookStack
- ZIP import
- better-auth
- SSO
- domain verification
- hardcoded key
- Shinobi
- CVE-2026-82456
- CVE-2026-14494
- CVE-2026-82452
- CVE-2026-82448
- CVE-2026-82454
- CVE-2026-82447
- CVE-2026-82450
- CVE-2026-80192

## argocd-mcp authentication bypass (GHSA-p2x5-x87w-v2xj / CVE-2026-82456)
`argocd-mcp` 0.8.0 **binds its HTTP transport to every network interface** and, when `ARGOCD_API_TOKEN` is configured, **accepts MCP sessions without requiring caller credentials**. An attacker who can reach the listener can invoke the full tool surface using the operator's stored token to **create applications, request syncs, and modify Argo CD resources** — an effectively-unauthenticated Argo CD control-plane primitive. CWE: CWE-1327 (Inadequate Authentication). No fixed version is published; the durable mitigation is to **rebind the listener to a trusted interface and require caller credentials**. Argo CD MCP servers are a high-value target because they are a privileged proxy to a GitOps control plane; see the [Wiz AI-infrastructure honeypot page](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md) for the broader MCP-as-privileged-proxy exposure class.

## Sigma Forms Pro WordPress RCE (GHSA-vgff-mr3q-h6mh / CVE-2026-14494)
The **Sigma Forms Pro** WordPress plugin is vulnerable to **unauthenticated RCE** in all versions up to and including **1.4.5** via the `handle_form_submission` function. The plugin **dynamically grants the `unfiltered_upload` capability to all users during form submissions** and **bypasses MIME-type validation when `allowed_file_types` is not configured**. Several default pre-built templates (Job Application, Support Ticket, Wholesale Application) ship with file-upload fields that have **no file-type restrictions by design**, making the flaw **immediately exploitable upon installation**. Reported by Wordfence. This is a "capability + no-MIME-gate → unfiltered upload → RCE" WordPress pattern.

## rust-iot-platform authentication bypass (GHSA-hc3c-8h8r-vcg7 / CVE-2026-82452)
`rust-iot-platform` through commit `5df942ab` contains an **authentication bypass** where **most REST API routes lack authentication guards in their handler signatures**. Unauthenticated attackers can **create, update, list, retrieve, and delete user accounts** by directly accessing unprotected endpoints. Companion advisory **GHSA-3wcf-94mw-cwgf / CVE-2026-82453** (High 7.5) notes the same codebase **stores user passwords in cleartext without hashing**, readable from user-retrieval/listing API responses.

## Shinobi hardcoded child-node key (GHSA-4v5f-2v2r-748m / CVE-2026-82448)
**Shinobi** before commit `5a76c74f` contains a **hardcoded connection key in the child-node service**. An unauthenticated attacker reaching the child-node port can present the hardcoded key during the WebSocket handshake and then **dispatch arbitrary SQL queries** through the `onWebSocketDataFromChildNode` handler to read and modify user records and camera configuration. Fixed in commit `5a76c74f`.

## Omnivore Apple Sign-In authentication bypass (GHSA-8fpq-5wcx-76h3 / CVE-2026-82454)
The **Omnivore API** (`packages/api`) before the fix in commit `abf53d6` contains an **authentication bypass in Apple sign-in token verification**. The `decodeAppleToken` function extracted the `alg` field from the **attacker-supplied JWT header and passed it as the sole allowed algorithm to `jwt.verify()`**. Using **jsonwebtoken v8** (which does not validate key/algorithm compatibility), an attacker sets **`alg=HS256`** and signs a forged token using **Apple's publicly available RSA public key as the HMAC secret**, bypassing signature verification and **impersonating any Apple-linked account**. This is the classic **JWT algorithm-confusion** flaw. Fixed in commit `abf53d6` (PR #4652).

## Skyvern Jinja sandbox escape (GHSA-57gg-9j2p-5v4x / CVE-2026-82447)
**Skyvern** before **1.0.45** contains a **sandbox escape** in `TextPromptBlock` that **renders prompts twice** — first through a sandboxed Jinja environment and then through an **unsandboxed** environment. An attacker injects malicious Jinja template syntax through **workflow parameters or upstream block output** to execute **arbitrary code with server-process privileges**. CWE: CWE-1336. Fixed in 1.0.45. Durable pattern: a template rendered in both a sandboxed and an unsandboxed context is an escape if the sandboxed pass does not sanitize the value consumed by the unsandboxed pass.

## BookStack portable-ZIP-import RCE (GHSA-jgmr-x24h-q8jj / CVE-2026-82450)
**BookStack** before **26.05.4** contains an **RCE in the portable ZIP import** feature. Users with **Import Content + Create Books** permissions upload a **PHP polyglot file as a book cover**, bypassing image-extension validation by embedding a `.php` file in the ZIP. The file is **stored in the public web root and executed by unauthenticated requests**. Fixed in 26.05.4.

## @better-auth/sso domain-ownership bypass (GHSA-xfj7-7fp8-rhvp / CVE-2026-80192)
**@better-auth/sso** before **1.6.27** (and before **1.4.8** in the 1.4.x line and before **1.7.0-rc.5** in the 1.7 prerelease line) contains **two domain-ownership flaws**:
1. **Domain-verification-disabled path:** when domain verification is off, automatic organization assignment accepts **unverified provider domains**, letting an authenticated org owner/admin register an SSO provider for an **arbitrary domain** and have **users with matching email domains added to the attacker's organization** with default member permissions.
2. **Domain-verification-enabled path:** a **race condition** between the `verify-domain` and `update-provider` endpoints can apply **completed DNS proof to a different domain**; combined with implicit account linking, this **links an attacker-controlled IdP to an existing user account**.

Exploitation requires the SSO plugin (and, for the org-assignment path, the organization plugin) with the relevant configuration. Fixed in 1.6.27.

## Why it matters
- **MCP-as-privileged-proxy is now a recurring critical:** the argocd-mcp item is the latest in the same trust-boundary class as the Wiz-reported CVE-2026-59822 MCP gateway auth bypass and the Kiro "Power Leak" MCP-config-rewrite exfil — a network-reachable MCP endpoint with a stored privileged token is a GitOps/control-plane takeover primitive.
- **JWT algorithm-confusion resurfaces:** the Omnivore Apple Sign-In bypass is a textbook `alg=HS256` + public-key-as-HMAC-secret flaw, now in a widely-embedded SSO helper; audit any `jsonwebtoken` v8 token-verification path that trusts the header `alg`.
- **WordPress "capability + no MIME gate" RCE:** the Sigma Forms Pro flaw is immediately exploitable on install for the default templates; it joins the standing set of unauthenticated WordPress upload→RCE patterns.

## Defender priorities
1. **argocd-mcp:** if you run `argocd-mcp` 0.8.0, **rebind the HTTP transport to a trusted interface and require caller credentials** (no patched release published); treat any exposed Argo CD MCP listener as compromised-eligible and rotate the `ARGOCD_API_TOKEN`.
2. **Sigma Forms Pro:** patch WordPress sites past 1.4.5 / apply the vendor fix; prioritize instances where the Job Application / Support Ticket / Wholesale templates are in use.
3. **Omnivore / @better-auth/sso:** upgrade Omnivore to ≥ commit `abf53d6` and @better-auth/sso to 1.6.27 (or the line-appropriate 1.4.8 / 1.7.0-rc.5); audit JWT verification so `alg` is not attacker-controllable.
4. **Skyvern / BookStack / Shinobi / rust-iot-platform:** apply the named fixed versions (1.0.45 / 26.05.4 / commit 5a76c74f / post-5df942ab).
5. **Treat as unattributed / no-exploitation.** None of the advisories names an actor, infrastructure, payload, or exploitation. Correlate to your own exposure model.
6. **Watch for the second wave:** the same batch included IBM ARE for i (CVE-2026-18527, 9.9), getgrav/grav-plugin-api (CVE-2026-80203, 9.8), Kimai (CVE-2026-80198 / -80193), StarRocks (CVE-2026-80346), su-exec (CVE-2026-82457), cohttp (CVE-2026-82481), and RubyGems (CVE-2026-82455) — inventory and patch those on their own merits.

## Assessment limits
- Severities are the advisories' own classification (GHSA/NVD CVSS). No in-the-wild exploitation indicator is present in any advisory.
- argocd-mcp, Sigma Forms Pro, and rust-iot-platform had **no published fixed version** at capture; their mitigations are configuration or pending release.
- The JWT-algorithm and WordPress capability mechanics are from the advisory descriptions; independent PoC corroboration was not available at capture.

## Related pages
- [Next.js August 2026 security release (AVIF/libheif + Windows RCE)](nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md)
- [Wiz AI-infrastructure honeypot telemetry (MCP RCE, prompt injection)](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md)
- [GitHub Security Advisories August 27, 2026 (Crossplane cosign TOCTOU + Silverstripe RCE)](github-advisories-crossplane-cosign-silverstripe-august-27-2026.md)

## Sources
- GitHub Security Advisory: [GHSA-p2x5-x87w-v2xj — argocd-mcp auth bypass (CVE-2026-82456)](https://github.com/advisories/GHSA-p2x5-x87w-v2xj)
- GitHub Security Advisory: [GHSA-vgff-mr3q-h6mh — Sigma Forms Pro RCE (CVE-2026-14494)](https://github.com/advisories/GHSA-vgff-mr3q-h6mh)
- GitHub Security Advisory: [GHSA-hc3c-8h8r-vcg7 — rust-iot-platform auth bypass (CVE-2026-82452)](https://github.com/advisories/GHSA-hc3c-8h8r-vcg7)
- GitHub Security Advisory: [GHSA-4v5f-2v2r-748m — Shinobi hardcoded child-node key (CVE-2026-82448)](https://github.com/advisories/GHSA-4v5f-2v2r-748m)
- GitHub Security Advisory: [GHSA-8fpq-5wcx-76h3 — Omnivore Apple Sign-In bypass (CVE-2026-82454)](https://github.com/advisories/GHSA-8fpq-5wcx-76h3)
- GitHub Security Advisory: [GHSA-57gg-9j2p-5v4x — Skyvern Jinja sandbox escape (CVE-2026-82447)](https://github.com/advisories/GHSA-57gg-9j2p-5v4x)
- GitHub Security Advisory: [GHSA-jgmr-x24h-q8jj — BookStack ZIP-import RCE (CVE-2026-82450)](https://github.com/advisories/GHSA-jgmr-x24h-q8jj)
- GitHub Security Advisory: [GHSA-xfj7-7fp8-rhvp — @better-auth/sso domain-ownership bypass (CVE-2026-80192)](https://github.com/advisories/GHSA-xfj7-7fp8-rhvp)
