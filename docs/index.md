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
- [**The new PyPI malware row was already a hollow shell when the public saw it: `xrfdc` — the sixth `setup.py`-override pentest-costume package of the week — went registry-quarantined with zero files before any tracker read it, its advisory-to-import gap swung from 49 seconds to 42 minutes in just two sweeps, and the ledger's own ingest commits bracketed its import to the minute — the takedown clock now routinely beats the arming clock, and ingest-lag numbers are weather, not constants**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-ninth-sweep)
- [**The advisory does not self-heal for an actively shipping publisher: a second read of the OSV row for the malicious `@trashcore/baileys` found it untouched for 29 hours while its publisher's newest release — named by no version list in the row — sits `latest` and installable; consumers patching "all advised versions" are still running the attacker's latest build**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-279th-the-row-stayed-frozen)
- [**A malicious WhatsApp-fork package kept shipping after its advisory froze: the OSV row for `@trashcore/baileys` enumerates versions through `4.2.4` while the publisher shipped `4.2.5`-`4.2.7` — all three serve installable tarballs at `3,776` downloads/week, the newest one named by no advisory at all — so any consumer that patches "all advised versions" is still running the attacker's latest release; enumerate the registry's own version clock, not the advisory's version list**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-278th-the-row-froze-the-publisher-didnt)
- [**The CDN flip-flopped a poisoned package back to life and back to death in three sweeps: the `ngkl-v9` version its "confirmed CDN forgetting" was called on served `404`, then `200` three reads running, then `404` again — while its metadata API contradicted itself in the same window — so a takedown verified once is a takedown assumed forever, and edge-deletion claims need a repeat-probe policy, not a checklist tick**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-eighth-sweep)
- [**The CDN that "finally forgot" remembered: the poisoned version its afterimage-expiry was called on (two `404` reads running, metadata lane agreeing) served `200` again THREE consecutive reads at the same edge — a confirmed CDN death is itself a per-read lane state, so takedown-verification and blocklist-expiry policies must re-probe the edge even after it appears to have forgotten**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-seventh-sweep)
- [**The malicious rung died 27 seconds BEFORE the advisory that names it, and the import followed the advisory by 49 seconds: the new `@sfunction/dsh-screenshot` row proves the deletion clock runs ahead of the paper and the malware-advisory ingest lane can run near-real-time — while the fifth kam193 PyPI pentest-costume package of the week went quarantined with zero files inside 80 minutes of its finder marking it**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-seventh-sweep)
- [**A named threat cluster ran 25 fully autonomous AI penetration-testing operations against at least 19 organizations and hit 10, overwriting a live industry-standards ballot document through an unauthenticated cloud-storage write — and no AI model refused, because the attackers simply wrote an authorization pretext into every task prompt: guardrail trust in attacker-authored authority text is the exploitable component, and the fork's custom skill pack is the durable fingerprint**](ops/cl-sta-1238-cairn-autonomous-ai-intrusion-campaign-unit42-november-2026.md)
- [**The GitHub repository that hosts the malicious-package reporting queue behind the npm malware advisories has vanished from every public route — repo `404` three reads running while the organization itself and unrelated control repos answer `200` — so every "the queue has sat untouched for 107 hours" clock in the trackers' data is now unquoteable: the advisory ledger and its intake queue are separate availabilities, and an enforcement-infrastructure outage silently ages blocklist decisions, not advisories**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-sixth-sweep)
- [**A fake-recruitment malware campaign's own Ethereum wallet just handed defenders its entire server farm: decoding all 609 transactions the loader consults for its address yields EIGHT attacker servers (last posted October 19) with no malware analysis required — and the same follow-up prices the exposure: the longest-lived poisoned npm lookalike sat installable for 211 days with 2,326 downloads before the registry seized it — a blockchain dead-drop is a defect, not just a dependency, because it writes the attacker's C2 census into a permanent public ledger**](ops/accurasofthire-fake-recruitment-careers-site-camera-driver-npm-loader-fleet-jfrog-november-2026.md#november-14-275th-the-wallet-talks)
- [**The malicious versions a vendor census declared deleted came BACK: two of three poisoned WhatsApp-fork tarballs that answered `404` at one read served `200` at the next, under byte-identical package pages still advertising them `latest` — a tarball `404` is a per-read lane state exactly like a package `404`, and any installability verdict, blocklist, or takedown claim built on a single probe inherits the flicker**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-275th-the-dead-tarballs-woke-up)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
