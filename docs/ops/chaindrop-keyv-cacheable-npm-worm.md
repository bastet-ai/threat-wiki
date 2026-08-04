# ChainDrop keyv / cacheable npm worm

## Summary
On August 4, 2026, StepSecurity, Socket, Aikido, Snyk, JFrog, and SafeDep reported a fast-moving npm supply-chain worm affecting `keyv`, the `cacheable` package family, and packages reachable through stolen maintainer identities. StepSecurity named the activity **ChainDrop**. Aikido and JFrog described it as Shai-Hulud activity; Socket assessed that its tradecraft closely matches Shai-Hulud but did not recover a self-identifying campaign marker from the analyzed payload.

The malicious releases add an npm `preinstall` hook, download Bun `1.3.13`, run a heavily obfuscated second stage, harvest developer, CI/CD, cloud, package-registry, Vault, and Kubernetes credentials, and use stolen npm access or OIDC trusted publishing to republish trojanized packages. Socket also reported GitHub and DNS exfiltration plus `.claude` and `.vscode` repository hooks that can execute when source is opened without requiring `npm install`.

This is an **active incident**. SafeDep's later August 4 snapshot counted **2,234 poisoned versions across 444 package names and 12 organizations**, 22 more versions than StepSecurity's 18:10 UTC snapshot while leaving the package-name count unchanged. Counts and registry state can change; use the linked vendor-maintained lists for live scoping.

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
- Ethereum
- EtherHiding
- remote-access
- persistence

## Why this matters
- StepSecurity's 18:10 UTC revision reported **444 package names and 2,212 compromised versions** observed between 09:40 and 13:20 UTC. Aikido separately reported at least **1,280 compromised packages** in an earlier update. The difference reflects changing collection windows and package classification during an active incident; neither count should be treated as final.
- StepSecurity separated **11 full worm carriers** in the Jared Wray ecosystem from **433 propagated package names covering 2,201 versions**. This distinction matters: the first group carried the complete propagation logic, while the second wave was republished through credentials harvested from at least a dozen unrelated organizations.
- The initial package family sits deep in common dependency trees. Public reporting identifies `keyv`, `cacheable-request`, `flat-cache`, `file-entry-cache`, and related caching packages used transitively by developer tooling.
- Aikido says malicious source changes were pushed to the legitimate repository and released through GitHub Actions, so affected packages could carry valid provenance. Provenance proved which workflow built the artifact, not that the source or maintainer identity was clean.
- The payload turns credential theft into automated package propagation and adds source-repository execution paths for IDEs and AI coding agents.
- By StepSecurity's 18:10 UTC update, npm had reverted all 11 full worm carriers to safe versions. Cleanup of the propagated wave was incomplete: `@servicetitan/*` and `@nebula.js/*` removals were underway, clean replacements existed for `@thiennq/docs-viewer` and `@onereach/ui-components`, and two reported malicious releases still held the `latest` tag. Registry cleanup does not remove copies already pinned in lockfiles, mirrors, caches, or artifacts.
- StepSecurity found real execution in ten public `backstage/backstage` CI runs between 09:31 and 10:40 UTC. Fresh E2E scaffolding resolved a compromised transitive dependency outside the repository's committed lockfile; Bun then contacted Ethereum RPC services and `npm-cache.com`. StepSecurity found no evidence of long-lived credential loss in those runs because the affected workflows referenced no repository secrets, but the payload did execute and reach C2.
- Snyk independently fetched and compared the maintainer-linked tarballs without installing them, confirmed the same 11 full-carrier releases, and published malicious-code advisory `SNYK-JS-KEYV-18515941` for `keyv@6.0.0`. Its registry sweep also found that the other `@keyv/*` packages published before the payload commit did not carry the malicious lifecycle hook, preventing an overbroad all-`@keyv` assessment.
- SafeDep's later registry reconstruction counted 2,234 poisoned versions under the same 444 package names across 12 organizations between 09:35 and 13:18 UTC. It found that 80% of affected names carried more than one poisoned release and 43 names carried at least 11, making package-name, lifecycle-hook, and payload-hash checks more durable than relying on an early version list.
- SafeDep found the same 727,680-byte payload across the initial `keyv`/`cacheable`, `@hubsync`, and `@ornikar` publisher clusters, but two loader builds and different publication paths. The initial family retained valid OIDC/SLSA provenance, while the latter clusters used direct npm identities without provenance. One campaign therefore crossed both source/CI compromise and stolen-token publication paths.
- JFrog independently recovered repository-infection and GitHub Actions secret-harvesting detail, including branch and workflow artifacts plus file hashes defenders can hunt independently of the package list.

## Confidence and attribution
- The compromise and malicious package behavior are corroborated by StepSecurity, Socket, Aikido, Snyk, JFrog, and SafeDep.
- Aikido labels the wave active Shai-Hulud activity. Socket says the behavior closely matches Shai-Hulud: TruffleHog-style secret collection, maintainer-package enumeration, npm token and OIDC publication, and victim-account GitHub repositories.
- Socket did **not** recover the campaign's self-identifying repository or commit markers because relevant strings were assembled at runtime. Public Shai-Hulud-derived tooling also makes copycat reuse possible. Track ChainDrop as a Shai-Hulud-lineage assessment, not confirmed TeamPCP attribution.
- StepSecurity assesses the payload as a direct, heavily evolved descendant of Shai-Hulud 2.0 based on Bun/preinstall delivery, `Runner.Worker` memory scraping, npm self-republication, and GitHub exfiltration. Its Russian-locale kill switch is an operator-language clue, not sufficient actor or nationality attribution.
- Socket and Aikido identify compromise of the `Jaredwray` maintainer/GitHub account as the initial high-impact access path. Maintainer and registry postmortems were not yet public at capture time.
- JFrog treats the `Shai-Hulud: Here We Go Again` dead-drop description as a self-identifying campaign marker. That supports Shai-Hulud lineage, but a reusable public marker still does not establish TeamPCP operator identity.

## Reported execution chain
1. The attacker publishes a new package version containing `setup.mjs`, `Math_Symbol.js` (also referenced internally as `math_init.js`), and `"preinstall": "node setup.mjs"`.
2. `setup.mjs` detects platform and architecture, including Alpine/musl, and obtains a platform-specific Bun `1.3.13` runtime from the legitimate `oven-sh/bun` GitHub Releases path when Bun is absent.
3. The loader extracts Bun with system `unzip`, PowerShell `Expand-Archive`, or a JavaScript ZIP fallback, then executes the second stage under Bun.
4. Socket describes the second stage as a roughly 728 KB bundle with polymorphic basE91-protected strings and internal modules tagged `[collector]`, `[dispatcher]`, `[provenance]`, and `[publish]`.
5. The collector reads local credentials, environment variables, cloud metadata, managed secret stores, runner identity material, and generic token/private-key patterns.
6. The worm calls npm identity and search endpoints, discovers packages reachable by the stolen maintainer identity, downloads clean tarballs, injects its files and lifecycle hook, bumps versions, recomputes integrity metadata, and republishes.
7. Where trusted publishing is available, it attempts npm's OIDC token-exchange endpoint. A poisoned source tree can therefore produce a valid npm/Sigstore provenance attestation.
8. Socket reports encrypted findings sent through attacker-created GitHub repositories and a separate DNS channel. StepSecurity further observed `results-*.json` staging repositories and a GitHub-token monitor that creates a delayed execution path when defenders revoke the stolen token.
9. The source repository can receive `.claude/settings.json` `SessionStart` hooks and `.vscode/tasks.json` `folderOpen` tasks that rerun the loader when a developer or coding agent opens a clone.
10. StepSecurity reports that the payload resolves command-and-control domains from an Ethereum mainnet contract, falls back to signed-commit searches on GitHub, and sends encrypted data to `/router`. A response containing a `code` field is passed to `eval`, making the channel bidirectional remote access rather than exfiltration only.

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
| `file-entry-cache` | `11.1.6` |

StepSecurity's early list also included packages in `@arv-bedrock`, `@deliveroo`, `@hubsync`, `@onereach`, `@or-sdk`, `@ornikar`, `@picsart`, `@qlik`, and `@servicetitan` scopes, plus `ecto`, `pob-test-typescript-package-in-monorepo`, and `tslint-folder-schema`. Aikido reported rapid spread into additional maintainers and organizations. Do not treat this table as complete.

### StepSecurity scope update — 13:20 UTC

StepSecurity's updated incident snapshot counted 444 package names and 2,212 malicious versions during the 09:40–13:20 UTC observation window. Eleven Jared Wray ecosystem packages were full carriers; the worm republished 433 additional package names and 2,201 versions through credentials belonging to at least a dozen unrelated organizations. Many historical versions were replayed, so the version count is not a victim or execution count. Scope exposure from lockfiles and caches separately from confirmed execution of the `preinstall` hook.

### StepSecurity technical update — 15:13 UTC

The expanded analysis places the first poisoned `keyv` commit (`ee2681a`) at 09:02:37 UTC and the repository-hook commit (`d8c850c`) at 09:04:30. `keyv@6.0.0` was then published at 09:35 through GitHub Actions workflow run `30896232272` with a valid trusted-publishing attestation. StepSecurity observed the automated second wave beginning at 09:38:13 and continuing through 11:44.

The payload also:

- exits when `LANG` indicates a Russian locale and otherwise respawns detached outside GitHub Actions;
- writes a camouflaged `<tmpdir>/tmp.dpkg_<pid>.lock` state file;
- creates `results-*.json` exfiltration commits under victim identities;
- installs `~/.local/bin/gh-token-monitor.sh` with a user service or macOS LaunchAgent, polls `api.github.com/user` every 60 seconds for 24 hours, and executes an attacker-supplied handler after token revocation;
- resolves C2 through Ethereum and sends a gzip, AES-256-GCM, RSA-OAEP-SHA256, and base64 envelope that StepSecurity says it intercepted and decrypted in its sandbox.

### StepSecurity containment update — 18:10 UTC

StepSecurity reported that npm's rolling response began with removal of `cacheable-request@13.0.20` at 10:39 UTC and a `keyv` dist-tag rollback to `5.6.0` around 11:15. By 18:10, all 11 full carriers had been reverted to safe versions. The response was still incomplete across the worm-propagated package set:

- `@servicetitan/*` and `@nebula.js/*` packages were being removed wholesale;
- clean releases were available for `@thiennq/docs-viewer@1.6.4` and `@onereach/ui-components@27.0.4`;
- `@picsart/ai-sdk@3.32.2` and `@deliveroo/reevent@1.0.1` reportedly remained on `latest` at the capture time; and
- the compromised maintainer account and three initially affected GitHub repositories were no longer available, limiting access to the original issue and commit history.

Treat these as a time-bounded response snapshot, not a final registry inventory. Continue using vendor-maintained affected-version lists and inspect internal registry proxies, package caches, lockfiles, and built artifacts even after public removal or dist-tag rollback.

### Confirmed public CI execution — Backstage

StepSecurity searched roughly 44,000 public workflow runs from an eight-hour window for connections to `npm-cache.com`. Excluding five runs in its own detonation repository, it found ten matching runs in `backstage/backstage`. In the affected E2E jobs, fresh application scaffolding installed current dependencies outside the project's committed lockfile. The resulting Bun process contacted `eth.llamarpc.com`, `go.getblock.io`, `eth-mainnet.nodereal.io`, and then `npm-cache.com` in the same sequence observed in StepSecurity's detonation.

The runs occurred across Renovate pull requests, pushes to `master`, and changeset branches between 09:31 and 10:40 UTC. StepSecurity reported the finding to Backstage as issue `backstage/backstage#35100`. It found no evidence of long-lived credential loss: the two affected workflow definitions referenced no repository secrets, the only job credential was an ephemeral `GITHUB_TOKEN`, and the older audit-mode agent did not record a `Runner.Worker` memory-read event. This is confirmed payload execution and C2 reachability, not confirmed credential theft.

The case demonstrates a lockfile boundary: a committed application lockfile does not constrain jobs that scaffold a new project or otherwise resolve fresh dependencies during testing.

### Snyk independent tarball validation

Snyk queried npm for 61 package names associated with maintainer `jaredwray`, checked August 4 releases, and independently confirmed the 11 full-carrier versions listed above. It found `ecto@5.0.1` particularly important for scoping because it appeared after the first public warnings, while the other `@keyv/*` version 6 packages published between 09:30 and 09:32 predated the payload and did not contain the malicious hook.

Its file-by-file comparison of `keyv@6.0.0` against `keyv@6.0.0-rc.1` found the compiled `dist/` tree unchanged. The material differences were the stable version metadata, `setup.mjs`, `Math_Symbol.js`, and the `preinstall` hook. Snyk calculated SHA-256 `d584f9b6af48b7ed1f93713944f033783bf149e1c25e1643eb8c0e9df5dc7782` for the `keyv@6.0.0` tarball and independently reproduced the two payload hashes below.

Snyk also clarified the commit-verification boundary. The initial poisoned release commits were reported as unsigned, while repository-hook commit `d8c850c7` was GitHub-verified and used `github-actions[bot]` identity. A verified commit badge proves how GitHub signed that commit object; it does not prove the project authorized the change. Snyk did not execute or independently decrypt the second stage, so detailed second-stage capabilities remain grounded in the runtime and malware analyses cited above rather than in Snyk's static validation.

### JFrog and SafeDep scope and infrastructure follow-up

SafeDep reconstructed 2,234 poisoned versions across 444 package names and 12 unrelated organizations between 09:35 and 13:18 UTC. This is 22 versions above StepSecurity's 18:10 snapshot but does not increase the package-name count. SafeDep reported 537 poisoned versions across 47 `@ornikar/*` and related names, 27 consecutive poisoned `@hubsync/web-sdk-react` releases, and continued republishing after initial public warnings. These are registry-observation counts, not confirmed installations or victims.

The same 727,680-byte stage-two payload, SHA-256 `9fc2570b7cef51c1b8df116d144d11ff4096357be7d2c4c6367cfc2509cf1bcc`, appeared under different filenames across three publisher clusters. SafeDep separated two loaders: the 29,918-byte `54dc7ea5…` build in the initial `keyv`/`cacheable` family and the 11,017-byte `fd3ca400…` build in `@hubsync`, `@ornikar`, and the repository's IDE hooks. The initial family published through a valid trusted-publisher workflow; the other two clusters lacked provenance and used direct npm identities. This demonstrates that one payload family can arrive through both compromised source/CI and stolen registry tokens.

SafeDep also verified that the earlier `@keyv/*` storage-adapter releases were clean as published, agreeing with Snyk's narrower scoping. It warned that a later repository commit staged the malicious files across 19 workspaces even though only core `keyv` had shipped the hook, so responders should distinguish published tarballs from compromised source awaiting a possible release.

Registry state remained uneven. SafeDep reported the initial `keyv`/`cacheable` family largely unpublished or rolled back, while many `@hubsync` and `@ornikar` names still resolved `latest` to poisoned releases. Its statement that there was “no C2 host” is narrower than, and conflicts with, StepSecurity and JFrog's dynamic-HTTPS analysis: JFrog independently documented the Ethereum contract, selector, and `/router` path. Treat SafeDep's finding as **no plaintext embedded host** in its analyzed material, not evidence that the Ethereum-resolved HTTPS channel was absent.

JFrog added hashes for the planted repository and workflow artifacts and reported that the worm can target up to 50 writable branches per repository, skipping `dependabot/*` and `copilot/*`. It described a separate `dependabot/github_actions/format/setup-formatter` branch containing `.github/workflows/codeql_analysis.yml`, which writes the secrets context to `format-results.txt` and uploads it as an artifact. These artifacts should be hunted even where package-install evidence is absent.

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
- `~/.local/bin/gh-token-monitor.sh` and unexpected associated user-level systemd service or macOS LaunchAgent
- temporary files matching `tmp.dpkg_<pid>.lock`
- victim-account repositories or commits containing `results-*.json`
- `~/.config/gh-token-monitor/`, `~/.config/systemd/user/gh-token-monitor.service`, or `~/Library/LaunchAgents/com.user.gh-token-monitor.plist`
- unexpected GitHub Actions workflow named `Run Copilot`, artifact named `format-results`, or workflow content that writes `${{ toJSON(secrets) }}` to `format-results.txt`
- branch `dependabot/github_actions/format/setup-formatter`, workflow `.github/workflows/codeql_analysis.yml`, output `format-results.txt`, commit message `Add CodeQL Analysis`, or forged `github-advanced-security[bot]` identity
- repository commits `ee2681a9b62f3637b0eb5133c36c864d3376cc5b` (payload), `d8c850c7800e…` (IDE/agent hooks), `f97eabcdd057105f1fce3f05d6c029dac3f2ac78` (evidence removal), and `174f6a55690b0812a69adef47260ba8714a9be48` (sibling staging)

### SHA-256
- `d584f9b6af48b7ed1f93713944f033783bf149e1c25e1643eb8c0e9df5dc7782` — `keyv@6.0.0` npm tarball, independently calculated by Snyk
- `fd3ca4007b225fdf8de7af4345a19179d5efa8c4bb9205f88cda806e5684b1eb` — `setup.mjs`
- `54dc7ea54a1317cca0e890a2770630cf7fa6c97813e0cb9d2caa93012b350668` — `setup.mjs` tarball variant
- `9fc2570b7cef51c1b8df116d144d11ff4096357be7d2c4c6367cfc2509cf1bcc` — `math_init.js` / `Math_Symbol.js`
- `927387d0cfac1118df4b383decc2ea6ba49c9d2f98b47098bcbcba1efc026e1f` — planted `.vscode/tasks.json`, per JFrog
- `14eb4ce01dd4307759887ff819359b70d7d9ff709ecde039a5abc1aac325b128` — planted `.claude/settings.json`, per JFrog
- `3f3f42d072bd36860ab7bd7fb5e10ac0d22c741c13c89505ccd6ec0ea572eea7` — injected GitHub Actions workflow, per JFrog
- `29ac906c8bd801dfe1cb39596197df49f80fff2270b3e7fbab52278c24e4f1a7` — runner-memory scraper, per JFrog

### Network and control-plane behavior
- `github[.]com/oven-sh/bun/releases/download/bun-v1.3.13/` — legitimate Bun distribution path; validate package-install process ancestry rather than blocking blindly
- `169[.]254[.]169[.]254` and `169[.]254[.]170[.]2` metadata access from developer or build processes
- `registry[.]npmjs[.]org/-/whoami`
- `registry[.]npmjs[.]org/-/npm/v1/tokens`
- `registry[.]npmjs[.]org/-/npm/v1/oidc/token/exchange/package/`
- GitHub API `POST /user/repos`, GraphQL `createCommitOnBranch`, newly created repositories, and commits from developer or CI identities
- anomalous DNS exfiltration from package-install or Bun processes
- Ethereum mainnet contract `0xE1f2395ee43e45A1556EC6438a88c31B83493103`, queried with `eth_call` selector `0x53ed5143`
- GitHub commit-search strings `thebeautifulmarchoftime` and `IfYouBlockThisAPIKeyItWillCrashTheLiveProductionServersOfAllThirdPartyClients`
- `npm-cache[.]com` — C2 domain observed by StepSecurity; investigate `GET /router` health checks returning HTTP 400/404 and encrypted `POST /router` traffic

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
3. Before revoking the stolen GitHub token, contain the host and remove the token-monitor persistence described above; StepSecurity reports that token revocation can trigger an attacker-supplied handler. Then revoke and replace npm, GitHub, cloud, Vault, Kubernetes, SSH, CI, and application secrets; do not rotate only npm tokens.
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
- Final affected package/version and download scope after npm containment; SafeDep's later August 4 snapshot is 444 packages and 2,234 versions across 12 organizations.
- Initial access and whether the `Jaredwray` account, endpoint, token, GitHub session, or another upstream identity was first compromised.
- Registry and GitHub containment actions, malicious-version removal times, and credential invalidation scope.
- Names, visibility, and recoverable indicators for attacker-created GitHub exfiltration repositories and the DNS channel.
- Current values and transaction history of the Ethereum C2 contract, replacement domains, and signed-commit fallback infrastructure.
- Whether ChainDrop is operated by TeamPCP, another Shai-Hulud-lineage actor, or a copycat using leaked tooling.
- Confirmed victim execution and downstream cloud/repository compromise beyond package publication.
- Final disposition of propagated releases, including the `@picsart`, `@deliveroo`, `@servicetitan`, and `@nebula.js` scopes, and whether clean restoration preserved or replaced package names.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [TeamPCP](../actors/teampcp.md)
- [Developer-tool configuration auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- StepSecurity: [ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum dead-drop C2](https://www.stepsecurity.io/blog/chaindrop-npm-worm)
- Snyk: [Inside the keyv npm Compromise: preinstall Malware, Trusted Provenance, and IDE Hooks](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/)
- JFrog Security Research: [Major Shai Hulud campaign strikes npm again, affecting keyv and 400+ packages](https://research.jfrog.com/post/shai-hulud-is-back-august/)
- SafeDep: [npm Worm Poisons keyv, cacheable and 400+ Other Packages Across Twelve Organisations](https://safedep.io/keyv-npm-supply-chain-compromise/)
- Socket: [Popular npm Packages in the keyv and Cacheable Namespaces Compromised in Active Supply Chain Attack](https://socket.dev/blog/popular-npm-packages-in-the-keyv-and-cacheable-namespaces-compromised-in-active-supply-chain)
- Aikido Security: [Keyv and friends compromised in active Shai-Hulud supply chain attack](https://www.aikido.dev/blog/keyv-and-friends-compromised-in-npm-supply-chain-attack)
