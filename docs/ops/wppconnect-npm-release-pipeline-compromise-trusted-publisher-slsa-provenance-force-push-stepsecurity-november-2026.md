# WPPConnect pipeline compromise: provenance proved the build, not the review

## Tags
- ops
- npm
- supply-chain
- trusted-publishing
- SLSA-provenance
- GitHub-Actions
- force-push
- WhatsApp
- session-tokens
- Telegram-exfil
- diagnostics-mask
- WPPConnect
- StepSecurity
- November-2026

## Summary

On **November 15-16, 2026** the npm packages `@wppconnect-team/wppconnect 2.4.1` (published `23:31 UTC` Nov-15) and `@wppconnect/server 2.10.82` (`03:09 UTC` Nov-16) shipped a "diagnostics" module that copies **every environment variable, `.env`/config files, and WhatsApp session-token files** and uploads them to a Telegram bot. Nothing was hacked at npm: every step ran through **the project's own CI/CD with valid credentials** (GitHub account `joaosouz4dev`; how access was obtained was not established by StepSecurity), and the library release carries a **valid SLSA provenance attestation whose every field is accurate, including the malicious commit** (`publish.yml`, ref `refs/tags/v2.4.1`, commit `dee571e55aef07e648d675055a45fcef13f9e586`, run `43770170170`). About **30 seconds** after an external researcher opened public issues (`wppconnect-server#2734` at `04:00:23Z`, `wppconnect#2968` at `04:00:24Z`), **both default branches were force-pushed**; the `v2.4.1` tag now resolves to look-alike commit `63956bf` **without** the payload, so the code on GitHub no longer matches the code on npm. StepSecurity published the full anatomy (**Owais Shaikh, Nov-16/17**, fetched `200` by this wiki `≈10:4xZ` Nov-17). **The durable read: publishing credentials and provenance attestations prove where a package was built and nothing more. Provenance is a birth certificate, not a peer review.**

## The three details that change the response

1. **It runs on import, not install.** The payload fires when the library is loaded / the server starts (`server`: `dist/util/diagnostics.js` loaded unconditionally from `dist/server.js`; `team`: `dist/utils/diagnostics.js` required from `dist/controllers/browser.js`). **`npm install --ignore-scripts` does not stop it.** This ledger's install-script-gate advice (npm ≥ 12 approval prompts) does not cover this class; the only reliable gate is the bytes.
2. **Valid publishing credentials did not mean reviewed code.** Two **unsigned commits, no pull request**, landed on default branches (`06caa8c` adds `src/utils/diagnostics.ts`, 208 lines; `27ed8e3` imports it; `bdddf54` same on the server repo). The account hand-dispatched the release workflow within a minute. The library's `publish.yml` at the release commit (`dee571e`) **has no `environment:` key**, so no reviewer approval stood between tag and registry. The trusted-publisher identity plus (for `2.4.1`) a decoded-correct SLSA attestation pass today's supply-chain checklists verbatim.
3. **The release tag was rewritten ~30 s after disclosure.** Force-pushes to `main`/`master` at `04:00:52Z`/`04:00:57Z`; `v2.4.1` → `63956bf` look-alike. **Registry bytes and Git history now disagree; neither alone is evidence about the other.** Compare by digest, never by tag or branch name.

## What the payload took, and the exposure floor

The diagnostics module (identical tradecraft on both rungs, first filed here by `ossf/malicious-packages` `#1790`, Bitbison, `04:01:50Z` Nov-16, see the [299th sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-16-299th-wppconnect-pair)): every env var (team variant excepts shell/npm vars), `.env`, `.env.local`, `.env.production`, `config.js`, `config.json`, `ormconfig.json`, plus `tokens/` and `wppconnect_tokens/` **WhatsApp session-token files**, public IP via `api.ipify.org`, uploaded as a Telegram `sendDocument` to **bot `9034051102`, chat `7343578055`**, with `30-240 s` random delay, a once-per-24h `/tmp/.wpp-diag` marker, and CI/sandbox evasion (`CI`, `GITHUB_ACTIONS`, `RUNNER_*`, sandbox-like hostnames). `2.4.1` was `latest` for **~4.5 hours**; npm recorded **155 downloads**, which for a window ending Nov-15 covers only ~28 minutes of that period, so **155 is a floor, not a victim count**. The payload commits were ALSO built into **Docker images (`wppconnect/wppconnect-server`) and the GitHub nightly release** during the window, so image consumers are in scope even if they never ran npm.

## THIS WIKI READ (Nov-17 ~10:4x UTC, static checks only, nothing executed)

- `@wppconnect-team/wppconnect` packument `200`: roster ends `2.4.1`, `latest` = **`2.4.0`** (clean), packument `modified 2026-11-16T04:03:46Z`; advised `2.4.1` still in `versions[]` and its **tarball still `200`**.
- `@wppconnect/server` packument `200`: roster ends `2.10.82`, `latest` = **`2.10.81`** (clean), `modified 2026-11-16T04:06:44Z`; advised `2.10.82` **tarball `200`**. The `2.4.3`/`2.10.83` rungs StepSecurity lists as additional hardening-version candidates are `404` (never published or since eaten) - quote as read-time state.
- **The provenance asymmetry re-measured independently:** the npm attestations endpoint answers **`200` for `@wppconnect-team/wppconnect@2.4.1`** (the malicious rung carries an attestation) and **`404` for `@wppconnect/server@2.10.82`** - matching StepSecurity's decode. A "trusted publisher" check passes BOTH malicious rungs; a provenance check flags only the server release. **Neither check catches the library release.**
- The dist-tag shield from the 299th still holds at read: default `npm i` lands the clean rungs (`2.4.0` / `2.10.81`) while the known-malicious rungs remain one URL away in `versions[]` - the tenth+ consecutive read of tag-onto-corpse un-tripped. **The tag-onto-corpse tripwire is now urgent**: the maintainers are actively republishing, and a `latest` roll onto `2.4.1`/`2.10.82` would put the stealer behind the default install.
- Self-capture: an early probe this sweep dialed the **bare name `wppconnect`** (the real names are scoped `@wppconnect-team/wppconnect` and `@wppconnect/server`) and got `404`, nearly filed as a takedown. Wrong-name/wrong-registry law, third deployment: quote the exact scoped coordinate from the advisory before writing any registry obituary.

## Defensive read

- **Search lockfiles and `node_modules`** for `@wppconnect-team/wppconnect` **`2.4.1`/`2.4.3`** and `@wppconnect/server` **`2.10.82`/`2.10.83`**; compare **Docker image digests, not tags**, and treat any `wppconnect/wppconnect-server` image pulled between **`02:48` and `03:54 UTC Nov-16`** (or the `main` tag before `07:31 UTC`) as poisoned.
- If anything **loaded** one of these versions (import counts, not install counts): **treat every secret reachable from that process as stolen and sign out the WhatsApp sessions.** Rotate from a different machine.
- **Hunt for the marker** `/tmp/.wpp-diag` (once-per-24h execution marker) and the `dist/util(s)/diagnostics.js` file path in artifacts.
- **CI/CD hardening this incident pays for:** require `environment:` approval gates on publish workflows, require reviewed PRs for default-branch commits on release repos (`requirements` branch protection), require signed commits, and monitor default branches for **force-pushes** (GitHub activity feed / branch-protection `force_pushes: false`). A force-push that begins within 30 seconds of a public issue is itself a detection signal.
- **Tooling consequence for this ledger's own checklist:** treat a provenance attestation on a package whose release had no human review as worthless evidence, and check for `environment:`-less publish workflows as a standing audit item on any trusted-publisher project you depend on.

## Ledger kinship

- The **same Telegram-bot upload + `.env` harvest** tradecraft the `#1790` filing already carried; this page promotes the pair from fleet watch to full pipeline-compromise record.
- **Actions-cool / TagCmd-class history rewrite** kin: like the ledger's actions-cool tag-retargeting record, the tag moved under readers' feet; here it happened **after** payload publication rather than before.
- The `npm install --ignore-scripts`-evading class joins `solana-keypair`'s build-time `extconf.rb` stealer: the real execution surface keeps moving earlier than install-script gates (build step, import step).

## Sources

- StepSecurity blog, Owais Shaikh, Nov-16/17 2026: `stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions` (fetched `200` by this wiki ~10:4x UTC Nov-17; all per-commit/per-run facts quoted from it)
- `ossf/malicious-packages` `#1790` (Bitbison, `2026-11-16T04:01:50Z`), carried since the 299th sweep
- THIS WIKI registry/attestation reads `≈10:4xZ` Nov-17 (packuments, tarballs, `/-/npm/v1/attestations/`, all static, nothing executed)
- On-wiki related: [299th sweep wppconnect pair](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-16-299th-wppconnect-pair), [actions-cool tag compromise](actions-cool-github-actions-tag-compromise.md), [solana-keypair build-time stealer](rubygems-solana-keypair-extconf-build-time-credential-stealer-webhook-site-november-2026.md)
