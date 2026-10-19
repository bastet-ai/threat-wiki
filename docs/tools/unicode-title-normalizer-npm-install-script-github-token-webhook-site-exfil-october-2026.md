# `unicode-title-normalizer` — npm install-script exfil of `${{GITHUB_TOKEN}}` through a webhook.site URL path (October 2026)

**Status: LIVE at this wiki's check — registry `latest 1.0.0`, zero OSV, zero GHSA.** Reported to the `ossf/malicious-packages` queue by `r-bedekar` (PR `#1653`, filed `2026-10-19T15:27:55Z`). Discovered/reported by the community reporter; this wiki verified registry state, not package internals (tarball pull deferred).

## The observation

`unicode-title-normalizer@1.0.0` published to npm `2026-10-19 ≈14:50Z`. Per the filing, the package's install script runs `curl` against a **webhook.site URL with `${{GITHUB_TOKEN}}` embedded in the URL PATH** — an attempt to ship the GitHub Actions runner token to a third-party request-capture endpoint **at install time**, i.e. while a CI job is installing dependencies. The rest of the package is filler (`index.js` returns a stub).

**This wiki's checks `≈15:25–15:35Z` (~35–45 min post-publish):** registry `200 latest 1.0.0` LIVE; OSV query `[]` — zero records; the filing itself is `≈4 min` behind the publish = one of the tightest publish→flag clocks on the ledger.

## Why it earns a page

- **Class: CI-token exfil at install time.** The ledger's install-hook cohort (MALFEX, the `conx3993` family, `imgdecode`) steals from the ENDPOINT environment. This is the runner-environment variant: the target is the workflow's own `${{GITHUB_TOKEN}}`, and the trigger is any `npm install` in a CI job that pulls the package — no import, no execution of package code, no victim interaction.
- **webhook.site as the sink** is the dead-drop-per-request shape the ledger already tracks with `requestbin`/`webhook.site` dead-drops — here weaponized inside an install script. Durable IoC family: any registry package whose lifecycle script `curl`s `webhook.site`/`requestbin`-class hosts.
- **The token is scoped to the repo of the running workflow** — the practical blast radius is that repository's Actions permissions (`contents`, sometimes `workflow`/packages), not the developer's account. Detection: egress from runners to `webhook.site` domains; audit any install-time outbound HTTP from `npm install` steps (default should be none).

## Monitor

- OSV/GHSA arrival for the name (none at check) and npm abuse-lane action (`0.0.1-security` seizure class) on `1.0.0`.
- The publisher account and any sibling publishes (name arrived alone; family check deferred to next sweep).
- Whether the webhook.site target URL survives for request-log recovery (reporter-side; if the token values reached it, rotation urgency for any installing repo).
- Copycats: other fresh names with lifecycle-script `curl` to request-capture endpoints.

Related: [MALFEX page](../ops/malfex-npm-single-operator-two-arms-function-flag-14-month-unadvised-postinstall-cloudsek-september-2026.md) (endpoint-side postinstall cohort), [algamil7x 142nd stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-19-one-hundred-and-forty-second-sweep).
