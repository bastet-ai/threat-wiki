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

Version-flip-flopping matters operationally: **npm currently serves `mathmain@1.0.0` (clean) as `latest`; the loader lives in `1.0.1`** — checking only the default release would miss it. `mathsbase` alternates clean/malicious by version too (registry check, Sep 19: `mathmain` latest = 1.0.0, `mathsbase` latest = 1.0.2, `math-universe` latest = 1.0.2).

## The public-source gap

The GitHub repos named by `mathsbase` (`tinystar8/mathsbase`, reviewed at commit `560d97e6…`) and `math-universe` (`mathubio/math-universe`, commit `da99dd46…`) **do not contain the loader** — the added `removeSolveValidation()` call exists in the npm builds only. Same publishing-vs-source divergence pattern as prior supply-chain cases: the registry artifact is not built from what you can read. SafeDep searched GitHub for importers/lockfile references/solver callers hoping to find the password-holder and found none (private consumers remain invisible).

## Staging hypothesis (SafeDep's own framing)

Working theory: the packages are **payload storage for a later attack** — a separate package would add one of these as a dependency and pass the correct matrix as the trigger; the trigger lives in the depending package while the encrypted payload lives in the dependency. SafeDep draws the contrast with its `ulid-xyz` investigation, where the loading package was identified: **here that half of the chain is missing**. The loader is judged suspicious because it sits inside a solver and is absent from the public source; the encrypted contents remain unproven either way.

## Defender translation

- **Detection does not require the plaintext.** Hunt for the loader files themselves: SHA-256 of `lib/cjs/utils/event.js` (`ab66c98e…`) and `lib/cjs/utils/is.js` (`5d9e952c…`) match across all five versions; grep dependencies for long base64 strings where a `.js` file should hold code, `scryptSync` + `createDecipheriv('aes-256-gcm'` in non-crypto libraries, and a `require()` of a path assembled from decrypted data.
- **The encrypted-blob-in-dependency shape is now a documented staging pattern** with two SafeDep cases in seven weeks: `ulid-xyz` (armed, trigger found) and this trio (armed, trigger not yet seen). Treat "package contains megabytes of base64 with no reader in the visible code" as its own query.
- **Version-checking hygiene:** clean `latest` + dirty non-default versions defeats trivial scanning; audit **lockfiles**, not "the latest version," and diff installed trees against public repo contents where both exist.
- **Registry/coordination asks:** these three packages remain **live on npm as of Sep 19** (versions listed above; no GHSA published for any of them as of this scan). Report/takedown pressure and a consumer-side lockfile sweep are the actionable moves until the password or plaintext surfaces.

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
