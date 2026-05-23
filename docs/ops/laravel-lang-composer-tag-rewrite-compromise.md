# Laravel-Lang Composer tag-rewrite compromise

## Summary
StepSecurity reported a May 22, 2026 Composer supply-chain compromise affecting three Laravel-Lang organization packages: `laravel-lang/http-statuses`, `laravel-lang/actions`, and `laravel-lang/attributes`.

Instead of publishing a new malicious release, the attacker rewrote every git tag in the affected repositories during a roughly 15-minute window from 23:41 UTC to 23:56 UTC. Consumers who ran `composer update`, or installed fresh against the rewritten tags, could pull malicious commits that added an eager Composer `autoload.files` payload.

StepSecurity confirmed end-to-end execution by detonating `laravel-lang/http-statuses` `v3.4.5` in an isolated GitHub Actions runner. The other affected packages shared the same commit structure and payload behavior, but had not all been detonated at publication time.

## Tags
- ops
- operations
- supply-chain
- Composer
- Packagist
- Laravel
- PHP
- CI/CD
- credential-theft
- tag rewrite

## Why this matters
- Mutable git tags are dangerous in Composer ecosystems: version ranges and tag pins can silently resolve to new malicious commits without a new package name or version.
- Composer `autoload.files` is eager; a payload listed there executes as soon as `vendor/autoload.php` is required by Laravel, Symfony, PHPUnit, or similar PHP applications.
- The reported synchronized rewrites across three repositories suggest a compromised maintainer credential or personal access token with organization-wide write access, not ordinary malicious package publication.
- The campaign targets CI and developer secrets, with a short-lived on-disk footprint that can disappear before post-run forensics begins.

## Reported chain
1. The attacker obtained push access to the Laravel-Lang GitHub organization or a credential with write rights across the affected repositories.
2. Automation walked existing tags and force-pushed malicious commits across `laravel-lang/http-statuses`, `laravel-lang/actions`, and `laravel-lang/attributes` between 23:41 UTC and 23:56 UTC on May 22, 2026.
3. Each malicious commit modified `composer.json` and added `src/helpers.php`; commits used fake author metadata (`Your Name <you@example.com>`).
4. `composer.json` added `src/helpers.php` to the Composer `autoload.files` map.
5. Requiring `vendor/autoload.php` executed `helpers.php`, which fetched `https://flipboxstudio.info/payload`.
6. The payload wrote a hidden PHP loader under `/tmp/.laravel_locale/<12 hex chars>.php` and a hidden extensionless ELF under `/tmp/.<8 hex chars>`.
7. The loader posted runner environment data to `https://flipboxstudio.info/exfil`, launched the ELF with `nohup`, and the artifacts self-deleted while processes could continue from memory.

## Affected package/tag scope
StepSecurity says every tag was rewritten in all three confirmed repositories:

| Package | Reported affected tag scope | Example malicious commits reported |
|---|---|---|
| `laravel-lang/http-statuses` | every tag from `v1.0.0` through `v3.4.5` | `bba2e443dc7ff1f8704f52a5375383e3f4f643b8`, `26c233e1a0d4fd2331e8e0f175e18f8eed904aa3`, `db0c3ef246103fd0f6c318e0d48f26b5289044c3`, `9ee599d248cc322fa26054694a83a1f4558cc716`, `6b1d5782a8c8c199d070857802d39bfe609eb6f2` |
| `laravel-lang/actions` | all 46 tags from `1.0.0` through `1.12.2` | `556d2b335d4d6d92139822017ee461b668afe375`, `722cee67326d932e7f71ba3438f62a255d779aa9`, `ad24b980db8f0dca50ccb3ba6badb3c2331e0ef4` |
| `laravel-lang/attributes` | all 86 tags | `d59561727927117e65b35f0183cae131baad19fe`, `1713b19cbf609cb101ff5e216be41f7224269082`, `daa5212264bb73fb39fe7a36618b62717dc564a5` |

StepSecurity cautions that a safe pin must be a pre-2026-05-22 commit SHA independently verified from a local clone or Packagist mirror. Projects whose `composer.lock` already pinned a known-good commit before the rewrite may be safe if they only ran `composer install` against that lockfile.

## Indicators and hunt pivots
- Affected packages: `laravel-lang/http-statuses`, `laravel-lang/actions`, `laravel-lang/attributes`.
- C2 / typosquat domain: `flipboxstudio.info`.
- Stage 1 fetch: `GET https://flipboxstudio.info/payload`.
- Stage 2 exfiltration: `POST https://flipboxstudio.info/exfil`.
- Hidden PHP loader path: `/tmp/.laravel_locale/<12 hex chars>.php`.
- Hidden ELF path: `/tmp/.<8 hex chars>`.
- Process indicators: orphaned `php` or unnamed ELF processes with `ppid=1`, possibly executing from deleted `/tmp` paths.
- Git indicators: commits modifying only `composer.json` and `src/helpers.php`; author `Your Name <you@example.com>`; timestamps clustered from 2026-05-22 23:41 UTC to 23:56 UTC.

## Defender heuristics
- Stop running `composer update` or fresh installs for projects depending on the three affected packages until tags and Packagist metadata are independently verified clean.
- Inspect `composer.lock` for the affected packages; treat lockfiles regenerated on or after 2026-05-22 23:41 UTC, or lockfiles pointing at reported imposter commits, as compromised.
- If a Composer install/update ran in CI or on a developer machine after the compromise window, rotate all reachable CI, GitHub, cloud, container-registry, deployment, database, and application secrets.
- Search runner telemetry, egress logs, DNS logs, and Harden-Runner detections for `flipboxstudio.info`.
- Hunt live systems for orphaned PHP/ELF processes with `ppid=1` and for transient hidden files under `/tmp/.laravel_locale/` or `/tmp/.<hex>`.
- For maintainers, restore tags to known-good SHAs, revoke organization-wide PATs and apps, enforce 2FA, notify Packagist, and audit all repositories for similar tag rewrites.

## Attribution notes
No public reporting used here attributes the Laravel-Lang compromise to TeamPCP, Mini Shai-Hulud, or Megalodon. Track it as a separate Composer tag-rewrite incident unless stronger infrastructure, credential, or operator overlap appears.

## Related pages
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- StepSecurity: https://www.stepsecurity.io/blog/laravel-lang-supply-chain-attack
