# macOS ClickFix fingerprinting-gate campaign

## Summary
Microsoft Threat Intelligence documented a macOS ClickFix operation that moved from openly serving malicious Terminal commands to revealing them only after a server-side browser-fingerprinting gate judged a visitor to be a likely genuine Mac user. The campaign uses more than **250 confirmed front-end domains**, often generated from dictionary words and the token `file`, and ultimately delivers the MacSync or Atomic Stealer (AMOS) information stealers.

The gate is the durable defender finding. The same URL can return a ClickFix lure, a blank or parked-looking page, or an unrelated browser-extension, VPN, or business decoy depending on the request. A benign response from a crawler or sandbox therefore does not clear the infrastructure.

## Tags
- ops
- operations
- ClickFix
- macOS
- Atomic Stealer
- AMOS
- infostealer
- social engineering
- user execution
- browser fingerprinting
- anti-analysis
- TDS
- cloaking
- credential theft
- cryptocurrency wallet theft
- Microsoft Threat Intelligence

## Why this matters
- Server-side qualification removes the malicious command from the initial response and reduces visibility to static scanners, crawlers, sandboxes, and researchers.
- The gate combines several ordinary browser signals. Detection should correlate its form-submission behavior, field names, domain-generation pattern, and downstream process activity rather than treat any one fingerprinting feature as malicious.
- ClickFix starts with a user-pasted Terminal command instead of a downloaded application bundle. This can avoid quarantine, code-signing, and notarization checks normally applied to downloaded macOS applications.
- The campaign's disposable front ends exceed 250 domains. Shared gate behavior and staging paths are more durable hunting pivots than a blocklist alone.
- MacSync and AMOS target high-value local material, including browser credentials, keychain data, SSH keys, authentication stores, cryptocurrency wallets, and other sensitive files.

## Delivery and infection chain
1. A victim reaches a look-alike domain, commonly following a `file<word><word>`-style naming pattern.
2. The initial response supplies a roughly 2.5 KB JavaScript profiling routine rather than the ClickFix command.
3. The script collects browser, display, hardware, page-context, and runtime attributes and silently submits the fingerprint to the same server.
4. The server returns blank, parked, or decoy content to requests that appear automated, virtualized, geographically unexpected, or inconsistent with the selected browser and platform.
5. A qualifying Mac visitor receives a counterfeit **Download for macOS** page with GitHub-themed branding, a forged **Verified Publisher** badge, and a button that copies an obfuscated `curl` one-liner. Microsoft states that the branding is spoofed and does not indicate a GitHub compromise.
6. After the user pastes and runs the command in Terminal, it retrieves a remote script from a `/curl/<id>` path. Multiple script stages then download and launch MacSync or AMOS.
7. The infostealer collects credentials, browser and wallet data, authentication stores, keys, and sensitive files for exfiltration.

## Fingerprinting and cloaking
The client builds a fingerprint from six browser objects: `navigator`, `screen`, `window`, `document`, `location`, and `console`. Reported attributes and checks include:

- claimed platform such as `MacIntel`, user agent, browser vendor, language, and plugins;
- screen and window dimensions, color depth, and pixel ratio;
- page title, referrer, character set, URL, and host;
- WebGL-derived GPU information used to distinguish likely Apple hardware from virtualized, emulated, software-rendered, or sandboxed environments;
- timezone offset, iframe execution, and touch-input support;
- a `toString()` counter that can change when an open developer console or logging tool serializes a temporary function;
- a `canPlayType("video/mp4")` tripwire that sets a `proto:true` signal when JavaScript-based codec spoofing reaches a hooked `Array.prototype.includes` path; and
- a fingerprint object carrying `mode: "php"` before same-origin submission.

Microsoft describes this as a traffic distribution system: the server selects what to deliver after evaluating the submitted profile. In testing, Windows-presenting requests received decoys such as a fake Urban VPN Proxy page or an unrelated logistics-company page, simple crawlers received empty or parked-looking content, and qualifying Mac requests received the lure.

## Domain and content pivots
Microsoft confirmed more than 250 campaign front ends. Many combine dictionary words with `file`, but some put the token in the middle or at the end and some omit it. Treat the naming convention as a clustering lead, not a standalone verdict.

Published examples:

| Domain | Reported role |
|---|---|
| `applefilevault[.]com` | ClickFix front end |
| `apricotfilepoint[.]com` | ClickFix front end; qualifying lure and non-qualifying decoy observed |
| `bananafastfile[.]com` | ClickFix front end |
| `cloudfilebridge[.]com` | ClickFix front end |
| `filecedarwallet[.]online` | ClickFix front end |
| `filecopperbasket[.]sbs` | ClickFix front end |
| `filecrimsonsignal[.]online` | ClickFix front end |
| `filemarblegarden[.]sbs` | ClickFix front end |
| `fileoceanhammer[.]sbs` | ClickFix front end |
| `filerubyfolder[.]sbs` | ClickFix front end |
| `filevelvettractor[.]sbs` | ClickFix front end |
| `lemonfilewave[.]com` | ClickFix front end |
| `limefilescope[.]com` | ClickFix front end |
| `mangocloudfile[.]com` | ClickFix front end |
| `orangesmartfile[.]com` | ClickFix front end |
| `syncdatavault[.]com` | ClickFix front end |
| `cloudsendhub[.]com` | ClickFix front end |

Additional content and traffic pivots:

- a minimal page that collects browser attributes and self-submits a hidden fingerprint to the same origin;
- a fingerprint field or object containing `mode: "php"`;
- dictionary-style `file<word><word>` domains combined with the gate behavior;
- counterfeit **Download for macOS** and **Verified Publisher** text;
- `/curl/<hex-id>` or similar staging paths; and
- different content from the same domain according to browser, hardware, runtime, or request context.

## Endpoint detection and response
- Alert when a browser visit is followed by Terminal or shell execution of `curl`, `base64`, `gunzip`, `zsh`, or `osascript`.
- Hunt sequences such as `curl` piped to `zsh`, `base64 -d`, and `xattr -c` followed by `chmod +x` and execution.
- Review `curl` downloads from newly registered or low-reputation domains, especially `/curl/<id>` paths and encoded or compressed responses.
- Detect unauthorized access to Keychain material, browser credential databases, SSH keys, authentication stores, and cryptocurrency-wallet files.
- Alert on sensitive-file archive creation followed by HTTP POST exfiltration.
- Correlate proxy or DNS sightings with browser history and endpoint process lineage; do not close an alert because a later fetch returned a benign decoy.
- Where infrastructure validation supports it, block shared staging or back-end hosts in addition to disposable front-end domains.
- Reinforce that legitimate downloads, CAPTCHAs, publisher verification, and software fixes do not require copying a website-provided command into Terminal.

Microsoft lists Defender behavior detections including `Behavior:MacOS/SuspAmosExecution`, `Behavior:MacOS/SuspOsascriptExec`, `Behavior:MacOS/SuspDownloadFileExec`, `Behavior:MacOS/SuspInfoExfil`, `Behavior:MacOS/SuspKeyChainCopy.AB`, `Behavior:MacOS/SuspInfostealExec`, `Behavior:MacOS/SuspCredCopy`, and `Behavior:MacOS/SuspPassSteal`.

Apple added a Terminal paste warning in macOS 26.4 and later for commands assessed as potentially malicious. Treat the warning as friction, not a substitute for web, network, and endpoint controls.

## Assessment limits
- Microsoft describes a campaign cluster and malware-delivery method but does not name or attribute the operator.
- More than 250 front-end domains were confirmed during Microsoft's tracking window; the complete population, victim count, and successful-infection count are not public in the cited report.
- Browser fingerprinting, WebGL checks, and traffic-distribution systems have legitimate uses. Confidence comes from correlated gate, infrastructure, lure, staging, and endpoint behavior.
- The listed domains are historical detection pivots. DNS, ownership, content, and server behavior can change.
- MacSync and AMOS are alternative reported outcomes of the chain; a front-end-domain sighting alone does not establish which payload, if any, executed.

## Related pages
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [TELEPUZ ClickFix / VIDAR campaign](telepuz-clickfix-vidar-campaign.md)
- [CrashStealer macOS notarized-dropper campaign](crashstealer-macos-notarized-dropper.md)
- [XCSSET v40 Xcode supply-chain campaign](xcsset-v40-xcode-supply-chain-campaign.md)

## Source
- Microsoft Security Blog: [From open lures to cloaked gates: How a macOS ClickFix campaign learned to hide](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/) — August 5, 2026
