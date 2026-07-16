# Glassworm developer supply-chain botnet

## Summary
CrowdStrike reported a coordinated 2026-05-26 takedown of Glassworm command-and-control infrastructure in partnership with Google and the Shadowserver Foundation. Glassworm is a developer-targeting supply-chain campaign active since at least early 2025, using malicious VS Code / OpenVSX extensions, npm and Python packages, and poisoned GitHub repositories to harvest developer credentials and maintain a botnet of compromised workstations.

CrowdStrike says the disruption simultaneously hit four C2 channels: Solana blockchain dead drops, BitTorrent DHT configuration lookups, Google Calendar dead drops, and direct VPS-hosted server infrastructure. The Hacker News summarized the same reporting and noted prior public Glassworm activity across VS Code marketplaces, npm, and Python package paths.

## Tags
- ops
- operations
- supply-chain
- developer-targeting
- VS Code
- OpenVSX
- WebAssembly
- TinyGo
- Solana
- browser-extensions
- npm
- PyPI
- GitHub
- credential-theft
- botnet
- RAT
- C2
- takedown
- Russia-linked cybercrime

## Why this matters
- Glassworm targets developers rather than only end users, so one workstation compromise can expose source repositories, package-registry tokens, cloud accounts, CI/CD pipelines, and downstream software consumers.
- The campaign spans multiple developer ecosystems: VS Code and VS Code forks, OpenVSX, npm, Python packages, and GitHub repositories.
- The C2 design used several resilient dead-drop and discovery layers, forcing defenders to coordinate simultaneous action instead of removing only a single server or domain.
- The takedown does not automatically remediate infected endpoints; it primarily prevents compromised machines from receiving new instructions or payloads while defenders identify hosts, rotate secrets, and rebuild trust.

## Initial-access and propagation paths
CrowdStrike and secondary reporting describe a multi-pronged developer compromise chain:

- Trojanized VS Code extensions published to OpenVSX and the Microsoft VS Code Marketplace, including extensions disguised as common developer utilities such as time trackers and code formatters.
- Targeting of VS Code forks and compatible editors, including Cursor, Positron, Windsurf, VSCodium, and similar OpenVSX-consuming environments.
- Compromised npm and Python packages that executed malicious code through normal install or setup workflows.
- More than 300 GitHub repositories poisoned with stolen developer credentials, including malicious code force-pushed into default branches.

## Payload behavior
Reported Glassworm capabilities include:

- developer credential harvesting, including GitHub, npm, and OpenVSX tokens;
- crypto-wallet theft and browser-data collection;
- host and environment profiling;
- conversion of infected hosts into covert infrastructure, including SOCKS proxies, hidden VNC servers, and remote-execution nodes;
- a WebSocket-based JavaScript RAT tracked as GlassWormRAT;
- arbitrary code execution through WebRTC or spawned Node.js processes;
- installation of a Chrome extension for screenshots, keystrokes, clipboard collection, and other browser-side theft.

## June 2026 GlassWASM Open VSX extension wave
Socket's June 15, 2026 report described a related Open VSX wave it named **GlassWASM** and attributed with medium confidence to the GlassWorm developer. The two reported malicious extensions were impersonated Open VSX copies of legitimate VS Code Marketplace listings:

- `exargd/vsblack@0.0.1`
- `noellee-doc/flint-debug@0.1.1`

Key differences from earlier plain JavaScript extension malware:

- The malicious Open VSX packages embedded `snqpkebiwrxmoivl.wasm`, a TinyGo-built `js/wasm` module loaded by an appended bootstrap that called `go.run()` when the extension activated.
- Strings, URLs, and commands were encrypted in the WebAssembly module with ChaCha20 and reconstructed only at runtime, reducing value from simple static string scans.
- The module queried `https://api.mainnet.solana.com` for transactions sent to attacker-controlled wallet `6ExrZayPZzMMSnszc42cH81DpuKT8FhCX9H6Sesn6rpz`, then read SPL Memo instructions to build the next-stage download-and-execute command.
- Socket reported memo-program IDs `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr` and `Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFM` in the chain.
- The second-stage templates used OS-specific paths under `https://dodod[.]lat/`, including `/win32/i/_`, `/darwin/i/_`, and `/linux/i/_`, executed through Node's `child_process` path.
- Socket said the legitimate VS Code Marketplace listings for `ExarGD.vsblack` and `noellee-doc.flint-debug` were clean older originals; scope removal to the malicious Open VSX copies and installations sourced from Open VSX.

Reported hashes for the WebAssembly payload and extension artifacts include:

- `558b4f1d9a263c13756ab0126c09dd080c85ba405b29488e1c4e6aa68b554f1f`
- `1e283327ad048bea39f4a8501770858a20f3555e87fe3e202274f2e87f8a3c25`
- `3aa31999398e7f80231c03d7137ffdb554a84b83dbcffc59ce16c9a65f9e5d58`

## Resilient C2 design
Glassworm used four reported command-and-control paths:

1. **Solana blockchain dead drops** — C2 server addresses stored in memo fields of Solana transactions.
2. **BitTorrent DHT** — peer-to-peer configuration retrieval through hardcoded public keys.
3. **Google Calendar dead drops** — Base64-encoded C2 paths placed in calendar event titles.
4. **Direct VPS C2** — traditional server infrastructure for payload delivery and tasking.

The combination let operators reconstitute from alternate discovery layers if defenders removed only one channel. CrowdStrike states that the 2026-05-26 action disrupted all four simultaneously, preventing infected machines from receiving new tasking or payloads.

## Attribution notes
CrowdStrike assesses the operators as likely Russia-based cybercriminals. Public evidence cited in the report includes runtime checks that exit on CIS-country systems, victim locale / language / timezone checks, and Russian-language source-code comments. Treat this as cluster-level cybercrime attribution rather than a state-actor finding.

## Defender heuristics
- Inventory VS Code, Cursor, Windsurf, VSCodium, Positron, and OpenVSX extension installs on developer workstations and CI/devcontainer images.
- Hunt for unexpected VS Code extensions, recently changed extension directories, and extension code that reaches Solana, BitTorrent DHT, Google Calendar, or unfamiliar VPS endpoints.
- For the GlassWASM wave, inspect extension directories such as `~/.vscode/extensions`, `~/.vscode-oss/extensions`, `~/.cursor/extensions`, and `~/.windsurf/extensions` for `ExarGD.vsblack@0.0.1`, `noellee-doc/flint-debug@0.1.1`, unexpected `.wasm` files next to JavaScript loaders, TinyGo `gojs.syscall/js` imports, and outbound Solana JSON-RPC access from editor processes.
- Treat WebAssembly inside editor extensions as executable code requiring disassembly and behavior review, not as a harmless packaged asset.
- Search workstations and CI runners for unexpected npm/Python lifecycle execution, WebSocket RAT behavior, SOCKS proxy listeners, hidden VNC processes, spawned Node.js remote-execution processes, and suspicious browser extensions.
- If Glassworm exposure is suspected, isolate affected developer hosts before rotating credentials. Assume GitHub, npm, OpenVSX, package-registry, cloud, SSH, browser, and crypto-wallet secrets may be compromised.
- Review GitHub default-branch force pushes, unusual commits, package-publish events, token use, workflow changes, and repository access from developer accounts after suspected infection windows.
- Treat a C2 takedown as a containment opportunity, not proof of endpoint cleanup; rebuild or deeply inspect developer machines before restoring trust.

## Related pages
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [node-ipc 2026 npm maintainer-account compromise](node-ipc-2026-npm-maintainer-compromise.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- CrowdStrike: <https://www.crowdstrike.com/en-us/blog/inside-crowdstrike-takedown-of-a-developer-targeting-botnet/>
- Socket: <https://socket.dev/blog/glasswasm-malware-open-vsx-extensions>
- The Hacker News: <https://thehackernews.com/2026/05/glassworm-malware-takedown-disrupts.html>
