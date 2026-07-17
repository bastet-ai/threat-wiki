# Contagious Interview SVG-steganography OtterCookie campaign

## Summary
Elastic Security Labs reported on July 18, 2026 a new **Contagious Interview**-aligned developer-targeting campaign, tracked as **REF9403**, after DPRK-aligned operators targeted Elastic's community Slack with a fake job posting and coding-challenge project.

The durable defender point: the repositories looked like functional ecommerce / coding-test projects, but hid payload fragments inside HTML comments embedded in SVG flag images. Running the project caused a JavaScript loader to reassemble and execute the payload, leading to a four-stage chain aligned with **OTTERCOOKIE**: browser and wallet theft, file theft, Socket.IO remote access, and clipboard theft.

## Tags
- ops
- operations
- Contagious Interview
- REF9403
- North Korea
- DPRK
- developer-targeting
- fake recruiting
- coding challenge
- GitHub
- SVG
- steganography
- JavaScript malware
- OtterCookie
- credential theft
- cryptocurrency wallet theft
- file theft
- clipboard theft
- Socket.IO
- RAT
- browser credential theft
- Elastic Security Labs

## Reported chain
1. The actor approached developers with a fake job posting and coding challenge / take-home assignment.
2. The supplied project was functional enough to appear legitimate, reducing suspicion during review or execution.
3. Payload chunks were Base64-encoded inside HTML comments across country-flag SVG files under an `assets/flags` directory, including normal-looking files such as `AE.svg` and `AF.svg`.
4. A repository JavaScript file named `serverValidation.js` read all `.svg` files in sorted order, extracted the comment bodies, concatenated the fragments, decoded them with a custom `Check()` function, and executed the result with `eval()`.
5. Elastic described a four-stage payload aligned with OTTERCOOKIE:
   - browser credential and cryptocurrency-wallet extension theft;
   - local file theft;
   - a Socket.IO-based remote access trojan capable of shell-command execution and follow-on payload delivery;
   - clipboard theft.
6. The browser/wallet module set its process title to `npm-cache`, enumerated Chrome-family browser profiles across Windows, macOS, and Linux, and collected `Login Data`, `Web Data`, and wallet-extension `Local Extension Settings` stores.
7. Elastic reported multipart HTTP POST exfiltration to `ldb.rightwidth[.]dev` endpoints including `/upload` and `/cldbs`, with User-Agent `axios/1.18.1`.

## Why this matters
- **Developer execution is the compromise boundary:** the risky action is running an apparently benign project, not installing a package from a registry.
- **Static review can miss distributed payloads:** malicious content is split across image files that still render as normal SVG assets.
- **The target set overlaps supply-chain blast radius:** browser sessions, wallet extensions, source-control credentials, cloud sessions, package-registry access, and AI/developer-tool context can all be reachable from developer endpoints.
- **The campaign tracks current developer tooling:** Elastic noted exclusions and file-scoping logic that show awareness of modern development environments and AI coding tooling directories such as `.claude`, `.cursor`, `.gemini`, `.windsurf`, `.pearai`, and `.llama`.

## Defender heuristics
- Treat unsolicited coding tests and take-home assignments as executable content. Review them in isolated environments with no logged-in browser, wallet, source-control, package-registry, cloud, or AI-assistant credentials.
- Search repositories for SVG files containing long HTML comments or Base64-like blobs, especially under `assets/flags` or other asset directories where payload fragments may hide in otherwise normal media files.
- Inspect project scripts for JavaScript that reads many asset files, sorts filenames, extracts comments with regexes such as `<!-- ... -->`, concatenates data, uses custom Base64 decoders, or calls `eval()` during server startup or validation routines.
- Hunt on developer endpoints for `node`/project processes renamed or presented as `npm-cache`, unexpected Socket.IO connections, suspicious `axios/1.18.1` POSTs, and requests to `/upload`, `/cldbs`, `/api/service/makelog`, or `/api/service/process/<uid>` on unfamiliar infrastructure.
- Monitor for browser credential-store access (`Login Data`, `Web Data`) and wallet-extension LevelDB reads from project-launched Node processes.
- If a coding-test project was run, isolate the endpoint before rotating credentials; then revoke browser sessions, source-control tokens, package-registry tokens, cloud/API keys, wallet secrets, and AI-tool credentials that were reachable from the host.

## Related pages
- [UNK_DeadDrop developer repository phishing](unk-deaddrop-developer-repository-phishing.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [StegaBin Pastebin-steganography npm campaign](stegabin-pastebin-steganography-npm-campaign.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)

## Sources
- Elastic Security Labs: [New North Korean campaign uses fake coding interviews to steal developer credentials](https://www.elastic.co/security-labs/contagious-interview-malware-svg-steganography)
- The Hacker News: [Fake Coding Tests Deliver OtterCookie-Aligned Malware Hidden in SVG Flag Images](https://thehackernews.com/2026/07/north-korea-linked-hackers-hide.html)
