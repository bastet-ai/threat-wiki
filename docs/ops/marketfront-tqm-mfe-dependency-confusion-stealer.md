# @marketfront / @tqm-mfe dependency-confusion stealer

## Summary
SafeDep reported a July 1, 2026 continuation of the `oob.moika.tech`-style dependency-confusion activity: npm user `marketfront` batch-published 25 `@marketfront/*` packages at version `7.0.0`, and npm user `t.tqm.mfe` published `@tqm-mfe/main` at versions `5.4.7` and `5.5.0` earlier the same day.

The packages reused the campaign's durable lure string, `Internal package — Platform Engineering Team`, but the payload had evolved from broad `process.env` collection into an install-time credential-file harvester. Treat any developer workstation or CI runner that installed one of these packages as credential-compromised.

## Tags
- ops
- operations
- supply-chain
- npm
- dependency confusion
- credential-theft
- cloud secrets
- postinstall
- developer-targeting
- CI/CD
- SafeDep
- X-Secret
- RC4
- obfuscator.io
- private registry fallback
- @marketfront
- @tqm-mfe

## Why this matters
- The packages look like internal frontend and platform-engineering modules, not generic typo packages. This is the exact failure mode of public-registry fallback when private scopes are not pinned to a private registry.
- The actor kept a stable lure marker across multiple waves while rotating accounts, scopes, version schemes, cover stories, and payload behavior.
- SafeDep reports that the July wave steals credential files directly: SSH, AWS, Kubernetes, Docker, npm, netrc, PostgreSQL, Git credentials, `.env`, and shell history.
- Versioning moved from obvious anomaly values such as `99.99.99` in earlier waves to more normal-looking versions such as `7.0.0`, `7.1.0`, `7.2.0`, `5.4.7`, and `5.5.0`.
- The source did not recover or publish a C2 host; defenders should not wait for a domain IOC before triaging installs.

## Reported campaign
- **Publishing date:** July 1, 2026.
- **Primary scope:** `@marketfront`, created and populated in one burst around `2026-07-01T22:59:33Z`.
- **Primary publisher:** npm user `marketfront`.
- **Primary versions:** 25 packages at `7.0.0`.
- **Sibling scope:** `@tqm-mfe/main`, published by npm user `t.tqm.mfe` at `5.4.7` and then `5.5.0` around `2026-07-01T17:12:57Z`.
- **Durable lure marker:** `Internal package — Platform Engineering Team`.
- **Install hook:** `postinstall: node scripts/postinstall.js`.
- **Payload shape:** single-line `obfuscator.io`-style JavaScript around 182 KB, with sensitive strings hidden behind RC4 plus XOR.
- **Exfil behavior:** gzip-compressed HTTPS POST to `/api/v1/events` with a custom `X-Secret` header, plus DNS resolver beaconing.

## Package set
All reported `@marketfront` packages were version `7.0.0` and carried the credential harvester.

| Package | Version | Publisher |
| --- | --- | --- |
| `@marketfront/actualordersnippetpopup` | `7.0.0` | `marketfront` |
| `@marketfront/advertisingdevtool` | `7.0.0` | `marketfront` |
| `@marketfront/bannerpopup` | `7.0.0` | `marketfront` |
| `@marketfront/baobabtech` | `7.0.0` | `marketfront` |
| `@marketfront/basemarkettemplate` | `7.0.0` | `marketfront` |
| `@marketfront/blenderdevtool` | `7.0.0` | `marketfront` |
| `@marketfront/captchaservice` | `7.0.0` | `marketfront` |
| `@marketfront/changefilter` | `7.0.0` | `marketfront` |
| `@marketfront/commonecommerce` | `7.0.0` | `marketfront` |
| `@marketfront/customdealsfeed` | `7.0.0` | `marketfront` |
| `@marketfront/designsystemdevtool` | `7.0.0` | `marketfront` |
| `@marketfront/devtoolsloader` | `7.0.0` | `marketfront` |
| `@marketfront/digitalherobannercarousel` | `7.0.0` | `marketfront` |
| `@marketfront/dynamicpageparams` | `7.0.0` | `marketfront` |
| `@marketfront/errorcounter` | `7.0.0` | `marketfront` |
| `@marketfront/fashiononboardingpopup` | `7.0.0` | `marketfront` |
| `@marketfront/fingerprint` | `7.0.0` | `marketfront` |
| `@marketfront/footer` | `7.0.0` | `marketfront` |
| `@marketfront/gotoauthpopup` | `7.0.0` | `marketfront` |
| `@marketfront/header` | `7.0.0` | `marketfront` |
| `@marketfront/infopopup` | `7.0.0` | `marketfront` |
| `@marketfront/livestreampreviewpopup` | `7.0.0` | `marketfront` |
| `@marketfront/madvpopup` | `7.0.0` | `marketfront` |
| `@marketfront/mychatspreloader` | `7.0.0` | `marketfront` |
| `@marketfront/navbar` | `7.0.0` | `marketfront` |
| `@tqm-mfe/main` | `5.4.7`, `5.5.0` | `t.tqm.mfe` |

## Credential-access behavior
SafeDep reports the payload reads roughly 20 local credential and secret locations, including:

- `~/.ssh`
- `~/.aws/credentials`
- `~/.kube/config`
- `~/.docker/config.json`
- `~/.npmrc`
- `~/.netrc`
- `~/.pgpass`
- `~/.git-credentials`
- `~/.env`
- shell history files

The collected material is compressed and posted to `/api/v1/events` with an `X-Secret` header. SafeDep did not publish a resolved C2 hostname because the host was hidden behind RC4 plus XOR and was not recovered without executing the payload.

## Relationship to earlier waves
SafeDep ties the July `@marketfront` / `@tqm-mfe` activity to the dependency-confusion template previously seen across `mr.4nd3r50n`, `pik-libs`, `t-in-one`, and `emcd-vue` accounts and documented in the `oob.moika.tech` campaign. The reusable marker is the README line `Internal package — Platform Engineering Team`, often paired with scope-parameterized decoy domains such as `github.<scope>.io`, `jira.<scope>.io`, `docs.<scope>.io`, and an internal-registry instruction.

The actor changed the payload underneath that marker:

1. Early packages used conspicuous `99.99.99`-style versions and broad environment-variable collection.
2. Microsoft reported overlapping waves with shared `X-Secret` header conventions and reconnaissance-first profiling.
3. The July SafeDep wave uses normal-looking release numbers and credential-file harvesting.
4. SafeDep observed the still-live predecessor scope `@emcd-vue` republished at `7.1.0` / `7.2.0`, preserving the template while the removed `@marketfront` pages returned 404.

## Defender heuristics
### Exposure triage
- Search lockfiles, SBOMs, npm caches, CI logs, private-registry mirrors, and artifact build logs for every package and version listed above.
- Treat any install as host compromise. Rotate SSH keys, npm tokens, Git credentials, AWS credentials, Kubernetes configs, Docker registry credentials, database secrets, and any secrets present in `.env` or shell history.
- Review developer workstations and CI runners, not just production systems. The campaign is optimized for dependency resolution during builds and local development.

### Package-manager controls
- Scope-lock every private npm namespace to an internal registry in `.npmrc`; do not allow public npm fallback for internal scopes.
- Add deny rules for public packages that claim internal platform-engineering scopes, especially when the package is new, has zero or low downloads, and carries a lifecycle hook.
- Flag `postinstall: node scripts/postinstall.js` when paired with a very large single-line obfuscated script and a trivial `dist/index.js` that re-exports absent source.

### Detection pivots
- Hunt package metadata where the `author` ends in `Platform Engineering` and package links point to `github.<scope>.io`, `jira.<scope>.io`, or `docs.<scope>.io`.
- Hunt install-time outbound HTTPS POSTs to `/api/v1/events` carrying an `X-Secret` header.
- Hunt DNS resolver activity during `npm install` windows from developer endpoints or CI runners.
- Preserve package tarballs and npm cache artifacts before cleanup; registry pages for pulled packages may already return 404.

## Related pages
- [oob.moika.tech dependency-confusion environment stealer](oob-moika-dependency-confusion-env-stealer.md)
- [wshu.net npm credential-stealer campaign](wshu-net-npm-credential-stealer-campaign.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- [SafeDep](https://safedep.io/marketfront-dependency-confusion-campaign)
- [Microsoft](https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/)
