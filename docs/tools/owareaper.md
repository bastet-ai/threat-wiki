# OWAReaper

## Summary
**OWAReaper** is a browser-resident JavaScript espionage implant that Proofpoint observed TA488 deploying through **CVE-2026-42897** in Microsoft Outlook Web Access in July 2026. It is an evolution of the actor's ZimReaper webmail payload, but replaces broad mailbox export with subtler credential, token, state, command-execution, and persistence functions.

## Tags
- tools
- malware
- OWAReaper
- TA488
- JavaScript malware
- browser-resident malware
- Outlook Web Access
- Microsoft Exchange Server
- CVE-2026-42897
- localStorage
- IndexedDB
- OAuth token theft
- EWS
- mailbox permission abuse
- GitHub dead drop
- DNS exfiltration
- persistence
- cyberespionage

## Capabilities
- Executes entirely in the authenticated OWA reading-pane context.
- Removes exploit content by rewriting the delivery message through Outlook APIs.
- Captures identity and OWA settings and places invisible fields in the DOM to solicit browser-autofilled credentials.
- Stores an encrypted implant and wrapper in `PageDataPayload.OwaUserDefaultSettings`, abusing `OwaFrontendSyncState` restoration for execution whenever OWA opens.
- Poisons messages in `owa_offline_db` with hidden iframes for cache-based reinfection.
- Uses qualifying `ReadWriteMailbox` add-ins to call `GetClientAccessToken` and steal EWS OAuth tokens.
- Grants Owner access on every folder to Exchange's `Default` principal.
- Pulls encrypted `code`, `domn`, and `cmnd` tasks from GitHub commit search or attacker-sent email.
- Exfiltrates through HTTPS/CDN relays or Base32-shaped DNS labels.

## Defensive priorities
- Treat the Exchange mailbox, browser-origin state, and add-in token plane as compromised together; an endpoint-only rebuild is incomplete.
- Preserve and inspect `PageDataPayload.OwaUserDefaultSettings` and `owa_offline_db` before cleanup.
- Audit all folder permissions for unauthorized rights assigned to `Default` and revoke affected EWS tokens.
- Detect `/assets/v1_` requests through image CDNs, named diagnostic/output file posts, suspicious GitHub commit search containing user addresses, and DNS labels to the published actor domains.

## Related pages
- [TA488 OWAReaper and CVE-2026-42897 exploitation](../ops/ta488-owareaper-owa-cve-2026-42897.md)
- [CL-STA-1114 / Void Blizzard](../actors/cl-sta-1114-void-blizzard.md)
- [Ulej / Flowerbed](ulej-flowerbed.md)

## Sources
- Proofpoint Threat Research: [Cleaning Out Inboxes: TA488 Comes for Outlook with Another Half-Click Exploit](https://www.proofpoint.com/us/blog/threat-insight/cleaning-out-inboxes-ta488-comes-outlook-another-half-click-exploit)
