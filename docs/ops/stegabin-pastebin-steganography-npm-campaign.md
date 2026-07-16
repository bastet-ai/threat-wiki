# StegaBin Pastebin-steganography npm campaign

## Summary
Socket reported **StegaBin** as a February 2026 developer-targeting npm campaign tied to North Korea's Contagious Interview activity. Twenty-six malicious npm typosquats used install-time execution to load an obfuscated `vendor/scrypt-js/version.js` file, decode command infrastructure hidden inside Pastebin text via character-level steganography, fetch platform-specific payloads from Vercel-hosted infrastructure, and deploy a RAT plus automated infostealer modules.

## Tags
- ops
- operations
- supply-chain
- npm
- typosquatting
- developer-targeting
- credential-theft
- RAT
- infostealer
- Pastebin
- Vercel
- Contagious Interview
- FAMOUS CHOLLIMA
- Lazarus
- North Korea

## Why this matters
- The campaign shows a resilient dead-drop pattern: Pastebin hosted innocuous-looking essays where selected characters encoded the C2 list.
- The malicious packages proxied or depended on the legitimate libraries they impersonated, delaying discovery because builds could continue working after compromise.
- The final payload targeted developer machines directly, including VS Code configuration, SSH keys, Git repositories, browser credential stores, clipboard data, crypto wallets, and local secrets.
- Socket captured the post-exploitation payload suite by simulating a compromised host, giving defenders a higher-confidence view of automated C2 behavior than package static analysis alone.

## Reported chain
1. Twenty-six npm typosquats were published across February 25-26, 2026, each under a throwaway account.
2. The packages declared install scripts such as `node ./scripts/test/install.js`.
3. `install.js` loaded the real payload from `vendor/scrypt-js/version.js`, a path chosen to look like vendored cryptographic library code.
4. `version.js` used RC4 string encryption, array rotation, anti-debug logic, and control-flow flattening, then decoded three Pastebin dead drops.
5. The Pastebin pages contained benign-looking computer-science text with systematic character substitutions; the decoder stripped zero-width characters, read a length marker, extracted evenly spaced characters, and split the result on `|||`.
6. The decoded list contained 31 Vercel-hosted domains, with `ext-checkdin[.]vercel[.]app` returning live payloads at Socket's analysis time.
7. The loader requested platform-specific shell payloads from `/api/m`, `/api/l`, or `/api/w` for macOS, Linux, and Windows.
8. A token-gated bootstrapper installed Node.js / Python dependencies as needed, downloaded `parser.js` and `package.json`, launched the RAT, and deleted itself.
9. `parser.js` connected to `103[.]106[.]67[.]63:1244` and accepted `cd` and `ss_exec` operations.
10. The C2 automatically deployed nine infostealer modules after a simulated host checked in.

## Package and infrastructure notes
Socket described the packages as typosquats of high-usage libraries across HTTP frameworks, utilities, database clients, auth/crypto, messaging, test/build tooling, and process management. Recurring `-lint` suffixes made several packages look like plausible developer tooling.

Socket identified nine packages not covered by the earlier kmsec.uk disclosure:

- `formmiderable`
- `bubble-core`
- `mqttoken`
- `windowston`
- `bee-quarl`
- `kafkajs-lint`
- `jslint-config`
- `zoddle`
- `hapi-lint`

Account naming clustered around coordinated personas including `christopher.smith.*47`, `andrew.*walker*`, and `joni*`.

## Indicators and hunt pivots
- Shared malicious file: `vendor/scrypt-js/version.js`
- Shared file SHA-256: `da1775d0fbe99fbc35b6f0b4a3a3cb84da3ca1b2c1bbac0842317f6f804e30a4`
- Install hook pattern: `node ./scripts/test/install.js`
- Pastebin dead drops:
  - `hxxps://pastebin[.]com/CJ5PrtNk`
  - `hxxps://pastebin[.]com/0ec7i68M`
  - `hxxps://pastebin[.]com/DjDCxcsT`
- Live Vercel domain at analysis time: `ext-checkdin[.]vercel[.]app`
- Additional decoded Vercel examples: `cleverstack-ext301[.]vercel[.]app`, `cleverstack-app998[.]vercel[.]app`, `brightlaunch-ext742[.]vercel[.]app`
- RAT C2: `103[.]106[.]67[.]63:1244`
- Payload endpoints: `/api/m`, `/api/l`, `/api/w`
- Decoy response to some non-`curl` requests: `Permanently suspended`

## Defender heuristics
- Treat npm install scripts in typosquats and lookalike developer-tool packages as endpoint compromise risks, not package-quality issues.
- Hunt for package installs that access Pastebin, Vercel, and shell-pipe payload endpoints during `npm install`.
- Look for vendored-library paths that unexpectedly contain obfuscated loader code, especially under names copied from legitimate crypto packages.
- Alert when developer endpoints download and execute platform-specific shell payloads from serverless preview/deployment platforms.
- If exposed, isolate the workstation before rotating secrets; the post-exploitation modules target SSH keys, Git repositories, VS Code state, browser credentials, crypto wallets, and clipboard data.

## Attribution notes
Socket assessed the tradecraft and infrastructure as consistent with FAMOUS CHOLLIMA and the broader North Korea-linked Contagious Interview activity associated with Lazarus. Track the package cluster separately from the actor label when recording detections, because future copycats may reuse Pastebin/Vercel dead-drop mechanics without sharing attribution.

## Related pages
- [js-logger-pack Hugging Face exfiltration campaign](js-logger-pack-hugging-face-exfiltration.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Polymarket npm wallet-drainer packages](polymarket-npm-wallet-drainer.md)
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- Socket: <https://socket.dev/blog/stegabin-26-malicious-npm-packages-use-pastebin-steganography>
- kmsec.uk disclosure referenced by Socket: <https://kmsec.uk/blog/dprk-text-steganography/>
