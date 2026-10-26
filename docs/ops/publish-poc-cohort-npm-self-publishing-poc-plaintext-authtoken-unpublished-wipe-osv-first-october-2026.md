# publish-poc cohort — the self-publishing publishing-PoC trio: cleartext npm token shipped to every installer, whole-name `unpublished` wipe ~9–13 h BEFORE the first advisory arrived, ZERO GHSAs, and the wipe-roster as the only surviving census

## Tags
- ops
- npm
- supply-chain
- malicious-package
- npm-token-theft
- self-publishing
- publishing-poc
- osv-first
- enforcement-asymmetry
- unpublished-wipe
- this-wiki-forensics

## Summary

`MAL-2026-18323` (`publish-poc-base@1.0.7`) and `MAL-2026-18324` (`publish-poc-test3@1.0.15` + six more rungs) minted `2026-10-26T06:31:13Z` / `06:30:51Z` — origin `amazon-inspector`, **`aliases: None`, ZERO GHSAs at capture** — the first OSV records for a three-name npm cohort whose packuments were created Oct-22/23 and **wiped whole-name via the `unpublished` time-map grammar ~9–13 h BEFORE either advisory existed** (`2026-10-22T20:22:36Z`, `2026-10-23T17:20:46/48Z`). Third name `publish-poc-test`: packument alive, ALL versions gone from its time map (even the Oct-23 `0.0.0-stage` rung), zero advisories, `modified` frozen at its own wipe — the wipe clock spans three packuments inside a ~5-minute window. Payload (per the OSV/amazon-inspector text, static-only, NEVER executed by this wiki): a postinstall that **publishes a fabricated package into the installing environment's OWN npm auth context** (`~/.npmrc` `_authToken` / `NPM_TOKEN`), reconstructing the string `npm publish` from printf fragments (`'np'+'m pu'+'blish'`) to dodge manifest/string scanners — an account-takeover amplifier that needs no victim-side exfil channel. `publish-poc-base` additionally **ships a hardcoded npm `_authToken` in cleartext to every installer** (`npm_DLcrGeNT…` prefix). The naming (`publish-poc-*`, self-mints `publish-poc-found-<rand>`) reads as security-testing activity — intent NOT asserted; the durable read is that OSV-first advice on a dead-payload cohort stayed dark ~16 h while any re-registration of three bare names would install first and be advised ~16 h later.

## The three packuments (direct reads, Oct 26 ~07:3x–08:0x UTC)

| | `publish-poc-base` | `publish-poc-test3` | `publish-poc-test` |
|---|---|---|---|
| created | `2026-10-22T13:33:42.703Z` | `2026-10-23T01:43:54.567Z` | `2026-10-23T11:38:03.959Z` |
| grammar | `0.0.0-stage` same second as created | `0.0.0-stage` same second as created | `0.0.0-stage` same second as created |
| ladder | `1.0.3` `1.0.5` `1.0.7` (15:03→18:51Z) | `1.0.15`…`1.0.27` seven rungs `06:58→11:01Z` | none after stage |
| wipe | `unpublished` `20:22:36.265Z` — all 4 versions | `unpublished` `17:20:48.722Z` — all 8 versions | time map carries ONLY created/modified — stage rung DELETED (third wipe subtype) |
| advised | `1.0.7` | `1.0.15/18/19/21/22/26/27` (every rung) | — (OSV `{}`, ZERO advisories) |
| advisories | `MAL-2026-18323`, `aliases None` | `MAL-2026-18324`, `aliases None` | ZERO |

- Packuments now answer with skeleton `_id/name/time/_rev` only: no `dist-tags`, no `versions`, no `maintainers` — the **whole-name `unpublished` wipe** variant of the history-delete law (vs single-version pull `numbors`, vs rollback-to-stage `dsh-native`).
- Advised tarballs `404` on the registry AND jsDelivr (`express` controls `200` first — controls-first law applied).
- `npm search` for `publish-poc` surfaces NONE of the three names while their packuments answer `200` = the search lane is silent on wiped names (same enforcement-lane split as the s4yhii scope).
- GHSA: none for any of the three names; the GHSA malware-lane head this window is the `06:30Z` NocoDB/Yoosee legit-import batch — the machine lane (amazon-inspector) advised first, ~16 h after the packuments died.
- **The advised versions ARE what `malicious-package-publish-poc` installs.** The advisory class itself carries an install path (the wiki's own wave-naming precedent: `testmetest`): `npm i malicious-package-publish-poc` is a live tripwire on any of these bare names the moment they re-register.

## The payload (per OSV source text — amazon-inspector; this wiki static-reads the ledger, NEVER executed the package)

- `publish-poc-test3` postinstall: `mktemp` → writes a fabricated `package.json` named `publish-poc-found-<random-hex>` (suffix via `openssl rand -hex 2`) → **runs `npm publish` from the temp dir against the public registry using the INSTALLER's own auth context** (`~/.npmrc` `_authToken`, `NPM_TOKEN`). The command string is assembled at runtime from three fragments — `'np'` + `'m pu'` + `'blish'` — via `printf`, explicitly to defeat manifest/string scanners.
- `publish-poc-base` postinstall: reads the first line of the installer's parent-workspace `README.md` as the staged package's description (victim-workspace fingerprinting), writes a `.npmrc` containing a **hardcoded `_authToken` (prefix `npm_DLcrGeNT…`) pointing at `registry.npmjs.org`** — a live credential distributed in cleartext to every installer — then `rm -rf` the staged dir before any publish/network call fires (this rung does not itself publish; the shipped token is the exposure).
- The `publish-poc-found-<rand>` self-mint grammar means successful runs spawn CHILD packages on the registry: the worm footprint is *published* packages, not dropped files. `publish-poc-found` itself `404`s at capture (zero found-rungs surfaced to the search lane — either the automaton ate them or none ever published).

## The laws this cohort proves or extends

1. **THE SLEEPER ADVISORY, npm edition.** Advice arrived ~16 h after the payload was already dead. The 213rd's published-clock law generalizes: on this lane `published` (06:31Z) is a *report-authoring* timestamp, not a first-seen clock — the registry events it describes are 3–4 days old and the seizure happened without any advisory. Consumers keying blocks to advisory arrival would block nothing (payload already 404) and consumers keying to `published` missed the entire registry-side event.
2. **The wipe precedes the paperwork.** `publish-poc-test` was wiped `17:20:46Z` Oct-23 and STILL has zero advisories — enforcement acted on evidence this wiki has never seen a record of. The unpublished-wipe lane runs on its own intel.
3. **Whole-name `unpublished` wipe is a THIRD time-map disposition**: (a) single-version object pull with time-map survivor/erasure (`numbors`, `dsh-native`), (b) holder-costume (`0.0.1-security` cohorts), (c) whole-name `unpublished` dict with per-version roster — and its sub-variant where even the wipe roster is erased (`publish-poc-test`, whose time map lost its stage rung entirely). The `unpublished` dict's version list is the ONLY surviving census of what these names ever shipped — read it before it, too, is erased.
4. **printf-split `npm publish` is a durable hunt string.** Any lifecycle script assembling commands from fragments (`'np'+'m pu'+'blish'`) is evasion with intent; the same shape appears in the wiki's eforms four-hook beacon grammar. Detection: `grep -rE "printf.*(np).*(m pu)|(m pu).*blish" postinstall scripts`.
5. **A shipped token is its own IOC.** `npm_DLcrGeNT…` is rotatable, so it dates the campaign window; hunt npm audit logs for auths with that token prefix and any `publish-poc-found-*` mints on internal accounts.
6. **`publish-poc-base` reads a workspace README as its package description** = pre-recon of the installing project — the same install-time victim-profiling grammar as the capsense/eforms beacons, aimed at the workspace instead of the host.

## Hunt strings

- Names: `publish-poc-base`, `publish-poc-test3`, `publish-poc-test`, any `publish-poc-found-<4hex>` mint (registry publish-event alert on the prefix).
- Token prefix `npm_DLcrGeNT` (`.npmrc` files, npm request logs, CI secret-scanner retro-scan).
- Grammar: postinstall that (a) writes `.npmrc` with `_authToken`, (b) assembles `npm publish` from fragments, (c) reads `../README.md` at install time.
- Tripwire: the three wiped names re-registering = live-installable with ZERO advisories for ~16 h on the observed clock; `malicious-package-publish-poc` installs whatever lands.

## Disposition at capture (Oct 26 ~08:0x UTC, 214th sweep)

- `publish-poc-base`: packument `200` skeleton, wiped Oct-22, advised `1.0.7` tarball `404` both lanes, ZERO GHSA.
- `publish-poc-test3`: packument `200` skeleton, wiped Oct-23, seven advised rungs tarball `404`, ZERO GHSA.
- `publish-poc-test`: packument `200` skeleton, wiped Oct-23, ZERO advisories of any kind — fully dead and fully un-advised.
- Sibling-name sweep (`publish-poc`, `publish-poc-found`, `publish-poc-test2`, `publish-poc-test4`): `404` = never registered or fully erased; family is three names at the public lane.

Sweep mechanics live in the [214th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-fourth-sweep).

## October 26 217th sweep follow-up (~13:5x UTC): THE COHORT GOT ITS GHSAs AT `09:31:06Z` — AND THE PAGE'S "ZERO GHSA" WAS A ROUTE BLIND SPOT

The 217th's missed-head correction (see stream section self-capture 1) reaches this page's own record: `GHSA-35j9-6ggx-3fcq` (`publish-poc-base`) and `GHSA-mq69-4j49-gmx8` (`publish-poc-test3`), both critical, published `2026-10-26T09:31:06Z` on the `type=malware` direct lane — `≈3 h` BEHIND the `06:30Z` OSV records, the retro-mirror pattern again (importer-path mints). The enforcement question is MOOT for this cohort — all three names were already whole-name wiped by the registry Oct-22/23, before any advisory existed — so these GHSAs change nothing at the registry and everything about the wiki's earlier "ZERO GHSAs" phrasing: the names were GHSA-less at capture (true then), and drew mirrors anyway (`≈3 h` mirror band, the kam193 band reproduced on the amazon-inspector npm lane). `publish-poc-test` (the third wiped name): still ZERO advisories of any kind on the verified lane, day five. The wipe-lane-intel question survives intact — enforcement wiped names the advisory lanes only documented `≈3 days` later. `publish-poc-found-*` mint alert: no mints standing; three bare names re-registration watch: quiet. Sweep context → [217th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-seventeenth-sweep).
