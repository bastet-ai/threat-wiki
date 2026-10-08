# MALFEX: one Portuguese-language npm operator, twelve packages, two delivery arms, three years of continuity — and the advisory pipeline's gap made visible: `function-flag` sat as a malicious postinstall with NO advisory for fourteen months, and `cdn-img-fetch` stayed installable after npm seized its parent

## Tags
- ops
- npm
- supply-chain
- malicious-package
- operator-continuity
- Overlord-RAT
- AutoIt
- Solana-C2
- Discord-stealer
- process-hollowing
- Windows
- CloudSEK
- takedown-gap

## Summary

CloudSEK (Sep 30, 2026) names **MALFEX**: an npm supply-chain operation running **August 2023 → September 2026** under a single operator publishing through Portuguese-language accounts. Twelve npm packages across at least eight publisher handles, one GitHub payload repo. Five packages carry OSV `MAL-` advisories (all issued by Amazon Inspector Sep 22–28, 2026); **three are malicious and unadvised — and those three are what's live today**; four are benign public tools shipped as reputation cover. The operator's identity is self-attested inside their own artifacts: the hardcoded key-derivation constant **`malfexteam2027`** is literally the operator's team name, word-for-word in the `function-flag@1.7.3` README ("criado pela equipe Malfex, cujo dono é Murizada"), across five publisher handles (`malfexkkj`, `malfex_user`, `malfexteste2/3/4`), and the git author email of the payload repo (**`corpmalfex@gmail.com`**, GitHub account `cavecrew`, display name "muriel", commits at UTC-0300 = Brazil).

| Arm | Packages | Delivery | Payload |
|---|---|---|---|
| **A** (advised trio + wrappers) | `tlxbnhd`, `tldriver`, `mxdriver` (co-advised), wrappers `native-runner`→`img-to-native` (seized, MAL-2026-17218) | Download PE disguised as `image/png` from `api.imghippo.com` → IExpress cabinet → **signed AutoIt3 interpreter** + EA06-encrypted a3x (cycled-XOR strings, RC4 key `8448433`, LZNT1) | **Overlord RAT** build (open-source Go RAT, Jamf Aug 6 2026 fake-Zoom macOS campaign — whose "initial delivery vector still under investigation" line this report answers: npm) |
| **B** (one arm still live) | `img-to-native` (seized), **`cdn-img-fetch` (LIVE)**, **`function-flag` (LIVE, malicious postinstall since 2025-07-18, zero advisories for 14 months)**, **`function-color` (LIVE wrapper pulling `function-flag`)** | PNG polyglot from `raw.githubusercontent.com/cavecrew/proj`, decrypted with the `malfexteam2027` key → fetch 64 MB Node.js bundle (`movinlike`) from `104.234.65.75:700` | Node.js stealer: injects Discord clients (token/account theft), browser cookies/credentials/wallets, Telegram `tdata`; exfil to a **live Discord webhook** |

## The durable findings

1. **Advisory-per-package is a structural blind spot.** CloudSEK's core argument: each individual `MAL-` advisory is *accurate* and collectively *incomplete* — they never connect the dropper trio, the parent, and the dependency into one operator with two arms. The concrete failure: **Amazon Inspector's own `MAL-2026-17216` for `img-to-native` NAMES `cdn-img-fetch` as a companion dependency in its text while `cdn-img-fetch` remained installable** — the advisory contained the takedown lead and nothing consumed it. Rule: **whenever a registry seizes a package, every declared dependency in its manifest needs its own review** — the takedown-vs-dependency gap is where live arms survive.
2. **A fourteen-month unadvised malicious postinstall.** `function-flag` (latest `1.7.3`, `postinstall: node example.js`) has been continuously malicious since **July 18, 2025** with zero advisories until CloudSEK's report; this wiki verified at check: **still serving** (1.7.3 latest; versions incl. 3.0.0/4.0.0, 533 downloads/wk), **OSV name-query: zero records**. `cdn-img-fetch` 1.0.4 live, 643 downloads/wk, zero OSV records. `function-color` live (2 dl/wk, zero OSV). Three live malicious names with real install bases, invisible to advisory-keyed tooling.
3. **First observed LIVE Solana C2 in the wild Overlord build.** Jamf's August write-up described Overlord's Solana-memo C2 resolver as "present but disabled"; this build wires it with live literal strings, i.e. the blockchain channel is actually operational. Also answers Jamf's open delivery-vector question: npm.
4. **Burner-per-package operator tradecraft with a self-owned constant.** Fresh npm account + randomized iCloud email for nearly every package, yet one constant (`malfexteam2027`) ties it all — the operator's branding instinct beat their opsec. The GitHub account publicly ships the campaign's two techniques (a Windows credential stealer + a process-hollowing PoC) = self-citation across platforms.
5. **Cover-package hygiene:** four benign packages (e.g. `centralizemiddle`) exist purely as reputation; account age and "some packages are clean" defeat naive publisher-reputation scoring.

## Persistence / hunt artifacts (CloudSEK)

- `%LOCALAPPDATA%\ScopeSmart Technologies Inc\AutoIt3.exe` (signed-AutoIt drop under a fake vendor dir)
- Scheduled task `\Maiden`
- Egress: `api.imghippo.com` (Arm A payload host), `104.234.65.75:700` (Arm B 64 MB bundle), `raw.githubusercontent.com/cavecrew/proj` (polyglot host), the campaign Discord webhook (live at CloudSEK's writing)
- Dropped names: `gldriver_pre_core.exe`, `gldriver_pre_asset.exe`
- String across four publishers + malware internals: `malfexteam2027` (the KDF constant is itself a hunt string)
- Registry: block `function-flag`, `cdn-img-fetch`, `function-color`, plus wrapper `function-color`→dependency chain; review any manifest declaring `cdn-img-fetch`

## This wiki's live state (October 1 ~11:30–12:00 UTC)

- `function-flag` **200, still serving 1.7.3** with the `postinstall: node example.js` hook intact, zero OSV by name-query. `cdn-img-fetch` **200, 1.0.4**, zero OSV by name-query. `function-color` 200, zero OSV. **Three-for-three: CloudSEK's "unadvised and live" claim held at our check ~48 h after publication — no advisory landed in the interim.**
- Advised-side mirror intact: `tlxbnhd` carries `MAL-2026-16385` (inside this wiki's tracked backlog-wave ID range).
- Watch: whether npm acts on `function-flag` (14-month survivor), whether an advisory batch covers the three live names, `104.234.65.75:700` liveness, Discord webhook lifecycle, and whether Amazon Inspector revises `MAL-2026-17216` to flag the dependency it named.

## Sources

- CloudSEK (Vikas Kundu et al.), "MALFEX — A malicious npm postinstall no advisory has caught for fourteen months," Sep 30, 2026 — full text captured by this wiki Oct 1 (exec summary + what's-new sections verbatim; full PDF at cdn.cloudsek.com) — https://www.cloudsek.com/blog/malfex-malicious-npm-postinstall-supply-chain-campaign
- Related: CloudSEK "TOPHIT Part 1" (Sep 29) — a SEPARATE one-operator npm typosquat flood (`@prime0`, 85 scoped packages in 3 min 13 s on Sep 15, generic 30-second shell-polling agent to `69.48.229.140:8080`, name-generator: delete one of the first three chars of a top-29 library; scope since removed from npm — 404 at this wiki's check; C2 port dead at this wiki's check) co-hosted with the VHX Harvester vast.ai GPU-cryptojacking panel — shared infrastructure, not shared victims.
- This wiki: npm registry liveness + download counts + OSV name-queries on `function-flag` / `cdn-img-fetch` / `function-color` / `tlxbnhd` / `@prime0/fhalk`, egress probe on `69.48.229.140:8080`, Oct 1 ~11:30 UTC.

## <a id="october-1-iteration-followup"></a>October 1 same-day follow-up: the named dependency ITERATED THROUGH ITS OWN EXPOSURE — two versions published after the report, one advisory that misses the live range

This wiki's thirty-sixth sweep (~15:05–15:25 UTC Oct 1) caught **`cdn-img-fetch` actively evolving across the campaign's own exposure window** (npm `time` block pulled by this wiki; CloudSEK published Sep 30):

| Version | Published (UTC) | Import-time behavior (this wiki unpacked every tarball) |
|---|---|---|
| 1.0.0 | Sep 26 02:18 | IIFE fetch `raw.githubusercontent.com/cavecrew/proj/main/banner.png` → hidden dotfile `os.tmpdir()/._cif_data` (the MAL-2026-17320 shape) |
| 1.0.1 | Sep 26 03:03 | same shape |
| 1.0.2 | Sep 28 04:52 | fetch URL renamed `banner.png` → cache `package/.cache/banner.jpg` (still the `.png` URL) |
| **1.0.3** | **Sep 30 03:43** | **fetch URL switches to `banner.jpg`** — points at a DIFFERENT staged file |
| **1.0.4** | **Sep 30 23:07 (same day CloudSEK published)** | **import-time fetch REMOVED** — pure `fetchAndCache` utility; `getCachePath()` returns `null` |

All five versions carry **no install hooks** — the drop is `require()`-time, so `allowScripts`-style controls never see it. `banner.png` (8,231,030 B) and `banner.jpg` (6,204,416 B) both still serve 200 from the still-live `cavecrew/proj` repo, which was **re-pushed at 2026-09-30T00:18:28Z** — the staged next-stage blobs are being actively maintained, and neither starts with JPEG magic bytes (first bytes of `banner.jpg`: `d9 c3 43 69 …`) = encrypted stage material, not an image.

**Advisory state at check:**
- **`MAL-2026-17320`** (Amazon Inspector, published Sep 30 04:38 UTC) now exists for `cdn-img-fetch` — but it covers **1.0.0–1.0.1 ONLY**, describes the superseded `._cif_data` shape, and was last modified Sep 28. **The live install-target range 1.0.2–1.0.4 is ADVISORY-FREE.** One MALFEX name now has a record; `function-flag` and `function-color` remain at zero.
- Zero GHSA (package-name GHSA queries return the generic recent-advisories list = no malware record for any MALFEX name).
- npm has taken no action on any of the three live names; `104.234.65.75:700` (Arm B bundle host) **still OPEN** at this check.
- `function-flag` unchanged (1.7.3, modified Aug 2025, 533 dl/wk, still zero OSV). `function-color` **2 dl/wk** (was 2 — wrapper) still zero OSV. `friendly-tools`/`friendly-greeting-tools` (the Sep 30 kam193 Snowflake pair) still 404 on PyPI.
- Publisher field unchanged (`devtools-community`) = no account rotation yet.

**Durable reads (this wiki):**
1. **Public naming did not pause the operator.** Both new versions landed on/around the report day: 1.0.3 on Sep 30 03:43 UTC and 1.0.4 at Sep 30 23:07 UTC, the same day CloudSEK's write-up went out — and the payload host repo was re-pushed Sep 30 00:18 UTC. Expect the live names to keep churning regardless of press coverage — takedown, not advisories, is the only stop.
2. **1.0.4's fetch removal is ambiguous and must be tracked, not trusted.** Either (a) pre-takedown cleanup (the PhantomSub `ishumdz-bail` precedent on this wiki: malware removed after exposure ≠ cleared package, re-insertion is one publish away) or (b) a deliberate dormancy switch — the utility now `require()`s clean, which lowers detection salience while the `cavecrew` infra stays live and re-pushed. Both readings say: never treat a clean-latest on this rail as clearance.
3. **The advisory lag is a version lag, not just a package lag.** MAL-2026-17320 was written against 1.0.0/1.0.1; the versions actual installs resolve (643 dl/wk flowing to `latest` = 1.0.4) sit outside its range. Advisory-keyed blocking with version ranges passes 1.0.2–1.0.4 silently. The registry `time` block — not the advisory — is the truth surface for a package under active iteration.
4. **Hunt update:** monitor the `cavecrew/proj` repo's push events and the sizes of `banner.png`/`banner.jpg` as the campaign's heartbeat; ANY new `cdn-img-fetch` publish, ANY re-add of a fetch line to `index.js`, or ANY size change on the two banner files = the operator is still operational after public naming.

## <a id="october-7-enforcement"></a>October 7 same-day enforcement: the three unadvised live names GOT ADVISED at 20:48–20:51Z — and the takedown that followed put a WORSE version back on `latest`

This wiki's one-hundred-and-seventh sweep (~20:55–21:35 UTC Oct 7) caught the full enforcement sequence on this page's three names live, inside a 45-minute window, eight days after CloudSEK's report and six days after this wiki's verification:

**(1) THE ADVICE BATCH — three GHSAs, 20:48:28–20:51:33Z:** `GHSA-ggcg-4pv7-wf9m` (`function-flag`, `= 1.7.3`), `GHSA-m6cg-6crx-mggv` (`function-color`, `= 1.0.0` AND `= 1.7.3`), `GHSA-v3rj-w7v4-jcfx` (`cdn-img-fetch`, `= 1.0.0` AND `= 1.0.3`). All zero-CVSS malware-class, standard "fully compromised" text. OSV forward-mirror arrived ~21:30Z — as TWO NEW sequential IDs, `MAL-2026-17647` = `function-color` and `MAL-2026-17648` = `function-flag` (fresh names, no prior MAL history = the one-hundred-and-fifth's mirror-dedupe rule correctly fires the OTHER way: no history → new sequential ID), while `cdn-img-fetch` got NO new ID — its GHSAs aliased into the existing `MAL-2026-17320`, which was REWRITTEN in place from `versions: [1.0.0, 1.0.1]` to `[1.0.0, 1.0.3]`. **HIGH-WATER `17648`, RESUME `17649`.**

**(2) THE ONE-HUNDRED-AND-SIXTH'S PENDING-MIRROR COUNT CORRECTS ITSELF:** that sweep's walk saw `17647`–`17653` at `code:5` and concluded the stream was quiet. The records were minted at 20:48–20:51Z, DURING the following sweep — the walk was ~40 min early, not wrong. Control discipline (probe the known-good id in-walk) again prevented over-reading; `code:5` means record-not-yet-created, and on an active day that can be minutes from false.

**(3) HEADLINE — THE `function-flag` TAKEDOWN REGRESSED THE PACKAGE:** this wiki read the npm `time` block at ~21:1xZ: malicious `1.7.3` was **unpublished at 20:48:02.593Z — 26 seconds BEFORE its own GHSA published 20:48:28Z** (holder-first shape on the abuse lane). Then npm's standard security-holder flow created `0.0.0-stage` 20:54:05Z + `0.0.1-security` 20:59:24Z — **but `function-flag`'s `latest` is NOT the holder: it is `4.0.0`, a version CloudSEK's own report lists in the MALFEX malicious-version set.** This wiki pulled the `4.0.0` tarball (no execution): `postinstall: node example.js` intact, and `index.js` carries an armed `as()` stager — `axios`-streams `https://apicdn.squareweb.app/attachments/1392577835742265576/1395570372077682768/svchost.exe` to `%APPDATA%\malfex.exe` and `exec`s it with `windowsHide` (sha256 of tgz `749c8032…`). The `3.0.0` tarball carries the SAME stager via a Discord-CDN attachment proxied through `bypasscdn.onrender.com`, and `4.0.0` is the SAME Discord channel/message attachment IDs reached through a new front, `apicdn.squareweb.app` = the operator rotated the C2 front, not the payload. The earlier 2.3.4 pull is clean (pure figlet wrapper) = the same account's clean→malicious version alternation this page's Oct 1 section already modeled. **DURABLE: a `0.0.1-security` holder is NOT a takedown guarantee — read `dist-tags.latest` after ANY security-holder event; if the name has multiple malicious versions, the seizure can land while a malicious `4.0.0` keeps serving (4.0.0 was still indexed when this wiki queried, 669 dl/wk, downloads API going 0/day Oct 6–7).**

**(4) VERSION-SPECIFIC ADVICE, LIVE CONFIRMED BLIND SPOTS:** `function-flag` is advised as `= 1.7.3` ONLY — the malicious live `latest` `4.0.0` is OUTSIDE every advisory range on the name (`MAL-2026-17648` also lists `1.7.3` only). `cdn-img-fetch` advised `= 1.0.0` + `= 1.0.3` while LIVE latest `1.0.4` (1,142 dl/wk) and installing `1.0.2` stay uncovered — the Oct 1 "advisory lag is a version lag" read confirmed for a second consecutive batch; `1.0.4`'s fetch-line removal (this wiki's clean-latest-≠-clearance flag) stayed exactly right.

**(5) INFRA COLLAPSE INSIDE THE WINDOW (this wiki's probes):** `cavecrew/proj` → 404 (repo gone, was re-pushed Sep 30); `banner.png`/`banner.jpg` → 404 (the campaign's published heartbeat died mid-sweep); `apicdn.squareweb.app` attachment → 404; `bypasscdn.onrender.com` → connection-fail; the raw Discord attachment → 404. Only `104.234.65.75:700` still answers (HTTP 404 = port open). Read: platform-side enforcement (GitHub repo + Discord attachments) closed this operator's public rails faster than npm closed its package names — and the `4.0.0` stager now points at a dead front, so installs fail silent rather than beacon. Silent ≠ removed.

**(6) THE 14-MONTH CLOCK, MEASURED:** `function-flag` was continuously malicious from Jul 18 2025 to Oct 7 2026 20:48Z = **~14.7 months unadvised**, advised ~8 days after CloudSEK named it, purged the same minute its advisory published. CloudSEK's report is the proximate cause; the pre-existing `MAL-2026-17320` version-drift story shows machine advisories track the package, not the campaign.

**(7) CURATED-LANE HEARTBEAT:** PRs #1604 + #1605 from yesterday (the Tailwind trio + `css-reading-display-polyfill`) remain OPEN with their subjects ALL STILL LIVE at this check (`2.0.6`/`2.0.6`/`2.0.7`/`1.0.0`, registry `modified` fields unchanged) = as of this sweep, abuse-lane takedown has NOT followed curated filing without relay marks — the one-hundred-and-sixth's live test still running.

**Monitor:** `17649`+ with control; whether npm re-seizes `function-flag` `4.0.0` (or the advice/range ever extends); `cdn-img-fetch` `1.0.4` registry action; `104.234.65.75:700` finally closing; any re-registration under `malfex*`/cavecrew-adjacent handles; #1604/#1605 subject lifetimes as the relay-test control.

## <a id="october-8-imgbundle-decoder"></a>October 8 one-hundred-and-eighth sweep (~23:05–01:50 UTC): THE DECODER HALF OF THE `cdn-img-fetch` STAGED DROPPER SURFACES IN THE SAME ENFORCEMENT NIGHT — `imgbundle` carried a public OSV malware record since Sep 30 and stayed INSTALLABLE for seven days (805 dl/wk) until tonight, when GitHub's malware bot + the npm holder took it out in a 104-second window

**(1) THE ADVISORY — `GHSA-hj6h-6xgx-mpjv`, `imgbundle`, critical, CWE-506, published 23:06:15Z, versions `= 1.0.0` + `= 1.0.1` + `= 1.0.2`, no CVE.** The GHSA carried no mechanism text, but the name's EXISTING OSV record `MAL-2026-17330` (published Sep 30 04:50:10Z, amazon-inspector origin, `1.0.0`/`1.0.1` imported Sep 30 05:19Z) does, and it describes this campaign's sibling dependency: the package advertises an image bundler, but on `require` a top-level IIFE reads an AES-256-CBC-encrypted file at `cdn-img-fetch/.cache/banner.jpg` INSIDE the declared sibling dependency `cdn-img-fetch`, decrypts with a hardcoded key derived from `sha256('nif-runtime-2027')`, writes the plaintext to `cdn-img-fetch/.runtime/rt.jpg`, deletes the source file, and registers an `fs.watch` on the source directory so the decrypt-and-stage step still fires if the encrypted blob is delivered LATER; an error-recovery path calls `cif.ensureCached()` on `cdn-img-fetch`, wiring the two names as one coordinated staged dropper — `cdn-img-fetch` supplies the encrypted bytes, `imgbundle` is the decoder that materializes attacker-controlled content onto the installer's filesystem at import time.

**(2) THE FAMILY LINK, RECORDED-NOT-ASSERTED:** `cdn-img-fetch` is this page's own name — advised two hours earlier tonight (`GHSA-v3rj` 20:51:33Z; `MAL-2026-17320` rewritten to `[1.0.0, 1.0.3]`), with LIVE `1.0.4` (1,142 dl/wk) still outside every advisory range. The KDF-constant grammar also rhymes: MALFEX's self-named `malfexteam2027` vs `imgbundle`'s `nif-runtime-2027` — same `-2027` suffix — and `banner`-named blobs appear on both sides (the MALFEX heartbeat `banner.png`/`banner.jpg` died 404 tonight; `imgbundle` reads `banner.jpg` as its payload carrier). No identity claim; the asserted fact is the dependency edge `imgbundle → cdn-img-fetch` plus tonight's shared enforcement window.

**(3) THE GAP MEASURED — OSV-ADVISED ≠ INSTALLABLE-BLOCKED:** `imgbundle` carried a public OSV malware record from Sep 30 and was still resolving and downloading through this wiki's checks (805 dl/wk in the Sep 28–Oct 4 window). Amazon Inspector saw it on day zero; the GHSA lane took SEVEN DAYS to catch up; the holder lane then took 104 seconds once it did: `0.0.0-stage` 23:06:01.538Z (13.5 s BEFORE the GHSA — third stage/holder-first instance on record), GHSA 23:06:15Z, `0.0.1-security` holder 23:07:45.935Z; all three versions gone, tarballs 404 at this wiki's re-pull, registry now `latest` = `0.0.1-security`, maintainer `npm`. Second concrete instance of the `spf-analytics` pattern (six weeks there, seven days here): the GHSA catch-up clock is a distribution, not a constant, and OSV-only visibility buys consumers a warning while leaving the registry arm silent.

**(4) MIRROR-DEDUPE RULE CONFIRMED AGAIN:** `GHSA-hj6h` ALIASED into the EXISTING `MAL-2026-17330` (ghsa-malware origin block imported 23:23:59Z, record modified 23:30:04Z) with ZERO new sequential ID — the machine lane again dedupes history-carrying names into their existing records instead of minting fresh IDs.

**(5) SIBLING CONTRAST — SEIZURE COMPLETENESS VARIES PER NAME:** `function-color`'s seizure is COMPLETE at this re-check (all versions gone, `latest` = `0.0.1-security`, 54 dl/wk week total), while `function-flag` is STILL serving malicious `4.0.0` as `latest` at 01:44Z — ~5 h after the holder event, no re-seizure, no range extension. The standing alert is confirmed on itself: nobody noticed the regression. One enforcement batch, three dispositions: complete seizure (`function-color`), incomplete seizure still serving a malicious `latest` (`function-flag`), and a name whose clean-looking surface today hid a seven-day-advised decoder (`imgbundle`).

**Monitor:** whether `cdn-img-fetch` `1.0.4` (still live, still uncovered) ever re-adds the fetch/`banner.jpg` line that makes `imgbundle`'s decoder resolve; whether `MAL-2026-17320` extends past `1.0.3`; whether anyone re-seizes `function-flag@4.0.0`; any NEW name declaring `cdn-img-fetch` as a sibling = decoder-adjacency hunt key.

## <a id="october-8-one-hundred-eighth-recheck"></a>October 8 one-hundred-and-ninth sweep (~03:26–03:55 UTC): THE STANDING ALERT CONFIRMS ITSELF A SECOND TIME — `function-flag` `dist-tags.latest` IS STILL MALICIOUS `4.0.0` ≈6.5 h after the holder event, nobody re-seized — and the surgical-purge shape gets MEASURED: `cdn-img-fetch`'s surviving version list `[1.0.1, 1.0.2, 1.0.4]` shows npm deleted EXACTLY the two GHSA-named versions, leaving `1.0.2` (inside the REWRITTEN OSV range) and uncovered `1.0.4` standing = registry action follows the GHSA range, not the OSV rewrite

Registry re-reads at this sweep: `function-flag` — versions `[2.3.4–2.3.9, 3.0.0, 4.0.0]`, `latest: 4.0.0`, `modified` frozen at the 20:48:02.593Z holder event = unchanged since the one-hundred-and-seventh's regression discovery; the armed `4.0.0` stager now points at dead fronts (installs fail silent) but the name still serves it as `latest`. `function-color` — `[0.0.0-stage, 0.0.1-security]` only: seizure COMPLETE, the contrast case holds. `imgbundle` — `[0.0.0-stage, 0.0.1-security]`, `latest` = holder: seizure complete, the seven-day-advised decoder is gone. `cdn-img-fetch` — `[1.0.1, 1.0.2, 1.0.4]`, `modified` 20:52:07.071Z: **the version list is the forensic artifact** — GHSA named `=1.0.0` + `=1.0.3`, registry deleted `1.0.0` and `1.0.3` and NOTHING else; `1.0.2` (inside the OSV record's rewritten `[1.0.0,1.0.3]` range) and `1.0.4` (outside every advisory, 1,142 dl/wk) both still resolve = for multi-version malware names, GHSA-range-following purges leave OSV-range siblings installable — durable: after a purge, diff the SURVIVING version list against the OSV record, not just the GHSA. Infra: `104.234.65.75:700` still answers 404 (port open, sole survivor re-confirmed); `cavecrew/proj` raw path still 404. Monitor unchanged: re-seizure of `4.0.0`; `1.0.4` fetch-line re-add; any `malfex*`/cavecrew re-registration.
