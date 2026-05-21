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

## Defender heuristics
- Inventory installed VS Code and OpenVSX extensions across developer endpoints; include version history, publisher, install time, and auto-update settings.
- Treat `nrwl.angular-console` `18.95.0` installs as endpoint compromise, not merely as a package-removal event.
- Hunt for unexpected outbound requests to opaque commit URLs, GitHub raw content, DNS exfiltration patterns, and newly created public repos from developer accounts.
- Review GitHub, npm, cloud, Kubernetes, Vault, Docker, SSH, and password-manager exposure for affected workstations.
- Rotate tokens only after persistence and exfiltration paths are contained; otherwise new credentials can be re-stolen.
- Add extension-marketplace telemetry to supply-chain monitoring alongside package registries and GitHub Actions workflows.

## Attribution notes
- GitHub's incident note links the employee-device compromise to the Nx Console security advisory, confirming the extension family involved in the source-code exfiltration event.
- StepSecurity links the broader durabletask and Mini Shai-Hulud activity to TeamPCP. For Nx Console, keep TeamPCP attribution caveated unless a primary source directly ties the extension compromise to TeamPCP.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/nx-console-vs-code-extension-compromised
- GitHub Blog: https://github.blog/security/investigating-unauthorized-access-to-githubs-internal-repositories/
- GitHub Security Advisory: https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w
- The Hacker News: https://thehackernews.com/2026/05/github-investigating-teampcp-claimed.html
