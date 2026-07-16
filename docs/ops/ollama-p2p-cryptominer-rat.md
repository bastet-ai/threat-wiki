# Ollama P2P cryptominer RAT campaign

## Summary
**Ollama P2P cryptominer RAT campaign** is a May 2026 Akamai-reported intrusion pattern targeting exposed Ollama API endpoints on port `11434`. Akamai observed attackers abusing Ollama model-creation flows to fetch and execute an installer script, then deploying a custom Go binary named `vc` that acts as a peer-to-peer remote-access Trojan, backdoor, and Monero cryptominer dropper.

The durable intelligence value is the AI-service exposure pattern: unauthenticated or weakly controlled local-AI endpoints can become command-execution surfaces, and commodity cryptomining crews are already combining LLM API abuse with RAM-disk execution, process masquerading, cron persistence, and decentralized libp2p networking.

## Tags
- ops
- operations
- Ollama
- AI tooling
- LLM
- API abuse
- cryptominer
- Monero
- XMRig
- RAT
- backdoor
- P2P
- libp2p
- Go
- Linux
- persistence
- RAM disk
- defense evasion
- command execution

## Why this matters
- Ollama is widely deployed by developers and AI experimenters, often on workstations or small servers that may also hold source code, tokens, local models, and cloud credentials.
- The campaign shows direct exploitation of AI runtime functionality rather than a traditional package-install path: malicious `Modelfile` content triggers shell execution through `/api/create` abuse.
- The payload avoids simple domain/IP blocking by routing mining traffic through a decentralized libp2p mesh using protocols such as WebRTC, QUIC, DTLS, and UPnP.
- RAM-disk staging and kernel-thread-style process names can hide the miner from casual filesystem and process review while persistence relaunches it every 15 minutes.

## Operational characteristics
- **Initial access:** HTTP requests to exposed Ollama `/api/create` on port `11434`, with malicious `Modelfile` content using `RUN` or `TEMPLATE`/`exec` to download and pipe `i.sh` into the shell.
- **Installer:** `i.sh` downloads the payload from Supabase-hosted storage using `curl`, `wget`, or Python fallback logic, writes it to `/dev/shm/.sys-update`, executes it, and avoids leaving a normal on-disk copy.
- **Primary payload:** `vc`, a custom Go 1.25.7 x86 binary with UPX packing/fake-UPX analysis friction, identified by Akamai as a P2P RAT and cryptominer dropper.
- **Masquerading:** the malware copies itself to `/dev/shm/.udev-mesh-node`, drops `/dev/shm/kworker-main` and `/dev/shm/kworker-run`, and renames the process to look like a `kworker` kernel thread.
- **Mining path:** `kworker-main` operates as a P2P networking proxy and `kworker-run` is XMRig; mining traffic is proxied locally through `127.0.0.1:41947` and routed into the P2P mesh.
- **Persistence:** Akamai reports a `hydraPersistence` function and cron entry that checks for `kworker-run` every 15 minutes and relaunches `/dev/shm/.udev-mesh-node` if needed.
- **Backdoor capability:** the binary can execute operating-system commands as the Ollama process owner, so impact depends heavily on how the Ollama service was run.

## Defender heuristics
- Do not expose Ollama APIs directly to the internet; bind local AI runtimes to localhost or authenticated internal networks, and place strong access controls in front of any required remote access.
- Review reverse proxies, firewall rules, container port mappings, and developer workstations for reachable TCP `11434` and unexpected `/api/create` traffic.
- Hunt for suspicious Ollama `Modelfile` content containing shell downloaders, `RUN curl ... | sh`, `TEMPLATE` plus `exec`, or requests that create throwaway model names such as `sys_check` and `sys_update`.
- Inspect Linux hosts for `/dev/shm/.sys-update`, `/dev/shm/.udev-mesh-node`, `/dev/shm/kworker-main`, `/dev/shm/kworker-run`, suspicious `kworker-*` userland processes, and cron entries relaunching RAM-disk binaries.
- Monitor for outbound QUIC/UDP 443, unexpected WebSocket traffic, libp2p-like peer activity, local mining proxies such as `127.0.0.1:41947`, and XMRig execution under AI-service users.
- If the payload ran, isolate the host, preserve volatile evidence first, capture process/memory artifacts where possible, then remove persistence and rotate credentials accessible to the Ollama service account.

## Selected indicators
- **Initial endpoint:** `/api/create` on Ollama TCP `11434`.
- **Installer:** `i.sh`; SHA-256 `18a60f4122d10fc342977345cc1d494784ca55285eea37dddf90c6b9829b6d4b`.
- **Payload hashes:** packed `vc` SHA-256 `424a5d4dca5fb9506e7a15abc95d9e8b2a8c91fcf340394db86e38342afe7ab9`; unpacked `vc` SHA-256 `4159fb1305a6c45f901aa0c5b8edf7192ca9f608acce445b0dc304edc040862c`.
- **Paths:** `/dev/shm/.sys-update`, `/dev/shm/.udev-mesh-node`, `/dev/shm/kworker-main`, `/dev/shm/kworker-run`.
- **Domain:** `cloud-metrics[.]io`.
- **P2P key:** `12D3KooWGfRjvTvgfV4eXnFWLV26GG7TciWX7ycBiGPnA7ubVmbG`.
- **Monero wallet:** `42qxWtESb9t1jvteBGCJybRiHB2x6fiMmhmosjUxfDsFUMLtJgYheVUaac2dvHrDfwcogpQFbTz4h2GXkB1rxonqUJQnUyz`.

## Related pages
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)
- [Langflow CVE-2025-34291 exploitation](langflow-cve-2025-34291-exploitation.md)
- [ROADtools](../tools/roadtools.md)

## Sources
- Akamai Security Research: <https://www.akamai.com/blog/security-research/stealthy-p2p-cryptominer-ollama-endpoints>
