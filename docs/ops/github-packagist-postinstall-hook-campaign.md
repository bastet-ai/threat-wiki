# GitHub / Packagist postinstall hook campaign

## Summary
Socket reported a May 2026 cross-ecosystem supply-chain campaign where attacker-made commits added the same malicious `package.json` `postinstall` hook to upstream GitHub repositories that also publish Composer packages through Packagist.

The confirmed Packagist impact involved eight branch-tracking Composer package versions. The malicious hook did not live in `composer.json`; it lived in JavaScript build metadata bundled with PHP projects. That placement matters because PHP dependency review can miss npm lifecycle hooks, while starter-kit projects may run `npm install` at the repository root and execute the hook directly.

Socket also found hundreds of public GitHub code-search hits for the same attacker account/infrastructure, but caveated that these results can include forks, duplicates, cached references, and unconfirmed compromises. Track the eight Packagist packages as confirmed and the broader GitHub result set as an expansion lead.

## Tags
- ops
- operations
- supply-chain
- GitHub
- Packagist
- Composer
- npm
- lifecycle hooks
- credential-theft
- Linux

## Why this matters
- Cross-ecosystem packages can hide executable npm lifecycle behavior inside PHP/Composer projects; reviewing only `composer.json` is not enough.
- Branch-tracking Composer versions such as `dev-main`, `dev-master`, and `3.x-dev` can move as upstream Git branches move, complicating package-version-only incident response.
- Starter kits are higher risk than libraries because the cloned/generated project becomes the developer's application root, where `npm install` commonly executes `package.json` lifecycle scripts.
- Even without the second-stage binary, an unauthenticated download-and-execute install hook is sufficient to treat the artifact as malicious.

## Reported chain
1. The attacker added a malicious `package.json` `postinstall` script directly to upstream GitHub repositories.
2. Packagist reflected those branch states into Composer package artifacts for `dev-main`, `dev-master`, or similar branch-tracking versions.
3. The hook downloaded a Linux binary named `gvfsd-network` from a GitHub Releases URL under attacker account `parikhpreyash4`.
4. The installer wrote the binary to `/tmp/.sshd`, made it executable, suppressed errors, and launched it in the background.
5. Several maintainers reverted the commits; Packagist removed the affected packages after Socket reported them. Socket warned that branch-tracking packages can reappear clean or dirty as the upstream branch changes.

## Confirmed affected Packagist packages
| Package | Affected version | Reported status when checked |
|---|---|---|
| `moritz-sauer-13/silverstripe-cms-theme` | `dev-master` | Hook still present on `master` |
| `crosiersource/crosierlib-base` | `dev-master` | Hook still present on `master` |
| `devdojo/wave` | `dev-main` | Reverted by `5afe6da` |
| `devdojo/genesis` | `dev-main` | Reverted by `3be1f20` |
| `katanaui/katana` | `dev-main` | Reverted by `f679252` |
| `elitedevsquad/sidecar-laravel` | `3.x-dev` | Reverted by `b1f5c53` |
| `r2luna/brain` | `dev-main` | Reverted by `421a1d5` |
| `baskarcm/tzi-chat-ui` | `dev-main` | Hook still present on `main` |

Socket highlighted `devdojo/wave` and `devdojo/genesis` as the most practically exposed because they are Laravel starter kits with meaningful adoption. In those projects, the malicious `package.json` can land at the application root and run during normal JavaScript dependency installation.

## Indicators and hunt pivots
- GitHub account: `parikhpreyash4`.
- GitHub repository: `parikhpreyash4/systemd-network-helper-aa5c751f`.
- Payload URL: `https://github.com/parikhpreyash4/systemd-network-helper-aa5c751f/releases/latest/download/gvfsd-network`.
- Local path: `/tmp/.sshd`.
- Command fragments: `curl -skL`, `chmod +x /tmp/.sshd`, `/tmp/.sshd &`.
- Package metadata: unexpected `postinstall` hook in `package.json` inside Composer/PHP repositories, especially branch-tracking versions.

## Defender heuristics
- Inspect bundled `package.json` files in Composer packages that include JavaScript tooling; do not limit review to `composer.json` scripts and plugin hooks.
- Prefer immutable tags/releases over branch-tracking Composer dependencies in build and production pipelines.
- Tie incident response to commit/archive state, not just a branch-version label that can later point to clean content.
- Block install-time download-and-execute patterns, especially `curl -k` / hidden `/tmp` executables / background execution chains.
- For affected starter-kit projects, treat any developer or CI environment that ran `npm install` against the poisoned state as potentially compromised and rotate reachable credentials.

## Attribution notes
Socket did not publicly attribute this campaign to TeamPCP or Mini Shai-Hulud. Keep it separate unless later reporting ties the attacker infrastructure or operator identity to a named group.

## Related pages
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Laravel-Lang Composer tag-rewrite compromise](laravel-lang-composer-tag-rewrite-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- [Socket](https://socket.dev/blog/malicious-postinstall-hook-found-across-700-github-repos)
