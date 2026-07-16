# Operation Phnom Penh MODBEACON activity

## Summary
Qianxin Threat Intelligence Center's Red Raindrop Team reported **Operation Phnom Penh** in July 2026: a Silver Fox / UTG-Q-1000 Ghost distributor used counterfeit-software SEO lures and Ghost infrastructure to deliver the custom **MODBEACON** Trojan to selected victims.

Qianxin's key assessment is that this distributor behaves like a hybrid actor: daily fake-software distribution and fraud traffic generation create a pool of controlled endpoints, while selected high-value access can be packaged for downstream customers or used for “black-on-black” targeting such as Cambodia gambling-industry lures.

## Tags
- ops
- Silver Fox
- UTG-Q-1000
- Ghost
- MODBEACON
- counterfeit software
- SEO poisoning
- fake installers
- Cambodia
- gambling industry targeting
- access broker
- traffic broker
- hybrid threat actor
- gRPC C2
- Qianxin Threat Intelligence Center
- Red Raindrop Team

## Why this matters
- The campaign links everyday fake-software distribution with selective deployment of a more professional private C2 framework.
- Qianxin reports MODBEACON C2 domains hosted behind Amazon CDN and Cloudflare CDN, raising the detection bar for network controls that rely on simple IP reputation.
- Lures around Phnom Penh, Poipet, Sihanoukville, Cambodian anti-scam crackdowns, and public-security incidents show timely regional social engineering layered on top of generic SEO software impersonation.
- Defenders should not treat Ghost / Silver Fox downloader activity as low-priority commodity malware when it may broker access to more capable operators.

## Reported campaign notes
- Qianxin observed the activity in mid-June 2026 through private intelligence and AI product telemetry.
- The distributor used counterfeit domains active since at least September 2025.
- A reported upstream counterfeit domain was `cn-mumu[.]com[.]cn`, staging `MeiqiWintsetup_x64.zip` from an Aliyun OSS bucket.
- Ghost C2 infrastructure was used to deliver MODBEACON and create persistence.
- Qianxin found related Ghost lures using Cambodian anti-scam and public-security themes in Chinese and Khmer-language forms.
- MODBEACON's C2 channel reuses concepts from Xray/V2Ray transport to wrap traffic as gRPC bidirectional streaming over HTTP/2.

## Defender guidance
- Inventory and block known Ghost / MODBEACON infrastructure from Qianxin where business requirements do not exist.
- Reimage or deeply investigate systems that executed counterfeit Chinese-market software installers from SEO results; persistence may include services, scheduled tasks, and WMI permanent subscriptions.
- Hunt for unusual outbound HTTP/2 gRPC sessions from endpoints and for binaries contacting `api.skystackservice[.]com`-style API endpoints without a legitimate software owner.
- Prioritize endpoints in government, enterprise, gambling, finance, and regional operations where fake installer exposure overlaps with privileged browser sessions or messaging tools.
- Preserve installer archives, browser download history, WMI repository data, scheduled-task XML, service creation events, DNS logs, and proxy logs before cleanup.

## Indicators
See [MODBEACON](../tools/modbeacon.md#indicators) for malware and infrastructure indicators reported by Qianxin.

## Related pages
- [MODBEACON](../tools/modbeacon.md)
- [WhatsApp VBScript ManageEngine RMM campaign](whatsapp-vbscript-manageengine-rmm-campaign.md)
- [Operation GriefLure Southeast Asia LNK dropper](operation-grieflure-southeast-asia-lnk-dropper.md)

## Sources
- Qianxin Threat Intelligence Center: [https://ti.qianxin.com/blog/articles/operation-phnom-penh-silverfox-ghost-distributor-targets-specific-victims-with-modbeacon-en/](https://ti.qianxin.com/blog/articles/operation-phnom-penh-silverfox-ghost-distributor-targets-specific-victims-with-modbeacon-en/)
- The Hacker News: [https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html](https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html)
