# Equation of Compromise: JFrog unifies the on-wiki mathmain/mathsbase/math-universe loader trio into a six-month targeted npm campaign — the scrypt password was RECOVERED (a 3×3 symmetric Pascal matrix fed through the victim's own LU factor), tasking runs over Ethereum Sepolia contracts AND a dual-channel Slack agent that ships payloads as message chunks, and a GitHub Actions worker farm manufactured up to 40.7 MILLION fake downloads per package (JFrog, Sep 21, 2026)

## Tags
- ops
- supply chain attack
- npm
- mathjs
- encrypted loader
- scrypt
- AES-256-GCM
- targeted attack
- quantitative finance
- DeFi
- Ethereum Sepolia
- smart contract C2
- Slack C2
- GitHub Actions abuse
- download inflation
- fake popularity
- JFrog
- Contagious Interview adjacent
- trojanised clone

## Summary

JFrog Security Research published **"Equation of Compromise: Anatomy of a Live npm Supply-Chain Campaign"** on **September 21, 2026** (canonical: `research.jfrog.com/post/equation-of-compromise/`, live-verified by this wiki), presenting one campaign behind what every prior vendor — including this wiki's [mathmain trio page](mathmain-encrypted-loader-npm-trojanised-mathjs-trio-safedep-september-2026.md) — reported as separate incidents. The durable headline: **the encrypted payload is no longer unread.** SafeDep's 17,000+ failed password guesses ended when JFrog exploited the fact that **AES-GCM's auth tag is a free oracle (~50 ms per candidate, no false positives)** and enumerated structured matrices. The trigger is `math.lusolve()` on the **3×3 symmetric Pascal matrix `[[1,1,1],[1,2,3],[1,3,6]]`** — the malware keys on `JSON.stringify` of the LU factor's `L._data` (`[[1,0,0],[1,1,0],[1,0.5,1]]`), exactly the construction on-wiki. JFrog's read: **a targeted operation aimed at quantitative/DeFi developers ("maybe an interview campaign")** — the implant only ever runs for people whose normal work calls a linear solver.

The campaign is bigger and older than the trio: **25+ malicious package versions from March 3 to Sep 17, 2026** (JFrog IoC table, XRAY IDs assigned), **two independent command channels** (Ethereum **Sepolia** smart-contract registries + a **dual-bot Slack agent** whose tasking channel is DH-encrypted and whose payload delivery is the chat messages themselves — chunked `{"t":"s"}/{"t":"c"}/{"t":"e"}` transfer protocol, no size ceiling), and a **GitHub Actions download farm** that manufactured **up to 40,715,826 fake downloads for a single package** (`events-sync`) to give disposable packages the look of established libraries **before** they are weaponised — roughly a day apart.

## The recovered trigger (what SafeDep could not do)

- Same loader, same layout (16-byte salt | 12-byte IV | 16-byte tag | ciphertext, `scryptSync(password, salt, 32)` → AES-256-GCM, write plaintext to disk, `require()` it) as documented on the [mathmain page](mathmain-encrypted-loader-npm-trojanised-mathjs-trio-safedep-september-2026.md).
- **The password was never brute-forced blindly — it was pattern-enumerated against the GCM tag oracle**: identities, small integer matrices, textbook examples… the winner was the **symmetric Pascal matrix**; `math.lup([[1,1,1],[1,2,3],[1,3,6]]).L._data` stringified decrypts the first blob, which yields the filename for the second, and "from there the whole package opened up."
- The hook placement read on-wiki is confirmed: the injected `removeSolveValidation(L._data)` runs **after** the math is correct and its return value is discarded — the victim's answer is always right, the trigger is silent.
- **Defender bonus artifact:** every package that consumes mathjs-shaped libraries and calls `lusolve`/`solve` in its normal workload is, by construction, a candidate victim profile — this is a filter for a profession, not a scattergun.

## Command-and-control: two channels that fail independently

1. **Ethereum/Base Sepolia smart-contract tasking** (on-wiki pattern family: ChainDrop, NullReceiver, KREMLIN, GoCaracal, ChainScript — this is the campaign-scale member). JFrog lists **13 contract addresses** across Ethereum Sepolia (`WalletDataRegistry`, `WebDataRegistry`, `WalletHelloWorld` variants, deployed Mar 5 – Jun 18) and Base Sepolia (Aug 28). **This wiki verified deployment live:** `eth_getCode` on the Jun 8 `WebDataRegistry` `0xc0445F1b679DC46280A0f03F451bdf613b5A0feA` via `ethereum-sepolia-rpc.publicnode.com` returns ~16 KB of bytecode — the enrollment/tasking registry is still on-chain. Registry-brand JSON-RPC endpoints (Alchemy/Infura project keys, three pairs in the IoC list) are the egress shape — **JSON-RPC to Sepolia from a developer workstation or build agent is the hunt signal** (same tell as this month's ChainScript page).
2. **Slack as a second, independent channel** — the genuinely new tradecraft:
   - **Reporting bot** (write-only, plain base64 messages) + a **tasking bot** whose bot token and channel ID are themselves AES-GCM-encrypted under the *trigger password*, and whose message bodies are encrypted under an **X25519 DH secret against a server key hardcoded in the malware**. Cracking one channel gives you nothing on the other; JFrog could not open **fifteen task payloads**.
   - The agent polls `conversations.history` **every 10 seconds, no jitter** (the hunt tell), acts **only on one hardcoded operator user ID** (holding the token ≠ tasking implants), and records the latest-message timestamp at startup so a fresh victim never replays the operator's back catalogue.
   - **Payload = the chat messages.** `{t:"s"}` opens a transfer, `{t:"c"}` delivers chunk *n*, `{t:"e"}` reassembles to `lib/cjs/utils/subwatcher`, chmod 755, execute. No file host, no download URL, no practical size ceiling — the messaging platform IS the file transfer. A body containing `exitexitexit` = shutdown order (marker deleted, parent killed).
   - IoCs include two Slack workspaces (tasking channels `C0ATC9UKKA4` / `C0B8GEPFMK9`, reporting `C0B554AQF1S` / `C0B8XPGCKQS`, operator IDs `U0B51HGMGJW` / `U0B91JWCVT6`, redacted `xoxb-…` tokens) and **two Telegram bot tokens + chats** in the clear in JFrog's list — unusual to see Telegram material in a campaign whose npm peers this wiki tracks beacon to Telegram chats.

## The download factories: weaponized GitHub Actions

- Three public GitHub accounts — `andrewstory18` (`worker1–10`), `davidbabcock96` (`job_worker1–10`), `azlanrahman322-creator` (`job-worker1–10`) — each running 10 repos with the same four files: `commands.json` (AES-encrypted target list), a minified `index.js` driver, a 122 KB Rust **WASM decoder** (identical md5 `91e020c13cb97a6365135b53b0d0fe5f` across all farms), and a workflow that executes the driver on every push. The driver resolves the tarball URL and **downloads it N times at 1-second intervals, then throws the bytes away** — only the completed request matters, because npm counts requests.
- **The key to the "encrypted" target list (`npm_workvr_protect_key_v1`) is compiled into the WASM in plain ASCII** — encrypted so the public repo wouldn't name its victims, key shipped in the same repository. JFrog recovered the full scheduling history: `events-sync` 40.7M, `events-channel` 38.2M, `indexed-btree` 38.0M, `quick-events` 37.9M, `btree-core` 37.7M, `@oliviamcdaniel12/safer-buffer` 18.0M, `matrixflow-js` 14.8M…
- Every commit across all farms carries the message **"Update commands from job_master"**, and the two newer farms receive **byte-identical `commands.json` pushes** = one orchestrator fanning one config to multiple hands. `job_master` itself is not public. JFrog: the farm **was still running as of publication**.
- Durable registry-side signal (JFrog's best one-liner for defenders): **over a million downloads with ZERO dependent packages and zero dependent repositories** held for every vehicle in the campaign. And the practical trap: **npm's `dependencies:` search qualifier is not supported and silently degrades to fuzzy matching** — use ecosyste.ms or libraries.io for reverse-dependency truth.

## Attribution-grade account plumbing (no actor named)

- One npm account per package; emails alternating `@proton.me`/`@outlook.com`; accounts abandoned the moment a package is removed; every GitHub identity in the cluster has **zero followers, zero following, zero stargazers**.
- The join was a reused handle: npm `weed0` publishes from `tinystar368@gmail.com`, and `tinystar8` (publisher of the backdoored `mathsbase`) uses `tinystar368@proton.me` — that collision stitched the DeFi-lure persona packages to the malware cluster; GitHub identity `UmajiHidekata` signs commits as `tinystar368@gmail.com`; the inflation tool's first commit is by a fourth identity, `andrewstory18`.
- Only 2 of 5 malicious packages had public repos, and **none of the malicious code was ever committed to GitHub** — the loader exists only in the npm tarball, injected at publish time. `tinystar8/mathsbase` carries all 5,694 genuine mathjs commits (3,674 still signed by mathjs's author) plus 136 mechanical rename commits by `Blustdp` = a repo that "looks like a long-maintained library at a glance."

## State at this wiki's Sep 21 check (~17:30–18:00 UTC)

- **Still live on npm:** `mathsbase@1.0.2` (latest; modified Sep 15 — tarball pulled and inspected by this wiki: **no `event.js` loader in 1.0.2**, but the slot carries obfuscated `graph.js` (`dcebfdf7…`, matches the on-wiki hash note), `fraction.js`, `bignumber/type.js`; the LICENSE infection marker string is ABSENT = not self-marked infected; per JFrog the LOADED version is `1.0.1`), `math-universe@1.0.2` (live, latest), `matrixhub@6.15.1` (live, inflated PuP per JFrog), `matrixflow-js@3.2.2` (live; per JFrog 3.2.2 "quietly removed the loader" — the sealed 3.2.1 payload keyed on a raw-matrix SHA-256 match means its trigger had to be operator-supplied and was never found), `events-sync@1.2.0`, `quick-events@2.1.4`; `mathmain@1.0.0` remains the loaded build per this wiki's Sep 19 check. `modern-events` shows `0.0.1-security` = npm security placeholder (taken over).
- **No GHSA mirrors** for any of the campaign names at check (GitHub advisories API, direct package queries) — JFrog's XRAY IDs are the only advisory coverage, same posture as this week's Telegram-fleet story.
- Sepolia `WebDataRegistry` contract **live on-chain** (verified above); Slack/Telegram channels are JFrog's indicators, not probed by this wiki.
- `jsonspack.com` (homepage listed in this sweep's `hardhat-devkit` dropper, same cover-story style — see [ipcheck-hashed cluster page](../tools/ipcheck-hashed-vercel-app-require-time-server-code-cluster-september-2026.md)) does not resolve — unrelated infrastructure, checked for cross-links, none asserted.

## <a id="september-21-evening-follow-up-npm-took-the-trio-down"></a>September 21 (evening) follow-up: **npm took the trio down ~2.5 h after this post went live** — the farm and the rest of the campaign inventory did not move

At ~20:20 UTC this wiki re-checked the registry: `mathmain` (19:48 UTC), `mathsbase` (20:05), and `math-universe` (20:06) were each deleted and replaced by `0.0.1-security` security-holder packages (`repository: npm/security-holder`, publisher `npm@npmjs.com`, empty maintainer list), with OSV malware mirrors (`MAL-2026-16368/16369/16367`) landing within minutes of each removal. Full metadata forensics on the [mathmain trio page](mathmain-encrypted-loader-npm-trojanised-mathjs-trio-safedep-september-2026.md#september-21-evening-takedown-executed). Still untouched at check: **`events-sync` (the farm's 40.7 M-download target) latest `1.2.0` unchanged with zero GHSA**, the farm accounts (`andrewstory18`, `davidbabcock96`, `azlanrahman322-creator`) all still returning 200 on GitHub, and the other named campaign packages (`modern-events`, `quick-events`, `matrixflow-js`, the inflated PuPs) unremoved — the three removed names are exactly the trio JFrog's title names, which reads as publication-pressure response rather than campaign-level disruption. The Jun-8 Sepolia `WebDataRegistry` and the Slack channels were outside this check's scope and must be assumed live. Practical inversion for defenders: **the trio disappearing from npm is NOT an all-clear — it is the confirmed-indicator event that should trigger the LICENSE-marker grep + `subwatcher` path hunt on every host that ever installed a math-clone version in Mar 3–Sep 17.**

## Durable reads

1. **"Encrypted blobs in a package" findings are not dead ends — they are countdowns.** SafeDep's page (on-wiki) said "no plaintext, no demonstrated behavior, staging hypothesis." Three days later the whole campaign is open because the password space had structure. A GCM tag is an encryption oracle; treat "encrypted with a derived-from-input key" as "breakable by enumeration of plausible inputs."
2. **A messaging platform as both C2 and file transfer defeats download-based detection.** Nothing is fetched from a suspicious host; `slack.com` is the only hostname in the module. Egress allowlists that trust collaboration SaaS (the exact list every corporate proxy whitelists) carry the payload reassembly.
3. **Fake popularity is a supply-chain WEAPON, not vanity.** The farm runs BEFORE weaponisation ("operators publish clean and weaponise roughly a day later") — which inverts this wiki's standing heuristic: *inflated downloads + zero dependents* marks packages as **pending, not safe**. Treat clean-but-inflated as loaded-adjacent (JFrog's own instruction).
4. **Registry-side detection is cheap here:** reverse-dependency ratio (millions of downloads / zero dependents), npm-metrics spikes with no importers, and a `.js` file that reaches `crypto`/`child_process` from a pure-math package's solver path.
5. **GitHub's own CI is the botnet** (third-plus instance this year): attacker-owned repos + free Actions runners + push-triggered workflows = a distributed, reputable-IP request generator that no download counter should trust as popularity.

## Caveats

- JFrog recovered the trigger and the mechanisms, **not the task payloads**: all fifteen Slack task payloads are sealed under ephemeral X25519; the DeFi-targeting inference is lure- and trigger-based, not payload-confirmed. The `matrixflow-js@3.2.1` sealed payload and the pre-July inflation mechanism remain open.
- **No actor attribution** is offered by JFrog. The Contagious-Interview-adjacent lure style (interview campaign, fake hiring) is this wiki's pattern observation only — no shared infrastructure with DPRK clusters is claimed by JFrog or verified here.
- JFrog customers get Xray/Curation detection + a Catalog "Equation of Compromise" label; the article is vendor-published but every load-bearing claim (loader mechanics, trio linkage) was independently verified by this wiki against SafeDep's and our own tarball analysis before this page went up.

## Indicators (selected; full set in the JFrog post)

| Type | Value |
|---|---|
| Trigger matrix | `[[1,1,1],[1,2,3],[1,3,6]]` (symmetric Pascal 3×3); password = `JSON.stringify(math.lup(A).L._data)` |
| Sepolia contracts (live-verified: first) | `0xc0445F1b679DC46280A0f03F451bdf613b5A0feA` (WebDataRegistry, Jun 8), `0x9E4dF8F253Eb439dd9538Fda30cC03B38fD3a631` (Jun 15), `0xE390863Dac96a7118C71227C2b099B50cF602D31` (WalletHelloWorld, Jun 18), `0xac0bfC4C48A679b667732128278EACBA1c191894` (Base Sepolia, Aug 28), + 9 earlier WalletDataRegistry deploys Mar 5–18 (see post) |
| Slack | channels `C0ATC9UKKA4`, `C0B8GEPFMK9` (tasking), `C0B554AQF1S`, `C0B8XPGCKQS` (reporting); operators `U0B51HGMGJW`, `U0B91JWCVT6`; `xoxb-…` tokens redacted in post |
| Telegram | bot/chat strings in the JFrog IoC block (two bot tokens, chats `-1003968723972`, `-1003952553968`, `-1004489630130`; monitor tool alerts to `@server_alert_0630`) |
| Farm WASM | md5 `91e020c13cb97a6365135b53b0d0fe5f`; commit message `Update commands from job_master`; AES key `npm_workvr_protect_key_v1` |
| Accounts | `tinystar8`, `weed0`, `UmajiHidekata`, `andrewstory18`, `davidbabcock96`, `azlanrahman322-creator`, `Blustdp`, `mathubio`, `allendev12` (deleted); emails `tinystar368@gmail.com` / `@proton.me` |
| Files | `lib/cjs/utils/event.js` (loader), `graph.js`, `fraction.js`, `bignumber/type.js` (~1.5 MB bundled ethers), `lib/cjs/utils/subwatcher` (dropped payload, mode 755) |
| LICENSE marker | trailing line `REDISTRIBUTION REQUIRES INCLUSION OF THIS LICENSE.` = actively-infected host (survives repacking — grep this, not hashes) |
| Malicious versions | JFrog table: `modern-events` 1.3.3–1.5.2 (Mar 3, XRAY-968383), `graphcore-js`, `graphlib-js`, `quick-events` 2.1.3, `@ignacionunez91/keccak24`, `crypto-hasher`, `events-router`, `events-runtime`, `sort-btree`, `ordered-btree`, `indexed-btree` 2.1.2, `@andrewstory18/is-real-odd`, `@oliviamcdaniel12/safer-buffer` 2.2.x, `mutex-forge/-thread/-core/-plus/-lite`, `matrixflow-js` 3.2.1, `matrixkit-js`, `mathsbase` 1.0.1, `math-universe` 1.0.x, `mathmain` 1.0.0, `events-channel` 2.3.x + inflated PuPs `secure-library-loader`, `matrixhub` 6.15.x, `matrix-ops-core` |

## Related pages

- [mathmain / mathsbase / math-universe trio page](mathmain-encrypted-loader-npm-trojanised-mathjs-trio-safedep-september-2026.md) — the Sep 18 SafeDep artifact this campaign absorbs (updated with the password recovery)
- [ulid-xyz transitive delivery chain](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md) — the armed variant of payload/trigger separation
- [ChainScript RAT — Polygon-resolved WebSocket C2](../tools/chainscript-rat-polygon-websocket-c2-blackpoint-september-2026.md) and [GoCaracal](../tools/gocaracal-dark-caracal-ethereum-smart-contract-c2-fallback.md) — same on-chain tasking family
- [Telegram chat-1064260758 recon fleet](telegram-chatid-1064260758-dependency-confusion-recon-cluster-september-2026.md) — same-week story of npm advisory feed outrunning takedowns
- [Deployment poisoning of GitHub Actions](../patterns/deployment-poisoning-github-actions.md) — the platform's CI running as attacker infrastructure

## Sources

- JFrog Security Research, "Equation of Compromise: Anatomy of a Live npm Supply-Chain Campaign" (Sep 21, 2026): <https://research.jfrog.com/post/equation-of-compromise/> (fetched full text + IoC table by this wiki from the live post, Sep 21 ~17:30 UTC; RSS confirmed pubDate Mon 21 Sep 2026)
- SafeDep, "Why Does an npm Math Library Need an Encrypted Loader?" (Sep 18, 2026) — the origin artifact, on-wiki
- This wiki live checks (Sep 21 ~17:30–18:00 UTC): npm registry metadata for `mathsbase` / `math-universe` / `matrixflow-js` / `matrixhub` / `events-sync` / `quick-events` / `modern-events` / `mathmain`; `mathsbase@1.0.2` tarball pulled + inspected (loader absent in 1.0.2, obfuscated blobs present, LICENSE marker absent); `eth_getCode` for the Jun-8 Sepolia `WebDataRegistry` via publicnode (deployed, ~16 KB bytecode); GitHub advisories API per-package queries (no GHSA mirrors at check)
