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
