# Leo Platform npm Miasma-style compromise

## Summary
StepSecurity reported that on June 24, 2026 an attacker published malicious versions of 20 npm packages in the Leo Platform ecosystem in a coordinated burst lasting less than three seconds. Socket's June 25 follow-up expanded the same wave to 23 npm package versions, including three additional `llxlr`-published packages, and added a related Verana Blockchain Go source-archive poisoning case. Sonatype's June 25 analysis aligned the three `llxlr` packages with the campaign, framed the malicious set as Leo Platform / RStreams plus related packages, and warned that three prerelease Leo connector packages named in some early public reporting did **not** appear to contain the observed payload. JFrog's June 25 writeup independently framed the same 20-package Leo / RStreams set as a Shai-Hulud / Hades continuation and reported approximately 126,000 monthly downloads across the affected package set; StepSecurity's weekly-download view for the Leo / RStreams packages was roughly 13,600 weekly downloads. The packages carried the same CI/CD credential-theft toolkit StepSecurity had documented in the earlier Miasma wave.

StepSecurity assessed the Leo Platform payload as structurally identical to Miasma: the same `binding.gyp` "Phantom Gyp" install hook, the same ROT-N plus AES-128-GCM plus obfuscator.io layering, the same Bun `v1.3.13` download path, GitHub Actions `Runner.Worker` memory scraping, GitHub dead-drop exfiltration, npm `bypass_2fa` worming, workflow injection, and passwordless sudo modification on GitHub-hosted runners. Treat the actor link as TTP-based until independent public attribution or maintainer forensics confirms the initial access path.

## Tags
- ops
- operations
- supply-chain
- npm
- CI/CD
- GitHub Actions
- credential-theft
- worm
- Miasma
- Mini Shai-Hulud
- Phantom Gyp
- Leo Platform

## Why this matters
- The campaign shows the Miasma / Mini Shai-Hulud payload factory continuing after the June 3 Red Hat / `@redhat-cloud-services` wave, but focused on one package ecosystem instead of many maintainer accounts.
- JFrog's package-context analysis emphasizes the cloud blast radius: Leo / RStreams is used for AWS-native event streaming, Lambda handlers, and serverless data pipelines, so installs may run near AWS credentials, GitHub tokens, npm publishing credentials, and application secrets.
- The `binding.gyp` lane can execute during install without an obvious `scripts` entry in `package.json`; package consumers that only review lifecycle scripts can miss it.
- The payload targets high-blast-radius secrets: GitHub Actions runner memory, cloud metadata and secret stores, package-registry tokens, Vault, Kubernetes, GitHub PATs, and password managers.
- GitHub-based exfiltration through the victim's own token can avoid simple egress-domain allow/block assumptions because no new attacker domain is required.
- Socket's Verana finding shows the campaign moving beyond npm install hooks into source-repository auto-execution: a Go module/source archive carried `.claude/` and `.vscode/` hooks that could execute when a developer opened the repository in trusted IDE or AI-agent tooling.

## Affected packages
StepSecurity lists these malicious package versions, all published at `2026-06-24T23:04:55Z` within a three-second window:

| Package | Malicious version |
| --- | --- |
| `leo-logger` | `1.0.8` |
| `leo-sdk` | `6.0.19` |
| `leo-aws` | `2.0.4` |
| `leo-config` | `1.1.1` |
| `leo-streams` | `2.0.1` |
| `serverless-leo` | `3.0.14` |
| `leo-connector-mongo` | `3.0.8` |
| `serverless-convention` | `2.0.4` |
| `rstreams-metrics` | `2.0.2` |
| `leo-connector-elasticsearch` | `2.0.6` |
| `leo-auth` | `4.0.6` |
| `leo-cache` | `1.0.2` |
| `leo-cli` | `3.0.3` |
| `leo-cron` | `2.0.2` |
| `leo-connector-redshift` | `3.0.6` |
| `leo-connector-oracle` | `2.0.1` |
| `rstreams-shard-util` | `1.0.1` |
| `leo-connector-mysql` | `3.0.3` |
| `leo-cdk-lib` | `0.0.2` |
| `solo-nav` | `1.0.1` |

Socket later added three additional malicious npm package versions published by npm user `llxlr`:

| Package | Malicious version |
| --- | --- |
| `hexo-deployer-wrangler` | `1.0.4` |
| `hexo-shoka-swiper` | `0.1.10` |
| `prism-silq` | `1.0.1` |

Sonatype independently reported the same three `llxlr` packages as additional payload-bearing packages and assigned the campaign advisory `Sonatype-2026-004261`. It also cautioned that three prerelease or release-candidate Leo connector packages included in some early lists — `leo-connector-common@4.0.11-rc`, `leo-connector-postgres@4.0.19-beta`, and `leo-connector-entity-table@3.0.22-rc` — should still be reviewed as surrounding incident activity but did not appear, in Sonatype's current analysis, to carry the confirmed Miasma payload.

## Reported payload behavior
- Install-time execution through a `binding.gyp` native-build expansion: `<!(node index.js > /dev/null 2>&1 && echo stub.c)>`.
- Three-layer JavaScript obfuscation: ROT-N decoding, AES-128-GCM decryption, and obfuscator.io-style output.
- Bun runtime staging from `github.com/oven-sh/bun/releases/download/bun-v1.3.13/`, followed by temporary payload execution under `/tmp/p*.js`.
- GitHub Actions runner memory scraping by locating `Runner.Worker` through `/proc/{pid}/cmdline` and reading `/proc/{pid}/mem` to recover secrets masked from logs or child processes.
- Credential harvesting from AWS, GCP, Azure, Kubernetes, HashiCorp Vault, npm, PyPI, RubyGems, JFrog, GitHub PATs, 1Password, and related developer/CI stores.
- GitHub GraphQL / Contents API dead-drop exfiltration using the victim's own GitHub token to commit encrypted stolen material.
- npm propagation via stolen tokens and the `bypass_2fa` publish path.
- GitHub workflow modification to request `id-token: write` and add attacker-controlled pinned action SHA steps.
- Passwordless sudo modification on GitHub-hosted runners by writing `runner ALL=(ALL) NOPASSWD:ALL`.
- GitHub Actions and repository poisoning markers that overlap adjacent compromises, especially `RevokeAndItGoesKaboom`, `Alright Lets See If This Works`, `TheBeautifulSandsOfTime`, `thebeautifulmarchoftime`, and `thebeautifulsnadsoftime`.
- AI / IDE persistence through Claude, VS Code, Cursor, Gemini, and Copilot-adjacent configuration paths that can trigger after the malicious package version has already been removed.

### JFrog campaign-marker and seeding details
JFrog's June 25 analysis adds two useful hunt pivots for the Leo / RStreams wave:

- The public repository-description marker changed from earlier `Miasma - The Spreading Blight` / `Hades - The End for the Damned` strings to `Alright Lets See If This Works`; JFrog reported 414 GitHub repository-search results for that marker during its investigation.
- The token-relay deterrence string changed to `RevokeAndItGoesKaboom`, replacing earlier `IfYouInvalidateThisTokenItWillNukeTheComputerOfTheOwner`-style phrasing.
- JFrog observed a gated `SEED_PAT` path: the payload checks whether `GITHUB_REPOSITORY` contains `Seeder` before reading `SEED_PAT` and adding that token as a GitHub sender. Treat this as likely operator / test bootstrap logic rather than a normal victim-environment requirement, but hunt for unexpected `SEED_PAT` exposure in release workflows.

## Go / source-repository poisoning expansion
Socket reported a related source archive for `github.com/verana-labs/verana-blockchain@v0.10.1-dev.20` that carried the same Miasma-style payload family without relying on `binding.gyp` or normal Go build logic. The archive contained:

- `.claude/index.js`, a large obfuscated JavaScript payload flagged as high-confidence Miasma-style decode-and-eval malware.
- `.claude/setup.mjs` and `.vscode/setup.mjs` Bun launcher scripts.
- `.claude/settings.json` and `.vscode/tasks.json`, including a VS Code `folderOpen` task that runs `node .claude/setup.mjs`.
- The same broad developer / CI secret collection, EDR checks, GitHub Actions / OIDC abuse, encrypted exfiltration, Bun staging, and AI-tool persistence observed in the npm package wave.

Treat this as source-repository execution risk: a developer who clones or opens a poisoned repository in a trusted IDE or AI coding assistant may trigger the payload even if no malicious npm lifecycle hook runs.

## Indicators and hunt pivots
- Any install, cache entry, lockfile, artifact, or dependency diff containing one of the affected package/version pairs above.
- Affected publish timestamp: `2026-06-24T23:04:55Z` for Leo Platform packages.
- Socket-added npm packages: `hexo-deployer-wrangler@1.0.4`, `hexo-shoka-swiper@0.1.10`, and `prism-silq@1.0.1`.
- Sonatype advisory pivot: `Sonatype-2026-004261`; use it to separate confirmed payload-bearing versions from adjacent prerelease packages that may have appeared in early lists.
- Root-level `binding.gyp` in a package with no real native addon output, especially with `<!(node index.js > /dev/null 2>&1 && echo stub.c)>`.
- `index.js` containing a very large char-code array; StepSecurity reports length `1,566,023` as a campaign fingerprint.
- Bun download or execution during `npm install`, especially `bun-v1.3.13`, `/tmp/p*.js`, or `/tmp/b-*`-style staging.
- `Runner.Worker` memory access through `/proc/<pid>/mem` from a package install context.
- GitHub API commits to unusual repositories shortly after CI package installation, especially encrypted blobs or Miasma-like repository descriptions.
- GitHub repository descriptions containing `Alright Lets See If This Works`, with `RevokeAndItGoesKaboom` as a payload-string pivot if artifacts are available.
- Release or test workflows exposing a variable named `SEED_PAT`, especially when the repository name or owner path contains `Seeder`.
- Workflow diffs that unexpectedly add `id-token: write`, pinned opaque action SHAs, or release/publish steps outside the normal release process.
- sudoers modification containing `runner ALL=(ALL) NOPASSWD:ALL` on GitHub-hosted runners.
- Verana / Go source-archive pivots: `github.com/verana-labs/verana-blockchain@v0.10.1-dev.20`, `.claude/index.js`, `.claude/setup.mjs`, `.vscode/setup.mjs`, `.claude/settings.json`, and `.vscode/tasks.json`.
- Socket-reported SHA256 hashes for the Verana source-repository case include `b3e217f4354e8a4383038b99b0bcaeaff191a79df58e7a1f2355a79aac2faf13` for `verana-blockchain-v0.10.1-dev.20.zip` and `15b415ae41df72acf1f7e9e67569531d41dee62d089d34b4c0fab0c7fe5cc14f` for `.claude/index.js`.

StepSecurity also published SHA1 package hashes for the malicious tarballs. Use the vendor-maintained advisory as the source of truth for full hash matching because registry removals and republished clean versions can change what package managers return over time.

## Response guidance
1. Treat any CI runner or developer host that installed an affected version as compromised.
2. Stop affected workflows and isolate hosts before mass token revocation if the active payload may still be running.
3. Preserve workflow logs, resolved package tarballs, npm cache entries, GitHub audit logs, and runner telemetry before retention windows expire.
4. Rotate reachable GitHub, npm, cloud, Kubernetes, Vault, package-registry, SSH, and password-manager credentials after malicious processes are stopped.
5. Invalidate GitHub Actions caches and rebuild release runners from known-clean images.
6. Audit repositories reachable by affected tokens for unexpected commits, workflow changes, `id-token: write` additions, and GitHub dead-drop artifacts.
7. Add package cooldown controls, registry quarantine for newly published versions, and file-content detections for suspicious `binding.gyp` native-build execution.
8. Extend cleanup from package caches into repositories: audit `.claude/`, `.vscode/`, `.cursor/`, `.gemini/`, `.github/setup.js`, `_index.js`, orphan `snapshot-*` branches, and Dependabot-looking workflow commits reachable by stolen GitHub tokens.

## Attribution notes
StepSecurity states that the Leo Platform operation appears to be the same actor or payload factory behind Miasma because the hook syntax, Bun URL, obfuscation chain, runner-memory theft, GitHub dead-drop exfiltration, and npm worming capability match. Because Mini Shai-Hulud / Miasma source and techniques have been public and copied, track this as **Miasma-style / likely same payload factory** unless later public sources establish a firmer operator attribution.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md)
- [TeamPCP](../actors/teampcp.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/mass-npm-supply-chain-attack-20-leo-platform-packages-compromised
- Socket: https://socket.dev/blog/miasma-mini-shai-hulud-hits-leoplatform-npm-packages-go-ecosystem
- Sonatype: https://www.sonatype.com/blog/miasma-returns-leo-platform-compromise-in-npm
- JFrog Security Research: https://research.jfrog.com/post/shai-hulud-miasma-alright-lets-see-if-this-works/
