# mathmain / mathsbase / math-universe: trojanised mathjs clones hide a scrypt+AES-GCM encrypted-payload loader keyed on solver input — the payload itself is still unread (SafeDep, Sep 18, 2026)

## Tags
- ops
- supply chain attack
- npm
- typosquat
- mathjs
- encrypted loader
- scrypt
- AES-256-GCM
- dormant payload
- staged payload
- trigger separation
- trojanised clone
- SafeDep
- undecrypted payload
- supply-chain staging

## Summary

SafeDep published a malicious-package analysis on **September 18, 2026** ("Why Does an npm Math Library Need an Encrypted Loader?") documenting a **loader for encrypted code inside `mathmain@1.0.1`** — an npm package that is a **renamed, obfuscated copy of mathjs** — with **identical loader files found in two sibling packages, `mathsbase` and `math-universe`, across five versions in total**. The durable finding is the design, not a demonstrated crime: the loader **derives its decryption password from data passed to the package's own linear solver**, so the payload can sit dormant inside a dependency until some *other* package supplies the matching input. SafeDep could **not recover the password and cannot read what the encrypted code does** — it publishes the loader mechanics, hashes, and a staging hypothesis, and explicitly says it has **not shown the code steals credentials, contacts a server, or persists**. This is a **staging primitive** finding, in the same design family as SafeDep's own `ulid-xyz` transitive-delivery chain, except the trigger half of the chain is missing from public view.

## The loader mechanics

- **Where it hides:** at the end of `lusolve()` in the CommonJS build (`lib/cjs/function/algebra/solver/lusolve.js`) an extra call `removeSolveValidation(l._data)` runs **after the solver has already computed its result**, passing the **lower-triangular matrix data**; the return value is assigned but never used — pure camouflage.
- **The decryptor:** the call routes to an added `isGraph()` in `lib/cjs/utils/is.js` beside genuine `isMatrix`/`isNumber` checks. It serializes its input (`JSON.stringify(x)`) and uses **that string as the password**: it decrypts an 8-byte ciphertext that yields a **filename** (suspected `graph.js`, also 8 chars — unconfirmed), then a helper decrypts that file, **writes the plaintext to disk** (stripping an `enc_` prefix), and `require()`s it — running with the Node process's permissions.
- **Crypto:** `scryptSync(password, salt, 32)` → **AES-256-GCM**; fixed blob layout = 16-byte salt + 12-byte IV + 16-byte auth tag + ciphertext, stored as base64 (`lib/cjs/utils/event.js`).
- **Password = caller's matrix data:** for solver calls the password is `JSON.stringify(L._data)`; a caller supplies `L` through the object form of `lusolve()`. **No password is embedded in the visible loader** — the trigger must come from a caller that knows the input.
- **Dormancy properties:** no install hooks in the manifest; plain import does not reach the code (the solver must pass validation first); a wrong password fails the GCM auth check **before anything is written to disk**.
- **Encrypted files in the package:** `lib/cjs/utils/graph.js` (20,918 B ciphertext), `fraction.js` (9,084 B), `bignumber/type.js` (**1,179,416 B**) — the last two are **not referenced by the visible loader at all**; what loads them is unknown.

## Publication timeline (UTC, from npm registry metadata)

| Date | Event |
|---|---|
| Aug 26, 08:14 | `mathmain@1.0.0` published — **no loader** |
| Aug 27, 07:44 | `mathmain@1.0.1` published **with loader + encrypted files** |
| Sep 15, 03:38 | `mathsbase@1.0.2` published **without** the matching loader |
| Sep 16, 12:06–14:14 | `math-universe@1.0.0/1.0.1/1.0.2` published **with** the loader |
| Sep 17, 06:53 | `mathmain@1.0.2` published **with** matching files |
| Sep 17 | SafeDep source review + 17,000+ password attempts; no plaintext recovered |

Version-flip-flopping matters operationally: **npm currently serves `mathmain@1.0.0` (clean) as `latest`; the loader lives in `1.0.1`** — checking only the default release would miss it. `mathsbase` alternates clean/malicious by version too (registry check, Sep 19 morning: `mathmain` latest = 1.0.0, `mathsbase` latest = 1.0.2, `math-universe` latest = 1.0.2). **Superseded by the evening Sep 19 check below — the surviving `mathmain` `1.0.0` is now the loaded build.**

## The public-source gap

The GitHub repos named by `mathsbase` (`tinystar8/mathsbase`, reviewed at commit `560d97e6…`) and `math-universe` (`mathubio/math-universe`, commit `da99dd46…`) **do not contain the loader** — the added `removeSolveValidation()` call exists in the npm builds only. Same publishing-vs-source divergence pattern as prior supply-chain cases: the registry artifact is not built from what you can read. SafeDep searched GitHub for importers/lockfile references/solver callers hoping to find the password-holder and found none (private consumers remain invisible).

## Staging hypothesis (SafeDep's own framing)

Working theory: the packages are **payload storage for a later attack** — a separate package would add one of these as a dependency and pass the correct matrix as the trigger; the trigger lives in the depending package while the encrypted payload lives in the dependency. SafeDep draws the contrast with its `ulid-xyz` investigation, where the loading package was identified: **here that half of the chain is missing**. The loader is judged suspicious because it sits inside a solver and is absent from the public source; the encrypted contents remain unproven either way.

## Defender translation

- **Detection does not require the plaintext.** Hunt for the loader files themselves: SHA-256 of `lib/cjs/utils/event.js` (`ab66c98e…`) and `lib/cjs/utils/is.js` (`5d9e952c…`) match across all five versions; grep dependencies for long base64 strings where a `.js` file should hold code, `scryptSync` + `createDecipheriv('aes-256-gcm'` in non-crypto libraries, and a `require()` of a path assembled from decrypted data.
- **The encrypted-blob-in-dependency shape is now a documented staging pattern** with two SafeDep cases in seven weeks: `ulid-xyz` (armed, trigger found) and this trio (armed, trigger not yet seen). Treat "package contains megabytes of base64 with no reader in the visible code" as its own query.
- **Version-checking hygiene:** clean `latest` + dirty non-default versions defeats trivial scanning; audit **lockfiles**, not "the latest version," and diff installed trees against public repo contents where both exist.
- **Registry/coordination asks:** these three packages remain **live on npm as of Sep 19** (versions listed above; no GHSA published for any of them as of this scan). Report/takedown pressure and a consumer-side lockfile sweep are the actionable moves until the password or plaintext surfaces.

## September 19 (evening) registry re-verification: the "clean latest" has FLIPPED — `mathmain` latest is now the loaded build

Live registry check (this wiki, Sep 19 ~13:45 UTC) materially changes the flip-flop story:

- **`mathmain` was unpublished and RECREATED.** The package name's `created` timestamp is now **2026-09-17T06:53:06Z** — the same minute as the Sep 17 republish in the timeline above — and the ONLY surviving version is **`1.0.0`, marked `latest`, and it CONTAINS the loader**: `lib/cjs/utils/event.js` with the campaign hash `ab66c98e…` (scryptSync present), the obfuscated `lusolve.js` carrying the `removeSolveValidation` call, and the 1,572,616-byte `bignumber/type.js` blob. The earlier note on this page ("npm currently serves the CLEAN `mathmain@1.0.0` as latest") reflected the ORIGINAL Aug-26 `1.0.0`; after the delete-and-recreate, **any fresh `npm i mathmain` today pulls the loaded build**. The clean/dirty flip-flop has resolved in the hostile direction: **latest = loaded**.
- **All three `math-universe` versions (1.0.0/1.0.1/1.0.2) carry the loader** (event.js with scryptSync in each; the 1.57 MB blob present in `1.0.2`).
- `mathsbase`: `1.0.1` carries the loader (tarball SHA-256 `03e13cdedd9c33e6…` — **matches SafeDep's indicator exactly**; live-verified). `1.0.0` and `1.0.2` lack `event.js`/the scryptSync loader, though `1.0.2` ships a differently-hashed `graph.js` (`dcebfdf7…`, 7,315 B) in the same slot.
- **Registry tarball hashes independently verified against SafeDep's published set** for `mathsbase@1.0.1`, `math-universe@1.0.1` (`bfe772e7…`), and `math-universe@1.0.2` (`4eb1d59d…`) — the on-wiki indicator set is confirmed live, not just reported.
- **Still no GHSA and no takedown for any of the three** (GHSA API sweep of npm advisories published since Sep 18, Sep 19 ~13:50 UTC). The delete-and-recreate at Sep 17 06:53 UTC reset the version history — **prior-version scanning tools that cached the Aug/Sep version list now hold phantom versions while the loaded build sits under a familiar-looking `1.0.0`**.
- Defender translation update: the "audit lockfiles, not latest" guidance STILL applies, but as of this check **`latest` itself is dirty for `mathmain`** — both checks are now mandatory. The unpublish-and-republish-with-the-same-loaded-code pattern is worth logging as a takedown-evasion behavior for the ongoing watch.

## September 21 follow-up: JFrog's "Equation of Compromise" absorbs this trio — the password was RECOVERED, and it was a matrix this wiki could have guessed

JFrog Security Research (Sep 21, 2026, "Equation of Compromise: Anatomy of a Live npm Supply-Chain Campaign") published the campaign view of exactly these packages, and **broke the encryption this page called unreadable**: AES-GCM's auth tag is an oracle at ~50 ms per guess with no false positives, so the password space collapsed once JFrog enumerated *structured* matrices instead of SafeDep's 17k blind candidates. **The trigger is `math.lusolve()` on the 3×3 symmetric Pascal matrix `[[1,1,1],[1,2,3],[1,3,6]]`** — its LU factor's `L._data` stringified is the scrypt password. Full teardown, recovered IoCs (13 Sepolia/Base-Sepolia tasking contracts — the Jun 8 `WebDataRegistry` `0xc0445F1b…` verified **still deployed on-chain by this wiki** Sep 21), the dual-bot Slack tasking channel that ships payloads as chunked chat messages, and the GitHub Actions download farm (up to 40.7M fake downloads for one package; still running at publication) live on the dedicated page: **[Equation of Compromise campaign page](equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md)**.

State corrections from this sweep's checks (~17:30 UTC): the trio is **still live and still has no GHSA**; `mathsbase` latest is `1.0.2` — tarball pulled by this wiki: **loader `event.js` absent in 1.0.2** (the loaded version is `1.0.1` per JFrog) but the obfuscated blob slots are present (`graph.js` `dcebfdf7…` — the differently-hashed file this page already recorded), LICENSE infection-marker string absent; `math-universe@1.0.2` live; `mathmain@1.0.0` remains the loaded latest. JFrog's campaign window: **Mar 3 – Sep 17, 2026, 25+ malicious versions across math/BTree/mutex/event/graph-themed clones** — the trio was the tip, and every "clean artifact, no demonstrated behavior" caveat on this page is now superseded by decrypted mechanics + enrollment/tasking infrastructure. The staging hypothesis is CONFIRMED in shape (payload in dependency, trigger in caller) but inverted in operator model: the caller trigger is a lure JFrog assesses as a possible interview-campaign task handed to the victim, not a future depending package.

## <a id="september-21-evening-takedown-executed"></a>September 21 (evening) registry re-check: **THE TRIO IS DOWN** — npm replaced all three names with `0.0.1-security` holding packages within ~2.5 h of the JFrog publication

At ~20:20 UTC this wiki re-pulled all three registry documents and the campaign's npm surface is gone:

- **`mathmain`**: `created` now 2026-09-21T19:48:19Z, sole version `0.0.1-security` (`repository: npm/security-holder`, publisher `npm@npmjs.com`), 422 bytes, `latest` = the security holder. The Sep-17-recreated loaded `1.0.0` is gone (its timestamp survives in the `time` block, per the standing time-block-forensics method).
- **`mathsbase`**: `created` 2026-09-21T20:05:34Z — time block still lists `1.0.0` (Aug 26), `1.0.1` (Aug 27, the loaded version), `1.0.2` (Sep 15) — all removed, replaced by the holder.
- **`math-universe`**: `created` 2026-09-21T20:06:04Z — all three Sep-16 versions removed, holder installed.

OSV mirrors landed minutes after each removal (`MAL-2026-16367` math-universe 20:06:33Z, `MAL-2026-16368` mathmain 19:49:06Z, `MAL-2026-16369` mathsbase 20:06:13Z) — the removal→mirror sequence confirms coordinated registry action, not operator self-unpublish (an operator does not install `npm/security-holder` packages under their own name). **Zero GHSA still** — npm went straight from no-advisory to takedown.

**Durable reads:** (1) this is what an npm takedown LOOKS like in the metadata: name recreated with a fresh `created` timestamp, one `0.0.1-security` version, `maintainers: []`, `repository: npm/security-holder` — distinguish from operator delete-and-recreate (which this page's Sep 19 section documents for `mathmain` itself: same shape, but the operator RE-ARMED where npm NEUTRALIZES — always check the publisher identity and version content, not just the reset); (2) takedown speed tracked publication pressure: ~72 h of live-while-advised status ended ~2.5 h after the JFrog post, echoing the advisory-feed-vs-takedown-pace story on the Telegram cluster page; (3) **removal ≠ remediation** still applies — the six-month campaign's other named packages (`modern-events`, `quick-events`, `matrixflow-js`, the inflated PuPs `secure-library-loader`/`matrixhub`/`matrix-ops-core`, and the download farm's `events-sync`) were NOT touched at check (`events-sync` latest `1.2.0`, unchanged; three farm GitHub accounts still 200), and every host that installed a dirty version between Mar 3 and Sep 17 is still tasked via the live Sepolia contracts + Slack agent until found. The LICENSE-marker grep (`REDISTRIBUTION REQUIRES INCLUSION OF THIS LICENSE.`) is now the primary hunt, since the packages themselves no longer appear in registry queries.

> **Sep 22 twelfth-sweep correction (this wiki, registry time-block pull):** one name in the "NOT touched" list above was wrong — **`modern-events` has been an `0.0.1-security` holder since Apr 24, 2026** (created timestamp = holder creation, no surviving versions), months before JFrog's writeup; either the operator never got a live version under that name or npm held it early. The rest of the list re-verified unchanged Sep 22 ~05:30 UTC: `quick-events` 2.1.4, `matrixflow-js` 3.2.2, `events-sync` 1.2.0, `secure-library-loader` 0.1.0–0.1.3, `matrixhub` 6.15.0/6.15.1, `matrix-ops-core` 1.0.0–1.1.0 — **all still LIVE with live versions.**

> **Sep 22 seventeenth-sweep correction (this wiki, direct GHSA fetch):** the "Zero GHSA still" line above was wrong — GHSA mirrors DID exist, published **within two minutes of each holder creation**: `GHSA-v6mx-2p6p-3628` (`mathmain`, 19:49 UTC vs holder 19:48:19), `GHSA-v4cx-64j6-84xm` (`mathsbase`, 20:06 vs 20:05:33), `GHSA-97cg-r346-fg22` (`math-universe`, 20:06 vs 20:06:03). The check-time sweep read used the advisories LIST endpoint, the standing unreliable path (see source-index API-quirk notes); direct GHSA fetch confirms them. The takedown + mirror coordination finding on this wiki's algamil7x page (tenth sweep) extends to this trio: **all three positive artifacts (security holder, GHSA, OSV) arrived inside a two-minute window per name.** Also re-verified Sep 22 ~15:30 UTC: all three holders still `0.0.1-security`, no resquat; `mathsbase` old tarballs no longer downloadable (1.0.1 → 404), so the LICENSE-marker host grep is the only victim-side check left.

## Caveats

- **No demonstrated malicious behavior.** No C2 endpoint found in readable code; no credential theft, network contact, or persistence shown. SafeDep: "We need a caller with the right input, or the decrypted code, to settle what it does."
- Who added the loader (author vs. compromised publisher) is **unknown**; no attribution is offered.
- The 8-byte filename decrypting to `graph.js` is a suspicion, not a confirmed fact.
- Password-search negative results (16,922 + 533 candidates) show SafeDep's tooling works on test vectors but do not prove the password is unrecoverable by others.

## Indicators

Archive SHA-256 (from the SafeDep post):

| Package / version | Tarball SHA-256 |
|---|---|
| mathmain@1.0.1 | 1723a0df210ac61281a504f3a07ec3605d20151631e0635cc344cacc71019135 |
| mathsbase (loader versions) | 03e13cdedd9c33e6fed25092b1ec7dcf11cc5962c0fbb6b3e90ba95bfec1b034 |
| (third loader version) | 7e5e1bcdc6a7b0e3437269a236b49ef2be4f77081c7de5130d503c103fd6be69 |
| (fourth loader version) | bfe772e7ee044fd6f0bdf53e83f44aad7c9ee1925baf0cf4d884a312aa9ba50e |
| (fifth loader version) | 4eb1d59df7dc80dbe3ec154481e61e8824422037092c188f0cc146b543615a66 |

Shared file hashes across all five versions: `lib/cjs/utils/event.js` = `ab66c98e8ed5235feb963ec8845765f62f5f26b1c58c266c409767e53bcb5ccd`; `lib/cjs/utils/is.js` = `5d9e952c51875d2b897eedc22b002b94ab21c8004d513bc99ce3a885f8a01dae`. Repos: `github[.]com/tinystar8/mathsbase`, `github[.]com/mathubio/math-universe`.

## Related pages

- [ulid-xyz transitive delivery chain — the armed version of the same design (SafeDep, Sep 1)](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md)
- [Deep-Live-Cam supply-chain compromise — hidden loader behind whitespace in a git+https setup.py (SafeDep, Sep 9)](deep-live-cam-python-dependency-supply-chain-clipboard-hijacker-safedep-september-2026.md)
- [SafeDep Baileys / libsignal-node npm WhatsApp campaign](baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md)
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)

## Watch items

1. Whether any npm/GHSA action lands on `mathmain` / `mathsbase` / `math-universe` (none as of Sep 19) and whether the packages are removed.
2. Appearance of the **trigger package** — the missing half of SafeDep's staging hypothesis (a dependency-declaring package that calls the solver with the password-shaped matrix).
3. Password/plaintext recovery by any researcher (turns "suspicious staging" into characterized malware), and whether the ~1.18 MB `bignumber/type.js` blob is ever read.
4. Whether the clean/malicious version flip-flop recurs or the operator republishes under new math-themed names.

## Sources

- SafeDep, "Why Does an npm Math Library Need an Encrypted Loader?" (Sep 18, 2026): <https://safedep.io/mathmain-encrypted-loader>
- npm registry metadata for `mathmain`, `mathsbase`, `math-universe` (verified live Sep 19, 2026 — packages still present, dist-tags as listed above)
- SafeDep, ulid-xyz transitive dependency delivery chain (Sep 1, 2026): <https://safedep.io/ulid-xyz-transitive-dependency-delivery-chain>
