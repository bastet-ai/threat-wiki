# ModHeader browser-extension surveillance capability

## Summary
Stripe OLT's July 2026 incident-response writeup found hidden surveillance functionality in the genuine Chrome Web Store build of **ModHeader (Modify HTTP headers)**, a trusted developer / QA browser extension with about **900,000 Chrome users**. The analyzed `7.0.18` build remained a functional header-editing tool, but also shipped a dormant browsing-history collection and exfiltration pipeline, install/update/uninstall telemetry, and all-URL request-metadata collection.

The immediate public finding is not confirmed bulk exfiltration: Stripe OLT reported the browsing-history upload path was gated by an empty allow-list. The durable risk is that the signed store-distributed extension already contained the collection, encryption, storage, scheduling, and endpoint code; a routine extension update could change the allow-list without new permissions or a fresh user decision. Google removed the Chrome Web Store listing on July 10, 2026, and The Hacker News reported Microsoft also removed the Edge listing after public reporting.

## Tags
- ops
- browser extension
- Chrome extension
- Edge extension
- browser security
- developer tooling
- data exfiltration
- surveillance
- browsing history
- IndexedDB
- AES-GCM
- official store compromise
- trusted extension risk
- adware
- ModHeader
- Stripe OLT
- HackIndex
- Chrome Web Store
- Microsoft Edge Add-ons
- The Hacker News

## Reported activity
- Stripe OLT analyzed **ModHeader 7.0.18**, extension ID **`idgpnmonknjnojddfkpgkljpfnnfcklj`**, while it was the live Chrome Web Store release.
- The version contained a service-worker pipeline that generated a device fingerprint, encrypted visited domains with AES-GCM, stored them in IndexedDB, and had code to upload the encrypted set to `api.stanfordstudies[.]com/app/log` roughly daily.
- The browsing-history upload was dormant in the analyzed build because an allow-list was empty. Stripe OLT emphasizes that the key, storage, scheduler, and endpoint logic were already present.
- Install, update, and uninstall telemetry was live and beaconed to `extensions-hub[.]com` with product/version/browser information.
- Stripe OLT verified the suspicious service-worker code against Chrome Web Store content-verification metadata: the code was in the signed, official store-distributed package, not a counterfeit extension reusing the ModHeader name.
- Google removed the Chrome listing on **July 10, 2026** after responsible disclosure. The Hacker News reported Microsoft removed the Edge listing on **July 3, 2026**, with third-party install estimates around 700,000 Edge users.
- Stripe OLT reports `api.stanfordstudies[.]com` and `api.extensions-hub[.]com` resolved to the same AWS us-east-2 host **3.147.61[.]167** at analysis time; this supports infrastructure linkage but should not be over-read as attribution.

## Indicators
| Type | Value | Notes |
| --- | --- | --- |
| Extension ID | `idgpnmonknjnojddfkpgkljpfnnfcklj` | ModHeader / Modify HTTP headers, version `7.0.18` in Stripe OLT analysis. |
| Extension version | `7.0.18` | Live Chrome Web Store release at time of July 6 analysis. |
| Network URL | `https://api.stanfordstudies[.]com/app/log` | Encrypted browsing-history exfiltration endpoint in dormant pipeline. |
| Network URL | `https://www.extensions-hub[.]com/partners/` | Install/update/uninstall telemetry path. |
| Domain | `stanfordstudies[.]com` | Exfiltration / operator-backend domain family. |
| Domain | `extensions-hub[.]com` | Telemetry / advertising-partner domain family. |
| Subdomain | `devos.stanfordstudies[.]com` | Operator-backend pivot reported by Stripe OLT. |
| Subdomain | `devlog.stanfordstudies[.]com` | Operator-backend pivot reported by Stripe OLT. |
| Shared IP | `3.147.61[.]167` | AWS us-east-2 host resolving `api.stanfordstudies[.]com` and `api.extensions-hub[.]com` at analysis time. |
| IndexedDB store | `temp` | AES-encrypted visited-domain map. |
| IndexedDB store | `settings` | Device fingerprint, AES IV, and scheduling material. |
| Path fragment | `chrome-extension_idgpnmonknjnojddfkpgkljpfnnfcklj_0.indexeddb.leveldb` | Local Chrome profile artifact to hunt. |
| Static marker | `mod盐header` | Internal marker string reported by Stripe OLT. |

## Why this matters
- **Official-store distribution is not sufficient trust.** The suspicious code was in a verified Chrome Web Store package for a popular, functional extension.
- **Dormant collection code still changes risk.** A disabled condition can be changed in a silent update, while broad extension permissions and host access are already granted.
- **Developer and administrator browsers are high-value targets.** Header-editing extensions are common on machines that access admin panels, staging systems, bearer-token URLs, SaaS consoles, and internal applications.
- **Browser-extension inventory needs behavioral review.** Permission review alone may miss a tool whose requested access plausibly matches its advertised purpose.

## Defender guidance
1. Remove ModHeader `7.0.18` and any untrusted ModHeader builds from managed and unmanaged Chrome / Edge profiles until a verified clean build and ownership chain are established.
2. Search browser-extension inventory for extension ID `idgpnmonknjnojddfkpgkljpfnnfcklj` across Chrome and Chromium-derived browsers.
3. Hunt DNS, proxy, and endpoint telemetry for `stanfordstudies[.]com`, `extensions-hub[.]com`, `/app/log`, and `3.147.61[.]167`, especially from developer or administrator workstations.
4. Inspect affected profiles for the `temp` and `settings` IndexedDB stores under the ModHeader extension path; correlate timestamps with browsing to sensitive SaaS/admin destinations.
5. For hits involving privileged users, review exposure of token-bearing URLs, password reset links, invitation links, cloud console sessions, and internal admin portals visited while the extension was installed.
6. Move high-privilege browser extension governance toward allow-listed extension IDs, publisher/ownership monitoring, and update diffing for extensions with `<all_urls>` or request-observation permissions.

## Related pages
- [Chrome live-wallpaper extension ad-fraud network](chrome-live-wallpaper-extension-ad-fraud.md)
- [StegoAd Edge extension steganography campaign](stegoad-edge-extension-steganography-campaign.md)
- [Adblock for YouTube BadBlocker remote-script injection risk](adblock-for-youtube-badblocker-remote-script-injection.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)

## Sources
- Stripe OLT: <https://stripeolt.com/knowledge-hub/threat-research/chrome-extension-hidden-data-exfiltration-900k-users/>
- The Hacker News: <https://thehackernews.com/2026/07/google-and-microsoft-pull-modheader.html>
- HackIndex: <https://hackindex.io/research/modheader-malware-chrome-spyware>
