# Wiz Threat Research: inside 90 days of attacks on AI infrastructure

## Summary
Wiz Threat Research published **"Inside 90 days of attacks on AI infrastructure"** on **August 27, 2026**, sharing 90+ days of honeypot telemetry from its AI/ML service canaries: **LiteLLM, Flowise, LangChain, Langflow, ChromaDB, Ollama, and others**. The post organizes observed attack activity into three patterns: **(1) exploiting internet-facing MCP servers for remote code execution**, **(2) blind prompt injection against AI agent frameworks**, and **(3) AI-native post-exploitation** with tooling adapted to AI infrastructure internals. It is one of the first public datasets of *observed, in-the-wild* (honeypot) attacks specifically targeting self-hosted AI infrastructure, and it corroborates the gateway-control-point compromise pattern Microsoft Security Research documented on the same theme the day before — with independently observed attacker tooling, an IOC set, and a public external-researcher attribution of the LiteLLM MCP injection chain to the **Qilin ransomware group**.

Wiz frames AI infrastructure as a mainstream cloud attack surface: its State of AI in the Cloud report found **90% of cloud environments run self-hosted AI software**, 81% run managed AI services, and 63% self-host AI models. Two properties drive the targeting: **credential concentration** (a LiteLLM proxy can hold keys for every model provider it routes to, plus cloud IAM permissions and MCP tool connections) and **agent reachability** (inputs that drive tool execution create a blind-prompt-injection vector).

## Tags
- ops
- operations
- AI infrastructure
- honeypot
- LiteLLM
- LangChain
- Langflow
- Flowise
- Ollama
- ChromaDB
- Node-RED
- OpenWebUI
- MCP
- Model Context Protocol
- MCP gateway
- authentication bypass
- command injection
- RCE
- blind prompt injection
- XMRig
- cryptomining
- credential harvesting
- LLMjacking
- Qilin
- CVE-2026-59822
- CVE-2026-42271
- CVE-2026-48710
- Wiz
- threat research

## What was observed (90 days, 3 patterns)

### Pattern 1: MCP server exploitation against LiteLLM
Two MCP-specific vulnerability classes were exploited in the honeypots:

- **MCP gateway authentication bypass — CVE-2026-59822** (fixed in LiteLLM **1.84.0**; Wiz Research originally disclosed it earlier in 2026). The OAuth2 header handling is broken: when token validation fails, the server returns an **empty `UserAPIKeyAuth()` object with no restrictions** instead of rejecting the request. Any Bearer token — even a single character such as `x` — grants full MCP access. Observed in the wild: requests with `Authorization: Bearer x` probing model-enumeration endpoints (`GET /v1/models`).
- **MCP stdio test-endpoint command injection — CVE-2026-42271** (in CISA KEV since June 2026). The `command` field of a submitted MCP stdio server configuration is passed to subprocess execution with no validation. Attackers submitted a fake MCP stdio configuration whose `command` downloaded and executed a **gmon Monero miner** (`http://185.62.1[.]8/mon/mon.zip` → `/tmp/.dbus-cache/gmon`) via an inline Python script, then returned a valid MCP handshake so the connection test *appeared to succeed*. The miner runs detached (`start_new_session=True`); the staging directory is `rmtree`'d after launch while the process keeps the binary inode open — a successful test connection, a miner still running, and little left on disk. Command output is returned inside the `description` field of a fake tool in the `tools/list` response.
- **Chain:** CVE-2026-42271 chains with **CVE-2026-48710** (Starlette host-header validation bypass) to achieve **fully unauthenticated RCE**. **External researchers have linked the Qilin ransomware group to active exploitation of this chain.** Wiz's caveat: any tool that verifies an MCP configuration by spawning the configured command has the same failure mode if the path is attacker-reachable.

### Pattern 2: blind prompt injection against agent frameworks
Attacks across **LangChain, Flowise, OpenWebUI, and Node-RED** deployments injected prompts designed to make an agent execute an OS command. Confirmation was out-of-band: a DNS query to an attacker-controlled callback (often an OAST provider), with the **attacker IP encoded in the subdomain** and a per-session random string mapping each callback to a specific target. Wiz did not capture the natural-language payload; it reconstructed one consistent with the observed process trees and public playbooks: instruction-override framing, a directive to invoke whatever shell tool the agent has, an out-of-band callback, and an instruction not to reveal the payload to the user. After execution was confirmed, payloads were fetched from **Pastebin** rather than sent inline (keeping malicious content out of application logs), **base64-encoded to bypass naive prompt-level filtering**. Successful Node-RED sessions ended with **XMRig deployment at `/usr/src/node-red/xmrig`**, a path chosen to blend with the Node.js process tree.

### Pattern 3: AI-native post-exploitation
Post-exploitation was adapted to where AI infrastructure actually keeps secrets:

- **LiteLLM master key from process memory:** because the master key is not on disk, attackers queried the running process's Python module state directly: `import litellm; print(litellm.api_key)` and `litellm.proxy.proxy_server.master_key` / `litellm_master_key_hash`. The same sessions enumerated framework-specific config paths (`/app/litellm_config.yaml`, `/etc/litellm/.env`, `~/.litellm/config.yaml`) and **fingerprinted accessible backend models** before deciding whether to steal keys, abuse inference quota (**LLMjacking**), or move on.
- **Default master key:** instances running with the default master key (`sk-1234`) were probed with `POST /chat/completions` asking the backend to reveal its model name.
- **Camouflage:** on a Langflow honeypot, an attacker staged a miner at **`/app/data/.claude/`** and renamed the binary **`unicorn`** — a `.claude/` directory blends into any host where Claude Code runs, the same hiding approach recent supply-chain attacks use.

## Indicators (from the post)

| Indicator | Type | Description |
|---|---|---|
| 185.62.1[.]8 | IP | Malware download server (LiteLLM/MCP campaign) |
| 185.84.98[.]85 | IP | Cryptominer C2 |
| pool.hashvault[.]pro | Domain | Monero mining pool (multiple campaigns) |
| crazyeltonproxy[.]top | Domain | Monero mining proxy (LangChain + Node-RED) |
| 94.26.106[.]29 | IP | Langflow binary staging |
| 1710.rwlp.be | Domain | Compromised WordPress site, binary staging |
| `/tmp/.dbus-cache/` | Path | Cryptominer staging |
| `/tmp/.dbus-cache/gmon` | File | Monero miner binary |
| `/tmp/x86_64`, `/tmp/amd64` | File | Langflow dropper (self-deletes) |

## Defender priorities
1. **Treat "unauthenticated on the internet" as "compromised"** for the AI stack — Marimo, Flowise, Langflow, Ollama, ChromaDB, Milvus, and others ship without authentication; require auth by default.
2. **Patch LiteLLM ≥ 1.84.0** (CVE-2026-59822 auth bypass) and **≥ 1.83.7** (CVE-2026-42271 command injection), and **Starlette ≥ 1.0.1** (CVE-2026-48710 host-header bypass); hunt for the MCP test-endpoint chain and the `Bearer x` / `Bearer 1` probing pattern.
3. **Monitor at the runtime layer:** process-ancestry detection (an AI server spawning a shell), unexpected `/tmp/.dbus-cache/` creation, XMRig at AI-tooling paths, and `start_new_session` detached miners.
4. **Scope credentials aggressively:** model-provider keys, proxy master keys, and cloud IAM behind an AI proxy are a Tier-0 secret store; restrict lateral reach and egress.
5. **Patch faster than CVE assignment for open-source AI infra:** Wiz says attackers often weaponize new vulnerabilities as soon as fixes appear in code, ahead of CVE assignment.

## Assessment limits
- Findings are **honeypot telemetry**, not customer or production incident telemetry; Wiz explicitly presents these as observed attack patterns, not confirmed victim compromise.
- The **Qilin linkage** to the CVE-2026-42271 + CVE-2026-48710 chain comes from **external researchers**, is third-party attribution, and is not confirmed by Wiz.
- The blind-prompt-injection payload is a **reconstruction** consistent with observed process trees and public playbooks, not a captured payload.
- Wiz's product references (AI-APP, Secret Scanning, ASM, Red Agent, Runtime Sensor) are vendor capability claims, not detection results.

- **CISA KEV listing update (September 2, 2026):** both **CVE-2026-59822** (LiteLLM MCP auth bypass, BOD 26-04 due 2026-09-16) and **CVE-2026-48710** (Starlette host-header bypass, due 2026-09-16) were **added to the KEV catalog**, formalizing the in-the-wild status of the two MCP/RCE-chain components documented above (see the [CISA KEV September 2, 2026 page](cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)).

## Related pages
- [LiteLLM CVE-2026-42271 MCP stdio command injection](litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [Microsoft: AI infrastructure gateways and control points as high-value intrusion targets](microsoft-ai-infrastructure-gateways-control-points-august-2026.md)
- [Internet-exposed unauthenticated MCP servers](../patterns/internet-exposed-unauthenticated-mcp-servers.md)
- [MCP stdio command-execution boundary](../patterns/mcp-stdio-command-execution.md)
- [Chainlit MCP: unauthenticated RCE and SSRF via /mcp](../tools/chainlit-mcp-cve-2026-45018-45019-mcp-rce-ssrf.md)

## Sources
- Wiz Threat Research: [Inside 90 days of attacks on AI infrastructure](https://www.wiz.io/blog/ai-infrastructure-honeypot) (published August 27, 2026; RSS `Thu, 27 Aug 2026 16:33:16 GMT`)
- GitHub advisory for CVE-2026-42271 (LiteLLM MCP stdio command injection): [GHSA-v4p8-mg3p-g94g](https://github.com/BerriAI/litellm/security/advisories/GHSA-v4p8-mg3p-g94g)
- NVD: [CVE-2026-59822](https://nvd.nist.gov/vuln/detail/CVE-2026-59822), [CVE-2026-42271](https://nvd.nist.gov/vuln/detail/CVE-2026-42271)
- CISA KEV catalog: [https://www.cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
