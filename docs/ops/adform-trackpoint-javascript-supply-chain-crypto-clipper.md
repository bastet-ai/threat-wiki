# Adform Trackpoint JavaScript supply-chain crypto clipper

## Summary
On July 27, 2026, advertising-technology provider **Adform** detected and contained malicious JavaScript appended to a shared tracking resource used by downstream websites. The injected code attempted to replace Bitcoin, Ethereum, and Tron wallet addresses while an affected page was open. Adform says it removed the code, notified affected clients, reported the incident to authorities, and found no evidence that the payload installed software or established persistence.

The compromise is a web supply-chain incident: modifying one centrally served script exposed visitors to unrelated customer sites that embedded it. Public analysis identifies the affected resource as `trackpoint-async.js` on `s2.adform[.]net`. A captured sample monitored clipboard and page interactions, rewrote matching wallet addresses in visible text and form fields, and contained logic to send the current page hostname and path to `84.32.102[.]230:7744`.

The public scope remains incomplete. Adform identifies July 27 as the affected date, while independent researcher Kevin Beaumont reported seeing malicious Adform activity over the preceding week. No affected-site count, visitor count, confirmed diverted transaction total, initial-access path, or actor attribution has been published.

## Tags
- ops
- supply-chain attack
- web supply chain
- Adform
- advertising technology
- third-party JavaScript
- crypto clipper
- clipboard hijacking
- cryptocurrency theft
- Bitcoin
- Ethereum
- Tron
- browser security
- incident response

## Why this matters
- A trusted third-party script can execute in every embedding site's page context without requiring the attacker to compromise each downstream site.
- The captured payload did more than alter clipboard copy operations: it traversed text nodes and rewrote `input`, `textarea`, and `contenteditable` values, including programmatic writes.
- Browser and intermediary caches can preserve compromised JavaScript after the origin is remediated, which is why Adform advised visitors and clients to clear relevant caches.
- Cryptocurrency transfers are difficult to reverse. Address verification must occur on a trusted display or out-of-band channel immediately before authorization, not only when an address is first copied.
- Adform's finding of no evidence of telemetry exfiltration is not equivalent to proving the code lacked that capability; the company says transmission was technically possible and remains under investigation.

## Reported timeline
- **Before July 27:** Beaumont says he could see malicious activity through Adform over the preceding week. This has not been reconciled with Adform's narrower public affected-date statement.
- **July 27:** Adform detected suspicious activity, initiated incident response, confirmed the threat, removed the malicious code, and contained the incident.
- **July 27:** Max Maass preserved a public copy of the modified script for analysis.
- **After containment:** Adform notified affected clients, advised cache clearing, reported the event to relevant authorities, and continued its investigation.
- **August 1:** Public reporting consolidated the provider notice and independent sample analysis.

## Technical behavior
The independently captured `trackpoint-async.js` sample contained two malicious blocks appended to legitimate library code:

1. One block watched clipboard activity and repeatedly attempted to replace strings matching Bitcoin, Ethereum, or Tron wallet formats with hardcoded actor-controlled addresses.
2. A second block walked page text nodes and form-like elements, hooked `input` and `textarea` value setters, and intercepted copy, cut, paste, and input events so an address could be replaced even without a straightforward clipboard-copy path.
3. Replacement strings were concealed with a six-byte XOR key.
4. The sample attempted an HTTP request to `84.32.102[.]230:7744` containing the page hostname and URL path.
5. Adform says the payload operated only while the affected page was open and was not designed to install software or establish persistence.

The sample demonstrates exfiltration-capable code, but public evidence does not establish that the request reached the operator or that visitor information was successfully collected. Adform reports no evidence of transmitted user IP addresses or visited-site information while acknowledging that transmission may have been possible.

## Defender actions

### For websites embedding Adform resources
1. **Confirm exposure with Adform.** Use the provider's dedicated client communication and support channel to establish which properties, time windows, resource variants, and cache layers were affected.
2. **Purge every cache layer.** Invalidate the affected object from browser-facing CDNs, reverse proxies, service-worker caches, tag managers, and other managed caches under your control. Do not assume origin replacement invalidated downstream copies.
3. **Preserve evidence first.** Retain historical response bodies, CDN and proxy logs, CSP reports, subresource-monitoring telemetry, page-load records, and cache metadata before routine expiration or purge where feasible.
4. **Notify exposed users based on evidence.** Prioritize visitors who loaded the affected resource and interacted with cryptocurrency addresses. Avoid implying confirmed theft where only script exposure is known.
5. **Reduce third-party script authority.** Inventory externally hosted JavaScript, remove unused tags, pin or self-host immutable assets where contractual and operational controls permit, and deploy Content Security Policy plus subresource or runtime integrity monitoring. Subresource Integrity only helps when the expected file is immutable and the page pins a known-good hash.
6. **Monitor vendor-script drift.** Alert on unexpected response-hash, size, syntax, destination, or behavior changes in high-reach scripts, especially clipboard access, DOM-wide mutation, form-setter hooks, and new raw-IP network destinations.

### For potentially exposed visitors and organizations
1. Clear browser cache as Adform recommends, especially for browsers used on July 27 to visit affected sites.
2. Review Bitcoin, Ethereum, and Tron transactions prepared while an affected page was open. Compare destination addresses against a trusted invoice, hardware-wallet display, signed message, or separately verified recipient channel.
3. If funds were sent to a substituted address, preserve the transaction ID, destination address, source wallet, screenshots, browser history, and relevant communications; notify the wallet or exchange provider and appropriate authorities promptly.
4. Hunt web and network telemetry for the resource and destination below. A request to the legitimate Adform script alone indicates possible exposure, not successful address replacement or theft.
5. Do not treat endpoint reimaging as the default response without evidence of another payload. Adform and the captured script analysis describe page-context JavaScript rather than host persistence; preserve and investigate first.

## Public indicators and pivots
- Affected host: `s2.adform[.]net`
- Reported resource: `/banners/scripts/st/trackpoint-async.js`
- External destination: `84.32.102[.]230:7744`
- Example request shape: `http://84.32.102[.]230:7744/p?h=<hostname>&u=<path>`
- Published captured-script SHA-256: `02ff86c7f9fe609a753ff15bda90baa3c3e0d4a2e559ec4fcf8a3de0954b7c55`

Treat these as historical investigation pivots. `s2.adform[.]net` is legitimate provider infrastructure and should not be treated as intrinsically malicious. The destination IP may be reassigned, and a hash match establishes possession or delivery of the captured script—not wallet theft by itself.

## Evidence limits
- Adform has not published the initial-access path into its deployment process or identified an actor.
- The provider's July 27 scope and Beaumont's longer observation window conflict; retain a broader evidence window until reconciled.
- No public count of affected clients, sites, page loads, visitors, replaced addresses, or diverted funds is available.
- The captured sample shows a hostname-and-path transmission attempt. It does not prove successful receipt, and Adform reports no evidence of such transmission to date.
- Platform-wide customer and daily-ad figures do not measure incident impact and should not be used as an exposure estimate.

## Related pages
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [Silent Swap Google Notes crypto clipper](silent-swap-google-notes-crypto-clipper.md)
- [VPN Go browser-extension clipboard stealer](vpn-go-browser-extension-clipboard-stealer.md)
- [SourTrade browser-assembled malware malvertising](sourtrade-browser-assembled-malware-malvertising.md)

## Sources
- Adform: [Security Incident](https://site.adform.com/resources/newsroom/security-incident-company-update/)
- Kevin Beaumont, DoublePulsar: [Adform compromised to serve crypto stealer via supply chain attack](https://doublepulsar.com/adform-compromised-to-serve-crypto-stealer-via-supply-chain-attack-2f1ec024f33e)
- Adform Help: [Custom Naming JavaScript implementation documentation](https://www.adformhelp.com/hc/en-us/articles/10023216886545-Custom-Naming-JavaScript)
- The Hacker News: [Hackers Poison Adform Script to Swap Crypto Wallet Addresses Across Customer Sites](https://thehackernews.com/2026/08/hackers-poison-adform-script-to-swap.html)
