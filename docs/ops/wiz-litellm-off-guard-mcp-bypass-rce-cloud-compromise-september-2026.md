# Wiz "Off Guard": Breaking LiteLLM from authentication bypass to cloud compromise (CVE-2026-59822 / CVE-2026-59821)

## Summary
Wiz Threat Research's **September 9, 2026** post ("Off Guard: Breaking LiteLLM from authentication bypass to cloud compromise"; Amitai Cohen, Yaara Shriki; previously presented at DEF CON 34) documents a chain in the most popular open-source LLM gateway, **BerriAI LiteLLM**. Scanning ~3,000 internet-facing deployments, Wiz found **9.6% accept the default master key (`sk-1234`) or require no authentication at all**. From there they reached **root-level RCE** on the host and, via the pass-through endpoint feature, **cloud/IAM credential theft**. Key findings:

- **CVE-2026-59822 — MCP authentication bypass:** an arbitrary Bearer token (even one character) can create a fully authenticated MCP session. Confirmed exploitable across hundreds of internet-facing instances. **Now on CISA KEV**; Wiz observed in-the-wild exploitation via its honeypot infrastructure.
- **CVE-2026-59821 — post-auth root-level RCE** via LiteLLM's **custom code guardrails** (an admin submits Python that the server passes to `exec(compile(...))`; the registration path lacks the forbidden-patterns check and `__builtins__` stripping that the "Run Test" UI enforces).
- **Unauthenticated admin by default (no CVE; fixed alongside CVE-2026-59821):** when no auth is configured, every request is granted **`PROXY_ADMIN`** access.
- **Post-auth cloud credential theft via the pass-through endpoint:** the pass-through proxy target URL is **never validated** (no private-range/localhost/metadata checks), so an admin can point it at the **AWS metadata service** and exfiltrate IAM credentials. Not considered a vulnerability on its own (admin-trusted), but effectively pre-auth when combined with a default/missing master key.
- **Unchanged default master key:** the master key doubles as the **HS256 signing secret for session JWTs**; unless changed from `sk-1234`, an attacker can **forge arbitrary user sessions** for the whole proxy.

All vulnerabilities have been responsibly disclosed; **patches are available**.

## Tags
- ops
- operations
- vulnerability
- AI gateway
- LLM gateway
- LiteLLM
- MCP
- Model Context Protocol
- authentication bypass
- RCE
- SSRF
- cloud metadata
- IAM credential theft
- default credentials
- CVE-2026-59822
- CVE-2026-59821
- CISA KEV
- Wiz

## The vulnerability chain
1. **MCP auth bypass (CVE-2026-59822).** LiteLLM's MCP endpoint has its own auth handler (`user_api_key_auth_mcp.py`) supporting a dual model: LiteLLM API keys for direct users, and OAuth2 passthrough for upstream providers (GitHub/Atlassian). The intended logic: if a Bearer token isn't a valid LiteLLM key, pass it through to the upstream MCP server. The flaw is the fallback — when validation fails with 401/403, the handler catches the exception and **returns an empty `UserAPIKeyAuth()` object**, granting access as if the request were authenticated. This triggers for **any** request with an `Authorization` header, so any garbage token authenticates. A single `Authorization: Bearer a` establishes a full MCP session, exposing the ability to **list and call configured MCP tools with arbitrary arguments** — databases, GitHub, filesystems, Jira, Slack, CI/CD.
2. **Guardrail RCE (CVE-2026-59821).** The "Custom Code Guardrails" feature lets admins write Python that runs before/after every inference call. The Web UI "Run Test" button validates against a forbidden-patterns list and strips `__builtins__` before execution. But the **registration endpoint (`POST /guardrails`) applies neither**: `_compile_custom_code()` calls `exec(compile(...))` without the forbidden-patterns check and without clearing `__builtins__` (which Python auto-repopulates). Submitted code executes **immediately at registration** (during initialization, before any LLM request); `import os; os.popen('id')` yields `uid=0 (root)`.
3. **Unauthenticated admin by default.** When no master key is set and no JWT/OAuth2 is configured, the proxy runs with **no authentication**, and pre-patch the auth handler **globally assigned `PROXY_ADMIN` to every request** — unauthenticated *admin* access, not merely unauthenticated access. Even when auth was enabled, the guardrail CRUD and config-update endpoints used a generic auth dependency accepting **any valid API key**, not `PROXY_ADMIN`.
4. **Default master key `sk-1234`.** Used throughout LiteLLM docs (quickstart, Docker Compose, config tutorials). It is both the admin credential and the **HS256 secret for signing session JWTs**, so leaving it default lets anyone **forge arbitrary user sessions**. A follow-up scan in August 2026 found 85,000+ instances (mostly honeypots/test deployments).
5. **Pass-through endpoint → cloud credential theft.** `POST /config/pass_through_endpoint` creates a proxy route to an arbitrary URL with **no target validation**. An admin can point it at `http://169.254.169.254/latest/` and read `meta-data/iam/security-credentials/<role>`. The `x-pass-` header-forwarding mechanism defeats **IMDSv2** (e.g. `x-pass-X-aws-ec2-metadata-token-ttl-seconds: 21600` arrives as `X-aws-ec2-metadata-token-ttl-seconds: 21600`), making IMDSv2 protections ineffective. Before **v1.83.0**, the config-update endpoint controlling pass-through routes did **not** require `PROXY_ADMIN` (any valid key) — fixed in v1.83.0 and assigned **CVE-2026-35029** (unrelated to this research).

## Fix status
- **CVE-2026-59821 (RCE) + MCP auth bypass:** fixed in **v1.82.0** (Feb 25, 2026, RCE + sandbox-escape) and **v1.84.0** (Apr 25, 2026, MCP auth bypass). PR #22095 gated the guardrail endpoints on `PROXY_ADMIN` and properly enforces the sandbox on registration.
- **Unauthenticated admin by default:** default role changed from `PROXY_ADMIN` to `INTERNAL_USER` (with the CVE-2026-59821 fix).
- **Pass-through config endpoint (CVE-2026-35029):** fixed in **v1.83.0**.
- **CVE-2026-59822 added to CISA KEV on 2026-09-02; BOD 26-04 due 2026-09-16.**

## Why it matters
- A compromised LiteLLM instance means **compromised AI infrastructure** — and, as shown, often the cloud environment it runs in. LiteLLM holds API keys for every configured LLM provider, executes server-side Python per inference request, proxies requests to arbitrary internal URLs, and connects to internal tools via MCP.
- This is part of a broader pattern: **AI gateways have become critical infrastructure without corresponding security controls**. They sit between application code and cloud services, hold privileged credentials, execute arbitrary code, and connect to internal tools — yet the security model is often reduced to a single shared secret. They should be treated as **Tier-1 security assets**, not developer tools.
- ~1 in 3 cloud environments run a LiteLLM deployment (per Wiz data); many more sit behind corporate networks/VPNs reachable by internal attackers, compromised workloads, or anyone with cluster access.

## Defender actions
1. **Use a strong, unique master key** — not `sk-1234` or other defaults.
2. **Upgrade LiteLLM to the patched release** (≥ v1.84.0 for the MCP bypass + guardrail RCE; the pass-through config fix is in v1.83.0).
3. **Review guardrails** for unexpected entries and restart the process to clear memory.
4. **Audit pass-through endpoints** and restrict container network egress (block `169.254.169.254`, private ranges, localhost).
5. **Apply least-privilege IAM roles** (IRSA or equivalent) so a compromised gateway cannot reach cloud metadata.
6. Hunt for the **single-character / arbitrary Bearer token** MCP probing pattern and host-header anomalies in ASGI access logs.

## Assessment limits
- The **unauthenticated-admin-by-default** behavior and the **pass-through endpoint cloud-credential vector** were not assigned a CVE (not considered vulnerabilities in the default admin-trust threat model); they are exploitable *because* default/weak credentials are widespread. Treat them as configuration risk, not a single patchable bug.
- Wiz frames the pass-through SSRF as "working as intended" under LiteLLM's admin-trust threat model; it is a security issue only when combined with default credentials or an auth bypass.
- "Root-level RCE" is within the LiteLLM container/process; the cloud impact (IAM theft) depends on the service account's privileges and whether the instance can reach the cloud metadata service.

## Related pages
- [CISA KEV September 2, 2026 additions: seven exploited flaws across Artifactory, Kestra, SonicWall, LiteLLM, Starlette, Switchvox](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)
- [LiteLLM compromise (TeamPCP supply-chain / PyPI)](litellm-compromise.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [MCP stdio command-execution boundary](../patterns/mcp-stdio-command-execution.md)
- [Wiz Threat Research: 90 days of honeypot telemetry on AI-infrastructure attacks](wiz-ai-infrastructure-honeypot-90-day-attack-telemetry.md)
- [Microsoft: AI infrastructure gateways and control points as high-value intrusion targets](microsoft-ai-infrastructure-gateways-control-points-august-2026.md)

## Sources
- Wiz: ["Off Guard: Breaking LiteLLM from authentication bypass to cloud compromise"](https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise) (September 9, 2026)
- CISA KEV: [catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (CVE-2026-59822, added 2026-09-02)
- LiteLLM GitHub advisories: [GHSA-7488-6r32-c95q (MCP auth bypass)](https://github.com/BerriAI/litellm/security/advisories/GHSA-7488-6r32-c95q)
