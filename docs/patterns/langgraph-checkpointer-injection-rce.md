# LangGraph checkpointer injection and unsafe deserialization

## Summary
Check Point Research disclosed a LangGraph checkpointer vulnerability chain where user-controlled checkpoint-history filters can cross from agent state lookup into database query injection and, in some self-hosted SQLite deployments, into runtime code execution through unsafe `msgpack` checkpoint deserialization.

The highest-risk shape is a self-hosted LangGraph application that exposes `get_state_history()` or equivalent checkpoint search with user-controlled filter keys, while using the SQLite checkpointer. LangChain's managed LangSmith Deployment / LangGraph Platform is described by Check Point as not affected because it uses PostgreSQL, but self-hosted agent services should inventory their checkpointer backends and patch.

## Tags
- patterns
- AI tooling
- AI agents
- LangGraph
- LangChain
- checkpointers
- agent state
- SQLite
- Redis
- RediSearch
- SQL injection
- query injection
- unsafe deserialization
- msgpack
- RCE
- self-hosted AI services
- Check Point Research
- GitHub Security Advisories

## Vulnerability set
- `CVE-2025-67644` / `GHSA-9rwj-6rc7-p77c`: SQL injection in `langgraph-checkpoint-sqlite` metadata filter-key handling. Affected versions are `< 3.0.1`; patched in `3.0.1`.
- `CVE-2026-28277` / `GHSA-g48c-2wqr-h844`: unsafe `msgpack` checkpoint deserialization in `langgraph`. Affected versions are `<= 1.0.9`; patched in `1.0.10`.
- `CVE-2026-27022` / `GHSA-5mx2-w598-339m`: RediSearch query injection in `@langchain/langgraph-checkpoint-redis` filter handling. The GitHub advisory lists affected versions as `< 1.0.1`; Check Point recommends updating to `1.0.2+`.

## Attack shape
- LangGraph checkpointers store agent execution state and metadata so applications can resume, inspect, or query prior agent runs.
- The vulnerable SQLite path built SQL predicates by interpolating filter keys into `json_extract(...)` expressions while parameterizing only filter values.
- If an application lets a user supply arbitrary metadata filter keys to `get_state_history()`, that user can manipulate the checkpoint query and bypass metadata-based filtering or access controls.
- Check Point describes a SQLite chain where SQL injection can return attacker-shaped checkpoint rows, and later checkpoint loading reaches unsafe `msgpack` object reconstruction, producing remote code execution in the application runtime.
- The Redis issue is parallel query-injection risk in RediSearch filter construction: unescaped filter keys or values can alter query logic and cross thread or namespace boundaries.
- The `msgpack` issue is also a post-exploitation blast-radius problem by itself: if an attacker can write checkpoint bytes at rest, loading those bytes can turn checkpoint-store compromise into code execution with the agent service's environment variables, cloud credentials, filesystem access, and network permissions.

## Defender heuristics
- Patch self-hosted LangGraph deployments to at least `langgraph-checkpoint-sqlite` `3.0.1`, `langgraph` `1.0.10`, and `@langchain/langgraph-checkpoint-redis` `1.0.2` where those packages are in use.
- Treat checkpoint filters as a trust boundary. Do not let tenants, chat users, tools, or API clients choose arbitrary metadata filter keys; map user choices to a small allow-list of server-side field names.
- Search application code for `get_state_history(` and check whether `filter` keys come from request JSON, URL parameters, LLM/tool output, plugin metadata, or other untrusted input.
- Review checkpoint stores for suspicious metadata keys, malformed `json_extract` / RediSearch syntax, unexpected checkpoint namespaces, and checkpoint rows not produced by normal agent execution.
- Run self-hosted agent services with least privilege: isolate checkpoint databases, keep runtime credentials narrow, block metadata-service access where possible, and restrict outbound network egress from agent workers.
- Add telemetry around checkpoint reads and loads, not only agent tool calls. Alert on checkpoint-history queries that use unusual filter keys, broad OR-style Redis predicates, or cross-tenant/thread access patterns.
- During incident response, preserve checkpoint databases before cleanup; they may contain both malicious serialized payloads and evidence of prompt/tool execution history.

## Related pages
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](../ops/litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](../ops/marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [PraisonAI CVE-2026-44338 rapid exploitation](../ops/praisonai-cve-2026-44338-rapid-exploitation.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)

## Sources
- Check Point Research: <https://research.checkpoint.com/2026/from-sqli-to-rce-exploiting-langgraphs-checkpointer/>
- GitHub Advisory `GHSA-9rwj-6rc7-p77c` / `CVE-2025-67644`: <https://github.com/langchain-ai/langgraph/security/advisories/GHSA-9rwj-6rc7-p77c>
- GitHub Advisory `GHSA-g48c-2wqr-h844` / `CVE-2026-28277`: <https://github.com/langchain-ai/langgraph/security/advisories/GHSA-g48c-2wqr-h844>
- GitHub Advisory `GHSA-5mx2-w598-339m` / `CVE-2026-27022`: <https://github.com/langchain-ai/langgraphjs/security/advisories/GHSA-5mx2-w598-339m>
- The Hacker News summary: <https://thehackernews.com/2026/06/langgraph-flaw-chain-exposes-self.html>
