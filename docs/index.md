---
title: threat.wiki
---

# threat.wiki

Threat intelligence notes, group profiles, named-person records, and defensive guidance.

## Popular this week
<!-- popular-this-week:auto -->
_Auto-maintained from Cloudflare zone analytics, last 7 days ending 2026-11-04 UTC (21880 of ~734 on-page requests attributable; 84 of 734 path batches ok)._
- [RubyGems 24-gem crypto-utility fleet, the 45.138.12.177 C2 RETURNS under fresh names](/ops/rubygems-crypto-utils-24-gem-fleet-c2-return-reqthrottle-grammar-45-138-12-177-october-2026/) — 295 reads
- [CISA KEV August 27, 2026 additions](/ops/cisa-kev-owncloud-linux-artifactory-august-27-2026/) — 258 reads
- [Source index](/notes/source-index/) — 163 reads
- [binding.gyp npm CI/CD worm](/ops/binding-gyp-npm-cicd-worm/) — 142 reads
- [SubQuery @subql/common@5.8.3](/ops/subql-common-ci-artifact-substitution-release-pipeline-compromise-october-2026/) — 140 reads
- [Cavern](/tools/cavern/) — 129 reads
- [Kimsuky / Emerald Sleet / TA427](/actors/kimsuky-emerald-sleet-ta427/) — 116 reads
- [SilkParasite](/actors/silkparasite/) — 112 reads
<!-- /popular-this-week:auto -->

## Recent entries
- [**Apache's HTTP/2 header path hides a pre-auth heap-corruption RCE across sixteen releases: 64% of cloud environments hold a vulnerable resource, no public exploit yet, and GitHub's own advisory row still read "severity unknown" nine hours in: the KEV listing would be the exploitation confirmation, not the patch reminder**](ops/apache-mod-http2-assign-headers-race-heap-corruption-rce-cve-2026-119618-wiz-november-2026.md)
- [**A patched web app is not a closed incident: unrelated actors are running the open-source GSocket relay on compromised Linux servers, both ends dial out to a shared public relay so there is no attacker IP to block, and the session keeps working after the entry-point vulnerability is fixed**](tools/gsocket-gs-netcat-gsrn-relay-c2-post-patch-persistence-linux-microsoft-november-2026.md)
- [**The quarantined payments backdoor got both ledger rows within two hours while its report PR still sat unmerged, and the C2 listener is still live on its second read: ledger silence on a hot name has a sub-sweep half-life, and a query-lane `{}` means not-yet-served, never not-yet-authored**](ops/aurum-pay-pypi-payments-sdk-first-call-command-execution-november-2026.md#november-11-250th-sweep-the-ledgers-catch-up-in-two-hours-and-no-gate-waited)
- [**Five lookalike npm packages carry live critical advisories and every advised version still installs: two hide a zlib byte-array in their own package.json under the same throwaway-mail publisher class, one impersonates @tailwindcss/forms at four identity fields, and a sixth name was wiped from the registry nine days before its advisory arrived**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-fiftieth-sweep)
- [**A PyPI "payments SDK" runs whatever its ping endpoint returns on the first API call, and PyPI quarantined the name on a reporter's ticket while both public ledgers stayed at zero: no OSV row, no GHSA, and the C2 listener still answers live**](ops/aurum-pay-pypi-payments-sdk-first-call-command-execution-november-2026.md)
- [**The critical React Server Components RCE (CVSS 9.5, no CVE) reached GitHub's global advisory database twenty-seven days after the fix shipped: CVE-keyed tooling never saw it, and the Next.js fix must come from `next` itself, not `react`**](ops/nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md#november-11-249th-rsc-rce-late-arrival)
- [**A package whose malware record was withdrawn months ago still installs today: the query lane hides the withdrawn row, the direct lane still serves it, and the npm registry never heard of the withdrawal at all**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-eighth-sweep)
- [**A Baileys fork's README claims "no hidden auto-follow" while its code silently follows WhatsApp channels, and its sibling was reported 90 minutes after birth with a file copied byte-for-byte from a previously-minted malware package**](ops/baileys-libsignal-node-npm-whatsapp-channel-follow-campaign.md#november-11-248th-queue-pair)
- [**One template minted 23 lookalike npm names in ninety minutes and the bot sealed every one inside three minutes: the biggest carried 9,476 weekly downloads, and its weekly counter was a pre-seal census**](ops/algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-seventh-sweep)
- [**npm's excision lane swept past the advisory: the AI security CLI's clean `0.28.9` release vanished with no advisory against it, so "the name still installs" was a fact with a two-hour half-life**](ops/0sec-cli-npm-ai-security-cli-compromise-november-2026.md#november-11-247th-second-excision)

## Sections
- **Ops**, campaign timelines, compromise chains, and sequencing
- **Tools**, malware, payloads, implants, and attacker infrastructure
- **Groups**, crews, cluster names, and shared operational personas
- **People**, publicly identified individuals or project personas when public sourcing supports it
- **Patterns**, reusable defender heuristics
- **Notes**, taxonomy, usage, and editorial guidance
