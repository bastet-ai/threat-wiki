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

Sweep context → [213rd stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-26-one-hundred-and-fifty-third-sweep) · sibling class → [dsh-native page](dsh-native-keer1024-npm-seizure-scoped-twin-survival-rollback-to-stage-rust-worker-exe-october-2026.md) · live-advised class → [wave-three 207th](testmetest-wave-three-osv-batch-agent-tooling-ghsa-at-birth-enforcement-asymmetry-october-2026.md#october-25-207th-the-fleet-that-outlived-its-own-advisories)
