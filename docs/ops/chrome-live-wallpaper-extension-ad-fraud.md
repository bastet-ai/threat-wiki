# Chrome live-wallpaper extension ad-fraud network

## Summary
Socket Threat Research reported a financially motivated Chrome Web Store operation using **152 new-tab “live wallpaper” extensions** built from one shared codebase and spread across **38 publisher accounts**. Socket assessed the family as adware-adjacent potentially unwanted programs (PUPs): the extensions override the new-tab page, report install / uninstall activity to operator domains, and in a 54-extension subset forge Google organic-search attribution so extension-driven visits look like normal Google search clicks.

Track this as an operation because the durable defender lesson is browser-extension supply-chain trust: low-permission, store-listed extensions can still manipulate telemetry, misrepresent privacy practices, and survive takedown pressure by cloning one template across many publisher identities.

## Tags
- ops
- operations
- browser-extensions
- Chrome Web Store
- adware
- PUP
- traffic-fraud
- privacy
- telemetry
- browser-security
- Socket Security Research

## Why this matters
- Socket found roughly **105,000 reported installs** across the family; Chrome Web Store install buckets mean this is an approximate floor, not exact telemetry.
- The extensions declared in Chrome Web Store privacy fields that they did not collect or use user data, while Socket said the linked operator privacy policy described logging IP address, ISP, referrer, click data, and extension use.
- A 54-listing `tabplugins[.]com` subset sent install traffic with forged `utm_source=google&utm_medium=organic` tags and wrapped uninstall pings in a `google.com/url` redirect to make extension-driven traffic appear to be Google organic search.
- The campaign used fragmentation as an evasion layer: one shared template was distributed through dozens of Chrome Web Store publisher accounts rather than one easy-to-remove account.
- Socket reported an IndexedDB enumerate-and-delete routine copied into every analyzed service worker. Socket scoped the impact to the extension origin, but treated the behavior as an anti-forensic family fingerprint with no legitimate wallpaper-extension purpose.

## Reported chain

### Extension template and publisher spread
- Socket collected **152 unique extension IDs**.
- Socket downloaded and SHA-256-verified `js/bg.js` for 141 extensions; the remaining 11 were already delisted when Socket checked.
- Across the 141 live listings, Socket observed the same template across **38 publisher accounts**.
- Socket highlighted three shared brand backends:
  - `tabplugins[.]com` — 109 analyzed extensions, including the newer template with forged Google attribution and cloaked uninstall redirect.
  - `yowgames[.]com` — 19 extensions, using a games-themed front without the forged Google attribution.
  - `chromewallpaper[.]com` — 13 extensions, structurally similar to the `yowgames` variant.

### Traffic laundering
- The `tabplugins[.]com` service worker hardcoded install and uninstall URLs.
- On install, the extension opened an operator-controlled `tabplugins[.]com` URL tagged as Google organic traffic even though the user arrived through extension behavior.
- On uninstall, the extension used `chrome.runtime.setUninstallURL` with a `google.com/url` wrapper, which Socket described as disguising the operator ping as a Google search-result click.
- Socket assessed the harm as measurement integrity and privacy abuse rather than remote-code execution: advertisers, affiliate systems, or analytics consumers see inflated “organic” traffic created by extension navigation.

### Privacy and telemetry contradiction
- Chrome Web Store listings reportedly stated that the developer would not collect or use user data.
- Socket said linked privacy policies for the operator domains contradicted that claim by describing logging of extension use, IP address, ISP, referrers, clicks, and ad-network sharing.
- Treat store privacy disclosures for cloned extension families as assertions to verify, not proof that the extension avoids telemetry.

### Anti-forensic fingerprint
- Socket reported the literal console string `Deleted IndexedDB database:` in the shared `js/bg.js` service worker.
- The routine enumerated and attempted to delete IndexedDB databases on each service-worker start.
- Socket emphasized that Manifest V3 origin partitioning limits this to the extension's own `chrome-extension://<id>` origin in the observed build, so it was not wiping arbitrary website IndexedDB stores.
- The behavior remains useful for defenders because the same boilerplate appears across the family and is unusual for a wallpaper new-tab extension.

## Defender heuristics

### Enterprise browser control
- Inventory installed Chrome / Chromium extensions that override the new tab page, request `search`, or come from unfamiliar “live wallpaper” publishers.
- Remove or block new-tab live-wallpaper extensions tied to `tabplugins[.]com`, `yowgames[.]com`, or `chromewallpaper[.]com` unless there is a documented business requirement.
- Prefer extension allow-lists for managed browsers; treat mass-produced lifestyle extensions as higher-risk even when they are not classic malware.
- Review extension privacy disclosures against the linked privacy policy and observed network behavior.

### Endpoint and network hunting
- Search unpacked extension bundles or browser extension caches for:
  - `Deleted IndexedDB database:`
  - `utm_source=google&utm_medium=organic`
  - `tabplugins[.]com`
  - `yowgames[.]com`
  - `chromewallpaper[.]com`
- Review proxy, DNS, and browser telemetry for unexpected new-tab navigation or install / uninstall pings to the operator domains.
- Use publisher-account fragmentation as a hunting clue: one takedown or one extension ID is not enough if the same background script appears across multiple listings.

### Browser-extension review lessons
- Do not rely only on permission count. A low-permission extension can still manipulate analytics, override new-tab behavior, and create privacy exposure.
- Compare claimed extension purpose with actual install, uninstall, and background-service-worker behavior.
- Flag wallpaper, game, coupon, and new-tab extensions that reuse identical code across many publisher accounts or domains.

## Related pages
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Socket Security Research: <https://socket.dev/blog/152-chrome-live-wallpaper-extensions-hid-ad-tracking>
