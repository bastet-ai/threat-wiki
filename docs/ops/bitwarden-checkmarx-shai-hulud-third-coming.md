# Bitwarden / Checkmarx Shai-Hulud Third Coming campaign

## Summary
On April 22, 2026, Unit 42 reported a TeamPCP-attributed supply-chain wave that used a malicious `@bitwarden/cli@2026.4.0` npm package as one delivery lane and reused the same payload across compromised Checkmarx distribution channels.

The package impersonated Bitwarden's command-line interface and executed during npm install. Unit 42 says the campaign's public GitHub artifacts included the string `Shai-Hulud: The Third Coming`, making it a bridge between the original Shai-Hulud worm lineage and the later Mini Shai-Hulud waves. Trend Micro later treated the Bitwarden/Checkmarx activity and the April 24 `elementary-data` compromise as case studies in the same TeamPCP supply-chain campaign.

## Page role
This page covers the April 22 Bitwarden/Checkmarx distribution-channel wave. Use [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) for the broader multi-wave campaign and [TeamPCP](../actors/teampcp.md) for actor-level tradecraft.

## Tags
- ops
- operations
- supply-chain
- npm
- VS Code
- Docker
- GitHub Actions
- CI/CD
- credential-theft
- persistence
- worm
- TeamPCP
- Shai-Hulud
- Checkmarx
- Bitwarden

## Why this matters
- The campaign crossed multiple trusted distribution lanes at once: npm, Docker Hub images, GitHub Actions, and VS Code extensions.
- The `@bitwarden/cli` npm package used both a lifecycle hook and a command-name masquerade path, so blocking install scripts alone may not remove every execution path.
- Unit 42 ties the same custom cipher and runner-memory/OIDC tradecraft to later SAP, TanStack, and Mini Shai-Hulud activity, making this wave useful for campaign correlation.
- Trend Micro's follow-up adds a second lesson from the adjacent `elementary-data` incident: a single unsanitized pull-request comment interpolated into a GitHub Actions `run:` block can become a project-signed PyPI/GHCR release without first stealing maintainer credentials.
- Bitwarden stated the affected window was limited to npm distribution for CLI version `2026.4.0` and reported no evidence that end-user vault data, production systems, or production data were accessed.

## Reported chain
1. `@bitwarden/cli@2026.4.0` was briefly distributed through npm between roughly 5:57 PM and 7:30 PM EST on April 22, 2026.
2. `package.json` added a `preinstall` execution path for `bw_setup.js`.
3. The package also registered `bw_setup.js` as the `bw` binary, matching the legitimate Bitwarden CLI command name and creating a secondary trigger if a user later invoked `bw`.
4. The bootstrap downloaded/ran Bun and staged an obfuscated payload.
5. The payload harvested developer, cloud, CI/CD, package-manager, and repository credentials, then used encrypted HTTPS and public GitHub repositories for exfiltration/fallback.
6. Unit 42 reported the same payload family across Checkmarx channels, including poisoned `checkmarx/kics` Docker Hub images, `checkmarx/ast-github-action`, and backdoored Checkmarx VS Code extensions.

## JFrog package deep dive
JFrog's April 23 real-time analysis supplies package-level indicators and confirms that the malicious packaging layer was added around an older legitimate build: root package version `2026.4.0` contained compiled application metadata still identifying Bitwarden CLI `2026.3.0`.

- `bw_setup.js` checked for Bun and, when absent, downloaded platform-specific Bun `1.3.13` archives from the official `oven-sh/bun` GitHub releases before executing `bw1.js`.
- Local collection included `gh auth token`, process environment variables, GitHub and npm token patterns, SSH keys and known-hosts data, Git credentials, `.npmrc`, `.env`, shell histories, AWS and GCP credential stores, and Claude/Kiro MCP configuration.
- JFrog reported active GitHub abuse rather than passive token collection. The payload validated tokens, enumerated writable repositories and Actions secrets, created a branch and workflow, waited for the workflow artifact, downloaded it, and deleted the branch and workflow run.
- The primary exfiltration path compressed results with gzip, encrypted them with AES-256-GCM, wrapped the AES key with embedded RSA/OAEP-SHA256 material, and posted the envelope to `audit.checkmarx[.]cx/v1/telemetry`.
- If that route failed, the payload searched public GitHub commits for `LongLiveTheResistanceAgainstMachines` to recover staged PATs and for RSA-verified `beautifulcastle` messages to recover a replacement destination. It could then create a repository in the victim account and upload encrypted result blobs under `results/`.

This adds two durable hunting lessons: successful blocking of the primary domain does not remove GitHub-based fallback and exfiltration, and responders should include short-lived workflow branches, artifacts, and deleted workflow runs when scoping a compromised developer token.

## Trend Micro follow-up: KICS and elementary-data
Trend Micro's May 2026 analysis links two April incidents to a broader TeamPCP campaign that abused trusted CI/CD and release workflows for credential theft at scale:

- **Checkmarx KICS / Bitwarden CLI, April 22-23:** Trend Micro reports that TeamPCP pushed malicious `checkmarx/kics` Docker Hub tags, poisoned Checkmarx VS Code/OpenVSX extensions, modified a Checkmarx GitHub Action workflow, and then reused stolen npm tokens within about 24 hours to publish `@bitwarden/cli@2026.4.0`.
- **elementary-data, April 24:** An attacker-controlled GitHub account posted a pull-request comment that was interpolated directly into `.github/workflows/update_pylon_issue.yml`. The runner's `GITHUB_TOKEN` was then used to create an orphan-tagged malicious release commit and trigger the legitimate release workflow, producing a project-signed `elementary-data==0.23.3` PyPI release and overwriting the GHCR `:latest` container tag.
- **Execution path:** KICS / Bitwarden used JavaScript executed through a downloaded Bun runtime. `elementary-data` used an `elementary.pth` Python startup hook, so the payload could execute whenever the Python interpreter started on a host with the malicious package installed, even if `elementary-data` was not imported by application code.
- **Credential scope:** Across the cases, Trend Micro says the payloads targeted GitHub PATs, npm tokens, cloud credentials, SSH keys, Kubernetes secrets, database credentials, infrastructure-as-code files, AI/MCP configuration such as Claude and Kiro settings, and cryptocurrency wallet material.
- **Managed-secret abuse:** The `elementary-data` stealer went beyond local files by using available AWS credentials to call Secrets Manager and SSM Parameter Store APIs, including `secretsmanager:ListSecrets`, `secretsmanager:GetSecretValue`, and `ssm:DescribeParameters`.
- **Cross-campaign markers:** Trend Micro highlights a reused Session messenger identifier as the XOR seed across LiteLLM, Xinference, and `elementary-data`, plus Dune-themed GitHub staging repositories and actor-branded exfiltration headers.

## Infrastructure and indicators to hunt
- `@bitwarden/cli@2026.4.0`
- Unexpected `preinstall` hooks or `bw_setup.js` in Bitwarden CLI installs
- C2 domain `audit.checkmarx[.]cx` and IP `94.154.172[.]43`
- Attacker-controlled `checkmarx[.]cx` and IP `91.195.240[.]123`
- GitHub dead-drop repository `helloworm00/hello-world`
- Commit messages matching `LongLiveTheResistanceAgainstMachines:*`
- Public exfiltration repositories named as Dune-style word pairs with numeric suffixes and description `Checkmarx Configuration Storage`
- Unexpected `.github/workflows/format-check.yml` on transient branches and `format-results` workflow artifacts
- Bun runtime downloads during package install or first `bw` invocation
- `elementary-data==0.23.3` or GHCR images `ghcr[.]io/elementary-data/elementary:0[.]23[.]3` / `:latest` pulled during the April 24-25 exposure window
- Unexpected oversized `elementary.pth` files in Python site-packages, Python interpreter startup spawning outbound HTTPS, or temporary `trin.tar.gz` collection artifacts
- GitHub Actions logs where `github.event.comment.body`, issue titles, or other user-controlled event fields are interpolated directly into `run:` blocks
- CloudTrail events for `secretsmanager:ListSecrets`, `secretsmanager:GetSecretValue`, or `ssm:DescribeParameters` from CI/CD runner roles or data-pipeline identities that do not normally enumerate managed secrets
- `bw1.js`
- Loader SHA-256 `18f784b3bc9a0bcdcb1a8d7f51bc5f54323fc40cbd874119354ab609bef6e4cb`
- Payload SHA-256 `8605e365edf11160aad517c7d79a3b26b62290e5072ef97b102a01ddbb343f14`
- Tampered root-metadata SHA-256 `167ce57ef59a32a6a0ef4137785828077879092d7f83ddbc1755d6e69116e0ad`
- GitHub commit-search marker `beautifulcastle` for signed fallback-domain routing
- Bun `1.3.13` archives fetched from `github[.]com/oven-sh/bun/releases` during package install or first command execution; validate process ancestry and package context before treating the legitimate host as malicious

## Defender heuristics
- Treat affected `@bitwarden/cli@2026.4.0` installs as developer-host compromise, not only package compromise.
- Search package-manager caches, shell history, EDR telemetry, and CI logs for `@bitwarden/cli@2026.4.0`, `bw_setup.js`, Bun downloads, and the listed C2/dead-drop indicators.
- Inventory Checkmarx-distributed artifacts used in build systems: KICS Docker images, AST GitHub Action versions, and Checkmarx VS Code extensions.
- Rebuild affected development and CI environments from known-clean images before rotating reachable credentials.
- Rotate GitHub, npm, Docker, cloud, Kubernetes, Vault, SSH, and CI/CD secrets that were accessible to affected hosts or runners.
- Add supply-chain monitoring for command-name masquerade in packages that register binaries matching high-trust tools.
- Audit GitHub Actions workflows for user-controlled GitHub event fields inside shell `run:` blocks; move untrusted data into environment variables or files and validate before execution.
- Pin Docker images by verified digest rather than mutable tags, especially in CI scanners and developer-security tooling.
- Add CI runner egress controls; both Bun-based and `.pth`-based payloads depend on outbound network access for runtime download, C2 discovery, or credential exfiltration.

## Attribution notes
- Unit 42 attributes the broader campaign to TeamPCP and reports that TeamPCP (`@pcpcats`) publicly took credit for the Checkmarx compromise.
- Trend Micro tracks the same financially motivated cluster as `SHADOW-WATER-058` and states that actor identity, geographic origin, and state affiliation remain low confidence.
- Keep Bitwarden customer-impact statements tied to Bitwarden's own incident response language: affected npm distribution path only, no evidence of vault or production compromise in the cited reporting.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)
- Bitwarden security advisory context as cited by Unit 42: [https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)
- Trend Micro: [https://www.trendmicro.com/en_us/research/26/e/analyzing-teampcp-supply-chain-attacks.html](https://www.trendmicro.com/en_us/research/26/e/analyzing-teampcp-supply-chain-attacks.html)
- JFrog Security Research: [https://research.jfrog.com/post/bitwarden-cli-hijack/](https://research.jfrog.com/post/bitwarden-cli-hijack/)
