# RedWing mobile MaaS Android bank-fraud operation

## Summary
On July 7, 2026, Zimperium zLabs published analysis of **RedWing**, a Telegram-sold Android malware-as-a-service operation for mobile banking fraud. RedWing gives affiliates a builder, fake app-store delivery flow, admin panel, credential overlays, SMS / notification interception, live device control, call-forwarding abuse, and DDoS capability.

Zimperium assesses RedWing as a new variant or close relative of **Oblivion**, citing similarities in the dropper stage and overlays, and describes the analyzed banking-trojan component as **Rokarolla**. Public reporting says many droppers and payloads associated with the operation evaded conventional security tooling at publication time.

## Tags
- ops
- RedWing
- Rokarolla
- Oblivion
- Android malware
- Android spyware
- banking trojan
- mobile banking fraud
- malware-as-a-service
- MaaS
- Telegram bot
- phishing
- fake app store
- sideloading
- Android Accessibility Service
- overlay attacks
- SMS interception
- notification interception
- call forwarding
- VNC
- DDoS
- credential theft
- Zimperium
- zLabs

## Timeline
- **2026-03-21:** Zimperium reported Oblivion RAT, later used as a comparison point for RedWing dropper and overlay behavior.
- **2026-05-09:** Zimperium's RedWing report includes example C2 permission telemetry timestamped May 9, 2026.
- **2026-07-07:** Zimperium published RedWing / Rokarolla analysis; The Hacker News amplified the campaign the same day.

## Attack chain
1. Operators or affiliates send mobile phishing links to fake app-store pages.
2. The landing page imitates Google Play, Galaxy Store, AppGallery-style stores, or a custom app-store page with fake ratings, reviews, and download counts.
3. The victim sideloads the malicious app outside the official store.
4. The app stages permission requests behind routine-looking prompts: battery exemption, default-SMS role, notifications, overlay permission, and Accessibility Service.
5. The implant reports granted permissions and device state to C2.
6. Operators use the admin panel to deploy overlays, collect SMS / notifications / files / contacts / call logs, start VNC-style live control, activate camera or microphone capture, and issue call-forwarding or DDoS commands.

## Technical notes
- **Builder / MaaS:** Telegram bot and channel support APK customization, obfuscation, subscription purchase, referral discounts, and operator documentation.
- **Dropper constructor:** fake store pages and customized lures bootstrap sideloading; Zimperium observed payloads masquerading as legitimate app-store extensions.
- **Permission telemetry:** C2 receives JSON-style state including SMS, phone, notification, contacts, location, Accessibility, default-SMS, battery level, online state, device ID, and team ID fields.
- **Accessibility customization:** the RAT panel lets operators customize the Accessibility-service name and descriptive text used to socially engineer permission grants.
- **Overlay control:** RedWing can request `android.settings.action.MANAGE_OVERLAY_PERMISSION` and draw fake login / card / PIN windows over selected banking and cryptocurrency apps.
- **Targeting:** Zimperium identified 82 institutions targeted in the analyzed overlay set, with a strong focus on Russian financial institutions; the target list can be changed in the admin panel without redistributing the malware.
- **Call forwarding:** the `call_forward_set` command can silently execute hidden USSD requests using `*21*` to redirect incoming calls to attacker-controlled numbers, undercutting voice-based 2FA and bank fraud checks.
- **Remote control:** reported functions include live screen streaming, keylogging, app / URL launch by package name or intent, screen manipulation, file enumeration under `/sdcard`, camera photos, microphone recording, and remote screen locking.

## Defender guidance
- Block or tightly govern Android sideloading on managed devices; require mobile-threat-defense telemetry for devices used in financial approval, MFA, or executive workflows.
- Alert on apps that combine Accessibility, notification listener, default-SMS, overlay, battery-exemption, contacts, call-log, and broad file access soon after installation.
- Add fraud controls for call-forwarding changes, especially unconditional forwarding via `*21*`, after mobile phishing or suspicious app-install events.
- Treat active screen sharing / VNC-like behavior, overlay permission, Accessibility use, and new default-SMS apps as high-risk banking-session context.
- For incident response, preserve the malicious APK, dropper page URL, package name, signing certificate, Accessibility label / description, C2 endpoints, panel commands, permission-grant timeline, call-forwarding state, SMS / notification access, and affected financial applications.
- Assume affiliate customization: package names, overlay targets, fake-store branding, and C2 infrastructure may vary by buyer.

## Related pages
- [RedWing](../tools/redwing.md)
- [Grandoreiro and BTMOB Latin America / Europe malware campaigns](grandoreiro-btmob-latam-europe-malware-campaigns.md)
- [Crypto Clipper Tor / USB worm](crypto-clipper-tor-usb-worm.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)

## Sources
- [Zimperium zLabs](https://zimperium.com/blog/redwing-a-mobile-malware-as-a-service-operation)
- [The Hacker News](https://thehackernews.com/2026/07/redwing-maas-packages-android-bank.html)
