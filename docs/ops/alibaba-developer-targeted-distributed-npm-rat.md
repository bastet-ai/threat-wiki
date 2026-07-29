# Alibaba developer-targeted distributed npm RAT campaign

## Summary
Socket Research reported on July 28, 2026 that an unattributed campaign split a malicious downloader across multiple npm packages and publisher accounts, then delivered a cross-platform remote-access trojan to environments that could resolve private Alibaba `@ali/*` dependencies. The lure packages copied names used by Alibaba's private development tooling, while individually plausible helper packages combined configuration retrieval with a Node.js `vm` escape and remote code execution.

The final `aone-cli` payload targets Alibaba-oriented developer and collaboration tooling, supports command execution, file transfer, reverse proxying, persistence, and DingTalk-assisted lateral movement, and was still backed by active infrastructure when Socket published. Socket assessed industrial espionage as the likely objective. Treat that objective and the Chinese-language artifacts as an assessment, not actor attribution.

## Tags
- ops
- operations
- supply-chain
- npm
- dependency confusion
- private packages
- developer targeting
- Alibaba
- Aone
- DingTalk
- remote access trojan
- cross-platform malware
- command execution
- lateral movement
- AI tools
- source-repository abuse
- credential theft
- industrial espionage

## Campaign and trust-boundary chain
Socket traced two related delivery paths:

1. `lib-mtop`, an unscoped lookalike for a private `@ali` package, received three new versions in late March 2026 and directly downloaded JavaScript with `curl` before loading it from disk. The sparse older package history suggests possible account takeover, but public evidence does not distinguish takeover from a malicious or rogue publisher.
2. A larger package cluster was staged across April 27–28. Top-layer lures copied private `@ali/*` package names and declared both the real private dependency and attacker-controlled `smart-config-manager`.
3. `smart-config-manager` pulled `cloud-config-fetcher` and `local-config-parser`, published through different accounts. Each helper looked consistent with its stated purpose when reviewed alone.
4. `cloud-config-fetcher` retrieved `preferences.json` from `smi1e2u/smart-config-manager` on GitHub and stored it as `.cloud-preferences.json`.
5. `local-config-parser` evaluated a disguised rule from that file. The rule escaped the Node.js `vm` sandbox through `items.constructor.constructor`, recovered `process` and module-loader access, and downloaded `setting.js` from Alibaba Cloud Object Storage.
6. `setting.js` profiled the host, suppressed or cleaned earlier artifacts, selected a platform path, and installed the final `aone-cli` RAT.

This is a compositional-evasion pattern: package-level review can miss malicious behavior when network retrieval, rule evaluation, sandbox escape, and execution are separated across dependencies and accounts.

## Reported npm packages
### Direct or early-stage packages
- `lib-mtop`
- `aone-kit`
- `aone-kit-cli`
- `aone-sandbox`
- `node-data-utils`
- `fast-transform-pipeline`

### Distributed loader and lure cluster
- `cloud-config-fetcher`
- `local-config-parser`
- `smart-config-manager`
- `aone-cloud-cli`
- `colder-cli`
- `def-open-client`
- `feedback-ai-sdk`
- `flight-compare-analyzer`
- `lwp-web-client`
- `lzd-unified-station-sdk`
- `open-worker-cli`
- `test-skill-zip`
- `uniapi-bridge`

Socket's IOC list omits `node-data-utils` from its final malicious-package block while describing it as an April 27 test of the multi-package delivery mechanism. Preserve that distinction when scoping confirmed installation versus campaign-adjacent publication.

## RAT behavior and persistence
The final payload uses an `aone-cli` name aligned with Alibaba's internal Aone research-and-development platform. Reported capabilities include:

- host and network discovery;
- arbitrary shell, JavaScript, and Python execution;
- upload, download, and additional payload staging;
- screenshot collection;
- encrypted reverse TCP proxying;
- Python and Node.js module installation;
- AI-tool poisoning and DingTalk lateral-movement commands.

Platform-specific behavior includes:

- **macOS:** adds a background command to `~/.zshrc` and a LaunchAgent that runs every 10 minutes;
- **Windows:** terminates the official Alilang security application and replaces its `app.asar` with a trojanized copy;
- **Linux:** runs a detached payload from `/tmp` and deletes the file after it is loaded;
- **developer/AI tooling:** injects marked Python code into `.skills` directories used by tools including DingTalk, Wukong, and Qoder so a Bun-hosted `script.js` is relaunched.

HTTP requests can carry fake `Origin` and `Referer` values of `https://alidocs.dingtalk.com` to blend with expected Alibaba collaboration traffic.

## High-value indicators
### Network and repository
- `smi1e2u/smart-config-manager`
- `aone-cli-next[.]oss-cn-beijing[.]aliyuncs[.]com`
- `aone-ai-cli[.]oss-cn-beijing[.]aliyuncs[.]com`
- `aone-kit[.]oss-cn-beijing[.]aliyuncs[.]com`
- `xemzqli2vu[.]ai-app[.]pub` — primary C2 reported by Socket
- `diamond-cli-znsxphqell[.]cn-shanghai[.]fcapp[.]run` — reverse-proxy WebSocket C2
- fake HTTP origin/referrer: `https://alidocs.dingtalk.com`

### Host and code
- `.cloud-preferences.json`
- injection marker `# __INJECT_MARKER__`
- environment variable `ROBOT_UID=3201d407b7899a12d6d439950511c6a5`
- unexpected `aone-cli`, `aone-kit-update`, `setting.js`, `crypto.js`, or `script.js` under developer-tool paths
- unapproved edits to Alilang `app.asar`, `.skills` Python files, `~/.zshrc`, or LaunchAgent definitions

### SHA-256
- `84a6ccaaab1596139d28e822f40cc99c68d337d4c81d1c6d9692c1d6bb22e4af` — malicious `preferences.json`
- `6044974c633b3a319c31bb32110411520c425e89722a64806528553227e7a50a` — `setting.js`
- `0910ecfa049738ef3f2540855341a380df89224ff71da94b4c21689fd66f62e3` — macOS `aone-cli.js`
- `b8b81af76163bdcc5b4f7d8fe6795f164991f8a62678c971db031b9e90a27813` — Linux `aone-cli`
- `ef9a1896eeaae929800eade768276e2240ef252d26d0d96c1950a1a5e1aadb34` — Windows `aone-cli.zip`
- `e5d8350f1540fe91145dc262c455bca7748ad97dafb2d9facd5adebed9f66d2d` — `aone-cli-deps.tar.gz`
- `41957bd0ba2d9c07af2e069f10780fdf6b2102c065bebe0db2136dfe07d67a28` — `crypto.js`
- `33b58598eb317553942e27545982d4c25ce6120eae10e42393746eb0e02ecae9` — Linux `aone-kit-update`

## Defender actions
1. Search lockfiles, SBOMs, npm caches, internal mirrors, CI logs, build artifacts, and developer-host package trees for the reported package names and versions.
2. Isolate systems that installed or imported affected packages. Preserve npm cache archives, `.cloud-preferences.json`, package trees, process telemetry, DNS/proxy logs, shell profiles, LaunchAgents, Alilang files, and `.skills` directories before cleanup.
3. Hunt for Node.js package activity followed by GitHub raw-content retrieval, Alibaba OSS payload downloads, `vm` sandbox escapes, detached execution from `/tmp`, or the C2 and header indicators above.
4. Search Python files for `# __INJECT_MARKER__` and inspect DingTalk, Wukong, Qoder, and adjacent agent-skill directories for unexpected Bun or `script.js` launch code.
5. Review DingTalk and developer-platform audit records for lateral movement or access originating from affected workstations.
6. From a known-clean host, rotate source-control, npm and other registry, cloud, Vault, Kubernetes, Docker, SSH, CI/CD, Slack, Twilio, and other credentials accessible to affected processes.
7. Pin private scopes to the intended private registry without public fallback. Alert when a public unscoped package imitates a private scoped name or combines private dependencies with newly published public helpers.
8. Analyze dependency behavior as a graph. Flag combinations where one package retrieves mutable configuration and another evaluates it, even if neither package contains a complete downloader by itself.
9. Rebuild affected developer systems from known-good media when execution cannot be ruled out. Package removal does not reverse profile, LaunchAgent, application, or skill-directory persistence.

## Assessment caveats
- Socket reported low package download counts and did not publish confirmed victim counts.
- Chinese comments, UTC+0800 commit timestamps, and targeting of Alibaba-oriented tools support a Chinese-speaking-operator hypothesis but are forgeable and do not identify an actor.
- The campaign's likely industrial-espionage objective is an analytic assessment based on target and capability, not a publicly confirmed operator statement.
- Possible maintainer-account takeover for `lib-mtop` and `local-config-parser` remains unconfirmed.

## Related pages
- [@marketfront / @tqm-mfe dependency-confusion stealer](marketfront-tqm-mfe-dependency-confusion-stealer.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [Joyfill npm blockchain-RAT compromise](joyfill-npm-blockchain-rat-compromise.md)

## Source
- Socket Research: [https://socket.dev/blog/npm-rat-targets-alibaba](https://socket.dev/blog/npm-rat-targets-alibaba) (July 28, 2026)
