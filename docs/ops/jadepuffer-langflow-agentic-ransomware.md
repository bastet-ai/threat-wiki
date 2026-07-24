# JADEPUFFER Langflow agentic ransomware

## Summary
Sysdig Threat Research Team reported **JADEPUFFER**, which it assesses as the first documented case of an end-to-end agentic ransomware operation driven by a large language model. The operator gained initial access to an internet-facing Langflow instance through **CVE-2025-3248**, used adaptive LLM-generated payloads to enumerate cloud/container context, then pivoted to a separate exposed production MySQL and Alibaba Nacos server to run a destructive database-extortion playbook. In a July 21 follow-up, Sysdig observed the same operator return to the Langflow host and deploy **ENCFORGE**, a compiled Go ransomware built to encrypt AI model, vector-index, and training-data formats.

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
- ENCFORGE
- Docker socket
- AI model encryption
- Sysdig

## Why this matters
- Sysdig describes a complete extortion operation delivered through an AI agent rather than a conventional operator-at-keyboard toolkit.
- The entry point was a public Langflow RCE, reinforcing that AI development / workflow services should be governed like internet-facing application infrastructure, not internal experiments.
- The agent did not just run a miner or web shell. It enumerated AWS and S3-compatible storage context, looked for credential-bearing object names, installed beacon persistence, pivoted to a production database / Nacos target, and executed a data-destruction extortion workflow.
- The Nacos impact was effectively unrecoverable: Sysdig says the agent encrypted 1,342 configuration items, dropped original tables, generated a random key, printed it once, and did not persist or transmit it.
- The follow-up operation replaced improvised encryption with ENCFORGE, a purpose-built locker covering roughly 180 extensions and using the Docker socket to cross from the compromised container to the host.

## Trend Micro July 24 analysis
Trend Micro published a synthesis of Sysdig's evidence and framed JADEPUFFER as the first reported case combining all three of these properties: an end-to-end agent-driven chain, destructive extortion impact, and a live production target. That is a useful description of the public claim, not independent victim telemetry: the underlying incident evidence still comes from Sysdig.

- The captured agent issued **more than 600 distinct purposeful payloads** during the intrusion rather than replaying one static toolchain.
- After creating a Nacos backdoor administrator with a malformed password hash, it diagnosed the failed login, removed the account, generated a valid hash, recreated the account, and confirmed access in about **31 seconds**.
- When an object-storage service returned an unexpected format, the agent rewrote its parser. When it learned that another path used a custom secret, it abandoned that path. These are durable examples of adaptive execution that defenders should model as behavior rather than as a reusable payload signature.
- The monetization path was nonfunctional: the agent failed to retain the encryption key and copied a public Bitcoin documentation example into the ransom note. Successful destructive impact therefore did not imply a viable decryption or payment workflow.
- Trend Micro cautions that `64.20.53[.]230` appeared only in a payload comment and was likely model-invented; the public example Bitcoin address is also not attacker infrastructure. Neither should be promoted as a confirmed malicious indicator.

The defender implication is narrower than “AI makes existing controls obsolete.” JADEPUFFER succeeded through a patched-in-2025 Langflow flaw, default MinIO credentials, a known Nacos authentication weakness, and an unrotated signing key. Autonomous execution compressed the sequence and made the payloads disposable, but established exposure reduction, credential rotation, process telemetry, and recoverable backups still address the durable failure modes.

## ENCFORGE follow-up
- JADEPUFFER returned to the same Langflow instance after Sysdig's first report and used the same CVE-2025-3248 entry point.
- After an in-container payload fetch failed, the operator iterated six Python scripts in five minutes and 24 seconds, ultimately creating a privileged container with host PID/network namespaces and a read-write host-root mount.
- The final script copied `lockd` through `/proc/<pid>/root`, used `nsenter` to execute it on the host, performed a `--try-run`, launched `--lock`, and counted `.locked` files to verify execution.
- The extortion contact matched the earlier operation. Sysdig disclosed one observed session and no victim count, so broader deployment remains unconfirmed.
- See the dedicated [ENCFORGE](../tools/encforge.md) page for hashes, file targeting, cryptography, and detection pivots.

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
7. Prefer behavior detections over JADEPUFFER's weak or disposable network indicators: application-server child processes decoding inline payloads, newly created fixed-interval cron beacons, forged or unexpected Nacos administrators, and bulk `AES_ENCRYPT()` activity followed by configuration-table deletion.

## Related pages
- [Langflow CVE-2026-33017 cryptominer SSH worm](langflow-cve-2026-33017-cryptominer-ssh-worm.md)
- [Langflow CVE-2025-34291 exploitation](langflow-cve-2025-34291-exploitation.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [AI-agent memory poisoning](../patterns/ai-agent-memory-poisoning.md)
- [ENCFORGE](../tools/encforge.md)

## Sources
- Sysdig Threat Research Team: [https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion](https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion)
- Sysdig Threat Research Team: [JADEPUFFER evolves: ransomware built to destroy AI models](https://www.sysdig.com/blog/jadepuffer-evolves-the-agentic-threat-actor-deploys-ransomware-built-to-destroy-ai-models)
- Trend Micro Research: [The Signs Were There: What the First Autonomous Ransomware Case Confirms](https://www.trendmicro.com/en_us/research/26/g/autonomous-ransomware.html)
- The Hacker News: [https://thehackernews.com/2026/07/ai-agent-exploits-langflow-rce-to.html](https://thehackernews.com/2026/07/ai-agent-exploits-langflow-rce-to.html)
