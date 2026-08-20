# Trusted collaboration-channel identity abuse

## Summary

Unit 42 (August 20, 2026) reports that threat actors now routinely misuse enterprise collaboration platforms — Microsoft Teams, Slack, and similar — as the trusted channel for identity phishing, impersonation, credential theft, malware delivery, and social engineering. Over the last 12 months, Unit 42's endpoint alerts of malicious activity associated with collaboration tools **more than quadrupled**, and **99% of those alerts relate to chat phishing operations**: attackers compromise an account (or an external federated tenant, guest account, or trusted third-party relationship), then operate *inside* the authenticated platform so that malicious activity looks like normal collaboration.

The durable pattern: **the authenticated channel itself is the trust transference primitive.** A request that would look suspicious in an unsolicited email looks routine when it arrives from a known contact's Teams chat, a branded Slack workspace, or a platform notification — so MFA approvals, credential hand-offs, remote-access installs, and file opens happen without the scrutiny email phishing gets.

## Tags
- patterns
- collaboration platforms
- collaboration-tool phishing
- identity phishing
- social engineering
- credential theft
- impersonation
- MFA fatigue
- remote access software
- DLL sideloading
- Slack webhook
- SaaS

## Operational shape

### Initial access: in-channel identity phishing
- Attackers initiate chat from external tenants, compromised accounts, guest accounts, or trusted partner relationships, then drive the victim toward MFA approval, credential harvesting, remote-assistance install, or a file transfer.
- Unlike email, the channel is interactive: the attacker can answer follow-up questions in real time and adapt the social engineering to the target.
- Example process tree: a Teams chat RAR transfer → victim extracts with WinRAR → `lpk.dll` (a known, older malicious language-pack DLL) runs via DLL sideloading. Older, well-known families are deliberately reused because the delivery channel, not the malware, is the novelty.

### Impersonation through staged collaboration environments
- **Recruitment-themed campaign (January 2026, Fireblocks disclosure):** attackers impersonated Fireblocks executives and recruiters, ran professional Google Meet interviews, then assigned a "code review" task — clone a GitHub repo and run `npm install` — executing malware. Fireblocks assessed the activity as closely aligned with the North Korea-linked **Contagious Interview** pattern.
- **Staged Slack workspace against the Axios npm maintainer (March 2026):** the attacker created a convincing Slack environment with company branding, channels, users, and message history, impersonating a legitimate company; the interaction moved to a staged Teams meeting where the maintainer was talked into installing software that delivered a RAT. The attacker then accessed the maintainer's npm account and **published two poisoned Axios versions** whose projects retrieve and execute a malicious dependency.
- **Linux Foundation TODO Group Slack campaign (April 2026, OpenSSF report):** impersonation of a known community leader via Slack DMs, with a Google Sites link leading to a fraudulent Google Workspace authentication flow (email + verification code), a malicious root-certificate install, and on macOS a binary download that could provide system access.

### Persistence: SaaS integrations as exfiltration and MFA-disablement channel
- CERT Polska investigated a December 2025 intrusion at a Polish manufacturing company where the threat actor modified compromised **firewall-VPN appliances**: weekly scheduled tasks using the appliance's built-in scripting retrieved a privileged identity's password, disabled 2FA for the privileged account, and **used the appliance's native Slack notification capability (webhook to `hooks.slack[.]com`) to exfiltrate the results** to an attacker-controlled channel — combining persistence, credential theft, and MFA removal with a legitimate SaaS integration, no separate exfil tooling.
- Perimeter visibility: many VPN/security appliances sit behind a separate perimeter firewall and send outbound webhook requests through the enterprise egress path.

### MITRE mapping (per Unit 42)
- Initial access: Phishing (T1566) — identity phishing through external collaboration channels.
- Stealth: Impersonation (T1684.001) — legitimate platform notifications, hosted content, direct messages.
- Persistence: Modify Authentication Process (T1556) — MFA removal and privileged-credential exfiltration through a native Slack webhook integration.

## Defender heuristics
- **Reduce exposure:** review external federation, guest access, and third-party integrations; allow-list external tenants; periodically review and prune guest accounts.
- **Behavioral correlation after authentication:** alert when an external/low-trust collaboration contact is followed by MFA approvals, risky sign-ins, device registration, new OAuth consent, unusual file sharing, or new external-tenant communications.
- **Webhook egress triage:** flag unexpected `hooks.slack[.]com` (or Teams incoming-webhook) POSTs, unusual user agents, and webhook activity from systems without an approved Slack/Teams integration — especially from VPN/security appliances.
- **Verification policy:** security-sensitive requests (MFA approval, RAS install, credential sharing, file transfer, access changes) require out-of-band verification through a known secondary channel; train users that collaboration messages carry the same trust risk as email.
- **Maintainer targeting:** the Axios case shows maintainer impersonation can convert directly into registry publishing access — treat unexpected Slack/Teams recruitment or vendor outreach toward open-source maintainers as high-risk social engineering, and correlate maintainer account activity (new releases, dependency changes) with any prior impersonation attempts.

## Related pages
- [Microsoft Teams external-chat phishing](microsoft-teams-external-chat-phishing.md) — the Teams-specific slice of this pattern (external-tenant lures, MFA-fatigue asks, Cloaked Ursa / UNC6692 examples)
- [BlackFile / UNC6671 vishing extortion operation](../ops/blackfile-unc6671-vishing-extortion.md) — identity-first vishing with SaaS pivots
- [Kali365 device-code phishing expansion](../ops/kali365-device-code-phishing-expansion.md) — device-code PhaaS lures across Microsoft / Okta / MAX Messenger
- [Microsoft Q2 2026 email and Teams phishing landscape](../ops/microsoft-q2-2026-email-teams-phishing-landscape.md) — Teams vishing growth and post-disruption activity measurements
- [DeBULL device-code phishing and GraphSpy](../ops/debull-device-code-phishing-graphspy.md) — post-authentication Graph / M365 artifacts

## Sources
- Unit 42: [Identity Abuse Through Trusted Communication Channels](https://unit42.paloaltonetworks.com/communication-channel-identity-risks/) — August 20, 2026 (alert-trend data, MITRE mapping, Fireblocks / Axios maintainer / Linux Foundation examples, CERT Polska Slack-webhook persistence case, defender recommendations)
- Cross-referenced primary disclosures cited by Unit 42: Fireblocks recruitment-campaign disclosure (January 2026), Okta Threat Intelligence Slack-workspace phishing, OpenSSF Linux Foundation TODO Group campaign report (April 2026), CERT Polska December 2025 appliance intrusion.
