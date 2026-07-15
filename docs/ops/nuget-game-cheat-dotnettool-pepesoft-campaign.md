# NuGet game-cheat DotnetTool pepesoft campaign

## Summary
Socket reported on July 14, 2026 that 11 malicious NuGet packages were published as `.NET` command-line tools (`DotnetTool`) masquerading as game cheats, bots, and control panels. Running the installed tool triggers a bundled .NET downloader that stages and executes a Windows payload named `pepesoft.exe` from operator-controlled GitHub Releases or Hugging Face paths under the `pepegit666` account.

The campaign is high-signal because it abuses NuGet's executable tool format rather than only library import paths: a developer, gamer, or CI host that runs an untrusted `dotnet tool install` / command can execute a remote payload that uses Google Sheets for telemetry or licensing state, binds activity to hardware IDs, and in some recovered builds exposes Telegram screenshot-control paths.

## Tags
- ops
- supply chain
- NuGet
- .NET
- DotnetTool
- game cheats
- Windows malware
- downloader
- PyInstaller
- PyArmor
- DNS-over-HTTPS
- Google Sheets
- Telegram
- screenshot theft
- host surveillance
- package registry
- developer endpoints
- Socket Security

## Affected packages
Socket identified these malicious NuGet package IDs:

- `albion-x-x`
- `amazing-x-x`
- `calc-x-x`
- `grandrp-x-x`
- `gta5rp-x-x`
- `l2-x-x`
- `majestic-x-x`
- `rmrp-x-x`
- `rusfish4-x-x`
- `throne-x-x`
- `trigger-x-x`

The packages map to Albion Online, GTA5RP, GrandRP, Majestic RP, RMRP, Amazing RP, Lineage 2, Throne and Liberty, Russian Fishing 4, and generic trigger-bot / calculator-themed tooling. Socket notes Russian-language updater text and comments in the bundled application manifest.

## Technical details
### First-stage .NET downloader
Each package places its downloader assembly under `tools/net8.0/any/` and exposes a console command through the NuGet `DotnetTool` mechanism. The downloader:

- prints updater-like Russian-language status messages;
- creates a shared process mutex, `Global\\{5BD61028-3D9C-4B4E-AD45-CA4F1B35D0F4}`, to prevent duplicate runs;
- in 10 of 11 packages, launches hidden PowerShell with `runas` to start `w32time` and run `w32tm /resync`, requesting elevation before network activity;
- resolves GitHub download hosts through `https://dns.google/resolve` rather than the system resolver, reducing the effectiveness of hosts-file or local DNS sinkhole blocks;
- stages `pepesoft.exe` from Hugging Face first, GitHub Releases second, and dormant BitTorrent code third; and
- passes downloader-supplied cloud configuration to the child payload through environment variables.

### Second-stage `pepesoft.exe`
Socket recovered `pepesoft.exe` payloads as PyInstaller-packed Python 3.13 applications. Eight payloads used PyArmor-protected `gtaobus.pyc` entrypoints; Albion, Calculator, and Throne shipped direct Python bytecode and exposed richer automation logic.

Across the recovered payload set, Socket observed remote configuration retrieval, Google Sheets authentication for telemetry or licensing state, hardware-fingerprint binding, and a server-side HWID / UUID ban list. In the direct-bytecode payloads, the larger game-automation applications also exposed Telegram bot commands that can send screenshots back to configured chats, enumerate host and window state, and write start / exit telemetry. The PyArmor-protected payloads add an authenticated HTTP proxy fallback for Google Sheets traffic when direct Google access is blocked.

## Infrastructure and indicators
Use these as hunt pivots, not as the only detection logic:

- Operator account: `pepegit666`
- GitHub staging: `github[.]com/pepegit666/123f53y45ysdf34/releases/download/<tag>/pepesoft.exe`
- Hugging Face staging: `huggingface[.]co/buckets/pepegit666/<tag>/resolve/pepesoft.exe?download=true`
- Cloudflare Worker endpoint: `calm-voice-9797.888c888x888[.]workers[.]dev`
- Selcloud endpoint: `s3[.]ru-3[.]storage[.]selcloud[.]ru`
- Google DNS-over-HTTPS resolver: `dns.google/resolve`
- Proxy fallback: `196[.]16[.]3[.]71:9528`
- Operator endpoints: `bots.pepesoft[.]ru`, `t[.]me/pepesoft777`
- Payload name: `pepesoft.exe`
- Local artifacts called out by Socket: `./_`, `./libgg/chat_ids.txt`, `./token.txt`, `credentials.txt`, `%LOCALAPPDATA%\\Windows Src\\key*.txt`, `%APPDATA%\\pepesoft`
- Downloader assembly SHA-256 examples: `d5385526f2f3e52c7d96087611c6cd4e479bf61828400efdb3ca09406d981609` (`albion.dll`), `9a2091e6625fc11cfd8f39c17aa271604e66322ee045028946274b988103e35b` (`amazingrp.dll`), `900ddb81d27e03967209fee4d17d13deb68eef0e1f10936eb520ca10575cb49e` (`calculator.dll`), `23808e7638f7a00b1ef9b9f4ca524f8a46cf63be6f6b79fec8e4a3fd1cc82a1e` (`trigger.dll`)

Socket also published hardcoded key material and webhook URLs; treat those as public IOCs in the original report, but avoid copying live credential-like values into internal tickets unless your handling process permits it.

## Defender guidance
1. Block and remove the affected packages from developer workstations, gaming endpoints, CI runners, caches, and internal NuGet mirrors.
2. Treat `DotnetTool` packages as executable software, not passive library dependencies. Review `tools/` contents, package publisher, repository metadata, and outbound behavior before installing or allowlisting.
3. Alert on `dotnet tool install` for unknown packages and on .NET tool child processes spawning hidden `powershell.exe` with `w32tm /resync`.
4. Hunt for .NET processes connecting to `dns.google/resolve`, `github[.]com/pepegit666`, `huggingface[.]co/buckets/pepegit666`, `bots.pepesoft[.]ru`, `t[.]me/pepesoft777`, or `196[.]16[.]3[.]71:9528`.
5. Search endpoints for `pepesoft.exe`, the shared mutex GUID, `%LOCALAPPDATA%\\Windows Src`, `%APPDATA%\\pepesoft`, `./libgg/chat_ids.txt`, `./token.txt`, and `credentials.txt`.
6. If the tool ran, assume screen-visible secrets and local tool credentials may have been exposed where screenshot-capable payloads were present. Rotate credentials that were entered into the tool or visible on screen while it executed.
7. Prefer CI and endpoint controls that restrict ad hoc package-manager tool installation; pin approved .NET tools and block remote-download-and-execute behavior from package-installed binaries.

## Related pages
- [Braintree.Net NuGet payment skimmer](braintree-net-nuget-payment-skimmer.md)
- [Paysafe / Skrill / Neteller npm and PyPI typosquat stealer campaign](paysafe-skrill-neteller-npm-pypi-typosquats.md)
- [Sicoob.Sdk NuGet banking certificate stealer](sicoob-sdk-nuget-banking-certificate-stealer.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- Socket: https://socket.dev/blog/11-malicious-nuget-tools-pose-as-game-cheats
