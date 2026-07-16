# O-UNC-066 Entra passkey vishing

## Summary
Okta Threat Intelligence's July 2026 report describes **O-UNC-066** using a panel-controlled phishing kit against Microsoft 365 users' **Microsoft Entra passkey enrollment** flow. Since April 2026, the cluster has registered passkey-themed domains, called targeted users, and steered them through Microsoft-branded enrollment pages while the operator attempts to register an attacker-controlled passkey on the victim's account.

Okta links O-UNC-066 to the data-leak site named **Pink**, which Unit 42 reports as **CL-CRI-1147**. Observed targeting includes food and beverage, technology, healthcare, automotive, construction, and aviation organizations, with data extortion assessed as the primary motive.

## Tags
- ops
- phishing
- vishing
- identity-first intrusion
- Microsoft 365
- Microsoft Entra ID
- passkeys
- FIDO2
- account takeover
- data extortion
- O-UNC-066
- Pink
- CL-CRI-1147
- Okta Threat Intelligence
- The Hacker News

## Why this matters
- Passkey rollout is becoming a realistic social-engineering pretext: Microsoft Entra registration campaigns can nudge users to enroll passkeys, and attackers can mimic that expected change.
- This is not classic credential phishing or transparent AiTM token proxying. The operator's goal is to trick the user into approving or cooperating with a live **authentication-method enrollment** that grants the attacker durable account access.
- Helpdesk, identity, and SOC teams need playbooks for unexpected passkey / FIDO2 registration, not only password resets and MFA fatigue.
- The campaign shows that stronger authentication can still be abused when enrollment governance and user-verification processes are weak.

## Reported tradecraft
- Operators register domains containing the word `passkey` and use phone calls to convince targets that passkey setup is required.
- The phishing kit creates per-target subdomains that mimic Microsoft Entra login pages and use the victim organization's legitimate branding.
- Generic Microsoft styling is loaded from Microsoft's CDN, while organization-specific logos and backgrounds are staged by the phishing backend.
- Okta reports the kit is **not** a transparent adversary-in-the-middle proxy and did not redirect to a federated identity provider during analysis.
- The operator can control the victim's page flow in real time and request additional verification steps such as push MFA number matching or SMS OTP.
- Recreated flow paths include `/gate` for loading / anti-analysis checks and `/identify` for username collection.
- Later passkey-themed pages ask the user to save a fake “recovery key” made from attacker-controlled BIP-39-style phrases and then verify the final word at `/passkey/check`; Okta assesses this as likely sleight-of-hand to keep the user occupied while the attacker enrolls their own passkey.

## Defensive guidance
- Alert on new passkey / FIDO2 / authentication-method registrations followed by mailbox, OneDrive, SharePoint, Teams, Salesforce, or admin-console access from unfamiliar devices, networks, or geographies.
- Require phishing-resistant, helpdesk-resistant enrollment controls: privileged users should enroll passkeys only from managed devices, trusted networks, or in supervised enrollment sessions.
- Treat unsolicited “passkey enrollment” phone calls as suspicious. Publish a known-good enrollment path and tell users that identity staff will not ask them to visit third-party passkey domains.
- Review Entra audit logs for authentication method additions, especially passkey/FIDO2 additions during or immediately after vishing reports.
- Correlate helpdesk tickets, phone-call reports, sign-in risk, MFA prompts, and authentication-method changes for the same user in short time windows.
- For suspected compromise, revoke sessions, remove unfamiliar authentication methods, reset credentials as needed, review OAuth grants and mailbox rules, and investigate downstream SaaS access.
- During passkey rollout, run user education that explicitly distinguishes legitimate Entra registration prompts from phone-driven enrollment on lookalike domains.

## Related pages
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)
- [UNC3753 law-firm vishing extortion campaign](../actors/unc3753.md)

## Sources
- [Okta Threat Intelligence](https://www.okta.com/blog/threat-intelligence/vishing-actors-target-microsoft-entra-passkey-enrollment-/)
- [The Hacker News](https://thehackernews.com/2026/07/hackers-use-fake-microsoft-entra.html)
