# art-template Coruna-style iOS watering-hole compromise

## Summary
Socket reported that the npm package **`art-template`** was compromised in May 2026 and used to deliver a Coruna-style Safari/iOS watering-hole exploit framework to downstream websites that bundled affected browser builds.

The reported entry point was maintainer handoff rather than a direct registry-token theft: the original maintainer said an unknown actor acquired project control under the pretense of maintenance, then released packages containing external scripts and deleted related issues. Socket reported malicious behavior in `art-template` versions `4.13.3`, `4.13.5`, and `4.13.6`, with `4.13.5` and `4.13.6` injecting a plaintext remote script loader into `lib/template-web.js`.

## Tags
- ops
- operations
- supply-chain
- npm
- watering-hole
- iOS
- Safari
- WebKit
- exploit-kit
- Coruna
- package-takeover

## Why this matters
- This is a different npm supply-chain impact model from developer credential theft: the compromised package could become **client-side exploit delivery** for every website that bundled the browser build.
- The payload was gated for Safari/WebKit and iOS version ranges, making it look like exploit preconditioning rather than generic web skimming or phishing.
- Project handoff and issue suppression are durable trust-boundary signals: an apparently legitimate maintainer transition can become the initial access path for a browser exploit kit.

## Reported chain
1. Control of the `art-template` project/package moved to an unknown actor under a maintenance pretext.
2. Affected releases modified the browser bundle path (`lib/template-web.js`) to load attacker-controlled JavaScript.
3. Socket reported loader infrastructure including `git.youzzjizz[.]com/git.js`, `v3.jiathis[.]com/code/art.js`, and redirects into `utaq[.]cfww[.]shop/gooll/gooll.html`.
4. The final JavaScript framework, reported as `49554fde7424c31c.js`, targeted Safari/WebKit on iOS 11.0 through 17.2 and rejected non-target browsers and iOS 17.3+.
5. The framework beaconed public IP address, iOS version, and a campaign code to `l1ewsu3yjkqeroy[.]xyz`, then performed anti-bot checks, WebAssembly-based fingerprinting, architecture/version gating, and content-addressed remote payload fetches.

## Tradecraft notes
- Socket described version-specific WebAssembly memory-offset checks, JIT-compiled-code reads, architecture discrimination between ARM64 and ARM64_32, and hard version cutoffs as consistent with browser exploit delivery.
- The affected package versions did not need to execute on developer workstations during install; the danger was downstream execution in end-user browsers when the package was bundled into web applications.
- The reported overlap with Coruna is behavioral and technical; keep attribution cautious unless later primary reporting names an operator.

## Defender heuristics
- Search lockfiles, package-manager caches, SBOMs, bundled web assets, and CDN/deployment artifacts for `art-template` versions `4.13.3`, `4.13.5`, and `4.13.6`.
- Diff any bundled `lib/template-web.js` against a known-clean version; flag unexpected `loadScript()` calls or remote script URLs appended after the legitimate bundle.
- Hunt web telemetry for requests to `v3.jiathis[.]com/code/art.js`, `utaq[.]cfww[.]shop/gooll/`, `git.youzzjizz[.]com/git.js`, and `l1ewsu3yjkqeroy[.]xyz`.
- Treat exposed websites as possible watering-hole delivery points; remove the affected bundle, redeploy from clean dependencies, and review user-impact windows separately from developer-machine exposure.
- Add package handoff/account-transfer events and deleted issue reports to maintainer-risk monitoring, especially for packages that produce browser-executed assets.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)

## Sources
- Socket: https://socket.dev/blog/coruna-respawned-compromised-art-template-npm-package
