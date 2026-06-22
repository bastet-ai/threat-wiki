# AI-agent memory poisoning

## Summary
Microsoft Security published a June 22, 2026 guidance post on **AI memory** as a new persistence surface for agents and assistants. The durable threat model is simple: once an agent can write and later retrieve memory, an attacker no longer needs to win in a single prompt. Untrusted content can seed malicious or misleading memory that affects future tool use after the original document, web page, chat, or ticket is out of view.

Treat agent memory as both sensitive data and behavior-shaping control state. It needs provenance, write-time validation, retrieval-time risk checks, audit logs, and user / administrator lifecycle controls.

## Tags
- patterns
- AI agents
- agent memory
- memory poisoning
- prompt injection
- indirect prompt injection
- delayed execution
- tool use
- data exfiltration
- provenance
- audit logging
- Microsoft
- Microsoft 365 Copilot
- Defender Advanced Hunting
- Sentinel

## Attack shape
- An agent or assistant processes attacker-controlled content: a shared document, web page, email, issue, ticket, repository file, chat message, calendar item, or observability record.
- The content includes hidden or adversarial instructions intended to influence what the agent stores as memory.
- The agent does not immediately take an obviously malicious action, so the exposure may look harmless in the original session.
- Later, during an unrelated task, the agent retrieves the poisoned memory and treats it as trusted context.
- The retrieved memory steers reasoning or tool calls: forwarding schedule updates, changing recipients, selecting attacker-controlled infrastructure, suppressing warnings, altering code-review criteria, or weakening future decisions.

Microsoft's example scenario is delayed tool execution: a user opens a shared document whose hidden instructions ask an assistant to exfiltrate schedule updates. Days later, the dormant instruction influences memory and causes later schedule updates to flow to the attacker.

## Why it matters
- **Temporal gap:** the malicious effect can happen long after ingestion, making user awareness and analyst reconstruction harder.
- **Context collapse:** memory can detach an instruction from the untrusted source that created it.
- **Policy bypass pressure:** single-turn prompt-injection defenses are insufficient if poisoned state can be replayed into future turns.
- **Blast-radius expansion:** memory may influence multiple future workflows, agents, tools, or users if isolation and provenance are weak.
- **Forensics burden:** responders need to know what changed, when, why, from where, and which later actions used that memory.

## Defender heuristics
### Design and hardening
- Require explicit user or service intent before persistent memory writes. Do not let arbitrary retrieved content silently become durable instruction state.
- Store provenance with every memory item: source object, source user or service, ingestion path, time, trust zone, and whether the source was external or untrusted.
- Enforce memory access, tenant isolation, and tool permissions outside the model. Prompt text is not an authorization boundary.
- Run write-time prompt-injection and task-adherence checks before memory is persisted.
- Re-evaluate memory at retrieval time for relevance, freshness, source trust, tampering, and policy fit before injecting it into model context.
- Separate factual preferences from executable instructions. Treat remembered instructions that request external communication, credential access, code execution, policy changes, or recipient changes as high risk.
- Give users and administrators clear review, edit, disable, delete, retention, and eDiscovery controls for memory.

### Detection and response
- Log memory create, update, delete, retrieval, and use events with enough context to reconstruct downstream tool calls.
- Alert on memory updates sourced from external documents, anonymous links, public repositories, untrusted tickets, customer-provided files, or other low-trust inputs.
- Hunt for memory updates followed by delayed high-impact tools: email forwarding, calendar sharing, file export, source-code modification, credential retrieval, deployment, package publication, or payment / custody actions.
- During an agent incident, preserve memory state before cleanup, then remove poisoned entries and rotate credentials or tokens reachable through affected agent tools.
- Correlate memory audit events with model/tool telemetry rather than reviewing chat transcripts alone.

Microsoft notes that Microsoft 365 Copilot records memory updates into organizational audit logs and exposes a `MemoryUpdated` field for Defender Advanced Hunting, Defender Sentinel, and Azure Portal Sentinel Analytics. Treat equivalent audit events as required telemetry for any enterprise agent-memory deployment.

## Questions for reviews
- Can memory be written from content the user did not explicitly trust?
- Can administrators identify the exact source and trust zone behind a memory item?
- Are memory writes and later retrievals linked to tool calls in logs?
- Can a user or SOC analyst remove a poisoned memory item and verify it is no longer retrievable?
- Are memory stores segmented by user, tenant, agent, workspace, and data classification?
- Does retrieval include policy checks, or does it blindly inject all matching memories into the prompt?

## Related pages
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/06/22/guarding-ai-memory/
