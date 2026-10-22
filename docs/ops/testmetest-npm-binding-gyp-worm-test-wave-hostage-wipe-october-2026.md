# The `*-testmetest` npm wave: a binding.gyp credential worm run as a PUBLIC TEST BENCH (`data-pipeline-testmetest`, `event-emitter-testmetest`, `log-sink-testmetest`, `pixel-map-testmetest`, `test-brotli-testmetest`) — Phantom-Gyp hook + Bun payload + self-republish worming + a NEW hostage dead-man switch that wipes `~/` when the stolen token is revoked (OSV `MAL-2026-18177`–`18181`, Oct 21–22, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- binding-gyp
- node-gyp
- Bun
- credential-stealer
- self-propagating-worm
- ransomware-adjacent
- data-wiping
- dead-man-switch
- github-token
- shai-hulud-lineage
- miasma
- phantom-gyp
- osv
- october-2026

## Summary

Between `16:00Z` and `18:00Z` on **October 21, 2026**, OSV published five unusually detailed malware records — `MAL-2026-18177`–`18181` — for five npm packages sharing the `-testmetest` name suffix. The records describe, in full, a **self-spreading credential-stealing worm that reuses the June-2026 `binding.gyp`/node-gyp install hook ("Phantom Gyp", the Miasma/Shai-Hulud-descendant technique this wiki already tracks on [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md))**, ships its stage-2 as an AES-GCM-encrypted blob piped into a **downloaded Bun runtime**, and adds an escalation the ledger has not recorded in this family before: **a hostage dead-man switch — a `net-health-checker` user service that runs `rm -rf ~/` when the victim revokes the stolen GitHub token** (the Tensorlake hostage-token grammar, Oct 8, now ported into the binding.gyp lane).

What makes this wave distinct is its **posture**: the accounts publish under openly disposable names (`testnewtestme2`, `newtestnewdont`), one package's `package.json` literally poses as a staged-publishing placeholder (`"stub": true`, "Temporary package placeholder for staged publishing"), versions are named for their role in a pipeline (`event-emitter-testmetest` 1.0.6–1.0.7 ship a FILLER stage "first to test the delivery chain… and then to ship it" the full stealer), and the OSV text documents the whole chain — including **decrypted in-memory payload hashes** (`939/941/948 KB` Bun payloads, `sha256 47de657a…`, `1fc5f1ba…`, `ca312e76…`). Whether this is an analyst red-team harness published carelessly or an operator testing the delivery chain in public, the artifacts are live weapons: the same grammar, unmasked, is one republish away from a real-name campaign.

- **The five names (OSV):** `data-pipeline-testmetest` `2.0.1` (`18177`), `event-emitter-testmetest` `1.0.6/1.0.7/4.1.0/5.0.0` (`18178`), `log-sink-testmetest` `1.0.1` (`18179`), `pixel-map-testmetest` `0.0.1/0.0.2` (`18180`), `test-brotli-testmetest` `1.0.0` (`18181`).
- **Publisher accounts:** `testnewtestme2` (`data-pipeline`, `event-emitter`, `log-sink`, `test-brotli`), `newtestnewdont` (`pixel-map`, plus the benign-looking decoys `color-utils-testmetest`, `string-helpers-testmetest`, `byte-stride-testmetest`).
- **Registry state at this wiki's check (~05:3xZ Oct 22): ALL EIGHT names (five malicious + three decoys) are ALREADY EMPTY on npm** — `versions: []`, `dist-tags: {}`, but the documents still answer `200` with surviving `time` blocks. Two scripted seizure windows survive in the timestamps: `15:07:26`–`15:07:38Z` (four names, `12 s` apart) and `23:26:04`–`23:26:14Z` (pixel-map + the three decoys, `10 s` apart). **The npm-side action PREDATED the OSV publications (`16:00`–`18:00Z`) by up to `≈9 h` for the first batch** — the inverse of the `@sudobility` advised-and-installable pattern read the same night.
- **GHSA: ZERO across all five names** at `≈13 h` post-birth (verified by per-name `affects=` queries, the route this wiki's own capture says to use) = OSV-only coverage; a Dependabot-blind consumer never sees this wave.

## Confirmed mechanics (from the OSV record texts + IOC blocks)

- **Hidden install hook, no lifecycle script:** `binding.gyp` with a source entry `<!(env node index.js >/dev/null 2>&1; echo stub.c)` makes node-gyp execute `index.js` during the CONFIGURE phase of `npm install` — byte-for-byte the Phantom-Gyp primitive (`binding.gyp` sha `fda4df74…` in `data-pipeline`/`pixel-map`; `98caee01…` in `event-emitter` 1.0.7+/`log-sink`; `9a876c0a…` in `test-brotli`). `test-brotli-testmetest` adds the explicit `install` script (`node-gyp rebuild`) ON TOP of the hook — belt and braces.
- **Loader → Bun:** obfuscated `index.js` decrypts (AES-GCM per-record notes; `data.bin` shipped in `log-sink`/`pixel-map`/`event-emitter` 5.0.0; **Brotli-compressed** payload in `test-brotli`) and pipes the plaintext into `bun run -`, downloading the Bun runtime from GitHub Releases if missing — the runtime-swap evasion that defeats Node-scoped process monitoring, unchanged from June's Miasma wave.
- **Payload:** `≈939–948 KB` stealer (three rebuilds observed with distinct hashes; `log-sink` 1.0.1 and `event-emitter` 5.0.0 share `ca312e76…` byte-identically). Steals GitHub, npm, PyPI, RubyGems and cloud credentials; **commits them to a PUBLIC repository the worm CREATES inside the victim's own GitHub account** (description `project-utils`); **republishes the victim's packages carrying the same hook** = classic Shai-Hulud-family self-propagation.
- **NEW for this family — hostage dead-man switch:** with a GitHub token found, the payload installs a `net-health-checker` user service that **runs `rm -rf ~/` (and `~/Documents`) once the stolen token is revoked** (dropped file `~/.local/bin/net-health-checker.sh`, sha `46ebfd3d…`). The OSV record carries the remediation ORDER as a warning: remove the service (file + systemd unit / LaunchAgent) BEFORE revoking the token, then rotate everything reachable. This is the Tensorlake `hostage-token` grammar (`tensorlake-npm-compromise-shai-hulud-hostage-token-worm-stepsecurity-october-2026.md`) ported onto the binding.gyp execution primitive — the two October/June escalations merged.
- **Version-as-pipeline tell:** `event-emitter-testmetest` `1.0.6` (runs on load) → `1.0.7` (moves execution to install via the gyp hook, filler payload) → `4.1.0` (stealer inline) → `5.0.0` (stealer encrypted in `data.bin`); `pixel-map` `0.0.1`→`0.0.2` `≈3.5 h` later = same loader, re-encrypted + additionally obfuscated. This is CI behavior run against the public registry.

## This wiki's verification + reads (Oct 22 ~05:2x–05:3x UTC, one-hundred-and-seventy-first sweep)

- All five OSV records live at the resume point (`18177`–`18181` contiguous `200`, `18182`–`18210` `404`); every one is `aliases: None` = **born GHSA-less**, and per-name `affects=` queries return zero advisories `≈13 h` on. The finder/source block is EMPTY (no `database_specific` campaign field) — unlike the kam193 lane, these read as analyst-authored OSV-native dossiers: publish timestamps sit on `30-minute` grid values (`16:00`/`17:30`/`18:00Z`), not machine import ticks (filing-supplied `published` metadata), and the IOC blocks enumerate per-file sha256s with **`IN_MEMORY`-source entries for DECRYPTED payloads** — the record itself is the forensic artifact, which no registry seizure can erase.
- **Provenance pinned this sweep:** `ossf/malicious-packages` PR **`#1656`** ('report: npm/data-pipeline-testmetest 2.0.1, npm/event-emitter-testmetest …') was **MERGED `04:15:25Z` Oct-22** and the five records' `modified` timestamps are the `04:30:03`–`03.55Z` import tick — `≈15 min` after the merge. The wave is a HUMAN/community-filed queue submission, not a bot import — the same queue lane that merged `#1655` (litellm `1.107.0`) the prior evening.
- Registry forensics via surviving `time` blocks (the npm `time` document outlives the versions — durable mechanic re-attested): all eight names `200` with `versions: []`; seizure windows `15:07:26`–`38Z` and `23:26:04`–`14Z` Oct-21, `10–12 s` scripted batches = npm security-holder batch grammar. **The registry seizures PREDATE the records surfacing on the API (`04:30Z` Oct-22) by `≈9–13 h`** — seizure-before-advisory on the npm lane, the inverse of the `@sudobility` class read the same night (note the caveat: filing-supplied `published` values `16:00`–`18:00Z` sit between the two clocks; the API-surfacing clock is the `modified` tick).
- The same night, the SAME registry left the fully-advised `@sudobility` scope untouched for `≈14 h` = enforcement is not a policy, it is a per-queue outcome; quote both classes when advising consumers.
- Prior art chain on this wiki: June `binding.gyp` worm ([page](binding-gyp-npm-cicd-worm.md)) → Mini Shai-Hulud Bun stealer → Aug keyv wave → Oct-8 Tensorlake hostage token → **this wave = binding.gyp primitive + Bun + worming + hostage wipe in one package**, with the June tooling-blindness (no lifecycle script to flag) fully preserved.

## Hunt keys

- npm `package.json`/tarball: `binding.gyp` present in a package with NO native addon; hook string `<!(env node index.js`; `index.js` a single multi-MB obfuscated line; `"stub": true` + "Temporary package placeholder for staged publishing" (the staging-grammar costume, now ninth-plus sighting); dependency on the `bun` runtime; GitHub Releases `oven-sh/bun` fetch at runtime.
- Post-incident: `~/.local/bin/net-health-checker.sh` + matching systemd unit/LaunchAgent; public repos created in maintainer accounts with description `project-utils`; republished package versions whose tarballs gained a `binding.gyp`.
- **Remediation order (from the record itself): remove the dead-man service BEFORE revoking the GitHub token; then rotate all reachable credentials.**

## Monitor

- Whether the `-testmetest` grammar goes quiet (test bench retired) or reappears WITHOUT the test suffix — the same code under a real-looking name is the graduation event; watch OSV for the payload hashes (`ca312e76…`, `47de657a…`, `fda4df74…`, `98caee01…`) and the hook string on other names.
- GHSA mirror arrival for the five names (expect: never — the wave was registry-seized before advisories, and GHSA botting keys on live packages).
- `net-health-checker` / `project-utils` sightings in victim postmortems; whether vendor telemetry vendors (StepSecurity/Socket/Snyk) publish an October binding.gyp-wave note at all (the June class names they tracked are not these).
- Whether the seized names get holder-purged to `0.0.1-security` (the batch-grammar close) or stay version-empty shells.
- Attribution: no vendor named these five at check; public reporting around the binding.gyp class covers the June wave (56-57 packages, "Phantom Gyp"/Miasma) — an October test-bench follow-on writeup would settle operator identity.

Sweep context → [171st stream section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-22-one-hundred-and-seventy-first-sweep).
