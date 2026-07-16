# Adblock for YouTube BadBlocker remote-script injection risk

## Summary
Island Security Research documented **Adblock for YouTube** (`cmedhionkhpnakcndndgjdbohmhepckk`), a Chrome Web Store extension with more than 11 million installs, a 4.4-star rating, and Featured-style user trust, as a high-blast-radius browser-extension risk. Island did **not** report observing a malicious payload delivered to users, but found production code and backend design that could let one server-side configuration change inject arbitrary JavaScript into pages without a Chrome Web Store update, review cycle, or visible browser prompt.

The risk comes from a YouTube-focused extension requesting `<all_urls>`, using a weak `youtube.com` substring gate, fetching remote rules every 24 hours from `api.adblock-for-youtube.com`, and allowing remote `scripletsRules` to drive `chrome.scripting.executeScript` in the page's `MAIN` world. That combination can turn an ad-blocking rule channel into a browser-session execution plane for webmail, SaaS apps, admin panels, internal tools, and other sensitive pages if the backend or operator intent changes.

## Tags
- ops
- operations
- browser extension
- Chrome Web Store
- Adblock for YouTube
- BadBlocker
- Island Security Research
- remote script injection
- arbitrary JavaScript
- MAIN world injection
- `<all_urls>`
- ad blocker
- browser session risk
- SaaS exposure
- extension supply-chain
- adware history

## Why this matters
- Browser extensions are durable, high-privilege supply-chain dependencies: once installed, a remote configuration plane can affect millions of browsers faster than enterprise endpoint controls may notice.
- Island's core finding is a **latent capability**, not confirmed active theft. Treat it as high-risk exposure and configuration-control failure, while preserving that caveat in incident communications.
- Ad blockers often receive broad host permissions for legitimate reasons. The defensible boundary is narrow, auditable rule handling — not all-site code execution controlled by a backend service.
- The extension's reported history increases risk: Island tied the ecosystem to sister ad-blocking extensions later removed for malware and to older ad-injection SDK behavior.

## Reported extension and infrastructure

| Item | Value |
| --- | --- |
| Extension name | `Adblock for YouTube` / `Adblock for YouTube™` |
| Chrome extension ID | `cmedhionkhpnakcndndgjdbohmhepckk` |
| Reported install base | 11M+ per Island; 10M+ in The Hacker News summary |
| Reported rating / reviews | 4.4 stars and roughly 374,000 reviews per Island |
| Remote rules endpoint | `https://api.adblock-for-youtube.com/api/v2/rules?version=7.2.1` |
| Historical related infrastructure | `get.adblock-for-youtube.com`, `update.adblock-for-y.com` |
| Related removed extensions named by Island | `Adblock for Chrome` (`onomjaelhagjjojbkcafidnepbfkpnee`), `Adblock for You` (`ogcaehilgakehloljjmajoempaflmdci`) |
| Separate remote configuration domain for related extension | `abu-xt.com` |

## Technical chain
1. The extension presents itself as a YouTube ad blocker, but its manifest includes `"host_permissions": ["<all_urls>"]`, giving it access to every visited site.
2. A pre-injection gate checks whether the full URL string contains `youtube.com`, rather than validating the hostname, frame origin, or YouTube-player context. Island showed non-YouTube pages can satisfy this check with URL parameters such as `?ref=youtube.com` or `?q=youtube.com`.
3. Roughly every 24 hours, the extension fetches remote rules from `api.adblock-for-youtube.com`.
4. The response includes normal ad-blocking material as well as `scripletsRules`, allowing the server to select scriptlets and arguments.
5. The extension constructs script text and calls `chrome.scripting.executeScript` with `world: 'MAIN'`, which runs inside the page context rather than only in an isolated extension world.
6. Island reported this creates the ingredients for arbitrary JavaScript execution across sensitive browsing sessions if a server-side rule change selects a powerful scriptlet or supplies hostile code.

## Defender heuristics
- Inventory Chrome / Chromium extension installations for ID `cmedhionkhpnakcndndgjdbohmhepckk` across managed and unmanaged browsers.
- In managed Chrome environments, block or at least force-review extensions with `<all_urls>`, remote-rule execution, or `chrome.scripting.executeScript` capability unless there is a documented business owner and review trail.
- Hunt proxy / DNS / EDR telemetry for requests to `api.adblock-for-youtube.com`, `get.adblock-for-youtube.com`, `update.adblock-for-y.com`, and `abu-xt.com` from enterprise browsers.
- Review browser extension policy for "allowed because popular" exceptions. Popularity, Featured badges, and ratings are not a substitute for manifest and backend-behavior review.
- If the extension is present on privileged workstations, consider the browser session potentially exposed: review SaaS/admin activity during the install window and rotate session tokens where suspicious browser activity exists.
- Preserve the Island caveat: absence of observed malicious payload means response can prioritize exposure reduction and telemetry review, rather than assuming confirmed credential theft on every host.

## Related pages
- [Chrome live-wallpaper extension ad-fraud network](chrome-live-wallpaper-extension-ad-fraud.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- [Island Security Research](http://www.island.io/blog/badblocker-11-million-users-one-server-call-away-from-compromise)
- [The Hacker News](https://thehackernews.com/2026/06/chrome-ad-blocker-with-10m-installs.html)
