# workerd / Cloudflare Code Mode: five memory-corruption bugs enable sandbox escape and cross-tenant "heap swipe"

## Summary
Check Point Research's August 6, 2026 writeup "When Agentic Glue Melts: Exploiting Cloudflare Code Mode and Workers" (presented at Black Hat USA 2026 with public proof-of-concept code) documents **five memory-corruption vulnerabilities in workerd's native C++ layer** — the in-process "glue" between JavaScript and the runtime in Cloudflare's open-source edge runtime **workerd**. workerd is the isolation substrate for both **Cloudflare Workers** (multi-tenant serverless, >10% of all traffic on Cloudflare's network) and the new **Code Mode** technique for AI-agent tool use, where an LLM writes a TypeScript program against a typed tool API instead of emitting one structured tool call at a time.

Because workerd isolates untrusted tenants in **V8 isolates inside a single shared process** — a software boundary, not an OS/hardware one — the five bugs collapse into two end-to-end attacks:

1. **Cross-tenant heap swipe (Workers)** — an out-of-bounds read in `URLPattern` lets one Worker reach across the shared process heap and read another tenant's secrets.
2. **Code Mode sandbox escape** — starting from a prompt injection, a use-after-free in `node:zlib` breaks out of the sandbox and executes native code on the host.

Cloudflare rated **two of the five bugs Critical**. Cloudflare's managed Workers environment was fixed in production; **self-hosted workerd / Code Mode deployments should update to `workerd v1.20260619.1`**. No in-the-wild exploitation or actor attribution is reported.

## Tags
- tools
- workerd
- Cloudflare
- Cloudflare Workers
- Code Mode
- MCP
- V8
- V8 isolates
- sandbox escape
- cross-tenant
- out-of-bounds read
- use-after-free
- memory corruption
- URLPattern
- node:zlib
- prompt injection
- agentic AI
- Black Hat USA 2026
- Check Point Research
- critical vulnerability

## Why this matters
- **Code Mode changes the agent attack surface.** In classic MCP/tool-calling loops the model emits one `{tool, args}` call per step; in Code Mode the model writes *one program* that orchestrates many tool calls locally. The generated code runs in workerd's Code Mode sandbox — so prompt injection that reaches Code Mode now lands in a runtime whose security model is a single in-process V8 isolate boundary, not a container or VM. A sandbox escape from that boundary is a host-code-execution primitive on an edge platform carrying more than 10% of Cloudflare's network traffic.
- **The blast radius is the whole multi-tenant runtime.** workerd packs many customers' untrusted code into one process; V8 isolates are the tenant boundary. Memory corruption in the native glue defeats that boundary for both tenants (cross-tenant read) and the host (sandbox escape) — the two failure modes a shared-edge-runtime operator has to treat as equivalent to cross-tenant data breach.
- **The "glue" layer is the recurring soft spot.** Same family as isolated-vm's `ExternalCopy` handoff and JSONata's host-object bridge: a "safe" sandbox whose native binding code between the JS world and the host reaches across the trust boundary.

## The two demonstrated attacks
**1. Cross-tenant heap swipe (URLPattern OOB read).** An out-of-bounds read in `URLPattern` allows one Worker to read across the shared process heap and exfiltrate another tenant's secrets — a direct cross-tenant data-theft primitive against the Workers multi-tenant model.

**2. Code Mode sandbox escape (node:zlib use-after-free).** Starting from a prompt-injection position inside Code Mode, a use-after-free in the `node:zlib` native module breaks out of the isolate sandbox and executes native code on the host — the full prompt-injection-to-host-execution chain.

The five underlying bugs are memory-corruption flaws in workerd's native C++ (the glue between JavaScript and the runtime); Check Point released proof-of-concept code with the Black Hat USA 2026 talk.

## Affected / patched
| Component | Exposure | Mitigation |
|---|---|---|
| Cloudflare managed Workers | Fixed in production by Cloudflare | No action required for managed Workers |
| Self-hosted `workerd` (GitHub `cloudflare/workerd`) | Cross-tenant + sandbox-escape exposure until patched | Update to **v1.20260619.1** or later |
| Code Mode deployments (AI-agent MCP tool-execution sandboxes on workerd) | Prompt-injection-to-host path | Update workerd; treat Code Mode output as untrusted native-code-adjacent input; add egress/tenant isolation controls |

## Defender notes
- **Self-hosted workerd is the action item:** inventory any self-hosted `workerd`/Code Mode deployments and pin to `v1.20260619.1` or later; verify the running version rather than the installed artifact.
- **For Code Mode specifically:** prompt injection is a standing pre-condition. If an agent's Code Mode sandbox can reach declared MCP tools only, verify that `fetch()`/`connect()` are indeed refused (the documented lockdown) and that no binding grants broader access; the research shows the *runtime itself*, not the tool bindings, was the break point.
- **Hunting context:** cross-tenant read via `URLPattern` OOB and a `node:zlib` UAF-driven host escape will not look like typical edge-app abuse; correlate unusual workerd process crashes / native-code execution anomalies on self-hosted deployments.

## Assessment limits
- No in-the-wild exploitation or actor attribution is reported; the two demonstrated attacks are researcher PoCs (public, Black Hat USA 2026).
- The bug count (five, two Critical per Cloudflare) and the per-bug locations (`URLPattern`, `node:zlib`) come from Check Point Research; the full per-bucket CVE/GHSA assignment is not itemized in the writeup captured here.

## Related pages
- [isolated-vm ExternalCopy type-confusion sandbox escape (GHSA-864f-rcv7-6rh4)](isolated-vm-external-copy-type-confusion-sandbox-escape.md)
- [JSONata arbitrary-code-execution trio (CVE-2026-77413 / -77414 / -77415)](jsonata-cve-2026-77413-77414-77415-arbitrary-code-execution.md)
- [vm2 NodeVM host state exposure and DNS hijack](vm2-nodevm-host-dns-hijack.md)
- [Cloudflare Workers remote Spectre co-located JWT leak](../ops/cloudflare-workers-spectre-co-located-jwt-leak.md)
- [Agentic workflow trust-boundary failures](../patterns/agentic-workflow-trust-boundary-failures.md)

## Sources
- Check Point Research: [When Agentic Glue Melts: Exploiting Cloudflare Code Mode and Workers](https://research.checkpoint.com/2026/when-agentic-glue-melts/) — published 2026-08-06 (Yarden Porat; Black Hat USA 2026)
- Cloudflare workerd: [cloudflare/workerd releases](https://github.com/cloudflare/workerd/releases) (patched release `v1.20260619.1`)
