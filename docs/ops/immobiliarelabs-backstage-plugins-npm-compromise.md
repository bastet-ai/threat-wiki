# Immobiliare Labs Backstage plugins npm compromise

## Summary
StepSecurity reported that on June 26, 2026 multiple versions across four Immobiliare Labs Backstage plugin packages were compromised on npm. The malicious releases used the Miasma / Phantom Gyp pattern: a root `binding.gyp` file caused npm's native-addon build path to run a newly added 5 MB `index.js` during `npm install`, even without an obvious `package.json` lifecycle script.

The affected packages are Backstage GitLab and LDAP authentication plugins used by platform-engineering teams that run self-hosted Backstage developer portals. StepSecurity said all compromised versions were inserted as patch releases across supported major release series within a 30-second window, making this a narrow but high-signal continuation of the Miasma-style supply-chain payload factory rather than ordinary typosquatting.

## Tags
- ops
- operations
- supply-chain
- npm
- Backstage
- CI/CD
- GitHub Actions
- credential-theft
- worm
- Miasma
- Mini Shai-Hulud
- Phantom Gyp
- node-gyp
- binding.gyp
- AI assistants

## Why this matters
- Backstage plugins commonly run in internal developer portals with GitLab, LDAP / Active Directory, CI/CD, cloud, and package-registry adjacency, so a plugin install can sit close to sensitive platform-engineering secrets.
- The `binding.gyp` trigger bypasses controls that only inspect `preinstall` / `postinstall` entries in `package.json`; npm can invoke `node-gyp rebuild` implicitly when a package contains a native-addon manifest.
- StepSecurity's analysis links the payload shape to the Miasma / Leo Platform wave: Bun `v1.3.13` staging, `Runner.Worker` memory scraping, cloud and package-registry credential theft, GitHub dead-drop exfiltration, and AI-assistant persistence.
- The simultaneous patch-release pattern means defenders should search lockfiles and caches by exact package/version pairs, not just by package family or latest version.

## Affected packages
StepSecurity lists the following compromised npm versions:

| Package | Compromised versions |
| --- | --- |
| `@immobiliarelabs/backstage-plugin-gitlab` | `1.0.1`, `2.1.2`, `3.0.3`, `4.0.2`, `5.2.1`, `6.13.1`, `7.0.2` |
| `@immobiliarelabs/backstage-plugin-gitlab-backend` | `3.0.3`, `4.0.2`, `5.2.1`, `6.13.1`, `7.0.2` |
| `@immobiliarelabs/backstage-plugin-ldap-auth` | `1.1.4`, `2.0.5`, `3.0.2`, `4.3.2`, `5.2.1` |
| `@immobiliarelabs/backstage-plugin-ldap-auth-backend` | `1.1.3`, `2.0.5`, `3.0.2`, `4.3.2`, `5.2.1` |

StepSecurity's worked diff compared `@immobiliarelabs/backstage-plugin-gitlab@2.1.2` against the prior clean `2.1.1` release and found two new root-level files absent from earlier releases: `index.js` and `binding.gyp`.

## Reported payload behavior
- Root-level `binding.gyp` executes the malicious `index.js` during npm install through the implicit `node-gyp` path.
- The 5 MB JavaScript payload uses multiple obfuscation layers: a ROT-2 Caesar transform, AES-128-GCM encrypted blobs, and obfuscator.io-style string-table rotation.
- The first decrypted stage downloads Bun from `https://github.com/oven-sh/bun/releases/download/bun-v1.3.13/`, writes the main payload to a random temporary file, executes it with Bun, and removes the temporary script.
- Static string-table analysis shows collection logic for GitHub PATs, GitHub App JWTs, OIDC tokens, GitHub Actions runner tokens, and masked GitHub Actions secrets via `/proc/<pid>/mem` reads of the `Runner.Worker` process.
- The payload targets AWS credentials and metadata, SSM Parameter Store, Secrets Manager, GCP service-account material, Azure managed identity / service principal / Key Vault credentials, Kubernetes service-account tokens and namespace secrets, HashiCorp Vault tokens, npm / PyPI / RubyGems / JFrog tokens, password-manager data from Bitwarden / 1Password / `gopass`, and related developer secrets.
- StepSecurity identified an `infectHost` function that attempts AI-assistant persistence, including modification of `.github/copilot-instructions.md`; treat this as repository-local persistence that can survive package yanking.
- Functions named `squatPackage`, `handleNpmTokens`, and `handlePypiTokens` suggest the same package-republication / worming capability seen in earlier Miasma-family reporting.

## Indicators and hunt pivots
- Any lockfile, package cache, artifact repository, CI log, or developer endpoint with one of the affected package/version pairs above.
- Root package files `binding.gyp` and a 5 MB `index.js` in Immobiliare Labs Backstage plugin packages.
- StepSecurity-reported npm integrity hash for the `@immobiliarelabs/backstage-plugin-gitlab@2.1.2` tarball: `sha512-k7pGY+wScfqX51fpF412dOze6kSIytHYwZAXPhu6pDV+R7JWnD98Uc0nzGVHFead99nwWU4x56fkre/jH3Q7Xg==`.
- Bun download URL pattern `https://github.com/oven-sh/bun/releases/download/bun-v1.3.13/bun-<os>-<arch>.zip` during a package install.
- `node-gyp` spawning Node, download tools, archive extraction, or Bun during dependency installation.
- Attempts to read `/proc/<pid>/mem` for `Runner.Worker` from an npm install context.
- Unexpected writes to `.github/copilot-instructions.md` or other AI-assistant / IDE configuration files after a package install.

## Response guidance
1. Treat installs of affected versions as developer-host or CI-runner compromise, not just bad dependency resolution.
2. Stop affected workflows and isolate potentially infected hosts before broad token revocation if an active Miasma-family token monitor may be running.
3. Preserve npm cache artifacts, lockfiles, CI logs, runner process telemetry, GitHub audit logs, and package tarballs before cleanup.
4. Remove affected package versions and rebuild developer / CI environments from known-clean images where practical.
5. Rotate reachable GitHub, npm, PyPI, RubyGems, JFrog, cloud, Kubernetes, Vault, SSH, LDAP/AD integration, and password-manager-derived credentials after malicious processes are stopped.
6. Audit repositories reachable by exposed GitHub tokens for workflow changes, newly committed AI-assistant config files, `.github/copilot-instructions.md` edits, and GitHub dead-drop artifacts.
7. Add registry cooldown / quarantine for freshly published patch releases and file-content detection for unexpected `binding.gyp` plus root-level multi-megabyte JavaScript payloads.

## Upstream-access reconstruction
Socket's follow-up likewise tracks the releases as part of the Miasma / Mini Shai-Hulud campaign and adds a public lead for incident reconstruction: `codfish/semantic-release-action`, compromised on June 24, 2026, was referenced by public repositories under the `simonecorsi` organization. Socket frames that as a **plausible but unconfirmed** path from mutable GitHub Action tag hijack to release automation with npm publishing or GitHub deployment permissions.

Treat this as a scoping hypothesis, not established root cause. For affected maintainers or downstream consumers, the useful defender action is to review deployment-triggered GitHub Actions, semantic-release workflows, mutable third-party action references, OIDC trust policies, npm publishing tokens, provenance attestations, and runner logs around the June 24--26 window.

## Attribution notes
StepSecurity frames the incident as connected to the Miasma campaign because it reuses the same Phantom Gyp execution technique, Bun staging, credential-theft scope, `Runner.Worker` memory scraping, and AI-assistant persistence patterns. Socket independently tracks the wave as ongoing Miasma / Mini Shai-Hulud activity and emphasizes that the payload is not a materially new malware family, but an expansion into another legitimate maintainer scope. Keep operator attribution caveated: public Mini Shai-Hulud / Miasma tooling and copycat reuse mean this should be tracked as **Miasma-style / likely same payload factory** unless maintainer or registry forensics establish a specific actor.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md)
- [Leo Platform npm Miasma-style compromise](leo-platform-npm-miasma-compromise.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised
- Socket: https://socket.dev/blog/miasma-mini-shai-hulud-hits-immobiliarelabs-npm-packages
