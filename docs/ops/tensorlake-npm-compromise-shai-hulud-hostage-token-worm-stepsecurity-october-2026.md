# `tensorlake@0.5.144`: the worm is back and it calls itself Shai-Hulud — a compromised scientific-workflow npm package with a hostage-token wiper

**Priority-watch event.** On October 8, 2026 StepSecurity published a full write-up of a compromise of the legitimate npm package `tensorlake`: release `0.5.144` was built from the project's OWN `main` branch, carries a VALID npm provenance attestation, steals credentials at install, republishes itself into the victim's own packages, persists through AI-agent and editor config files, exfiltrates into a GitHub repo the malware creates IN THE VICTIM'S ACCOUNT with the description **"Shai-Hulud: Here We Go Again"** — and installs a watchdog that deletes the victim's home directory if the stolen GitHub token is ever revoked. This wiki independently pulled and hashed both payload files from the LIVE `main` branch and confirmed the exfil domain resolves. Identity attribution to the original Shai-Hulud actor is branding, not proven — recorded as declared, not asserted.

## Timeline (all UTC, this wiki's own verified reads marked ✓)

| Time | Event |
|---|---|
| Oct 7 01:20 | First malicious commit pushed directly to `main` of `tensorlakeai/tensorlake` under a maintainer's name — no PR. Seven more commits follow over the next ~22 h |
| Oct 7 03:57–23:41 | ✓ Commit tail visible via GitHub API: `e65ed94` "Update package.json" 03:57:54 → `1c89f03`/`47725d2` version bumps 04:44/04:55 → `8135848` "bump version to 0.5.144" 23:15:50 → `c77b335`/`6386121` dependency pins 23:30/23:41 — all authored under the maintainer identity "Shanshan Wang" |
| Oct 8 01:12:07 | ✓ `0.5.144` published to npm from the repo's own release workflow — time block timestamp `2026-10-08T01:12:07.320Z` (StepSecurity says 01:12, exact match) |
| Oct 8 01:22:02 | ✓ StepSecurity's GitHub issue #1014 filed (this wiki: `created_at 2026-10-08T01:22:02Z`, state OPEN) |
| Oct 8 02:54:27 | ✓ npm registry `modified` stamp — `0.5.144` removed from the package document, `latest` back to `0.5.143`, tarball now `404` (this wiki: `npm view tensorlake@0.5.144` → E404, tarball GET → 404). Exposure window ≈ 1 h 42 m |
| Oct 8 02:54:39 | ✓ `GHSA-rqxj-g25x-4v9v` published (critical, CWE-506, `= 0.5.144`, no CVE) — **12 SECONDS after the registry's own modified stamp = first action on the abuse lane, advisory second** |
| Oct 8 ~03:5x | ✓ OSV `v1/query` for `tensorlake` (npm AND PyPI): EMPTY — the forward mirror had not arrived at this wiki's check; `MAL-2026-17650` still `code:5` absent. Pending-mirror watch armed |
| Oct 8 ~03:5x | ✓ **The payload is STILL ON `main`**: `raw.githubusercontent.com/tensorlakeai/tensorlake/main/typescript/lib/Math_Symbol.js` answers 200, 856,501 B; `lib/setup.mjs` answers 200, 32,645 B — ~27 h after the first malicious commit, the repository-side cleanup has NOT happened |

## Verified hashes (this wiki, no execution)

- `typescript/lib/setup.mjs` — sha256 `25a0735d0db7dc40e5d45ce42d9c106067e6a66e184d967cfecfab17c3bcb5ef` — **byte-identical to StepSecurity's published IoC**
- `typescript/lib/Math_Symbol.js` — sha256 `b50a00900399ba99fb6ce1fc151519cb99d44320ef2a631f2237e1aea0ad6fec` — **byte-identical to StepSecurity's published IoC**

The `preinstall` hook runs `setup.mjs`, which self-skips on CI (developer machines are the target), downloads the Bun runtime, and executes the obfuscated 856 KB `Math_Symbol.js` under it. Malicious commit range per StepSecurity: `e90c47b`–`6386121` under `typescript/lib/`.

## What the payload does (StepSecurity analysis, captured full text)

**Harvests:** GitHub + npm tokens, cloud keys, Kubernetes and Vault secrets, SSH keys, saved browser logins, and config files for AI tools (Claude, Cursor, Windsurf).

**Exfiltrates** by encrypting and pushing to (a) a public GitHub repo the malware CREATES IN THE VICTIM'S OWN ACCOUNT, description verbatim **"Shai-Hulud: Here We Go Again"**, or (b) `iseekaigogo.com` — ✓ this wiki: the domain RESOLVES (Cloudflare `2606:4700:3032::6815:16d9` / `2606:4700:3033::ac43:cf21`) and answers HTTP `301` = LIVE at check.

**Spreads:** with a stolen npm token it downloads the victim's own packages, adds itself, bumps the version, and republishes — the classic self-replicating npm worm loop; with a stolen GitHub token it commits `.claude/settings.json` and `.vscode/tasks.json` into the victim's repos under author `claude@users.noreply.github.com` with message `chore: update dependencies` = re-execution the next time anyone opens the project in Claude Code or VS Code.

**The hostage token — the wiper tripwire:** once it holds a GitHub token it installs `gh-token-monitor` (`~/.config/gh-token-monitor/`, `~/.local/bin/gh-token-monitor.sh`, systemd user unit / LaunchAgent / Task-Scheduler `monitor.ps1`). Every 60 s for up to 24 h it validates the token against the GitHub API; if GitHub REJECTS the token, the monitor runs `rm -rf ~/` (PowerShell profile-delete on Windows). **Revoking the stolen token — the reflexive IR first move — is exactly what detonates the wipe.** Remediation order is mandatory: find and remove the monitor FIRST, then revoke, then rotate everything.

## The durable reads

1. **Provenance attests the WHO, not the WHAT — second time in three days.** Oct 5: `@subql/common@5.8.3` built its payload in CI via a tampered publish workflow with valid OIDC trusted-publisher identity. Oct 8: `tensorlake@0.5.144` built from real `main`, real release workflow, valid npm provenance — because the malicious code was in the repo before the build. A provenance-trusting policy let BOTH through. The durable hunt is unchanged: diff release commits and workflow changes, not attestation signatures; a maintainer-authored commit series with no PRs landing right before a release is the tell.
2. **Registry action preceded the advisory by 12 seconds.** The npm document was cleaned at 02:54:27.126Z; the GHSA published at 02:54:39Z. On high-visibility, reporter-flagged names the abuse lane moves first and the advisory documents it — the same first-abuse-lane shape this wiki measured on the curated lane (`css-nesting-transform` purged with zero advisories) now caught on a machine-name.
3. **AI-agent config files as a persistence rail.** `.claude/settings.json` and `.vscode/tasks.json` written into repos by a worm, disguised as an AI-authored chore commit — this is the same reinfection rail class this wiki flagged with `Azure/durabletask`-style AI-assistant/editor persistence and the `abstract-claude` hook cluster, now rebuilt worm-native. Hunt: unexpected `.claude`/`.vscode` files with author `claude@users.noreply.github.com`.
4. **The Bun grammar.** Setup downloads Bun and runs the payload under it — the same runtime-retrieval grammar as `@7nohe/openapi-react-query-codegen` (Aug 28, this wiki's page). Grammar recurrence, identity NOT asserted.
5. **The Shai-Hulud brand is the intelligence, until attribution isn't.** The repo-description taunt is the actor's own naming convention from the original campaign. Treat as continuity CLAIM; the mechanically verifiable continuities at check are: repo-description exfil channel, install-time credential harvest, npm-token worm republish, GitHub-token repo poisoning. Nothing here proves the same operator; everything here gives defender hunt keys regardless of who holds it.
6. **Registry cleanup ≠ repository cleanup.** npm purged the version in under two hours; `main` STILL serves both payload files at this wiki's write — every clone-and-build path from the repo since Oct 7 01:20Z remains a candidate execution path until the repo is cleaned. Check whether you `git pull`ed `main` and ran `npm install` under `typescript/`, per StepSecurity.

## Defender hunt keys

- Lockfiles containing `tensorlake@0.5.144` (pin to `0.5.143` until the repo is clean).
- On any machine that installed it: `~/.config/gh-token-monitor/` — **remove the service BEFORE revoking anything**.
- GitHub: new public repos on user/org accounts with description `Shai-Hulud: Here We Go Again`; commits authored `claude@users.noreply.github.com`; `.claude/settings.json` / `.vscode/tasks.json` nobody added; npm republish bursts from maintainer accounts.
- Network: `iseekaigogo.com` (Cloudflare-fronted, live at this wiki's check — expect front rotation).
- File-integrity: sha256 `25a0735d0db7dc40e5d45ce42d9c106067e6a66e184d967cfecfab17c3bcb5ef` (setup.mjs), `b50a00900399ba99fb6ce1fc151519cb99d44320ef2a631f2237e1aea0ad6fec` (Math_Symbol.js).
- Process: `curl`/fetch of a Bun binary by an npm lifecycle script (`preinstall` → bun → 856 KB obfuscated JS) on a developer workstation, absent in CI.

## Monitoring

Whether the OSV mirror (`MAL-2026-17650`) lands for `tensorlake` — **LANDED Oct 8 04:45:04Z** (one-hundred-and-tenth sweep: `GHSA-rqxj-g25x-4v9v` published 02:54:39Z; registry `latest` back to `0.5.143`, malicious `0.5.144` purged 02:54:27Z = 12 s before its own GHSA, delete-then-advise on a legitimate brand; both advisories + OSV live = consumers warned, registry rail severed). Remaining watches: whether `main` is finally cleaned or force-pushed (payload files live at write per StepSecurity); which packages the worm republished under stolen npm tokens (StepSecurity's Threat Center list is the rolling feed); whether the hostage-wiper actually fires in the wild; whether the Shai-Hulud branding draws copycats or a second named wave; PyPI-side `tensorlake` status (clean at check).

## Related pages

- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) — the prior-generation worm this campaign brands itself as successor to
- [Bitwarden/Checkmarx Shai-Hulud third coming](bitwarden-checkmarx-shai-hulud-third-coming.md) — earlier continuity chapter
- [`@7nohe/openapi-react-query-codegen` compromise](7nohe-openapi-react-query-codegen-npm-compromised-august-2026.md) — the Bun-retrieval grammar precedent
- [SubQuery `@subql/common` release-pipeline compromise](subql-common-ci-artifact-substitution-release-pipeline-compromise-october-2026.md) — the same week's second valid-provenance malicious build
- [OSV stream watch](../notes/source-index.md) — high-water `MAL-2026-17649` at this writing, tensorlake mirror pending

## Sources

- StepSecurity, "Tensorlake npm Package Compromised: A Worm With a Hostage Token That Wipes Your Machine If You Revoke It" (October 8, 2026, full text captured by this wiki): <https://www.stepsecurity.io/blog/tensorlake-npm-compromised-hostage-token-worm>
- GitHub advisory `GHSA-rqxj-g25x-4v9v` (published Oct 8 02:54:39Z, critical, CWE-506, `= 0.5.144`)
- `tensorlakeai/tensorlake` issue #1014 (open, Oct 8 01:22:02Z) and live commit list (this wiki, GitHub API)
- npm registry time block + tarball 404, payload-file pulls and sha256 (this wiki, no execution)
- `iseekaigogo.com` DNS + HTTP probe (this wiki)
