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
- [**A malware advisory filed against the wrong registry: `MAL-2026-19242` advises `tdesign-vue-mono 1.0.1` as a RubyGems package, RubyGems has never heard of the name (API "could not be found", versions 404) — while npm serves the exact advised rung 200, born ninety-eight seconds after its stage placeholder with no seal visit and the CDN missing it: an OSV row's ecosystem field is a claim, not an oracle, so read every registry for the name before calling a record phantom or live**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventieth-sweep)
- [**The edge cache that outlived a registry takedown turned out to forget on an hourly clock: the `0sec-cli 0.26.0` version jsDelivr kept serving for two sweeps after the registry deleted it answered 404 at its third read — a CDN afterimage is a lease, not a monument, and the next sweep that quotes CDN liveness from memory is quoting the past**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-270th-the-cdn-forgot)
- [**The catch lane's "paper before the ledger" gap measured at 46 minutes: the two malicious names the previous sweep found carrying critical advisories with empty ledgers (`@claudecode/cli`, `casamare`) took their OSV rows on a single 17:16:46Z import tick, 46-54 minutes behind their advisories, alias-at-birth — advisory-first blindness on a fresh malicious name is an hour, not an era, and every absent row is a clock until proven a hole**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-seventieth-sweep)
- [**GitHub's malware-advisory severity clock turned out to be predictable, not absent: the `mod_http2` RCE row (`GHSA-hjhf-gpg9-qqfj`, `CVE-2026-119618`) sat `severity unknown` and finally took `high`/`8.1` at exactly `published +48 h 0 m 31 s`, on a `:31`-batcher tick — so CVSS-keyed triage tooling is structurally blind to fresh critical rows for a two-day window you can forecast, and `unknown` means scheduled, not unimportant**](ops/apache-mod-http2-assign-headers-race-heap-corruption-rce-cve-2026-119618-wiz-november-2026.md#november-13-269th-the-enrichment-clock-fires-at-48-hours)
- [**An advisory's version list is a draft too: the `0sec-cli` critical (`GHSA-9j97`) that this wiki watched naming a single poisoned version for three days rewrote itself to name TWENTY versions twenty-five seconds after the registry bulk-deleted its newest version line — the enrichment landed inside one sweep window and the carried quote outlived it by two, so any triage that quotes an advisory's version list from memory is quoting the past**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-269th-the-paper-caught-the-ladder)
- [**Eight malicious npm packages caught today were all re-registrations of previously seized names: every one was `created` hours ago yet carries `time[]` stamps from weeks, months, even fifteen months in the past — the holder-seal costume erases the publisher but never the version-history ghosts, and the weekly download counters on these names (up to 774) are pre-seal victim flow you can use to size the exposure of a wave the moment it lands**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-sixty-ninth-sweep)
- [**A critical React Server Components RCE was patched on npm twenty-seven days BEFORE its advisory existed: CVE-2026-126187 (`GHSA-xqc2-xf4c-x3h3`, CVSS 9.5) in the Flight transport of `react-server-dom-webpack`/`-parcel`/`-turbopack` shipped its fixed rungs on Oct 14 while GitHub published the CVE on Nov 10, so advisory-driven patch discipline ran four weeks late in silence while the fix sat in plain view on the registry: watch the registry's publish clock, not just the advisory feed**](ops/react-server-components-flight-rce-cve-2026-126187-typed-array-deserialization-november-2026.md)
- [**A malware reporter's unmerged report spent thirty hours chasing the attacker's version ladder instead of leading it: the `@xzvbailss/baileys` Baileys-fork campaign shipped SIX new malicious-looking rungs today (to `6.0.9`) at 841 downloads a week while its open report sat untouched, and the reporter's first edit added exactly the rungs the attacker had already shipped — with the ledger and GitHub's advisory index still empty on the name, installs never waited for either**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-13-two-hundred-and-sixty-eighth-sweep)
- [**The malware publisher that resumed shipping after a six-sweep drought reads CLEAN: this wiki diffed `raiden-baileys 2.2.6`/`2.2.7` against the `2.2.5` baseline and the two new rungs touch four files of pure feature work, zero new attack surface and zero new endpoints — which neither excuses the resumption under a live full-range advisory nor convict the tarballs: a publishing-silence verdict and a payload verdict are different claims, and only the second needs a diff**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-13-268th-the-resumed-rungs-read-clean)
- [**A registry takedown does not reach the edge cache: the `0sec-cli` version `0.26.0` the registry deleted at 11:23Z today still serves HTTP 200 from jsDelivr, while the package's download counter keeps climbing to 2,944 a week on a name whose three newest version lines no longer exist at the origin — a takedown is a per-lane claim, and the CDN is the last lane to forget**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-13-268th-floor-holds-one-read-cdn-forgets)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
