# TheHatman: Microsoft Entra tenant credential-theft and forum sale claims

## Summary

Unit 42's "Mitigating Large-Scale Credential Attacks" threat brief (updated August 18, 2026) added a new entry for an actor operating under the handle **TheHatman** (also written "The Hatman"). From **August 1 to August 17, 2026**, the actor made posts across multiple forums offering to sell employee information for multiple enterprises. TheHatman alleges the data was exfiltrated from organizations' **Microsoft Entra tenants** and claims the access was gained through compromised credentials obtained via **MFA fatigue** and **password spraying**. The activity was publicly reported as early as August 16, 2026. The brief names no victims and states that TheHatman claims to hold sensitive or confidential information from several high-profile organizations. **Unit 42 has not verified these claims or identified a specific intrusion vector.**

This is an unverified, forum-claimed credential-theft operation, not a confirmed intrusion. The durable value is the tradecraft pattern: Entra tenant data as a marketable product, with MFA fatigue plus password spraying as the claimed acquisition vector — and the need to distinguish claimed theft from validated compromise.

## Tags

- credential theft
- password spraying
- MFA fatigue
- Microsoft Entra
- identity attack
- cybercrime forum
- TheHatman
- threat brief

## Why this matters

- Identity is the perimeter: the actor's product is access to Entra tenant employee data, sold directly on criminal forums — a monetization path that follows the same logic as FortiBleed's credential harvest.
- The claimed vector (MFA fatigue + password spraying against the tenant) is a well-known, low-tech path that most tenants can suppress with the right policy controls. Even if the specific claims are unverified, defenders should be able to produce evidence that they are not the source of any such data.
- Forum sales of "Entra tenant data" are increasingly used as leverage or extortion pre-staging. A public claim of theft against your organization is itself an event worth logging and responding to.

## Reported activity

- **August 1–17, 2026**: TheHatman posts across multiple forums offering to sell employee information for multiple enterprises.
- **August 16, 2026**: The activity is publicly reported; Unit 42 publishes initial guidance through social media.
- **August 18, 2026**: Unit 42 folds TheHatman into the "Mitigating Large-Scale Credential Attacks" brief alongside the FortiBleed campaign, with a shared recommendation to audit remote-access logs for successful logins shortly after large-volume password-failure events.
- TheHatman claims the data was obtained from Microsoft Entra tenants using compromised credentials gained through MFA fatigue and password spraying. No intrusion vector has been independently verified.

## Claims versus evidence

- **Claimed**: large-volume Entra tenant credential/employee-data theft across multiple high-profile organizations; sale of that data on forums; MFA fatigue and password spraying as the access path.
- **Not verified**: any specific victim, any intrusion vector, any sample of the allegedly stolen data. Treat all of TheHatman's claims as unconfirmed until corroborated by victim telemetry or enforcement action.
- The forum-handle persona ("TheHatman") may be marketing, not operator identity. Do not treat the handle as an attribution.

## Indicators and hunting pivots

- No public IOCs are published in the brief. Pivots are behavioral and identity-centric:
- Successful MFA fatigue events: clusters of MFA push notifications (or phishing-resistant MFA prompts) to a single user, especially with acceptance followed by sign-in from an unusual location or new device.
- Password spraying against the tenant: broad low-and-slow password failures across many accounts, followed by a small number of successes; correlate successes to the failure window.
- New device registration, new sign-in location, first-time device, or new application consent shortly after either pattern.
- Identity-token activity after anomalous sign-in: token issuance (including device-code or PRT issuance), privileged role grants, directory read/export activity, or mailbox access.
- Dark-web / forum monitoring: forum posts offering to sell "Microsoft Entra" or tenant employee data; use the claimed data shape (employee directory data, not raw password hashes) as the validation artifact — request samples where the claim concerns your tenant.

## Defender actions

- Require phishing-resistant MFA (FIDO2/passkey) and limit or monitor MFA prompt volume; MFA fatigue collapses when the prompt surface is phishing-resistant.
- Enforce risk-based Conditional Access that blocks or challenges sign-ins from anonymous/low-trust networks and unusual locations; require device compliance or hybrid join for directory-sensitive access.
- Audit remote-access and identity logs for successful logins shortly after large password-failure events — the specific Unit 42 recommendation for this brief.
- Hunt device-code phishing flows (device-code sign-in followed by new device registration), which is the most common MFA-bypass path that pairs with password spraying for Entra access.
- If your organization is named or plausibly implicated in forum posts: treat it as an incident trigger. Pull the last 30–90 days of sign-in, audit-log, and device-registration history; check token lifetime and PRT issuance; reset privileged credentials; and verify no directory export (e.g., `Directory.Read.All` grants, mailbox forwarding rules) correlates with the claimed window.
- Do not publish or amplify unverified victim names from the brief.

## Open questions

- Which organizations are actually implicated, and can any produce telemetry confirming or refuting tenant access during August 1–17?
- Does TheHatman sell raw directory data, token access, or live account access, and at what volume — the answer determines the response posture.
- Is TheHatman the same operator behind any of the credential-spray operations already tracked in this wiki (FortiBleed's post-compromise credential list, or earlier Entra spray campaigns)?
- Will law enforcement or Microsoft confirm any victim set?

## Related pages

- [FortiBleed Fortinet credential-exposure campaign](../ops/fortibleed-fortinet-credential-exposure.md)
- [Entra ID rogue device registration and AI-generated identifiers](../patterns/entra-rogue-device-registration-ai-identifiers.md)
- [DeBull device-code phishing and GraphSpy](../ops/debull-device-code-phishing-graphspy.md)
- [Kali365 device-code phishing expansion](../ops/kali365-device-code-phishing-expansion.md)

## Sources

- Unit 42: [Threat Brief: Mitigating Large-Scale Credential Attacks (Updated August 18)](https://unit42.paloaltonetworks.com/large-scale-credential-attacks/)
