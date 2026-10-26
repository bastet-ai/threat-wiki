---
title: "@eforms/forms-api (npm) — OSV-first advisory on a LIVE dependency-confusion beacon canary: eight rungs in 40 minutes by a GitHub-less npm account, a FOUR-dist-tag grammar (latest/one/tildedwo/snapshot), two payload generations (preinstall.js 'Bugcrowd natwest-og PoC' → four-hook beacon.js), THREE independently ARMED oastify collectors on one name, and latest 2.99.1 fully installable while only 2.0.0-SNAPSHOT is advised (this wiki forensics, Oct 25, 205th sweep)"
---

# `@eforms/forms-api`: the machine lane advised ONE rung of an eight-rung live canary — and the other seven are nobody's advisory scope

**Observed:** OSV `MAL-2026-18252` published `2026-10-25T06:26:03Z` (origin `ossf-package-analysis`, import `06:27:19Z`); GHSA twin `GHSA-2cfq-pcr7-8572` minted `06:30:25Z` = **OSV→GHSA `+4 m 22 s`, OSV-first with `aliases: None` at birth**. Packument created `05:28:15Z`, publisher `tabaahi123 <hackingisfuture@gmail.com>`. This wiki captured the registry state, both payload generations (static extract ONLY, NEVER executed), and collector arm-state within `≈1 h 15 m` of birth.

**Disposition at capture (205th sweep, ~07:2x–07:4x UTC): LIVE AND INSTALLABLE.** `latest 2.99.1`, ALL EIGHT rungs tarball-`200`, jsDelivr versioned probe `200` (express control first). The advisory enumerates EXACTLY ONE version — `['2.0.0-SNAPSHOT']`, `ranges: None` — so the other seven rungs, including `latest`, sit OUTSIDE every published advisory scope. Whole-name consumers see a hit; version-diff consumers see nothing for `latest`.

## <a id="the-forty-minute-ladder"></a>The forty-minute ladder: what the `time` block records

One account, `05:28:15 → 06:08:05Z`, eight rungs in two bursts (`05:28–05:29` gen-1, `06:06–06:08` gen-2):

| version | published | hook generation |
|---|---|---|
| `0.0.0-stage` | `05:28:15Z` | none (staging stub) |
| `1.99.0` | `05:28:50Z` | gen-1: `preinstall` only |
| `2.99.0` | `05:29:16Z` | gen-1 |
| `99.0.0` | `05:29:18Z` | gen-1 |
| `1.99.1` | `06:06:38Z` | gen-2: four hooks |
| `2.99.1` (`latest`) | `06:06:43Z` | gen-2 |
| `2.0.99` | `06:07:57Z` | gen-2 |
| `2.0.0-SNAPSHOT` | `06:08:05Z` | gen-2 — **the only advised rung** |

**THE DIST-TAG SIGNATURE (new grammar on this ledger):** FOUR dist-tags on one packument — `latest → 2.99.1`, `one → 1.99.1`, `tildetwo → 2.0.99`, `snapshot → 2.0.0-SNAPSHOT`. `one` and `tildetwo` are not release channels anyone consumes; they are resolver TEST fixtures — a ladder built to check whether installers, mirrors, and scanners resolve tags correctly. Combined with the version grammar (`1.99/2.99/99.0/2.0.99/2.0.0-SNAPSHOT` spanning every comparison class a resolver can get wrong), the shape is a DIST-TAG/semver-resolution test harness wearing a package costume. Recorded as artifact behavior, not intent.

## <a id="two-generations"></a>Two payload generations, both self-declared research beacons (static read ONLY, NEVER executed)

**Gen-1 (`preinstall: node preinstall.js`, rungs `1.99.0/2.99.0/99.0.0`).** Tarball `2,020 B`. Header comment: *"Authorized security-research canary — Bugcrowd `natwest-og` dependency-confusion PoC… emits ONE DNS + HTTP beacon carrying the build host's identity (hostname, username, working directory)… reads no files, dumps no environment, always exits 0 so the installation it interrupted appears to succeed."* Mechanics match the prose: `depconf-<host>-<id>` label + `querystring` GET carrying `pkg/ver/id/host/who/pwd/platform/node/ci/uid` to two Burp Collaborator tokens `rpkfvtsptfrhcgbe62qg11ywjnpij6ma1cfpke.oastify.com` and `f6mk7lyjsuk3u1t49ypp9q2jbah15rtg.oastify.com`.

**Gen-2 (`beacon.js` wired into ALL FOUR lifecycle hooks `preinstall/install/postinstall/prepare`, rungs `1.99.1/2.99.1/2.0.99/2.0.0-SNAPSHOT`).** Tarball `1,560 B` (advised rung `sha256 aec8141b…`, this wiki's capture). `package.json` description: *"Security research canary for dependency-confusion testing. Emits one DNS and one HTTPS beacon carrying build-host metadata."* Mechanics: `dns.lookup` + `dns.resolve4` of `esc013-<host>-<stage>-<rand>.2z237udr1jxdaiw54xzmzfb7nytohszuplipn34fm4.oastify.com` + HTTPS GET `/<stage>?d=<base64>` with `host/user/cwd/platform/arch/node` and **the NAMES of twelve CI/env keys with their values** (`CI, JENKINS_URL, JOB_NAME, BUILD_NUMBER, GITLAB_CI, GITHUB_ACTIONS, TF_BUILD, BUILD_BUILDID, SYSTEM_TEAMPROJECT, npm_config_registry, NODE_ENV, npm_lifecycle_event`, values truncated `120 B`); a `/late-<stage>` re-beacon at `+4 s` keeps sockets alive before clean exit. UA `npm-canary/2.99.1`. Note the gen-2 upgrade is EXACTLY the `@wix-thunderbolt`/`ltidisafe` fleet grammar this ledger already hunts: installer identity + CI-flag inventory → publisher-held OAST collector.

**The standing rule applies unchanged:** publisher framing (Bugcrowd engagement, "canary", "authorized") is metadata, never exculpation (precedents on-wiki: `@pwaplatform` self-labeled canary → real exfil; `radio-player-theme` "XSS PoC" → live XSS; `react-dropzone-v4` CanaryToken squat). What IS behaviorally true here: a beacon, no file reads, no second stage, no persistence — recon-class. What is ALSO true: the name `@eforms/forms-api` is scope-confusion bait (a plausible private-scope name for any org with an "eforms" internal package — recorded as targeting shape, not asserted), so ANY incidental `npm install` of this public name feeds real victim hosts to the publisher's collectors, authorized engagement or not.

## <a id="collectors-armed"></a>Collector arm-state: THREE distinct Burp accounts on one package (control-first)

Fabricated-token control answered the stock `1,190 B` Collaborator page (per the Oct-6 armed-verification law: `200` is nothing, unique body is everything). All three recorded tokens answered SMALL UNIQUE bodies = ARMED:

- `rpkfvtsptfrhcgbe62qg…` → `61 B` body prefix `gy6potiqudrrqngc63dp…`
- `f6mk7lyjsuk3u1t49ypp…` → `55 B` body prefix `xttjqm3k12qrv8m8jc…`
- `2z237udr1jxdaiw54xzm…` → `65 B` body prefix `t0jypgkom5xef0knzsl4…`

Three DIFFERENT account prefixes on one package at one check — the gen-1 pair already had two accounts (`depconf` labels split across them); gen-2 added a third. The collectors outlive nothing yet (package is ~2 h old) — but per the ledger's collector law, expect these tokens to keep answering long after any takedown. **Hunt strings now:** the three token subdomains in resolver logs; UA `npm-canary/*`; `beacon.js` four-hook grammar in any manifest; the `one`+`tildedwo`+`snapshot` dist-tag triple on unfamiliar names.

## <a id="lane-shape"></a>Lane shape: OSV-first, GHSA 4½ min behind, queue blind, GitHub-less publisher

- **`aliases: None` at OSV birth, GHSA arrived `+4 m 22 s` AFTER** — the birth-only alias-join law (per the curated never-join test, Oct 16) predicts this record STAYS unaliased: GHSA/Dependabot-keyed consumers see the twin; OSV-only consumers see a different id. Watch `MAL-2026-18252.aliases` for a merge-join exception (the `arsya` precedent).
- **The `06:26Z` mint KILLED the ledger's own projection:** the standing `≈42 h` inter-wave law projected the next drip `≈Oct-26` — the drip came the SAME day, `≈20 h` early, as a single OSV-first record with no cohort. Wave-gap projections are per-batch rhythm, not a clock; a single OSSFPAM detection can arrive any hour.
- **ossf/malicious-packages queue search for the name: `total 0`** — the curated lane has never seen it; the machine lane alone carries it.
- **Publisher footprint:** `-/v1/search?text=maintainer:tabaahi123` = `total 1` (this name only); GitHub `users/tabaahi123` = `404` — npm-only account, no repo staging, no CI lane. The whole instrument is the packument.

## <a id="defensive-reading"></a>Defensive reading

1. **Advisory-scope arithmetic matters on this class.** One enumerated version + `ranges: None` + LIVE installable `latest` = a security product that flags-by-advisory-scope is silent on seven of eight rungs, including the one `npm install @eforms/forms-api` fetches.
2. **Four-hook lifecycle coverage (`preinstall/install/postinstall/prepare`) is the broadest hook grammar on this ledger** — it fires under most installer configurations short of `--ignore-scripts` entirely; `prepare` additionally fires on git-dependency checkouts.
3. **A dist-tag fixture on a confusion-bait scope name is hunt-able without any payload:** `curl -s registry.npmjs.org/<name> | jq '.["dist-tags"]'` — unexpected tags beyond `latest/next` on a young single-maintainer scoped name deserve a tarball look.
4. **`*.oastify.com` resolution from build hosts stays a first-class hunt signal** whatever the publisher claims — three new tokens on today's list.

## Monitor

- `MAL-2026-18252` `aliases` — does the `+4 m 22 s` GHSA merge in (join-class exception) or stay `None` (law holds)?
- Registry action on the name: hold/`404`/silence — and whether enforcement scopes the WHOLE name or just the advised rung (the advisory-scope differential is the test).
- Re-registration under other `@eforms` names or the maintainer's next move (`hackingisfuture@gmail.com`, GitHub-less).
- The three collectors' heartbeat pattern (armed-dark cycles, body stability) per the standing collector law.
- Whether `beacon.js`/`esc013-`/`npm-canary` grammar appears under any name claiming a real engagement.

## Cross-references

- [react-dropzone-v4 canarytokens preinstall beacon](../tools/react-dropzone-v4-npm-typosquat-canarytokens-preinstall-hostname-beacon-bane1010-october-2026.md) — the OOB-vendor-as-payload precedent and the "POC label never exculpates" rule
- [product-instructed npx squat pattern](../patterns/product-instructed-npx-command-unclaimed-package-name-squat-september-2026.md) — self-declared research framing → real victim leaks
- [Wix Thunderbolt confusion fleet](wix-thunderbolt-dependency-confusion-recon-fleet-npm-october-2026.md) — the CI-env-inventory → oastify collector grammar this canary copies
- [ltidisafe GCS-loader fleet](ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — collector-fingerprint verification law (unique body vs stock page)
- [205th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-25-one-hundred-and-forty-fifth-sweep) — lane context

## <a id="october-25-206th-second-sweep"></a>October 25 206th sweep — SECOND-SWEEP READ: LIVE-ADVISED, UNTOUCHED, AND THE JOIN LAW ANSWERS

`latest 2.99.1` unchanged, packument `modified` FROZEN `2026-10-25T06:08:05Z`, `2.99.1` tarball `200` = **second consecutive sweep LIVE under a live critical advisory with ZERO enforcement action** — armed-but-untouched clock `≈3.5 h` and climbing; the eight-rung, four-dist-tag shape stands whole. **THE JOIN-LAW TEST RESOLVES AGAINST THE MERGE: OSV `MAL-2026-18252` `aliases` STILL `None` `≈3 h` after the `GHSA-2cfq-pcr7-8572` twin existed, `modified` frozen `06:30:04Z` = the Oct-16 never-join law holds its live head-to-head against the `arsya` merge precedent — OSV-first records stay permanently invisible to alias-keyed reconcilers; consume GHSA + OSV as disjoint feeds (standing law, now with a birth-window-controlled experiment on the record).** The eighteen-name cohort minted the same morning around it (whole-name `>= 0` seizure at `09:33Z`) — this name was NOT seized: single-rung-scoped records (`['2.0.0-SNAPSHOT']`) draw no automaton, and the enforcement asymmetry between scoped and whole-name records is now observable on the same clock face. Sweep context → [206th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-25-one-hundred-and-forty-sixth-sweep).

## <a id="october-25-207th-third-sweep"></a>October 25 207th sweep — **THIRD SWEEP, STILL LIVE, STILL TOUCHED NOTHING: `latest 2.99.1`, packument `modified` FROZEN `2026-10-25T06:08:05Z`, armed-but-untouched clock `≈11 h` — and the singleton it was is now a cohort: the same-day `MAL-2026-18271`–`18293` batch proved the OSV-first live-advised state is the DEFAULT disposition on this lane, `≈20` names installing under fresh records while the GHSA-lane name `w-mousekey` got eaten in `≈1.5 h`**

The scope differential stands unchanged (OSV enumerates ONLY `2.0.0-SNAPSHOT`, seven-eighths of the rungs including `latest` outside every scope); the `MAL-2026-18252` `aliases None` join-law answer recorded 206th is now corroborated cohort-wide: all twenty-two OSV-first siblings ALSO carry `aliases None` zero-GHSA. The live-advised class the canary defined at birth is the lane's majority disposition, and the enforcement asymmetry it exposed (GHSA-aliased names get the seizure automaton; OSV-first names get a text record and a running installer) is now measured at fleet scale → [wave-three 207th](testmetest-wave-three-osv-batch-agent-tooling-ghsa-at-birth-enforcement-asymmetry-october-2026.md#october-25-207th-the-fleet-that-outlived-its-own-advisories).

## <a id="october-26-219th-follow-up"></a>October 26 219th sweep follow-up (~17:3x UTC): **THE SCOPED-RECORD IMMUNITY CLASS DIED IN THE WAVE — `≈1.5 MIN` FROM GHSA TO HOLDER**

`GHSA-39p9-96vf-fxjh` minted `16:21:38Z` in the enforcement wave; packument reads `0.0.0-stage` `16:20:53Z` → holder `0.0.1-security` `16:23:05Z` — all eight advised-and-unadvised rungs (`1.99.1`…`2.99.1`, `2.0.0-SNAPSHOT`) now time-map ghosts, version objects only the stage + holder pair. The 206th's law — "scoped records draw no seizure automaton; enforcement asymmetry on one clock face" — is FALSIFIED: @eforms was the class specimen for `≈35 h` and the automaton took it in `≈1.5 min` once the ghsa-malware bot's live pass NAMED it. The asymmetry was never record-scope-keyed; it was lane-keyed (bot-lane names die, mirror/OSV-only names live). BONUS MEASUREMENT: OSV `18252` — the 205th's own birth-record, `aliases None` through the `arsya` challenge and two law-revisions — RETRO-JOINED `GHSA-39p9` at the `16:45:06Z` tick: the never-join law died on this page's own record.
