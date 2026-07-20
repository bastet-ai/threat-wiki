# FakeGit AgentBaiting and SmartLoader campaign

## Summary
Island Security Research disclosed **FakeGit** on July 20, 2026: a large GitHub malware-distribution operation that copies or fabricates projects, uses lookalike developer profiles and convincing READMEs, and directs users to malicious ZIP archives carrying **SmartLoader**. Island confirmed roughly **7,600 malicious repositories created by about 6,600 profiles**. More than 800 repositories posed as AI Skills or Model Context Protocol (MCP) servers, and campaign material appeared in more than 600 listings across public AI capability registries and catalogs.

Island calls the AI-discovery variant **AgentBaiting**. An AI assistant searching for a Skill or MCP server can independently surface a malicious repository, trust its README, and repeat the attacker's installation instructions without receiving a malicious link directly. Island reproduced this failure mode with Claude Code, Gemini, and ChatGPT, although results varied and some runs recognized the suspicious content.

## Tags
- ops
- operations
- FakeGit
- AgentBaiting
- SmartLoader
- StealC
- GitHub
- repository poisoning
- developer targeting
- AI agents
- agent skills
- MCP
- Model Context Protocol
- marketplace abuse
- social engineering
- malware delivery
- credential theft
- session theft
- LuaJIT
- blockchain dead drop
- Island Security Research

## Why this matters
- The campaign does not need to compromise a registry, maintainer, or vendor. It exploits open software discovery, copied reputation signals, and attacker-authored setup instructions.
- Public Skill and MCP catalogs can amplify unreviewed GitHub content and reproduce malicious README instructions; a catalog listing is not evidence that a capability was reviewed.
- AI assistants can become an additional social-engineering relay. Their search and summarization steps may transform malicious documentation into trusted-looking installation advice.
- The payload reaches developer endpoints close to browser sessions, source repositories, cloud tokens, build systems, and other high-value credentials.

## Reported scope
Island reported the following measurements as of July 2026:

| Measurement | Reported scope |
| --- | ---: |
| Confirmed malicious GitHub repositories | about 7,600 |
| Campaign profiles | about 6,600 |
| Repositories tied to AI tools, agents, or workflows | about 1,400 |
| Repositories posing as Skills or MCP servers | more than 800 |
| Campaign listings in public Skill/MCP catalogs | more than 600 |
| Measured GitHub Release asset downloads | more than 14 million across about 200 repositories |

The download figure covers measurable GitHub Release assets. Island noted that thousands of other repositories embedded ZIP files directly, where public download counts were unavailable. These are campaign-scale measurements, not confirmed infection counts.

The AI-themed wave grew through March and peaked in April 2026. Island found lures spanning consumer integrations and enterprise tooling, including Gmail, WhatsApp, Databricks, Jenkins, Docker, source-code, cloud-service, database, API, and security-workflow themes. Sixty-two percent of the malicious Skill and MCP repositories were positioned for enterprise or internal-developer use.

## Deception and delivery chain
FakeGit builds credibility through several layers:

1. Copy an established project or fabricate a plausible tool.
2. Publish it from a lookalike profile, sometimes differing from a legitimate developer name by one character.
3. Add familiar documentation, modest stars or forks, and a plausible enterprise or developer use case.
4. Present a ZIP archive as the release, installer, Skill, plugin, or MCP server.
5. Tell the user—or an AI assistant acting as an installation guide—to extract and run it.

Island's `45d5r/databricks-mcp-server` example advertised 263 Databricks tools, but its ZIP contained only a command launcher, `luau.exe`, and `ico64.txt`. The launcher ran:

```text
start luau.exe ico64.txt
```

`luau.exe` was a renamed LuaJIT-style runtime. The apparent text file was an approximately 300 KB, single-line, heavily obfuscated Lua program. Filenames differ across samples, but Island describes a recurring structure: a small `.cmd` or `.bat` launcher, a LuaJIT-style runtime, and executable Lua disguised as a text, icon, license, or data file.

Independent FakeGit analysis by Derp.ca describes subsequent behavior in analyzed variants: hide the console, resolve current command infrastructure from a Polygon smart contract, create scheduled-task persistence under `%LOCALAPPDATA%`, retrieve encrypted stages from GitHub dead-drop repositories, and use a PE crypter to inject **StealC** into another process. StealC then targets browser passwords and cookies, active sessions, browser-extension data, email and remote-access credentials, screenshots, and host information.

Treat this sequence as behavior observed in analyzed FakeGit variants rather than proof that every one of the thousands of reported repositories contains an identical payload.

## AgentBaiting
Island demonstrated that the malicious repository does not have to be supplied directly to the model:

- Claude Code independently found a malicious cinematic-prompt Skill through search and a marketplace. In one run it repeated instructions to download and run an executable and bypass a Windows warning; in other runs it rejected the content.
- Gemini and ChatGPT surfaced a malicious Walmart-themed MCP repository from a generic request for a free Walmart MCP server.
- More than 600 campaign listings appeared across LobeHub, Glama, MCP.so, and MCP Market. Some listings reproduced repository READMEs and raw GitHub download links.

The durable issue is **discovery-to-execution provenance**. Search relevance, repository popularity, copied documentation, and marketplace indexing can all be attacker-controlled or misleading. An assistant's natural-language recommendation does not establish publisher identity, code integrity, or safe runtime behavior.

## Detection and response guidance

### Discovery and governance
- Maintain an allowlisted catalog of reviewed Skills, MCP servers, plugins, and agent extensions. Record source repository, immutable commit, version, publisher identity, and artifact hash.
- Do not treat GitHub stars, forks, profile similarity, README quality, or public marketplace placement as security signals.
- Require source and manifest review. Reject a purported Skill or MCP server that installs through an unexplained Windows executable or a ZIP containing only a launcher, renamed interpreter, and opaque payload.
- Evaluate new capabilities in an isolated environment with no browser sessions, cloud credentials, SSH keys, source-control tokens, production data, or access to developer home directories.
- Log agent-originated downloads, clones, shell commands, writes to Skill directories, and changes to MCP configuration with the same scrutiny as user-originated software installation.

### Endpoint and network hunting
- Hunt for `.cmd` or `.bat` launchers invoking `luajit.exe`, `luau.exe`, or an unusually named runtime against a `.txt`, icon, license, or data file.
- Flag extracted GitHub ZIPs that contain no expected source or manifest and instead pair a small launcher with a roughly 300 KB single-line obfuscated Lua payload.
- Review scheduled tasks executing from `%LOCALAPPDATA%`, especially when preceded by a GitHub ZIP download and followed by GitHub dead-drop retrieval or Polygon RPC traffic.
- Hunt for process hollowing or injection after a LuaJIT-style runtime, followed by browser credential-store, cookie, extension, email-client, remote-access, or screenshot collection.
- Match observed repository names and ZIP hashes against Island's maintained artifact list rather than relying only on the representative indicators below.

### Incident response
- If SmartLoader execution is suspected, isolate the endpoint and preserve the downloaded archive, extracted files, process tree, memory, scheduled tasks, browser state, network telemetry, and agent/tool logs.
- Revoke active browser sessions, OAuth grants, API tokens, source-control and package-registry credentials, cloud credentials, SSH keys, and remote-access credentials reachable from the host. Password reset alone is insufficient because StealC targets live sessions.
- Review repositories, CI/CD systems, cloud audit logs, and SaaS applications for follow-on use of credentials stolen from the developer endpoint.

## Representative indicators
These are selected examples from Island's disclosure, not the full campaign set. Repository availability can change after platform response.

| Repository | Reported archive | SHA-256 |
| --- | --- | --- |
| `Mann1988/awesome-claude-skills` | `awesome-skills-claude-3.3.zip` | `91e5dbfaf45edf25fbc2168f92083e05dfa427afa7633e991392e33cc7427dad` |
| `StanLeyJ03/mcp-for-security` | `for-security-mcp-3.3.zip` | `62744baa8077bb8be237647fd78e3bea2ca0932bf4be3d5618600f97118095f8` |
| `DomingosNgongo/walmart-mcp` | `mcp-walmart-2.2.zip` | `c15693106682f2ddb26649cab6e1962a64537627cde4c5d3c79d5a0be8c1b5a8` |
| `45d5r/databricks-mcp-server` | `server_databricks_mcp_1.6.zip` | `66afc7d87d10dbe392898c4e5c613e0442fabb396415c2bef3a5ef2ac752c5ad` |
| `MauManto/jenkins-mcp-server` | `mcp-server-jenkins-3.2.zip` | `a33f40cab1ab7f971d3464af3e7595918107332b9e83342007571842b9e22826` |
| `waynestimulative605/docker-mcp-gateway` | `gateway-docker-mcp-v1.6-alpha.5.zip` | `3c858facbad66f5479e2c4add171421dc1b6488b36f33e7cff073aba585954a7` |

## Attribution caveats
Island describes FakeGit as an established operation but does not identify a named real-world actor in this disclosure. Derp.ca assesses that a Vietnamese-speaking operator has distributed the LuaJIT-based campaign through GitHub since March 2025. Language, shared payloads, and infrastructure are useful clustering evidence but do not independently establish legal identity or prove that every repository was operated by one person.

## Related pages
- [Agent skill marketplace poisoning](../patterns/agent-skill-marketplace-poisoning.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Phantom squatting AI-hallucinated domains](../patterns/phantom-squatting-ai-hallucinated-domains.md)
- [StealC / Amadey infrastructure disruption](stealc-amadey-infrastructure-disruption.md)
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)

## Sources
- Island Security Research: [AgentBaiting: How 800+ Fake AI Skills and MCP Servers Delivered Malware](https://www.island.io/blog/agentbaiting-how-800-fake-ai-skills-and-mcp-servers-delivered-malware)
- Island Security Research Artifacts: [AgentBaiting repository and ZIP indicators](https://github.com/island-io/island-security-research-artifacts/tree/main/agentbaiting)
- Derp.ca: [FakeGit LuaJIT GitHub campaign](https://www.derp.ca/research/fakegit-luajit-github-campaign/)
