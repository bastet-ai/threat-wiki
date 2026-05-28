# oob.moika.tech dependency-confusion environment stealer

## Summary
SafeDep reported a May 27, 2026 npm dependency-confusion campaign that published 164 packages across five scoped namespaces, with 162 active packages using `postinstall` execution to steal full environment variables and fetch a second-stage script from `oob.moika.tech`.

The package names were tailored to cloud-platform, ML-workspace, car-loan, deposit-form, and debit / internet-banking micro-frontend scopes, indicating the actor profiled internal package ecosystems rather than spraying generic typosquats.

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
- Suspicious version: `99.99.99` in the targeted scopes listed above
- Npm users: `mr.4nd3r50n`, `pik-libs`

## Defender heuristics
- Scope-lock private package namespaces in `.npmrc`; internal scopes should resolve only to trusted private registries.
- Search lockfiles, npm caches, artifact mirrors, CI logs, and package-manager telemetry for version `99.99.99` under the targeted scopes.
- If any active package installed, rotate secrets present in the affected user's or CI runner's environment at install time; environment-only rotation may not be enough if the detached second stage ran.
- Hunt for `._cloudplatform-single-spa_init.js` in temp directories and Node.js child processes that outlive package-manager execution.
- Review egress logs for `oob.moika.tech` and for package installs followed by unexpected HTTPS POSTs during lifecycle-script execution.
- Treat "telemetry" disclosures in untrusted packages as claims to verify, not evidence of benign behavior.

## Related pages
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [Laravel-Lang Composer tag-rewrite compromise](laravel-lang-composer-tag-rewrite-compromise.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [js-logger-pack Hugging Face exfiltration campaign](js-logger-pack-hugging-face-exfiltration.md)

## Sources
- SafeDep: https://safedep.io/oob-moika-tech-dependency-confusion-campaign/
