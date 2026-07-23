# @copilot-mcp/apex macOS infostealer campaign

## Summary
SafeDep reported a same-operator npm and MCP campaign centered on `@apexfdn/apex`, its rapid replacement `@copilot-mcp/apex`, and the payload-free but attacker-controlled `@apexfdn/copilot-mcp` front. Both dropper package names were removed by npm, but SafeDep reported that the GitHub-hosted binaries, remote MCP endpoint, and `apex-arena-router[.]com` command-and-control infrastructure remained reachable when its July 22, 2026 analysis was updated.

The malicious packages used an npm `postinstall` hook to download and execute a large platform-specific binary. On macOS, a second chain fetched an AES-encrypted, AMOS-family AppleScript stealer, phished the user's login password with a native-looking prompt, collected developer, browser, wallet, messaging, and document data, and staged it as `/tmp/osalogging.zip`. It also installed a fake “System Notifications” application and a LaunchAgent that polled the C2 every 60 seconds for commands.

The campaign is notable for surviving its first npm takedown in roughly 11 hours: after npm removed `@apexfdn/apex`, the operator republished the same dropper as `@copilot-mcp/apex` and pushed more than 20 versions in about eight hours while changing launcher techniques. npm subsequently removed the replacement as well.

## Tags
- ops
- operations
- npm
- supply-chain
- macOS
- macOS malware
- infostealer
- Atomic Stealer
- AMOS
- postinstall
- install-time execution
- developer-targeting
- cryptocurrency theft
- wallet theft
- credential theft
- SSH keys
- AWS
- Kubernetes
- browser credential theft
- Keychain theft
- LaunchAgent
- persistence
- MCP
- remote MCP
- GitHub release assets
- source-package mismatch
- package takedown
- package republishing
- SafeDep

## Why this matters
- **Package removal did not remove the delivery system.** SafeDep found the replacement package about 11 hours after the first takedown and reported that the GitHub organization, release binaries, remote MCP endpoint, and C2 remained available after both npm removals.
- **The reviewed source was not the executed artifact.** Package metadata pointed to a payload-free TypeScript repository, while `install.cjs` downloaded binaries from a different GitHub repository and a mutable release asset behind a static `v1.0.0` tag.
- **A functional tool and aged brand supplied cover.** The operator maintained a payload-free MCP package for about three months and forked the legitimate `oh-my-pi` coding agent, so victims received a working AI tool while the install chain executed separately.
- **The theft crossed crypto and developer boundaries.** In addition to wallets, the reported stealer collected SSH keys, AWS credentials, Kubernetes configuration, browser sessions, Keychain material, shell history, and source-adjacent documents.
- **The no-install MCP path remains a trust concern.** SafeDep reported that the hosted MCP endpoint accepted a Bearer token and forwarded tokens and document excerpts to operator-controlled infrastructure even though the associated package itself contained no malicious payload.

## Reported timeline
| Time (UTC) | Event |
| --- | --- |
| 2026-04-30 23:03 | `Apex-Foundation` and payload-free `@apexfdn/copilot-mcp@0.1.0` were created. |
| 2026-07-05 11:53 | First `@apexfdn/apex` dropper version was published. |
| 2026-07-05 to 2026-07-21 | The original package shipped 33 additional versions and remained installable for roughly two and a half weeks. |
| 2026-07-21 21:00 | npm removed the original package and replaced it with `0.0.1-security`. |
| 2026-07-22 08:04 | The operator republished the dropper as `@copilot-mcp/apex`. |
| 2026-07-22 08:04–16:48 | More than 20 replacement versions were published while launcher behavior changed. |
| 2026-07-22 after 17:53 | npm removed the replacement package; registry requests returned `Not found`. |

A July 23 public-registry check by threat.wiki confirmed that `@apexfdn/apex` resolved only to npm's `0.0.1-security` placeholder and that `@copilot-mcp/apex` returned HTTP 404. Registry removal does not establish whether cached tarballs, mirrors, private registries, cloned repositories, or downloaded release assets were removed.

## Delivery and execution chain
1. Installation or `npx` execution ran `node install.cjs` through `postinstall`.
2. The installer selected and downloaded a roughly 120–150 MB binary from `Apex-Foundation/copilot` GitHub release `v1.0.0`, not from the repository named in package metadata.
3. The static release tag allowed its assets to be replaced without a new npm version. SafeDep observed release assets re-uploaded while replacement package versions were being published.
4. On macOS, launcher variants fetched `loader.sh` directly, ran a compiled helper, or invoked the shell chain through `osascript`; later variants detached and suppressed output.
5. The loader downloaded `payload.enc`, derived an AES-256-CBC key from an embedded upload token, decrypted the payload, and piped the plaintext to `osascript` without writing a separate plaintext script.
6. The AMOS-family AppleScript collected data under `/tmp/sync<random>/`, produced `/tmp/osalogging.zip`, and the loader uploaded it through an initialization request followed by HTTPS PUT retries.
7. After successful upload the loader deleted the archive, while a LaunchAgent continued polling `/v1/agent/ping` every 60 seconds.

SafeDep did not report a confirmed malicious path inside the large Linux or Windows binaries beyond the unreviewed download-and-execute behavior. Those platforms should not be treated as safe: `postinstall` still ran a remotely hosted binary whose source and publisher authenticity were not established.

## Reported collection and persistence
The decrypted macOS payload reportedly collected:

- login credentials through a fake system password dialog validated with `dscl . authonly`;
- cookies, saved passwords, autofill, and decryption state from Safari, 13 Chromium-family browsers, and four Gecko-family browsers;
- more than 20 desktop cryptocurrency wallets and more than 100 wallet-extension IDs;
- `~/.ssh`, `~/.aws`, `~/.kube`, login Keychains, iCloud keys, Telegram Desktop sessions, Apple Notes, `.gitconfig`, and shell histories;
- selected PDF, Office, wallet, private-key, certificate, and VPN files from Desktop, Documents, and Downloads; and
- hardware, serial, UUID, SIP, process, and application inventory.

Reported persistence consisted of:

- `~/Library/LaunchAgents/com.system.notifications.agent.plist`
- label `com.system.notifications.agent`
- `StartInterval` of 60 seconds
- `~/Library/Application Support/System/System Notifications.app`
- bundle ID `com.system.notifications.helper.bld013`

The LaunchAgent was a command channel rather than passive persistence: SafeDep reported that authenticated polling of `/v1/agent/ping` returned a live `{"cmd":"idle"}` response during analysis.

## Indicators
### Packages and distribution
- `@apexfdn/apex` — original malicious dropper; removed and replaced with `0.0.1-security`
- `@copilot-mcp/apex` versions `1.0.0` through at least `1.0.22` — republished malicious dropper; removed
- `@apexfdn/copilot-mcp` — payload-free same-operator front; treat as attacker-controlled
- `hxxps://arena[.]apexfdn[.]xyz/api/copilot/mcp` — hosted remote MCP endpoint
- GitHub organization: `Apex-Foundation`
- Weaponized binary repository: `Apex-Foundation/copilot`
- Advertised source/front repository: `Apex-Foundation/copilot-mcp`
- npm accounts: `copilotapex`, `apex-fdn`

### Network
- `update[.]apex-arena-router[.]com`
- `apex-arena-router[.]com`
- `apexfdn[.]xyz`
- `arena[.]apexfdn[.]xyz`
- `docs[.]apexfdn[.]xyz`
- `172.93.185[.]150`
- `/loader.sh`
- `/payload.enc`
- `/v1/asset/{id}/init`
- `/v1/asset/{id}`
- `/v1/asset/{id}/segment/{n}`
- `/v1/agent/ping`
- `/v1/capture`

SafeDep described a Caddy reverse proxy in front of Uvicorn/FastAPI and a publicly exposed `/openapi.json`. Its route schema suggested a multi-tenant panel capable of provisioning campaign subdomains and upload tokens. Do not probe suspected attacker infrastructure during ordinary hunting; use preserved proxy, DNS, EDR, and passive-intelligence records.

### Files and hashes
- `/tmp/osalogging.zip` — staged theft archive, deleted after successful upload
- `/tmp/sync<random>/` — temporary collection directory
- `~/Library/LaunchAgents/com.system.notifications.agent.plist`
- `~/Library/Application Support/System/System Notifications.app`
- `payload.enc` SHA-256: `ecd1113fae1ede9869afd9d1af612bab7f1a2054e5c45a346e18c107c22b9164`
- `@copilot-mcp/apex@1.0.0` tarball SHA-1: `233f90180b529aa32911901e5222e9ed9c3cd24c`
- `@copilot-mcp/apex@1.0.19` tarball SHA-1: `3b9a880ae4e1c5b7bbd68e118a1c3c8b592f7bfb`

Hashes are useful for retrospective matching but package names, install behavior, release-asset source mismatch, persistence, and network behavior are more durable because the operator changed versions and launcher implementations rapidly.

## Defender guidance
- Search manifests, lockfiles, SBOMs, npm caches, proxy logs, private registries, CI artifacts, and developer endpoints for all three package names and the `Apex-Foundation` repositories.
- Block the malicious package names and reported domain family. Treat `@apexfdn/copilot-mcp` and its hosted MCP endpoint as attacker infrastructure, not as a clean replacement.
- Hunt for package-manager or Node.js ancestry launching `install.cjs`, `osascript`, `zsh`, large unsigned binaries from GitHub release paths, and detached helpers during or immediately after npm operations.
- On affected Macs, preserve evidence before cleanup where incident scope warrants it. Isolate the host, unload and preserve the LaunchAgent and fake application bundle, and collect process, unified-log, DNS, proxy, npm-cache, shell-history, and filesystem metadata.
- Assume credentials accessible to the host were exposed. Revoke browser sessions and rotate SSH keys, AWS and Kubernetes credentials, Git/package-registry/CI tokens, API keys, login credentials, and wallet seed material from a known-clean system.
- Search cloud and source-control audit logs for post-theft use. Credential rotation without reviewing IAM changes, new keys, repository access, CI workflows, and token sessions can leave attacker persistence intact.
- Require package artifacts to match reviewed source and provenance. Flag install hooks that retrieve mutable GitHub release assets, especially when package metadata names a different source repository.
- Disable lifecycle scripts by default where workflows permit, then explicitly approve reviewed packages. This control would block the reported npm path but not the hosted remote-MCP path.
- Inventory remote MCP endpoints, restrict tokens and documents agents may send, and avoid attaching developer or production credentials to untrusted hosted tools.

## Attribution and scope caveats
SafeDep linked the package set through shared domains, package metadata, repository references, account ownership, and runtime behavior. This supports common control of the campaign infrastructure but does not identify a real-world actor. The payload was described as AMOS-family based on its AppleScript behavior; that does not by itself establish a relationship with a particular malware seller or affiliate.

Download counters reflected only release assets uploaded on July 22 and were not a victim count. The original package had been available for roughly two and a half weeks, cached artifacts may survive registry removal, and a download can represent analysis, CI, retry behavior, or a noninfected platform.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [codexui-android OpenAI token stealer](codexui-android-openai-token-stealer.md)
- [Malware-Slop Claude user-data npm infostealer](malware-slop-claude-user-data-npm-infostealer.md)
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [CrashStealer macOS notarized-dropper campaign](crashstealer-macos-notarized-dropper.md)

## Sources
- SafeDep: [https://safedep.io/malicious-copilot-mcp-apex-npm-macos-infostealer](https://safedep.io/malicious-copilot-mcp-apex-npm-macos-infostealer)
- npm registry: [https://registry.npmjs.org/%40apexfdn%2Fapex](https://registry.npmjs.org/%40apexfdn%2Fapex)
- npm registry: [https://registry.npmjs.org/%40copilot-mcp%2Fapex](https://registry.npmjs.org/%40copilot-mcp%2Fapex)
