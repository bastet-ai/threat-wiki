# Product-instructed commands over unclaimed package names: `npx ubiquiti-agents-link-mcp@latest`

**Category:** patterns
**First seen:** 2026-09-22
**Last verified:** 2026-09-22 ~23:15 UTC (this wiki — registry pulls, tarball analysis, live C2 probe; re-pull at ~22:30 UTC caught a fourth version)

## Summary

On September 22, 2026 at 19:36 UTC, the npm name **`ubiquiti-agents-link-mcp`** was registered by publisher `deadinfluence` (`npm@graphics4us.com`) and within minutes began shipping a package whose stated purpose is to prove a supply-chain gap: the package description claims that **Ubiquiti's UniFi Site Manager UI and its agents relay instruct operators to run `npx ubiquiti-agents-link-mcp@latest`** while the npm name sat unclaimed. Whoever registers a name that a product's own UI tells operators to execute obtains arbitrary code execution, at the operator's own privileges, on every machine whose operator follows the instruction. The registered package is self-labeled a **security research placeholder**: it runs `id`, reads username + hostname, and POSTs them to a researcher-controlled Burp Collaborator host. OpenSSF Package Analysis flagged it malicious as `MAL-2026-16409` **fourteen minutes after first publication** (published 19:36:12 UTC, OSV record 19:50:54 UTC).

Independent corroboration of the Ubiquiti claim was **not retrievable by this wiki at capture time** — no public Ubiquiti statement, no screenshot source, no secondary report. Treat "the UI says to run this" as the publisher's assertion. The durable pattern does not depend on it: **if any product's documentation, UI, error message, or support relay ever tells a human to run `npx <name>` for a package the vendor does not publish, the name is an unclaimed execution primitive, and the first registrant — researcher, criminal, or squatter — gets code execution on the operator fleet.**

## What this wiki verified directly (Sep 22 ~20:30–21:00 UTC)

- **Registry document**: created 2026-09-22T19:36:11Z; versions `0.0.1` (19:36:12), `0.0.2` (19:43:31), `0.2.0` (20:34:05); `dist-tags.latest = 0.2.0`; maintainer `deadinfluence <npm@graphics4us.com>`. npm downloads API returns "package not found" for the name (too new to index) — no install telemetry is publicly readable yet.
- **Tarballs pulled and read** (`0.0.2`, `0.2.0`): no install hooks, no postinstall — execution requires the operator to actually run the `bin` entry (`npx` fetches and executes on demand). `index.js` runs `execSync("id")`, collects `os.userInfo().username` + `os.hostname()`; `0.2.0` additionally adds `ls -la` of the cwd and `process.cwd()`. Everything is POSTed once to `uhffaanwxy0io5bfc0icu5lpug07o9cy[.]oastify.com/<random-int>`. No persistence, no file reads beyond directory listing, no second stage — consistent with the self-declared demonstration purpose. The `0.0.1` tarball anomalously contains a nested copy of itself (`package/ubiquiti-agents-link-mcp-0.0.1.tgz` inside `package/`), an artifact of how the publisher packed it.
- **C2 liveness**: the Collaborator host answers HTTP 200 at root at check — the collector is deployed and POST-ready (the same class of finding this wiki logged for `radio-player-theme`, `pwaplatform`, and the `algamil7x` collectors: `*.oastify.com` from endpoints/build hosts is a standing hunt signal regardless of which campaign lit it).
- **Advisory state**: `MAL-2026-16409` (OpenSSF Package Analysis; reason: "communicates with a domain associated with malicious activity" — i.e., the automation judged by the Collaborator endpoint, not by intent). `0.0.2` was imported into the OSV record at 20:40 UTC, ~57 minutes after publication. **Zero GHSA at check.** The name is live and `0.2.0` installable at check time.

## Why the automation's "malicious" verdict is not the end of the story

The OpenSSF flag is mechanically correct — exfiltrating identity data to an attacker-class endpoint is what malware does — but the artifact read in full is a demonstration with a stated handoff path ("Contact the maintainer to have this name transferred to Ubiquiti"). This creates a genuinely unresolved triage class that every consumer needs a policy for:

1. **Self-declared research is untrusted metadata.** This wiki's standing rule (from the `algamil7x` cluster, `@pwaplatform`, and `radio-player-theme`): a publisher's benign framing — bug bounty, canary, PoC, placeholder — is never exculpation; the binary's behavior is the record. Here the behavior is mild but real: every operator who ran the command leaked `id` + username + hostname (and, post-`0.2.0`, a directory listing and cwd) to a server the publisher controls.
2. **The placeholder is itself now a supply-chain object.** The name holds its payload under one npm account. If that account is phished, abandoned, or transferred sloppily, the "proof" becomes the incident. Version `0.0.1 → 0.0.2 → 0.2.0` in one hour (adding exfil breadth each step) shows the mutable `latest` tag doing exactly what mutable `latest` does — **and the ladder continued after first publication of this page: `0.2.1` landed 22:25:18 UTC, ~2 h 50 m after `0.2.0`, ADDING `cat .env`, `cat package.json`, and `ls /` to the POSTed payload** (tarball read by this wiki). Five hours after registration the "demo" is exfiltrating environment files and project manifests — the exact dataset a real theft operation steals first. Each `@latest` run by an obedient operator since 19:36 UTC POSTs whatever the CURRENT version collects; the version ladder means consent granted against `0.0.1`'s behavior is being charged against `0.2.1`'s.
3. **The finding is only real if the vendor confirms the instruction.** If Ubiquiti's UI really emits that command, the durable fix is Ubiquiti publishing the name (or changing the instruction). If no UI ever said it, the registrant manufactured the pretext — and the OSV flag is the whole story. The monitoring item is therefore **Ubiquiti's disposition**: confirmation + transfer, or silence.

## The durable pattern, independent of this case

**Vendor-instructed execution of an unclaimed name is a designed-in squatting surface.** It sits beside — not inside — phantom squatting (LLM-hallucinated domains/names): here no model hallucinates anything; the trusted product itself is the recommender, which makes the path *stronger* than the LLM variant because the instruction arrives in the product's own UI, not a probabilistic assistant reply. Failure ingredients:

- `npx <name>` = fetch-and-execute with no install-time review step, no lockfile, no provenance prompt in default configurations.
- `@latest` = attacker-controlled version channel, re-armable at any time after the first run.
- Unclaimed registry name = zero-cost registration of a command that already has a distribution channel (the vendor's own docs/UI/support).
- Operator trust = the instruction carries the product's authority; no user will question a command their admin console printed.

**Detection/defense actions:**
- **Audit your own products** (this is a vendor-side checklist): grep documentation, UI strings, error messages, support macros, and agent-relay content for `npx`, `pip install`, `go install`, `cargo install`, `npm i -g` referencing package names — then verify the vendor owns those names on every registry they hit. Unclaimed = either publish them or change the instruction (scoped, vendor-published packages, pinned versions).
- **Audit your operators**: egress/EDR hunts for `npx` invocations whose package name is not in an allowlist, especially names first published within the last N days (`npm view <name> time.created`).
- **Monitor the squatting window**: for any product-instructed command, name-registration monitoring (registry `created` timestamps) is the only early-warning; the registrant needs the name for minutes, not months.
- Treat `*.oastify.com` / `*.burpcollaborator.net` / `webhook.site` POSTs from operator and build hosts as a standing hunt signal (fifth on-wiki sighting across four unrelated clusters this month).

## State at this wiki's check (Sep 22 ~21:00 UTC)

- Name LIVE, `latest = 0.2.0` installable; no GHSA; OSV `MAL-2026-16409` covers `0.0.1` + `0.0.2` (any new version will need re-flagging — watch for `0.2.x`/`0.3.x` imports).
- Collaborator collector live (HTTP 200 root).
- No Ubiquiti statement, no security-researcher writeup, no attribution of `deadinfluence`/`graphics4us.com` to a known researcher at capture.

## Monitoring

1. **Ubiquiti disposition**: confirmation that any UniFi Site Manager surface printed the command; transfer of the npm name; a CVE/GHSA on the vendor's side; or silence (which is itself the answer about the claim).
2. **The npm account**: account takeover or handoff of `deadinfluence` turns the placeholder into an active stealer for anyone who `npx`-runs the name — same dead-switch shape as the unpinned `github:tenka-san/libsignal-node` findings this week, one npm account instead of one GitHub account.
3. **Copycats**: researchers squatting vendor-instructed commands to prove findings is a cheap, high-signal stunt — expect repetition against other appliances/agents (any vendor whose support docs say "run this command" without owning the name).
4. **OSV/GHSA drift**: whether GitHub's malware bot ever mirrors this name and how long the OSV-only window persists for self-labeled research artifacts.

## Tags
- patterns
- supply-chain
- npm
- npx
- package name squatting
- vendor instructions
- UniFi
- Ubiquiti
- Burp Collaborator
- oastify
- security research placeholders
- untrusted metadata
- OpenSSF Package Analysis

## Related pages
- [Phantom squatting: AI-hallucinated domains](phantom-squatting-ai-hallucinated-domains.md) — the LLM-mediated sibling of the same squatting primitive
- [npm install explicit-trust controls](npm-install-explicit-trust-controls.md) — npx fetch-and-execute is the path npm v12's script approvals do not gate
- [algamil7x npm DNS-exfil cluster](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — the self-declared-benign-label cluster tell this rule came from
- [PhantomRaven page](../tools/phantomraven-llm-generated-npm-infostealer-bug-bounty-hunter-crowdstrike-september-2026.md) — the `radio-player-theme` jsDelivr-routed "bug-bounty PoC" case, same costume

## Sources

- npm registry document + tarballs for `ubiquiti-agents-link-mcp` (this wiki, direct pulls Sep 22 ~20:30 UTC): <https://registry.npmjs.org/ubiquiti-agents-link-mcp>
- OSV record `MAL-2026-16409` (OpenSSF Package Analysis, published 2026-09-22T19:50:54Z): <https://osv.dev/vulnerability/MAL-2026-16409>
- npm.io listing (index entry, no report computed at check): <https://npm.io/package/ubiquiti-agents-link-mcp>
- Publisher claim source: the package description and `index.js` comments themselves (captured verbatim in this wiki's tarball pulls); no independent public source for the UniFi UI instruction at capture time.
