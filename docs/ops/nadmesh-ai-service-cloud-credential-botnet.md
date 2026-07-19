# NadMesh AI-service and cloud-credential botnet

## Summary
QiAnXin XLab reported **NadMesh**, a Go botnet observed spreading at scale in early July 2026. Its autonomous scan-and-exploit loop gives highest priority to exposed ComfyUI, Ollama, n8n, Open WebUI, Langflow, and Gradio services, while also targeting MCP, Docker, Kubernetes, Redis, Jenkins, databases, and weak remote-access credentials.

The durable risk is broader than cryptomining or host takeover: NadMesh harvests AWS configuration and keys, Kubernetes service-account tokens, Docker registry configuration, environment files, model inventories, and callable MCP tools. It combines that collection with three-way persistence, polymorphic builds, canary deployment, rescan prioritization, and honeypot avoidance.

## Tags
- ops
- operations
- NadMesh
- botnet
- Go malware
- AI services
- MCP
- Model Context Protocol
- cloud credential theft
- Kubernetes
- Docker
- Redis
- Jenkins
- ComfyUI
- Ollama
- n8n
- Open WebUI
- Langflow
- Gradio
- Shodan
- credential theft
- SSH backdoor
- cron persistence
- Garble
- UPX
- autonomous scanning
- QiAnXin XLab

## Autonomous attack loop
1. `ai_harvest.py` uses Shodan to collect exposed AI-service assets and injects them into the scan queue at priority 20.
2. Go or Python controllers on ports 80 and 8443 register bots, dispatch CIDR/port tasks, collect findings and credentials, and expose an operator panel.
3. `yield_generator.py`, `auto_inject.sh`, `reinject.sh`, and `auto_blacklist.sh` amplify productive ranges, rescan recent targets, and suppress likely honeypots.
4. `build_agent.sh` applies Garble symbol/literal obfuscation, UPX `-9` packing, signature stripping, and random padding so builds do not share a stable hash.
5. `vps_deployer.py` and `push_deployer.py` deliver agents and watchdogs through exposed services and weak credentials.

XLab observed more than 20 exploit or misconfiguration vectors. Docker containers API RCE and Jenkins script-console execution made up the largest reported shares of observed attempts, while the bot also tested unauthenticated Redis, weak Telnet/SSH, Kubernetes surfaces, MCP command tools, and vulnerabilities including Marimo CVE-2026-39987 and rclone CVE-2026-41176.

## Collection and persistence
NadMesh searches environment variables and files including `~/.aws/config`, `.env`, and `~/.docker/config.json`; it also collects Kubernetes service-account tokens, cloud credentials, AI model inventories, and MCP tool information. Operator-panel totals are attacker-controlled and internally inconsistent, so claims such as 3,811 unique AWS keys or 17,700 deployments should be treated as unverified scale indicators, not confirmed victim counts.

Persistence is deliberately redundant:
- an attacker SSH key appended to `.ssh/authorized_keys`;
- agent copies at `/dev/shm/.a`, `/var/tmp/.a`, and `/tmp/.a`;
- cron watchdogs at `/etc/cron.d/.sys_monitor` and `/etc/cron.d/.s`.

Removing only one artifact can allow the others to restore the implant. Hash-only detection is also weak because each build receives random padding after obfuscation and packing.

## Exposure and detection pivots
NadMesh probes a 30-port set covering web applications, Kubernetes, databases, Docker, Redis, Elasticsearch, and AI services. High-priority AI ports include:

| Port | Common service |
| --- | --- |
| 8188 | ComfyUI |
| 11434 | Ollama |
| 7860 | Gradio |
| 5678 | n8n |

Other notable surfaces include Docker API ports 2375/2376, Kubernetes API 6443, kubelet 10250, etcd 2379, Redis 6379, Elasticsearch 9200, PostgreSQL 5432, MySQL 3306, and common web/admin ports.

Behavioral pivots include:
- creation or execution of `.a` from `/dev/shm`, `/var/tmp`, or `/tmp`;
- hidden dot-file cron entries that retrieve or restart an agent;
- unauthorized SSH-key additions followed by periodic Go binary execution;
- high-rate 30-port internet or LAN scanning from an AI, CI, notebook, or container host;
- requests to MCP JSON-RPC `tools/call` for an `execute_command` tool;
- reads of cloud, Kubernetes, Docker, and `.env` credentials by an unrelated packed Go process;
- open controller paths such as `/api/register`, `/api/beacon`, `/api/agent/binary`, `/api/agent/loader`, `/api/endpoints`, and static-looking `/cdn/<token>/assets/img.bin`.

## Defender guidance
- Remove AI inference, workflow, notebook, MCP, Docker, Kubernetes, Redis, and Jenkins administration surfaces from the public internet. Require strong authentication and network allow-listing; do not expose Docker TCP/2375 or command-capable MCP tools anonymously.
- Inventory internet-facing ports 8188, 11434, 7860, and 5678 first, then the broader container, orchestration, database, and administration set. Patch Marimo before 0.23.0 and rclone RC versions 1.45.0 through 1.73.5 where exposed without HTTP authentication.
- Hunt all three persistence layers before replacement credentials are issued. Isolate affected hosts, preserve cron files, keys, binaries, shell history, process memory, and controller traffic, then remove the implant from a trusted environment.
- Revoke—not merely rotate in place—AWS keys, Kubernetes tokens, Docker registry credentials, `.env` secrets, model-provider keys, MCP credentials, and other secrets readable by the compromised process. Review cloud audit logs and Kubernetes API activity for downstream use.
- Prefer behavioral detections over sample hashes: watch for packed/obfuscated Go processes combining scanning, credential-file access, SSH-key modification, cron creation, and outbound controller beacons.

## Related pages
- [Langflow CVE-2026-33017 cryptominer / SSH worm](langflow-cve-2026-33017-cryptominer-ssh-worm.md)
- [TuxBot v3 Evolution IoT botnet](tuxbot-v3-evolution-iot-botnet.md)
- [LiteLLM CVE-2026-42271 MCP stdio command injection](litellm-cve-2026-42271-mcp-stdio-command-injection.md)
- [Agent localhost control-plane RCE](../patterns/agent-localhost-control-plane-rce.md)

## Sources
- QiAnXin XLab: <https://blog.xlab.qianxin.com/nadmesh-botnet-analysis-a-product-grade-threat-for-the-ai-service-era-en/>
- Censys: <https://censys.com/blog/mcp-servers-on-the-internet/>
