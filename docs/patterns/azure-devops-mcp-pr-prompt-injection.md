# Azure DevOps MCP pull-request prompt injection

## Summary
Manifold Security disclosed an indirect prompt-injection and confused-deputy path in Microsoft's open-source Azure DevOps MCP server. An attacker with contributor access to one project can hide instructions in an HTML comment inside a pull-request description. Azure DevOps does not render the comment to the human reviewer, but its API returns the raw Markdown and the MCP tool `repo_get_pull_request_by_id` passes the pull-request object into the agent's context.

In Manifold's proof of concept against a local, PAT-authenticated v2.7.0 server, Copilot CLI and Claude Code agents operating with auto-approved tools followed the hidden text, started a pipeline in another project, read a confidential wiki page, and posted the content back to the attacker's pull request. The attacker did not directly acquire the reviewer's rights; the agent used the reviewer's existing cross-project authority on the attacker's behalf.

As checked on July 22, 2026, no CVE or fixed public release was identified. The latest public release was v2.8.0, and the main-branch implementation still serialized the pull-request response directly rather than wrapping it with the repository's `createExternalContentResponse` spotlighting helper. This is a point-in-time source review, not a claim about future releases or hosted-service behavior.

## Tags
- patterns
- AI agents
- AI coding agents
- Azure DevOps
- Microsoft
- MCP
- Model Context Protocol
- indirect prompt injection
- confused deputy
- pull requests
- HTML comments
- hidden instructions
- cross-project access
- source code
- secrets
- wiki
- pipelines
- Copilot CLI
- Claude Code
- personal access tokens
- least privilege
- Manifold Security

## Attack prerequisites
The demonstrated chain requires all of the following:
- The attacker can create or edit a pull request in at least one Azure DevOps project.
- A more-privileged user or automation asks an AI agent to inspect that pull request.
- The agent receives raw attacker-controlled description text through the Azure DevOps MCP server.
- The agent's credential can reach other projects or sensitive resources that the attacker cannot access.
- The agent is allowed to invoke consequential MCP tools without a meaningful approval boundary.
- A write-capable tool, pull-request comment, work item, pipeline artifact, or other channel is available for exfiltration.

## Demonstrated chain
1. The attacker opens a plausible pull request and places instructions inside `<!-- ... -->` in its description.
2. The Azure DevOps web interface hides the comment, so the human sees an ordinary description.
3. The reviewer asks Copilot CLI or Claude Code to review the pull request through the Azure DevOps MCP server.
4. `repo_get_pull_request_by_id` retrieves the raw object, including the hidden comment, and serializes it into model context.
5. The injected text changes the agent's effective goal. Using the reviewer's authority, the agent triggers a pipeline in a different project and reads a wiki page unavailable to the attacker.
6. The agent posts the retrieved data as a comment on the attacker-controlled pull request.

Manifold tested a deliberate no-prompt/auto-approve posture. Per-tool confirmation could interrupt the sequence, but generic approval dialogs are not a strong control when they do not expose why a code-review task is crossing projects, starting pipelines, or publishing unrelated data.

## Root cause and status
- Microsoft added “spotlighting” support to the server in pull request 1062, merged March 30, 2026. The helper marks external content so the model can distinguish untrusted data from instructions.
- Manifold found inconsistent coverage: wiki and pipeline paths use the helper, while `repo_get_pull_request_by_id` returned the pull-request object without that wrapper.
- Current public main-branch source checked July 22 still returned `JSON.stringify(enhancedResponse, null, 2)` directly from that tool.
- Spotlighting is defense in depth, not a security boundary by itself. Even consistent delimiters cannot guarantee that a model will ignore adversarial text.
- Manifold tested the local PAT-based server. The shared code path suggests concern for other transports, but the researchers did not claim to have validated Microsoft's hosted remote MCP service.
- Microsoft told public reporting that this is a known class of AI risk and recommended limiting project access and reviewing proposed changes. No CVE was public at the time of review.

## Defender heuristics
### Reduce authority
- Give review agents project-scoped, read-only credentials where possible. Do not reuse a human administrator's broad PAT or interactive identity for routine pull-request review.
- Separate read tools from write/execution tools. A review profile should not need to start pipelines, read unrelated wikis, post arbitrary comments, change work items, or access every project in the organization.
- Use the server's domain-selection controls, including `-d` where applicable, to load only the Azure DevOps tool domains required for the task.
- Keep auto-approval disabled for cross-project reads, pipeline execution, comment posting, repository writes, work-item changes, and secret-bearing operations.

### Treat repository text as hostile
- Inspect raw pull-request Markdown, not only rendered HTML. Alert on HTML comments, CSS-hidden text, encoded instruction blocks, unusual role/instruction language, and content asking an agent to access another project or publish results.
- Label all pull-request descriptions, comments, work items, build logs, wiki text, commit messages, and artifacts as untrusted provenance before they enter model context.
- Do not depend on spotlighting alone. Enforce policy outside the model: project allow-lists, read/write separation, destination restrictions, and deterministic denial of unrelated tool calls.
- Bind every agent task to an explicit project, repository, pull request, allowed read set, and allowed output destination.

### Hunt and respond
- Review MCP/agent tool traces for a pull-request read followed by cross-project pipeline starts, wiki reads, source access, work-item queries, or comments unrelated to the requested review.
- Correlate Azure DevOps audit logs by identity and time sequence. Ordinary authenticated API calls become suspicious when a review task suddenly traverses projects or accesses resources the initiating contributor cannot reach.
- Search open and recently reviewed pull-request descriptions through the API for hidden HTML comments and preserve the raw descriptions, agent transcripts, tool-call logs, PAT scope, Azure DevOps audit events, pipeline logs, and posted comments.
- If sensitive data was exposed, remove the public/output copy only after preservation, revoke or rotate the agent credential, determine every resource it could read, and investigate additional exfiltration channels.

## Why this matters
This is a concrete version of the agentic “lethal trifecta”: access to private data, exposure to untrusted content, and a way to communicate outward. Every individual API call can be authorized while the overall sequence violates the user's intent. The durable control is therefore not just input sanitization; it is constraining the agent's authority and monitoring action sequences against the task it was given.

## Related pages
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)

## Sources
- Manifold Security: [https://www.manifold.security/blog/azure-devops-mcp-server-vulnerability](https://www.manifold.security/blog/azure-devops-mcp-server-vulnerability)
- Microsoft Azure DevOps MCP repository: [https://github.com/microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp)
- Spotlighting pull request 1062: [https://github.com/microsoft/azure-devops-mcp/pull/1062](https://github.com/microsoft/azure-devops-mcp/pull/1062)
- Current repository tool implementation: [https://github.com/microsoft/azure-devops-mcp/blob/main/src/tools/repositories.ts](https://github.com/microsoft/azure-devops-mcp/blob/main/src/tools/repositories.ts)
- Latest public release checked July 22, 2026: [https://github.com/microsoft/azure-devops-mcp/releases/tag/v2.8.0](https://github.com/microsoft/azure-devops-mcp/releases/tag/v2.8.0)
- Microsoft indirect prompt-injection defense overview: [https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)
- The Hacker News summary: [https://thehackernews.com/2026/07/microsoft-azure-devops-mcp-flaw-lets.html](https://thehackernews.com/2026/07/microsoft-azure-devops-mcp-flaw-lets.html)
