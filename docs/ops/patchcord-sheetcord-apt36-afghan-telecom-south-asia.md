# PATCHCORD / SHEETCORD: APT36 backdoor campaign against Afghan telecom and South Asian critical infrastructure

## Summary
Acronis Threat Research Unit (TRU) reported a new, ongoing campaign delivering a previously undocumented backdoor, **PATCHCORD**, against **Afghan telecom providers and South Asian (including Indian) critical-infrastructure organizations**. PATCHCORD is a compiled **C/C++** implant delivered through sector-specific lures — including **fake VPN installers impersonating Afghan Telecom (AFTEL)** and telecom management tools. Infrastructure analysis also surfaced a second, **Go-based** backdoor, **SHEETCORD**, which uses **Google Sheets** for command-and-control. The delivery chain's starting point is a ZIP named `Telecom_TMS.zip` containing an Inno Setup installer (`TMS_AfghanTelecom.exe`) that deploys PATCHCORD. The activity is assessed with **moderate confidence** to be **APT36 (aka Transparent Tribe)**, a Pakistan-aligned actor, based on targeting overlaps, malware similarities, shared infrastructure, and tradecraft. A SHEETCORD-related domain impersonates India's **National Informatics Centre (NIC)**, and the campaign centers on a single C2 server with associated domains — including domains impersonating Afghan telecom operators and a hijacked legitimate healthcare domain.

## Tags
- ops
- operations
- PATCHCORD
- SHEETCORD
- APT36
- Transparent Tribe
- Afghan telecom
- South Asia
- critical infrastructure
- Inno Setup
- fake VPN
- C2
- Google Sheets C2
- backdoor
- Acronis TRU
- Pakistan-aligned
- NIC impersonation

## Why this matters
- **Telecom + critical-infrastructure convergence:** the lures impersonate real internal systems (AFTEL's Transport Management System) and a national government IT body (India's NIC), signaling targeted rather than spray-and-pray delivery.
- **Two backdoors, two languages, two C2 styles:** C/C++ PATCHCORD plus Go SHEETCORD with a consumer-cloud C2 (Google Sheets) — a tradecraft mix that complicates a single-detection-rule response.
- **Moderate-confidence APT36 attribution** adds this campaign to the Pakistan-aligned cluster already tracked for telecom and critical-infrastructure intrusions; shared-infrastructure and malware-overlap evidence should be cross-checked against existing APT36/Transparent Tribe sightings.
- **Hijacked legitimate healthcare domain** in the C2 set is a concrete, durable hunting pivot.

## Reported chain
1. Victim receives sector-specific lure (fake AFTEL VPN installer / telecom management tool).
2. `Telecom_TMS.zip` → Inno Setup installer `TMS_AfghanTelecom.exe` (TMS = Transport Management System, AFTEL's internal system for tracking corporate vehicle/transport requests).
3. On execution, PATCHCORD conceals its console window and establishes persistence by hijacking the browser (per the report summary).
4. C2 traffic to a single C2 server and associated domains (Afghan telecom operator impersonations, hijacked healthcare domain).
5. SHEETCORD (Go) uses Google Sheets for C2; a related domain impersonates India's National Informatics Centre (NIC).

## Indicators and pivots
- `Telecom_TMS.zip`, `TMS_AfghanTelecom.exe` (Inno Setup installer).
- Lure impersonation: Afghan Telecom (AFTEL) VPN / telecom management tools; India National Informatics Centre (NIC) domain.
- C2 architecture: single C2 server + associated domains, including a **hijacked legitimate healthcare domain** and Afghan telecom operator impersonations.
- Two implant families: C/C++ PATCHCORD; Go SHEETCORD (Google Sheets C2).

## Defender actions
- **Inventory and validate** any Inno Setup "VPN"/"TMS"/telecom-management installers on endpoints, especially in telecom, transport, and government/critical-infrastructure environments; treat unexpected `Telecom_TMS.zip` / `TMS_AfghanTelecom.exe` as malicious.
- **Hunt the hijacked healthcare domain** and Afghan telecom impersonation domains in proxy/DNS logs; a legitimate healthcare domain acting as C2 is a strong, durable indicator.
- **Detect Google Sheets C2:** outbound access to `docs.google.com` sheet endpoints from server/telecom workstations is atypical and worth alerting on as a SHEETCORD-style C2 channel.
- **Cross-check APT36 / Transparent Tribe** infrastructure and malware families (moderate confidence); correlate with existing APT36 sightings on shared domains, tooling, and target sectors.
- **For telecom operators:** review remote-access/VPN distribution channels and internal system branding (TMS) for spoofing; verify integrity of distributed installers.

## Confidence and limits
- Attribution to APT36 is **moderate confidence** per Acronis TRU, based on overlaps rather than a definitive link.
- Researchers cited: Darrel Virtusio, Santiago Pontiroli, Subhajeet Singha (Acronis TRU).
- Full IOC set (domains, hashes, C2 endpoints) is in Acronis's report; this page records the durable campaign structure and named artifacts.

## Related pages
- [Turla STOCKSTAY backdoor operations](turla-stockstay-backdoor-operations.md)
- [Pakistani law enforcement espionage convergence](pakistani-law-enforcement-espionage-convergence.md)
- [Operation DragonReturn India tax-season DcRAT campaign](operation-dragonreturn-india-tax-dcrat.md)

## Sources
- Acronis TRU: [PATCHCORD: new malware cluster targets Afghan telecom and South Asian critical infrastructure](https://www.acronis.com/en/tru/posts/patchcord-new-malware-cluster-targets-afghan-telecom-and-south-asian-critical-infrastructure/)
- The Hacker News: [New PATCHCORD Backdoor Targets Afghan Telecom and Indian Critical Infrastructure](https://thehackernews.com/2026/08/new-patchcord-backdoor-targets-afghan.html) — August 13, 2026
