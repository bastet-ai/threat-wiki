# Joyfill npm blockchain-RAT compromise

## Summary
Socket Research reported on July 28, 2026 that beta releases in the legitimate `@joyfill` npm namespace contained an import-time JavaScript implant. Socket initially analyzed one release of each package; a same-day StepSecurity follow-up expanded the affected set to six `2773` prereleases across `@joyfill/layouts` and `@joyfill/components`. The functional layouts release resolved encrypted code through Tron, Aptos, and BNB Smart Chain transactions, recovered a 77 KB Node.js remote-access trojan, and launched a separate detached downloader. The same source-level injection reached components, although Socket found that a throwing dynamic-`require` shim limited normal execution in the first components artifact it analyzed.

The loader has exact PolinRider-family fingerprints, while the recovered RAT and live downstream captures overlap with DEV#POPPER and an OmniStealer-like Python credential stealer. Socket explicitly described these as malware-family assessments, not attribution of the Joyfill compromise to a particular actor.

## Tags
- ops
- operations
- supply-chain
- npm
- maintainer compromise
- import-time execution
- developer targeting
- blockchain C2
- PolinRider
- DEV#POPPER
- OmniStealer
- Node.js
- credential theft
- remote access trojan

## Affected releases
- `@joyfill/layouts@0.1.2-2773.beta.0`, `0.1.2-2773.beta.1`, and `0.1.2-2773.beta.2` — StepSecurity found the injected block prepended to `dist/index.cjs.js` and `dist/index.es.js`; Socket recorded beta.0 as published at `2026-07-28T10:54:57.311Z` and confirmed its CommonJS entrypoint executes the implant when imported.
- `@joyfill/components@4.0.0-rc24-2773-beta.4`, `4.0.0-rc24-2773-beta.5`, and `4.0.0-rc24-2773-beta.6` — StepSecurity found the injected block appended to `dist/index.js`, `dist/index.esm.js`, and `dist/joyfill.min.js`; Socket recorded beta.4 as published at `2026-07-28T11:03:59.568Z` but found that its bundled dynamic-`require` shim prevents normal dependency resolution through the analyzed path.

Socket found the preceding `@joyfill/layouts@0.1.1` and `@joyfill/components@4.0.0-rc24` releases clean and did not find the signature in other public `@joyfill` packages it checked. The shared `2773` prerelease marker, publisher identity, and bundle source maps show that the implant was present at build time, but public evidence does not yet distinguish developer-workstation, repository, CI, or publishing-credential initial access.

## Execution and payload chain
1. The implant is appended to legitimate package code and runs when Node.js loads the package; it does not require an npm lifecycle script.
2. An obfuscated bootstrap exposes Node.js module primitives through globals, sets marker `A9-0135-3`, and starts two payload-resolution branches.
3. The in-process branch uses a hard-coded Tron address, with Aptos fallback, to obtain a BSC transaction hash. It reverses, decodes, and XOR-decrypts the BSC transaction input before evaluating it.
4. A second blockchain hop recovers a 77,276-byte Node.js RAT. The RAT uses Socket.IO and supports JavaScript and shell execution, upload, file management, host discovery, clipboard collection, and additional payload retrieval.
5. A parallel branch launches detached `node -e` execution, requests `23[.]27[.]13[.]43/$/boot` with `Sec-V: A9-0135-3`, decrypts the response, and evaluates it. The detached process can outlive the build, test, or CLI command that imported the package.
6. Matching live boot captures can provision Python and retrieve a cross-platform credential stealer. Socket assessed with medium likelihood that the captured Python payload is an OmniStealer iteration; it cautioned that the captures lack request provenance proving every infected Joyfill host received that payload.

The use of public blockchain transactions makes payload selection mutable without republishing the package. Blocking one conventional C2 address does not stop the initial resolution path.

## Capabilities and persistence
The recovered RAT identifies hosts with a client UUID, PID, hostname, OS details, and timestamps. It can execute supplied code or shell commands, upload and modify files, query public IP information, and read clipboards through PowerShell, `pbpaste`, `xclip`, or `xsel`.

It can persist by injecting self-reloading code into developer applications and tooling, including:
- `@vscode/deviceid` under VS Code, Cursor, and Antigravity;
- Discord Desktop's core module;
- GitHub Desktop `resources/app/main.js`;
- the global npm CLI at `node_modules/npm/lib/cli.js`.

Observed injection markers include `/*C250617A*/`, `/*C250618A*/`, `/*C250619A*/`, `/*C250620A*/`, `/*C260511A*/`, `/*C260512A*/`, and `/*RS260605*/`.

The matching Python stealer collects environment and host data, browser credentials and cookies, wallet and password-manager extension storage, Git credentials, GitHub CLI configuration, VS Code storage, GitHub Desktop logs, and platform credential stores. It stages data under `%USERPROFILE%\.npm` or `/tmp/.npm` before encrypted upload.

## High-value indicators
### Network and protocol
- `166[.]88[.]134[.]62:443` and `166[.]88[.]134[.]62:80`
- `23[.]27[.]13[.]43/$/boot`
- `198[.]105[.]127[.]210:443` and `198[.]105[.]127[.]210:80`
- `23[.]27[.]202[.]27:443` and `23[.]27[.]202[.]27:27017`
- header `Sec-V: A9-0135-3`
- `api[.]trongrid[.]io`, `fullnode[.]mainnet[.]aptoslabs[.]com`, `bsc-dataseed[.]binance[.]org`, and `bsc-rpc[.]publicnode[.]com`

### SHA-256
- layouts archive: `adc4af90540d33cd1e98f44b51482ae9250fbeb97d6f8d7841c81b618cb2c6e6`
- components archive: `bcc93dc55bc7daedf4ca57254f0e7a7f1c40e09851eab98fe10cde801982db17`
- first blockchain-resolved loader: `cb46f12d70824ea24ed1f8bcf45bf3f86680e02a9089aafc03b27f691be57be3`
- detached bootstrap: `78f0de8682e0e894a5784eb7e95db4da6088f528918ca3107dd1e76f80a561d8`
- final Node.js RAT: `26351aed0397158d3a3b8cc8fd3047d4c015d264c9895f10f20f1521b974ed18`
- matching Python stealer capture: `36ff00b45e67baa7e3674b0c80f48e88737264c61e5c6b3b091200972de8157c`

Socket's source report contains the full file-hash, wallet/address, and transaction-hash set. Blockchain identifiers should be used as resolver and telemetry pivots, not as proof of actor identity.

StepSecurity additionally documented request paths `/$/boot`, `/u/e`, `/u/f`, `/0x/js`, `/verify-human/`, and `/snv`; `ip-api[.]com` as a lookup endpoint; and Tron addresses `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP`, `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG`, and `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`.

## Independent runtime validation
StepSecurity detonated all six `2773` versions in a sandbox with install-time and import-time observation. Installation produced no lifecycle-script or child-process activity, while importing loaded the compromised bundles. Direct payload detonation then reached `api[.]trongrid[.]io`, the two documented BSC RPC services, and the Aptos fallback, and recovered a live second stage from the attacker's on-chain transaction. This independently confirms that the blockchain resolver and downstream infrastructure were reachable during StepSecurity's July 28 testing; it does not prove that every package import completed the same path. Bundle diffs against clean siblings exposed roughly 333 lines of injected code and the decoded `global.r = require` assignment.

## Defender actions
1. Block and remove all six affected versions from lockfiles, caches, internal mirrors, images, and deployment artifacts. Avoid the packages' `beta` dist-tag pending public remediation confirmation.
2. Treat any system that **imported** an affected package as potentially compromised. `npm install --ignore-scripts` is not protective because this is module-load execution.
3. Isolate affected hosts and preserve endpoint, process, DNS, proxy, package, lockfile, CI, source-map, and registry-cache evidence before cleanup.
4. From a known-clean system, rotate npm and source-control credentials, cloud and Kubernetes secrets, SSH keys, browser sessions, wallet material, password-manager data, and other credentials reachable from the affected process.
5. Hunt for detached `node -e` processes; `Sec-V` requests; blockchain RPC traffic from developer or CI hosts; and unexpected modifications to VS Code, Cursor, Antigravity, Discord, GitHub Desktop, and global npm files.
6. If the Python follow-on may have run, inspect `%USERPROFILE%\.npm` and `/tmp/.npm`, and assume browser-saved credentials, cookies, extension storage, and platform credential stores were exposed.
7. Rebuild affected developer and CI systems from known-good media after evidence collection. Removing the package alone does not remove developer-tool persistence.

## Assessment caveats
- Public source maps prove that malicious code was present at bundle time, not which upstream trust boundary was first compromised.
- Socket found that the first components artifact did not execute normally through its analyzed bundle path. StepSecurity confirmed injected bundles across three components versions and separately demonstrated live blockchain resolution through direct payload detonation, but did not report that every normal package import completed downstream C2 execution; do not generalize either result to all versions or bundle paths.
- PolinRider, DEV#POPPER, and OmniStealer describe code and infrastructure overlap. They do not establish actor attribution for this incident.
- The live boot and Python captures match campaign keys and infrastructure but lack provenance proving universal delivery to affected Joyfill systems.

## Related pages
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)
- [Famous Chollima Packagist dev-branch loader](famous-chollima-packagist-dev-branch-loader.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- Socket Research: [Two Joyfill npm Beta Releases Compromised With Blockchain-Backed Remote Access Trojan Loader](https://socket.dev/blog/joyfill-npm-beta-releases-compromised)
- StepSecurity: [Compromised npm Packages: @joyfill/components and @joyfill/layouts Ship an Obfuscated Remote Access Trojan](https://www.stepsecurity.io/blog/joyfill-npm-supply-chain-compromise)
- npm registry: [`@joyfill/layouts`](https://www.npmjs.com/package/@joyfill/layouts) and [`@joyfill/components`](https://www.npmjs.com/package/@joyfill/components)
