# CL-STA-1114 / Void Blizzard

## Summary
**CL-STA-1114** is a Unit 42 activity cluster that overlaps with the Russia-affiliated actor Microsoft tracks as **Void Blizzard** and Dutch intelligence tracks as **LAUNDRY BEAR**. Unit 42 reported in July 2026 that the cluster had operated since at least 2024 and had targeted vulnerable Zimbra Collaboration Suite webmail since July 2025.

Microsoft independently described Void Blizzard in May 2025 as a Russia-affiliated espionage actor active since at least April 2024. Its broader operations target organizations important to Russian strategic objectives, especially NATO members and Ukraine, and collect large volumes of email and files. Treat the naming as an assessed overlap rather than a universal one-to-one alias: Unit 42 used overlap language, while earlier Seqrite analysis attributed one technically related Zimbra campaign to APT28 with medium confidence.

## Tags
- groups
- CL-STA-1114
- Void Blizzard
- LAUNDRY BEAR
- Russia-affiliated
- cyberespionage
- Zimbra
- webmail
- CVE-2025-66376
- credential theft
- mailbox theft
- government targeting
- defense
- transportation
- financial sector
- NATO
- Ukraine
- CIS
- Africa
- Microsoft
- Unit 42

## Public activity profile
- Microsoft reported global operations disproportionately focused on NATO member states and Ukraine, with government, defense, transportation, media, NGO, healthcare, education, aviation, and law-enforcement targeting.
- Earlier access relied heavily on password spraying and credentials or cookies likely acquired through commodity infostealer and criminal ecosystems.
- Microsoft observed a more targeted adversary-in-the-middle phishing path in April 2025: fake European Defense and Security Summit invitations and a typosquatted Entra sign-in page used Evilginx to capture credentials and session cookies.
- After cloud-account compromise, the actor used legitimate Exchange Online and Microsoft Graph APIs to enumerate and bulk-collect email and files. Microsoft also observed limited Teams-message access and AzureHound-based Entra ID discovery.
- Unit 42's July 2026 reporting adds a browser-resident Zimbra collection path using crafted HTML email and CVE-2025-66376, with government, defense, transportation, and financial victims across NATO states, Ukraine, CIS countries, and Africa.

## Defender heuristics
- Prioritize exposed or unsupported Zimbra Classic UI deployments and patch CVE-2025-66376. Investigate crafted HTML mail that contains hidden or Base64-encoded SVG/JavaScript and CSS `@import` sanitization-bypass structures.
- Hunt for Zimbra SOAP API calls, daily `/home/~/?fmt=tgz` mailbox exports, new app-specific passwords, 2FA scratch-code access, and anomalous retrieval of 90 days of mail immediately after a message is viewed.
- Detect high-volume DNS labels or HTTPS uploads to new mail-analytics-themed domains. Correlate DNS and proxy telemetry because related samples used both channels for the same collected values.
- For Microsoft 365, monitor unusual Exchange Online or Graph bulk collection, non-owner mailbox access, Teams web-client access, AzureHound-like tenant enumeration, impossible travel, unfamiliar session cookies, and sign-ins following infostealer detections.
- Resetting the primary password alone may be insufficient. Revoke sessions, app-specific passwords, 2FA recovery codes, OAuth grants, and other durable authentication material after confirmed compromise.

## Attribution notes
Unit 42 says CL-STA-1114 **overlaps** Void Blizzard / LAUNDRY BEAR. Microsoft assesses Void Blizzard is Russia-affiliated with high confidence. Seqrite's March 2026 Operation GhostMail report assessed a related Ukrainian Zimbra case as APT28 with medium confidence based on technical and targeting overlaps. The public reports therefore support Russia-linked clustering but do not resolve the actor identity conclusively; defenders should retain the source-specific labels.

## Related pages
- [CL-STA-1114 Zimbra webmail espionage](../ops/cl-sta-1114-zimbra-webmail-espionage.md)
- [UNK_MassTraction Roundcube university mailserver campaign](../ops/unk-masstraction-roundcube-university-mailserver-campaign.md)
- [Russian intelligence Signal backup-key phishing](../ops/russian-intelligence-signal-backup-key-phishing.md)

## Sources
- Unit 42: [Russian Global Webmail Espionage](https://unit42.paloaltonetworks.com/russian-webmail-espionage/)
- Microsoft Security Blog: [New Russia-affiliated actor Void Blizzard targets critical sectors for espionage](https://www.microsoft.com/en-us/security/blog/2025/05/27/new-russia-affiliated-actor-void-blizzard-targets-critical-sectors-for-espionage/)
- Seqrite Labs: [Operation GhostMail: Russian APT exploits Zimbra Webmail to Target Ukraine State Agency](https://www.seqrite.com/blog/operation-ghostmail-zimbra-xss-russian-apt-ukraine/)
