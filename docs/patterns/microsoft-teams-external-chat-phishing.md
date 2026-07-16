# Microsoft Teams external-chat phishing

## Summary

Unit 42 reports that threat actors are increasingly using Microsoft Teams and other collaboration tools as phishing delivery paths because users often trust chat tools more than email. In the first four months of 2026, Unit 42 says collaboration-tool phishing alerts represented 42% of phishing alerts in Cortex, up from 30% in the preceding four months.

The durable pattern is not a single malware family: external chat, open federation, typosquatted Microsoft 365 tenants, and compromised partner accounts can make an unsolicited "IT support" message look operationally normal enough to drive MFA approval, credential reset, device registration, malware download, or remote-assistance abuse.

## Tags
- patterns
- Microsoft Teams
- collaboration-tool phishing
- social engineering
- identity security
- MFA fatigue
- external federation
- typosquatting
- Cloaked Ursa
- UNC6692

## Operational shape

### Initial contact
- Attackers initiate Microsoft Teams chats from external tenants, unmanaged / personal Teams accounts, typosquatted domains, or compromised service-provider / partner accounts.
- Tenant and display names may mimic IT support, security teams, managed service providers, or trusted vendors.
- The chat request can appear directly in an employee's Teams feed. Teams can show external-sender and impersonation warnings, but the user still has to decide whether to accept the contact.

### Social-engineering asks
- Unit 42's example lure poses as IT and claims an account anomaly, then asks the user to approve an MFA prompt.
- Similar collaboration-tool flows can push users to credential-harvesting pages, mailbox-repair pages, remote-assistance sessions, local "security" tools, or device-registration steps.
- The value to the attacker is trust transference: a message inside Teams can feel closer to internal operations than a traditional email lure.

### Public actor examples
- Unit 42 cites Cloaked Ursa / APT29 / Cozy Bear / Midnight Blizzard use of Microsoft Teams messages from compromised accounts that linked to Microsoft-themed credential-harvesting pages.
- Unit 42 also cites Mandiant's December 2025 UNC6692 reporting, where actors impersonated IT helpdesk staff over Teams and pushed victims into a fake Microsoft mailbox-repair flow.

## Defender heuristics

### Reduce exposure before the user sees the lure
- Review whether unmanaged or personal Teams accounts can initiate chats with internal users. Disable this path if there is no clear business need.
- Review Teams federation. Prefer an allow-list of approved external domains over open communication with any external Microsoft 365 tenant.
- Treat newly seen external tenants, typosquatted domains, and tenant names resembling IT / security / MSP functions as higher-risk senders.

### Identity and endpoint correlation
- Alert when an external Teams chat is followed by MFA approvals, risky sign-ins, device registration, Conditional Access failures, password resets, or new OAuth consent.
- Correlate collaboration-tool contact with remote-assistance launches, downloads from Microsoft-themed pages, AutoHotKey / script execution, browser-extension installation, or new local HTTP listeners.
- Require compliant devices, phishing-resistant MFA where possible, and just-in-time privileged access for high-impact actions so one accepted chat cannot become broad access.

### User-reporting and response
- Train users that Teams messages can be external and should not be trusted simply because they appear in a collaboration feed.
- Give users a supported way to report suspicious Teams messages, similar to email phishing reporting.
- When malicious chats are confirmed, remove them from user views where licensing and administrative controls allow, then review all users who accepted or interacted with the sender.

## Related pages
- [UNC6692 SNOW malware social-engineering campaign](../ops/unc6692-snow-malware-social-engineering.md)
- [APT29](../actors/apt29-cozy-bear-midnight-blizzard.md)
- [Kali365 device-code phishing expansion](../ops/kali365-device-code-phishing-expansion.md)
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md)

## Sources
- [Unit 42](https://unit42.paloaltonetworks.com/microsoft-teams-phishing/)
