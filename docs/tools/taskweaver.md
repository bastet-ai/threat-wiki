# TaskWeaver

## Summary
**TaskWeaver** is a heavily obfuscated Node.js loader reported by Blackpoint Cyber and summarized publicly by The Hacker News on June 30, 2026. Blackpoint observed TaskWeaver after exploitation of SimpleHelp CVE-2026-48558, where an attacker used a forged SimpleHelp technician session to transfer and execute malware through the trusted RMM channel.

In the reported chain, TaskWeaver was delivered as `jquery.js`, executed through `node.exe`, fingerprinted the host, established encrypted communications with attacker infrastructure, and retrieved additional JavaScript payloads. The observed second stage was [Djinn Stealer](djinn-stealer.md), a cross-platform credential and developer-secret stealer.

## Tags
- tools
- malware
- loader
- Node.js
- JavaScript
- SimpleHelp
- CVE-2026-48558
- RMM abuse
- post-exploitation
- encrypted C2
- payload loader
- TaskWeaver
- Djinn Stealer
- Blackpoint Cyber

## Why this matters
- RMM exploitation converts a remote-support server into a trusted administrative deployment channel; the malware may arrive from an expected management path rather than phishing or ordinary download telemetry.
- Node.js-based payload staging blends into developer and admin workstations where Node runtimes are common.
- TaskWeaver's role is reusable payload delivery, so defenders should not scope triage only to the observed Djinn Stealer payload.
- The chain targets developer, cloud, AI-assistant, and infrastructure credentials after initial endpoint access, turning endpoint compromise into source-code, CI/CD, cloud, and customer-environment risk.

## Reported execution chain
1. An attacker exploits SimpleHelp CVE-2026-48558 against an OIDC-enabled SimpleHelp server to obtain an authenticated technician session.
2. The attacker uses SimpleHelp's remote-support capabilities to transfer files and execute commands on systems managed through the server.
3. TaskWeaver is delivered as `jquery.js` and run with `node.exe`.
4. TaskWeaver fingerprints the host, establishes encrypted communications with `a.dev-tunnels[.]com`, and retrieves/executes additional JavaScript payloads with access to the Node.js runtime.
5. The observed second-stage payload, Djinn Stealer, collects broad credential and secret material, packages it, encrypts it, and exfiltrates it to attacker-controlled infrastructure.

## Network and artifact pivots
- Filename reported for the loader: `jquery.js`.
- Runtime: `node.exe` / Node.js.
- C2 / staging host reported by The Hacker News from Blackpoint's analysis: `a.dev-tunnels[.]com`.
- Observed follow-on exfiltration endpoint in the same intrusion chain: `96.126.130[.]126:58942`.

## Defender heuristics
- On SimpleHelp-managed hosts, hunt for file transfer and command-execution events that created or ran `jquery.js`, `node.exe`, or unexpected JavaScript from technician sessions.
- Correlate SimpleHelp technician-session creation with IdP/OIDC events. Treat technician sessions without matching IdP-signed authentication telemetry as suspect.
- Alert on Node.js execution launched by RMM agents, remote-support services, unusual service accounts, or recently created technician sessions.
- Review outbound connections to `a.dev-tunnels[.]com` and `96.126.130[.]126:58942`; include historical DNS/proxy logs for developer and admin workstations.
- Scope response beyond the endpoint: rotate cloud, source-control, package-registry, AI-assistant, SSH, Docker, IaC, and wallet credentials accessible to the affected user or machine.
- Preserve RMM logs, process telemetry, command lines, file-transfer records, JavaScript payloads, memory where feasible, and network captures before cleanup.

## Related pages
- [Djinn Stealer](djinn-stealer.md)
- [SimpleHelp CVE-2026-48558 authentication-bypass exploitation](../ops/simplehelp-cve-2026-48558-authentication-bypass-exploitation.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)

## Sources
- The Hacker News: https://thehackernews.com/2026/06/attackers-exploit-simplehelp-cve-2026.html
- Blackpoint Cyber: https://blackpointcyber.com/blog/a-djinn-in-the-machine-taskweavers-node-js-intrusion-chain/
- Horizon3.ai: https://horizon3.ai/attack-research/disclosures/cve-2026-48558-simplehelp-authentication-bypass-iocs/
