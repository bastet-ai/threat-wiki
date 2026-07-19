# SleeperGem RubyGems maintainer-account compromise

## Summary
Aikido Security and StepSecurity reported **SleeperGem** on July 19, 2026: a coordinated RubyGems supply-chain attack in which malicious versions of `git_credential_manager`, `Dendreo`, and `fastlane-plugin-run_tests_firebase_testlab` targeted developer workstations. The campaign combined a new package impersonating Microsoft's Git Credential Manager with releases from two long-dormant, apparently unrelated maintainer accounts.

The gems fetched a second stage from an attacker-controlled account on the public `git.disroot.org` Forgejo service. The loaders deliberately avoided common CI environments, while the observed Linux chain installed a native daemon under the user's home directory, added systemd-user and cron persistence, and attempted to create a setuid-root shell when passwordless sudo was available.

## Tags
- ops
- operations
- supply-chain
- RubyGems
- maintainer-compromise
- dormant accounts
- developer-targeting
- developer workstations
- credential-theft
- persistence
- systemd
- cron
- setuid
- Forgejo

## Why this matters
- The primary exposure surface is the developer workstation, not only CI. The loader checks roughly 30 build-system environment markers and exits when it detects platforms such as GitHub Actions, GitLab CI, CircleCI, Travis, Jenkins, or Vercel.
- `git_credential_manager` 2.8.2 and 2.8.3 execute from the library load path, so merely requiring the gem can trigger the installer; defenders should not limit review to package-install logs.
- `Dendreo` and the fastlane plugin had been dormant for roughly six and seven years. Their sudden malicious releases show why reactivation of stale maintainer identities should be treated as a registry security event.
- Aikido reported that the fastlane plugin had more than 574,000 total downloads and belonged to a different maintainer from the other gems, suggesting compromise across at least two accounts rather than one malicious publisher.
- A valid public code-hosting service and an official-looking `git-ecosystem` account supplied the payload. Blocklisting the entire shared host is imprecise; path, process, and baseline-aware network detections are more durable.

## Confirmed affected releases
| Package | Malicious versions | Registry SHA-256 |
| --- | --- | --- |
| `git_credential_manager` | `2.8.0`, `2.8.1`, `2.8.2`, `2.8.3` | `4cc63a2da5066d4b31d799a9d45b3880d55752369488dca1679986336c26a8ab`; `b03cdc4682ba433b52b1591b0dcbd6c69beed7ea99d8c7ee739b8cbd26b45ad7`; `61361688cf3590c6fc9259004bf159cd1510faf9287cfb6a9d7102c40b977a98`; `5f28b623bb9bce2d5140cec045a1911b0fb441d128a79e366986d424990e03ba` |
| `Dendreo` | `1.1.3`, `1.1.4` | `dd75857ec8f3cc768931592b83c1c3b13eee3723c6aefde7f50c4069b19b2765`; `cd37b55603dea2ec624e255124f270681b5689a26905dfad02cc3bab9f6905df` |
| `fastlane-plugin-run_tests_firebase_testlab` | `0.3.2` | `c55d9f4bbe6b82bb44464bf6703392e595455b0037fb77dd41ade58a8b0ce9a2` |

Aikido found that `Dendreo` 1.1.3 and 1.1.4 added `git_credential_manager` as a dependency. The fastlane plugin's 0.3.2 registry release had no corresponding upstream Git tag; the source repository's tags stopped at 0.3.1. StepSecurity reported the same registry-versus-source mismatch across the malicious releases.

## Reported execution chain

### Loader evolution and CI evasion
- Aikido described `git_credential_manager` 2.8.0 as a working dropper that downloaded and executed platform-specific payloads with TLS certificate verification disabled; 2.8.1 made Unix execution quieter by redirecting output.
- Version 2.8.2 moved installer execution into the gem's load path. StepSecurity observed that its downloaded-script launch line was commented out, making that version a staging release in its test path.
- Version 2.8.3 enabled the script and detonated the full observed chain when the gem was required.
- The loader sent a `Git` user agent and downloaded `deploy.sh` plus a native binary from `git.disroot.org/git-ecosystem/` paths.
- The CI-environment check makes a clean pipeline run weak evidence of safety. Investigation must cover developer endpoints and local dependency caches.

### Persistence and privilege path
StepSecurity's controlled execution of 2.8.3 recorded this Linux behavior:

1. A child Ruby process ran the gem's bundled installer.
2. The installer executed the downloaded `deploy.sh`.
3. The native binary was copied to `$HOME/.local/share/gcm/git-credential-manager` and launched with `--daemon`.
4. A systemd user service named `git-credential-manager` was installed.
5. A cron entry using the same service name was added as a second persistence path.
6. The script checked membership in the `sudo` and `wheel` groups.
7. If passwordless sudo was available, the root path could create `/usr/local/sbin/ping6` as a setuid shell with mode `6777`.

StepSecurity stated that credential harvesting and exfiltration capability resides in the native daemon rather than the small Ruby loader. Its published run confirmed payload retrieval and process/file activity, but did not yet characterize the daemon's complete network behavior. Treat claims beyond the observed loader and persistence chain as pending deeper binary analysis.

## Indicators and hunt pivots
### Packages and infrastructure
- `git_credential_manager` versions 2.8.0–2.8.3
- `Dendreo` versions 1.1.3–1.1.4
- `fastlane-plugin-run_tests_firebase_testlab` version 0.3.2
- `git.disroot.org/git-ecosystem/` — attacker-controlled account/path on a legitimate public Forgejo host
- HTTPS requests from Ruby with certificate verification disabled and user agent `Git`

### Host artifacts
- `$HOME/.local/share/gcm/git-credential-manager`
- `$HOME/.local/share/gcm/.env`
- a systemd user unit named `git-credential-manager` whose `ExecStart` points into `.local/share/gcm/`
- a cron entry launching the same daemon
- `/usr/local/sbin/ping6` as a setuid shell, particularly mode `6777`
- Ruby spawning another Ruby process and a shell when the library is required

### Repository and registry checks
Search Ruby lockfiles for the affected releases:

```bash
grep -RniE 'git_credential_manager \((2\.8\.[0-3])\)|Dendreo \(1\.1\.[34]\)|run_tests_firebase_testlab \(0\.3\.2\)' --include='Gemfile.lock' .
```

Also compare resolved gem releases with source tags and commits. A registry version from a long-dormant project without a matching source release is a high-signal review condition.

## Response guidance
- If an affected gem was installed or required on a developer machine, isolate the host and preserve the gem cache, process, persistence, shell-history, and network evidence before cleanup.
- Treat every secret reachable from the affected user context as exposed. After containment, rotate source-control and registry tokens, SSH keys, cloud credentials, `.env` secrets, browser-stored sessions, and any signing or release credentials present on the host.
- Disable and remove the `git-credential-manager` systemd user unit and cron entry; remove `$HOME/.local/share/gcm/`; inspect `/usr/local/sbin/ping6` and remove it if confirmed as the malicious setuid shell.
- Rebuild high-value developer workstations from trusted media when the native daemon executed. Artifact deletion alone does not establish eradication.
- Review outbound access to the specific Forgejo account/path and correlate it with Ruby process ancestry. Do not assume all `git.disroot.org` use is malicious.
- Review dormant maintainer accounts, enforce phishing-resistant MFA, use narrowly scoped publishing credentials, and alert on publication after long inactivity or without a matching source tag.

## Attribution notes
Public reporting names the campaign **SleeperGem** but does not attribute it to a known actor. Keep it separate from TeamPCP, Shai-Hulud, Mini Shai-Hulud, and other RubyGems campaigns unless later reporting establishes shared account control, infrastructure, code lineage, or operational overlap.

## Related pages
- [BufferZoneCorp RubyGems / Go module CI poisoning](bufferzonecorp-ruby-go-ci-poisoning.md)
- [Atomic Arch AUR package hijack](atomic-arch-aur-package-hijack.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Aikido Security: [SleeperGem: RubyGems supply chain attack targets dormant maintainer accounts](https://www.aikido.dev/blog/sleepergem-rubygems-supply-chain-attack)
- StepSecurity: [SleeperGem: Compromised git_credential_manager, Dendreo, and fastlane RubyGems Drop a Persistent Backdoor](https://www.stepsecurity.io/blog/sleepergem-compromised-rubygems-drop-persistent-backdoor)
- RubyGems version API: [`git_credential_manager`](https://rubygems.org/api/v1/versions/git_credential_manager.json), [`Dendreo`](https://rubygems.org/api/v1/versions/Dendreo.json), and [`fastlane-plugin-run_tests_firebase_testlab`](https://rubygems.org/api/v1/versions/fastlane-plugin-run_tests_firebase_testlab.json)
