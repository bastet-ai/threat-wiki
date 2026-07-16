# Lucide Proxy npm browser DDoS botnet

## Summary
JFrog Security Research reported a campaign of **148 npm packages** that abused the registry as a CDN for student web-proxy applications rather than as traditional dependency malware. The packages presented a working proxy branded **Lucide** and disguised as **Riverbend Tutoring** or **Northstar Tutoring**, but the browser-side application loaded mutable remote JavaScript and a Wisp-compatible WebSocket traffic generator that could turn visitors' browsers into DDoS nodes.

The first package wave began on May 27, 2026 under npm account `terminal3airport`; a newer wave followed on July 8, 2026 under `eerikakirk`. JFrog said many packages were removed, but some remained active at publication time, including `charlie-kirk` versions `2.0.0` and `3.0.1`.

## Tags
- ops
- operations
- npm
- browser malware
- DDoS
- botnet
- web proxy
- malvertising
- package registry abuse
- JFrog
- student targeting

## Why this matters
- This was **not** an install-script compromise. The risk is to users who visit hosted proxy instances and to environments that allow npm-hosted static assets to become public application infrastructure.
- The campaign combines package-registry abuse, student-targeted proxy lures, popunder advertising revenue, mutable remote code loading, service-worker/cache persistence concerns, and browser-based traffic generation.
- Defender scope is different from normal npm malware triage: schools, corporate networks, DNS filters, browser caches, and endpoint web telemetry matter as much as developer lockfiles.

## Campaign shape
JFrog described two overlapping waves:

| Wave | Start | npm account | Notes |
| --- | --- | --- | --- |
| Initial wave | 2026-05-27 | `terminal3airport` | SafeDep previously documented 141 packages as adware / proxy spam; JFrog's deobfuscation found the DDoS-capable traffic generator. |
| Newer wave | 2026-07-08 | `eerikakirk` | Added packages / versions; JFrog reported some active packages remained during its publication window. |

Representative package names and families include `charlie-kirk`, `ilovefemboys`, `miguelphonk`, `testdonotredeemit`, `acidic`, `backupgenuine-updated`, `bismillahitidakimas`, `captainindia`, `crazynut`, `fflc-updated`, `kirkland`, `omglucidesotuff`, `changiairportpromax`, plus numbered families such as `abuden`, `imillegal`, `ishowfeet`, `nottuff`, `ratelimitsucks`, `sixseven`, `speed`, `backupsitetuff`, `timmytuffknuckles`, and `backup*-updated` variants.

## Execution chain
1. The application loads from `index.html` and runs `assets/73sxysj46r.js`, a 5.4 MB single-line obfuscated JavaScript bundle.
2. Static deobfuscation exposed two hidden modules that run before the visible proxy interface renders:
   - a mutable remote JavaScript loader, backed by jsDelivr / GitHub-hosted content;
   - a Wisp-compatible WebSocket traffic generator.
3. The visible proxy continued to work for students seeking to bypass web filters, while hidden code connected visitors into a remotely controlled traffic-generation network.
4. JFrog's recovered historical payloads showed an operational window in late May where visiting browsers could be used as high-volume HTTP flood participants.

## Infrastructure and indicators
JFrog published these durable pivots:

### Domains / URLs
- `https://cdn.jsdelivr.net/gh/canyoupleasesaysomething/cdn@main/cdn.js`
- `https://cdn.jsdelivr.net/gh/canyoupleasesaysomething/cdn@main/websocket.txt`
- `https://cdn.caan.edu/-/?v=`
- `https://woofbeginner.com/jivd2xu8`
- `https://woofbeginner.com/0a/91/35/0a913561831bdf2c26dcf18b852b5cc1.js`
- `https://wisp.breadarchive.dpdns.org`
- `https://21baseballacademy.com`
- `https://lucideon.top`
- `https://c.vipersfutbol.com/script.js`
- `https://realizationnewestfangs.com`
- `https://protrafficinspector.com/stats`
- `https://preferencenail.com/sfp.js`
- `https://skinnycrawlinglax.com/dnn2hkn8`
- `https://cdn.conditionfuneral.com`

### Infrastructure IPs
- `92.38.177.17`
- `92.38.177.10`
- `153.75.225.178`
- `5.188.124.67`
- `92.38.177.16`
- `92.38.177.37`

### Campaign identifiers
- Google Analytics ID: `G-0VL3ZSBXDH`
- Publisher placement: `0a913561831bdf2c26dcf18b852b5cc1`
- Popunder key: `c6851a038da578a80eeb201e0588c84c`
- Developer emails: `main@geeked.wtf`, `me@geeked.wtf`, `stefanvangetson54@gmail.com`

### Payload hashes
- `eb4e1394d537d8eba509dd5c57e7aaf4c1df57715c7161330012a11f6202af84` — `assets/73sxysj46r.js`
- `10ddbbae0070267b8d15888b09a3cdb19fa74d861315b71f21c9ace8b9f85c75` — `assets/script.js`
- `4b188d179e50e8208a6efec85e273e88d8fc390c836f299ba12915e0840408fd` — archived HTTP flood payload

## Response guidance
1. Block the listed domains and Wisp endpoints in school, corporate, and managed-browser networks.
2. Hunt for visits to Lucide / Riverbend Tutoring / Northstar Tutoring proxy instances, especially from student or shared lab endpoints.
3. Clear browser cache, cookies, and site data for affected proxy domains; unregister suspicious service workers associated with tutoring or proxy domains.
4. Audit dependency manifests and lockfiles for campaign package names, but do not treat lockfile presence as the only exposure path.
5. Detect browser-originated high-volume WebSocket or HTTP traffic to the listed infrastructure, especially when the initiating tab is a tutoring/proxy/game-unblocker page.
6. Treat npm-hosted static web apps as untrusted internet content; package-registry allowlists do not make browser-delivered JavaScript safe.

## Related pages
- [wshu.net npm credential-stealer campaign](wshu-net-npm-credential-stealer-campaign.md)
- [Operation Muck and Load GitHub lure network](operation-muck-and-load-github-lure-network.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)

## Sources
- JFrog Security Research: <https://research.jfrog.com/post/lucide-proxy-npm-malware-campaign/>
- The Hacker News: <https://thehackernews.com/2026/07/148-npm-packages-disguised-as-student.html>
