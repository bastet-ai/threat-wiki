# Bitwarden / Checkmarx Shai-Hulud Third Coming campaign

## Summary
On April 22, 2026, Unit 42 reported a TeamPCP-attributed supply-chain wave that used a malicious `@bitwarden/cli@2026.4.0` npm package as one delivery lane and reused the same payload across compromised Checkmarx distribution channels.

The package impersonated Bitwarden's command-line interface and executed during npm install. Unit 42 says the campaign's public GitHub artifacts included the string `Shai-Hulud: The Third Coming`, making it a bridge between the original Shai-Hulud worm lineage and the later Mini Shai-Hulud waves.

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
- Bitwarden stated the affected window was limited to npm distribution for CLI version `2026.4.0` and reported no evidence that end-user vault data, production systems, or production data were accessed.

## Reported chain
1. `@bitwarden/cli@2026.4.0` was briefly distributed through npm between roughly 5:57 PM and 7:30 PM EST on April 22, 2026.
2. `package.json` added a `preinstall` execution path for `bw_setup.js`.
3. The package also registered `bw_setup.js` as the `bw` binary, matching the legitimate Bitwarden CLI command name and creating a secondary trigger if a user later invoked `bw`.
4. The bootstrap downloaded/ran Bun and staged an obfuscated payload.
5. The payload harvested developer, cloud, CI/CD, package-manager, and repository credentials, then used encrypted HTTPS and public GitHub repositories for exfiltration/fallback.
6. Unit 42 reported the same payload family across Checkmarx channels, including poisoned `checkmarx/kics` Docker Hub images, `checkmarx/ast-github-action`, and backdoored Checkmarx VS Code extensions.

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

## Defender heuristics
- Treat affected `@bitwarden/cli@2026.4.0` installs as developer-host compromise, not only package compromise.
- Search package-manager caches, shell history, EDR telemetry, and CI logs for `@bitwarden/cli@2026.4.0`, `bw_setup.js`, Bun downloads, and the listed C2/dead-drop indicators.
- Inventory Checkmarx-distributed artifacts used in build systems: KICS Docker images, AST GitHub Action versions, and Checkmarx VS Code extensions.
- Rebuild affected development and CI environments from known-clean images before rotating reachable credentials.
- Rotate GitHub, npm, Docker, cloud, Kubernetes, Vault, SSH, and CI/CD secrets that were accessible to affected hosts or runners.
- Add supply-chain monitoring for command-name masquerade in packages that register binaries matching high-trust tools.

## Attribution notes
- Unit 42 attributes the broader campaign to TeamPCP and reports that TeamPCP (`@pcpcats`) publicly took credit for the Checkmarx compromise.
- Keep Bitwarden customer-impact statements tied to Bitwarden's own incident response language: affected npm distribution path only, no evidence of vault or production compromise in the cited reporting.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [actions-cool GitHub Actions tag compromise](actions-cool-github-actions-tag-compromise.md)

## Sources
- Unit 42: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
- Bitwarden security advisory context as cited by Unit 42: https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
