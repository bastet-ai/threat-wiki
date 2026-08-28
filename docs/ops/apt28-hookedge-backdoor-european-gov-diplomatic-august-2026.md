# APT28-linked HOOKEDGE backdoor targets European government and diplomatic organizations

## Summary
Recorded Future Insikt Group's **August 28, 2026** analysis (cited via The Hacker News) documents a previously undocumented backdoor dubbed **HOOKEDGE** deployed in campaigns against **Romanian, Spanish, and Turkish** government and diplomatic organizations between **late September 2025 and early April 2026**. HOOKEDGE is a **lightweight Windows batch-script backdoor** delivered via macro-enabled Word documents with diplomatic-themed lures. Recorded Future attributes the activity to **APT28 / Fancy Bear / Forest Blizzard** with **moderate confidence** and tracks the cluster under the moniker **BlueDelta**; the attribution rests on significant code and tradecraft overlap with **HEADLACE**, a modular Windows backdoor APT28 has used against diplomats since April 2023. Recorded Future describes HOOKEDGE as a **"direct evolutionary successor to HEADLACE."**

## Tags
- APT28
- Fancy Bear
- Forest Blizzard
- BlueDelta
- HOOKEDGE
- HEADLACE
- webhook.site
- scheduled task
- macro-enabled Word
- batch script
- headless Edge
- Romania
- Spain
- Turkey
- diplomatic
- government
- espionage

## Why this matters
- HOOKEDGE adds a durable, named batch-script backdoor to APT28's espionage tradecraft and shows the cluster deliberately refining *existing* tooling rather than introducing new capabilities.
- The C2 dependency on **webhook[.]site** (a public request-catching service) and its free-tier request quota (100 requests per unique endpoint) drove a two-stage architecture: broad initial access first, then escalation of high-value victims to dedicated second-stage webhooks with beaconing as fast as **5 minutes**.
- Defender signals are concrete and cheap to hunt: scheduled-task abuse with 30-minute intervals, **headless or hidden Microsoft Edge** making outbound HTTP requests, and connections to `webhook[.]site`-class services.

## Reported chain
1. Macro-enabled Word document with a diplomatic-themed lure (early versions impersonated Spanish government material; a social-engineering approach replaced that roughly a month later).
2. Victim clicks "Enable Content"; the macro writes **six files** to `%userprofile%` and launches the HOOKEDGE installer chain.
3. An installer launcher creates a **scheduled task running every 30 minutes** that executes the HOOKEDGE launcher with the backdoor as its argument.
4. The main installer then deletes itself, the installer launcher, and the task definition file to reduce the forensic footprint.
5. The batch backdoor runs a polling loop: fetches arbitrary `.cmd` payloads from a staging `webhook[.]site` URL, executes them, and returns output to the webhook **using an HTML file**, with retrieval and exfiltration performed by launching **Microsoft Edge in headless mode or a hidden window**.
6. After transmission, temporary files are deleted and any process whose window title matches the HOOKEDGE task identifier is terminated.
7. A hidden image in the lure document originally referenced a `webhook[.]site` URL to alert operators when the document was opened; that canary was later **removed** to reduce network-based IOCs.
8. For high-value targets, a **second-stage payload** was deployed with beaconing intervals as short as five minutes — separating initial-access infrastructure from active collection infrastructure because the free-tier quota would otherwise be exhausted within ~2–3 days at a 30-minute interval.

## Attribution notes
- Recorded Future Insikt Group (Mastercard-owned) attributes the campaigns to APT28 with **moderate confidence**, based on code and tradecraft overlap with HEADLACE, including shared core architecture and shared abuse of `webhook[.]site` for C2, payload staging, and exfiltration.
- Keep attribution phrasing tied to Recorded Future; this wiki does not independently corroborate the APT28 link.
- The public relay is The Hacker News (August 28, 2026); the primary source is the Recorded Future research page.

## Defender heuristics
- Block macro execution from internet-originated documents; treat `Enable Content` + mass file writes to `%userprofile%` as high-priority.
- Hunt scheduled tasks with ~30-minute intervals whose action is a batch file or launcher under user profiles.
- Alert on headless or hidden Microsoft Edge processes making outbound HTTP requests (a rare and strong indicator of this implant family).
- Egress-block or alert on `webhook[.]site` and analogous public request-capture services; inspect for `.cmd`-shaped fetch/POST patterns and HTML-file output posts.
- Scope Romanian, Spanish, and Turkish government and diplomatic environments first; watch for a shift to new staging domains after sandbox evasion tuning.

## Related pages
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)
- [Ghostwriter](../actors/ghostwriter.md)

## Sources
- Recorded Future Insikt Group: [BlueDelta targets with HOOKEDGE](https://www.recordedfuture.com/research/bluedelta-targets-with-hookedge)
- The Hacker News: [APT28-Linked HOOKEDGE Backdoor Targets European Government and Diplomatic Organizations](https://thehackernews.com/2026/08/apt28-linked-hookedge-backdoor-targets.html)
