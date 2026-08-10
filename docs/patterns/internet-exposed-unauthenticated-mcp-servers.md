# Internet-exposed unauthenticated MCP servers

## Summary
Wiz Research found internet-reachable Model Context Protocol (MCP) servers that exposed production data, privileged write operations, server-side code execution, cloud metadata access, and credentials without authenticating callers. The core failure is a privileged-proxy boundary: the public MCP endpoint accepts an anonymous request, then uses its own stored API token, database connection, cloud role, or agent runtime to act on a protected backend.

MCP makes this exposure unusually easy to discover and operate at scale. A standard client can negotiate with many implementations, and `tools/list` returns a machine-readable capability catalog and parameter schemas by design. Some deployments also wrap a language-model agent with shell access, making a natural-language prompt another path to backend execution.

This is exposure research, not evidence that the reported servers were exploited in the wild. Wiz says it did not invoke advertised write or delete operations, and anonymous tool discovery alone does not prove that a sensitive operation will succeed.

## Tags
- patterns
- AI agents
- AI application infrastructure
- Model Context Protocol
- MCP
- internet exposure
- unauthenticated access
- privileged proxy
- cloud credentials
- cloud metadata service
- SSRF
- command execution
- data exposure
- destructive actions
- OAuth 2.1
- least privilege
- invocation logging
- Wiz Research
- Meta Ads
- access token theft
- error-message disclosure
- Flyto2 Core
- CVE-2026-67426
- callback URL
- internal secret exfiltration

## Reported prevalence
Wiz reported the following measurements from its cloud-environment data and exposed-server testing:

- MCP appeared in 80% of observed cloud environments.
- About one in six of those environments exposed at least one MCP server.
- Roughly 70% of exposed servers returned their complete tool catalog to an anonymous caller.
- Roughly 42% returned real data when an anonymously invoked tool was called.
- Roughly 10% exposed a sensitive backend.
- A small but confirmed subset allowed server-side requests to a cloud instance-metadata service and returned temporary credentials.
- Nearly all observed servers negotiated the original `2024-11-05` protocol version, which predates the March 2025 authentication and tool-annotation additions.

Treat these figures as Wiz telemetry, not a census of all cloud tenants or all public MCP servers. An open catalog can also be intentional; risk depends on whether anonymous callers can reach sensitive data or actions and on the permissions held by the server.

## Meta Ads MCP concrete case
GitHub advisory `GHSA-9gw6-46qc-99vr` / `CVE-2026-48039` documents the same privileged-proxy failure in `pipeboard-co/meta-ads-mcp`. In affected releases, `AuthInjectionMiddleware.dispatch()` logs that no authentication token was supplied but still forwards the request to the MCP tool handler. The handler can then fall back to the server operator's `META_ACCESS_TOKEN` environment variable.

The flaw compounds unauthenticated tool execution with direct credential disclosure. The Meta Graph API client places `access_token` in the request URL; its error path serializes the raw URL into the JSON-RPC response. A remote caller who can reach the Streamable HTTP endpoint can therefore invoke registered tools as the operator and deliberately trigger an API error that returns the long-lived Meta token. Depending on the connected account and token scope, this can expose Meta Ads data, consume API quota, or permit write operations outside the MCP server after the token is copied.

The advisory currently scopes `meta-ads-mcp` versions through `1.0.108` as vulnerable and identifies `1.0.109` as the first patched release. Operators should upgrade, require authentication before dispatching any tool, stop placing access tokens in query strings, and redact request URLs from errors and logs. Rotate the Meta token after any internet exposure because patching cannot invalidate a credential already returned to an anonymous caller.

This is a public code-level vulnerability and proof of concept, not evidence of exploitation in the wild. The advisory was originally published on June 11, 2026 and updated on August 7 with the affected and fixed package range.

## Flyto2 Core concrete case
GitHub's reviewed `GHSA-jx74-cqjv-2c67` / `CVE-2026-67426` documents a related trust-boundary failure in Flyto2 Core, an MCP-native automation and AI-agent workflow engine. The standalone `flyto-verification` service exposed `POST /run` without authentication, and the shipped container listened on all interfaces at port `8344`. A caller could set `callback_url` to an arbitrary destination; after running the supplied verification workflow, the service sent a JSON callback to that URL and attached `X-Internal-Key: $FLYTO_RUNNER_SECRET`.

This combined two impacts. An unauthenticated caller could direct the service to make a server-side request to an internal or cloud-metadata destination, and an attacker-controlled callback host could directly receive the runner secret. The latter crossed the vulnerability from network reachability into credential compromise: the copied key could be replayed when forging callbacks to the real Flyto engine.

The application's existing destination control did not cover this path. `target_allowed` checked only `params.target_url`; `resolve_callback_url` returned the separate caller-provided callback verbatim, and the callback code added the internal header whenever the environment variable existed. This is a useful review rule beyond Flyto: validate every outbound destination at its final network sink, and bind privileged headers to a trusted destination identity rather than to the request type or code path.

The reviewed advisory scopes `flyto-core` **2.26.6** as affected and identifies **2.26.7** as the first patched version. The security release adds authentication to `/run`, fails closed when no verification key is configured, applies the SSRF guard to callbacks, and sends the internal key only to configured trusted hosts. The same release also fixes missing SSRF checks in several HTTP-emitting modules and revalidates each redirect hop for generic HTTP modules.

Operators should upgrade to 2.26.7 or later, remove public reachability to port 8344, rotate `FLYTO_RUNNER_SECRET` and any equivalent verification key after exposure, and inspect reverse-proxy, container, application, DNS, and egress logs for anonymous `/run` requests and callbacks to first-seen or non-engine destinations. Preserve workflow bodies and subsequent authenticated callback activity before rotation. The public advisory provides code-level proof but does **not** report malicious exploitation or confirmed victims.

## Exposure classes
### Sensitive-data access
Wiz observed anonymous MCP tools proxying production databases, mailboxes, issue trackers, regulated records, application-security findings, and business-intelligence systems. Reported examples included a retirement-account balance, security cases with hardcoded credentials, component-level application-security findings, and a BI tool that exposed database schema discovery and arbitrary SQL-query capabilities.

### Write and delete authority
Some catalogs advertised create, update, and delete operations against CRM, IAM, scheduling, and infrastructure backends. Examples included application-management methods on an IAM backend and bulk messaging plus roster and appointment deletion on a team-management platform. Wiz did not execute potentially destructive calls, so catalog presence should be treated as exposed capability that still requires safe validation.

### Code execution and internal-network access
The highest-impact cases exposed direct command or code execution, or an agent with shell access behind a prompt-like tool. URL-fetch and proxy tools could also become SSRF paths into internal services and instance metadata. Wiz reports that a direct request for AWS credentials was refused by one agent, while a maintenance-framed request to validate its IAM role through IMDS returned credentials. This shows that model guardrails are not an authorization boundary.

### Direct secret return
Some tools returned credentials without a further pivot. Wiz reported API keys in Lambda environment variables retrieved through a CloudWatch-log tool and an embedded database credential in a returned connection string.

## Why ordinary controls miss it
- Backend requests use the MCP server's valid credential, so protected services may see authorized, well-formed traffic rather than login failures or access-denied spikes.
- `tools/list` gives an anonymous caller structured reconnaissance without implementation-specific API knowledge.
- One generic MCP client can interact with otherwise unrelated exposed servers.
- Prompt-driven tools can hide malicious intent behind normal server-to-backend traffic.
- Older protocol deployments may lack OAuth 2.1 and the `readOnlyHint` / `destructiveHint` annotations added after the original protocol version.
- Prompt and tool-invocation logs may be the clearest evidence for agent-mediated execution, but many deployments do not capture them.

## Defender heuristics
- Inventory MCP listeners across cloud load balancers, serverless endpoints, containers, Kubernetes ingress, developer gateways, and directly exposed hosts. Confirm both network reachability and authentication at tool invocation, not only at a UI.
- If a catalog must remain public, require authorization before every tool call. Prefer the protocol's OAuth 2.1 support or an equivalent identity-aware gateway; do not rely on a hidden URL or model refusal.
- Treat each MCP server identity as a privileged service account. Minimize database, SaaS, IAM, messaging, filesystem, shell, and cloud permissions; separate read-only and destructive roles.
- Block instance-metadata and unnecessary internal-network access from MCP workloads. Where metadata access is required, enforce workload-specific controls and short-lived, narrowly scoped roles.
- Remove generic shell, code-evaluation, arbitrary SQL, URL-fetch, and unrestricted proxy tools unless the use case requires them. Put high-impact tools behind explicit policy and human approval.
- Record client identity, source address, negotiated protocol version, `tools/list` requests, tool name, normalized arguments, backend resource, result class, prompt, agent action, and process/network side effects. Protect logs from secrets and sensitive response bodies.
- Alert on anonymous initialization followed by tool enumeration; first-seen or internet-origin invocation of sensitive tools; metadata-service destinations; unusual SQL/schema enumeration; IAM application changes; bulk messaging; secret-like output; and shell or interpreter children of MCP services.
- For a confirmed exposed sensitive tool, preserve endpoint, gateway, cloud, prompt, invocation, backend, IAM, process, and network logs before changing access. Revoke or rotate the server's backend credentials and review every resource they could access; closing the listener alone does not invalidate copied credentials.

## Validation boundaries
Use non-destructive checks. Confirm authentication and authorization with a benign tool or a test tenant, and inspect configuration or code to establish backend permissions. Do not invoke production write/delete methods, query sensitive records, request secrets, or probe metadata endpoints merely to prove impact.

## Related pages
- [Ruflo CVE-2026-59726 unauthenticated MCP bridge RCE](../ops/ruflo-cve-2026-59726-unauthenticated-mcp-rce.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](../ops/litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [NadMesh AI-service and cloud-credential botnet](../ops/nadmesh-ai-service-cloud-credential-botnet.md)

## Sources
- Wiz Research: [The risk hiding behind exposed MCP servers](https://www.wiz.io/blog/the-risk-hiding-behind-exposed-mcp-servers) (2026-07-28)
- GitHub Security Advisory: [Meta Ads MCP unauthenticated HTTP tool execution leaks the operator Meta access token](https://github.com/advisories/GHSA-9gw6-46qc-99vr) (`GHSA-9gw6-46qc-99vr`, `CVE-2026-48039`; updated 2026-08-07)
- `pipeboard-co/meta-ads-mcp`: [release 1.0.109](https://github.com/pipeboard-co/meta-ads-mcp/releases/tag/1.0.109)
- GitHub Security Advisory: [Flyto2 Core unauthenticated callback SSRF and internal runner-secret exfiltration](https://github.com/advisories/GHSA-jx74-cqjv-2c67) (`GHSA-jx74-cqjv-2c67`, `CVE-2026-67426`; reviewed 2026-08-10)
- `flytohub/flyto-core`: [2.26.7 security release](https://github.com/flytohub/flyto-core/releases/tag/v2.26.7) and [remediation commit](https://github.com/flytohub/flyto-core/commit/0a0a528520ec18f5a21f1ddf858a71cc1edfb6e9)
