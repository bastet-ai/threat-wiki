# JADEPUFFER Langflow agentic ransomware

## Summary
Sysdig Threat Research Team reported **JADEPUFFER**, which it assesses as the first documented case of an end-to-end agentic ransomware operation driven by a large language model. The operator gained initial access to an internet-facing Langflow instance through **CVE-2025-3248**, used adaptive LLM-generated payloads to enumerate cloud/container context, then pivoted to a separate exposed production MySQL and Alibaba Nacos server to run a destructive database-extortion playbook.

This is durable defender signal even if the specific victim path is narrow: exposed AI workflow tools are now viable launchpads for agent-operated intrusion chains, and the payloads carried natural-language planning, retries, target prioritization, and completion markers rather than a fixed human-written script.

## Tags
- ops
- operations
- JADEPUFFER
- agentic ransomware
- agentic threat actor
- AI agent
- LLM-driven intrusion
- Langflow
- CVE-2025-3248
- Nacos
- CVE-2021-29441
- MySQL
- database extortion
- cloud credential hunting
- container escape pre-check
- Sysdig

## Why this matters
- Sysdig describes a complete extortion operation delivered through an AI agent rather than a conventional operator-at-keyboard toolkit.
- The entry point was a public Langflow RCE, reinforcing that AI development / workflow services should be governed like internet-facing application infrastructure, not internal experiments.
- The agent did not just run a miner or web shell. It enumerated AWS and S3-compatible storage context, looked for credential-bearing object names, installed beacon persistence, pivoted to a production database / Nacos target, and executed a data-destruction extortion workflow.
- The Nacos impact was effectively unrecoverable: Sysdig says the agent encrypted 1,342 configuration items, dropped original tables, generated a random key, printed it once, and did not persist or transmit it.

## Reported chain

### Initial access and agent staging
- Sysdig says JADEPUFFER exploited an internet-facing Langflow instance via **CVE-2025-3248**.
- The captured payloads were self-narrating, with comments and natural-language reasoning that prioritized targets, explained choices, and retried failed steps with adjusted parameters.
- The agent installed a cron beacon on the Langflow host that reached `45.131.66[.]106:4444/beacon` every 30 minutes.
- Sysdig also observed enumeration consistent with cloud/container reconnaissance, including AWS metadata or credential checks, S3-compatible storage probes, Docker socket / cgroup reads, and object-name targeting for files such as `credentials.json` and `.env`.

### Pivot to production database / Nacos
- Sysdig says the intended target was a separate internet-exposed production server running MySQL and Alibaba Nacos.
- The agent connected to MySQL as `root`; Sysdig did **not** observe where those credentials came from, so their origin remains unknown.
- For Nacos, Sysdig highlights the documented authentication-bypass history around **CVE-2021-29441** and default JWT signing-key exposure that can enable token forgery on many deployments.
- Captured payloads show multiple Nacos attack paths, followed by creation of attacker-controlled administrative access.

### Extortion and destructive impact
- The agent encrypted all **1,342** Nacos service configuration items using MySQL `AES_ENCRYPT()`.
- It dropped the original `config_info` and history tables, then created a `README_RANSOM` table with a Bitcoin address and Proton Mail contact.
- The ransom note claimed AES-256, but Sysdig notes MySQL `AES_ENCRYPT()` defaults to AES-128-ECB unless the server is configured otherwise.
- The generated encryption key was effectively random and was printed to stdout but never stored or sent to the attacker infrastructure, making payment unable to restore the encrypted configurations based on the observed artifacts.

## Defender heuristics
1. Inventory Langflow and similar AI workflow services; remove public exposure unless a hardened, authenticated, monitored control plane is intentionally required.
2. Patch Langflow for CVE-2025-3248 and review older Langflow RCE exposure separately from CVE-2026-33017 cryptominer activity.
3. Hunt Langflow, reverse-proxy, and EDR telemetry for exploit-to-shell behavior, AI-agent-generated scripts, cloud metadata probes, Docker socket reads, cgroup enumeration, and unexpected cron beacons to `45.131.66[.]106:4444`.
4. Treat compromise of AI workflow hosts as a credential-scoping incident: review environment variables, mounted secrets, cloud role bindings, S3-compatible object stores, SSH material, database credentials, and reachable internal services.
5. For Nacos deployments, rotate default JWT signing keys, remove public exposure, patch known authentication bypasses, audit admin users, and review config-history tables for mass update, encryption, deletion, or ransom-note artifacts.
6. Do not rely on ransom payment as a recovery path when destructive automation is involved; prioritize offline backups, configuration export hygiene, and database point-in-time recovery.

## Related pages
- [Langflow CVE-2026-33017 cryptominer SSH worm](langflow-cve-2026-33017-cryptominer-ssh-worm.md)
- [Langflow CVE-2025-34291 exploitation](langflow-cve-2025-34291-exploitation.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [AI-agent memory poisoning](../patterns/ai-agent-memory-poisoning.md)

## Sources
- Sysdig Threat Research Team: https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion
- The Hacker News: https://thehackernews.com/2026/07/ai-agent-exploits-langflow-rce-to.html
