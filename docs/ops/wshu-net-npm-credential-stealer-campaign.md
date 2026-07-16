# wshu.net npm credential-stealer campaign

## Summary
SafeDep reported a June 2026 npm campaign that used 15 plausible utility packages across 13 throwaway scopes to deliver a cross-platform Rust infostealer. The actor published most packages on June 4, 2026 in a roughly 40-minute burst, then expanded version ranges over the next two weeks for a total of 64 malicious or related versions.

Treat any developer workstation or CI runner that installed one of the payload versions as compromised. SafeDep reports that the packages execute an obfuscated JavaScript downloader through `postinstall`; two packages also trigger from runtime imports, which means `npm install --ignore-scripts` is not complete protection once application code calls the poisoned library.

## Tags
- ops
- operations
- supply-chain
- npm
- JavaScript
- Rust
- credential-theft
- infostealer
- postinstall
- runtime execution
- developer-targeting
- crypto wallets
- cloud credentials
- Telegram C2
- persistence

## Why this matters
- The campaign is not a single typosquat. It is a templated multi-scope operation with one publisher pattern, shared obfuscation fingerprints, and utility-shaped package names.
- The malicious versions are often not the current `latest` version. The actor published scrubbed follow-up releases so quick `npm view` / latest-only review can look clean while pinned or cached versions remain dangerous.
- The second-stage binary targets developer and cloud control material: crypto wallets, browser stores, AWS / GCP / Azure / Kubernetes credentials, SSH keys, Discord / Telegram sessions, npm / GitHub / PyPI tokens, `.env` files, `.npmrc`, and database client connection strings.
- Runtime triggers in `@petitcode/eb-retry` and `@briskforge/envcheck` preserve an execution path after install scripts are skipped.
- The persistence path lands in user-owned Linux locations, so developer endpoints without root access can still retain the stealer.

## Reported chain
1. On June 4, 2026, one actor created or used npm accounts with publisher emails following `<scope>-<six random characters>@wshu[.]net`. SafeDep notes that `wshu.net` is a public disposable-email provider, so the domain is a pivot when paired with the scope burst, obfuscation, and delivery account rather than a standalone attribution signal.
2. The packages presented as small developer utilities: JWT helpers, retry wrappers, loggers, date helpers, validators, and parsing utilities.
3. Payload versions declared `postinstall` hooks such as `node dist/prelude.cjs`, `node lib/warmup.js`, `node lib/preflight.js`, `node dist/bootstrap.js`, or similar package-local bootstrap files.
4. Each bootstrap file contained a roughly 260-282 KB obfuscated JavaScript blob that SafeDep describes as the largest file in the package and much larger than the legitimate decoy utility code.
5. The obfuscated JavaScript spawned a detached child process behind environment guards, downloaded a roughly 10.6 MB Rust-compiled binary from a GitHub Releases path, and executed it.
6. SafeDep, citing Amazon Inspector's dynamic analysis, reports the removed delivery path as `github[.]com/angelmaybeth21-oss/test/releases/download/v1.0.0/{linux,mac,win.js}`. The GitHub account `angelmaybeth21-oss` was created on June 3, 2026, one day before the npm burst.
7. The Rust binary swept wallet, browser, cloud, SSH, messaging, developer, and database credentials.
8. The binary installed user-level persistence as a systemd service masquerading as benign daemons such as `colord` or `haveged`.
9. Windows exfiltration used the Telegram Bot API (`api[.]telegram[.]org`); SafeDep reports Linux and macOS variants used multipart HTTP POST gated behind anti-VM checks.
10. After publishing payload releases, the actor moved `latest` to scrubbed versions with empty scripts blocks or no payload. SafeDep counts 44 versions with active payload hooks, 12 scrubbed latest tags, four intermediate no-hook releases, three scope-reservation stubs, and one unpublished payload version.

## Package set
| Package | Reported version span | Notes |
| --- | --- | --- |
| `@apexcraft/nano-key` | `1.2.4`-`1.3.8` | Payload and scrubbed releases; publisher pattern `apexcraft-8uiljr@wshu[.]net`. |
| `@briskforge/envcheck` | `0.5.2`-`0.5.5` | Payload and scrubbed releases; includes runtime execution through `lib/preflight.js`. |
| `@bytemend/mfebus` | `1.4.0`-`1.4.5` | Payload, no-hook, and scrubbed releases. |
| `@chunklab/hexparse` | `1.0.7`-`1.1.7` | Payload and scrubbed releases. |
| `@frostnode/probe` | `0.0.1` | Scope-reservation stub. |
| `@frostnode/waitfor` | `0.9.0`-`0.10.6` | Payload and scrubbed releases. |
| `@gleamkit/probe` | `0.0.1` | Scope-reservation stub. |
| `@glitchpad/throttler` | `2.1.1`-`2.2.4` | Payload and scrubbed releases; shares a payload hash cluster with `@lazyutil/dater`. |
| `@lazyutil/dater` | `0.8.1`-`0.9.5` | Payload and scrubbed releases. |
| `@nullzero/urlcat` | `1.4.2`-`1.4.5` | One reported payload version was unpublished; surviving versions are scrubbed or no-hook. |
| `@petitcode/eb-retry` | `1.3.3`-`1.3.6` | Payload and scrubbed releases; runtime execution occurs when the copied retry wrapper is called. |
| `@thymelab/logfx` | `2.15.3`-`2.15.6` | Payload and scrubbed releases. |
| `@tinyfox/shapecheck` | `0.7.4`-`0.8.8` | Payload and scrubbed releases. |
| `@zynkit/jwtbytes` | `0.4.3`-`0.5.4` | Payload and scrubbed releases. |
| `@zynkit/probe` | `0.0.1` | Scope-reservation stub. |

## Reported indicators and pivots
- Publisher email pattern: `<scope>-<six random characters>@wshu[.]net`
- Package author pattern: `<scope>@pm[.]me` with `github[.]com/<scope>` homepages
- Delivery account / removed repository: `github[.]com/angelmaybeth21-oss/test`
- Delivery path reported from dynamic analysis: `/releases/download/v1.0.0/{linux,mac,win.js}`
- Additional GitHub account mentioned by SafeDep: `smilingdusty233`
- Windows exfiltration endpoint family: `api[.]telegram[.]org`
- Host artifacts reported by SafeDep:
  - `/tmp/_installer-0/`
  - `~/.local/bin/<daemon>`
  - `~/.config/systemd/user/<daemon>.service`
  - `~/.local/state/<daemon>/{install.nonce,machine.id}`
- Service-name masquerade examples: `colord`, `haveged`

## Defender heuristics
### Exposure triage
- Search manifests, lockfiles, SBOMs, package-manager caches, private registry mirrors, CI logs, artifact build logs, and endpoint process telemetry for every package and version span in the table.
- Do not trust a package's current `latest` tag as a clean signal. Review all resolved versions, cached tarballs, and lockfile pins.
- Treat any install of a payload version on a developer workstation or CI runner as full host compromise, not as a package-cleanup-only event.
- Include `npm install --ignore-scripts` environments in scope when `@petitcode/eb-retry` or `@briskforge/envcheck` reached runtime code paths.

### Endpoint hunting
- Hunt for `node` spawning detached child processes or downloaders during npm install windows.
- Inspect user-level systemd services under `~/.config/systemd/user/`, especially recently created services named like normal daemons (`colord`, `haveged`) and pointing into `~/.local/bin/`.
- Review `/tmp/_installer-0/`, `~/.local/bin/`, and `~/.local/state/` for recent binaries and nonce / machine-id artifacts.
- Hunt outbound requests to GitHub Releases paths under removed or low-reputation accounts and to `api.telegram.org` from developer machines and CI runners.
- Rotate credentials reachable from affected hosts: npm, GitHub, PyPI, SSH, cloud provider keys, Kubernetes configs, database clients, browser-stored credentials, messaging sessions, and cryptocurrency wallets.

### Package-review lessons
- Flag large obfuscated package-local JavaScript blobs in otherwise small utility packages, especially when the blob is the package's largest file by a wide margin.
- Correlate packages by publisher email templates, creation-time bursts, homepage / author patterns, payload hashes, and obfuscation fingerprints, not just maintainer account names.
- Review historical versions and dist-tags, not only the latest tarball.
- Treat runtime-side bootstrap calls as equivalent to lifecycle hooks for risk scoring; install-time controls do not cover import-time or first-use execution.

## Related pages
- [procwire / routecraft npm Windows dropper](procwire-routecraft-npm-windows-dropper.md)
- [MYRA RAT](../tools/myra-rat.md)
- [Mastra `easy-day-js` npm scope compromise](mastra-easy-day-js-npm-scope-compromise.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- SafeDep: <https://safedep.io/wshu-net-npm-credential-stealer-campaign>
