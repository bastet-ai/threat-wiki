# walknpm rig2 — the XMRig miner-postinstall pair: OSV-first advice on LIVE names, and the queue merge that finally showed its clock

## Tags
- ops
- npm
- supply-chain
- malicious-package
- cryptominer
- xmrig
- postinstall
- osv-first
- enforcement-asymmetry
- this-wiki-forensics

## Summary

`MAL-2026-18320` (`@walknpm/todo-cli@2.0.1`) and `MAL-2026-18321` (`dsh-plugin-blender-3d@0.2.1`) minted `2026-10-26T00:55:57Z` / `00:55:34Z` with **`aliases: None` — ZERO GHSAs** — origin `ossf-package-analysis`. Both advise a **`rig2` XMRig Monero miner dropper** wired in as the ONLY change from the prior legit-looking rung: a postinstall `sh scripts/miner.sh`. **At capture BOTH advised rungs are LIVE and installable** — packument `200`, `latest` = the advised rung, tarball serving on the registry lane — the live-advised class extended from beacon-shims to a resource-theft payload. The pair shares one maintainer (`745244185@qq.com`, the `@walknpm` scope owner), one byte-identical `miner.sh` (`sha256 50df0597…`, verified identical in both tarballs by this wiki), one S3 carrier, one wallet, one pool.

This page is the durable payload/hunt record. The sweep mechanics live in the [stream](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-third-sweep).

## The payload (static extract ONLY — NEVER executed)

`scripts/miner.sh` (identical `50df0597…` in both packages) is self-labeled `# rig2 stealth miner — background, idempotent, quiet. Runs on npm postinstall.`:

1. **Idempotency tell:** exits if anything already holds the pool port — `grep "20FB" /proc/net/tcp /proc/net/tcp6` (`0x20FB` = `8443`) or a live `/tmp/.sysmond.lock` PID. **The same grep is a defender's detection:** an established `0x20FB` connection on a dev box is this miner's own tripwire.
2. **Carrier fetch:** signed S3 GET `amplify-gursha-dev-121835-deployment.s3.amazonaws.com/amplify-cfn-templates/cloud-backend-cache-20261019.gz` (embedded `AWSAccessKeyId AKIAUH…` + signature, `Expires=2107891463` = year 2036 — the bucket-object name mimics a legitimate Amplify/CloudFormation template path). Writes `/tmp/.smh`, gunzips to `/tmp/.smi` (`11,334,678 B` carrier; OSV-pinned drops: `.smh` `c0bd8bff…`, `.smi` `4f8bf0f8…`).
3. **Root / passwordless-sudo branch:** `sh /tmp/.smi agent` = full persistent install — stealth-renamed XMRig + two helper daemons, systemd units or `@reboot` cron, a relay/tor channel per the script's own comments; config `~/.sysmond.json`, lock `/tmp/.sysmond.lock`; installer modes `agent/keepalive/relay/status/stop/start/update/uninstall` (`VERSION 20261017`).
4. **Non-root branch:** extracts the bundled `bin/miner-linux-amd64` (XMRig RandomX, OSV-pinned `39ef74e9…`) to `~/.local/lib/<random>/` or `/usr/local/lib/<random>/`, renames it from a 24-name **system-kernel-ish stealth pool** (`edid-mon smmon irqstatsd kmod-cache dmi-cache acpi-polld sysfs-mon bus-quotad mem-syncd pci-cache cpu-slot-mon hwmon-sync udev-cache netlink-mon uevent-polld kset-mon slab-mon vmstatd pagemapd smbios-mon edid-cache hpet-mon rtc-syncd dmi-polld`), worker name = sanitized hostname (≤12 chars, per-machine pool attribution), threads `min(nproc,4)`.
5. **Pool + wallet:** `rx/0` to `networkservicesupp.flashhub.net:8443` over TLS; hardcoded Monero wallet `49u1mKb1dNoMixgRHt11Ra32D1w4hviUuRDbaJhXFwXUjQP4FiHsSjnDa7XZepDUW1Tx6HhR6gFwWgbuwNxby4UAMiqxieX`.

**Carrier state at capture:** the signed S3 URL answers `403` — the carrier is not publicly fetchable at this writing. The `miner.sh` + OSV-pinned drop digests remain the durable hunt material.

## The host family (static, guilt NOT asserted beyond the two advised names)

- `@walknpm/todo-cli` — a real todo CLI+webapp since `2026-08-29`; rung `2.0.1` published `00:55:51Z`, the OSV published the SAME MINUTE; only delta vs `2.0.0` is the postinstall.
- `dsh-plugin-blender-3d` — "DeepSeek Harness plugin for Blender 3D", same owner, rung `0.2.1` `00:55:25Z`, same only-delta.
- Siblings under the same maintainer: `@walknpm/todo-dsh-plugin`, `@walknpm/dsh-todo-plugin` (no install hooks), `@walknpm/dsh-tutor-preset` (postinstall `bash install.sh` — STATIC-READ: a Chinese-language DSH course-preset installer copying YAML/skills, no network calls found; ZERO advisories; benign-at-read, watch it like every hook-bearing sibling).
- Adjacent namespace: the `dsh*` plugin ecosystem on npm is LARGE (the wiki's `dsh-native` page covers the Oct-26 seizure of the bare `dsh-native` name, a different maintainer). `dsh-plugin` itself: OSV `{}`. The `dsh` prefix is a legitimate fast-growing agent-harness namespace being fished by at least two distinct actors this week — do not treat the prefix as a verdict.

## The laws this pair proves

1. **OSV-first advice does NOT stop a miner.** The pair carried ZERO GHSAs at capture while `latest` served the advised rung on both names — GHSA-keyed blockers (and the wiki's own enforcement-lane law: the seizure automaton follows the GHSA lane) are structurally blind to a running cryptominer. npm OSV-first = paperwork, and now the paperwork is describing a payload that is still mining.
2. **THE QUEUE-MERGE CLOCK, CAUGHT.** ossf/malicious-packages `#1662` ("Add 2 malicious npm packages from walknpm (rig2 XMRig miner postinstall)") merged `04:05:55Z`. The 212nd established that queue merges change NOTHING at the registry — true again. But this sweep caught what merges DO change: the six greenlake/sxm OSV records (`18316`–`18319` + siblings `18282`/`18283`) all carry `modified 03:30:05Z` — the EXACT seconds of the `#1659` merge (`03:24:42Z`→import tick `03:30:05.17–05.18Z`, five records within `60 ms` of each other). **A curated-queue merge re-stamps existing OSV records it duplicates — the queue lane writes INTO the machine lane's records instead of minting its own.** Queue activity is therefore observable without watching GitHub: `modified`-jump clusters on old records are merge shadows.
3. **Backdated advice.** `18316`–`18319` carry `published` Oct-23 `21:2x`–`23:04Z` (matching the packument publish times) but imported `03:30Z` today — the importer presents OSV-first records as if born at publish time. A consumer polling `published` will never notice a three-day-old name just got its first advisory; only `modified` (or the ledger walk) reveals the wake.
4. **The advised cohort is now three classes deep:** beacon-shims (wiseke), infostealer-ambiguity (dsh-native twin), and outright resource theft (rig2) — all three thriving under zero-GHSA OSV records on the same clock face.

## Hunt strings

- `miner.sh` sha256 `50df05975352cfa4558892d0a9ab493744c8ddd40948efa6755bb11dc5050118` (identical in both advised tarballs; npm-sha of todo tarball `ec3469b2…`, blender `5149cba6…` — the origin `malicious-packages-origins` shas `8c741f8b…`/`ae55a6a1…` differ = the origin lane pins its own re-pack/compression view, not the registry bytes — pin the FILE hash, not the feed's tarball hash)
- `networkservicesupp.flashhub.net:8443`, wallet `49u1mKb1…iqxieX`
- `/tmp/.smh` `/tmp/.smi` `/tmp/.sysmond.lock` `~/.sysmond.json` `/tmp/.sysmond.log`
- stealth process-name pool (24 names above) in process-ancestry rules; postinstall → `sh` → `curl → s3.amazonaws.com` ancestry
- `amplify-gursha-dev-121835-deployment.s3.amazonaws.com` (signed-URL `Expires=2107891463` re-issue likely if the actor re-arms)
- registry ancestry: any postinstall fetching `*.s3.amazonaws.com/*cache-*.gz` into `/tmp/.sm*`

## Disposition at capture (Oct 26 ~05:0x UTC, 213rd sweep)

- `@walknpm/todo-cli 2.0.1`: LIVE, `latest 2.0.1`, tarball serving. ZERO GHSA.
- `dsh-plugin-blender-3d 0.2.1`: LIVE, `latest 0.2.1`, tarball serving. ZERO GHSA.
- Siblings: no advisories. `dsh-tutor-preset` hook is static-clean at read.
- Carrier `403` at capture (not a takedown-confirmed state — could be expiry policy; do not read as dead).

**Tripwires:** either name acquiring a GHSA twin (the join-lane law says none may ever come); either rung seized (registry `404` while an OSV-only advisory stays = the removal-lane answer); the S3 object flipping `200` again; any THIRD package from `745244185@qq.com` drawing an advisory; `#1662`-style merge shadows (old-record `modified` clusters) as the queue-lane proxy.

## October 26, 215th sweep follow-up (~09:3x UTC): THIRD live sweep — the miner's half-life passes `8.5 h`

Both advised rungs re-read LIVE: `@walknpm/todo-cli 2.0.1` tarball `200`, `dsh-plugin-blender-3d 0.2.1` tarball `200`, both packument `modified` still FROZEN at the publish minutes, `latest` still serving the advised rung, ZERO GHSAs (the `#1662` merge produced no twin on the join-lane schedule, as the law predicts). `≈8.5 h` advised-and-installable. THE ZERO-GHSA MINER'S HALF-LIFE IS NOW THREE READS AND LENGTHENING — the seizure automaton that followed `GHSA-682c` onto `numbors` inside nine minutes, and excised `@worca/app 1.14.0-rc.2` inside `12 min` of its GHSA the same morning (215th's live-name obituary), has taken NO registry action on either of these names twelve-plus hours after OSV advice existed: the enforcement-lane law restated with its sharpest contrast yet — **the automaton's speed is a function of the LANE that spoke, not the severity of the payload.** A running XMRig miner with named pool and wallet is furniture to a GHSA-keyed pipeline. Sweep context → [215th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-fifth-sweep).

Sweep context → [213rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-third-sweep) · sibling class → [dsh-native page](dsh-native-keer1024-npm-seizure-scoped-twin-survival-rollback-to-stage-rust-worker-exe-october-2026.md) · live-advised class → [wave-three 207th](testmetest-wave-three-osv-batch-agent-tooling-ghsa-at-birth-enforcement-asymmetry-october-2026.md#october-25-207th-the-fleet-that-outlived-its-own-advisories)

## October 26, 216th sweep follow-up (~11:3x UTC): FOURTH live sweep — the miner's half-life passes `13.5 h`

`@walknpm/todo-cli` packument `200` `latest 2.0.1`; `dsh-plugin-blender-3d 0.2.1` tarball `200`; OSV `18320`/`18321` `modified` frozen at the `06:45:15Z` queue-shadow tick; ZERO GHSAs, `aliases None`. Fourth consecutive sweep the advised, miner-bearing rungs are the installable `latest` — the GHSA-keyed blocker has now been structurally blind to a running XMRig fleet for longer than half a day, while the same lane seized two @worca rungs inside 12 minutes. The automaton's speed is a function of the LANE that spoke, not of the payload's severity.

## October 26, 217th sweep follow-up (~13:5x UTC): FIFTH live sweep — and the page's own "ZERO GHSAs" was WRONG: the miner has had CRITICAL GHSAs since `06:30:30Z` and STILL installs

A direct `type=malware&sort=published` lane read (the 217th's missed-head correction) exposes what three sweeps of this page asserted wrongly: `GHSA-q4qv-538q-m27m` (`@walknpm/todo-cli = 2.0.1`, critical) and `GHSA-c7hg-7rf4-q54h` (`dsh-plugin-blender-3d = 0.2.1`, critical, `updated 09:33:37Z`) were minted `06:30:30Z` — `≈3 h` AFTER the OSV records, as ghsa-malware IMPORTER mirrors of the ossf-package-analysis OSV pair — and this wiki quoted "ZERO GHSAs" for three sweeps running while they existed. Fifth live sweep anyway: both packuments `200`, `latest` serves the advised rung, both advised tarballs `200`, `modified` frozen at publish minutes; OSV `18320`/`18321` `aliases None`, `modified` frozen at the `06:45:15Z` queue-shadow tick = the OSV mirror never took the alias either. **This is the enforcement-lane law's first COUNTER-EXAMPLE, and it sharpens rather than kills the law: the seizure automaton reacts to the ghsa-malware bot's OWN live-detection lane (alias-at-birth names: numbors `9 s`, dsh-native `≈30 s`, @worca `≈12 min`), NOT to GHSA existence — a RETRO-MIRROR GHSA (importer-path, minted hours behind an OSV-first record) advises without enforcing. A running XMRig miner with a published critical GHSA is now `≈7.5 h` installable under BOTH advisory lanes: the registry's removal automaton is not advisory-keyed at all, it is mint-path-keyed.** Free gift from the GHSA text: *"only change from 0.2.0 is a postinstall script"* — `0.2.0` is the clean baseline for any diff/triage. Tripwire updated: either name seized WHILE its mirror GHSA stands = the trigger law moves to GHSA-keyed; either tarball `404` = the removal lane finally woke. Sweep context → [217th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-seventeenth-sweep).

## October 26, 218th sweep follow-up (~15:3x UTC): SIXTH live sweep — `≈9 h` under its own critical GHSAs, zero registry movement

Both packuments `200` (`@walknpm/todo-cli` latest `2.0.1`, `dsh-plugin-blender-3d` latest `0.2.1` = the advised rungs), both advised tarballs `200`, `modified` still frozen at the publish minutes; OSV `18320`/`18321` `aliases None`, `modified` frozen `06:45:15Z`; GHSA malware-lane echo-checked head read carries the pair's own `GHSA-q4qv`/`GHSA-c7hg` unchanged. The mint-path-vs-GHSA-existence counter-example stands a sixth read — tripwire unchanged: seizure or tarball `404` while the GHSAs stand = the trigger law moves to GHSA-keyed. Sweep context → [218th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-eighteenth-sweep).

## October 26, 219th sweep follow-up (~17:3x UTC): SEVENTH live sweep — `≈11 h` under its own critical GHSAs — and the pair SAT OUT THE ENFORCEMENT WAVE THAT ATE `≈20` NAMED NAMES IN `11 MIN`

The `16:17`–`16:28` ghsa-malware live-detection wave seized everything it named in `≈2 min` — capsense, eforms, the greenlake/ppa/drone/sxm fleet, the new css-named batch — and the walknpm pair, whose critical GHSAs (`q4qv`/`c7hg`) were minted by the MIRROR-IMPORT path at `06:30:30Z`, was not in it: `todo-cli latest 2.0.1` `modified` frozen `00:55:52Z`, `blender latest 0.2.1` frozen `00:55:25Z`, both advised tarballs `200`, OSV `18320`/`18321` STILL `aliases None` (`modified` frozen `06:45:15Z`) `11 h` after their GHSAs existed. The enforcement-lane law sharpens again on the same pair: what gets seized is written by the bot's LIVE pass, not by the mirror — a miner can now advertise a critical GHSA for half a day while the registry eats a cohort around it. Falsification terminus remains: if this pair NEVER moves, the law reads "mirror-advised names are permanently exempt until the bot itself re-detects."

## October 26, 220th sweep follow-up (~19:4x UTC): THE COHORT SPLITS — the pre-registered terminus arrived inside ONE sweep, on HALF the pair

The "permanently exempt" reading is DEAD, killed between sweeps exactly where the 219th pre-registered its falsification test: `@walknpm/dsh-plugin-blender-3d` is **WIPED WHOLE-NAME** — packument `404` (the publish-poc whole-name-erasure grammar, not a holder costume), advised tarball `404`, **jsDelivr `404`, unpkg `404`** = four-lane death, no install or sample path survives — while **`@walknpm/todo-cli` is STILL LIVE**: packument `200`, `latest 2.0.1` = the advised miner-bearing rung, tarball `200`, `modified` frozen `00:55:51Z`, `≈18.8 h` installable since publish and `≈13.2 h` under `GHSA-q4qv`. **THE MINT-PATH LAW SURVIVES REFINED, NOT DEAD: it always described the WAVE automaton (`GHSA`→holder in `≈2 min`); the WIPE lane is a DIFFERENT machinery and it reached a mirror-cohort name `≈13 h` after the wave, ONE NAME AT A TIME — cohort-mates sharing a publisher, a payload (the byte-identical `miner.sh`), and same-second GHSAs can get different dispositions.** AND THE WIPED NAME LEFT NO PAPER TRAIL: OSV `18321` `modified` STILL frozen `06:45:15Z` with `aliases None`, `GHSA-c7hg` `updated_at` STILL frozen `09:33:37Z` — the registry ate the package while both advisory lanes sat motionless = **enforcement is INVISIBLE in the advisory clocks; registry disposition must be probed at the registry, never inferred from OSV/GHSA staleness (the stale-mirror law's enforcement-side twin)**. Standing tripwires: does `todo-cli` get the same whole-name wipe (split completes vs permanent name-level split); does `18321`/`c7hg` EVER re-stamp post-wipe (would falsify the no-paper-trail read); does either record ever retro-join. Sweep context → [220th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-twentieth-sweep).

## October 26, 221st sweep follow-up (~21:3x UTC): EIGHTH live sweep — the split SURVIVES the window, `todo-cli` `≈20.5 h` installable / `≈14.9 h` under its own critical GHSA

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` = the advised miner rung, tarball `200`, `modified` frozen `00:55:52Z`; `blender` re-confirmed dead on all four lanes with the CORRECTED jsDelivr grammar (`cdn.jsdelivr.net/npm/<name>@<ver>/package.json` — the `/+package.json` variant `404`s even on live names, left-pad control proved it; see stream self-captures). The 220th's PRIMARY falsification test came back NEGATIVE this sweep: the wipe lane has still moved exactly ONE of the byte-identical cohort's two names, `≈1.5 h` after the first strike; `18321`/`GHSA-c7hg` clocks still frozen through the split window (no paper trail, second read). The name-level split either hardens into a law ("mirror-cohort wipes pick names, not cohorts") or completes within the next window — tripwire unchanged: `todo-cli` packument `404` = split completes; tarball `404` with packument `200` = a FOURTH disposition (surgical excision of the advised rung, the @worca grammar) arriving on the mirror lane for the first time. Sweep context → [221st stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-twenty-first-sweep).

## October 26, 222nd sweep follow-up (~23:2x–23:5x UTC): NINTH live sweep — the split survives a SECOND full window, all five lanes sampled

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` = the advised miner rung, `modified` frozen `00:55:52Z`; the advised tarball now probed on ALL THREE registry lanes this sweep — registry `200`, unpkg `200`, jsDelivr `200` on `@2.0.1/package.json` = the advised miner version is fully installable everywhere `≈22.5 h` after publish and `≈17 h` under its own critical `GHSA-q4qv` (clocks STILL frozen: `q4qv updated_at 09:31:06Z`, `18320`/`18321` `modified 06:45:15Z` `aliases None`). `blender-3d` packument re-confirmed `404` (whole-name death holds, no re-registration). The 220th's split now has TWO survived windows: the WIPE lane has moved exactly one of the byte-identical cohort in `≈5 h` of its own lane-time; if the split survives a third window the law hardens from "wipes pick names" to "cohort membership never predicts disposition, per-name per-disposition only." Tripwires unchanged: packument `404` = split completes; tarball-`404`-with-packument-`200` = the @worca surgical grammar arriving on the mirror lane. Sweep context → [222nd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-twenty-second-sweep).

## October 27, 223rd sweep follow-up (~01:2x–01:5x UTC): TENTH live sweep — the split survives its THIRD window: the law hardens

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` = the advised miner rung, tarball `200`, `modified` frozen `00:55:52Z` — `≈24.9 h` post-publish, `≈19 h` under its own critical `GHSA-q4qv` (frozen `09:31:06Z`); `18320`/`18321` frozen `06:45:15Z` `aliases None`; `blender-3d` stays four-lane dead. THREE full windows survived by the byte-identical cohort's untouched half: the reading upgrades from "wipes pick names" to **cohort membership NEVER predicts disposition — per-name per-disposition only** (the falsification that would still kill it: `todo-cli` packument `404` = a late completion; tarball-`404`-with-packument-`200` = the @worca surgical grammar arriving on the mirror lane). Sweep context → [223rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-one-hundred-and-twenty-third-sweep).

## October 27, 224th sweep follow-up (~03:3x–04:0x UTC): ELEVENTH live sweep — fourth window running

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` advised miner rung, tarball `200` — `≈26.5 h` post-publish, `≈18+ h` under its own critical `GHSA-q4qv` (frozen `09:31:06Z`); `18320`/`18321` frozen `06:45:15Z` `aliases None`; `blender-3d` stays four-lane dead. Hardened law stands (cohort membership never predicts disposition). Falsifiers unchanged: packument `404` = late wipe completion; tarball-`404`-with-packument-`200` = @worca surgical grammar on the mirror lane. Sweep context → [224th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-one-hundred-and-twenty-fourth-sweep).

## October 27, 225th sweep follow-up (~05:2x–05:5x UTC): TWELFTH live sweep — fifth window running

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` advised miner rung, `modified` frozen `00:55:52Z` — `≈29 h` post-publish, `≈20 h` under its own critical `GHSA-q4qv` (frozen `09:31:06Z`); `18320`/`18321` unchanged `aliases None`; `blender-3d` stays four-lane dead. The split law holds a fifth window. Falsifiers unchanged: packument `404` = late wipe completion; tarball-`404`-with-packument-`200` = @worca surgical grammar on the mirror lane. Sweep context → [225th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-one-hundred-and-twenty-fifth-sweep).

## <a id="october-27-226th-sweep-follow-up-073x-utc-thirteenth-live-sweep--sixth-window-running"></a>October 27, 226th sweep follow-up (~07:3x UTC): THIRTEENTH live sweep — sixth window running

`@walknpm/todo-cli` packument `200`, `latest 2.0.1` advised miner rung, `modified` frozen `00:55:52Z` — `≈30.5 h` post-publish, `≈21.5 h` under its own critical `GHSA-q4qv` (frozen `09:31:06Z`); `18320`/`18321` unchanged `aliases None` `modified` frozen; `blender-3d` stays four-lane dead (packument `404`). The WIPE lane did not visit a thirteenth sweep; the split law holds a sixth window. Sweep context → [226th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-27-one-hundred-and-twenty-sixth-sweep)
