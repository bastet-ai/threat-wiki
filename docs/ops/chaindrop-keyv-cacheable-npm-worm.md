# ChainDrop keyv / cacheable npm worm

## Summary
On August 4, 2026, StepSecurity, Socket, and Aikido reported a fast-moving npm supply-chain worm affecting `keyv`, the `cacheable` package family, and packages reachable through stolen maintainer identities. StepSecurity named the activity **ChainDrop**. Aikido described it as active Shai-Hulud activity; Socket assessed that its tradecraft closely matches Shai-Hulud but did not recover a self-identifying campaign marker from the analyzed payload.

The malicious releases add an npm `preinstall` hook, download Bun `1.3.13`, run a heavily obfuscated second stage, harvest developer, CI/CD, cloud, package-registry, Vault, and Kubernetes credentials, and use stolen npm access or OIDC trusted publishing to republish trojanized packages. Socket also reported GitHub and DNS exfiltration plus `.claude` and `.vscode` repository hooks that can execute when source is opened without requiring `npm install`.

This is an **active incident**. Package and version counts below reflect public reporting captured around 11:25 UTC on August 4 and will change. Use the linked vendor-maintained lists for live scoping.

## Tags
- ops
- operations
- supply-chain
- npm
- credential-theft
- worm
- Shai-Hulud
- ChainDrop
- Bun
- GitHub Actions
- OIDC
- CI/CD
- developer-targeting

## Why this matters
- Aikido reported at least **1,280 compromised packages** by its 13:20 CEST update, while StepSecurity observed dozens of releases across unrelated scopes in one hour. The vendor lists were still expanding at publication time.
- The initial package family sits deep in common dependency trees. Public reporting identifies `keyv`, `cacheable-request`, `flat-cache`, `file-entry-cache`, and related caching packages used transitively by developer tooling.
- Aikido says malicious source changes were pushed to the legitimate repository and released through GitHub Actions, so affected packages could carry valid provenance. Provenance proved which workflow built the artifact, not that the source or maintainer identity was clean.
- The payload turns credential theft into automated package propagation and adds source-repository execution paths for IDEs and AI coding agents.

## Confidence and attribution
- The compromise and malicious package behavior are corroborated by StepSecurity, Socket, and Aikido.
- Aikido labels the wave active Shai-Hulud activity. Socket says the behavior closely matches Shai-Hulud: TruffleHog-style secret collection, maintainer-package enumeration, npm token and OIDC publication, and victim-account GitHub repositories.
- Socket did **not** recover the campaign's self-identifying repository or commit markers because relevant strings were assembled at runtime. Public Shai-Hulud-derived tooling also makes copycat reuse possible. Track ChainDrop as a Shai-Hulud-lineage assessment, not confirmed TeamPCP attribution.
- Socket and Aikido identify compromise of the `Jaredwray` maintainer/GitHub account as the initial high-impact access path. Maintainer and registry postmortems were not yet public at capture time.

## Reported execution chain
1. The attacker publishes a new package version containing `setup.mjs`, `Math_Symbol.js` (also referenced internally as `math_init.js`), and `"preinstall": "node setup.mjs"`.
2. `setup.mjs` detects platform and architecture, including Alpine/musl, and obtains a platform-specific Bun `1.3.13` runtime from the legitimate `oven-sh/bun` GitHub Releases path when Bun is absent.
3. The loader extracts Bun with system `unzip`, PowerShell `Expand-Archive`, or a JavaScript ZIP fallback, then executes the second stage under Bun.
4. Socket describes the second stage as a roughly 728 KB bundle with polymorphic basE91-protected strings and internal modules tagged `[collector]`, `[dispatcher]`, `[provenance]`, and `[publish]`.
5. The collector reads local credentials, environment variables, cloud metadata, managed secret stores, runner identity material, and generic token/private-key patterns.
6. The worm calls npm identity and search endpoints, discovers packages reachable by the stolen maintainer identity, downloads clean tarballs, injects its files and lifecycle hook, bumps versions, recomputes integrity metadata, and republishes.
7. Where trusted publishing is available, it attempts npm's OIDC token-exchange endpoint. A poisoned source tree can therefore produce a valid npm/Sigstore provenance attestation.
8. Socket reports encrypted findings sent through attacker-created GitHub repositories and a separate DNS channel. The source repository can also receive `.claude/settings.json` `SessionStart` hooks and `.vscode/tasks.json` `folderOpen` tasks that rerun the loader when a developer or coding agent opens a clone.

## Credential and secret targets
Reported collection includes:

- npm authentication tokens and registry identity/token endpoints;
- GitHub CLI tokens, PATs, session material, Actions OIDC request tokens, and organization/repository secrets;
- AWS credential chains, instance/container metadata, and Secrets Manager across regions;
- GCP service-account private keys and Azure client secrets;
- HashiCorp Vault tokens, including `/home/runner/.vault-token`, `/run/secrets/VAULT_TOKEN`, and `VAULT_TOKEN`;
- Kubernetes service-account tokens under `/var/run/secrets/kubernetes.io/serviceaccount/token`;
- generic bearer tokens, API keys, and private-key blocks discovered with a TruffleHog-style filesystem sweep.

## Initial high-impact package set
Socket's ongoing list at capture time included:

| Package | Reported malicious version |
|---|---:|
| `keyv` | `6.0.0` |
| `cacheable` | `2.5.1` |
| `cacheable-request` | `13.0.20` |
| `flat-cache` | `6.1.24` |
| `@cacheable/net` | `2.1.1` |
| `@cacheable/node-cache` | `3.1.2` |
| `@cacheable/memory` | `2.2.1` |
| `@cacheable/utils` | `2.5.1` |
| `cache-manager` | `7.2.10` |
| `file-entry-cache` / `@file-entry-cache` | `11.1.6` as reported; verify registry identity against vendor lists |

StepSecurity's early list also included packages in `@arv-bedrock`, `@deliveroo`, `@hubsync`, `@onereach`, `@or-sdk`, `@ornikar`, `@picsart`, `@qlik`, and `@servicetitan` scopes, plus `ecto`, `pob-test-typescript-package-in-monorepo`, and `tslint-folder-schema`. Aikido reported rapid spread into additional maintainers and organizations. Do not treat this table as complete.

## Indicators and hunting pivots

### Files and execution
- `setup.mjs`
- `Math_Symbol.js`
- `math_init.js`
- npm lifecycle entry `"preinstall": "node setup.mjs"`
- process chain `node setup.mjs` spawning a downloaded `bun`
- temporary paths matching `bun-dl-*`
- unexpected `.claude/settings.json` `SessionStart` hooks
- unexpected `.vscode/tasks.json` tasks with `runOn: folderOpen`

### SHA-256
- `fd3ca4007b225fdf8de7af4345a19179d5efa8c4bb9205f88cda806e5684b1eb` — `setup.mjs`
- `54dc7ea54a1317cca0e890a2770630cf7fa6c97813e0cb9d2caa93012b350668` — `setup.mjs` tarball variant
- `9fc2570b7cef51c1b8df116d144d11ff4096357be7d2c4c6367cfc2509cf1bcc` — `math_init.js` / `Math_Symbol.js`

### Network and control-plane behavior
- `github[.]com/oven-sh/bun/releases/download/bun-v1.3.13/` — legitimate Bun distribution path; validate package-install process ancestry rather than blocking blindly
- `169[.]254[.]169[.]254` and `169[.]254[.]170[.]2` metadata access from developer or build processes
- `registry[.]npmjs[.]org/-/whoami`
- `registry[.]npmjs[.]org/-/npm/v1/tokens`
- `registry[.]npmjs[.]org/-/npm/v1/oidc/token/exchange/package/`
- GitHub API `POST /user/repos`, GraphQL `createCommitOnBranch`, newly created repositories, and commits from developer or CI identities
- anomalous DNS exfiltration from package-install or Bun processes

The npm and GitHub endpoints are legitimate. Alert on unusual process ancestry, identity, volume, and timing rather than treating the domains as stand-alone malicious indicators.

## Defender actions

### Immediate exposure check
1. Freeze dependency updates and block the affected package families/scopes at registry proxies while the maintainer and registry response is unresolved.
2. Search `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, package-manager caches, CI logs, SBOMs, and artifact repositories for the vendor-maintained package/version lists.
3. Determine whether install scripts executed. A lockfile reference without installation is a different exposure class from a developer host or runner that ran the malicious `preinstall` hook.
4. Search cloned repositories independently for `.claude` and `.vscode` hooks because those paths can execute without npm installation.

### If an affected version executed
1. Isolate developer hosts and runners; stop active workflows and publication paths.
2. Preserve endpoint, CI, npm, GitHub, DNS, cloud, and registry evidence before rebuilding.
3. Treat every credential reachable from the process as exposed. Revoke and replace npm, GitHub, cloud, Vault, Kubernetes, SSH, CI, and application secrets; do not rotate only npm tokens.
4. Audit npm for unexpected versions published by affected identities and GitHub for force pushes, deleted/recreated tags, new repositories, unexpected commits, transient workflows, OIDC exchanges, and repository hooks.
5. Rebuild affected machines/runners and dependency caches from known-clean images and commits. Roll back to verified clean package versions only after maintainer or registry confirmation.
6. Review cloud control planes for metadata-credential use outside expected hosts, broad secret enumeration, and activity by CI identities after the first package installation.

### Preventive controls
- Deny package install scripts by default where feasible and explicitly approve required scripts. This reduces the initial `preinstall` lane but does not stop malicious source hooks or runtime imports.
- Use dependency cooldowns and tarball diffs; flag new lifecycle hooks, large obfuscated root files, runtime downloads, and sudden releases across many packages.
- Bind trusted publishing to protected GitHub Environments and branch rules. Provenance alone cannot distinguish a legitimate workflow building attacker-controlled source.
- Separate untrusted pull-request workflows from release permissions, protect release branches/tags, require reviewed changes to workflow and editor/agent configuration, and monitor force pushes.
- Restrict CI and developer egress to cloud metadata, secret stores, npm publication endpoints, GitHub repository creation, and unnecessary DNS resolvers.

## Open questions
- Final affected package/version and download scope after npm containment.
- Initial access and whether the `Jaredwray` account, endpoint, token, GitHub session, or another upstream identity was first compromised.
- Registry and GitHub containment actions, malicious-version removal times, and credential invalidation scope.
- Names, visibility, and recoverable indicators for attacker-created GitHub exfiltration repositories and the DNS channel.
- Whether ChainDrop is operated by TeamPCP, another Shai-Hulud-lineage actor, or a copycat using leaked tooling.
- Confirmed victim execution and downstream cloud/repository compromise beyond package publication.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Developer-tool configuration auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- StepSecurity: [ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum dead-drop C2](https://www.stepsecurity.io/blog/chaindrop-npm-worm)
- Socket: [Popular npm Packages in the keyv and Cacheable Namespaces Compromised in Active Supply Chain Attack](https://socket.dev/blog/popular-npm-packages-in-the-keyv-and-cacheable-namespaces-compromised-in-active-supply-chain)
- Aikido Security: [Keyv and friends compromised in active Shai-Hulud supply chain attack](https://www.aikido.dev/blog/keyv-and-friends-compromised-in-npm-supply-chain-attack)
