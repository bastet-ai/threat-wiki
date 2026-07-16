# Perplexity AI-spoofing Chromium extension search hijacker

## Summary
Microsoft Defender Security Research documented a malicious Chromium extension, **Search for perplexity ai** (`flkebkiofojicogddingbdmcmkpbplcd`), that spoofed Perplexity AI branding and routed user search activity through attacker-controlled infrastructure before showing expected search results. Google removed the extension after Microsoft's report.

The durable defender signal is not just the single removed extension ID. The chain combines AI-brand social engineering, `chrome_settings_overrides`, Manifest V3 `declarativeNetRequest` permissions, and a two-hop redirect design that captures full Omnibox queries and real-time search suggestions through `perplexity-ai[.]online` while preserving normal-looking search outcomes.

## Tags
- ops
- operations
- browser extension
- Chromium
- Chrome Web Store
- Microsoft Security Blog
- Microsoft Defender Security Research
- Perplexity AI
- AI brand impersonation
- search hijacking
- browser hijacking
- Manifest V3
- declarativeNetRequest
- chrome_settings_overrides
- Omnibox
- input capture
- privacy exposure
- browser session risk

## Why this matters
- Browser extensions can observe and alter high-value browser workflows. Search-provider overrides are especially sensitive because typed queries may include internal project names, customer names, credentials pasted into the wrong box, incident details, and privileged infrastructure terms.
- AI branding is now a recurring lure class. Users may treat AI search assistants as productivity tooling rather than browser-control software, lowering scrutiny of permissions and store listings.
- The redirect chain is quiet by design: users still land on legitimate search providers, so the visible browsing experience may not reveal that query data was processed by an intermediary domain first.
- MV3 and DNR are legitimate extension mechanisms. Detection should correlate the declared purpose, requested permissions, host permissions, default-search overrides, and non-vendor infrastructure rather than keying only on one API.

## Reported extension and infrastructure

| Item | Value |
| --- | --- |
| Extension name | `Search for perplexity ai` |
| Extension ID | `flkebkiofojicogddingbdmcmkpbplcd` |
| Manifest version | MV3 |
| Extension version | `2.2` |
| Referenced brand | Perplexity AI |
| Suspicious domain | `perplexity-ai[.]online` |
| Search URL | `hxxps://perplexity-ai[.]online/search/{searchTerms}` |
| Suggest URL | `hxxps://perplexity-ai[.]online/search?output=firefox&q={searchTerms}` |
| Installation / onboarding URL | `extension.tilda[.]ws/perplexityai` |
| Status in Microsoft report | Reported to Google and taken down |

## Technical chain
1. The user installs a Chromium extension that resembles a Perplexity AI search assistant.
2. The manifest sets a default search provider through `chrome_settings_overrides`, including `"is_default": true`, a `search_url`, and a `suggest_url` hosted on `perplexity-ai[.]online`.
3. Full searches and real-time suggestion traffic are sent to the lookalike domain before the browser is redirected to the expected search provider.
4. The extension requests `declarativeNetRequest`, `declarativeNetRequestFeedback`, and `declarativeNetRequestWithHostAccess`, plus host access to `perplexity-ai[.]online`.
5. Microsoft observed modular rule resources for Perplexity, Bing, and Google redirection. The attacker-controlled first hop can log queries, headers, IP address, and user-agent; the second hop preserves the appearance of normal search results.
6. Microsoft noted that shipped server-side code (`server.js`) explicitly logged incoming requests, supporting data-collection intent. Microsoft did not report confirmed credential theft beyond search and suggestion interception capability.

## Defender heuristics
- Inventory managed and unmanaged Chromium-family browsers for extension ID `flkebkiofojicogddingbdmcmkpbplcd` and remove it where present.
- Hunt DNS, proxy, and EDR network telemetry for `perplexity-ai.online` and the defanged equivalent `perplexity-ai[.]online`; treat traffic from browser processes as likely extension-mediated interception.
- Review extension inventories for combinations of:
  - `chrome_settings_overrides` with `is_default=true`;
  - `search_url` or `suggest_url` pointing to a domain not controlled by the impersonated vendor;
  - `declarativeNetRequest*` permissions in a search-assistant extension;
  - `host_permissions` scoped to newly registered, typosquatted, or AI-brand lookalike domains.
- In Microsoft Defender telemetry, pivot on file or folder paths containing `flkebkiofojicogddingbdmcmkpbplcd`, and on network events where `RemoteUrl` contains `perplexity-ai.online`.
- For high-risk users, review recent browser search history, SaaS/admin session activity, and sensitive queries during the install window. Rotate exposed secrets only when query or session evidence suggests leakage; the public report confirms search/suggestion interception capability, not broad credential theft.
- Enforce browser-extension allowlists for privileged workstations and require security review for default-search overrides, all-site network manipulation, and AI-branded extensions that are not published by the legitimate vendor.

## Related pages
- [StegoAd Edge extension steganography campaign](stegoad-edge-extension-steganography-campaign.md)
- [Adblock for YouTube BadBlocker remote-script injection risk](adblock-for-youtube-badblocker-remote-script-injection.md)
- [Chrome live-wallpaper extension ad-fraud network](chrome-live-wallpaper-extension-ad-fraud.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)

## Sources
- [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/29/chromium-extension-uses-airelated-branding-redirect-browser-search/)
