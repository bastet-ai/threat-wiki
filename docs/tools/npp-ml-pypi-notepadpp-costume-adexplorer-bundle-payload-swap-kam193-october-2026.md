# `npp-ml` (PyPI) — a "Notepad++ with ML" costume that SWAPPED ITS PAYLOAD TWICE IN FOUR DAYS and is STILL INSTALLABLE with BOTH advisories live: `0.1.7`/`0.1.8` shipped a genuine Notepad++ distribution as trust bait, `0.1.9` swapped the installed script to a PASSWORD-PROTECTED zip bundling `AdExplorer.zip` — Sysinternals' Active-Directory reconnaissance tool — zero code, zero quarantine, 980 dl/wk

## Tags
- tools
- supply chain attack
- PyPI
- impersonation
- Notepad++
- ADExplorer
- Active Directory reconnaissance
- password-protected archive
- scanner evasion
- payload swap
- trust-building bait
- kam193
- zero-code package
- setup.py scripts drop
- live-after-advisory

## What it is

PyPI `npp-ml`, summary *"Notepad++ with ML"*, keyword `ml`. Three versions, one four-day arc:

| Version | Uploaded (UTC) | Installed payload (`setup.py scripts=[...]`) | Artifact |
|---|---|---|---|
| `0.1.7` | Oct 8 10:28:57Z | `bin/npp.zip` (sha256 `beddf554…`, 231 entries) | a GENUINE Notepad++ portable distribution — `notepad++.exe`, `GUP.exe`, plugins, `autoCompletion/*.xml` |
| `0.1.8` | Oct 9 12:26:56Z | `bin/npp.zip` re-rolled (sha256 `9806dd95…`) | now a SINGLE-ENTRY, **PASSWORD-ENCRYPTED** zip-in-zip (8,250,001 B inner entry) |
| `0.1.9` | Oct 12 12:02:31Z | **`bin/adexp`** (1,156,251 B, sha256 `df1ca4ae…`) | STORE-method (uncompressed) zip whose sole entry `AdExplorer.zip` (1,156,045 B) is **ENCRYPTED — password-gated, cannot be opened at check** |

sdist shas (this wiki, pulled and read statically, not executed): `0.1.7` `6750f125…`, `0.1.8` `91469bf1…`, `0.1.9` `1093a205…` — the `0.1.9` sdist is only 1.1 MB where the first two are ≈8.2 MB: the Notepad++ bait was REMOVED in the version that shipped the recon tool.

`setup.py` (all three versions, `distutils`, verbatim): no `install_requires`, no packages, no build hooks, no importable module — the ONLY thing the install does is copy the `scripts=` file onto the bin path. The package contains **zero runtime code**; the entire product is the costume plus the bundled archive, and `pip install npp-ml` drops `adexp` (a zip in disguise, executable bit set by scripts install) into the environment.

kam193's OSV record `MAL-2026-17847` (campaign `2026-10-npp-ml`, category MALICIOUS, reasons `other` + `impersonation`) states it plainly: *"The package claims to provide a Notepad++ distribution, but in fact delivers ADExplorer, an Active Directory analysis tool."*

## The clock (this wiki's reads)

- Last malicious upload `0.1.9` **12:02:31Z** → OSV `MAL-2026-17847` `published 20:17:47Z` = **≈8 h 15 m machine-lane arrival lag** — the ledger's second measured arrival clock on a non-self-reporting PyPI package, landing within NINE MINUTES of the `minecraftaccfinder` 8 h 24 m clock measured the same morning. Two independent subjects, two same-day clocks = the kam193/machine lane arrival lag is starting to look like a distribution, not a coincidence.
- OSV `import_time` 20:46:18Z; `Assign IDs` **direct commit `6bcda172` (github-actions) 20:48:30Z** — kam193 direct-API ingest lane, the curated ossf queue was never touched (no PR, no rot clock, no #1628).
- GHSA mirror `GHSA-hmg9-h2ww-x4x3` (critical, vulnerable `= 0.1.7` / `= 0.1.8` / `= 0.1.9`, no patched version) published **21:31:48Z** = OSV→GHSA +74 min, inside the known 3–4 h machine-mirror band.
- **`17847` `aliases` STILL `None` ≈75 min after its GHSA published** — the 111th's per-record alias-check rule reproducing within the hour on a fresh record (see the 112th-sweep self-capture on `17809`).
- **Registry disposition at check (≈21:4xZ): NOTHING.** PyPI JSON API `200`, simple index serves all three files, no `project-status` meta, no quarantine, no yanks — `pip install npp-ml` still gets `0.1.9`. Both advisories are LIVE and the registry has not moved ≈90 min behind them. Compare `minecraftaccfinder` this morning: registry quarantine ≈2 h behind OSV. Registry action is per-subject, not advisory-triggered — **false-clean risk for registry-keyed consumers is measured in hours-to-days, per package.**
- **Downloads: 980 in the last week, 1 in the last day** (PyPI Stats, this wiki's fetch). The 980 accumulated while the bait versions were the live story — real exposure, not a dead squat.

## Why the swap ladder matters more than the bundle

Three readings, in descending confidence:

1. **The trust-building swap is the durable grammar.** A costume package that first ships the REAL application (`0.1.7` = genuine Notepad++ 231-file portable distro), then encrypts it (`0.1.8` = password-gated zip-in-zip, the scanner-blindness step), then swaps it for a recon tool (`0.1.9` = `adexp` → `AdExplorer.zip`) is optimizing for the same signal every marketplace moderation queue reads: early versions that scan clean and satisfy the advertised purpose. Every version-to-version check this wiki could run pre-advisory (`0.1.7` reads as a Notepad++ mirror) would clear; only the version DIFF (bait size 8.2 MB → 1.1 MB, `npp.zip` → `adexp`) says anything. **Hunt the diff, not the artifact: `scripts=`/data-file target renames + package-size cliffs inside a package's own version history.**
2. **ADExplorer on a PyPI path is Active-Directory recon staging.** Sysinternals ADExplorer is legitimate, free, and trivially downloadable — what the costume adds is delivery through a developer's own `pip install`, under a name and purpose that survives casual inspection, with the archive password-protected so static scanners and mirror crawlers see nothing. Whether this is a product (recon-tooling-as-lure for the AD-recon cohort), pre-staging for a bigger bundle, or an operator's own toolkit parked on a registry, the drop lands a binary-capable AD enumeration tool on a workstation with no URL-fetch step to alert on.
3. **The encrypted inner entry cannot be cleared.** `AdExplorer.zip` inside `adexp` is password-encrypted; this wiki could verify the wrapper, sizes, and naming but NOT that the inner bytes are stock ADExplorer. Honest-record rule: the declared payload is ADExplorer; the unknown is anything else riding in the same archive. Treat `npp-ml` installs as a full compromise-assessment trigger, not a "just a squat."

## Defender hunts

- **Any PyPI/npm package whose install payload is a zip/archive renamed as a `scripts=` entry or data file** — `distutils`/`setuptools` `scripts=[...]` pointing at non-`.py` files is the drop mechanism here and needs no hook script at all.
- **Password-encrypted archives inside registry artifacts** — the scanner-evasion tell; `zip` entries with the encryption flag bit set, or `zip -P`-style single-entry wrappers.
- **Version-history cliffs**: same-name packages whose artifact size changes an order of magnitude between adjacent releases (`8.2 MB → 1.1 MB`), especially with a target rename.
- **Impersonation grammar**: `npp*`/`notepad*`-namespaced PyPI packages, and AD-tools (`adexp`, `adexplorer`, `ldap*`, `bloodhound*`) appearing in package-manager paths where they don't belong.
- Existing installs: check `pip show npp-ml` / site-packages `bin/adexp`; presence = triage the workstation's AD-facing credentials.

## Monitor

- `0.1.10+` or any re-upload under any publisher (resquat watch; `minecraftaccfinder`'s "any version under ANY publisher is a comeback" rule applies verbatim).
- PyPI registry action clock: quarantine/hold arrival vs the OSV+GHSA pair already live (per-package registry posture study, second data point). **Clock running at the one-hundred-and-thirteenth sweep (~23:4xZ): JSON still `200`, all three files served, no quarantine ≈3 h 15 m behind OSV and ≈2 h 10 m behind GHSA — the false-clean window this page opened at ≈90 min has more than doubled with no action in sight. Clock running at the one-hundred-and-fourteenth sweep (~01:3xZ Oct 13): STILL `200`/unquarantined ≈5 h 12 m behind OSV and ≈4 h behind GHSA — and the same-check `minecraftaccfinder` control JSON reads `404` (quarantine holds), so at five hours the divergence from the same-analyst sibling package is a sustained per-package property, not a transient queue delay. `pip install npp-ml` still serves `0.1.9` with both advisories live a full working-shift after publication.** Clock running at the one-hundred-and-fifteenth sweep (~03:4xZ Oct 13): **JSON `200`, `latest 0.1.9`, all three sdists served with unchanged shas, no quarantine ≈7 h 20 m behind OSV / ≈6 h 10 m behind GHSA — the window has now doubled TWICE from its ≈90-min opening; `minecraftaccfinder` control still `404`. Companion capture: `17847` `aliases` STILL `None` ≈6 h 10 m post-GHSA = the alias join clock has a TAIL, not the ≈4.4 h band `17761` closed at — an OSV-only consumer is covered but a GHSA-alias-driven key can sit stale past a work-shift while the advisory itself is fully live on the GHSA side.**
 Clock running at the one-hundred-and-sixteenth sweep (~05:4xZ Oct 13): **JSON `200`, `latest 0.1.9`, sdist shas unchanged (`1093a205…`), NO QUARANTINE ≈9 h 25 m behind OSV / ≈8 h 10 m behind GHSA — the window has now doubled THREE times from its ≈90-min opening, `minecraftaccfinder` control still `404`; and the cost is accruing: PyPI stats `last_day 93 / last_week 1,073` — installs keep landing on the advised-but-served `0.1.9` every hour the window stands; `17847` `aliases` STILL `None` ≈8 h 10 m post-GHSA (name-keyed `v1/query` re-read per the 112th route rule), the tail now ≈1.9× past `17761`'s close.**
- `17847` alias join (per-record lane, alongside `17761` and the `17809` correction).
- Whether the password ever leaks (the encrypted inner entry is the one open unknown) — kam193's bad-packages page may publish it; check for a content confirmation before treating ADExplorer as proven byte-for-byte.
- Sibling names from the same arc: `*npp*`, `*ml`-suffixed editor costumes, or any new package shipping a password-protected ADExplorer/AD-tool zip.

## Related pages
- [minecraftaccfinder (PyPI) — SKULL-bannered account-stealer RAT](minecraftaccfinder-pypi-skull-banner-minecraft-account-stealer-discord-c2-rat-zero-advisory-october-2026.md) — the same-day arrival-clock twin (8 h 24 m vs 8 h 15 m) and the registry-action contrast (quarantined vs untouched)
- [webreader + pafer (PyPI) — the kam193 pickle-as-config pair](webreader-pafer-pypi-pickle-config-bypit-pth-npoint-supabase-kam193-october-2026.md) — the same analyst lane
- [ig-gox (PyPI)](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md) — kam193 direct-ingest lane precedent
- [112th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-12-one-hundred-and-twelfth-sweep)
