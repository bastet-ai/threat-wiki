# BlueKit (SpyCloud, Sep 15, 2026): the first Browser-in-the-Middle PhaaS — the legitimate login page runs in an attacker-hosted remote browser and only the pixels stream to the victim; in **38% of observed compromises the kit auto-enrolled its own TOTP authenticator on the victim account**, so password rotation + session revoke alone leaves the attacker in

## Tags
- ops
- phishing
- PhaaS
- phishing-as-a-service
- BlueKit
- Browser-in-the-middle
- BitM
- AiTM
- adversary-in-the-middle
- MFA bypass
- TOTP enrollment
- session persistence
- remote browser
- interaction replay
- Doraemon
- device code phishing
- anti-analysis
- browser fingerprinting
- WebRTC STUN enumeration
- RAM CPU checks
- PwnForums
- BlgCloud
- LeakBase
- LeakBase revival
- Chucky
- backend database reuse
- copycat forums
- Russian-speaking
- SpyCloud
- identity security
- SaaS breaches

## Summary

**BlueKit** is a full-featured subscription phishing-as-a-service kit documented by **SpyCloud Labs on September 15, 2026** that SpyCloud tracks as **the only PhaaS kit so far offering Browser-in-the-Middle (BitM)** — an evolution past adversary-in-the-middle (AiTM). Where AiTM proxies traffic between the victim's browser and the real login service, **BitM loads the legitimate login page inside attacker-controlled infrastructure (a remote browser) and streams the rendered page to the victim, relaying live interactions back**. The credential and MFA entry never touches a proxied HTTP session the way classic AiTM does; the victim is interacting with a real Microsoft/SSO page that just happens to be running somewhere else.

SpyCloud first recaptured BlueKit-stolen victim data on **September 3, 2026**, then collected **~1,000 attributable messages documenting session captures against 37 organizations** — including **U.S. and EU defense contractors, law firms, healthcare providers, multinational food distributors, and construction companies** — arriving in two bursts (September 4 and September 10).

The marquee durable finding is the **persistence step**: in **38% of observed compromises BlueKit automatically enrolled its own TOTP authenticator on the victim's account** after login. That requires driving a real browser *inside* the authenticated account (consistent with the BitM architecture, which has one anyway) and leaves the attacker with **MFA-valid access that survives a password reset**. SpyCloud's remediation guidance follows directly: incident response for session-theft phishing **must audit registered MFA methods on the account — not just rotate the password and revoke active sessions** — because a kicked session with an enrolled attacker authenticator simply comes back through the front door on the next login.

## Kit capabilities (per SpyCloud)

- **Panel:** subscriptions, phishing-site creation, **automated domain purchasing and registration**, campaign management with **80+ preconfigured templates (including device-code and BitM flows)**, delivery tooling (SMS sending + an AI assistant), and victim-log tracking in one interface.
- **Visitor qualification before anything malicious is served:** custom CAPTCHAs, browser fingerprinting, **WebRTC/STUN IP enumeration**, device filtering, **RAM/CPU checks**, and IP-reputation filtering — all aimed at blocking security scanners and researchers (the same anti-scan posture this wiki notes on NovaCookies' Cloudflare gate and the RMM kit's disposable infra, now with hardware-floor checks).
- **Attribution-adjacent signals (suggestive, not proof):** the kit's CIS-country blocking filter, advertising on Russian-language forums (**XSS.is, Exploit.in, T1erOne, Lolzteam**), and consistent **Doraemon branding** across panel/website/Telegram all suggest Russian-speaking developers.

## Why BitM matters defensively

- BitM is positioned as an evasion of the **detectability of AiTM**: defender tooling and user awareness have caught up to proxy-phishing (cookie-thepin, reverse-proxy tells, TLS anomalies on lookalike hosts). A remote-rendered genuine page defeats "the login page came from the real origin in *your* browser" checks — the origin is real, the browser isn't yours.
- The **attacker-enrolled TOTP** step converts a one-time session theft into durable account ownership. Rotation workflows that don't enumerate authenticator registrations will "remediate" an account the attacker can still log into with a valid second factor.
- Same intake window shape as other campaigns: two discrete data bursts a week apart = campaign scheduling, not continuous operation — useful for correlating victim exposure windows.

## Related findings in the same SpyCloud update

- **BlgCloud leak series (PwnForums):** through August 2026, **five apparently unaffiliated actor accounts coordinated to trickle out 15+ breaches** stolen from customer instances of **BlgCloud**, a French business-management SaaS — every post titled "BLGCloud Leak #N," monetizing via unreleased-breach sales, selling "the access method," or pressuring BlgCloud itself. The pattern is the **ShinyHunters extortion model** (breach individual SaaS customer instances, pressure the provider) executed by a **coordinating group that claims no shared brand** — coordination without clout-seeking, which SpyCloud calls somewhat novel against the forum-billing backdrop.
- **LeakBase revival:** after owner "Chucky" was arrested (March 2026) and the forum seized, **LeakBase reappeared in late July 2026** under a new administrator holding **a copy of the original backend database** and administrative control of Chucky's old Telegram channels — mirroring the BreachForums→PwnForums copycat playbook (leaked backend + user base = instant forum). The new admin has released multiple unique datasets; SpyCloud assesses it is likely *not* a Russian MVD sting because a sting wouldn't keep publishing real data.

## Defender actions

1. **Add MFA-method audit to every phishing-session IR runbook:** on suspected session theft, list registered authenticator apps / TOTP seeds / FIDO2 keys on the account and remove unknown enrollments; password rotation + session revoke is incomplete remediation.
2. **Alert on MFA-enrollment events outside the user's normal change window** (new TOTP enrollment is a rare, high-signal event in most tenants).
3. Hunt the qualification-gate fingerprints: phishing landing pages that do WebRTC/STUN enumeration, RAM/CPU checks, or custom CAPTCHAs before serving content are PhaaS-qualifying visitors — treat passing such checks as an indicator the page is deliberate, not misconfig.
4. Watch for BitM copycats: BlueKit is the first kit *offering* BitM in its template menu; the architecture is serviceable by other kit developers on the same timeline the AiTM proxies were commoditized.

## Caveats

- Victimology, counts (37 orgs, ~1,000 messages, 38% TOTP enrollment) are **SpyCloud's own recaptured-data visibility**, not a global census; burst timing reflects when stolen data was posted where SpyCloud watches.
- "Only kit offering BitM" is SpyCloud's tracking statement as of September 2026.
- Russian-speaking origin is inferred from forum presence, branding, and CIS filters — suggestively-patterned, not attributed to any named group.

## Sources

- [https://spycloud.com/blog/cybercrime-update-19-bluekit-bitm-saas-breach-leakbase-return/](https://spycloud.com/blog/cybercrime-update-19-bluekit-bitm-saas-breach-leakbase-return/) — SpyCloud Labs, "BlueKit Browser-in-the-Middle, SaaS Breaches, and the Return of LeakBase" (Aurora Johnson, Kyla Cardona, Trina Lin, Paul Sansom, Trevor Hilligoss), September 15, 2026
