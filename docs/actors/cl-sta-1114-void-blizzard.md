# CL-STA-1114 / Void Blizzard

## Summary
**CL-STA-1114** is a Unit 42 activity cluster that overlaps with the actor Microsoft tracks as **Void Blizzard** and Dutch intelligence tracks as **LAUNDRY BEAR**. A July 23, 2026 joint advisory from CISA, NSA, FBI, AIVD, MIVD, and more than 20 government partners identifies the operator as Russian state-supported and also lists Proofpoint's **TA488** (formerly **UNK_PitStop**) as an overlapping industry label. The advisory warns that these names may not map one-to-one to the governments' understanding.

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
- CISA
- TA488
- UNK_PitStop
- Ulej
- Flowerbed
- Russian state-supported

## Public activity profile
- Microsoft reported global operations disproportionately focused on NATO member states and Ukraine, with government, defense, transportation, media, NGO, healthcare, education, aviation, and law-enforcement targeting.
- Earlier access relied heavily on password spraying and credentials or cookies likely acquired through commodity infostealer and criminal ecosystems.
- Microsoft observed a more targeted adversary-in-the-middle phishing path in April 2025: fake European Defense and Security Summit invitations and a typosquatted Entra sign-in page used Evilginx to capture credentials and session cookies.
- After cloud-account compromise, the actor used legitimate Exchange Online and Microsoft Graph APIs to enumerate and bulk-collect email and files. Microsoft also observed limited Teams-message access and AzureHound-based Entra ID discovery.
- Unit 42's July 2026 reporting adds a browser-resident Zimbra collection path using crafted HTML email and CVE-2025-66376, with government, defense, transportation, and financial victims across NATO states, Ukraine, CIS countries, and Africa.
- The joint advisory names the Zimbra capability Ulej and its Flowerbed collection framework. It expands confirmed targeting to the defense industrial base, federal and local government, education, energy, law enforcement, media, NGOs, and technology, and says compromised accounts distributed payloads from at least November 2025.
- Public infrastructure analysis says the actor used fabricated identities, short-lived VPSs, Mullvad VPN administration, Dockerized collection servers, and onward SSH transfer to non-public infrastructure.

## July 2026 OWAReaper expansion
Proofpoint reported that TA488 began a broader campaign on July 22, 2026 exploiting Microsoft Outlook Web Access **CVE-2026-42897**. Crafted email executes the browser-resident **OWAReaper** implant when viewed in vulnerable OWA. The malware persists through OWA `localStorage` and the offline IndexedDB cache, can steal EWS OAuth tokens through privileged add-ins, and grants Owner permission on mailbox folders to Exchange's `Default` principal. It accepts tasks through GitHub commit search or inbound email and exfiltrates over HTTPS or DNS.

Observed targeting included U.S. and European government, telecommunications, financial, hospitality, and aerospace organizations. Proofpoint assesses that zero-day exploitation before Microsoft's May 2026 patch is feasible because related infrastructure predates disclosure, but does not claim it as confirmed. This activity materially expands the actor's half-click webmail tradecraft from Zimbra to on-premises Exchange.

## Defender heuristics
- Prioritize exposed or unsupported Zimbra Classic UI deployments and patch CVE-2025-66376. Investigate crafted HTML mail that contains hidden or Base64-encoded SVG/JavaScript and CSS `@import` sanitization-bypass structures.
- Hunt for Zimbra SOAP API calls, daily `/home/~/?fmt=tgz` mailbox exports, new app-specific passwords, 2FA scratch-code access, and anomalous retrieval of 90 days of mail immediately after a message is viewed.
- Detect high-volume DNS labels or HTTPS uploads to new mail-analytics-themed domains. Correlate DNS and proxy telemetry because related samples used both channels for the same collected values.
- For Microsoft 365, monitor unusual Exchange Online or Graph bulk collection, non-owner mailbox access, Teams web-client access, AzureHound-like tenant enumeration, impossible travel, unfamiliar session cookies, and sign-ins following infostealer detections.
- Resetting the primary password alone may be insufficient. Revoke sessions, app-specific passwords, 2FA recovery codes, OAuth grants, and other durable authentication material after confirmed compromise.
- Preserve Zimbra-origin browser local storage and hunt `zd_comp_YYYY-MM-DD` keys before cleanup; these can identify affected users and help estimate which mailbox days Ulej attempted to export.
- For Exchange, patch CVE-2026-42897; preserve and inspect `PageDataPayload.OwaUserDefaultSettings` and `owa_offline_db`; revoke affected EWS tokens; and remove unauthorized Owner grants to the `Default` principal across all mailbox folders.

## Attribution notes
The multi-government advisory identifies the operator as Russian state-supported and lists LAUNDRY BEAR, Void Blizzard, CL-STA-1114, and TA488 as overlapping public labels, but explicitly cautions against assuming a one-to-one mapping. Seqrite's March 2026 Operation GhostMail report assessed a related Ukrainian Zimbra case as APT28 with medium confidence based on technical and targeting overlaps. Retain source-specific labels rather than treating every name as a universal alias.

## Related pages
- [TA488 OWAReaper and CVE-2026-42897 exploitation](../ops/ta488-owareaper-owa-cve-2026-42897.md)
- [OWAReaper](../tools/owareaper.md)
- [CL-STA-1114 Zimbra webmail espionage](../ops/cl-sta-1114-zimbra-webmail-espionage.md)
- [Ulej / Flowerbed](../tools/ulej-flowerbed.md)
- [UNK_MassTraction Roundcube university mailserver campaign](../ops/unk-masstraction-roundcube-university-mailserver-campaign.md)
- [Russian intelligence Signal backup-key phishing](../ops/russian-intelligence-signal-backup-key-phishing.md)

## Sources
- Proofpoint Threat Research: [Cleaning Out Inboxes: TA488 Comes for Outlook with Another Half-Click Exploit](https://www.proofpoint.com/us/blog/threat-insight/cleaning-out-inboxes-ta488-comes-outlook-another-half-click-exploit)
- CISA et al.: [AA26-204A — Russian State-Supported Cyber Actors Conduct Phishing Campaign Targeting Users of Zimbra Collaboration Suite](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-204a)
- Unit 42: [Russian Global Webmail Espionage](https://unit42.paloaltonetworks.com/russian-webmail-espionage/)
- Microsoft Security Blog: [New Russia-affiliated actor Void Blizzard targets critical sectors for espionage](https://www.microsoft.com/en-us/security/blog/2025/05/27/new-russia-affiliated-actor-void-blizzard-targets-critical-sectors-for-espionage/)
- Seqrite Labs: [Operation GhostMail: Russian APT exploits Zimbra Webmail to Target Ukraine State Agency](https://www.seqrite.com/blog/operation-ghostmail-zimbra-xss-russian-apt-ukraine/)
