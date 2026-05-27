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
- CrowdStrike: https://www.crowdstrike.com/en-us/blog/inside-crowdstrike-takedown-of-a-developer-targeting-botnet/
- The Hacker News: https://thehackernews.com/2026/05/glassworm-malware-takedown-disrupts.html
