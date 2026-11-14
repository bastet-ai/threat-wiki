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
- [**GitHub blocked every malicious workflow it could see, and the same stealer ran anyway: all 7 observable workflow-file payload runs were held at `action_required` and never started, while the identical payload smuggled into an `npm postinstall` hook executed in 18 of 19 sampled repos reporting successful secret exfiltration — a per-artifact-class control is an attacker's routing table, and audit lifecycle hooks with the same severity as workflow diffs**](ops/wfx-phantom-github-actions-secret-stealer-stolen-tokens-flyio-app-telegram-exfil-run-deletion-november-2026.md#november-14-273th-the-hold-and-the-bypass)
- [**A maintained npm package with 300+ releases and 1,286 weekly downloads was backdoored on a single version and the registry deleted the poisoned rung 11.5 seconds BEFORE the advisory was even published: `@jelou/cli-win32-x64 4.26.1` now exists only in the version-history ledger while `latest 4.29.0` ships 45 MB to users — read `time[]`, not the version roster, to know what a package ever contained**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-thirty-third-sweep)
- [**Two real compromises rode out inside a 250-package burst of pirated-ebook lure names: `rush-mfa` (born and holder-sealed in 77 seconds) and the genuine `@jelou/cli-win32-x64` sat in the same advisory flush as ~250 generated lures — filters that write off a batch as generated junk drop the real backdoor hiding in its middle**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-thirty-third-sweep)
- [**A package PyPI had fully REMOVED came back as a quarantined page one read later: `testing1345` went 404-whole-name-gone at one sweep and served `project-status: quarantined` the next — even a whole-name removal is a per-read lane state, and any blocklist or clean-list decision built on one registry answer inherits the flicker**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-thirty-third-sweep)
- [**The pirated-ebook npm name factory dropped its own signature mid-burst: of 380 malicious packages minted in one three-hour window, eleven carried the same `<title>_by_<author>_<5 chars>` template with NO misspelled `dowload_ebok_` prefix at all — a hunt keyed on the prefix would have missed them, so cluster malicious generated names on the name GRAMMAR and treat every prefix as costume**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-second-sweep)
- [**Three malicious pip packages were quarantined inside one hour of appearing, and the campaign's payload repo — opened on schedule — hosts nothing but `echo Hello!`: `testing1345` escalated from quarantine to whole-name removal, `qap793gl4l` held quarantine, and the third name `axiom-dragon-xyz` (wallet-file and cloud-credential stealer with a Discord-webhook exfil IOC) was quarantined before most defenders saw its advisory: the pull clock now beats the arming clock by hours**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-second-sweep)
- [**The CDN that called a package version dead changed its mind: jsDelivr answered 404 on the one `0sec-cli` version the registry still ships, then served it again one read later — a single edge-cache read, alive OR dead, is not a lane state, and any pinning or blocking decision built on one probe of one CDN is built on noise**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-272th-the-edge-woke-up-again)
- [**Thirty-six malicious npm packages in one day, all generated from one template: `dowload_ebok_<book title>_by_<author>_<5 chars>`, pirated-ebook download lures (`berserk_tome_05`, `bleach_tome_53`, `one_piece..._oda`) shipped in two publish waves and imported on two queue ticks, every name holder-sealed inside 76 s to 4 m — when the names are generated, the misspelled `dowload` prefix is the cluster key, and per-name forensics is waste**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)
- [**Three ledgers disagreed about one malicious package at once: the advisory enumerated seven poisoned versions `0.3.1`-`0.3.7` of `node-global-key-listener-v9`, npm's own version history has never heard of ANY of them, and the CDN still byte-serves `0.3.7` — a version list is an artifact, not a mirror, and triage that trusts any single census is triaging a draft**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)
- [**The pip RAT campaign that got its first name quarantined in twenty-three minutes grew a second name the same evening: `qap793gl4l` shares the `2026-11-testing1345` tag, the same `helper-exe.vercel.app` dropper infrastructure, and quarantined in ~30 min — and the advisory's own text records that the attacker's payload repo was STILL EMPTY at analysis: the takedown clock is beating the arming clock**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventy-first-sweep)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
