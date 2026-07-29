# Flying Eagle and Night Dragon Android RAT ecosystem

## Summary
On 2026-07-29, Hunt.io and NetAskari published a joint investigation into **Flying Eagle** (飞鹰), a Chinese-language Android remote-access and fraud framework whose leaked source code is circulating among multiple criminal operators. The research began with a malicious APK impersonating a Chinese Provincial Public Security Bureau service application and expanded through panel, TLS-certificate, source-code, and infrastructure pivots.

Hunt.io identified **170 distinct Flying Eagle servers active during a 30-day observation window**: 158 matched a conservative HTTP-panel fingerprint and 12 additional systems matched the default TLS certificate bundled with the leaked framework. The infrastructure was concentrated in Hong Kong, with smaller clusters in the United States and mainland China and individual systems in Finland, Malaysia, Canada, and Japan. This is an observed server count, not a victim or operator count.

The framework combines customizable APK generation, phishing overlays, Accessibility Service abuse, keylogging, screen and camera capture, SMS and file access, gesture injection, and WebSocket/Firebase communications. Two Telegram channels, `SQLRCE0` and `Yx科技` (Yx Technology), distribute modified builds, provide operational support, and advertise cash-out services. Neither is confirmed as the original developer. Hunt.io also found a newer, apparently independent Android RAT platform called **Night Dragon** (夜龙), introduced by `SQLRCE0` on 2026-06-23 and under version 2 development as of 2026-07-12.

## Tags
- ops
- operations
- Flying Eagle
- Feiying
- Night Dragon
- Android
- Android RAT
- Android malware
- mobile malware
- banking malware
- financial fraud
- Accessibility Service
- phishing overlays
- keylogging
- screen capture
- SMS theft
- WebSocket
- Firebase
- Telegram
- leaked source code
- malware framework
- MaaS
- China
- Chinese-language cybercrime
- government impersonation
- Public Security Bureau impersonation
- infrastructure
- TLS certificates
- Hong Kong
- SQLRCE0
- Yx Technology

## Why this matters
- Leaked full-stack malware source lowers the cost of entry and fragments attribution. Shared code, certificates, panel routes, and class names can connect deployments technically without proving one operator controls all of them.
- The builder changes package and class names and adds low-entropy padding, so defenders should not depend on static identifiers or APK size alone. Accessibility behavior, encrypted callback configuration, panel fingerprints, and certificate pivots are more durable.
- The fraud path is end to end: operators can generate lures, control devices, deploy application-specific overlays, capture payment credentials, and use advertised cash-out support.
- Government-service impersonation can convert institutional trust into sideloading. A June 2026 Chinese public warning independently corroborated fraudulent Public Security Bureau-themed applications, but does not establish the full 170-server set as one campaign.
- Night Dragon suggests exposed or disrupted codebases can be replaced quickly by successor platforms. Detection should target capabilities and infrastructure patterns rather than a single brand.

## Framework and delivery chain
1. Operators customize one of the bundled Android templates with a lure name, icon, text, and C2 callback address.
2. The builder replaces the original `com.icontrol.protector` package name with legitimate-looking randomized segments and renames recognizable classes with random 8–14 character strings.
3. Callback URLs are encrypted with AES-128-CBC; the builder derives the key with PBKDF2-SHA1 using 65,536 iterations and hard-coded defaults retained for compatibility with the earlier Windows `.NET` component `EaodWorker.exe`.
4. The build script adds roughly 2.8–3.5 MB of Base64-looking JSON assets intended to resemble SDK caches and reduce simple entropy-based detection.
5. Victims are lured into sideloading APKs impersonating government services, adult-streaming or social-media applications, financial applications, or public-welfare projects.
6. The implant abuses Android Accessibility Service and gesture injection, communicates over WebSocket and Firebase, and exposes device surveillance and financial-phishing functions through the operator panel.

Recovered original class names describe the core capability set:

| Original identifier | Reported purpose |
| --- | --- |
| `RecordPayPassword` | Payment-credential capture |
| `LiveKeysStrok` | Keylogging |
| `ScreenCaps` | Screen capture |
| `Webjector` | Web injection and phishing overlays |
| `AccessibilityActivity` | Accessibility Service abuse |

## Leaked-code ecosystem
Hunt.io analyzed a 388 MB Docker deployment named `中国龙.zip` distributed by Yx Technology. It contained nginx, PHP, MySQL, a Node.js WebSocket server, Android build tooling, phishing templates, and a default TLS certificate. A separate 292 MB XAMPP-oriented build, `飞鹰控打包.zip`, appeared through `SQLRCE0`.

An exposed directory at `77.105.161[.]235:8000` contained 2,383 files across 576 directories and shared the same misspelled `SECRIT_KEY` variable, PHP filenames, and code structure. Public channel messages claimed the original Flying Eagle source and 189 customer databases had been stolen in early 2026. Treat that database count as a leaked-channel claim, not independently validated victim telemetry.

Yx Technology published operational fraud instructions and cash-out offers charging 20–50 percent. `SQLRCE0` advertised a repaired build for 2,000 USDT and posted fixes for connectivity, WebSocket stability, and anti-uninstall behavior. These observations support a financially motivated Chinese-language criminal ecosystem; they do not prove that every panel or APK belongs to one group.

## Night Dragon follow-on
Night Dragon was advertised with payment-password capture for Alipay, WeChat, and banking applications, a black-screen fake-update mode, and automatic icon hiding. Hunt.io found two active panel servers on AS54801 in Hong Kong. One exposed panel displayed 46 devices, 29 marked connected, all in China; the researchers could not verify whether these represented real victims or test data.

The observed panel exposed live-screen, SMS, gallery, audio, camera, and file controls plus single-click overlays for major Chinese banks and the TokenPocket and imToken cryptocurrency wallets. Hunt.io assesses Night Dragon as an independent successor rather than merely another Flying Eagle fork, but that relationship remains analytical rather than a confirmed developer attribution.

## Public infrastructure and artifacts
Use these as historical investigation pivots, not a complete blocklist:

```text
207.56.30.188
207.56.30.194
108.187.7.66
108.187.7.71
77.105.161.235
154.44.25.12
85.137.253.48

110gongan.com
fusu666.cc
fusu.us.ci
ls.j2x8a.top
alcs.xyttkx.cc
txl.xyttkx.cc
h5.xyttkx.cc
s.orove.cn
```

Default packaged certificate fingerprints:

```text
SHA-256 06:E5:4E:95:28:F4:F8:CF:EB:DC:48:6D:78:C6:5B:46:21:2E
SHA-1   AB:42:24:A6:36:1E:6F:82:6F:DB:26:22:76:41:1E:03:F8:17:7E:30
```

Representative APK SHA-256 hashes published by Hunt.io:

```text
c692ad120cc90548d48dbe57d006f2403c49833b8993af3c38fe031eb39999bd
0376db397807c1f1e32a99a9db622f35f4fe5597bd05b4fd5e93117062e0131f
4395db6ad53a415532673b16f5b64207d53cecc5b15a736c038cf3890368a164
5dee5cde6f2874c582effe302960b21569ee007e9e0cd4f7499d418cceb9095b
b803cd5032dc1abd7aabc45c8cadc471c8a59872a95d48807f13e230c58230f3
d8a82d7b4457352774772bfac094127d7f67526ae7011d838cc3f7ccc15fd86e
1456f31bf6b5d4ade90fe080006478133296080353bf69c1819fa9b766e7f57a
773c77494d6321e4e449c9558c7915166bcb6c05e3c42a9d30e5eac4db8ee0df
```

Panel hunting features reported by Hunt.io include the route `/login?redirect=list/basic-list`, an initial `AdminPro` page title, an HTTP 302 redirect to HTTPS, and `Strict-Transport-Security: max-age=31536000`. These traits can collide with benign or separately operated deployments; require multiple matching features and validate ownership before escalation.

## Defender actions
1. **Block known lures and infrastructure with context.** Search mobile-DNS, proxy, certificate, and endpoint telemetry for the published domains, addresses, and hashes, but pair indicator matches with APK installation, Accessibility enrollment, WebSocket/Firebase behavior, or panel fingerprints.
2. **Restrict Android sideloading.** Use managed-device policy to deny installation from unknown sources, constrain app stores, and alert on government- or banking-themed applications outside approved channels.
3. **Monitor Accessibility abuse.** Inventory applications granted Accessibility Service, notification, SMS, screen-capture, camera, microphone, overlay, device-administrator, and battery-optimization exemptions. Investigate newly granted combinations rather than each permission in isolation.
4. **Hunt behaviorally.** Look for rapidly randomized package/class names alongside the same four-DEX and asset-layout pattern, encrypted callback configuration, large low-entropy Base64 JSON assets, gesture injection, persistent WebSocket traffic, and unexpected Firebase communication.
5. **Protect financial sessions.** Where supported, use transaction signing or out-of-band verification that does not rely on the potentially compromised Android device. Treat observed overlay, keylogging, or remote-screen behavior as credential and payment-instrument compromise.
6. **Respond at the account level.** Isolate affected devices, preserve APKs and Android forensic data, revoke mobile sessions, reset financial and messaging credentials from a clean device, contact financial providers, and review unauthorized transfers and new device enrollments.
7. **Track forks, not only names.** Cluster new samples and panels using certificate reuse, route structure, headers, source-code misspellings, PHP filenames, protocol behavior, and builder artifacts while keeping operator attribution separate from code-family attribution.

## Evidence and attribution caveats
The 170-server count is Hunt.io's 30-day infrastructure measurement, not a count of victims, infections, customers, or distinct criminal groups. The exposed Night Dragon panel's device totals were not validated. Telegram claims about stolen source, 189 customer databases, backdoor removal, and platform ownership may be self-serving. Shared leaked code and default certificates create strong family-level links but weak actor-level attribution. The observed targeting is primarily China-focused and financially motivated; international templates indicate possible expansion, not confirmed victim scope outside China.

## Related pages
- [RedWing mobile MaaS Android bank-fraud operation](redwing-mobile-maas-android-bank-fraud.md)
- [BTMOB and Grandoreiro campaigns](grandoreiro-btmob-latam-europe-malware-campaigns.md)
- [COWARDDUCK Android activity](uac-0145-clickfix-smartaxe-cowardduck.md)

## Sources
- Hunt.io and NetAskari, “Flying Eagle Android RAT: Leaked Source Code, 170 Active Servers, and a New Platform Called Night Dragon,” 2026-07-29: [https://hunt.io/blog/flying-eagle-android-rat-170-servers-night-dragon](https://hunt.io/blog/flying-eagle-android-rat-170-servers-night-dragon)
- Jiangsu public cybersecurity notice cited by the researchers, 2026-06-18: [https://www.jswx.gov.cn/anquan/guanli/202606/t20260618_1338409.shtml](https://www.jswx.gov.cn/anquan/guanli/202606/t20260618_1338409.shtml)
- The Hacker News pointer to the primary investigation, 2026-07-29: [https://thehackernews.com/2026/07/flying-eagle-android-rat-traces-found.html](https://thehackernews.com/2026/07/flying-eagle-android-rat-traces-found.html)
