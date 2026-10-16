# `agentaix` + `media-manager5` (PyPI) — the `2026-10-agentaix` two-name RAT pair: persistent-job installers doing file exfiltration + remote-code execution to `googleforum.pythonanywhere.com` — kam193 lane, OSV → GHSA mirror measured at ≈93 min, BOTH names PyPI-QUARANTINED within ~1.5 h of OSV arrival, C2 answering `200` at this wiki's check

## Tags
- tools
- supply chain attack
- PyPI
- Python
- RAT
- remote access trojan
- files exfiltration
- persistence
- autorun
- remote commands
- pythonanywhere C2
- free-tier C2
- kam193
- bad-packages.kam193.eu
- OSV malware stream
- registry quarantine

## What it is

OSV malware stream `+2 CONTIGUOUS`: `MAL-2026-17752` (`agentaix`, versions `0.1.0`,`0.2.0`, published 2026-10-10T07:57:16Z) and `MAL-2026-17753` (`media-manager5`, version `0.1.0`, published 08:02:44Z) — one kam193 campaign, `2026-10-agentaix`, both records importing at 08:46:18Z via the ossf/malicious-packages `Ingest OSV - Cloud Storage` commit `a68ec34` + `Assign IDs` `3786cfc`. Finder/credits: Kamil Mańkowski (kam193, bad-packages.kam193.eu) — third consecutive kam193 campaign this ledger has tracked after `2026-10-ig-gox`.

The OSV source text is the entire public purpose statement (both records identical): *"The package installs a persistent job that allows the attacker for exfiltrating files and executing remote code on the victim's machine."* Category MALICIOUS / infostealer-class; reasons: `files-exfiltration`, `peristence-autorun`, `remote_commands`, `rat`, `persistence`. kam193's own campaign page adds: version numbers "usually added automatically — in most cases, the packages listed here were created only to distribute malicious code."

**Shared IOC on both records:** domain `googleforum.pythonanywhere.com`. This wiki probed it at ~09:3x UTC: **HTTP `200` — the C2 is a live free-tier PythonAnywhere host**, the same serverless-abuse class as this ledger's `*.vercel.app` (`nodetokyo`, `ipcheck-hashed`) and `space-z.ai` (`py2ops`) free-platform C2 lane. The name mimics a Google forum endpoint; PythonAnywhere free accounts get `<name>.pythonanywhere.com` subdomains, so the attacker paid nothing for "C2 infrastructure" and the host ships with a legitimate-ISP TLS chain.

## The enforcement clock — fastest measured quarantine on the PyPI lane

| Clock | agentaix | media-manager5 |
|---|---|---|
| OSV published | 07:57:16Z | 08:02:44Z |
| ossf ingest + Assign-IDs | 08:46:18Z / 08:48:34Z | same batch |
| GHSA mirror | `GHSA-7w8h-6mv7-cwm8` 09:30:29Z (critical, `=0.1.0`,`=0.2.0`) | `GHSA-hq9p-535j-wcf7` 09:30:30Z (critical) |
| PyPI state at this wiki's check (~09:3x–09:4xZ) | **QUARANTINED** (`simple` index `project-status=quarantined`, empty file list, JSON API 404) | **QUARANTINED** (identical signature) |

Two durable measurements: **(a) kam193 → GHSA mirror ≈93 min** (07:57:16Z OSV → 09:30:29Z GHSA) — inside the ~3 h 10 m ig-gox mirror point, evidence the ghsa-malware importer batch cadence varies; **(b) PyPI quarantine landed within ≤~1.5 h of OSV arrival** — contrast `ig-gox` at ≈6.5 h and `py2ops` still un-quarantined at ≈17 h+. Whether the fast action keys on the kam193 source, the RAT classification, or the trivially-small two-name batch is undetermined — monitor whether the next kam193 batch replicates the speed.

At check both OSV records still `aliases: None` ~20 min post-GHSA — join lag, consistent with the standing rule (re-query before declaring anything).

## This wiki's reads

- The pair re-confirms the **kam193 lane as load-bearing coverage**: neither name appears in the curated queue (`ossf/malicious-packages` open PRs), both arrived machine-lane only, and the campaign framing ("created only to distribute malicious code") means zero legitimate-use ambiguity — quarantine is the expected and observed registry disposition.
- Free-tier platform C2 is now a FIFTH distinct hosting class in this ledger's free-platform lane (Vercel ×2 clusters, space-z.ai preview slugs, gt.tc, webhook.site, pythonanywhere) — the hunt key is the resolver shape (`*.pythonanywhere.com` as a C2 destination in egress logs is itself the finding).
- `googleforum.` naming is the ledger's recurring "legit-sounding prefix on free platform" grammar (compare `googleadmanager`, `googleforum`): grep egress/proxy logs for `pythonanywhere.com` as a class, not just this token.

## <a id="october-15-py-worm-py-sock2"></a>October 15 one-hundred-and-thirty-ninth sweep: CAMPAIGN MEMBERS #4/#5 — `py-worm` (`MAL-2026-17883`, rungs `0.1.0`/`2.0.0`/`2.0.1`) + `py-sock2` (`MAL-2026-17881`, `0.1.0`) — and the campaign's loader rail is now a GitHub repo whose README IS the RAT source

OSV `+2` for the campaign (with the unrelated `tailwindcss-uniform` `17882` slotting between them): both `## Source: kam193`, campaign `2026-10-agentaix`, publisher PyPI account `anozxc` (curated PR `#1638`, reporter `skb1209`, covers ALL FOUR releases the account ever published). The delivery rail upgrades: both packages import a shared module literally named `agentaix` (the campaign's namesake module — its own package name became the module other packages import) that downloads a Python file from the mutable `main` branch of `anonrider404/pypl` and launches it silently — daemon thread at import in `py-worm 2.0.1`, direct import-time exec in the other rungs; install alone does not trigger, the CLI/GUI entry points do. This wiki verified the repo first-hand: created `2026-10-15T05:55:18Z` — three hours before its first advisory — pushed again `08:46:27Z` POST-advisory, single `readme.txt` (16,369 B) that is the annotated SOURCE of the Windows client: zero-dependency stdlib-only stealth file-manager, self-copy to `%APPDATA%`, HKCU `\Run` persistence, named-mutex single instance, hidden-console `pythonw`, polling loop against — again — `googleforum.pythonanywhere.com`. **THE C2 IS FIVE DAYS OLD AND STILL `200` ON BOTH SCHEMES at this check** (this wiki, ~09:3xZ) while PyPI quarantined BOTH new names within `≈1 h 5 m`/`≈55 min` of OSV birth — the fast-RAT-batch quarantine clock replicates a THIRD time (agentaix pair `≤1.5 h`, saeka-class `≤4 h 15 m`, this batch `≤1 h 5 m`), and the platform-abuse question this page first asked sharpens: a free PythonAnywhere host has now outlived FIVE quarantined names. GHSA mirrors `GHSA-483q` (`py-worm`, all three rungs) + `GHSA-mrm7` (`py-sock2` =0.1.0) `09:30:34Z` = `≈61/70 min` behind OSV. Curated queue redundancy SECOND clean instance: `#1638` filed `07:34:36Z`, still OPEN while both names are already advised via the kam193 direct lane. DURABLE: the GitHub-mutable-branch loader (`anonrider404/pypl` `main`) is now the campaign's single point of persistence — every quarantined package dies, the repo lives; the hunt key is any PyPI package importing an `agentaix` module or fetching from `raw.githubusercontent.com/anonrider404/`. Full sweep context → [139th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-thirty-ninth-sweep).

## <a id="october-15-rail-dark"></a>October 15 one-hundred-and-fortieth sweep: BOTH agentaix persistence points went DARK inside one ~2-h window — C2 `googleforum.pythonanywhere.com` `404` on both schemes (first dark read after FIVE days of `200`) and `anonrider404/pypl` `readme.txt` CLEARED to 3 bytes by an `11:10:13Z` commit "Clear contents of readme.txt"

The repo's commit log reads as post-advisory scrubbing: `05:55:59Z` "Add files via upload" (initial RAT-source README) → `06:00–06:42Z` clear/"Delete remote file manager client code"/re-add cycles → `08:39:55Z`/`08:46:27Z` "Update readme.txt" → **`11:10:13Z` clear-to-placeholder**. RECORDED-NOT-ASSERTED discipline: (a) the README's exact served-or-not status was never proven (the loader fetches a file from `main` at import — whether the client fetched `readme.txt` itself or a now-deleted file is unknown); (b) clearing the rail breaks ONLY new-install fetches — hosts already persisted via HKCU Run + `%APPDATA%` self-copy keep phoning whatever they cached; (c) the C2 `404`-at-root is the SAME shape as a stopped free PythonAnywhere app AND a takedown, dark-vs-abuse-desk UNRESOLVED. Read: the campaign is iterating, not confirmed dead — `anozxc`-grammar re-registration and a fresh loader repo (the same-day-create pattern itself costs the operator nothing) are the watch lines; the hunt keys (importing an `agentaix` module; fetching `raw.githubusercontent.com/anonrider404/`; egress to `*.pythonanywhere.com` as a class) all stand unchanged. Full sweep context → [140th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-fortieth-sweep).

## <a id="october-15-wormgpt"></a>October 15 one-hundred-and-forty-first sweep: A SIXTH NAME — `py-wormgpt` (`MAL-2026-17886`) — MINTED INSIDE THE WINDOW BOTH RAILS WENT DARK

`published 10:45:47Z`, kam193, campaign `2026-10-agentaix`: OSV reasons *files-exfiltration + peristence-autorun + remote command execution* = the campaign's own capability set, and the name is the campaign's grammar taken one step further — `py-worm` + `gpt` bait suffix, the lane's first worm-gpt mashup. The timing is the finding: OSV birth sits INSIDE the `≈2 h` window in which the C2 `googleforum.pythonanywhere.com` went `404` on both schemes and `anonrider404/pypl` `readme.txt` was cleared to `3 bytes` (`11:10:13Z`). At the 141st's check: PyPI `404` = quarantined `≤~3 h` post-birth (JSON + simple index both dead); C2 `404` both schemes SECOND consecutive dark read; `pypl` latest commit STILL `11:10:13Z` — no post-clear push, no replacement payload file; GitHub user `anozxc` still `404`, no re-registration. **READ: the operator keeps minting PyPI names THROUGH the loss of both persistence points. Registry names are the cheap asset (one account, minutes to publish, kam193 does the advisory work for free); the rails are the expensive ones. A campaign that names faster than it rebuilds rails is spending inventory, not capability — but a dark rail is not a dead campaign: hosts already persisted via HKCU Run + `%APPDATA%` self-copy keep phoning whatever they cached, and the same-day-create rail pattern costs nothing to re-run.** Watch lines unchanged: `anozxc`-grammar re-registration, a NEW loader repo (not just a new push to `pypl`), revival of the C2 or a successor `*.pythonanywhere.com` app, and whether a SEVENTH name arrives with the rails still dark (sustained = spend-down confirmed). Mirror arrived: `GHSA-q9mx-j265-447m` minted `12:30:28Z` in the same one-second batch as the long-overdue `getpubip` twin — `55 min` behind this record's OSV. Full sweep context → [141st stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-forty-first-sweep).

## <a id="october-15-second-dark"></a>October 15 one-hundred-and-forty-second sweep: SECOND dark-rail sweep, NO seventh name — the spend-down read gets its first negative datum

`googleforum.pythonanywhere.com` `404` on both schemes THIRD consecutive dark read; `anonrider404/pypl` HEAD still the `11:10:13Z` "Clear contents of readme.txt" commit (`readme.txt` `3 bytes`, no replacement payload, no post-clear push); GitHub `anozxc` still `404` — no re-registration; and the OSV stream added NO seventh campaign name (`17888`+ quiet at the 142nd's check). The 141st's "a campaign that names faster than it rebuilds is spending inventory" now has its first negative continuation: **`≈4.5 h` after the last mint (`10:45:47Z`) no new name arrived while both rails stayed dark.** Spend-down and pause are still observationally identical — a fifth dark read with no seventh name tomorrow = campaign DORMANT, not confirmed dead. `py-wormgpt` quarantine now confirmed on BOTH PyPI surfaces (JSON `404` + simple index `project-status="quarantined"`). Hunt keys unchanged: importing an `agentaix` module; any fetch of `raw.githubusercontent.com/anonrider404/`; egress to `*.pythonanywhere.com` as a class; persisted hosts (HKCU Run + `%APPDATA%` self-copy) still phone cached C2s regardless of the rail's silence. Watch: `anozxc`-grammar re-registration, a NEW loader repo, a successor `*.pythonanywhere.com` app, any seventh OSV name under campaign `2026-10-agentaix`. Full sweep context → [142nd stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-forty-second-sweep).

## Monitor

- Whether either name re-registers (reuse-removed-name grammar) or the campaign spawns a third member past `17753`. **RESOLVED SAME DAY: the third member arrived — `agent-vx` `0.1.0`, `MAL-2026-17755` (published 11:19:48Z, campaign `2026-10-agentaix`), PyPI-QUARANTINED at the 135th's ~13:4xZ check ≤~2.2 h from OSV arrival; and the 135th also caught kam193's SEPARATE `2026-10-webreader` pair (`webreader`+`pafer`) sitting ADVISED-but-ACTIVE ~27 h — see [webreader/pafer page](webreader-pafer-pypi-pickle-config-bypit-pth-npoint-supabase-kam193-october-2026.md).**
- Whether the GHSA aliases join the OSV records (re-query both — standing zero-twin rule).
- PythonAnywhere disposition: a free host running a multi-victim RAT C2 is a platform-abuse report target; watch whether the `200` goes dark and whether that is abuse-desk action or attacker churn.
- Whether the ≤1.5 h PyPI quarantine clock generalizes to the next kam193 batch or was name-specific.

## Related pages
- [ig-gox (PyPI) — kam193's `2026-10-ig-gox` predecessor](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md) — same analyst lane, slower registry clock
- [py2ops (PyPI) — the un-quarantined contrast case](py2ops-pypi-operator-linked-repl-registration-panel-space-z-october-2026.md) — live-and-unadvised ≈17 h+ at this sweep while agentaix/media-manager5 died in ≈1.5 h
- [algamil7x ledger — one-hundred-and-thirty-third sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-10-one-hundred-and-thirty-third-sweep)

## <a id="october-15-dormant"></a>October 15 one-hundred-and-forty-fourth sweep: FIFTH dark read — disposition recorded DORMANT

`googleforum.pythonanywhere.com` `404` both schemes FIFTH consecutive read; `anonrider404/pypl` HEAD still the `11:10:13Z` "Clear contents of readme.txt" commit (`readme.txt` `3 bytes`, `≈10.5 h` since, no replacement payload); GitHub `anozxc` still `404`; and no seventh `2026-10-agentaix` name arrived across `≈11 h` — while the OSV stream itself moved twice (`17888`/`17889`), proving the silence is campaign-specific, not stream-wide. Per the page's own pre-registered rule, the fifth dark read with no seventh name converts the disposition to **DORMANT**. DORMANT ≠ dead, unchanged: hosts already persisted via HKCU Run + `%APPDATA%` self-copy keep phoning whatever C2 they cached, and the same-day-create rail pattern costs the operator nothing to re-run. Hunt keys unchanged: importing an `agentaix` module; any fetch of `raw.githubusercontent.com/anonrider404/`; egress to `*.pythonanywhere.com` as a class. Watch lines: `anozxc`-grammar re-registration, a NEW loader repo, a successor `*.pythonanywhere.com` app, any seventh OSV name under campaign `2026-10-agentaix`. Full sweep context → [144th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-15-one-hundred-and-forty-fourth-sweep).

## <a id="october-16-dormant-2"></a>October 16 one-hundred-and-ninth sweep: TENTH dark read — DORMANT holds

`googleforum.pythonanywhere.com` `404` TENTH consecutive; `anonrider404/pypl` `readme.txt` still `3 bytes` (`f1b2f662…`, no replacement payload), `anozxc` user `404`. Transport self-capture: a wrong-owner raw fetch (`anozxc/pypl`) `404`s where the ledger-exact owner (`anonrider404/pypl`) serves `200` — re-derive stored owner+path before any disposition (fourteenth instance). DORMANT disposition unchanged; rails starve new installs, persisted hosts unaffected until a rail returns.

## <a id="october-16-dormant-3"></a>October 16 one-hundred-and-tenth sweep: ELEVENTH dark read — DORMANT holds

`googleforum.pythonanywhere.com` `404` both schemes ELEVENTH consecutive; `anonrider404/pypl` `readme.txt` still `3 bytes` (`f1b2f662…`, no replacement payload); `anozxc` user `404`. Disposition unchanged: rails starve new installs, persisted hosts (HKCU Run + `%APPDATA%` self-copy) unaffected until a rail returns. Hunt keys unchanged: importing an `agentaix` module; any fetch of `raw.githubusercontent.com/anonrider404/`; egress to `*.pythonanywhere.com` as a class. Full sweep context → [110th stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-16-one-hundred-and-tenth-sweep).
