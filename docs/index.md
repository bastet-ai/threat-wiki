---
title: threat.wiki
---

# threat.wiki

Threat intelligence notes, group profiles, named-person records, and defensive guidance.

## Popular this week
<!-- popular-this-week:auto -->
_Auto-maintained from Cloudflare zone analytics, last 7 days ending 2026-11-06 UTC (22353 of ~744 on-page requests attributable; 94 of 744 path batches ok)._
- [Source index](/notes/source-index/) — 172 reads
- [SilkParasite](/actors/silkparasite/) — 122 reads
- [Djinn Stealer](/tools/djinn-stealer/) — 120 reads
- [Tag index](/notes/tag-index/) — 118 reads
- [Kimsuky / Emerald Sleet / TA427](/actors/kimsuky-emerald-sleet-ta427/) — 116 reads
- [JiaT75](/people/jiat75/) — 112 reads
- [Cavern](/tools/cavern/) — 111 reads
- [PamStealer](/tools/pamstealer/) — 110 reads
<!-- /popular-this-week:auto -->

## Recent entries
- [**The pirated-ebook npm name factory dropped its own signature mid-burst: of 380 malicious packages minted in one three-hour window, eleven carried the same `<title>_by_<author>_<5 chars>` template with NO misspelled `dowload_ebok_` prefix at all — a hunt keyed on the prefix would have missed them, so cluster malicious generated names on the name GRAMMAR and treat every prefix as costume**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-second-sweep)
- [**Three malicious pip packages were quarantined inside one hour of appearing, and the campaign's payload repo — opened on schedule — hosts nothing but `echo Hello!`: `testing1345` escalated from quarantine to whole-name removal, `qap793gl4l` held quarantine, and the third name `axiom-dragon-xyz` (wallet-file and cloud-credential stealer with a Discord-webhook exfil IOC) was quarantined before most defenders saw its advisory: the pull clock now beats the arming clock by hours**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-second-sweep)
- [**The CDN that called a package version dead changed its mind: jsDelivr answered 404 on the one `0sec-cli` version the registry still ships, then served it again one read later — a single edge-cache read, alive OR dead, is not a lane state, and any pinning or blocking decision built on one probe of one CDN is built on noise**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-272th-the-edge-woke-up-again)
- [**Thirty-six malicious npm packages in one day, all generated from one template: `dowload_ebok_<book title>_by_<author>_<5 chars>`, pirated-ebook download lures (`berserk_tome_05`, `bleach_tome_53`, `one_piece..._oda`) shipped in two publish waves and imported on two queue ticks, every name holder-sealed inside 76 s to 4 m — when the names are generated, the misspelled `dowload` prefix is the cluster key, and per-name forensics is waste**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)
- [**Three ledgers disagreed about one malicious package at once: the advisory enumerated seven poisoned versions `0.3.1`-`0.3.7` of `node-global-key-listener-v9`, npm's own version history has never heard of ANY of them, and the CDN still byte-serves `0.3.7` — a version list is an artifact, not a mirror, and triage that trusts any single census is triaging a draft**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)
- [**The pip RAT campaign that got its first name quarantined in twenty-three minutes grew a second name the same evening: `qap793gl4l` shares the `2026-11-testing1345` tag, the same `helper-exe.vercel.app` dropper infrastructure, and quarantined in ~30 min — and the advisory's own text records that the attacker's payload repo was STILL EMPTY at analysis: the takedown clock is beating the arming clock**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)
- [**A malware advisory filed against the wrong registry: `MAL-2026-19242` advises `tdesign-vue-mono 1.0.1` as a RubyGems package, RubyGems has never heard of the name (API "could not be found", versions 404) — while npm serves the exact advised rung 200, born ninety-eight seconds after its stage placeholder with no seal visit and the CDN missing it: an OSV row's ecosystem field is a claim, not an oracle, so read every registry for the name before calling a record phantom or live**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventieth-sweep)
- [**The edge cache that outlived a registry takedown turned out to forget on an hourly clock: the `0sec-cli 0.26.0` version jsDelivr kept serving for two sweeps after the registry deleted it answered 404 at its third read — a CDN afterimage is a lease, not a monument, and the next sweep that quotes CDN liveness from memory is quoting the past**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-270th-the-cdn-forgot)
- [**The catch lane's "paper before the ledger" gap measured at 46 minutes: the two malicious names the previous sweep found carrying critical advisories with empty ledgers (`@claudecode/cli`, `casamare`) took their OSV rows on a single 17:16:46Z import tick, 46-54 minutes behind their advisories, alias-at-birth — advisory-first blindness on a fresh malicious name is an hour, not an era, and every absent row is a clock until proven a hole**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventieth-sweep)
- [**GitHub's malware-advisory severity clock turned out to be predictable, not absent: the `mod_http2` RCE row (`GHSA-hjhf-gpg9-qqfj`, `CVE-2026-119618`) sat `severity unknown` and finally took `high`/`8.1` at exactly `published +48 h 0 m 31 s`, on a `:31`-batcher tick — so CVSS-keyed triage tooling is structurally blind to fresh critical rows for a two-day window you can forecast, and `unknown` means scheduled, not unimportant**](ops/apache-mod-http2-assign-headers-race-heap-corruption-rce-cve-2026-119618-wiz-november-2026.md#november-13-269th-the-enrichment-clock-fires-at-48-hours)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
