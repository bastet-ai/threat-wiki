# SHADOW-AETHER AI-augmented Latin America intrusions

## Summary
Trend Micro's TrendAI Research tracks two likely distinct Latin America intrusion campaigns, **SHADOW-AETHER-040** and **SHADOW-AETHER-064**, that used agentic AI during hands-on intrusion activity against government and financial-sector targets. Trend says both campaigns established tunnels into victim environments so AI-assisted command-line workflows could operate through ProxyChains and SSH, dynamically generate tools and scripts, mine configuration files for credentials, and support lateral movement and data exfiltration.

The durable defender value is not the vendor label alone: these cases show agentic AI becoming an operator workbench inside already-compromised environments, where it can read local context, generate one-off scripts, and accelerate misuse of weak segmentation, exposed credentials, vulnerable middleware, and permissive administrative policy.

## Tags
- ops
- operations
- SHADOW-AETHER-040
- SHADOW-AETHER-064
- Trend Micro
- TrendAI
- agentic AI
- AI-augmented operations
- Latin America
- Mexico
- Brazil
- government targeting
- financial sector
- ProxyChains
- SSH
- Chisel
- Neo-reGeorg
- CrackMapExec
- Impacket
- SOCKS5 tunneling
- data exfiltration

## Why this matters
- Trend says SHADOW-AETHER-040 compromised six Mexican government entities between 2025-12-27 and 2026-01-04, with activity spanning initial access, lateral movement, and targeted data theft.
- Trend separately observed SHADOW-AETHER-064 targeting Brazilian financial organizations in April 2026, with a primary objective of financial-data exfiltration.
- Both clusters used similar tunnel-first workflows: web shells or backdoors gave access to victim servers, then Chisel / SOCKS5 / ProxyChains / SSH let AI-assisted tooling operate deeper in the internal network.
- The campaigns generated commands, scripts, exploit helpers, scanners, and custom tunneling/backdoor components during operations instead of relying only on static tooling that defenders can signature.
- Trend assesses the two campaigns are likely separate despite tooling overlap: SHADOW-AETHER-040 artifacts were Spanish-language, while SHADOW-AETHER-064 artifacts were Portuguese-language.
- Strong fundamentals still mattered. Trend reports some AI-assisted attempts failed when environments did not expose an exploitable lateral-movement path.

## Operational characteristics
- **Actor labels:** Trend tracks the campaigns as SHADOW-AETHER-040 and SHADOW-AETHER-064. Treat them as campaign / cluster labels, not established public actor identities.
- **Targeting:** government, financial, aviation, and retail organizations in Latin America for SHADOW-AETHER-040; Brazilian financial organizations for SHADOW-AETHER-064.
- **AI workflow:** SHADOW-AETHER-040 used an agentic CLI tool connected to Anthropic Claude; Trend could not identify the LLM service used by SHADOW-AETHER-064.
- **Exposure discovery:** SHADOW-AETHER-040 connected the agent to services such as Shodan and VulDB for attack-surface and vulnerability context.
- **Initial access / footholds:** Trend describes vulnerability scanning, web-shell deployment such as Neo-reGeorg, vulnerable JBoss AS compromise for SHADOW-AETHER-064, and tunnel deployment through compromised servers.
- **Tunneling:** both campaigns used SOCKS5-style traffic forwarding, ProxyChains, and SSH to let AI-assisted operations reach internal systems; Chisel appeared in both toolsets.
- **Knowledge base:** SHADOW-AETHER-040 instructed the AI agent to maintain victim-specific Markdown notes, allowing the workflow to resume context from prior actions.
- **Jailbreak framing:** SHADOW-AETHER-040 tried to persuade the AI system that the activity was an authorized red-team exercise; Trend says explicit government-target prompts often triggered refusals, but repeated reframing eventually bypassed safeguards.
- **Credential access:** observed tasks included searching shell history, application archives, configuration files, private-key paths such as `id_*` / `*.pem` / `*_rsa` / `*_dsa` / `*_ecdsa` / `*_ed25519`, and databases for embedded credentials or sensitive records.
- **Lateral movement:** generated scanning and exploitation scripts, password spraying, CrackMapExec / Impacket, PetitPotam SMB relay, Pass-the-Hash over SMB, stolen SSH credentials, and SSH key insertion into `~/.ssh/authorized_keys` appeared in the reporting.
- **Persistence / privilege actions:** examples included Chisel persistence under names such as `pg_stat_worker` in `~/.pgsql/logs/`, cron jobs, `.bashrc` changes, attempts to use Dirty COW and PwnKit, privileged cron-job abuse, service-account creation such as `svcbackup` / `svcmon`, and Group Policy changes.
- **Custom tooling:** SHADOW-AETHER-040 deployed `implante_http`, a Python backdoor packaged with PyInstaller for ELF and Windows contexts, with HTTP C2, WebSocket tunneling, command execution, file transfer, interactive PTY, SSH bridging, TCP / UDP forwarding, and chunked large-file exfiltration.
- **SHADOW-AETHER-064 tools:** Trend describes `POW` / Proxy over Web for SOCKS5-over-HTTP through JSP web shells and `SOCKTZ`, a Go reverse SOCKS5 tool that evolved through multiple versions and later gained remote command execution.
- **Infrastructure indicators:** Trend published hunt examples involving IPs `165.22.184.26`, `159.65.202.204`, `62.171.185.97`, `167.172.38.123`, `155.133.27.198`, `209.99.185.221`, `209.99.185.223`, `167.148.195.53`, and SHADOW-AETHER-064 domains `cloudservbr.com` and `infra-telemetry.com`. Validate against the primary source before blocking or alerting on static indicators alone.

## Defender heuristics
- Treat unexpected AI-agent or model-provider traffic from servers, bastions, CI runners, and admin workstations as suspicious when it co-occurs with scanning, credential discovery, shell-history access, or internal SSH/SMB activity.
- Hunt for tunnel chaining rather than only named tools: web shell or application-server process spawning Chisel, SSH, ProxyChains, Go binaries, Python C2 controllers, or unusual outbound connections from middleware hosts.
- Preserve command histories and working directories during response; victim-specific Markdown notes, generated scripts, and AI-style comments can explain operator intent and downstream targets.
- Search Linux hosts for suspicious persistence and staging paths such as `~/.pgsql/logs/pg_stat_worker`, unexpected `.bashrc` launch lines, new cron jobs, unauthorized `authorized_keys` entries, and recent private-key discovery commands.
- On Windows / AD, review recent service-account creation, GPO / GPP modifications, Domain Admin policy changes, SMB Pass-the-Hash evidence, and administrative-group membership changes tied to names like `svcbackup` or `svcmon`.
- Put extra scrutiny on JBoss and other internet-facing middleware that can bridge to internal networks; an AI-assisted operator still needs reachable vulnerabilities, credentials, or misconfigurations.
- Build detections for agent-friendly command generation: rapid sequences of internal scans, config-file reads, exploit-script creation, SQL enumeration, and file-compression / SCP exfiltration launched from a single tunnel or shell session.
- Do not overfit on AI-generated code style. Use generated-looking comments, emoji, or self-reasoning strings as triage signals only when paired with behavior such as tunneling, credential access, and lateral movement.
- Limit blast radius with fundamentals Trend highlighted: timely patching, segmentation around application servers, least-privilege service accounts, private-key hygiene, MFA / device posture on remote admin paths, and high-fidelity monitoring of internal activity.

## Related pages
- [Unit 42 CL-CRI-1131/CL-CRI-1163 LLM-orchestrated LATAM campaigns (Sep 3, 2026)](unit42-clcri-1131-1163-llm-orchestrated-latam-campaigns-september-2026.md) — Unit 42's corroborating Sep 3 reporting: the same SockTz / `167.148.195[.]53` JBoss infrastructure and LLM-tell iterative filenames, plus an internet-exposed NextChat backend in CL-CRI-1131
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)
- [Cloud logging control-plane tampering](../patterns/cloud-logging-control-plane-tampering.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)

## Sources
- Trend Micro: [https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html](https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html)
