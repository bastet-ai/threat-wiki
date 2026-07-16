# Patriot Bait AI-assisted C2 botnet

## Summary
Trend Micro / TrendAI Research reported on July 14, 2026 that a Russian-speaking solo actor tracked as **bandcampro** used Google Gemini CLI as the primary operator interface for a small command-and-control botnet. Trend analyzed more than 200 Gemini CLI session logs from March 19-April 21, 2026 and found the actor using AI to migrate C2 infrastructure, operate infected hosts, crack and mutate passwords, compromise WordPress merchants, process infostealer dumps, and plan phone-based cryptocurrency fraud.

The durable signal is not a novel malware family. It is the operational model: a low-skill actor encoded C2 deployment and troubleshooting knowledge into a small plain-text skill bundle, then let an AI coding agent write, deploy, debug, and operate disposable infrastructure in minutes.

## Tags
- ops
- operations
- AI
- Gemini CLI
- AI-assisted malware
- agentic AI
- botnet
- C2
- command and control
- PowerShell
- Cloudflare tunnels
- credential attacks
- password spraying
- WordPress
- fraud
- Russia-speaking operator
- Patriot Bait
- bandcampro

## Why this matters
- Trend says the actor completed a live C2 migration in about **six minutes** by giving high-level Russian-language intent while the AI handled architecture, code, deployment, Cloudflare tunnel configuration, and debugging.
- The C2 operation fit into **three plain-text files** totaling roughly 5 KB, including a `C2_MIGRATION_GUIDE.md` skill file. That makes the operating knowledge shareable on forums and quickly reusable by other actors.
- The actor contributed only about **11%** of the text across the month of logs; Trend attributes 89% of the text, 100% of coding / command execution, and most architecture and debugging work to the AI agent.
- Takedowns remain useful, but disposable AI-regenerated infrastructure reduces the value of one-time IOC blocks. Defenders need behavior-based detections for polling, persistence, and abnormal PowerShell execution.
- Trend observed guardrails sometimes refusing requests such as a self-spreading “agent-bomb,” but the same logs showed the actor using the AI successfully for live malicious operations and receiving workaround-style suggestions in some blocked contexts.

## Observed operation
Trend describes an existing C2 architecture where victim machines connected through Cloudflare tunnels. When firewalls and antivirus products began blocking those tunnels, the actor asked Gemini CLI to study a migration guide and deploy a new architecture.

Key timeline from the Trend report:

| Time (UTC) | Event |
| --- | --- |
| 12:42 | Actor instructed the AI to “study the C2 migration.” |
| 12:48 | AI had the server running, tunnels configured, and new C2 operational. |
| 14:20 | Actor returned; AI reported no bots connected. |
| 15:12 | AI diagnosed a split-brain issue where traffic was load-balanced across old and new C2 servers and told the actor to shut down the old server. |
| 15:22 | Actor shut down the old C2; AI confirmed all bots reconnected. |

Trend reported that the botnet controlled eight computers in a dental clinic and accessed their OpenDental database. Day-to-day operation also flowed through the AI: the actor did not type directly into a C2 console, but issued natural-language prompts that the AI translated into C2 actions.

## C2 and payload behavior
The C2 implementation was intentionally simple and disposable:

| Component | Behavior |
| --- | --- |
| C2 server | Single Python HTTP server with in-memory state and no disk writes. |
| API camouflage | `/api/v1` paths, likely to resemble OpenAI-compatible traffic. |
| Victim polling | PowerShell beacon polls every five seconds. |
| Tasking | Actor queues Base64-encoded PowerShell commands that victims pull from the server. |
| Telemetry | Victims POST Base64-encoded command output back to C2. |
| Staging | Stager downloads `agent_final.ps1` from `payloads.tralalarkefe[.]com` and saves it under `%TEMP%` with a `win_update_svc_<random>.ps1` pattern. |

Reported API paths:

| Path | Purpose |
| --- | --- |
| `GET /api/v1/update` | Victim polls for next command; returns no-op status or a Base64 task. |
| `POST /api/v1/telemetry` | Victim uploads command output. |
| `GET /api/v1/agents` | Lists registered agents with hostname, IP, last-seen time, and queue depth. |
| `POST /api/v1/interact` | Operator pushes a command to one agent or broadcasts to `ALL`. |

## Persistence and host indicators
Trend lists these behavior-level indicators from the source code. Treat literal names as mutable because the actor can ask AI to regenerate them; the persistence shapes are more durable.

| Area | Pivot |
| --- | --- |
| Polling | Fixed five-second HTTP GET polling to `/api/v1/update`. |
| Headers | Non-standard HTTP header carrying computer name and username. |
| User-Agent | Browser-style User-Agent string sent from a PowerShell script. |
| Staging | PowerShell downloads `.ps1` to `%TEMP%\win_update_svc_*`. |
| Masquerading | `powershell.exe` copied to `%APPDATA%\Microsoft\Windows\Runtime\svchost.exe`. |
| WMI | WMI filter on `Win32_PerfFormattedData_PerfOS_System`. |
| Scheduled task | Startup / logon task disguised as `OneDrive Standalone Update Task-S-1-5-21-<random>`. |
| Logon script | `HKCU:\Environment\UserInitMprLogonScript` set to payload execution. |

The victim identification header used `X-Agent-ID: $env:COMPUTERNAME + "_" + $env:USERNAME`, and the reported hardcoded User-Agent resembled `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`.

## Broader AI-assisted activity
Beyond the C2 migration, Trend says the same session-log set showed the actor using AI to:

- set up residential proxy infrastructure;
- run multithreaded password scanning;
- mutate password guesses from AntiPublic credential data;
- target WordPress admin panels, including merchant sites;
- process infostealer dumps and reason about VPN / Duo / internal admin access;
- write code around third-party APIs;
- conduct website reconnaissance; and
- plan phone-based cryptocurrency fraud against elderly people in the US and Canada.

## Defender guidance
1. Hunt by behavior, not just static IOCs: PowerShell polling loops, non-standard HTTP headers with host/user identity, short-interval outbound GETs, and Base64 command tasking are harder for the actor to remove than a specific filename.
2. Alert on `powershell.exe` copied or executed from user-profile masquerade paths such as `%APPDATA%\Microsoft\Windows\Runtime\svchost.exe`.
3. Review WMI event subscriptions and logon/startup scheduled tasks created near suspicious PowerShell downloads, especially OneDrive-update-themed task names.
4. Treat Cloudflare tunnel changes, small Python HTTP C2 servers, and `/api/v1` beacon paths from unusual VPS or workstation contexts as suspicious when paired with PowerShell agents.
5. Harden credentials against AI-assisted mutation: enforce unique passwords, phishing-resistant MFA, password reuse monitoring, and rapid revocation for exposed infostealer dumps.
6. After C2 takedown, continue monitoring for regenerated infrastructure. The skill-file model lets the actor rebuild quickly on a new VPS with altered filenames, paths, and API routes.
7. In AI-governance programs, monitor for coding-agent use that creates C2-like infrastructure, automates credential attacks, or ingests breach datasets; keep audit logs for prompt, tool, and shell execution chains.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [SHADOW-AETHER AI-augmented Latin America intrusions](shadow-aether-ai-augmented-latam-intrusions.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [PraisonAI CVE-2026-44338 rapid exploitation](praisonai-cve-2026-44338-rapid-exploitation.md)

## Sources
- Trend Micro / TrendAI Research: [https://www.trendmicro.com/en_us/research/26/g/actor-behind-patriot-bait-used-ai-to-deploy-c2-botnet.html](https://www.trendmicro.com/en_us/research/26/g/actor-behind-patriot-bait-used-ai-to-deploy-c2-botnet.html)
