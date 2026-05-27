# Nx Console VS Code extension compromise

## Summary
On May 18, 2026, public reporting from StepSecurity and the Nx project described a compromised release of the **Nx Console** VS Code extension (`nrwl.angular-console` version `18.95.0`). The malicious extension used the IDE extension channel rather than npm package publication: once a developer opened a workspace, the extension fetched and executed an obfuscated payload from an orphan commit hidden in the official `nrwl/nx` GitHub repository.

StepSecurity reported that the payload stole developer and CI/CD credentials, exfiltrated through multiple channels, and installed macOS persistence. GitHub later publicly confirmed that an employee device was compromised by a poisoned third-party VS Code extension and linked to the Nx Console security advisory; GitHub said the activity involved exfiltration of GitHub-internal repositories only and that the attacker's claim of roughly 3,800 repositories was directionally consistent with its investigation.

## Tags
- ops
- operations
- supply-chain
- VS Code
- IDE extension
- GitHub
- credential-theft
- persistence
- TeamPCP

## Why this matters
- IDE extensions run on high-trust developer machines where source code, cloud credentials, package-publishing tokens, password-manager sessions, and GitHub access often coexist.
- Marketplace distribution is an adjacent supply-chain lane: defenders who only scan package lockfiles can miss poisoned editor extensions.
- The campaign shows a useful attacker pattern: stolen contributor or maintainer tokens can be used to plant unreachable/orphaned repository content that is still retrievable by commit hash, then referenced by a trusted release artifact.
- GitHub's May 20 incident note confirms source-code theft as a downstream impact of the poisoned extension channel: developer endpoint compromise can become internal-repository exposure even without customer-repository compromise.

## Reported chain
1. A contributor token was reportedly stolen during an earlier supply-chain incident.
2. The attacker pushed an orphan commit to the official `nrwl/nx` repository.
3. A compromised `nrwl.angular-console` extension version `18.95.0` was published to the VS Code Marketplace.
4. Opening a workspace triggered the extension to fetch and execute a large obfuscated payload from the orphan commit.
5. The payload targeted GitHub, npm, cloud, Kubernetes, Vault, 1Password, and other developer secrets; StepSecurity also reported HTTPS, GitHub API, and DNS-tunneling exfiltration plus macOS Python backdoor persistence.

## StepSecurity technical update (May 21)
StepSecurity's expanded analysis adds several durable details for defenders:

- **Exposure window:** the malicious VS Code Marketplace release was reportedly live for roughly 11 minutes, from `12:36` to `12:47` UTC on May 18, 2026. OpenVSX was not affected.
- **Delivery:** the injected extension code launched a hidden VS Code task named `install-mcp-extension` that ran `npx -y github:nrwl/nx#558b09d7ad0d1660e2a0fb8a06da81a6f42e06d2`; the orphan commit presented itself as `nx-next` and pulled `bun` to provide the runtime.
- **Anti-analysis and stealth:** the payload checked CPU count, likely geofenced Russian/CIS locale/timezone signals, created a lock file, and daemonized with `__DAEMONIZED=1` so the parent task returned cleanly.
- **Collection breadth:** collectors targeted GitHub, npm, AWS, Vault, Kubernetes, 1Password, local filesystem secrets, Claude Code configuration under `~/.claude/`, and Linux process memory via `/proc/*/mem`.
- **Exfiltration:** StepSecurity described three independent paths: encrypted HTTPS, GitHub API abuse using discovered tokens, and DNS tunneling.
- **Trust forgery risk:** the payload included Fulcio/Rekor/SLSA/in-toto logic and npm OIDC token exchange support, meaning a stolen trusted-publishing context could produce malicious packages with apparently valid Sigstore/SLSA provenance.
- **Persistence:** macOS persistence wrote `~/.local/share/kitty/cat.py` and `~/Library/LaunchAgents/com.user.kitty-monitor.plist`; the backdoor polled GitHub commit search for `firedalazer` commands signed with an embedded RSA key.
- **Privilege escalation:** on Linux, the payload probed passwordless sudo and attempted to add NOPASSWD sudoers access if that path was available.

## Indicators and hunt pivots
- Extension: `nrwl.angular-console` exactly `18.95.0`.
- Orphan commit: `558b09d7ad0d1660e2a0fb8a06da81a6f42e06d2`; tree `ba642fe2c7c65e42dd7f6444b83023dc6827e08c`; `index.js` blob `acfc3f957a63b4cde93ff645f2b6bf26a8ed1bbf`; `package.json` blob `9d88f040c44b5f4d5f9db15ff89310776c168e99`.
- SHA-256: malicious VSIX `1a4afce34918bdc74ae3f31edaffffaa0ee074d83618f53edfd88137927340b8`; malicious `main.js` `b0cefb66b953e5184b6adb3035e9e267335ac5eabfe1848e07834777b9397b74`; orphan-commit `index.js` `e7347d90653efc565f03733a95e9209d78f9cfa81e31ff2b2dd9d48d75a4b8b1`; dropper `package.json` `43f2b001846c4966073ebffa5be8f15e491a1e7d32bbd805d57406ff540e0dd9`.
- Host artifacts: `~/.local/share/kitty/cat.py`, `~/Library/LaunchAgents/com.user.kitty-monitor.plist`, `/var/tmp/.gh_update_state`, `/tmp/kitty-*`, VS Code globalState key `nxConsole.mcpExtensionInstalledSha` set to the orphan commit, and npm cache entries for `github:nrwl/nx#558b09d7`.
- Runtime/network pivots: `__DAEMONIZED=1`, Bun/Node processes from `/tmp/kitty-*`, `python3` running `cat.py`, GitHub search queries for `firedalazer`, DNS tunneling from developer endpoints, IMDS/ECS metadata hits (`169.254.169.254`, `169.254.170.2`), and unexpected Fulcio/Rekor/Sigstore activity under affected identities.

## Defender heuristics
- Inventory installed VS Code and OpenVSX extensions across developer endpoints; include version history, publisher, install time, and auto-update settings.
- Treat `nrwl.angular-console` `18.95.0` installs as endpoint compromise, not merely as a package-removal event.
- Hunt for unexpected outbound requests to opaque commit URLs, GitHub raw content, DNS exfiltration patterns, and newly created public repos from developer accounts.
- Review GitHub, npm, cloud, Kubernetes, Vault, Docker, SSH, and password-manager exposure for affected workstations.
- Rotate tokens only after persistence and exfiltration paths are contained; otherwise new credentials can be re-stolen.
- Add extension-marketplace telemetry to supply-chain monitoring alongside package registries and GitHub Actions workflows.

## Attribution notes
- GitHub's incident note links the employee-device compromise to the Nx Console security advisory, confirming the extension family involved in the source-code exfiltration event.
- StepSecurity's May 21 update states that TeamPCP is behind the GitHub breach and is attempting to sell the stolen data. Treat that as a strong vendor assessment, while preserving the distinction that GitHub's own note did not publicly name TeamPCP.

## CISA KEV update (May 27)
CISA added **CVE-2026-48027** to the Known Exploited Vulnerabilities catalog on May 27, 2026 as "Nx Console Embedded Malicious Code Vulnerability," with remediation due by June 10, 2026 for covered agencies. CISA's entry reinforces the operational framing here: a malicious extension release should be handled as exploitation of a trusted software channel with credential harvesting, not as a normal vulnerable-version upgrade.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/nx-console-vs-code-extension-compromised
- GitHub Blog: https://github.blog/security/investigating-unauthorized-access-to-githubs-internal-repositories/
- GitHub Security Advisory: https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- The Hacker News: https://thehackernews.com/2026/05/github-investigating-teampcp-claimed.html
