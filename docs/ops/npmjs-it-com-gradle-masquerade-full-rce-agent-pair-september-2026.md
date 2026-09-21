# The `npmjs.it.com` agent pair: two Element Plus-themed npm packages that masquerade as Gradle instrumentation to drop a full remote-access agent — with sentinel-file targeting of fintech/trading monorepos — on install AND on import (Amazon Inspector via OSV, Sep 21, 2026)

## Tags
- ops
- npm
- supply-chain
- malicious-package
- dependency-confusion
- scope-squat
- typosquat
- remote-access-trojan
- command-and-control
- install-script
- import-time-execution
- obfuscation
- gradle
- Amazon-Inspector
- OSV
- npmjs.it.com

## Summary

In the Amazon-Inspector-sourced OSV batch that landed **September 21, 2026 (~04:00 UTC)**, two npm packages — `@asenfotech/unplugin-element-plus` (`MAL-2026-16318`, versions 2.9.3/2.9.5) and `element-plus-vite-cli` (`MAL-2026-16331`, versions 2.9.3/2.9.5) — carry the same dropper dressed as **Gradle build tooling** inside a package that advertises itself as Vue/Element Plus tooling. Unlike the recon beaconers dominating the same week's advisories, this pair is a **full operator-driven remote-access agent**: the dropped MJS payload registers a persistent agent ID, long-polls for tasks, and executes attacker-supplied `exec`, `ls`, `download`, `upload`, `delete`, `ps`, and `move` commands. The C2 host, **`npmjs.it.com` — a lookalike of npmjs.com** — was **live and answering at this wiki's check on Sep 21 (~05:25 UTC)**: `POST /api/register` returns HTTP 400 `invalid agent_id` behind Cloudflare. Both npm names had their versions unpublished at the same check. No public vendor writeup was findable at capture time (search for the package names + "malicious" returns nothing) — this wiki's record is built directly from the OSV/Inspector analyses plus live registry and C2 probes.

The targeting detail is the marquee: the import-time path is **gated on a hardcoded allowlist of workspace marker files** characteristic of specific fintech/trading monorepos — `src/api/AITrading.js`, `src/api/agentShot.ts`, `src/pages/ETF-quant-trading/history.vue`, `src/views/orderCenter/orderCenter.vue`, `src/pages/GameAggregator/GameAggrBusinessPage/index.tsx`, `src/master/src/router/routes.tsx`, and similar (nine sentinels in one variant, workspace markers in the other). Outside a matching repo the package sits quiet. **This is not spray-and-pray malware — it is a targeted implant that uses npm as its delivery rail**, and the beacon-only failure mode means victims who `npm install` without importing never see activity.

## Confirmed mechanics (from the `MAL-2026-16318` / `MAL-2026-16331` Amazon Inspector analyses)

- **Cover story:** `index.js` is a small, genuine-looking Element Plus resolver / Vite CLI stub. The bulk of the tarball lives under `lib/gradle/` (or in `tooling-bootstrap.cjs`), naming every component after Gradle daemon infrastructure (`postinstall-run.cjs`, `gradle-daemon-sync.cjs`, `homeGradleDaemon`, `tooling-api-runtime.mjs`) — none of which relates to the declared Vue purpose.
- **Payload assembly:** ~85–90 base64 chunks are embedded across source files (`agent-bytecode.segments.cjs` and siblings), concatenated and decoded via `Buffer.from(joined, 'base64')` at runtime.
- **Dropper:** the decoded MJS agent is written to a Gradle-cache-sounding path — `~/.gradle/caches/transforms-3/8.7/instrumented/.../instrumentation-agent-runtime.mjs` (16318) or `~/.gradle-cache/tooling-api-runtime.mjs` (16331) — then **spawned as a detached, hidden Node process** (`detached: true, stdio: 'ignore', windowsHide: true`, `child.unref()`, PID-file tracked in 16331).
- **Trigger paths (both):** the declared lifecycle hook (postinstall / preinstall+postinstall) **and** the `main`/`bin` entry chain — the bootstrap runs again on plain `require()`/import, so the agent re-drops on every build that touches the package.
- **Targeting gate (16331, import path):** the bootstrap walks up from `cwd`/`INIT_CWD` looking for **nine hardcoded sentinel files** characteristic of fintech/trading applications; the agent only drops when a sentinel matches. 16318 uses a comparable workspace-marker allowlist (specific `GameAggregator`/`routes.tsx` paths). A miss = fully silent package.
- **C2 protocol:** register at `POST https://npmjs.it.com/api/register` with `os.hostname()`, `os.userInfo().username`, `os.type()/release()` and a **persisted agent UUID cached at `~/.gradle-cache/.aid`**; then long-poll `/api/task/<agent_id>`; results POST to `/api/result/<agent_id>`; file exfil POSTs arbitrary local file contents to `/api/file/<agent>/<task>`. Operator commands: `exec` (spawns `/bin/sh -c` or `cmd.exe /c` on attacker-supplied strings), `ls`, `download`, `upload` (writes attacker bytes to arbitrary paths), `delete` (`rm -rf`), `ps`, `move`.
- **Evasion knobs:** `C2_TLS_INSECURE` sets `NODE_TLS_REJECT_UNAUTHORIZED=0`; `C2_SERVER_URL` overrides the hardcoded host — the agent is operator-reconfigurable after install.
- **Domain:** `npmjs.it.com` is a subdomain of `it.com` crafted to read as `npmjs.com` in a hurried glance or a log skim. At this wiki's Sep 21 check it resolved to Cloudflare (`104.21.5.72` / `172.67.133.40`) and the register endpoint responded actively.

## Registry state (live checks by this wiki, Sep 21 ~05:25 UTC)

| Name | Versions | State |
|---|---|---|
| `@asenfotech/unplugin-element-plus` | 2.9.3, 2.9.5 (per OSV refs) | **versions unpublished** (registry returns empty) |
| `element-plus-vite-cli` | 2.9.3, 2.9.5 (per OSV refs) | **versions unpublished** (created Sep 16 08:06 UTC, modified Sep 16 16:34 UTC, `latest` empty) |
| `npmjs.it.com` C2 | — | **LIVE** — `/api/register` → HTTP 400 `invalid agent_id` behind Cloudflare |

Note the ~5-day gap between package creation (Sep 16) and advisory landing (Sep 21) — installs during that window are the exposure period, and the C2 still answering means **any surviving infected host is still beaconable**.

## Why it matters (durable reads)

1. **An npm-distributed implant impersonating Gradle infrastructure is a cross-ecosystem detection trap.** Analysts triaging `~/.gradle-cache/tooling-api-runtime.mjs` or a Gradle-masquerading process will look at Java/Android toolchains, not the Node supply chain. Hunt the *path + node-parent* combination, not the name.
2. **Sentinel-file gating is the targeted-attack adaptation of supply-chain delivery.** The operator buys reach from npm but spends it only where the repo fingerprint matches. Defenders of fintech/trading codebases should treat any dependency-tree entry whose files mention `gradle`/`instrumentation` inside a JS package as hostile by default. It also means **beacon-free, behavior-free dormancy is normal for this class** — a quiet install is not a clean install unless the dependency tree says it shouldn't be there.
3. **`npmjs.it.com` reads as the operator choosing the registry's own brand as C2 camouflage** — egress alerts keyed on `npmjs.com` may whitelist-adjacent this hostname; alert on `npmjs.it.com` exactly, and generically on any outbound `*.it.com` (or other registrable-suffix lookalikes) from build hosts.
4. **Persisted `.aid` agent UUIDs + task long-polling is standard post-exposure tradecraft ported to Node.** Existing implant-detection logic (registration POST, task-poll cadence, file-read-and-POST bursts) transfers directly; the novelty is only the delivery rail.
5. **Amazon Inspector caught this before any vendor blog.** As already recorded on the [algamil7x page](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md), `## Source: amazon-inspector` OSV/GHSA entries are now the fastest structured feed for npm implant analysis — this cluster had zero public coverage at capture; the Inspector text is the primary.

## Hunt guidance

- **Filesystem:** `~/.gradle-cache/` or `~/.gradle/caches/transforms-3/.../instrumented/` paths created by a **node** process on developer/CI hosts; any `.mjs` under a Gradle-named path whose parent process is Node rather than Gradle; `~/.gradle-cache/.aid` files.
- **Process:** `node <path>/tooling-api-runtime.mjs` or `instrumentation-agent-runtime.mjs` spawned detached with no controlling terminal; npm install trees containing `tooling-bootstrap.cjs`, `postinstall-run.cjs`, `gradle-daemon-sync.cjs`, or `agent-bytecode.segments.cjs`.
- **Network:** any DNS/HTTPS to `npmjs.it.com`; POST bodies to `/api/register`, `/api/task/`, `/api/result/`, `/api/file/`; env vars `C2_TLS_INSECURE` / `C2_SERVER_URL` in process environments.
- **Lockfile audit:** the two names above at all versions, plus anything else shipping base64-chunk arrays assembled with `Buffer.from(...,'base64')` + detached spawn (static grep: `detached: !0`/`detached: true` with `stdio:'ignore'`).
- **Sentinel awareness:** orgs whose repos contain files like `src/api/AITrading.js`, `src/pages/ETF-quant-trading/*`, or an `orderCenter` view should assume they were explicitly fingerprinted and audit dependency trees from Sep 16 onward.

## See also

- [The `algamil7x` npm DNS-exfil recon cluster](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — same Amazon-Inspector feeder, same week, recon-only cousins; same intake window, different clusters (compare destination before merging).
- [The Telegram `chat_id 1064260758` dependency-confusion recon cluster](telegram-chatid-1064260758-dependency-confusion-recon-cluster-september-2026.md) — the other new cluster from the same Sep 21 Inspector batch.
- [WeaselBiscuit](../tools/weaselbiscuit-npm-stealer-beavertail-ottercookie-dprk-opensourcemalware-september-2026.md) — import-time execution npm cluster from the prior week; import-time paths defeat npm ≥ 12 install-script approval the same way.
