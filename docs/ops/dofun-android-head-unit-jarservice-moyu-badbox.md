# DoFun Android head-unit malware: MoYu/BADBOX ad-fraud and proxy botnet via TWCore updaters

## Summary
On August 21, 2026, Kaspersky published analysis (discovered June 2026) of the first documented malware infection chain specific to **Android-based automotive head units** running firmware from the Chinese vendor **DoFun**. Attackers weaponize **TWCore**, the legitimate system app that handles software updates on DoFun head units, to deliver a Trojan dropper named **JarService** that installs a multi-stage downloader. The downloader establishes C2, retrieves a clicker payload, and enables **ad fraud** and **residential proxy botnet** use of the infected vehicle. The Hacker News attributes the activity with high confidence to the **MoYu Group**, the same operator HUMAN Satori Threat Intelligence and Research outed in 2025 behind the **BADBOX** ad-fraud and residential-proxy scheme; Google sued 25 unnamed Chinese individuals or entities over BADBOX in July 2025.

DoFun serves more than 30 million vehicle owners worldwide, which makes the affected-firmware base large even though the infection chain is specific to DoFun head units.

## Tags
- ops
- operations
- DoFun
- head unit
- infotainment
- TWCore
- JarService
- ad fraud
- clicker
- proxy botnet
- residential proxy
- MoYu
- BADBOX
- HUMAN Satori
- automotive
- Android automotive
- C2
- loadlib2
- Kaspersky

## Infection chain
- **Infection vector: the built-in updaters.** DoFun head units ship firmware, applications, and cloud services; **TWCore** is the legitimate system app that pulls update metadata from DoFun's cloud and installs files. Attackers abused that update channel to push a new app to head units with **no user interaction**.
- **JarService dropper.** A UI-less ("empty") application that contains the next-stage payload in encrypted form plus its version and entry point. It decrypts and launches the downloader. No impersonation of a legitimate service; nothing the driver has to click.
- **Downloader → C2.** The downloader sends implant information to an attacker server (HTTP POST) to `144.217.243[.]201`, which responds with the next-stage payload path (`/vr34der34/dex3.68.png`). The payload name encodes a version number (`dex3.68`), letting Kaspersky recover seven distinct variants back to version 3.57.
- **Clicker final stage.** The payload runs as a background user application with no UI. It POSTs to C2 (`/cpc/api/task`) every 90 minutes by default, reporting device model, display resolution, Wi-Fi network identifier, MAC address, and configuration version. C2 responds with either an updated configuration (new C2 addresses/paths) or integer command identifiers ("productId") mapped to commands stored as serialized JSON via the SharedPreferences API.
- **Commands.** Nine commands, including `http` (arbitrary POST/GET), `web` (open a link in WebView and run arbitrary JavaScript), `copy` (clipboard), `loadlib2` (download and execute arbitrary code from a URL — the one actively observed), `deeplink`, `traceroute`, and value/clipboard helpers. The observed use: ad-click fraud and proxy use.

## Attribution
- **MoYu Group**, attributed with high confidence by The Hacker News, based on Kaspersky's reporting. HUMAN Satori identified MoYu in 2025 as the operator behind **BADBOX**, a broad ad-fraud and residential-proxy scheme; Google's July 2025 lawsuit against 25 unnamed Chinese individuals/entities targets BADBOX infrastructure.
- Kaspersky's researcher Dmitry Kalinin: "This is the first documented case of malware found on a car head unit with an infection chain specific to that type of device."
- Preserve the attribution caveat: the MoYu/BADBOX linkage is reported by secondary coverage (The Hacker News) of Kaspersky's research; Kaspersky's own write-up focuses on the DoFun/TWCore mechanics.

## Defender priorities
1. **Inventory DoFun-firmware vehicles.** Fleet and OEM operators using DoFun head-unit software should treat the TWCore update channel as a compromised trust boundary: audit what apps have been auto-installed beyond expected DoFun updates.
2. **Hunt for JarService.** Look for a UI-less app with encrypted embedded payloads and POST beacons to `/cpc/api/task` at roughly 90-minute intervals, and to the `144.217.243[.]201` range.
3. **Treat infected head units as proxy/exit nodes.** A car on a home or office Wi-Fi acting as a residential proxy changes that network's egress fingerprint; correlate outbound traffic and ad-click volume from vehicle IPs.
4. **Preserve evidence.** Retain C2 configuration blobs (SharedPreferences JSON), C2 address/rotation history, and version strings (`dex3.57`–`dex3.68`) before wiping.
5. **Correlate with BADBOX.** Check whether the same operator's ad-fraud/residential-proxy infrastructure overlaps with this campaign's C2.

## Assessment limits
- No confirmed victim count or fleet scope is published; the 30 million DoFun vehicle owners is the addressable base, not the infected base.
- No KEV entry, no vendor (DoFun) public advisory was located as of this scan; monitor DoFun and Kaspersky for a DoFun-patched firmware release.
- Attribution is "high confidence" per secondary reporting, not a multi-agency confirmation.

## Related pages
- [Dysphoria IoT botnet: blockchain C2 and victim-operated relays](dysphoria-iot-botnet.md)
- [Flying Eagle / Night Dragon Android RAT ecosystem](flying-eagle-night-dragon-android-rat-ecosystem.md)

## Sources
- Kaspersky: [Malware in car infotainment systems: how infection occurs](https://www.kaspersky.com/blog/car-botnet-malware-for-head-units-with-android/56296/) — August 21, 2026
- The Hacker News: [Android Car Malware Spreads Through Built-In Updaters for Ad Fraud, Proxy Botnet](https://thehackernews.com/2026/08/android-car-malware-spreads-through.html) — August 21, 2026
