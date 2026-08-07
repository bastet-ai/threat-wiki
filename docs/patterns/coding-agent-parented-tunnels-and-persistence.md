# Coding-agent-parented tunnels and persistence

## Summary
Elastic Security Labs documented a July 2026 macOS investigation in which shells under Claude Code ancestry authenticated to an application exposed through ephemeral tunnel hosts, queried application metrics, created a Cloudflare Quick Tunnel, and installed user LaunchAgents that kept tunnel access alive. Related cases included JavaScript staging through Apple-signed interpreters, an endpoint-blocked attempt to filter a decrypted keychain dump for Linear and MCP OAuth material, and an unsigned binary fetched over plaintext HTTP followed by quarantine removal, ad-hoc signing, and shell-profile probing.

The report does **not** establish that the main sequence was malware or a confirmed intrusion. Elastic says the same telemetry can fit developer-assisted remote administration of a local dashboard. The durable defender pattern is therefore outcome-based: a trusted coding-agent parent does not make credential access, public tunneling, persistence, unsigned payload retrieval, or security-control bypass benign.

## Tags
- patterns
- AI coding agents
- Claude Code
- Cursor
- macOS
- reverse tunnels
- Cloudflare Tunnel
- localhost.run
- ngrok
- LaunchAgent
- credential exposure
- keychain theft
- developer endpoints
- dual-use tooling
- detection engineering

## Observed sequence
Elastic reconstructed a multi-day window on a macOS developer endpoint:

1. Tunnel- and VPN-class binaries appeared before the central agent session, alongside increasing coding-agent child-process volume.
2. A shell-launched Python script under `/tmp` made an outbound MCP-style analytics request, and a separate process touched Claude project memory under `~/.claude/projects/*/memory/MEMORY.md`.
3. Claude Code sessions used `--allow-dangerously-skip-permissions`, reducing interactive approval friction for later tool calls.
4. Shells under the agent polled `/login` on ephemeral tunnel URLs, posted credentials, and queried API summaries such as spending metrics.
5. A Cloudflare Quick Tunnel published a loopback service without requiring an inbound firewall rule. An ngrok binary appeared in the same day's telemetry.
6. User LaunchAgents in a shared application-naming family kept the service, tunnel, and watchdog alive across logout or reboot; a watchdog checked the public `/login` URL on an interval.
7. Process-discovery commands checked related workloads while the access path was being assembled.

The immediate parent of many actions was `zsh`, not the coding-agent binary itself. Analysts need full ancestry rather than a direct-child-only query.

## High-signal correlations
No single item below proves malicious use. Escalate when several outcomes occur in one agent session or endpoint window:

- Claude Code, Cursor, or another coding agent starts shells that contact `*.lhr[.]life`, `*.trycloudflare[.]com`, ngrok infrastructure, or another public tunnel broker.
- A loopback service is published and then exercised through its public URL, especially when `/login` polling and credential-bearing command lines follow.
- The same lineage creates or loads `~/Library/LaunchAgents/*.plist` entries with `KeepAlive`, short `StartInterval` values, tunnel binaries, public-URL liveness checks, or user-writable executable paths.
- Permission-bypass modes precede credential access, tunnel creation, persistence, unsigned downloads, quarantine stripping, ad-hoc signing, or shell-profile modification.
- Temporary Python, JavaScript, or shell files under `/tmp` combine network access with agent-memory or MCP-related activity.
- Keychain commands, decrypted keychain databases, or filtered output target coding-agent, Linear, MCP, OAuth, browser, package-registry, or cloud credentials.
- `cloudflared`, ngrok, SSH reverse tunnels, and LaunchAgents appear together rather than as an isolated approved tool installation.

Broker apex reputation and rare-domain alerts are useful pivots, but they are not verdicts. Free tunnel services are legitimate and attacker-abused; ephemeral subdomains also rotate too quickly to serve as durable standalone indicators.

## Defender guidance
- Preserve process ancestry, arguments, signing and quarantine metadata, file writes, LaunchAgent contents, network events, and agent audit/session logs. Do not suppress shell activity merely because a signed coding agent is an ancestor.
- Alert on outcomes beneath agent parents: credential-store reads, secrets in command lines, public tunneling of loopback services, persistence creation, unsigned downloads, and security-control bypass.
- Inventory approved tunnel tools, accounts, destinations, local ports, and persistence requirements. Block or require approval for public tunnel brokers where developer workflows do not need them.
- Prohibit unattended permission-bypass modes on production-connected developer endpoints. If an exception is necessary, use a secretless sandbox with restricted egress and no ambient browser, keychain, cloud, source-control, or package-registry sessions.
- Detect new or modified user LaunchAgents and correlate them with recent agent sessions and tunnel execution. Review `RunAtLoad`, `KeepAlive`, `StartInterval`, liveness loops, and programs in `/tmp` or other user-writable paths.
- Treat credentials embedded in `curl` arguments or scripts as exposed even when transport uses HTTPS: process arguments, shell history, endpoint telemetry, and agent transcripts may retain them. Rotate secrets if exposure cannot be ruled out.
- During triage, document both plausible readings. Confirm who initiated the session, what local service was exposed, whether the public URL was authorized, who accessed it, and whether persistence was expected before labeling the activity malicious.

## ATT&CK mapping
- **T1059.004** — Unix Shell
- **T1090** — Proxy
- **T1105** — Ingress Tool Transfer
- **T1543.001** — Launch Agent
- **T1555.001** — Keychain
- **T1057** — Process Discovery

## Related pages
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [AI coding-agent symlink write confusion](ai-coding-agent-symlink-write-confusion.md)
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [macOS.Gaslight Rust backdoor](../ops/macos-gaslight-rust-backdoor.md)

## Sources
- Elastic Security Labs, “Living off the coding agent: Two tales of tunnels and LaunchAgents,” 2026-08-07: [https://www.elastic.co/security-labs/coding-agent-launchagent-tunnel-detection](https://www.elastic.co/security-labs/coding-agent-launchagent-tunnel-detection)
