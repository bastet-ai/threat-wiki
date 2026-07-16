# MCP stdio command-execution boundary

## Summary
OX Security reports a systemic command-execution boundary in Model Context Protocol (MCP) implementations that accept user- or network-controlled stdio server configuration. The issue is not a single package bug: MCP stdio transport intentionally launches a configured command, and downstream applications become vulnerable when they let untrusted input populate fields such as `command` and `args` without allow-listing or sandboxing.

OX frames this as an architectural vulnerability in Anthropic-maintained MCP SDKs and MCP-adapter ecosystems, and says it disclosed more than 30 related issues with 10+ CVEs across downstream platforms. Anthropic reportedly treated the core stdio behavior as expected protocol behavior, so defenders should treat MCP server configuration as a high-risk execution boundary rather than waiting for one universal protocol-side fix.

## Tags
- patterns
- AI tooling
- AI agents
- Model Context Protocol
- MCP
- stdio
- command execution
- RCE
- agent frameworks
- supply-chain
- developer machines
- LangChain
- LangFlow
- LiteLLM
- OX Security

## Attack shape
- An application exposes MCP server configuration through a UI, API, marketplace entry, or extension/package metadata.
- The application passes that configuration to MCP stdio transport primitives such as `StdioServerParameters` or adapter wrappers that eventually call the same subprocess-launch path.
- If an attacker can influence `command`, `args`, or equivalent fields, the MCP client or server launches attacker-selected processes under the application’s OS account.
- In exposed AI-agent or workflow platforms, this can become authenticated or unauthenticated remote command execution depending on how the platform gates configuration changes.
- In developer tooling, the same primitive can turn malicious MCP registry entries, copied JSON snippets, or typosquatted MCP servers into shell execution on developer workstations or CI runners.

## Public reporting
- Wiz Research reported `CVE-2026-12957` in Amazon Q Developer / Language Servers for AWS: Amazon Q automatically loaded `.amazonq/mcp.json` from a trusted workspace and spawned MCP servers with the developer's environment, turning a malicious repository into local command execution and potential cloud credential theft. AWS patched the issue in Language Servers for AWS and Amazon Q plugin releases.
- OX says the root pattern is direct configuration-to-command execution through MCP stdio interfaces in multiple language implementations and in intermediate adapters.
- OX says it successfully poisoned 9 of 11 MCP registries with a trial-balloon package, showing that marketplace and registry discovery can become a distribution channel for malicious MCP configuration.
- OX reports testing command execution on six live production platforms and names affected downstream projects including LiteLLM, LangChain, LangFlow, GPT Researcher, Agent Zero, Fay Framework, Bisheng, and Langchain-Chatchat.
- OX lists multiple downstream CVEs in its summary table, including CVE-2026-30623 for LiteLLM, CVE-2026-30624 for Agent Zero, CVE-2026-30618 for Fay Framework, CVE-2026-33224 for Bisheng, and CVE-2026-30617 for Langchain-Chatchat. Treat project-level patch status separately; the underlying stdio trust boundary remains a design and integration concern.
- The technical deep dive shows the vulnerable implementation pattern: user-controlled `command` / `args` flow into MCP stdio configuration, which then launches a subprocess.

## Defender heuristics
- Treat MCP configuration as code execution. Do not accept arbitrary stdio `command` or `args` from users, external registries, pull requests, chat transcripts, READMEs, or marketplace metadata.
- Prefer a small allow-list of preconfigured MCP servers. Let users select a known server profile rather than writing raw commands.
- If raw configuration is unavoidable, require explicit dangerous-mode gating, review, and least-privilege execution; never run it with broad filesystem, cloud, browser, SSH, or secrets access.
- Sandbox MCP-enabled services and developer tools. Containerize where practical, mount only required directories, block metadata-service access, and restrict outbound egress from MCP subprocesses.
- Instrument MCP subprocess creation: log parent process, command line, working directory, environment-secret exposure, network destinations, and tool invocations.
- Hunt for unexpected stdio MCP launches from AI-agent servers, IDEs, CI runners, and developer machines; investigate MCP tools that spawn shells, interpreters, downloaders, credential collectors, or archive utilities.
- Review MCP marketplace, registry, and extension ingestion paths for typosquatting, unverified publisher identity, mutable package metadata, and copied configuration snippets.
- Keep downstream AI-agent platforms patched, but do not assume patching one platform removes the MCP stdio risk from other tools in the environment.

## Related pages
- [MCP tool-description poisoning](mcp-tool-description-poisoning.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Amazon Q CVE-2026-12957 MCP auto-execution](../ops/amazon-q-cve-2026-12957-mcp-auto-execution.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](../ops/litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [PraisonAI CVE-2026-44338 rapid exploitation](../ops/praisonai-cve-2026-44338-rapid-exploitation.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](../ops/marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [LiteLLM compromise](../ops/litellm-compromise.md)
- [Supply-chain group profile](supply-chain-actor-profile.md)

## Sources
- [Wiz Research](https://www.wiz.io/blog/amazon-q-vulnerability)
- [AWS security bulletin 2026-047-AWS](https://aws.amazon.com/security/security-bulletins/2026-047-aws/)
- [OX Security](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/)
- [OX Security technical deep dive](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-technical-deep-dive/)
