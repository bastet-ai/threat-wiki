# Sentry MCP Agentjacking

## Summary
Tenet Security's Threat Labs documented an "Agentjacking" pattern where attacker-injected Sentry error events are relayed through the Sentry MCP server to AI coding agents as trusted troubleshooting context. The critical boundary is not a Sentry software exploit: Sentry DSNs are intentionally public, write-only ingest credentials, but AI agents may treat the resulting error text, markdown, and context fields as instructions rather than untrusted event data.

In Tenet's controlled validation, a crafted Sentry event included fake remediation guidance that steered agents such as Claude Code, Cursor, and Codex toward running an `npx` diagnostic package. Tenet reported 2,388 exposed organizations found through public reconnaissance and 100+ confirmed agent executions during controlled testing, while stating that payloads self-identified as a responsible-disclosure scan and did not retain collected probe data.

## Tags
- patterns
- AI tooling
- AI agents
- MCP
- Sentry
- Agentjacking
- indirect prompt injection
- tool output injection
- developer workstations
- npm
- npx
- credential exposure
- Claude Code
- Cursor
- Codex
- Tenet Security

## Attack shape
- The attacker finds a target Sentry DSN from public frontend JavaScript, code search, CDN content, or internet indexing. Sentry documents DSNs as safe to expose because they are used for event ingestion rather than account access.
- The attacker posts a crafted error event to Sentry's ingest endpoint. Tenet notes that the attacker can control fields such as the error message, tags, context keys, breadcrumbs, user data, stack traces, and fingerprint.
- The event uses markdown and Sentry-looking structure to create a fake remediation section, such as a diagnostic command presented as a resolution step.
- A developer asks an AI coding agent to investigate or fix unresolved Sentry issues. Through MCP, the agent receives the injected event as external tool output.
- If the agent fails to separate untrusted event content from trusted tool/system instructions, it may execute attacker-supplied commands with the developer workstation's privileges.
- Tenet's proof path used a controlled npm package invoked through `npx`; a malicious operator could instead target environment variables, cloud credentials, GitHub and npm tokens, Sentry auth tokens, git remotes, private repository metadata, Docker/Kubernetes configuration, or VPN/network context.

## Defender heuristics
- Treat observability, ticketing, chat, issue, support, and CRM records as untrusted input when they enter AI-agent context. MCP output should be data to inspect, not instructions to execute.
- For Sentry MCP usage, block or require explicit human approval for shell execution, package-manager execution, `npx`/`npm exec`, `curl | sh`, dynamic downloads, and writes outside a constrained workspace when the plan originates from error-event text.
- Render or label event-originated markdown as quoted evidence. Do not let fields such as error messages, breadcrumbs, tags, context keys, stack traces, or "resolution" text appear indistinguishable from trusted MCP server guidance.
- Add allow-lists for diagnostic commands that agents may run while handling observability alerts. Prefer repository-local scripts reviewed in source control over one-off package downloads from public registries.
- Monitor developer endpoints and CI runners for `npx` / `npm exec` invocations following Sentry MCP queries, especially commands that reference newly published, scoped, or single-purpose packages.
- Review Sentry projects for unusual synthetic events that include markdown headings, code blocks, command lines, package names, or instructions to avoid source-code investigation.
- Keep developer-machine credentials narrow and short-lived. Assume an agent that can run shell commands can read environment variables, cloud config files, git credentials, package-manager tokens, and local repository data unless sandboxed.
- During response, preserve the Sentry event payload, MCP transcript, agent plan/tool-call logs, shell history, package-manager cache, and endpoint network telemetry before deleting suspicious events or packages.

## Why this matters
Agentjacking is a reusable prompt/tool-output injection pattern, not a one-off Sentry issue. Any external system that accepts attacker-controlled text and later feeds that text to an agent with file, shell, package-manager, browser, or network tools can become an execution path. The durable lesson is to bind agent privileges to data provenance: public or third-party records can help with triage, but they should not be able to create executable instructions without a separate trusted policy decision.

## Related pages
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [LangGraph checkpointer injection and unsafe deserialization](langgraph-checkpointer-injection-rce.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- [Tenet Security](https://tenetsecurity.ai/blog/agentjacking-coding-agents-with-fake-sentry-errors/)
- [The Hacker News summary](https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html)
