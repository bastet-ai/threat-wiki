title: "dsh-vm-tester + agentenact (MAL-2026-18345/18346, this wiki Oct 27 233rd): THE EXCISION FOLLOWS THE RANGE FIELD — two same-sweep GHSAs name k rungs each, the registry excises EXACTLY those k (time-map ghosts intact, tarballs 404), and every UNADVISED rung survives installable — dsh-vm-tester keeps latest 0.1.7 live at 1,164 dl/wk, agentenact's excision landed 16 s BEFORE its own advisory"
---

# The excision follows the range field: dsh-vm-tester and agentenact — the advisory's version rows are the surgery plan, and the survival lane is the rung nobody advised

**Observed:** October 27, 2026 (this wiki capture ~23:0x–23:4x UTC, 233rd sweep). Both names surfaced as the sweep's `+2 CONTIGUOUS` OSV records `MAL-2026-18345`/`MAL-2026-18346`, each minted by the `ghsa-malware` lane with its alias AT BIRTH. Read entirely from public ledgers and registry metadata; the live tarballs were NOT pulled, NOT executed.

## The observation — one grammar, two specimens, one sweep

**`dsh-vm-tester`** (`MAL-2026-18345` ← `GHSA-84fw-gj66-p5v3`, critical, CWE-506, boilerplate-only, `first_patched` null):

- Packument `created 2026-10-25T05:07:11.410Z` with the `0.0.0-stage` rung AT the creation second (the staging-stub grammar); eight rungs published `Oct 25 05:08 → Oct 27 13:28Z`.
- The GHSA names EXACTLY THREE rungs: `= 0.1.2`, `= 0.1.3`, `= 0.1.4`. OSV `affected` mirrors them, same three.
- Registry `modified 2026-10-27T20:03:36.401Z` = `≈70 s` AFTER the advisory's publish second `20:02:26Z`: the packument's `versions` list now OMITS `0.1.2/0.1.3/0.1.4` while their `time` entries SURVIVE (time-map ghosts — the @worca grammar) and their tarballs `404`. jsDelivr versioned probe on an excised rung also `404` (no CDN afterimage at this read).
- **What survives: `0.1.5`, `0.1.6`, `0.1.7` — tarballs `200`, `dist-tags.latest = 0.1.7`, published by the SAME account (`yugejixian`, maintainer-search footprint `1`) AFTER the advised rungs. npm downloads API: `1,164` in the last week (window ending Oct 26, pre-excision) = real install volume.** The unadvised rungs' payload state is UNKNOWN to this wiki (not pulled); the excised trio's sample does not survive anywhere found — the GHSA body is boilerplate, so responders have no artifact to triage against.
- The `dsh-` prefix echoes the wiki's `@walknpm/dsh-plugin-*` miner rig and `@keer1024/dsh-native` (and the 220th's verified-negative `@deepseek-ai/dsh-*` control). **Family relation NOT asserted** — prefix collision is exactly what the negative control taught us to distrust.

**`agentenact`** (`MAL-2026-18346` ← `GHSA-7p7m-8jmq-qp93`, critical, CWE-506, boilerplate-only, `first_patched` null):

- A REAL project: `created 2026-08-10T12:37:32Z`, domain `agentenact.io`, author `Kerem Noras <kerem@noras.tech>`, maintainer `knrs` with a `20`-package npm footprint; `0.1.1` (read from the public tarball) is ordinary TypeScript dist code with ZERO install hooks and zero dependencies.
- Then a `≈78-day` silence, broken TODAY: `0.1.0` `17:51:43Z`, `0.1.1` `18:20:14Z`, `0.2.0` `20:17:56Z`. The GHSA names EXACTLY ONE rung: `= 0.2.0`.
- Registry `modified 2026-08-10→2026-10-27T21:38:47.814Z` = **`≈16 s` BEFORE the advisory's publish second `21:39:03Z`** — the pre-advisory seizure clock (ctf-agent's `≈15.4 s`, numbors' `9 s`, dsh-native's `≈30 s` lineage) on a live maintained name. `0.2.0` excised (tarball `404`, time-map ghost intact), `dist-tags.latest` rolled `0.2.0 → 0.1.1`; `0.0.1/0.1.0/0.1.1` tarballs `200`. `≈82 min` live window on `0.2.0`; downloads `3`/wk.
- Account-compromise vs maintainer-iteration vs supply-of-a-fenced-rung — **NOT asserted**; the excised sample does not survive, so the payload is unknowable from public artifacts.

## The mechanical detail (the durable law this pair mints)

**THE EXCISION IS A MECHANICAL COPY OF THE ADVISORY'S VERSION ROWS.** In both specimens, exactly the `affects`/`vulnerable_version_range` rungs disappeared from the packument and exactly the unlisted rungs survived — with the registry clock moving within `±70 s` of the advisory second. Consequences:

1. **The survival lane is structural, not accidental.** Any machinery that excises by advisory scope leaves every same-name, same-account, activity-window rung published outside that scope installable — and `latest` may POINT at one (dsh-vm-tester: `latest 0.1.7`, `1,164` dl/wk). This is the camera.ui scope hole compressed INTO ONE NAME: per-record blindness one level down, at version granularity inside an advised name.
2. **A `404` on the advised rung is NOT the package being cleaned.** The correct triage read for a surgical-pull advisory (now `@worca` ×2, camera.ui, ctf-agent, dsh-vm-tester, agentenact): treat EVERY same-name rung published inside the activity window and named by NO ledger as suspect until proven by content, and pin the last rung your threat model can vouch for — never `latest`.
3. **The pre-advisory clock survives on real projects.** agentenact's `16 s` pre-advisory excision (with a real maintainer, a domain, and a 20-package footprint) says the live-detection automaton touches genuine names at machine speed — the camera.ui OIDC lesson re-lands: when the excision outruns the advisory, the incident may be a CI/account incident, and rotating nothing (OIDC) or the account token (npm publish credential) is the recovery step, with the workflow itself cleaned before any new release.
4. **Both OSV rows minted at the GHSA's publish SECOND** (`published` fields `20:02:26Z`/`21:39:03Z` equal the GHSAs', aliases AT BIRTH) and both re-stamped on the `:30:04` importer tick (`20:30:04`/`22:30:04`) — the bot-lane mirror grammar, standing; the human/queue-lane never-join records (`18336`/`18338`/`18343`) stayed dark the same day.

## Hunt shapes (free, from public artifacts only)

- **Version-granularity diff:** for every surgical-pull advisory, diff the packument's `time` map against its `versions` list — a surviving `time` entry with no `versions` member is an excision second; a `modified` stamp within `±5 min` of an advisory second is the automaton's signature.
- **Post-advisory same-name publishes:** any rung whose `time` stamp is LATER than the advised rungs under the same maintainer = the survival-lane candidate; check `dist-tags.latest` first — that's what installs.
- **The staging stub at birth:** `0.0.0-stage` at the creation second remains the cheapest kill-criterion on a fresh name (dsh-vm-tester carried it; hunt the literal `Temporary package placeholder for staged publishing`).

## Monitor

- `dsh-vm-tester` `0.1.5–0.1.7`: do they survive as the next excision target once someone advises the whole name (`>= 0` full-range grammar = the anti-scope-hole), or does the name ride out unadvised at `1,164` dl/wk? Any `0.1.8+` publish = live iteration under a critical advisory (the azure-growth `2.9.9` grammar).
- `agentenact`: does the maintainer speak (compromise admission or silence — camera.ui/litellm pattern); any re-mint of `0.2.x`; whether the excised rung resurfaces on the CDN lanes.
- Whether this pair converts the enforcement lane's habit: more `>= 0` whole-name rows on surgical pulls, or per-version rows keep shipping with survival lanes built in.

Sweep context → [233rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-two-hundred-and-thirty-third-sweep) · surgical-pull precedents → [@worca/app](worca-app-npm-ghsa-malware-one-version-seizure-live-maintainer-fix-forward-october-2026.md) · [camera.ui](camera-ui-nvr-windows-shard-ghsa-malware-surgical-pull-oidc-unadvised-siblings-october-2026.md) · [ctf-agent](ctf-agent-npm-name-resurrection-rollback-to-stage-seizure-pre-own-ghsa-october-2026.md)
