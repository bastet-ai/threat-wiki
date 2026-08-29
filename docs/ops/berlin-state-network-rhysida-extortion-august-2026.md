# Berlin state network compromise: Rhysida extortion after August exfiltration of the state administrative network (Aug 28–29, 2026)

## Tags
- ops
- operations
- ransomware
- extortion
- data exfiltration
- Rhysida
- government
- public sector
- critical infrastructure
- leak site
- CISA
- FBI
- MS-ISAC
- MFA
- Zerologon
- VPN
- Berlin
- Germany

## Summary

On **August 28, 2026**, the Berlin state government (Senate Chancellery) confirmed it is the target of an **extortion attempt** following an **August compromise of the city's state administrative network** and said it **will not meet the extortionists' demands**. The same statement disclosed that forensic work found further data outflows in the portfolio of the **Senate Department for Mobility, Transport, Climate Protection and Environment**, with exfiltration dated **August 7–12, 2026**; scope and content are still being examined, and the Senate Chancellery said personal or other non-public data **cannot be excluded**.

The department first reported an outflow on **August 7** — seven days before it was **cut off from the network on August 14**. Berlin has published no figure for how much data left; the only itemized account in circulation is the attackers' own.

## Attribution (moderate confidence, not state-named by CISA/FBI)

- **Der Spiegel** named **Rhysida** as the group on **August 28, 2026**, citing an entry on the group's darknet leak site and security sources involved in the response.
- The Hacker News confirmed via a leak-site monitoring service on **August 29, 2026** that an entry titled **"Berlin, Germany"** was added to Rhysida's leak site on **August 28**.
- The leak-site post claims **5.79 TB** of scanned data and **~1.44 million files**, identifying the victim only as "Berlin, Germany" (not the Senate or a specific department). Its eleven file categories — the largest being **124,823 maps and geodata files** — account for about a quarter of the claimed total file count. No ransom figure appeared in the entry.
- **Governing Mayor Kai Wegner**: "The state of Berlin is being blackmailed" (quoted in the machine-translated English version on Berlin's official city portal).
- The **state criminal police, public prosecutor, and federal security authorities** are investigating; **no group has been publicly confirmed** by authorities as of the August 29 reporting.

## Rhysida tradecraft context (CISA / FBI / MS-ISAC joint advisory, November 2023)

The joint CISA/FBI/MS-ISAC advisory on Rhysida documents three initial-access routes relevant to this incident:
- **Valid accounts on external-facing remote services** — authenticating to internal VPN access points with compromised credentials, notably at organizations **lacking MFA enabled by default**.
- **Zerologon (CVE-2020-1472)** — elevation of privilege in the Netlogon Remote Protocol (Microsoft-patched August 11, 2020).
- **Phishing** — recorded as a successful route into victim networks.

Rhysida is a financially motivated actor with a public extortion/leak-site model. Microsoft's May 2026 reporting linked Fox Tempest malware-signing-as-a-service to **Rhysida deployment** by Vanilla Tempest, and to families including Oyster, Lumma Stealer, and Vidar (see the [Fox Tempest profile](../actors/fox-tempest.md)).

## Indicators / durable signals

- **Victim:** Berlin, Germany (state administrative network / Senate Department for Mobility, Transport, Climate Protection and Environment portfolio).
- **Exfiltration window:** August 7–12, 2026 (department outflow reported Aug 7; network cut-off Aug 14).
- **Leak-site entry:** "Berlin, Germany" added to the Rhysida leak site on August 28, 2026; claimed 5.79 TB / ~1.44M files; largest category 124,823 maps/geodata files; no published ransom figure.
- **Response posture:** Berlin publicly **refused to pay** — a notable public-sector extortion-refusal data point.
- **Initial-access hypothesis (from the 2023 advisory, not yet confirmed for this incident):** VPN with valid-but-compromised credentials where MFA was not enforced; this is the highest-value durable lesson for any public-sector VPN.

## Defender guidance

- **Enforce MFA on all remote/VPN access points by default** — Rhysida's documented primary route is valid-account VPN access where MFA was off. This is the single highest-value control.
- **Patch and verify Netlogon / Zerologon posture** on domain controllers and member servers (CVE-2020-1472 and related Netlogon EOPs).
- **Assume exfiltration, not just encryption:** in extortion cases the data has likely already left; hunt for the outflow window (Aug 7–12 here), review DLP / egress logs, and treat "no data" as unproven until forensics confirm.
- **Public-sector MFA audit:** any organization (public or private) exposing VPN, RDP, or remote services without MFA-by-default matches Rhysida's initial-access profile.
- **Leak-site monitoring:** track the Rhysida leak site for the "Berlin, Germany" entry and any ransom figure, additional file categories, or follow-on publication that refines attribution or scope.

## Why this matters

- A **named, high-value public-sector victim** (a German state government) with a **documented exfiltration window** and a **leak-site entry** is a durable, verifiable data point — not a rumor.
- The **public refusal to pay** is a rare, citable signal in extortion-response literature and a useful benchmark for organizational extortion posture.
- Attribution to Rhysida is **moderate confidence** (press + leak-site entry, no authority confirmation yet); the CISA/FBI/MS-ISAC tradecraft provides the durable initial-access pattern to hunt for regardless of final attribution.

## Related pages

- [Fox Tempest (Malware-Signing-as-a-Service; linked to Rhysida deployment)](../actors/fox-tempest.md)
- [MISTIC Backdoor / KongTuke / ModelORAT (Rhysida-adjacent actor tooling)](mistic-backdoor-kongtuke-modelorat.md)

## Sources

- The Hacker News — "Berlin Refuses to Pay Hackers Who Stole Data From the City's State Network" (Swati Khandelwal; published 2026-08-28, feed pubDate Sat, 29 Aug 2026 03:00:52 +0530): [https://thehackernews.com/2026/08/berlin-refuses-to-pay-hackers-who-stole.html](https://thehackernews.com/2026/08/berlin-refuses-to-pay-hackers-who-stole.html)
- CISA / FBI / MS-ISAC joint advisory on Rhysida (November 2023) — initial-access routes: valid-account VPN without MFA, Zerologon (CVE-2020-1472), phishing.
- Der Spiegel (August 28, 2026) — naming of Rhysida, cited by The Hacker News.
- Berlin official city portal (machine-translated English) — Governing Mayor Kai Wegner statement.
