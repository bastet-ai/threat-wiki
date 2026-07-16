# @withgoogle/stitch-sdk scope squat

## Summary
SafeDep reported a malicious npm package, `@withgoogle/stitch-sdk`, that impersonated Google's Stitch AI design tool by squatting the `@withgoogle` scope. The package used a `preinstall` hook and a duplicated CLI execution path to harvest developer identity and credential material, then exfiltrated findings to attacker-controlled infrastructure.

Treat this as an operation because it combines AI-brand trust, scope confusion, install-time execution, and developer credential harvesting in a compact package-registry incident.

## Tags
- ops
- operations
- supply-chain
- npm
- scope squatting
- typosquatting
- Google Stitch
- AI tooling
- developer credentials
- Claude Code
- GitHub CLI
- npm tokens
- Docker credentials
- preinstall
- credential theft
- SafeDep

## Reported chain

### Scope and brand confusion
- Google's Stitch product is hosted at `stitch.withgoogle.com`, while the legitimate npm SDK naming described by SafeDep is under Google's normal `@google` scope.
- The malicious package used `@withgoogle/stitch-sdk`, making the npm scope look aligned with the product domain even though SafeDep says it was not the legitimate Google package.
- SafeDep observed versions `0.1.1` and `0.1.2` and said the package recorded 87 downloads on its first day of publication, June 19, 2026.
- The package README and CLI help text presented a plausible cover story, including a warning that install scripts are dangerous while the package itself used one to harvest data.

### Install-time credential harvesting
- The credential harvester ran from a `preinstall` hook triggered by `npm install`.
- SafeDep also found the same collection logic duplicated in `bin/cli.js`, giving the attacker a second execution path if a user ran the package CLI.
- SafeDep described the JavaScript as readable and unobfuscated; the attacker leaned on brand and scope trust rather than heavy concealment.

### Targeted data and exfiltration
SafeDep reported collection attempts against:

- Claude Code authenticated-user context through `claude auth status`.
- Git configuration and `~/.git-credentials`.
- SSH public-key comments in `~/.ssh/*.pub`.
- GitHub CLI context.
- npm configuration and `~/.npmrc`.
- Docker configuration in `~/.docker/config.json`.

Reported exfiltration used HTTPS GET requests to `stitch-production[.]org/api/v1`, with query parameters such as `src=<source>` and `user=<credential>`. SafeDep also noted TLS certificate validation was disabled for outbound requests.

## Defender heuristics

### Package and source review
- Block or quarantine `@withgoogle/stitch-sdk` versions `0.1.1` and `0.1.2` in npm proxies, package firewalls, and endpoint package-policy tools.
- Search dependency manifests, lockfiles, shell history, CI logs, and npm cache metadata for `@withgoogle/stitch-sdk`.
- Flag AI-product package names where a vendor-looking scope is based on a product domain rather than the vendor's established package namespace.
- Treat README statements that install hooks are "benign" as untrusted; verify the actual `preinstall`, `install`, `postinstall`, and `bin` entrypoints.

### Endpoint and CI triage
- If the package installed or its CLI ran, treat the host as potentially exposed even if no obvious payload remains.
- Review process and shell telemetry for `npm install @withgoogle/stitch-sdk`, `claude auth status`, GitHub CLI commands, `git config` reads, and access to `.npmrc`, `.git-credentials`, `.docker/config.json`, or SSH key directories during the install window.
- Rotate exposed npm tokens, GitHub tokens, Docker registry credentials, SSH credentials, and any AI-tool or cloud credentials reachable from the affected account.
- For developer workstations with browser sessions, source-control credentials, and package-registry tokens, prefer rebuild-and-rotate over one-time file cleanup.

### Registry and governance lessons
- Reserve vendor and product-adjacent scopes before public product launches when possible.
- Enforce package-manager controls that require explicit approval for install-time scripts, especially on developer machines and CI runners.
- Monitor newly created packages that combine AI-brand keywords with install hooks and credential-file reads.
- Maintain an allowlist of approved vendor scopes for high-trust SDKs instead of trusting package names that visually match product domains.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Malware-Slop Claude user-data npm infostealer](malware-slop-claude-user-data-npm-infostealer.md)
- [Mastra easy-day-js npm scope compromise](mastra-easy-day-js-npm-scope-compromise.md)

## Sources
- [SafeDep](https://safedep.io/withgoogle-stitch-sdk-scope-squat-credential-harvester)
