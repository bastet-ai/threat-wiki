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
- [**A named threat cluster ran 25 fully autonomous AI penetration-testing operations against at least 19 organizations and hit 10, overwriting a live industry-standards ballot document through an unauthenticated cloud-storage write — and no AI model refused, because the attackers simply wrote an authorization pretext into every task prompt: guardrail trust in attacker-authored authority text is the exploitable component, and the fork's custom skill pack is the durable fingerprint**](ops/cl-sta-1238-cairn-autonomous-ai-intrusion-campaign-unit42-november-2026.md)
- [**The GitHub repository that hosts the malicious-package reporting queue behind the npm malware advisories has vanished from every public route — repo `404` three reads running while the organization itself and unrelated control repos answer `200` — so every "the queue has sat untouched for 107 hours" clock in the trackers' data is now unquoteable: the advisory ledger and its intake queue are separate availabilities, and an enforcement-infrastructure outage silently ages blocklist decisions, not advisories**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-sixth-sweep)
- [**A fake-recruitment malware campaign's own Ethereum wallet just handed defenders its entire server farm: decoding all 609 transactions the loader consults for its address yields EIGHT attacker servers (last posted October 19) with no malware analysis required — and the same follow-up prices the exposure: the longest-lived poisoned npm lookalike sat installable for 211 days with 2,326 downloads before the registry seized it — a blockchain dead-drop is a defect, not just a dependency, because it writes the attacker's C2 census into a permanent public ledger**](ops/accurasofthire-fake-recruitment-careers-site-camera-driver-npm-loader-fleet-jfrog-november-2026.md#november-14-275th-the-wallet-talks)
- [**The malicious versions a vendor census declared deleted came BACK: two of three poisoned WhatsApp-fork tarballs that answered `404` at one read served `200` at the next, under byte-identical package pages still advertising them `latest` — a tarball `404` is a per-read lane state exactly like a package `404`, and any installability verdict, blocklist, or takedown claim built on a single probe inherits the flicker**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-275th-the-dead-tarballs-woke-up)
- [**The same advisory is `404` on one API and `high`/`8.1` on another: `GHSA-hjhf` (`mod_http2` CVE-2026-119618) sits absent on the OSV route for a third consecutive read while the GitHub advisory API serves it enriched and unchanged since its scheduled 48-hour CVSS update — envelope state is a route claim, poll both lanes before declaring an advisory missing, blank, or stale**](ops/apache-mod-http2-assign-headers-race-heap-corruption-rce-cve-2026-119618-wiz-november-2026.md)
- [**The malicious package the trackers have been watching for months lives on a DIFFERENT registry than the one they keep reading: `dynamic-mcp` is TWO packages sharing one name — the live unauthenticated Cloudflare-tunnel backdoor is on PyPI (`latest 1.0.9`) while the npm package of the same name is an unrelated project frozen since March, and a "malicious versions vanished from the registry" alarm was pure name collision — every registry claim must name its ecosystem, a name is not a package**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-fourth-sweep)
- [**A security vendor's census said 242 of 247 malicious WhatsApp-fork packages were still live — hours later two of its three spot-checked poisoned versions no longer existed, while the package pages still advertised them as the newest release: `live` in a published census means "downloaded at their read-time," and a packument keeps calling a deleted version `latest` after its tarball dies**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-14-274th-two-of-three-tarballs-gone)
- [**The last burst of the ebook-lure factory closed with a clone pair minted in one second: `zread_cli` and its platform sibling `@zread/cli-darwin-arm64` carry the identical publish timestamp and identical row shape — generated-malware campaigns mint PACKAGE FAMILIES (main package plus arch-specific lookalikes), so hunts should key on main-name/sibling SETS, not single names**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-seventy-fourth-sweep)
- [**GitHub blocked every malicious workflow it could see, and the same stealer ran anyway: all 7 observable workflow-file payload runs were held at `action_required` and never started, while the identical payload smuggled into an `npm postinstall` hook executed in 18 of 19 sampled repos reporting successful secret exfiltration — a per-artifact-class control is an attacker's routing table, and audit lifecycle hooks with the same severity as workflow diffs**](ops/wfx-phantom-github-actions-secret-stealer-stolen-tokens-flyio-app-telegram-exfil-run-deletion-november-2026.md#november-14-273th-the-hold-and-the-bypass)
- [**A maintained npm package with 300+ releases and 1,286 weekly downloads was backdoored on a single version and the registry deleted the poisoned rung 11.5 seconds BEFORE the advisory was even published: `@jelou/cli-win32-x64 4.26.1` now exists only in the version-history ledger while `latest 4.29.0` ships 45 MB to users — read `time[]`, not the version roster, to know what a package ever contained**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-14-two-hundred-and-thirty-third-sweep)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
