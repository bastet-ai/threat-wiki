# CISA KEV October 13, 2026: a two-row pair on a three-day clock — Ivanti Connect Secure auth-bypass-by-spoofing and Microsoft Windows Shell command injection, both due October 16

**Category:** ops
**First seen:** 2026-10-13
**Last verified:** 2026-10-14 (this wiki, KEV JSON pulled ~03:2x UTC, catalog 2026.10.13 / 1,741)

## What happened

CISA moved the KEV catalog twice on October 13 — its first movement since October 8 — closing this wiki's five-day KEV-lag streak in one day. The catalog now stands at **2026.10.13 / 1,741 entries** (+2 on the day: 1,739 → 1,740 → 1,741). Both rows carry compressed **due dates of 2026-10-16** — a three-day BOD clock, the same compressed posture this wiki logged on the September 22 security-product batch.

This page resolves the double-page decision this ledger carried since the 123rd sweep (both rows were recorded in stream sections at first sighting; the 123rd flagged "both page decisions next sweep"). They land together because they share the deadline, the compressed-clock posture, and — for the Windows row — a new BOD-era note field.

## The two rows

| CVE | Product | Mechanism (per catalog) | Date added | KEV due | Ransomware |
|---|---|---|---|---|---|
| CVE-2026-104935 | Ivanti Connect Secure | Authentication Bypass by Spoofing (CWE-290); unauthenticated → arbitrary commands per vendor advisory chain | 2026-10-13 | 2026-10-16 | Unknown |
| CVE-2026-96951 | Microsoft Windows (Windows Shell) | Command Injection (CWE-77) | 2026-10-13 | 2026-10-16 | Unknown |

## CVE-2026-104935 — Ivanti Connect Secure

- Catalog notes cite the vendor advisory at `forums.ivanti.com` (Security Advisory: Ivanti Connect Secure CVE-2026-104935) and the NVD record.
- This is the **third Ivanti-edge KEV pressure point of 2026** on this ledger's watch: ICS/ISE-class appliances have repeatedly been the fastest-follow KEV entries after confirmation, and the same pattern holds here — the KEV row followed public exploitation confirmation by roughly four days (CIRCL exploitation reporting preceded the listing; see the 121st-sweep stream section).
- Hunt posture is unchanged from this wiki's standing ICS guidance: edge appliance with exposed console/portal, credential-integrity anomalies, and post-auth session artifacts; assume compromise of any unpatched ICS in the window since early October.

## CVE-2026-96951 — Windows Shell command injection

- Catalog notes cite the MSRC guidance page and — the durable part — **`BOD 26-04: Prioritizing Security Updates Based on Risk`** plus its **Forensics Triage Requirements** implementation-guidance link. This is the BOD-26-04 era's triage language arriving in a KEV note: the deadline is not just "patch by Oct 16" but "patch by Oct 16 **and** perform the BOD triage forensics steps," which materially changes federal-response obligations and is a reasonable template for non-federal triage scoping too.
- Windows Shell command injection (CWE-77) is user-interaction-adjacent by class: phishing/document lures are the expected initial vector; the deadline compression suggests Microsoft/CISA assess active exploitation pressure.

## Why this pair matters together

1. **Two compressed clocks, one day.** Both due 2026-10-16. Federal owners have a weekend-sized window on an edge VPN appliance and a workstation shell flaw simultaneously — patch-planning contention is itself the risk.
2. **KEV lag again ~4 days.** The Ivanti row followed confirmed exploitation by ~4 days (same lag shape this ledger measured on prior Ivanti listings). Defenders should treat vendor "actively exploited" language as the KEV-inbound signal, not wait for the catalog row.
3. **BOD 26-04 triage language appears in a KEV note.** Watch whether subsequent rows carry the same forensics-triage citation — if it sticks, KEV rows are becoming two-part obligations (deadline + triage), and this wiki will note it per-row.

## Monitor forward

- Patch/triage confirmation on both rows before the **2026-10-16** deadline; whether CISA adds forensics-triage citations to future rows.
- Whether Ivanti's advisory gets an exploitation-detail follow-up (actor attribution, session-token mechanics) — the CIRCL confirmation predates the row, more detail typically follows the listing.
- Whether the Windows Shell CVE matures beyond "Awaiting Analysis" at NVD (at this wiki's check the MSRC guidance is the primary artifact).
