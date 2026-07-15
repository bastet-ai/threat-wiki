# OkoBot cryptocurrency-wallet malware framework

## Summary
Kaspersky GReAT reported **OkoBot** on July 15, 2026 as an active Windows malware framework targeting cryptocurrency users. Kaspersky reconstructed a four-stage infection chain that starts with the TookPS PowerShell downloader and then uses an automated SSH-bot delivery path to deploy more than 20 payloads and implants.

The highest-signal component is **SeedHunter**: it monitors for Trezor Suite, Ledger Wallet, and Ledger Live processes, injects into the legitimate Electron wallet application, and can present malicious seed-phrase collection UI from inside the real wallet software. Kaspersky telemetry counted hundreds of attacked users across more than 25 countries from April 2025 through June 2026, with the largest shares in Brazil, Vietnam, Canada, Mexico, and Türkiye.

## Tags
- ops
- active threat
- malware framework
- cryptocurrency theft
- cryptocurrency wallets
- Windows malware
- TookPS
- OkoBot
- SeedHunter
- TeviRAT
- Rilide
- Ledger
- Trezor
- Electron
- process injection
- seed phrase theft
- SSH tunnel
- browser extension loader
- keylogger
- spyware
- Kaspersky GReAT
- The Hacker News

## Why this matters
- OkoBot shifts seed-phrase phishing into the trusted desktop-wallet context. The malicious prompt can appear inside a genuine Ledger or Trezor application process rather than in an obvious browser phishing page.
- The framework is modular: Kaspersky describes more than 20 payloads covering UAC bypass, browser-extension loading, process injection, keylogging, spyware, artifact exfiltration, and TeviRAT delivery.
- SeedHunter can wait for hardware-wallet USB device presence before showing the phrase-collection flow, making the prompt more plausible to the victim.
- The campaign is active and geographically broad. Kaspersky observed hundreds of attacked end users in 25+ countries from April 2025 to June 2026.
- Attribution is unresolved. Kaspersky notes Russia/CIS geoblocking in the initial script-delivery servers and Rilide ecosystem overlap, but did not attribute the campaign to a known crimeware actor.

## Technical notes
- Initial infection uses the previously described **TookPS** downloader. Kaspersky observed TookPS activity in March 2025, a TeviRAT-delivery wave in April 2025, and a redesigned OkoBot chain beginning at the end of April 2025.
- The OkoBot chain uses an automated SSH bot for payload delivery and orchestration after the initial TookPS stage.
- A launcher and plugin dispatcher deliver modules including a browser-extension loader, process-injected implants, SeedHunter, MC Keylogger, and OkoSpyware.
- SeedHunter monitors active processes for Trezor Suite, Ledger Wallet, and Ledger Live. It then injects wallet-targeting code and hooks internal Electron framework functions.
- The module communicates with `moonsand[.]store` over HTTPS, sending Base64-encoded JSON with fields such as `Pid`, `HWID`, and `Build`.
- A C2 `Wait` flag can cause the malware to poll USB devices by vendor/product ID and delay prompting until a Trezor or Ledger device is connected.
- Kaspersky reports that MC Keylogger and OkoSpyware artifacts are exfiltrated to the C2 endpoint `ir-post.php`, after which local files and PowerShell command history are cleared.

## Defender heuristics
1. Treat any wallet UI that asks for a seed phrase on an already-initialized device as hostile until proven otherwise. Ledger's normal safety guidance is that the recovery phrase should never be typed anywhere except the Ledger device itself; Trezor recovery behavior differs by model, but unexpected prompts still warrant immediate stop-and-verify.
2. On suspected endpoints, preserve evidence before cleanup: PowerShell logs, scheduled tasks, SSH client/tunnel artifacts, process-injection telemetry, browser-extension directories, wallet-application logs, temporary directories, and EDR process trees.
3. Hunt for TookPS and OkoBot detections named by Kaspersky, including `Trojan-Downloader.Win32.TookPS.*`, `Trojan.Win64.BypassUAC.*`, `Trojan-Banker.Script.Agent.gen`, `Trojan.Win32.Dllhijack.*`, `Backdoor.Win32.TeviRat.*`, `Trojan-PSW.Win64.Stealer.*`, `Trojan-Spy.Win64.Keylogger.*`, and `Trojan-Spy.Win64.Agent.*`.
4. Monitor for non-standard child processes, DLL injection, or module loads inside `Trezor Suite`, `Ledger Wallet`, and `Ledger Live`, especially around USB wallet connection events.
5. Block and investigate traffic to Kaspersky-published OkoBot infrastructure, including `moonsand[.]store` and `ir-post.php` paths, while validating against the full IOC list in the Securelist post.
6. If a user entered a recovery phrase, assume wallet compromise. Move funds using a clean device and a newly generated wallet/seed; do not reuse the exposed seed after malware removal.
7. Rebuild high-risk developer or finance endpoints from trusted media when compromise cannot be ruled out, because the framework includes persistence, credential theft, keylogging, and anti-forensic cleanup behavior.

## Related pages
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [Silent Swap Google Notes crypto clipper](silent-swap-google-notes-crypto-clipper.md)
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [Injective SDK npm wallet stealer](injective-sdk-npm-wallet-stealer.md)

## Sources
- Kaspersky Securelist, July 15, 2026: https://securelist.com/okobot-framework-targets-cryptocurrency-wallets/120660/
- The Hacker News, July 15, 2026: https://thehackernews.com/2026/07/okobot-malware-framework-injects-seed.html
- Ledger recovery phrase safety guidance: https://support.ledger.com/article/360023518653-zd
- Trezor recovery guidance: https://trezor.io/guides/backups-recovery/general-standards/recover-wallet-on-model-one
