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

## Monitor

- Whether either name re-registers (reuse-removed-name grammar) or the campaign spawns a third member past `17753`. **RESOLVED SAME DAY: the third member arrived — `agent-vx` `0.1.0`, `MAL-2026-17755` (published 11:19:48Z, campaign `2026-10-agentaix`), PyPI-QUARANTINED at the 135th's ~13:4xZ check ≤~2.2 h from OSV arrival; and the 135th also caught kam193's SEPARATE `2026-10-webreader` pair (`webreader`+`pafer`) sitting ADVISED-but-ACTIVE ~27 h — see [webreader/pafer page](webreader-pafer-pypi-pickle-config-bypit-pth-npoint-supabase-kam193-october-2026.md).**
- Whether the GHSA aliases join the OSV records (re-query both — standing zero-twin rule).
- PythonAnywhere disposition: a free host running a multi-victim RAT C2 is a platform-abuse report target; watch whether the `200` goes dark and whether that is abuse-desk action or attacker churn.
- Whether the ≤1.5 h PyPI quarantine clock generalizes to the next kam193 batch or was name-specific.

## Related pages
- [ig-gox (PyPI) — kam193's `2026-10-ig-gox` predecessor](ig-gox-pypi-termux-license-gated-inmemory-exec-loader-goxtools-shop-october-2026.md) — same analyst lane, slower registry clock
- [py2ops (PyPI) — the un-quarantined contrast case](py2ops-pypi-operator-linked-repl-registration-panel-space-z-october-2026.md) — live-and-unadvised ≈17 h+ at this sweep while agentaix/media-manager5 died in ≈1.5 h
- [algamil7x ledger — one-hundred-and-thirty-third sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-10-one-hundred-and-thirty-third-sweep)
