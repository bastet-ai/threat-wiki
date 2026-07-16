# VPN Go browser-extension clipboard stealer

## Summary
Socket Threat Research reported on June 29, 2026 that Chrome and Firefox extensions branded as **VPN Go** / **Free VPN by VPN GO** added clipboard-stealing behavior through later extension updates. The extensions still presented visible proxy/VPN functionality, but malicious versions continuously read copied text, split it into chunks, and exfiltrated it over HTTP to hardcoded infrastructure.

The durable lesson is staged browser-extension abuse: an extension can enter a marketplace as plausible privacy tooling, later request or use clipboard and all-site permissions, and quietly harvest passwords, API keys, OAuth tokens, MFA recovery material, package-registry tokens, cloud credentials, and cryptocurrency seed phrases without needing a native payload.

## Tags
- ops
- operations
- browser extension
- Chrome Web Store
- Firefox Add-ons
- VPN Go
- clipboard theft
- clipboard stealer
- browser credential theft
- browser session risk
- proxy
- VPN
- staged malicious update
- supply-chain
- Socket

## Why this matters
- Clipboard access is close to secrets. Users routinely copy passwords, API keys, GitHub tokens, cloud credentials, MFA codes, package-registry tokens, and wallet seed material.
- The visible VPN/proxy feature gives broad browser permissions a plausible explanation and may keep the extension installed even when the privacy claims are false.
- The malicious behavior was introduced after earlier analyzed versions looked like proxy extensions, so extension update review and permission-change monitoring matter as much as initial installation review.
- Browser-extension compromise can affect managed developer endpoints even when package dependencies, CI workflows, and native endpoint malware controls are clean.

## Reported extensions and malicious versions

| Marketplace | Public / manifest name | ID | Confirmed malicious versions | Reported users at publication |
| --- | --- | --- | --- | --- |
| Chrome Web Store | `VPN Go: Free VPN` | `jgpfgonjjolillilkjfkiddakagkkpoj` | `1.1`, `1.2`, `1.3` | 146 |
| Mozilla Firefox Add-ons | `Free VPN by VPN GO` / manifest `VPN Go` | `vpngo@vpngo[.]com` | `1.3.3`, `1.3.4` | 3,499 |

Socket reported that Chrome version `1.0`, published December 22, 2025, behaved like a proxy extension without the confirmed clipboard exfiltration chain. Chrome versions `1.1` and `1.2`, published after the staged update, added clipboard theft; version `1.3` kept the behavior but moved infrastructure. Firefox versions `1.1`, `1.2`, `1.3.1`, and `1.3.2` were described as proxy extensions without confirmed clipboard theft, while `1.3.3` and `1.3.4` contained the malicious branch.

## Technical chain
1. The extension presents itself as privacy/VPN tooling and provides enough proxy behavior to look useful.
2. Malicious Chrome versions add clipboard access and an all-site content script that runs early in page load.
3. The Chrome content script calls `navigator.clipboard.readText()` every roughly 500 milliseconds, suppresses errors, skips duplicates, chunks copied text, and sends chunks to the extension background service worker.
4. The Chrome background worker builds HTTP exfiltration requests to `/html/continue.php` with `uid`, `part`, `total`, and `data` query parameters.
5. Malicious Firefox versions move the clipboard loop into the background script. Firefox polls every roughly 1.5 seconds, uses the same chunking/session pattern, and sends copied data to the same endpoint path and query-parameter structure.
6. The malicious versions also retrieve proxy locations from the same infrastructure families, reinforcing that the actor combined functional proxy presentation with clipboard theft.
7. Socket reported overlap between Chrome and Firefox builds, including Chrome version `1.3` carrying Firefox-specific Gecko settings, pointing to shared source material or a common build process.

## Indicators and hunt pivots

### Extension identifiers and accounts
- Chrome extension ID: `jgpfgonjjolillilkjfkiddakagkkpoj`
- Chrome developer listed by Socket: `zegivati83`
- Chrome developer email: `zegivati83@gmail[.]com`
- Privacy policy URL: `hxxps://telegra[.]ph/Privacy-Policy-12-11-127`
- Privacy policy contact email: `info@vpngogmail[.]com`
- Firefox Gecko ID: `vpngo@vpngo[.]com`

### Infrastructure
- Chrome `1.1` / `1.2`: `178[.]236[.]252[.]133`
- Firefox `1.3.3`: `178[.]236[.]252[.]161`
- Chrome `1.3` and Firefox `1.3.4`: `77[.]91[.]123[.]187`
- Clipboard exfiltration endpoint path: `/html/continue[.]php`
- Proxy-location endpoint path: `/locations`
- Exfiltration query parameters: `uid`, `part`, `total`, `data`
- JavaScript API: `navigator.clipboard.readText`
- Fetch mode reported by Socket: `no-cors`

### Hashes reported by Socket
- Chrome CRX `1.1`: `43dc5b1d4c73d5ed9f4f7f561830079896eeb533a7c21bc577e4e267d5a3aa56`
- Chrome CRX `1.2`: `b3b63970833b3379ecec2d3ef8fea328fef8dd1c1574b1bcdfebad5bdce9280c`
- Chrome CRX `1.3`: `72fc06a8b03720f4a64744eecd5b3f658ad880bdb327c0c465c7bdc66b14a8d2`
- Firefox XPI `1.3.3`: `fbbdf4bc490ad7b28953630c1707aa68b89d319b9b735f3d8563320b81b21a97`
- Firefox XPI `1.3.4`: `2fe9c41901045013ba28ccb9af5870f9aef4f1ffd1e717cd5e0189ffdbe7fca2`

## Defender heuristics
- Remove the Chrome and Firefox extensions where present and block the listed extension IDs in managed browser policy.
- Treat secrets copied while a malicious version was active as exposed. Prioritize GitHub, cloud, package-registry, password-manager recovery, OAuth, MFA recovery, and cryptocurrency material.
- Hunt browser extension directories, EDR telemetry, proxy logs, and DNS/HTTP telemetry for the extension IDs, the three IP addresses, `/html/continue.php`, `/locations`, and the `uid` / `part` / `total` / `data` exfiltration parameter pattern.
- Review browser-extension inventory for VPN, proxy, wallet, AI assistant, downloader, coupon, screenshot, and productivity extensions that combine clipboard permissions, proxy control, all-site access, or broad tab permissions.
- Require security review for extension permission changes before auto-updates are allowed on privileged workstations. A new `clipboardRead` permission or all-site content script in a VPN/proxy extension should be treated as high-risk.
- For developer and finance users, correlate the extension install/update window with recently copied credentials, admin-console access, package publishing activity, and cryptocurrency-wallet activity.

## Related pages
- [Perplexity AI-spoofing Chromium extension search hijacker](perplexity-ai-chromium-extension-search-hijacker.md)
- [StegoAd Edge extension steganography campaign](stegoad-edge-extension-steganography-campaign.md)
- [Adblock for YouTube BadBlocker remote-script injection risk](adblock-for-youtube-badblocker-remote-script-injection.md)
- [Chrome live-wallpaper extension ad-fraud network](chrome-live-wallpaper-extension-ad-fraud.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)

## Sources
- [Socket](https://socket.dev/blog/chrome-and-firefox-extensions-free-vpns-add-clipboard-stealers)
