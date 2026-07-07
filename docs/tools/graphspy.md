# GraphSpy

## Summary

**GraphSpy** is a public Microsoft Graph / Microsoft 365 post-exploitation tool referenced by ZeroBEC in its July 2026 DEBULL device-code phishing report. ZeroBEC observed a post-authentication tenant artifact named `GraphSpy-Device` after a victim completed a Microsoft Authentication Broker device-code flow, and assessed with high probability that the DEBULL tooling layer uses GraphSpy or a GraphSpy-derived workflow for Microsoft 365 and Entra post-exploitation.

Treat GraphSpy indicators as cloud-identity compromise evidence. The relevant intrusion path is not endpoint malware first; it is OAuth token issuance through a legitimate identity-provider flow followed by Microsoft Graph access, device registration, mailbox / file / collaboration access, and possible persistence through app or device artifacts.

## Tags

- tools
- cloud tooling
- Microsoft Graph
- Microsoft 365
- Entra ID
- OAuth
- device-code phishing
- GraphSpy
- DEBULL
- post-exploitation
- token theft
- cloud identity
- ZeroBEC

## Observed use

ZeroBEC's DEBULL report links GraphSpy to a late-June / early-July 2026 Microsoft 365 phishing campaign:

- A DEBULL landing page generated Microsoft Authentication Broker device codes and pushed the victim to Microsoft's legitimate device-login page.
- The attacker received a valid Microsoft 365 session after the victim entered the code and completed MFA.
- A post-authentication device object named `GraphSpy-Device` appeared in the tenant.
- ZeroBEC connected that artifact, the Authentication Broker flow, attacker session handoff, and public GraphSpy capabilities to assess GraphSpy or a GraphSpy-derived workflow with high confidence.

## Defender pivots

- Search Entra ID device and audit logs for `GraphSpy-Device` and unexpected device registrations near Microsoft Authentication Broker / device-code sign-ins.
- Correlate GraphSpy-like artifacts with Microsoft Graph API usage, mailbox access, OneDrive / SharePoint downloads, Teams access, OAuth consent changes, and suspicious OfficeHome / Outlook Web sessions.
- Investigate successful MFA events that follow unsolicited document, meeting, shared-folder, or secure-message lures asking users to enter a code at `microsoft.com/devicelogin`.
- Revoke refresh tokens and active sessions for affected accounts; Graph-based post-exploitation can continue after password reset if tokens remain valid.
- Preserve sign-in, audit, device, app-consent, mailbox, Graph API, and web-proxy logs before tenant retention windows roll over.

## Related pages

- [DEBULL device-code phishing and GraphSpy post-exploitation](../ops/debull-device-code-phishing-graphspy.md)
- [Kali365 device-code phishing expansion](../ops/kali365-device-code-phishing-expansion.md)
- [ROADtools](roadtools.md)

## Sources

- ZeroBEC, DEBULL: Storm-2372-Style Microsoft Device-Code Phishing With GraphSpy Post-Exploitation: https://zerobec.com/blog/debull-storm-2372-microsoft-device-code-phishing-graphspy
- The Hacker News summary: https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html
