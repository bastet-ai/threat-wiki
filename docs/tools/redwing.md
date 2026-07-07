# RedWing

## Summary
RedWing is an Android malware-as-a-service (MaaS) family documented by Zimperium zLabs on July 7, 2026. Zimperium describes it as a new Android spyware / banking-trojan variant offered through Telegram, with dropper construction, payload customization, subscription tiers, referral incentives, and operator documentation that lower the barrier for mobile banking fraud.

The family appears related to, or derived from, Oblivion based on dropper-stage and overlay similarities. Zimperium also uses the name **Rokarolla** in its reporting for the Android banking trojan component observed in the RedWing operation.

## Tags
- tools
- malware
- Android malware
- Android spyware
- banking trojan
- mobile malware
- malware-as-a-service
- MaaS
- RedWing
- Rokarolla
- Oblivion
- Telegram bot
- Android Accessibility Service
- overlay attacks
- SMS interception
- VNC
- call forwarding
- DDoS
- credential theft
- Zimperium
- zLabs

## Why this matters
- RedWing packages mobile-bank fraud as a rentable service: affiliates can build custom APKs and phishing-store pages through Telegram rather than writing malware.
- The malware combines credential overlays, SMS / notification interception, Accessibility abuse, VNC-style live control, camera / microphone access, file collection, contact and call-log theft, location tracking, and DDoS capability.
- Its C2 panel can customize target apps and overlay content, so defenders should not treat one static target list as complete.
- Silent unconditional call forwarding through the `*21*` USSD path can defeat voice-based verification and bank fraud callbacks.

## Delivery and operator model
Zimperium reports that RedWing operators distribute payloads through mobile-targeted phishing sites. The dropper constructor can forge fake app-store pages that mimic Google Play, Galaxy Store, Huawei AppGallery / AppGallery-style flows, or fully custom landing pages with fake ratings, reviews, and download counts.

The MaaS backend includes:

- a Telegram channel and bot-driven builder flow;
- subscription tiers and referral discounts;
- APK customization, obfuscation, and creation through Telegram;
- a dropper constructor for tailoring the initial sideload lure;
- a RAT / admin panel for payload configuration, permission telemetry, overlays, and live device control.

## Capabilities
Reported RedWing / Rokarolla capabilities include:

- harvesting SMS messages, contacts, call logs, files, device metadata, and location;
- intercepting notifications and default-SMS app events;
- abusing Android Accessibility Service for screen reading, UI monitoring, gestures, clicks, text entry, and sensitive-data capture;
- displaying fake overlays over banking and cryptocurrency apps to collect credentials, PINs, card data, and one-time codes;
- generating or changing custom injects from the C2/admin panel;
- live screen streaming / VNC and remote screen locking;
- hiding the application icon for persistence and evasion;
- camera photo capture and microphone audio recording;
- launching apps or URLs by package name / intent;
- unconditional call forwarding through hidden USSD requests using `*21*` after receiving a `call_forward_set` command;
- DDoS traffic generation from infected devices.

Zimperium observed RedWing telemetry where the implant reports permission state to C2, allowing the panel to decide which commands can run on the compromised device.

## Defender notes
- Treat Android devices used for banking, finance, executive communications, or workforce MFA as fraud-relevant endpoints, not just personal devices.
- Hunt for sideloaded apps that request Accessibility, notification access, default-SMS status, overlay / draw-over permission, battery-optimization exemptions, contact / call-log access, and file-system access in staged onboarding flows.
- Monitor for suspicious unconditional call-forwarding activation (`*21*`), especially after mobile phishing, sideloading, or Accessibility prompts.
- For financial institutions, correlate mobile-device risk signals such as active screen sharing, overlay permission grants, Accessibility abuse, SMS interception, call-forwarding changes, and new device / IP login anomalies before approving high-risk transfers.
- During response, preserve the APK / dropper, install source, phishing URL, Accessibility-service label and description, package name, granted permissions, C2 traffic, overlay target list, call-forwarding status, and related SMS / notification artifacts.
- Do not rely only on static package names or hard-coded overlay targets; RedWing's builder and panel allow per-affiliate customization.

## Related pages
- [RedWing mobile MaaS Android bank-fraud operation](../ops/redwing-mobile-maas-android-bank-fraud.md)
- [QuimaRAT](quimarat.md)
- [Crypto Clipper Tor / USB worm](../ops/crypto-clipper-tor-usb-worm.md)
- [Grandoreiro and BTMOB Latin America / Europe malware campaigns](../ops/grandoreiro-btmob-latam-europe-malware-campaigns.md)

## Sources
- Zimperium zLabs: https://zimperium.com/blog/redwing-a-mobile-malware-as-a-service-operation
- The Hacker News: https://thehackernews.com/2026/07/redwing-maas-packages-android-bank.html
