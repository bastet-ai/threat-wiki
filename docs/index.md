---
title: threat.wiki
---

# threat.wiki

Threat intelligence notes, group profiles, named-person records, and defensive guidance.

## Popular this week
<!-- popular-this-week:auto -->
_Auto-maintained from Cloudflare zone analytics, last 7 days ending 2026-11-07 UTC (22344 of ~746 on-page requests attributable; 96 of 746 path batches ok)._
- [Source index](/notes/source-index/) — 169 reads
- [Tag index](/notes/tag-index/) — 123 reads
- [SilkParasite](/actors/silkparasite/) — 123 reads
- [Djinn Stealer](/tools/djinn-stealer/) — 120 reads
- [Kimsuky / Emerald Sleet / TA427](/actors/kimsuky-emerald-sleet-ta427/) — 113 reads
- [JiaT75](/people/jiat75/) — 112 reads
- [Cavern](/tools/cavern/) — 111 reads
- [PamStealer](/tools/pamstealer/) — 110 reads
<!-- /popular-this-week:auto -->

## Recent entries
- [**The malware advisory minted today already misses the version that installs as `latest`: the new npm `testpackage83` row names only `1.0.0`, while the same publisher's `1.0.1` — shipped the same morning, installable right now — points its "Chromium" downloader at a SECOND drop server, and the first server is currently serving a 20-byte "start calc" placeholder that any installer runs the moment the operator swaps the bytes. Five hours later a second reporter filed TEN more trojanized WhatsApp-library forks with zero advisories anywhere, the biggest pulling `2,211` downloads a week — together `27` named-malicious packages installing unadvised at `≈10,000` weekly installs — and even the ledger's own over-broad-range corrections are stuck in the same unmerged queue: paper is never a census, and a correction in the queue is a correction nowhere**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-eighty-fourth-sweep)
- [**Seventeen publicly-reported malicious packages entered the malware queue in seventy-two seconds and every one still installs today, together pulling about 3,500 downloads a week: one finder filed four batch reports covering six trojanized WhatsApp-library forks that auto-follow attacker channels, seven crypto-wallet lookalikes that post private keys to Telegram bots — three of which hand the stolen key off to their own sibling lookalikes, so removing one silently reroutes victims to another — plus a Telegram-session harvester and two install-time remote-code packages; none of the seventeen had any public advisory, and the queue had merged nothing hours after intake, so every automated defense was blind by construction: measure malicious packages by install flow, not by advisory count**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-eighty-third-sweep)
- [**Three crypto-exchange lookalike packages on PyPI tried to steal environment variables and host details in one publish run minutes apart, and all three were already registry-quarantined hollow shells before anyone read them — while the malware tracker that caught them introduced a brand-new "questionable pentest" label mid-flush next to its "probably harmless" label for the same trick, and the takedown serial numbers scrambled against the publish order, so serial order can never be used to order events: when one lookalike of a brand falls, sweep the whole brand, and read a tracker's new campaign tag as a filing decision, not a new threat**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-eighty-second-sweep)
- [**A confirmed Android spyware package shipped wearing the "probably harmless pentest tool" label: the new PyPI `ps-bool` row says its obfuscated import-time code exfiltrates photos and documents to a Telegram bot on Android devices, yet it arrived in the same one-minute finder flush as a package the same researcher filed as low-risk, and both were already registry-quarantined hollow shells — zero files — before any tracker read them — so triage malware by the artifact and behavior, never by the advisor's category label alone**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-eighty-first-sweep)
- [**A fourth consecutive read of the abandoned advisory for the malicious `@trashcore/baileys` fork found it untouched for 37 hours — its version list still stops at `4.2.4` while the attacker's publisher ships `4.2.7` as `latest` with an installable tarball — confirming there is no self-heal mechanism anywhere in the advisory pipeline, so "patched to the latest advised version" still means running the attacker's newest release**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-281st-fourth-read-frozen)
- [**When a malware advisory widened its own range after publish, the registry had already deleted the newly named version 22 seconds BEFORE the correction landed: the `@rclaude/darwin-arm64` advisory grew to name `0.2.1` at `14:08:16Z` while the package page changed at `14:07:53Z` — both advised tarballs `404`, the unadvised newest release still installable — so if you patch from an advisory's version list instead of the registry's own version clock, you are always trusting a document the takedown machines read first**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-eightieth-sweep)
- [**A malware advisory untouched for 35 hours is not slow, it is dead: the third consecutive read of the `@trashcore/baileys` row still stops at version `4.2.4` while the attacker's publisher ships `4.2.7` as `latest` with an installable tarball — nothing in the advisory pipeline re-checks a row against an actively shipping package, so "patched to the latest advised version" currently means running the attacker's newest release**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-280th-three-reads-frozen)
- [**The new PyPI malware row was already a hollow shell when the public saw it: `xrfdc` — the sixth `setup.py`-override pentest-costume package of the week — went registry-quarantined with zero files before any tracker read it, its advisory-to-import gap swung from 49 seconds to 42 minutes in just two sweeps, and the ledger's own ingest commits bracketed its import to the minute — the takedown clock now routinely beats the arming clock, and ingest-lag numbers are weather, not constants**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-ninth-sweep)
- [**The advisory does not self-heal for an actively shipping publisher: a second read of the OSV row for the malicious `@trashcore/baileys` found it untouched for 29 hours while its publisher's newest release — named by no version list in the row — sits `latest` and installable; consumers patching "all advised versions" are still running the attacker's latest build**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-279th-the-row-stayed-frozen)
- [**A malicious WhatsApp-fork package kept shipping after its advisory froze: the OSV row for `@trashcore/baileys` enumerates versions through `4.2.4` while the publisher shipped `4.2.5`-`4.2.7` — all three serve installable tarballs at `3,776` downloads/week, the newest one named by no advisory at all — so any consumer that patches "all advised versions" is still running the attacker's latest release; enumerate the registry's own version clock, not the advisory's version list**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-278th-the-row-froze-the-publisher-didnt)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
