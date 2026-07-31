# XCSSET v40 Xcode supply-chain campaign

## Summary
Unit 42 reported on July 31, 2026 that **XCSSET v40** has infected Xcode projects since early April 2026, with a second deployment wave in early May. The campaign hides malicious build-phase code in legitimate Xcode projects and vulnerable Git repositories; a developer triggers endpoint infection by building a poisoned project. Unit 42 observed the malware in projects for dozens of legitimate applications with thousands of active users and a higher volume of targeting against developers in South Asia.

V40 is a substantial architectural change rather than a simple loader refresh. It executes a memory-resident orchestrator, streams polymorphic modules from rotating command-and-control infrastructure, infects additional local Xcode projects and Git workflows, and adds Chrome DevTools Protocol browser control and Telegram Desktop replacement. Its defense-evasion chain interferes with macOS updates, cloud telemetry, XProtect database updates, and Transparency, Consent and Control decisions.

## Tags
- ops
- operations
- XCSSET
- XCSSET v40
- macOS
- Xcode
- GitHub
- supply-chain
- developer targeting
- source-repository poisoning
- build-time compromise
- worm
- browser hijacking
- credential theft
- defense evasion
- in-memory malware

## Campaign chronology and scope
- **Mid-April 2026:** Unit 42 began tracking the new version after activity dating to early April.
- **Early May 2026:** a second wave introduced an expanded module suite, including a Telegram Desktop trojanizer not seen in the April deployment.
- **July 31, 2026:** Unit 42 published its technical analysis, 17-module map, infrastructure set, and mitigations.

Unit 42 described infections in Xcode projects associated with dozens of legitimate applications and thousands of active users, but did not publish an affected-project list or a count of confirmed compromised endpoints. The report attributes the malware to the operators behind the known XCSSET family; it does not identify a named threat actor.

## Infection and propagation chain
1. An injected Xcode run-script phase executes when a developer builds a poisoned project.
2. Nested hexadecimal and Base64 decoding produces an initial downloader, which contacts a C2 `/a` endpoint with `p=xcode_phase` context.
3. A second stage collects basic host metadata. C2-approved systems receive a substitution-cipher-obfuscated script that performs deeper hardware and serial-number fingerprinting.
4. The script stages a loader at `/tmp/r`, compiles `/tmp/p.app`, and runs the wrapper through `osascript`.
5. The wrapper retrieves the `boot` orchestrator and loader, then kills staging processes and removes the temporary files.
6. `boot` downloads AES-encrypted modules from `/s/<encoded_module_name>` and pipes them to AppleScript for in-memory execution.
7. `replicator_finder`, `git_finder`, and `zip_infect_finder` infect local Xcode projects, Git pre-commit paths, and Xcode projects found inside ZIP archives, turning an infected developer workstation into a source-repository propagation point.

This is **build-time execution**, not a conventional package-manager install hook. Repository provenance and a clean dependency install do not rule out a poisoned Xcode build phase.

## New operational capabilities
### Chrome DevTools Protocol backdoor
The new `chrome_remote` component wraps the legitimate Chrome binary with a persistence script, restarts the XCSSET orchestrator when Chrome launches, enables Chrome DevTools Protocol on a local port, and attaches a Go backdoor to that port. A persistent C2 WebSocket can then supply JavaScript for execution before pages load.

The injected scripts can hook `fetch` and `XMLHttpRequest`, collect credentials and API tokens, capture password-manager autofill, and manipulate MetaMask addresses or decentralized-application transactions. Specially delimited browser-console messages are converted into local shell commands by the helper binary, with output returned through the CDP WebSocket. Unit 42 reported the behavior to Google; its report says equivalent protection exists on Windows and Google is working to extend it to macOS.

### Telegram Desktop replacement
The `tdesktop` module downloads a malicious `Telegram.app` archive, removes the legitimate application, installs and ad hoc signs the replacement, and kills the original process so the user relaunches the trojanized copy. It retrieves an AES-encrypted configuration from `/w?tr`, stores state in `~/.tr` and `~/.tr_map`, and uploads those files to C2. Unit 42 did not capture the configuration blob and therefore could not verify its exact contents.

### Other modules
Unit 42 mapped 17 modules. They include the `boot` orchestrator; host and anti-VM reconnaissance; clipboard and keyboard hijacking; Firefox, Apple Notes, and folder-data theft; Xcode/Git/ZIP propagation; LaunchDaemon, shell, Dock-app, and trojanized-application persistence; Safari and multi-browser hijacking; and the new Chrome and Telegram components.

## Evasion and persistence
- C2 recompiles the loader every few hours; Unit 42 received eight hashes at one endpoint in 24 hours.
- Modules use AES-256-CBC with a per-build key and randomized IV, while inbound and outbound traffic use separate keys.
- Internal strings use per-module keyed Caesar ciphers and randomized alphabets; function and variable names are substituted before compilation.
- A Base64 staging payload is stored under randomized keys in a per-host macOS `defaults` preferences domain. A trojanized app can decode it and re-arm the infection without another predictable script on disk.
- The malware disables automatic update settings affecting XProtect, MRT, TCC, and Rapid Security Response delivery; repeatedly terminates `CloudTelemetryService`; and holds an exclusive lock on the XProtect `XPdb` YARA database.
- If a user denies AppleEvents automation, it runs `tccutil reset AppleEvents` and presents another prompt while masquerading as System Settings or Xcode.
- The `stats` module reports VM indicators to C2; Unit 42 observed virtualized hosts receiving no further modules.

## High-value indicators
### Infrastructure
- IPs: `91.108.106[.]229`, `95.142.35[.]34`, `95.142.35[.]206`, `95.142.37[.]159`, `151.243.109[.]188`, `178.208.92[.]129`, `178.208.92[.]168`
- Reused SSL SHA-1 thumbprint: `6e480d648fa1b70612f5d198a66875e28847547d`
- Representative C2 domains: `amzndev[.]in`, `amzndev[.]ru`, `googlenets[.]ru`, `netcdndev[.]in`, `whitead[.]in`, `whiteads[.]ru`, `applecdn[.]ru`, `cdnapple[.]in`, `chromeads[.]ru`, `dnsapple[.]ru`, `rigmanets[.]in`, `timewebnet[.]in`
- Chrome helper path pattern: `/d/zw_sfp64`
- Module and configuration paths: `/s/<rotated_module_name>`, `/w?tr`, `/w?cbp`

Unit 42 published a larger domain set. The operators registered roughly 40 domains in bursts and aged them before activation. Shared hosting addresses, SSH keys, a self-signed RDP certificate, and the SSL thumbprint linked infrastructure across campaign sets.

### Host artifacts and behavior
- poisoned Xcode run-script phases making `curl` requests with `p=xcode_phase`
- temporary `/tmp/r` and `/tmp/p.app` followed by `osascript` execution and deletion
- unusual `defaults` domains containing Base64 payloads under random-looking keys
- `~/.tr`, `~/.tr_map`, and uploads named `base_tr_file.txt` or `base_tr_map.txt`
- Chrome launched with CDP enabled on a local port, followed by an unknown `chrome_remote` helper and long-lived WebSocket
- unexpected ad hoc replacement of `/Applications/Telegram.app`
- recurring termination of `CloudTelemetryService`, a Perl process locking XProtect `XPdb`, update-setting changes, or `tccutil reset AppleEvents`
- Git pre-commit hook changes and newly modified Xcode project files or Xcode projects inside ZIP archives

## Defender actions
1. Inventory and diff Xcode build phases, project files, Git hooks, and archived source against known-good upstream revisions before building. Do this for every project on a suspected developer host, not only the project that first triggered an alert.
2. Isolate suspected systems and preserve memory, process, unified-log, shell-history, filesystem, browser-launch, DNS/proxy, Git, Xcode, TCC, preferences, and code-signing evidence before cleanup. The core module is largely memory resident and staging files self-delete.
3. Hunt for the host behaviors above, especially Xcode-to-shell/`curl`/`osascript` lineage, `/tmp/p.app`, randomized `defaults` domains, CDP-enabled Chrome, ad hoc Telegram replacement, and suppression of update or telemetry controls.
4. Block the published infrastructure and monitor the URI patterns, but do not rely on static hashes: loaders and encrypted module blobs rotate frequently.
5. From a known-clean system, revoke browser sessions and rotate source-control, cloud, signing, package-registry, messaging, wallet, password-manager, and other credentials accessible to the developer account.
6. Restore update and XProtect functionality, verify Rapid Security Response status, and inspect TCC decisions. Rebuild compromised development systems from known-good media after evidence collection.
7. Scope repositories and downstream builds touched by the host. Review commits, hooks, release artifacts, signing events, CI executions, and collaborator clones for propagation before restoring trust.

## Assessment caveats
- The public report establishes widespread poisoned-project distribution but does not name affected projects or distinguish all initial repository-compromise paths.
- A project containing injected code is not proof that every user built it or that every host passed C2 targeting and anti-VM gates.
- Infrastructure and the shared certificate/key material are campaign pivots, not proof that unrelated traffic to a co-hosted IP is malicious.
- Unit 42's report provides family-level attribution to XCSSET operators, not a named actor or state sponsor.

## Related pages
- [XCSSET](../tools/xcsset.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Operation FlutterBridge macOS malvertising](operation-flutterbridge-fluttershell-macos-malvertising.md)
- [CrashStealer macOS notarized-dropper campaign](crashstealer-macos-notarized-dropper.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/xcsset-v40-malware-analysis/](https://unit42.paloaltonetworks.com/xcsset-v40-malware-analysis/)
