# vpmdhaj OpenSearch npm cloud-secret stealer

## Summary
Microsoft Defender Security Research reported a May 28, 2026 npm campaign in which a single newly created maintainer identity, `vpmdhaj`, published 14 malicious typosquat packages that spoofed OpenSearch, Elasticsearch, DevOps, and environment-configuration tooling.

The packages executed during npm install, stole cloud and CI/CD secrets, and used two loader generations: an HTTP C2 downloader and a quieter Bun-runtime loader that executed a bundled second-stage payload from inside the npm tarball.

## Tags
- ops
- operations
- supply-chain
- npm
- typosquatting
- OpenSearch
- Elasticsearch
- credential-theft
- cloud secrets
- CI/CD
- AWS
- HashiCorp Vault
- Bun runtime abuse

## Why this matters
- The package names and metadata were tuned for developers likely to manage search clusters, cloud infrastructure, and CI/CD environments.
- The second-stage payload targeted AWS credentials, ECS and EC2 metadata, Secrets Manager, HashiCorp Vault tokens, GitHub Actions context, and npm publish tokens.
- Stolen npm publish tokens create a direct path from one accidental install to downstream package compromise.
- The newer loader reduced install-time network visibility by downloading the legitimate Bun runtime from GitHub Releases and running a pre-bundled payload already present in the malicious package.

## Reported campaign
- **Date:** May 28, 2026.
- **Maintainer alias:** `vpmdhaj`.
- **Email reported by Microsoft:** `a39155771@gmail[.]com`.
- **Scale:** 14 malicious npm packages published within roughly four hours.
- **Theme:** OpenSearch, Elasticsearch, DevOps, and environment-configuration package names.
- **Registry response:** Microsoft says it reported the activity to npm and the packages / users were taken down.

## Package set
Microsoft listed the following packages:

- `@vpmdhaj/devops-tools`
- `@vpmdhaj/elastic-helper`
- `@vpmdhaj/opensearch-setup`
- `@vpmdhaj/search-setup`
- `app-config-utility`
- `elastic-opensearch-helper`
- `env-config-manager`
- `opensearch-config-utility`
- `opensearch-security-scanner`
- `opensearch-setup`
- `opensearch-setup-tool`
- `search-cluster-setup`
- `search-engine-setup`
- `vpmdhaj-opensearch-setup`

The unscoped packages spoofed legitimate `github.com/opensearch-project/opensearch-js` metadata through `homepage`, `repository`, and `bugs` fields, and used inflated version numbers such as `1.0.7265`, `1.0.9108`, and `2.1.9201` to look mature.

## Payload chain
### Gen-1 loader
1. A `preinstall` hook runs `preinstall.js` during package installation.
2. The script collects host context including hostname, platform, architecture, Node version, user, current working directory, package name, and package version.
3. It base64-encodes that context and sends it to actor C2 with an `X-Supply: 1` header.
4. The C2 returns a gunzip-compressed second-stage binary.
5. The loader writes the payload as `payload.bin`, marks it executable, and spawns it detached.
6. `index.js` can relaunch the same `payload.bin` when the module is later required.

### Gen-2 loader
1. Newer versions replace the install-time C2 fetch with `setup.mjs`.
2. The loader checks for Bun locally; if absent, it downloads legitimate Bun `v1.3.13` from GitHub Releases for the host OS and architecture.
3. It extracts Bun using platform-native extraction or a bundled parser.
4. Bun runs a bundled second-stage script such as `opensearch_init.js` or `ai_init.js` that shipped inside the npm tarball.

## Credential theft focus
Microsoft describes the bundled second stage as a roughly 195 KB Bun-compiled JavaScript credential harvester. Reported target areas include:

- **AWS:** environment credentials, EC2 IMDSv2 at `169.254.169[.]254`, ECS task-role metadata at `169.254.170[.]2`, STS caller identity / role assumption, and Secrets Manager enumeration across 16+ regions.
- **HashiCorp Vault:** `VAULT_TOKEN` and `VAULT_AUTH_TOKEN` environment variables.
- **npm:** token validation through `/-/whoami` and publish-access discovery through `/-/npm/v1/tokens`.
- **GitHub Actions / CI:** repository and runner context such as `GITHUB_REPOSITORY` and `RUNNER_OS`, plus CI-behavior manipulation including resetting `CI=false` and using `__DAEMONIZED=1` to avoid re-entry.

## Defender heuristics
- Search dependency manifests, package-manager caches, artifact mirrors, proxy logs, and CI install logs for the 14 package names above.
- Treat installation as a cloud and CI/CD credential exposure event; rotate AWS, Vault, npm, GitHub, and deployment secrets available to the process at install time.
- Review egress for `X-Supply: 1` during npm install, unexpected payload downloads followed by detached execution, and GitHub Release downloads of Bun immediately triggered by package lifecycle scripts.
- Alert on package installs that fetch and execute runtimes such as Bun from lifecycle hooks, especially for packages whose domain should not require runtime bootstrapping.
- Monitor npm publish-token use after exposure; stolen publish tokens may be used to push malicious versions to unrelated packages controlled by the victim identity.
- Do not rely on provenance or repository metadata alone when packages spoof legitimate project URLs; compare publisher identity, package age, and release history against the upstream project.

## Related pages
- [oob.moika.tech dependency-confusion environment stealer](oob-moika-dependency-confusion-env-stealer.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [SANDWORM_MODE AI-toolchain npm worm](sandworm-mode-ai-toolchain-worm.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/05/28/typosquatted-npm-packages-used-steal-cloud-ci-cd-secrets/>
- The Hacker News roundup: <https://thehackernews.com/2026/05/malicious-sicoob-nuget-steals-banking.html>
