# oob.moika.tech dependency-confusion environment stealer

## Summary
SafeDep reported a May 27, 2026 npm dependency-confusion campaign that published 164 packages across five scoped namespaces, with 162 active packages using `postinstall` execution to steal full environment variables and fetch a second-stage script from `oob.moika.tech`.

Microsoft Threat Intelligence later reported a May 28–29 follow-up cluster of 33 malicious npm packages that reused `oob.moika.tech` infrastructure, shifted toward reconnaissance-first profiling, and published under additional maintainer aliases and internal-looking organizational scopes.

The package names were tailored to cloud-platform, ML-workspace, car-loan, deposit-form, debit / internet-banking, payment-widget, data-science, travel-automation, and SberPay-style micro-frontend scopes, indicating the actor profiled internal package ecosystems rather than spraying generic typosquats.

## Tags
- ops
- operations
- supply-chain
- npm
- dependency confusion
- credential-theft
- CI/CD
- cloud secrets
- finance
- environment variables
- postinstall

## Why this matters
- The campaign targeted specific internal-looking scopes and service names, making public-registry fallback especially dangerous for developers and CI jobs that do not scope-lock private packages.
- The first stage exfiltrated raw `process.env`, which often contains npm, cloud, GitHub, database, and deployment credentials.
- Two inert packages used a "BugBounty testing" marker while the remaining active packages executed real credential-theft code, a pattern defenders should not treat as benign proof of authorized testing.
- Microsoft observed a later reconnaissance-first variant with a `*_RECON_ONLY=1` flag and server-side architecture that could support selective follow-on exploitation after target profiling.
- The README text framed outbound install-time activity as "anonymous telemetry" to lower reviewer suspicion while actual reports went to attacker infrastructure.

## Reported campaign
- **Publishing window:** May 27, 2026, beginning around 21:15 UTC, with a second account publishing 22 minutes later.
- **Accounts:** `mr.4nd3r50n` and `pik-libs`.
- **Scale:** 164 packages, all versioned `99.99.99`; 162 carried an active payload and two were inert probes.
- **Targeted scopes:**
  - `@cloudplatform-single-spa` — 122 packages for cloud-platform micro-frontend modules.
  - `@mlspace` — 17 packages for ML / AI workspace modules.
  - `@car-loans` — 19 car-loan application micro-frontend packages.
  - `@fb-deposit` — 4 banking deposit-form packages.
  - `@debit-ib` — 2 debit / internet-banking form packages.
- **Representative names:** `certificate-manager`, `vpn`, `ml-inference`, `experiments-monitoring`, `mobile-car-loans-application`, `form-deposit-auth`.

## Microsoft follow-up cluster: May 28–29, 2026
- **Source:** Microsoft Threat Intelligence, published May 29, 2026.
- **Scale:** 33 malicious npm packages across two publishing bursts.
- **Maintainer aliases:** `mr.4nd3r50n`, `ce-rwb`, and `t-in-one`; Microsoft assessed the aliases as a single operator based on shared C2, shared `X-Secret` value, near-identical staging code, and registry metadata overlap.
- **Additional targeted scopes:** `@cloudplatform-single-spa`, `@wb-track`, `@data-science`, `@ce-rwb`, `@payments-widget`, `@travel-autotests`, `@t-in-one`, `@capibar.chat`, and `@sber-ecom-core`.
- **Representative names:** `svp-baas`, `enterprise`, `monitoring`, `ssh-keys`, `shared-front`, `payments-widget-sdk`, `add_application_service_token`, `ui-kit`, and `sberpay-widget`.
- **Version strategy:** inflated versions such as `100.100.100`, `99.5.7`, and `99.5.8` to win dependency resolution; `@capibar.chat/ui-kit` and `@sber-ecom-core/sberpay-widget` were reportedly pre-staged at `99.0.7` on May 4 before the main bursts.
- **Spoofed metadata:** package `homepage`, `repository`, `bugs`, and `author` fields imitated internal GitHub Enterprise, Jira, documentation, and platform-team metadata.
- **Execution model:** `postinstall` launched an obfuscated `scripts/postinstall.js` stager that performed CI checks, Node.js version validation, project-root discovery, cache deduplication, platform selection, C2 download, temp-file write, and detached Node.js execution.
- **Payload mode:** Microsoft described the observed payload as reconnaissance-first, collecting system information, hostnames, environment variables, installed-package or project context, and developer environment details while carrying a `RECON_ONLY` flag that could enable later selective exploitation.
- **Response:** Microsoft reported the packages and users to npm, and the repositories and users were removed.

## Payload chain
1. Package install triggers `scripts/postinstall.js` through the npm lifecycle hook.
2. The script waits roughly three seconds, likely to outlast short sandbox runs.
3. It detects the operating system and downloads `hxxps://oob[.]moika[.]tech/payload/{mac|win|linux}.js`.
4. The second stage is written to the OS temp directory as `._cloudplatform-single-spa_init.js`.
5. The downloaded script is spawned as a detached Node.js process so it can continue after `npm install` exits.
6. The first stage POSTs hostname, username, platform, architecture, current working directory, Node.js version, and full `process.env` to `hxxps://oob[.]moika[.]tech/report`.
7. If the second-stage download fails, the first stage still sends the same system and environment data directly.

## Infrastructure and indicators
- C2 / report endpoint: `hxxps://oob[.]moika[.]tech/report`
- Payload base: `hxxps://oob[.]moika[.]tech/payload`
- Payload paths: `/payload/mac.js`, `/payload/win.js`, `/payload/linux.js`
- Shared header secret: `l95HdDaz3kQx1Zsg3WxH6HvKANf51RY1` in `X-Secret`
- Temp file: `._cloudplatform-single-spa_init.js`
- Suspicious versions: `99.99.99`, `99.0.7`, `99.5.7`, `99.5.8`, and `100.100.100` in the targeted scopes listed above
- Npm users / aliases: `mr.4nd3r50n`, `pik-libs`, `ce-rwb`, `t-in-one`

## Defender heuristics
- Scope-lock private package namespaces in `.npmrc`; internal scopes should resolve only to trusted private registries.
- Search lockfiles, npm caches, artifact mirrors, CI logs, and package-manager telemetry for suspicious high versions such as `99.99.99`, `99.5.7`, `99.5.8`, and `100.100.100` under the targeted scopes.
- If any active package installed, rotate secrets present in the affected user's or CI runner's environment at install time; environment-only rotation may not be enough if the detached second stage ran.
- Hunt for `._cloudplatform-single-spa_init.js` in temp directories and Node.js child processes that outlive package-manager execution.
- Review egress logs for `oob.moika.tech` and for package installs followed by unexpected HTTPS POSTs during lifecycle-script execution.
- Treat "telemetry" disclosures in untrusted packages as claims to verify, not evidence of benign behavior.

## Related pages
- [`@marketfront` / `@tqm-mfe` dependency-confusion stealer](marketfront-tqm-mfe-dependency-confusion-stealer.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [Laravel-Lang Composer tag-rewrite compromise](laravel-lang-composer-tag-rewrite-compromise.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [js-logger-pack Hugging Face exfiltration campaign](js-logger-pack-hugging-face-exfiltration.md)

## Sources
- SafeDep: <https://safedep.io/oob-moika-tech-dependency-confusion-campaign/>
- Microsoft: <https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/>
