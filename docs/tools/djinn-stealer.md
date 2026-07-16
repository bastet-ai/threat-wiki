# Djinn Stealer

## Summary
**Djinn Stealer** is a cross-platform information stealer reported by Blackpoint Cyber and summarized publicly by The Hacker News on June 30, 2026. It was observed as the second-stage payload in a SimpleHelp CVE-2026-48558 intrusion chain where the attacker first deployed the [TaskWeaver](taskweaver.md) Node.js loader through a compromised SimpleHelp technician session.

Djinn targets Windows, macOS, and Linux systems. Its collection scope spans browser data, cloud credentials, source-control and package-registry secrets, infrastructure tooling, AI development assistants, SSH material, Docker/Helm/S3/MinIO configuration, and cryptocurrency wallets.

## Tags
- tools
- malware
- infostealer
- cross-platform
- Windows
- macOS
- Linux
- SimpleHelp
- CVE-2026-48558
- developer credential theft
- cloud credential theft
- package registry credentials
- AI assistant credentials
- browser credential theft
- SSH keys
- cryptocurrency wallets
- process environment scraping
- AES-256-GCM
- RSA-2048
- Djinn Stealer
- TaskWeaver
- Blackpoint Cyber

## Why this matters
- Djinn's target list maps directly to modern developer and administrator blast radius: cloud tenants, code repositories, package registries, build tools, AI assistants, and wallets.
- On Linux, the stealer attempts to read `/proc/<pid>/cmdline` and `/proc/<pid>/environ`, which can expose secrets passed through command-line arguments or environment variables.
- Exfiltrated developer credentials can outlive endpoint containment through repository access, CI/CD tokens, cloud sessions, deployment credentials, and package-publishing authority.
- The SimpleHelp delivery path means infected systems may be managed endpoints reached through a trusted support channel, not only developer machines directly exposed to phishing.

## Targeted data classes
The Hacker News summary of Blackpoint's analysis says Djinn attempts to collect:

- browser credentials, history, and bookmarks;
- cloud and SaaS credentials for AWS, Azure, Google Cloud, Oracle Cloud Infrastructure, Okta, Cloudflare, DigitalOcean, Linode, Heroku, Vercel, Railway, Supabase, Pulumi, Terraform, HashiCorp Vault, and Consul;
- GitHub CLI data, Git configuration, SSH keys, Docker authentication, Helm registry information, S3 and MinIO client configuration, and Subversion credentials;
- package-manager and registry credentials for npm, pnpm, Yarn, NuGet, Cargo, Composer, Maven, Gradle, pip, PyPI, Conda, Bun, Ivy, and Scala Build Tool;
- AI-development-assistant configuration, authentication, session, and project data for Anthropic Claude, Google Gemini, OpenAI Codex, Cline, OpenCode, and Kilo;
- cryptocurrency wallets and keystores for Bitcoin, Litecoin, Dogecoin, Dash, Ethereum, Monero, Zcash, Exodus, Atomic Wallet, and Electrum;
- Linux process command lines and environments via `/proc/<pid>/cmdline` and `/proc/<pid>/environ`.

## Exfiltration behavior
- Collected material is packed into a TAR archive and compressed with GZIP.
- The archive is encrypted with AES-256-GCM.
- The AES key is protected by an RSA-2048 public key embedded in TaskWeaver.
- The exfiltration endpoint reported by The Hacker News from Blackpoint's analysis is `96.126.130[.]126:58942`.

## Defender heuristics
- Hunt for outbound connections to `96.126.130[.]126:58942`, especially from SimpleHelp-managed endpoints or hosts that recently executed Node.js payloads.
- Search for suspicious archive staging followed by GZIP compression and network egress from user workstations, admin hosts, build systems, and support-managed endpoints.
- Treat infection as a credential incident. Rotate or revoke browser-derived sessions, SSH keys, cloud credentials, source-control tokens, package-registry tokens, Docker/Helm/S3 credentials, AI-assistant tokens, and wallet material that may have been present.
- On Linux, audit process-environment secret handling: long-lived services, shells, CI agents, package managers, and developer tools that expose tokens in `/proc` to same-user or elevated processes.
- Correlate with SimpleHelp logs for technician file transfers, script execution, and sessions created through OIDC claims that do not match normal IdP telemetry.
- Preserve payloads, process trees, command lines, browser profile timestamps, cloud CLI config timestamps, package-manager config files, and network logs before wiping hosts.

## Related pages
- [TaskWeaver](taskweaver.md)
- [SimpleHelp CVE-2026-48558 authentication-bypass exploitation](../ops/simplehelp-cve-2026-48558-authentication-bypass-exploitation.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)
- [JetBrains AI plugin API-key theft](../ops/jetbrains-ai-plugin-api-key-theft.md)

## Sources
- The Hacker News: [https://thehackernews.com/2026/06/attackers-exploit-simplehelp-cve-2026.html](https://thehackernews.com/2026/06/attackers-exploit-simplehelp-cve-2026.html)
- Blackpoint Cyber: [https://blackpointcyber.com/blog/a-djinn-in-the-machine-taskweavers-node-js-intrusion-chain/](https://blackpointcyber.com/blog/a-djinn-in-the-machine-taskweavers-node-js-intrusion-chain/)
- Horizon3.ai: [https://horizon3.ai/attack-research/disclosures/cve-2026-48558-simplehelp-authentication-bypass-iocs/](https://horizon3.ai/attack-research/disclosures/cve-2026-48558-simplehelp-authentication-bypass-iocs/)
