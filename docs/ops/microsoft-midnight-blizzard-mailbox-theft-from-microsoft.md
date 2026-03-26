# Microsoft Midnight Blizzard mailbox theft from Microsoft

## Summary
In January 2024, Microsoft disclosed that Midnight Blizzard had accessed Microsoft corporate email accounts. Microsoft said the intrusion was part of a nation-state attack and that the threat actor used the access to review mailbox content and target additional organizations.

## Scope
This page covers the Microsoft-disclosed mailbox theft and the immediate public response, not the entire history of APT29 activity.

## Timeline
- **2024-01-12** — Microsoft detected a nation-state intrusion in corporate systems and began response actions.
- **2024-01-25** — Microsoft published responder guidance and identified the actor as Midnight Blizzard, also known as NOBELIUM.
- **2024-10-29** — Microsoft reported additional Midnight Blizzard spear-phishing activity using signed RDP configuration files.

## Related groups and people
- [APT29 / Cozy Bear / Midnight Blizzard](../actors/apt29-cozy-bear-midnight-blizzard.md)

## Defender takeaways
- Watch for EWS activity, mailbox access anomalies, and unexpected OAuth or delegation changes.
- Treat cloud identity and mailbox review as high-signal indicators after a nation-state intrusion.
- Use strong MFA, audit logging, and conditional-access controls that reduce the impact of stolen credentials.

## Sources
- Microsoft Security blog, 2024-01-25: https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/
- Microsoft Security blog, 2024-10-29: https://www.microsoft.com/en-us/security/blog/2024/10/29/midnight-blizzard-conducts-large-scale-spear-phishing-campaign-using-rdp-files/
- Microsoft Security blog, 2021-03-04: https://www.microsoft.com/en-us/security/blog/2021/03/04/goldmax-goldfinder-sibot-analyzing-nobelium-malware/
