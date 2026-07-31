# npm install explicit-trust controls

## Summary
JFrog Security Research documented npm v12's move from implicit install-time trust to explicit approvals for the three npm dependency-ingestion paths most often abused by recent supply-chain malware: lifecycle scripts, Git dependencies, and remote URL dependencies. On July 8, 2026, GitHub announced that **npm v12 is generally available and tagged `latest`**, turning those install-time security defaults on in the shipped release rather than leaving them as an upcoming change.

StepSecurity's June 2026 developer-machine package-configuration guidance adds the fleet-control side of the same pattern: registry, cooldown, and authentication policy only protects hosts that are actually configured to use it. Treat package-manager configuration drift on laptops and CI runners as an exposure class, not a compliance footnote.

Track this as a defender pattern rather than a single operation. The same install-time execution paths have appeared across Shai-Hulud / Miasma, Mastra `easy-day-js`, `binding.gyp`, and other developer-machine compromise chains. npm v12 reduces one default execution path, but it does not remove the need to govern approved scripts, Git dependencies, remote URL dependencies, package-manager configuration drift, import-time execution, and runtime package behavior.

## Tags
- patterns
- supply-chain
- npm
- npm v12
- JavaScript
- lifecycle-hooks
- install-time-execution
- developer-workstations
- CI-CD
- package-manager-hardening
- registry-controls
- package-cooldowns
- developer-machine-fleet
- bypass2fa
- granular access tokens
- Shai-Hulud
- Miasma

## What changed
- GitHub's July 8 changelog says npm v12 is now generally available and tagged `latest`; teams should stop treating the new install-time defaults as future planning and start testing real project behavior.
- `allowScripts` controls which third-party packages may run lifecycle scripts during install, including `preinstall`, `install`, `postinstall`, `prepare`, and implicit `binding.gyp` native-build execution.
- npm v12 changes the default posture so third-party lifecycle scripts do not run unless explicitly approved.
- `--allow-git` gates direct and transitive Git repository dependencies.
- `--allow-remote` gates direct and transitive remote URL dependencies.
- JFrog said these three vectors appeared in about 53% of malicious npm attacks it observed over the prior year, with lifecycle scripts alone appearing in about 46% of observed malicious npm packages.
- GitHub also began deprecating **granular access tokens with `bypass2fa` privileges**. As of July 31, those tokens can no longer create or delete tokens; change package access, maintainers, or trusted-publishing configuration; or manage organization/team membership and package grants. Those operations now require an interactive 2FA challenge. This restriction applies to npm granular access tokens, not GitHub PATs, GitHub App tokens, or Actions `GITHUB_TOKEN`.
- Direct publication with npm 2FA-bypass tokens remains temporarily available, but GitHub targets **January 2027** for removing it. The remaining surface is expected to permit reading private packages and staging a publish that a maintainer approves with 2FA. Migrate automation to trusted publishing with OIDC or staged publishing rather than treating the current management-action restriction as full token retirement.

## Why this matters
- Recent npm worms and credential stealers have relied on automatic install-time execution because it runs on developer machines and CI runners before application code is reviewed.
- Blocking scripts by default reduces the blast radius of newly published malicious versions and typosquats, especially when combined with registry cooldowns and internal mirrors.
- Git and remote URL dependencies bypass some registry-centric controls; requiring explicit allowance makes those dependency sources visible policy decisions.
- Native-module builds deserve special review: packages that legitimately need `node-gyp` or postinstall downloads can become high-value compromise targets because organizations may pre-approve their scripts.
- Internal registries, secure registries, and package-version cooldowns are only effective when developer machines and CI runners consistently use them. A single laptop with a direct public-registry path can become the first compromised host in a supply-chain incident.

## Attacker adaptations to expect
- Compromise of packages that are already approved in an organization's `allowScripts` / `approve-scripts` configuration.
- Migration from install-time execution to import-time execution, where code runs when a package is imported by application or build tooling.
- Runtime invocation payloads hidden behind normal-looking API calls or build steps.
- More abuse of trusted package maintainers, release automation, and transitive dependencies that inherit approval decisions.
- Social engineering or documentation changes that ask developers to run installs with broad `--allow-*` flags.

## Defender heuristics

### Policy and inventory
- Inventory `.npmrc`, `package.json`, lockfiles, package-manager wrappers, and CI templates for current script, Git dependency, and remote URL behavior.
- Inventory Python package-manager configuration alongside npm: `pip.conf`, `pip.ini`, `pyproject.toml`, `requirements*.txt`, `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, and tool-specific config for Poetry, uv, and pip-tools.
- Verify whether each developer machine and CI runner resolves packages through the intended internal registry / secure registry, whether fallback to public indexes is allowed, and whether package-version cooldown policy is actually enforced at the endpoint.
- Audit package-manager authentication posture: remove stale registry tokens, eliminate granular access tokens that retain legacy `bypass2fa` publication privileges, avoid shared long-lived tokens on developer machines, and prefer scoped credentials that cannot publish or read unrelated private packages.
- Review automation for account, organization, team, maintainer, package-access, and trusted-publishing changes formerly performed with npm bypass-2FA tokens; move those actions to an interactive, phishing-resistant 2FA path and alert on failed legacy attempts.
- Treat every existing lifecycle-script approval as a privileged allowlist entry; record who owns it, why it is needed, and how updates are reviewed.
- Prefer package-specific approvals over broad flags that allow all scripts or all non-registry dependency sources.
- Require review for dependency changes that introduce Git URLs, tarball URLs, `preinstall`, `postinstall`, `prepare`, or `binding.gyp` paths.

### CI / developer hardening
- Roll npm upgrades deliberately: test npm v12 behavior on representative projects before forcing fleet-wide adoption, then remove compatibility bypasses once packages are remediated.
- Pair npm v12 controls with registry cooldowns, internal mirrors, and malicious-package blocking; npm's install controls do not replace package intelligence.
- Continuously check package-manager configuration drift on developer laptops, not only in golden images. Attackers only need one host that bypasses the internal registry or cooldown path.
- Fail closed when a workstation or runner cannot reach the approved registry path; do not silently fall back to the public npm or PyPI indexes during outages.
- For CI, fail closed when a dependency needs a newly unapproved script or non-registry source instead of falling back to permissive install flags.
- Monitor build logs for `--allow-git`, `--allow-remote`, broad script approvals, `--ignore-scripts` bypass workarounds followed by manual execution, and unexpected `npm rebuild` behavior.

### Detection pivots
- Alert on lifecycle scripts added to packages that did not previously need install-time execution.
- Alert when package-manager config changes introduce public-index fallback, disable cooldown enforcement, add broad extra indexes, or replace an organization registry with direct upstream npm / PyPI access.
- Correlate package approval changes with maintainer-account changes, newly published versions, and package-source repository changes.
- Hunt for developer or runner processes where `npm` spawns shells, network tools, Python, Bun, native compilers, or updater-like binaries during dependency installation.
- Continue import-time and runtime scanning; npm v12 controls reduce install-time execution but do not stop malicious code that waits for application import or invocation.

## Related pages
- [npm publish-time malware scanning and dual-use declarations](npm-publish-time-malware-scanning.md)
- [Dependabot cross-ecosystem malware advisory alerts](dependabot-cross-ecosystem-malware-alerts.md)
- [binding.gyp npm CI/CD worm](../ops/binding-gyp-npm-cicd-worm.md)
- [Mastra `easy-day-js` npm scope compromise](../ops/mastra-easy-day-js-npm-scope-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)

## Sources
- JFrog Security Research: [https://jfrog.com/blog/npm-v12-from-implicit-to-explicit-trust/](https://jfrog.com/blog/npm-v12-from-implicit-to-explicit-trust/)
- StepSecurity: [https://www.stepsecurity.io/blog/prevent-npm-and-python-supply-chain-attacks-on-developer-machines-with-package-configs](https://www.stepsecurity.io/blog/prevent-npm-and-python-supply-chain-attacks-on-developer-machines-with-package-configs)
- GitHub Changelog: [https://github.blog/changelog/2026-07-08-npm-install-time-security-and-gat-bypass2fa-deprecation/](https://github.blog/changelog/2026-07-08-npm-install-time-security-and-gat-bypass2fa-deprecation/)
- GitHub Changelog, “Restricting npm bypass-2FA granular access tokens,” 2026-07-31: [https://github.blog/changelog/2026-07-31-restricting-npm-bypass-2fa-granular-access-tokens](https://github.blog/changelog/2026-07-31-restricting-npm-bypass-2fa-granular-access-tokens)
- Socket: [https://socket.dev/blog/npm-12](https://socket.dev/blog/npm-12)
