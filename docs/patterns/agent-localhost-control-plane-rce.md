# Agent localhost control-plane RCE

## Summary
Microsoft Security Research described **AutoJack**, an exploit chain in the development branch of AutoGen Studio where untrusted web content rendered by a browsing AI agent could cross the loopback boundary, connect to a local MCP WebSocket control plane, and spawn arbitrary processes through attacker-supplied `StdioServerParams`.

Microsoft says the affected MCP WebSocket route was hardened in upstream commit `b047730` before it shipped in a PyPI release. Users who install `autogenstudio` from PyPI were not exposed to this specific chain. The durable lesson is broader: if an agent can browse untrusted content and also reach privileged localhost services, loopback is not a security boundary.

## Tags
- patterns
- AI agents
- agent frameworks
- AutoGen Studio
- AutoJack
- localhost
- loopback
- Model Context Protocol
- MCP
- WebSocket
- stdio
- command execution
- RCE
- confused deputy
- developer machines
- browser automation
- prompt injection
- Microsoft

## Attack shape
- A developer or service runs an AI-agent framework on a workstation or server.
- The agent has a browsing tool, headless browser, code-execution tool, or HTTP/WebSocket-capable tool that can render or fetch attacker-controlled content.
- A privileged local service also runs on `localhost` / `127.0.0.1`, such as an agent control plane, MCP bridge, debugger, code executor, database admin surface, or development API.
- The local service trusts loopback origin, skips authentication for WebSocket or API paths, or accepts high-risk parameters from requests.
- Attacker-controlled content steers the agent into contacting the local service as a confused deputy. From the service's perspective, the request comes from the same host and can satisfy localhost allowlists.
- If the control plane can launch tools or subprocesses, the chain becomes remote code execution on the host running the agent.

## AutoJack case study
Microsoft's AutoJack writeup chains three weaknesses in AutoGen Studio's development MCP WebSocket surface:

1. **Origin allowlist that trusted localhost**: the MCP WebSocket accepted origins such as `http://127.0.0.1` and `http://localhost`. That blocks a normal browser tab on an attacker domain, but not JavaScript rendered by a headless browser controlled by an agent running on the same machine.
2. **Authentication skipped for MCP paths**: AutoGen Studio's middleware skipped `/api/mcp/*` and `/api/ws/*` paths on the assumption that WebSocket handlers would enforce their own checks. The MCP handler did not add a separate authentication check.
3. **URL-supplied stdio server parameters**: the WebSocket accepted a base64-encoded `server_params` query parameter, parsed it into `StdioServerParams`, and passed `command` / `args` to MCP stdio launch logic without an executable allowlist.

The proof-of-concept shape was simple: get an AutoGen browsing agent, such as a web-page summarizer using `MultimodalWebSurfer`, to render a malicious page. The page's JavaScript opened a WebSocket to `ws://localhost:8081/api/mcp/ws/<id>?server_params=<base64>`. The payload could specify commands such as `calc.exe`, `powershell.exe`, or `bash -c ...` as an MCP "server" process.

Microsoft says the vulnerable chain was addressed on AutoGen Studio's main branch by moving MCP parameters to a server-side `POST /api/mcp/ws/connect` flow keyed by UUID, refusing unknown WebSocket session IDs, and tightening the authentication skip list so `/api/mcp` no longer bypasses normal auth. The affected route was not present in the current PyPI package inspected by Microsoft.

## Defender heuristics
### Architecture and hardening
- Treat localhost as reachable by any agent, browser automation process, plugin, extension, or sandbox escape path running under the same user context.
- Require authentication and authorization on all agent control planes, including WebSocket, MCP, debug, code-execution, and `/api/*` routes. Do not rely on Origin or loopback checks alone.
- Do not accept raw process-launch parameters from URLs, chat content, web pages, plugin metadata, repository files, or MCP registry entries.
- Use allowlisted MCP server profiles instead of caller-supplied `command` / `args`. If arbitrary stdio configuration is unavoidable, require explicit review and run it in a constrained sandbox.
- Separate browsing agents from control planes. Use different OS users, containers, VMs, or cloud dev boxes for agents that render untrusted content.
- Run research-grade agent frameworks as low-privilege users with minimal filesystem, browser-profile, credential-store, cloud-token, SSH, and source-repository access.
- Block or tightly monitor agent egress to loopback management ports that the agent does not need.

### Detection and response
- Hunt for agent framework processes followed by unexpected child processes such as shells, PowerShell, `bash`, `curl`, `wget`, `mshta`, `rundll32`, `regsvr32`, `certutil`, archive tools, or credential utilities.
- On hosts running AutoGen Studio experiments, review local connections to ports such as `8081` / `8080` with paths containing `/api/mcp/ws/` and `server_params=`.
- Correlate browser-automation processes (`python`, `node`, Playwright, Chromium, `MultimodalWebSurfer`, or framework-specific agent runners) with navigation to non-corporate domains during local agent sessions.
- Treat confirmed arbitrary subprocess launch from an agent control plane as developer-host compromise: preserve evidence, rotate source-control, package-registry, cloud, LLM-provider, SSH, and CI/CD credentials accessible from the host, then rebuild from trusted media.
- Inventory agent-framework builds installed from Git branches or source checkouts separately from PyPI/npm releases; development branches may include unshipped attack surfaces.

## Related pages
- [MCP stdio command-execution boundary](mcp-stdio-command-execution.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Claude Code GitHub Action prompt-injection boundary](claude-code-github-action-prompt-injection.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/06/18/autojack-single-page-rce-host-running-ai-agent/
