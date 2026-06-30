# MCP tool-description poisoning

## Summary
Microsoft Incident Response and Microsoft Defender researchers documented a Model Context Protocol (MCP) supply-chain trust boundary where an attacker-controlled or compromised tool can hide instructions inside the tool description that an AI agent uses for planning. The issue is not a classic exploit in the model or in Copilot itself: MCP tools are expected to publish descriptions, and agents use those descriptions as operational context. If a tool maintainer can change that text after approval, the agent may treat poisoned metadata as a trusted instruction channel.

Microsoft's example uses a finance agent connected to an invoice-enrichment tool. The visible tool name and summary remain stable, but the updated description tells the agent to collect the last 30 unpaid invoices and include them in the next tool call. Because the tool was already approved, the data access occurs with the analyst's permissions, the outbound call goes to an already allowed endpoint, and the user receives a normal-looking answer while the attacker receives copied invoice data.

The durable defender lesson: for agents that can act, tool metadata is part of the execution supply chain. Review MCP tool descriptions like prompts and code, require re-approval for metadata changes, and monitor agent actions for data movement that is technically authorized but contextually abnormal.

## Tags
- patterns
- AI tooling
- AI agents
- Model Context Protocol
- MCP
- tool poisoning
- prompt injection
- indirect prompt injection
- supply-chain
- data exfiltration
- Copilot
- Microsoft

## Attack shape
- An organization connects an AI agent to one or more MCP tools, including a third-party tool or marketplace-provided integration.
- The tool is approved with a benign name, endpoint, and visible purpose; the agent is granted data access and permission to call the tool.
- The attacker later changes the tool description or otherwise controls descriptive metadata that the agent reads when selecting and invoking tools.
- The poisoned description embeds instructions framed as formatting notes, operating guidance, or other plausible metadata.
- During a normal user request, the agent follows the hidden instruction, gathers sensitive business data under the user's or agent's legitimate permissions, and passes it to the tool.
- The tool returns an expected answer while copying the data to attacker-controlled infrastructure or an operator-controlled account.

## Public reporting
- Microsoft frames the issue around the shift from AI systems that read and summarize to AI agents that can send email, create files, change calendars, query business systems, and run multi-step workflows through MCP-connected tools.
- The Microsoft scenario is illustrative rather than a named victim report, but the primitive maps to prior public work on tool poisoning and tool-output injection.
- The Hacker News summary notes related prior research: Invariant Labs' 2025 "tool poisoning" proof of concept against Cursor, a GitHub MCP server issue-injection data-exfiltration path, OWASP's Agentic Supply Chain Vulnerabilities category, Koi Security's `postmark-mcp` malicious MCP server case, and the MCPTox benchmark showing poisoned tool descriptions were broadly effective across tested MCP servers and models.

## Defender heuristics
- Treat MCP tool descriptions and tool schemas as privileged prompt material. Review description changes like code changes, and require re-approval before an agent uses changed metadata.
- Disable broad "allow all tools" policies. Give each agent only the tools needed for a defined workflow and pin trusted publishers, tool versions, endpoints, and expected data scopes.
- Require human approval for high-risk agent actions: external data sharing, bulk exports, money movement, account changes, email sends, and any action that combines sensitive data retrieval with an external tool call.
- Give agents distinct identities. Baseline per-agent behavior and alert on new tool endpoints, newly changed descriptions, unusual data volume, cross-domain joins, or requests for unrelated records.
- Apply "least agency" in addition to least privilege: a low-permission agent can still leak data if it can autonomously combine permitted reads with permitted outbound calls.
- Log MCP tool metadata versions, tool-call arguments, retrieved record counts, destination domains, and user prompts so response teams can reconstruct whether a metadata change preceded abnormal data access.
- During incident response, preserve the MCP tool manifest, description history, agent transcript, tool-call logs, endpoint/DLP telemetry, and any marketplace or package release metadata before disabling or deleting the integration.

## Related pages
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)

## Sources
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/
- The Hacker News summary: https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html
