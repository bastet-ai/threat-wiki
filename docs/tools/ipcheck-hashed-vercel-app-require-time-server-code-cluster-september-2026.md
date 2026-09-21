# The `ipcheck-hashed[.]vercel.app` require-time server-code cluster goes PUBLIC-CLOUD-permanent: `hardhat-base` (4th member, same server, new endpoint) and `hardhat-devkit` (5th, a 4 MB obfuscator.io dropper behind a pino cover story) cross the pattern-promotion bar this wiki set on Sep 21 — and this wiki verified the C2 endpoint is STILL ANSWERING 200 on a POST with no credentials, on free Vercel infrastructure anyone can provision

## Tags
- patterns
- supply chain attack
- npm
- server-side code execution
- new Function
- process.env theft
- vercel.app
- serverless C2
- amazon inspector
- OSV
- cover story packages
- obfuscator.io
- Hardhat ecosystem
- Ethereum developers
- pino cover
- dependency-confusion shaped

## Summary

On September 21 at ~16:41 UTC the Amazon Inspector → OSV pipeline admitted two more npm packages running the construction this wiki has been tracking all week: **full `process.env` POST to a base64-concealed `*.vercel.app` endpoint, response body piped into `new Function('require', …)` and invoked with the real `require`** = the server hands back arbitrary code executed with full module privileges on every import. `chai-as-indexed` and `chai-as-viem` established the shape (see [the algamil7x cluster page's third-sweep section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#september-21-third-sweep-survivors-still-live-chai-as-viem-ghsa-lands-and-chai-as-indexed-is-now-fully-gone), where this wiki set the promotion bar: *"if a fourth member or a second vercel.app server appears, this pattern promotes to its own page"*). **`hardhat-base` (OSV `MAL-2026-16348`) is member four** — and it shares the exact server `ipcheck-hashed[.]vercel.app`, under a different endpoint. This page is the promotion.

The cluster's durable shape, now with five members and two naming templates:

| Package | OSV / GHSA | Cover story | Endpoint | Status at Sep 21 check |
|---|---|---|---|---|
| `chai-as-indexed` | GHSA-727r-6hg5-947x | chai assertion plugin | `ipcheck-hashed[.]vercel.app/api/auth/…` | versions fully unpublished (name shell) |
| `chai-as-viem` | `MAL-2026-16329` / GHSA-c67f-wr24-prw9 (critical) | chai/viem/pino utility | `ipcheck-hashed[.]vercel.app/api/auth/6c1d60d35852ef0c05df` | 1.1.3 **still installable** (checked again this sweep, unchanged) |
| (same shape inside Sep 18–19 burst) | — | — | same server | — |
| **`hardhat-base`** 2.2.0/2.2.2 | `MAL-2026-16348` (IN-MAL-2026-020258/9) | pino-compatible logger (module.exports.pino = middleware; keywords fast/logger/stream/json), manifest description = vulnerability-management text | **same server**, endpoint `/api/auth/f1f097d93c318c92f0c5`, fetched from a **detached child process** (`lib/caller.js`) | **unpublished Sep 14 13:49 UTC per the registry time block** — both versions died the same day they appeared (~11 h and ~2 h live); OSV only published Sep 21 16:41 = **7-day detection latency** |
| **`hardhat-devkit`** 2.3.6 | `MAL-2026-16349` (IN-MAL-2026-020257) | Ethereum/Hardhat dev toolkit; README/`index.d.ts`/keywords **copied from pinojs/pino**; homepage `jsonspack.com`, author `hello@jsonspack.com` | none readable — `index.js` requires `lib/config.js`: a **single-line ~4,070,107-byte obfuscator.io blob** (RC4+base64 string decoder, control-flow flattening, debugger self-check) executing on any `require`/`import` | **unpublished Sep 17 22:36 UTC, ~47 minutes after creation** per the time block; `jsonspack.com` **does not resolve** at this wiki's check |

## What the two new members add to the pattern

1. **The child-process variant.** `hardhat-base` does not run the fetch in the importing process: `index.js` spawns `lib/caller.js` as a **detached child on middleware invocation**. The child decodes a fake `process.env`-shaped constant (`DEV_API_KEY`, base64) → the URL, POSTs via axios, and pipes the response into `new Function.constructor("require", s)`. Evasion value: the network call and the code exec are attributed to an orphan process your EDR parent-graph ties to nothing; the trigger is *calling* the exported middleware, not `require` — a package that "does nothing on install" is only inert until used.
2. **The full-dropper variant.** `hardhat-devkit` skips the readout construction entirely: `require('./lib/config')` detonates a 4 MB obfuscated blob at import time. Inspector's own line is the target-qualification read: the audience is **Ethereum developers, whose machines hold wallet keystores, mnemonics, and deployment keys** — same audience-profiling logic this sweep's JFrog [Equation of Compromise page](../ops/equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md) documents for the mathjs-cluster `lusolve` trigger, executed through naming instead of mathematics.
3. **The cover-story template is now explicit:** README/keyword/type-definition material **lifted verbatim from an unrelated legitimate project** (`pino`) while the `package.json` description says something else — a manifest-vs-content mismatch that is trivially checkable and currently checked by nobody. Inspector itself used that mismatch as evidence of intentionality ("cover-story pino API surface … confirm intentional supply-chain attack rather than an insecure update mechanism").
4. **Server-side persistence of the C2 is the point.** This wiki probed `POST ipcheck-hashed[.]vercel.app/api/auth/f1f097d93c318c92f0c5` at check time: **HTTP 200, live.** The endpoint answers a bare POST with no credentials. Deployment is a free-tier Vercel project — re-registration after any report is a re-deploy, not an infrastructure rebuild; domain-level blocklisting of `ipcheck-hashed.vercel.app` blocks one deployment of one function. (Root path 404s = only the function routes exist; consistent with a purpose-built serverless dropper.)
5. **Detection latency, again quantified via the time-block method** (on-wiki durable method): `hardhat-base` lived ~11 hours on Sep 14 and was advised Sep 21; `hardhat-devkit` lived **47 minutes** and was advised Sep 21. These packages were gone *before the advisories naming them existed* — an install-time scanner's clean verdict on Sep 15 tells you nothing about what ran on Sep 14. The registry `time` document remains the forensic record.

## Why "server-supplied code at require time" is the cluster's real artifact

The pattern is the require-time twin of WeaselBiscuit's Npoint dead-drop fetch (on-wiki) and the npm-era form of the same decision every implant maker since makes: **keep the payload off the registry so nothing scannable exists.** Its consequences, restated with five members of evidence:

- **Removal ≠ remediation.** Unpublishing the package does not disable the endpoint; a cached/host-vendored copy of the package re-fires at every import. Disposition for any host that installed a member: treat as **actively tasked**, hunt egress + child processes, rotate what the exported `process.env` could reach (which by construction includes every credential-shaped variable on the host — same exposure calculus as the on-wiki Telegram chat-ID fleet, but with the VALUES going out, as `chai-as-viem`'s GHSA text states: POSTs the full `process.env` with an `x-secret-header`).
- **The delivery rail is serverless SaaS the proxy already allowlists.** Corporate egress trusts `*.vercel.app` the way it trusts `slack.com` and `api.telegram.org` — all three are now documented npm-malware C2 rails this month.
- **The naming templates are the pivot, not the hashes:** `chai-as-*` (assertion-plugin squatting) and `hardhat-*` (Ethereum-tooling squatting), both aimed at crypto-adjacent developers. A third naming template, a second vercel.app server, or a member in a different ecosystem (PyPI/PyPI-shaped) means the template has escaped its author — watch accordingly.

## Hunt

- Egress (build + dev hosts) to `*.vercel.app/api/*` from `node`/package processes. No legitimate dependency phones a serverless function on require. **The endpoint path shape `/api/auth/<20-hex>` is the artifact** — two endpoints observed, same grammar.
- `new Function` + `atob`/base64-string decoders + `process.env` serialization inside third-party package code (static grep of node_modules is cheap: `new Function(` has almost no legitimate require-time uses in utility packages).
- Detached/orphan `node` children whose command line is a package `lib/` path (the `hardhat-base` variant's whole signature is the parent-graph gap).
- Lockfiles containing `hardhat-base`, `hardhat-devkit`, `chai-as-indexed`, `chai-as-viem`, or any `chai-as-*`/`hardhat-*` name whose publisher/version history doesn't match the genuine ecosystem (the real `chai-as-*` plugin ecosystem and the real Hardhat toolchain are both large — check publisher + time block, not the name prefix).
- `package.json` where keywords/README describe a well-known project (pino today, others tomorrow) but the description or homepage doesn't — manifest/cover mismatch.
- Triage discipline: for ANY member, pull the registry `time` block first (exposure window = created→unpublished, not created→advisory), then treat the host as tasked, not merely exposed.

## Caveats

- **No actor attribution exists.** The shared server stitches members 1–4 (the `hardhat-devkit` dropper has no readable endpoint); whether one author or one template copyset is unknowable from public data. The `jsonspack.com` homepage of `hardhat-devkit` resolving nowhere neither links nor unlinks it.
- `hardhat-base`'s OSV text is Amazon Inspector's analysis; this wiki verified registry state (both members unpublished with machine-readable `unpublished` blocks), the OSV records themselves, and endpoint liveness (HTTP 200), but did not re-analyze the tarballs — hashes/tarball SHAs are in the OSV records (`IN-MAL-2026-020257/8/9`).
- The endpoint answering 200 does not prove it still returns malicious code — an empty/auth-gated 200 is indistinguishable from outside; it does prove the operator's deployment **survived a week after the cluster's first advisories**.

## Sources

- OSV direct-ID records (this wiki, API-verified Sep 21 ~17:00 UTC): `MAL-2026-16348` (`hardhat-base` 2.2.0/2.2.2, Amazon Inspector, published 16:41:31Z, evidence-file SHAs + tarball hashes in-record), `MAL-2026-16349` (`hardhat-devkit` 2.3.6, published 16:41:23Z).
- npm registry `time` documents (this wiki, live): `hardhat-base` created 2026-09-14T02:55:03Z, unpublished 2026-09-14T13:49:47Z `[2.2.0, 2.2.2]`; `hardhat-devkit` created 2026-09-17T21:49:14Z, unpublished 2026-09-17T22:36:23Z `[2.3.6]`.
- Endpoint liveness probe (this wiki, Sep 21 ~17:15 UTC): `POST https://ipcheck-hashed[.]vercel.app/api/auth/f1f097d93c318c92f0c5` → HTTP 200; root 404. `jsonspack.com` → NXDOMAIN.
- Prior-cluster context on-wiki: [algamil7x page third-sweep section](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) (`chai-as-indexed`/`chai-as-viem`, GHSA-c67f-wr24-prw9 critical, promotion bar); [WeaselBiscuit](../tools/weaselbiscuit-npm-stealer-beavertail-ottercookie-dprk-opensourcemalware-september-2026.md) (fetch→`new Function` twin).

## Related pages

- [Equation of Compromise campaign page](../ops/equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md) — same-day discovery: the mathjs-cluster proves the audience-profiling half of this cluster's shape
- [algamil7x npm DNS-exfil recon cluster](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — week's other install-script family
- [Telegram chat-1064260758 dependency-confusion recon fleet](../ops/telegram-chatid-1064260758-dependency-confusion-recon-cluster-september-2026.md) — same-batch Inspector output, third rail (Telegram) of the same month
- [WeaselBiscuit npm stealer](../tools/weaselbiscuit-npm-stealer-beavertail-ottercookie-dprk-opensourcemalware-september-2026.md) — dead-drop fetch pattern ancestor
