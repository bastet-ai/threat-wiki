# Fox Tempest

## Summary
Fox Tempest is Microsoft's name for a financially motivated cybercrime actor operating a malware-signing-as-a-service operation. Microsoft says Fox Tempest abused Microsoft Artifact Signing to issue short-lived fraudulent code-signing certificates, letting criminal customers disguise malware as legitimate signed software.

Microsoft reported in May 2026 that Fox Tempest had created more than a thousand certificates and hundreds of Azure tenants and subscriptions. Microsoft's Digital Crimes Unit disrupted the service in an operation codenamed **OpFauxSign**, seizing `signspace[.]cloud`, taking hundreds of virtual machines offline, blocking access to code-hosting infrastructure, and revoking over one thousand attributed certificates.

## Tags
- actors
- groups
- cybercrime
- malware-signing-as-a-service
- code signing
- ransomware
- Microsoft
- Azure
- Artifact Signing
- Fox Tempest
- OpFauxSign

## Why this matters
- Code signing is a trust signal that many users and controls still overweight; signed malware can bypass reputation, policy, and human suspicion.
- The service industrialized certificate abuse for other crews rather than serving one malware family, increasing blast radius across ransomware, loaders, and stealers.
- Microsoft connected Fox Tempest-enabled signing to Rhysida deployment by Vanilla Tempest and to malware families including Oyster, Lumma Stealer, and Vidar.
- Short-lived 72-hour certificates create a detection window problem: defenders need issuer/subscription and signing-pattern analytics, not just stale certificate blocklists.

## Service model
- Customers uploaded malicious files to a signing portal backed by Azure subscriptions, certificates, and a management database.
- Microsoft assesses the actor likely used stolen identities in the United States and Canada to pass validation and obtain digital credentials.
- Pricing publicly reported by Microsoft/THN ranged from roughly USD $5,000 to $9,000.
- Starting in February 2026, Fox Tempest reportedly shifted toward preconfigured Cloudzy-hosted virtual machines that customers could use to submit artifacts and retrieve signed binaries.

## Defender heuristics
- Do not trust code-signing status alone; verify publisher identity, reputation age, file prevalence, download source, and campaign context.
- Hunt for malware masquerading as common remote-work/admin apps such as AnyDesk, Microsoft Teams, PuTTY, and Cisco Webex.
- Alert on newly issued or very short-lived certificates signing high-risk binaries, especially where publisher identity and distribution channel do not match.
- Review signed binaries delivered through malvertising or search-result ads; Microsoft reported signed Oyster delivery from bogus Microsoft Teams download pages.
- Track revocation telemetry and certificate transparency-style metadata where available.

## Related pages
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/05/19/exposing-fox-tempest-a-malware-signing-service-operation/>
- Microsoft Digital Crimes Unit: <https://blogs.microsoft.com/on-the-issues/2026/05/19/disrupting-fox-tempest-a-cybercrime-service/>
- The Hacker News summary: <https://thehackernews.com/2026/05/microsoft-takes-down-malware-signing.html>
