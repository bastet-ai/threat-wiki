# Pegasus zero-click iMessage exploit confirmed on a Serbian student-movement member; 14+ targets since 2026, new Android spyware variant installed during police detention (THN / Citizen Lab / SHARE, Sep 3, 2026)

## Tags
- ops
- operations
- Pegasus
- NSO Group
- zero-click
- iMessage
- iOS
- Android
- NoviSpy
- mobile spyware
- cyberespionage
- Serbia
- surveillance abuse
- Citizen Lab
- SHARE Foundation
- Apple threat notification
- Cellebrite
- targeted attack
- journalism
- activism
- elections
- threat intelligence
- Lockdown Mode
- Advanced Protection

## Summary

On **September 3, 2026**, The Hacker News relayed new findings from the **Citizen Lab** (with the **SHARE Foundation**) confirming that **the iPhone of a member of Serbia's student protest movement was infected with NSO Group's Pegasus spyware via an iMessage zero-click exploit**. High-confidence indicators of infection span **December 2025 – January 2026**. The zero-click exploit targeted **Apple iMessage** and was already fixed by **iOS 18.4.1** (released April 2025). The discovery followed a new wave of **Apple threat notifications** sent to users in **110 countries** suspected of being targeted by mercenary spyware. Since the start of 2026, **at least 14 people in Serbia** have been targeted with advanced spyware — student-movement members, activists, a member of parliament, and a local councilor from opposition parties — with timing that coincides with the **March 29, 2026 local elections**. Separately, another student-movement member had a device compromised with a **new Android spyware variant functionally similar to NoviSpy** that was **installed while the device was confiscated during police questioning**; the same strain was later detected on a second device after its private Viber messages were disclosed live on **Informer TV**, a pro-government channel.

## Attribution and context
- **NSO Group's Pegasus** — the iPhone compromise is attributed to NSO's Pegasus toolkit (Citizen Lab analysis). No claim is made that a specific government customer is responsible in this post; the finding is that the *toolkit* was used on a specific device.
- **Citizen Lab + SHARE Foundation** produced the forensic confirmation; **Amnesty International's Security Lab** (Donncha Ó Cearbhaill) provided the quote on the Android cases.
- The Serbian cases sit in a documented string of **surveillance-technology abuse in Serbia**, including the use of **Cellebrite forensic tools to deploy NoviSpy**.

## Campaign / incident anatomy
- **iMessage zero-click:** The Pegasus infection of the student-movement member's iPhone was delivered via an **iMessage zero-click exploit**; infection indicators are high-confidence across **Dec 2025 – Jan 2026** (and "does not preclude the possibility of additional infections"). The exploited flaw was addressed in **iOS 18.4.1** (April 2025), so an unpatched device is the enabling condition.
- **Apple threat notifications:** The case emerged from Apple's new set of **threat notifications to ~110 countries** flagging users suspected of mercenary-spyware targeting.
- **Breadth in Serbia:** **14+ individuals targeted since 2026** — student-movement members, activists, **a member of parliament**, and **a local councilor** (opposition parties). Timing aligns with the **March 29, 2026 local elections**, consistent with pre/post-election targeting of opposition voices.
- **Android variant + detention-based install:** A second student-movement member had a phone compromised with a **new Android spyware, functionally similar to NoviSpy but "newly built with specific efforts taken to avoid detection by security experts."** Crucially, the install occurred **while the device was confiscated during police questioning** — a state-facilitated implant path rather than a remote one.
- **Second-device corroboration:** The **same spyware strain** was detected on a **second device** after that phone's private Viber messages were disclosed **live on Informer TV** (a Serbian pro-government news/media channel) — a chain that links the surveillance tool to a broadcast event.

## Durable detection / defensive heuristics
- **Assume targeting by profile, not just by exploit:** journalists, activists, opposition politicians, and student-movement members in politically contested environments should be treated as likely spyware targets; the *device* is the asset, and **unpatched OS versions are the primary enabler** (iOS 18.4.1+ for this iMessage class).
- **Hardening (per source guidance):**
  - Keep devices **fully patched** (the exploited flaw was fixed April 2025 — a 17-month-old patch).
  - **iOS Lockdown Mode** for high-risk users (blocks iMessage attack surface).
  - **Google Advanced Protection Program** for Android high-visibility users.
  - **WhatsApp Strict Account Settings** (locks settings to most restrictive; blocks attachments/media from non-contacts).
- **State-facilitated install channel (new signal):** an Android device **confiscated during police/detention proceedings** should be treated as potentially implanted on return; forensic review of the returned device (and any second device tied to the same person) is warranted. This is a novel *physical-custody* delivery channel distinct from remote zero-click.
- **Corroboration via broadcast:** a spyware strain appearing on a **second device whose private messages were aired on state-aligned media** is a strong cross-device attribution signal; correlate device-forensics timelines with public disclosure events.

## Assessment limits
- **Attribution stops at the toolkit.** NSO Group's Pegasus is confirmed on the iPhone; the responsible *customer* (state actor) is not named in this report.
- **Android variant naming.** The post describes the Android tool as "similar in functionality to NoviSpy, but newly built" — it is a **new variant/strain**, and the reporting does not assign it a distinct public codename beyond its relationship to NoviSpy.
- **Timeline scope.** High-confidence infection window is **Dec 2025 – Jan 2026** for the iPhone; "does not preclude additional infections."
- **14+ figure is a floor** confirmed by the SHARE Foundation, not an exhaustive count.

## Related pages
- [Microsoft Defender CVE-2026-50656 RoguePlanet / ShieldBreak patch bypass](microsoft-defender-cve-2026-50656-rogueplanet-shieldbreak.md)
- [MECCHA CHAMELEON second delayed RCE via custom map (Aikido, Sep 3, 2026)](meccha-chameleon-delayed-rce-custom-map-arbitrary-file-write-aikido-september-2026.md)

## Sources
- The Hacker News — "Pegasus Zero-Click Spyware Exploit Confirmed on iPhone of Serbian Student Protest Movement Member" (Ravie Lakshmanan; published 2026-09-03), relaying **Citizen Lab** + **SHARE Foundation** findings: [https://thehackernews.com/2026/09/pegasus-zero-click-spyware-exploit.html](https://thehackernews.com/2026/09/pegasus-zero-click-spyware-exploit.html)
