# High-volume Microsoft 365 outage-lure phishing wave (November 13, 2026)

On November 13, 2026 a coordinated, high-volume phishing wave sprayed organizations across multiple sectors worldwide with emails disguised as **Microsoft 365 service-health notifications**: your messages were held during an outage and will be **deleted in 24 hours** unless you click RESTORE MESSAGES. Microsoft Security Research published the write-up on November 16 and left the honest verdict on the record: this is *likely* credential phishing, but the available evidence did **not** confirm credential capture, malware delivery, or post-compromise activity, and no named actor was attributed.

This page exists because the wave is a durable defensive pattern, not because it is dramatic: **outage-lure phishing weaponizes whatever news cycle is live**, and a Microsoft 365 disruption is a force multiplier for credential urgency. The public IOCs below are the triage set. If a similar wave rides the next headline, the grammar here transfers even though the domains will not.

## The anatomy (from the published samples)

- **Pretext:** claimed Exchange Online incident on November 12; "four messages were held after the outage"; 24-hour deletion deadline; prominent RESTORE MESSAGES call to action.
- **Subject pattern:** `Outage – <random token>` (randomized subjects defeat subject-matching rules).
- **Display names:** a three-character, organization-style prefix + `Outage Notification` or `Service Health`.
- **Sender domains (three observed):** `moments-notice[.]com`, `planetmaison[.]com`, `newbooker[.]com`.
- **Destination:** recipient-specific tracking URLs from email-delivery/link-tracking infrastructure converging on a **common non-Microsoft destination**: `reallifeaccounting[.]com`, including the path `/themelist0.html`.
- **Payload state:** link-based only; no QR codes, no attachments, no observed malware delivery; Microsoft did not obtain final-page source or credential-submission telemetry.

## Why it works, and where the tells are

The lure is *plausible logistics* - during a real service disruption, held-message restore notices are exactly what users expect, so the 24-hour deadline rides a wave of genuine inbox confusion. The tells are structural, not tonal:

1. **The sender domain is never Microsoft.** `moments-notice.com`, `planetmaison.com`, `newbooker.com` have no Microsoft relationship; the display name carries the brand, the envelope carries nothing.
2. **Recipient-specific tracking links from third-party senders.** Legitimate Microsoft service health flows through Microsoft domains and the admin center, not through generic email-marketing trackers and a small-business-looking landing domain.
3. **The destination is a single shared host across "distinct" campaigns.** Multiple sender domains funneling to one destination (`reallifeaccounting[.]com`) is campaign plumbing, not coincidence.

## What to do

- **Hunt the IOCs historically and forward:** sender domains `moments-notice[.]com`, `planetmaison[.]com`, `newbooker[.]com`; destination `reallifeaccounting[.]com` (any path, incl. `/themelist0.html`); subject regex `Outage\s*[-–]\s*[A-Za-z0-9]+`; display-name regex `^... (Outage Notification|Service Health)$`.
- **Treat clicks as the triage boundary.** Microsoft confirmed no credential-capture telemetry; if your users clicked, the incident is a *possible* exposure - reset creds, revoke sessions, audit inbox rules and OAuth grants for anyone who may have submitted on the destination page.
- **Pre-wire the next wave.** Outage-lure waves arrive within days of any major provider disruption. Have the mailbox-level search and block playbook ready before the next headline, and make sure users are told what a *real* service-health notice looks like (admin center + Microsoft domains, no delete-deadline countdown).
- **Defender/Defender for Office 365 blocked the campaign domains at publication** (per Microsoft); quote the block state with the read-time.

## Durable reads

- **An outage is a phishing force multiplier.** Held-message + deletion-deadline pretexts spike whenever a major platform degrades; your next wave will reuse this grammar with fresh domains.
- **Randomized subjects and distinct sender domains defeat pattern matching; the shared destination does not.** Hunt convergence points, not per-message cosmetics.
- **Publishing an unconfirmed campaign is still useful intelligence.** "Likely credential phishing, capture unconfirmed, no attribution" is the honest shape of most phishing intel - defend on the observable structure, and reserve incident escalation for confirmed telemetry.

## Monitor

- Whether any named actor or follow-on BEC activity attaches to the November 13 wave (Microsoft promised continued monitoring).
- Domain re-registration/rotation around `reallifeaccounting[.]com` (infrastructure reuse is the pivot if it appears in later waves).
- KEV/other feeds: no related entry (`2026.11.17`/`1,782` grep `0` for the three sender domains and the destination).

*Source: Microsoft Security Blog, "High volume phishing campaign uses Microsoft 365 outage lures to target multiple industry sectors" (Nov-16, Jasmin/Armer/Kale), fetched `200` by this wiki Nov-18 `≈00:4xZ`. IOCs quoted verbatim from the post in defanged form.*
