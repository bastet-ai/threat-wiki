# Agentic workflow trust-boundary failures

## Summary

July 2026 public research added two high-signal agentic-workflow boundary failures:

- **GitLost** — Noma Labs reported that GitHub Agentic Workflows could be steered by an unauthenticated public GitHub issue into reading private-repository content and posting it back to the public issue thread, when the workflow was configured with broader organization repository read access.
- **WriteOut** — SAND Security reported a Writer AI live-preview isolation flaw where a shared preview link could cause a logged-in victim's Writer session cookie to be forwarded into an attacker-controlled sandbox, enabling account takeover with the victim's privileges. Writer fixed the issue by removing the dashboard session credential from preview sandboxes and moving previews onto an isolated origin.

These are not the same bug class, but they point to the same defender lesson: agentic workflows collapse untrusted content, ambient identity, tool permissions, code execution, and SaaS session state into one execution path. Every boundary needs to be explicit: which text is instruction versus data, which repositories or tenants the agent identity can read, which browser/session credentials reach preview code, and which outputs may be published externally.

## Tags

- patterns
- AI agents
- agentic workflows
- prompt injection
- indirect prompt injection
- sandbox escape
- SaaS
- GitHub
- Writer AI
- session theft
- data exfiltration
- private repositories
- trust boundaries
- GitLost
- WriteOut

## GitLost: public issue to private-repository leak

Noma Labs' July 6, 2026 GitLost report describes a prompt-injection path in GitHub's technical-preview Agentic Workflows. The tested workflow was configured to trigger on `issues.assigned`, read the issue title/body, post a comment through an `add-comment` tool, and run with read access to other repositories in the same organization, including private repositories.

The attack shape is simple:

1. An unauthenticated attacker opens a plausible issue in a public repository owned by an organization using the workflow.
2. The issue body carries natural-language instructions that the agent treats as tasking rather than untrusted user content.
3. When the issue is assigned, the workflow runs, the agent reads the public issue, and the injected instructions ask it to retrieve content from both public and private repositories.
4. The agent posts the retrieved content back as a public issue comment, making private-repository data readable to anyone with access to the public issue.

Noma reported that adding the word **“Additionally”** helped bypass guardrail behavior in their test by causing the model to reframe its output rather than refuse. Treat that as a concrete reminder that LLM guardrails are brittle when the underlying workflow grants the agent broad read scope and a public write-back channel.

Defensive takeaways:

- Do not let public issue, discussion, PR, comment, or README text become instructions for an agent that has private-repository or organization-wide access.
- Use separate, least-privilege GitHub App / workflow identities for public-repository triage versus private-repository maintenance.
- Block or require human approval before an agent copies repository contents, secrets-like strings, configuration files, or internal documentation into public comments.
- Treat external issue text as data. Quote, summarize, or classify it instead of handing it to an agent as executable instructions.
- Log agent tool calls with repository names, visibility, triggering actor, event type, and output destination. Alert when a workflow triggered from a public repository reads private repositories or writes unusually large comments.

## WriteOut: shared AI preview to cross-tenant session takeover

SAND Security's July 2026 WriteOut disclosure covers a different agentic SaaS failure: an attacker could build a Writer AI agent with a live preview, share the public preview link, and collect session tokens from logged-in Writer users who opened it.

The reported root cause was origin and credential forwarding rather than prompt injection alone:

1. Writer served agent live previews under the main Writer application origin instead of an isolated preview origin.
2. A victim logged in to Writer opened an attacker-controlled preview link.
3. The victim's browser attached the Writer session cookie to the preview request.
4. The preview proxy forwarded that session cookie into the attacker's sandbox.
5. Code running in the attacker-controlled sandbox read and exfiltrated the token.
6. The attacker replayed the token and acted as the victim inside Writer.

SAND reported that impact could include access to private chats, sensitive documents and files, agent configurations, system prompts, private models, connectors, data sources, LLM credentials, and administrative settings depending on the victim's role. The attacker and victim did not need to be in the same organization.

SAND also noted a secondary guardrail gap: input filtering looked at submitted instructions rather than runtime behavior, so an attacker could ask the agent to fetch and run a remote script instead of embedding the exploit logic inline. The decisive fix was not a stronger prompt filter; it was removing high-value session credentials from preview sandboxes and isolating the preview origin.

Defensive takeaways:

- Treat AI preview, plugin, and sandbox runtimes as hostile execution surfaces when they can be shared across users or tenants.
- Never forward dashboard, admin, or broad SaaS session cookies into user-authored sandbox code. Use narrowly scoped preview tokens with separate origins and explicit audience limits.
- Inventory AI products that host live previews, embedded agent apps, notebooks, code sandboxes, or “run generated code” features under primary application domains.
- Inspect runtime behavior, not just prompt text. Fetch-and-run patterns, child-process execution, memory reads, and network egress from preview sandboxes should be logged and policy-controlled.
- Add session-replay detection around AI-builder platforms: new device/IP/token use after opening a shared preview link, rapid access to agents/connectors/data sources, or administrative changes after preview activity.

## Defender checklist

- **Separate instruction from data:** content from issues, PRs, documents, web pages, tickets, chats, and previews should be labeled as untrusted data when an agent consumes it.
- **Minimize ambient authority:** agent identities should not inherit broad organization repository, SaaS, cloud, connector, or browser-session access by default.
- **Constrain output channels:** agents that can read private data should not be able to post to public issues, external tickets, emails, webhooks, or attacker-controlled tools without approval.
- **Isolate agent runtimes:** use separate origins, tenants, containers, and credentials for preview/sandbox code; do not rely on “sandbox” as a trust boundary if privileged tokens are placed inside it.
- **Approve sensitive joins:** require human approval when a workflow combines untrusted external input with private-repository reads, connector access, bulk export, credential reads, or public write-back.
- **Capture evidence:** preserve trigger payloads, prompts, generated plans, tool-call logs, repository/API access logs, preview URLs, sandbox network traces, and session-token events during incident response.

## Related pages

- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)

## Sources

- Noma Labs: https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/
- SAND Security: https://www.sandsecurity.ai/blog/writeout-writer-ai-cross-tenant
- The Hacker News GitLost summary: https://thehackernews.com/2026/07/public-github-issue-could-trick-github.html
- The Hacker News WriteOut summary: https://thehackernews.com/2026/07/writer-ai-flaw-could-let-agent-previews.html
