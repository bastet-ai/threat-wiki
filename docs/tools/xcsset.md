# XCSSET

## Summary
**XCSSET** is modular macOS malware that propagates through poisoned Xcode projects and Git repositories, compromising developers when they build infected source. Unit 42's 2026 analysis calls the latest generation **XCSSET v40**. It uses a memory-resident orchestrator, polymorphic C2-delivered modules, local project and Git-hook infection, credential and data theft, browser hijacking, and multiple persistence and defense-evasion paths.

## Tags
- tools
- malware
- XCSSET
- XCSSET v40
- macOS
- Xcode
- supply-chain
- developer targeting
- worm
- browser hijacking
- credential theft
- in-memory malware
- defense evasion

## Execution and propagation
A malicious Xcode run-script phase executes when a developer builds a poisoned project. The staged chain fingerprints the host, retrieves a loader and AppleScript wrapper, starts the `boot` orchestrator, removes temporary files, and streams encrypted modules into memory.

Propagation modules infect local Xcode projects, Git pre-commit paths, and Xcode projects contained in ZIP archives. XCSSET can therefore turn a developer endpoint into a repository and downstream-build compromise point.

## V40 module set
Unit 42 mapped 17 modules, including:
- `boot` — orchestration and module dispatch;
- `stats` — host, browser-extension, and VM reconnaissance;
- `replicator_finder`, `git_finder`, and `zip_infect_finder` — Xcode, Git-hook, and archive infection;
- `data_folders_finder`, `firefox_data`, and `notes_app` — data discovery and theft;
- `settings_app`, `finder_app`, and `persist` — LaunchDaemon, trojanized-app, shell, Dock-app, and TCC-related persistence;
- `browser_remote`, `safari_remote`, and `chrome_remote` — browser dispatch, hijacking, and remote access;
- `tdesktop` — Telegram Desktop replacement.

The v40 `chrome_remote` helper enables Chrome DevTools Protocol, attaches to the browser, receives JavaScript over a C2 WebSocket, hooks browser APIs, steals cookies and credentials, manipulates wallet transactions, and converts specially formatted console messages into host shell commands. `tdesktop` replaces and ad hoc signs Telegram Desktop and maintains C2-supplied state in `~/.tr` and `~/.tr_map`.

## Stealth and persistence
- frequently recompiled loaders and randomized AES-256-CBC module blobs;
- separate inbound and outbound C2 keys;
- per-module string ciphers and pre-compilation identifier substitution;
- Base64 staging payloads stored in randomized macOS `defaults` preference domains;
- largely in-memory module execution and deletion of staging files;
- disabling update channels, terminating `CloudTelemetryService`, locking XProtect `XPdb`, and resetting AppleEvents TCC decisions;
- anti-VM reporting that can stop module delivery to analysis systems.

## Defender notes
- Hunt behaviorally for Xcode build processes spawning shell, `curl`, or `osascript`; temporary `/tmp/r` and `/tmp/p.app`; Git-hook or project-file changes; unusual `defaults` domains; CDP-enabled Chrome; ad hoc Telegram replacement; and update/XProtect/telemetry impairment.
- Treat every Xcode project and repository touched by an infected host as untrusted until diffed against known-good history. Scope downstream clones, commits, CI builds, releases, and signing activity.
- Preserve memory and volatile process/network evidence before remediation because the orchestrator and modules are largely memory resident.
- Static hashes have short value because loaders and encrypted payloads rotate. Use the infrastructure, certificate thumbprint, URI patterns, and endpoint behavior documented on the campaign page as pivots.

## Related pages
- [XCSSET v40 Xcode supply-chain campaign](../ops/xcsset-v40-xcode-supply-chain-campaign.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/xcsset-v40-malware-analysis/](https://unit42.paloaltonetworks.com/xcsset-v40-malware-analysis/)
