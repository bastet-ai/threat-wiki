# Microsoft: AI infrastructure gateways and control points as high-value intrusion targets

## Tags
- ops
- operations
- AI infrastructure
- LLM gateway
- LiteLLM
- RAGFlow
- Kestra
- credential theft
- cryptomining
- XMRig
- supply-chain
- MITRE ATT&CK
- control plane
- Docker socket
- /proc/1/environ
- OAST
- DNS rebinding

## Summary

On August 26, 2026, Microsoft Security Research published "When AI infrastructure becomes the target: Securing gateways and control points," documenting three distinct compromises of AI workloads — a **LiteLLM** LLM proxy gateway, a **RAGFlow** retrieval-augmented-generation deployment, and a **Kestra** workflow orchestration environment. Although the initial-access vectors differed, the post-compromise objectives converged: **credential theft, durable host access, and compute-resource monetization (cryptomining)**. The post frames AI gateways, retrieval platforms, and orchestration services as a new Tier-0 layer that concentrates model-provider keys, database connection strings, workflow execution, and container privileges in a single runtime context.

This page focuses on the operational chain, indicators, and defender takeaways from the Microsoft publication. It complements the existing [LiteLLM compromise](litellm-compromise.md) and [LiteLLM CVE-2026-42271](litellm-cve-2026-42271-mcp-stdio-command-injection.md) pages by adding three new case studies, a new IOC set, and a durable "AI infrastructure as control point" defender pattern.

## Case study 1: LiteLLM gateway compromise

### Initial access
Microsoft assesses with **high confidence** that initial access occurred through exploitation of the exposed LiteLLM gateway surface, consistent with the vulnerability chain involving:
- **CVE-2026-42271** (authenticated command execution via MCP stdio test endpoints)
- **CVE-2026-48710** (Starlette host-header validation bypass)

The chain: CVE-2026-42271 provides the command-execution capability through the MCP stdio test path, while CVE-2026-48710 weakens the authentication boundary in affected configurations, potentially making that capability reachable without valid credentials.

### Observed attack chain
| Stage | Activity |
|-------|----------|
| 1. Credential harvesting | Payload read the gateway process environment (`/proc/1/environ` in containerized PID-1 deployments), filtered for credential-related values (model-provider API keys, LiteLLM master key, database connection strings, UI credentials, tokens, passwords), and exfiltrated via Python urllib, curl, and wget fallbacks |
| 2. Payload delivery | Two paths: (a) inline Python launched from the gateway process retrieved a masqueraded ELF binary staged under a temporary path, marked executable, and launched with service-process-style arguments; (b) a shell-stage downloader with multiple download methods, short timeouts, and fallback behavior |
| 3. Host discovery | Fingerprinted the host, checked privilege boundaries, inspected listening ports, and searched for competing miners or remote-access activity. Silent passwordless-sudo check, multiple process sweeps for miner/RAT tooling |
| 4. Cryptominer preparation | XMRig or XMRig-like mining components with RandomX-related tuning. Loaded the Linux **Model-Specific Register (MSR) module** with write access enabled (a behavior commonly associated with RandomX/XMRig CPU tuning). Crontab rewrite removed entries associated with other miner names |
| 5. Database access | Used the collected database connection string to access the LiteLLM-backed **Azure Database for PostgreSQL**. A self-contained `python3` one-liner parsed `DATABASE_URL`, installed/imported PostgreSQL support, connected, and dumped `LiteLLM_ProxyModelTable` and `LiteLLM_VerificationToken` records. Output base64-encoded and exfiltrated in small chunks to an OOB callback endpoint |
| 6. Persistence / C2 / defense evasion | Service-account **SSH authorized_keys** modification, hidden-file relay execution, masqueraded systemd service names, self-relaunch loops under hidden temporary files, and **immutable-file attributes** (`chattr +i`) |

### Impact
Provider credential exposure, proxy-issued virtual-key exposure, database-backed configuration access, host resource abuse, and durable service-account access.

## Case study 2: RAGFlow compromise

### Framework role
RAGFlow supports document-processing and retrieval-augmented-generation workflows and stores tenant LLM configuration. The affected code paths process provider credentials when users add or modify LLM settings.

### Initial access
Microsoft assesses with **high confidence** that initial access likely occurred through exploitation of the exposed RAGFlow application surface. Telemetry showed the RAGFlow server process retrieving an attacker-supplied URL through the application's own HTTP client, resulting in an **outbound Burp Collaborator callback** without corresponding child-process execution. Remote code execution in the same service context followed several days later.

Microsoft assesses with **low confidence** which specific vulnerability, if any, enabled that code execution. Publicly documented vulnerabilities affecting relevant RAGFlow versions include:
- **CVE-2026-45312** — authenticated Jinja2 SSTI in the prompt generator
- **CVE-2026-28797** — authenticated Jinja2 SSTI in the Agent workflow component
- **CVE-2026-24770** — MinerU parser path-traversal (arbitrary file overwrite → code execution)
- **CVE-2025-68700** — Canvas CodeExec sandbox-bypass (GHSA-8xw3-v6c2-j84j)
- **CVE-2025-69286** — account-access weakness that could influence access to authenticated functionality

None of these are attributed as the confirmed cause. The possible SSRF activity through the OASTify relay network is a useful precursor signal because RCE in the same service context followed.

### Observed attack chain
| Stage | Activity |
|-------|----------|
| 1. Application discovery and hook creation | Located the RAGFlow installation from inside the container, identified the tenant LLM model-configuration path, and created a hidden runtime hook under the application tree |
| 2. Persistence through startup modification | Modified the application startup or import path so the hidden hook would load with the RAGFlow service |
| 3. Credential interception | The hook **monkey-patched `TenantLLM.insert()`** to intercept provider API keys (OpenAI, Azure, Anthropic, Gemini) on every LLM configuration event, capturing provider type, model name, API key material, and endpoint metadata. Exfiltrated via outbound HTTP from within the container |
| 4. Finalization | Wrote/refreshed the hook and created a local marker indicating installation had completed |

### Impact
Primarily LLM credential collection rather than host monetization. No miner deployment or interactive reverse shell observed. SSH-key material was also written inside the container.

## Case study 3: Kestra compromise

### Framework role
Kestra is a workflow orchestration environment. Abuse of workflow-creation and execution capabilities can provide direct code execution in the worker runtime.

### Initial access
Microsoft assesses with **high confidence** that initial access involved exploitation of **CVE-2026-49869**, a critical authentication-bypass vulnerability in Kestra. Exploitation allows an unauthenticated remote attacker with network access to bypass the login mechanism, define a malicious workflow using the Process runner, and trigger worker-side shell-script execution.

### Observed attack chain
| Stage | Activity |
|-------|----------|
| 1. Workflow-origin shell execution | Two closely timed workflow-origin shell sessions; the first produced shell initialization, the second performed the main follow-on actions |
| 2. Docker container environment discovery | Accessed the **mounted Docker socket** from inside the orchestration environment. Queried container metadata and inspected container environment arrays, exposing environment-backed values from other containers reachable through the socket |
| 3. Cryptominer deployment | XMRig retrieval from a public release source, archive extraction, binary renaming, background execution, and mining-pool communication. CPU-tuning behavior commonly associated with RandomX/XMRig. Defence-evasion file operations around a temporary path including restrictive permissions and immutable-file attributes |
| 4. Data harvesting | Later workflow-origin event used a **curl-pipe-shell** pattern for follow-on collection. Remote script content retrieved and executed directly by the shell without being written as a standalone file. Output encoded and stored through Kestra's own key-value interface |

### Possible AI-assisted payload development
Several payloads exhibited characteristics often associated with assisted or generated code: organized imports, explicit timeout handling, dependency fallbacks, formatted output, defensive exception handling, and explanatory comments. Microsoft explicitly states these are **observations about the tooling, not evidence of attribution**.

## Key patterns across AI workloads

| Pattern | Detail |
|---------|--------|
| Initial access varied by workload | LiteLLM: command execution from gateway runtime. RAGFlow: SSRF-style probing → runtime modification. Kestra: workflow execution as shell-access path |
| Consistent objectives | Credential collection, durable access mechanisms, and resource monetization |
| Payload behavior specific to each workload | LiteLLM: gateway env vars + DB proxy records. RAGFlow: LLM credential configuration. Kestra: workflow execution + container discovery + cryptomining |
| Docker socket as privilege amplifier | Kestra's mounted Docker socket exposed container environment arrays containing cloud keys, database passwords, API tokens, and internal service endpoints |
| /proc/1/environ as secret store | In containerized AI gateways where the service runs as PID 1, `/proc/1/environ` exposes model-provider API keys, the gateway master key, database connection strings, and UI passwords |
| AI-assisted payload development | Structured imports, timeout handling, dependency fallbacks, non-English comments; improves portability across Linux and container environments |

## Defender takeaways

### Treat AI gateways as Tier-0 secrets stores
- Keep LiteLLM and similar proxies patched; require authentication across API and UI surfaces
- Restrict administrative and management ports; do not expose management interfaces directly to the internet
- Issue per-team virtual keys with spend limits instead of sharing master keys
- Store upstream API keys in a managed secret store rather than process environment variables
- Rotate credentials associated with an exposed or compromised gateway

### Scope and protect provider credentials
- Apply least privilege to gateway and database access: run the proxy under a dedicated service account, limit PostgreSQL permissions to required objects, place the database behind a private endpoint with restrictive firewall rules
- Constrain outbound traffic: deny-by-default egress rules, allowlist only required model-provider and service endpoints, block direct connections to raw-IP hosts and non-standard ports

### Monitor AI workloads by control-plane role
- Correlate unexpected application-origin shells or interpreters with secret access, application-file modification, Docker socket use, outbound callbacks, and resource-hijacking activity
- High-value detections: gateway process spawning shells/downloaders/interpreters; `/proc/1/environ` access; LiteLLM-specific secret/table discovery; Python-based database credential discovery; Docker socket access to container env arrays
- Treat these signals as a connected compromise path to expose attacks earlier than product-specific indicators alone

### Harden the host runtime
- Mount temporary directories as non-executable where operationally feasible
- Alert on execution from world-writable paths
- Monitor changes to cron entries, SSH `authorized_keys` files, and immutable-file attributes
- Enable endpoint protections on Linux for files written to disk, newly observed droppers, miners, and second-stage payloads

## Reported indicators

### Network
| IOC | Type | Role |
|-----|------|------|
| `45.150.109[.]151` | IPv4 | Scanning/recon — multiple targeted AI workloads |
| `135.125.10[.]56:19888` | IPv4:port | RAGFlow exploitation C2 — LLM API key exfiltration endpoint |
| `172.232.38[.]92:32991` | IPv4:port | Kestra reverse shell C2 (Linode VPS) |
| `45.150.109.151.sslip[.]io` | Domain | DNS rebinding used in LiteLLM attacks to evade domain reputation checks |
| `auto.c3pool[.]org:443` | Domain:port | XMRig Monero mining pool (Kestra) |
| `2001:41d0:701:1100::adfd` | IPv6 | c3pool mining endpoint (Kestra) |
| `47.86.197[.]116` | IPv4 | c3pool mining endpoint (Kestra) |
| `yosemite[.]jp` | Domain | C2/exfiltration — LiteLLM credential harvesting (OAST + recv.php) |
| `gobygo[.]net` | Domain | C2 beacon infrastructure — subdomain-encoded LiteLLM beacons |
| `oast[.]me` / `oast[.]pro` / `oast[.]fun` | Domains | OOB callback domains — execution confirmation and credential exfiltration (LiteLLM) |
| `194.213.18[.]133` | IPv4 | Attacker-controlled mail MX / mail infrastructure |

### File
| File / Path | SHA-256 | Notes |
|-------------|---------|-------|
| `/tmp/d` (ELF binary) | `f64b88e9318bdf23f2dd119a0ce1dd1bdb3c8cd2e0e1e23ba3ef2e19072b79cc` | LiteLLM stage-2 — unknown ELF |
| XMRig cryptominer | `49fdcf32bfe837899a84e8938f0d07ae96ddd218a280a09eb60df8d64597bd8f` | LiteLLM |
| XMRig cryptominer (variant) | `3af9f25a4d45bb4f1ec5627cdbc6703cf3b4be75a892162d299d80ddfb266f42` | LiteLLM variant |
| Installer / bridge script | `3d24ac736635e0fa0c5c459c9e18ca09d1ec9a1751a4503130934395609bd7e0` | LiteLLM — drops `/tmp/python3` and launches supervisord bridge |

### Process / behavioral
- Gateway process (`litellm`, `litellm-proxy`, `litellm_proxy`, `ragflow`, `kestra`) spawning `bash`, `sh`, `dash`, `curl`, `wget`, `python`, `python3`
- Command-line references to `/proc/1/environ`, `database_url`, `psycopg2`, `urllib.request`, `urlretrieve`, `base64`
- `modprobe msr allow_writes`
- `exec /tmp/.` with `-c /tmp/.`
- `crontab` with `grep -v`
- `chattr`
- `authorized_keys` with `>>`
- Process command lines referencing `/private/python3`, `/anonymus/bins_s`, `BRIDGE_STANDALONE`, `PORT`, `/tmp/python3` + `supervisord`
- RAGFlow: `TenantLLM.insert()` monkey-patching
- Kestra: Docker socket access to container `Config.Env` arrays; curl-pipe-shell delivery

### MITRE ATT&CK techniques
| Tactic | Technique | Observed activity |
|--------|-----------|-------------------|
| Initial Access | T1190 Exploit Public-Facing Application | Abuse of internet-exposed AI workload surfaces |
| Execution | T1059 Command and Scripting Interpreter | python3 one-liners and shell scripts from gateway process |
| Credential Access | T1552.001 Unsecured Credentials: Credentials in Files | Harvest of provider API keys from `/proc/1/environ` and LiteLLM model-config table |
| Discovery | T1057 Process Discovery / T1518 Software Discovery | pgrep sweeps for rival miners; PostgreSQL config file enumeration |
| Defense Evasion | T1036.005 Masquerading / T1564.001 Hidden Files | Payloads named after system daemons, executed from hidden `/tmp` files |
| Impact | T1496 Resource Hijacking | Cryptomining with MSR tuning and competing-miner eviction |
| Persistence | T1098.004 SSH Authorized Keys / T1053.003 Cron | Service-account SSH key and cron entries |
| Defense Evasion | T1222.002 Linux File and Directory Permissions Modification | `chattr +i` immutable flags |
| C2 | T1071.001 Application Layer Protocol / T1095 Non-Application Layer Protocol | HTTP beacons to raw-IP infrastructure, exfil to `yosemite[.]jp`, OAST callbacks |

## Related pages
- [LiteLLM compromise](litellm-compromise.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [Trivy → TeamPCP → CanisterWorm timeline](trivy-lite-llm-compromise-timeline.md)
- [TeamPCP](../actors/teampcp.md)

## Sources
- Microsoft Security Blog, "When AI infrastructure becomes the target: Securing gateways and control points" (August 26, 2026): [https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)
- CVE-2026-42271 (LiteLLM MCP command execution)
- CVE-2026-48710 (Starlette host-header validation bypass)
- CVE-2026-49869 (Kestra authentication bypass)
- CVE-2026-45312 / CVE-2026-28797 (RAGFlow Jinja2 SSTI)
- CVE-2026-24770 (RAGFlow MinerU parser path-traversal)
- CVE-2025-68700 / GHSA-8xw3-v6c2-j84j (RAGFlow Canvas CodeExec sandbox-bypass)
- CVE-2025-69286 (RAGFlow account-access weakness)
