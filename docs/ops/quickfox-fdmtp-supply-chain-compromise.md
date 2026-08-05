# QuickFox FDMTP software supply-chain compromise

## Summary
FortiGuard Labs disclosed on August 4, 2026 that Windows installers for **QuickFox**, a VPN proxy and game accelerator used largely by overseas Chinese users, had been trojanized since at least August 2025. Malicious JavaScript added to an Electron renderer downloaded a target-selection loader, which installed the modular **FDMTP** backdoor only on selected Windows systems.

Fortinet identified affected Windows builds after version 3.0.35 and before the remediated version 3.59.6. QuickFox removed the malicious components after Fortinet notified it and began an internal investigation. Fortinet reported that campaign infrastructure remained active at publication time.

## Tags
- ops
- operations
- supply-chain
- QuickFox
- FDMTP
- Windows
- Electron
- JavaScript
- DLL sideloading
- execution guardrails
- backdoor
- espionage
- China-nexus
- Mustang Panda
- Twill Typhoon
- developer-targeting
- cryptocurrency
- translation software

## Why this matters
- The malicious code was bundled into a legitimate installer and ran inside QuickFox's Electron process tree, weakening simple publisher, filename, and parent-process trust.
- The first stage deliberately rejected systems running Steam and required at least one of 26 administration, development, cryptocurrency, messaging, or Chinese translation applications. Fortinet assesses this likely filtered out personal gaming systems and prioritized corporate or otherwise valuable endpoints.
- The victim-selection list included Git, IntelliJ IDEA, Visual Studio Code, Xshell, MobaXterm, Navicat, DBeaver, cryptocurrency wallets, Telegram, and multiple Chinese translation tools. This supports developer, administrator, cryptocurrency, and cross-border professional exposure checks without proving the final victim-selection objective.
- Fortinet identified several infected victims but observed little post-exploitation activity beyond initial enumeration. The initial compromise appears opportunistic, with centralized target validation likely preceding selective operator tasking.
- The campaign evolved from an embedded FDMTP payload to an encrypted external payload and rotated staging domains and API names, so defenders should prioritize behavior, file paths, process lineage, and protocol patterns over one static indicator.

## Affected scope and response
Fortinet's available installer set was incomplete because QuickFox does not publish a full Windows release timeline or historical installer archive. Its tested set found versions 3.0.29, 3.0.30, and 3.0.35 clean; versions 3.0.51.0/3.51.0, 3.52.0, 3.55.0, 3.55.5, 3.59.3, and 3.59.5 trojanized; and 3.59.6 clean after vendor remediation.

Fortinet places introduction of the malicious component between July 25 and August 13, 2025. Some macOS builds inherited the modified HTML, but the downloaded loader's Windows-only guardrail prevented the infection chain from progressing. Fortinet found no equivalent initial-stage behavior in the Android or iOS applications.

Organizations should not use the incomplete observed-version table as a sole exclusion test. Inventory all QuickFox use, preserve installers and endpoint evidence, upgrade to a vendor-confirmed clean build, and investigate any Windows system that ran an uncertain build during the exposure window.

## Infection chain
1. The installer contains two added JavaScript references in `<version>.7z\resources\app.asar\candy\core\service\index.html`.
2. The Electron renderer retrieves `firebase-app-compat.js` and a legitimate Firebase decoy, `firebase-analytics-compat.js`, from the typosquatted `cdns3.51quickfox[.]cn` rather than the legitimate `51quickfox[.]com` infrastructure.
3. The obfuscated loader checks for Windows, queries C2 to avoid reinfection, and launches `cmd.exe /c tasklist` from a QuickFox child process.
4. It exits if `steam.exe` is present or if none of its 26 target-process strings match.
5. It downloads `update.zip` to `%TEMP%\quickfox\update.zip`, extracts it under `%APPDATA%\Local\Temp\quickfox\updated\`, creates one-byte mutex `data.dat`, and launches legitimate Microsoft binary `csmonitor.exe`.
6. `csmonitor.exe` sideloads malicious `Microsoft.ServiceHosting.Tools.dll`. The first generation embedded `Client.dll`; the second decrypted an AES-128-ECB `update.bin` or `config.bin` payload and reflectively loaded FDMTP.
7. FDMTP registers through a staging domain with requests such as `GET /GetCluster?protocol=DotNet-TcpFDMTP&tag=<campaign>`, receives cluster IPs and ports, and opens its TouchSocket Duplex Message Transport Protocol channel.
8. The implant can survey the host, enumerate processes, load server-provided plugins, store compressed plugin assemblies under `HKCU\SOFTWARE\Microsoft\IME\{HWID}`, transfer files, and execute additional payloads.

## Target-selection process pivots
High-value process strings included:

- remote administration and database tools: `xshell`, `finalshell`, `MobaXterm`, `Tabby`, `navicat`, `dbeaver`;
- developer tooling: `git.exe`, `idea64.exe`, `sublime_text`, `notepad++.exe`, `Code.exe`;
- cryptocurrency software: `Exodus.exe`, `Binance.exe`, `Ledger`, `Trezor`;
- communications and translation software: `telegram.exe`, `SafeW.exe`, `Hello-GPT.exe`, `posend`, and several Chinese-language translation-product strings.

Treat these as victim-filter context, not malicious processes. The stronger behavior is QuickFox/Electron spawning `cmd.exe` for process discovery and then writing and running the sideload chain from the `quickfox\updated` directory.

## Attribution and confidence
- Fortinet did **not** confidently attribute the QuickFox compromise to a named actor.
- It found high-confidence tooling and infrastructure continuity with a Darktrace-reported FDMTP campaign publicly associated with **Twill Typhoon / Mustang Panda**, including shared cluster IPs, code structure, loader components, and DLL-sideloading design.
- Those technical links show use of the same FDMTP ecosystem and infrastructure. Limited visibility into second-stage operator activity prevents a confident Mustang Panda attribution for the software-supply-chain access itself.
- Hypotheses include Chinese citizens living abroad and professionals who interact with Chinese speakers in trade or diplomacy. Neither is confirmed without second-stage victim context.

## Indicators and hunting pivots

### Files and registry
- modified `resources\app.asar\candy\core\service\index.html`
- `%TEMP%\quickfox\update.zip`
- `%APPDATA%\Local\Temp\quickfox\updated\csmonitor.exe`
- `%APPDATA%\Local\Temp\quickfox\updated\Microsoft.ServiceHosting.Tools.dll`
- collocated `update.bin`, `config.bin`, and one-byte `data.dat`
- `HKCU\SOFTWARE\Microsoft\IME\{HWID}` plugin storage
- legitimate `csmonitor.exe` loading `Microsoft.ServiceHosting.Tools.dll` from a user-writable QuickFox temporary directory

### SHA-256
- `2b6cdafdfe427a3de1a94a8a2ca1f09fc4c8f90e4f59089fd9b35b73185ed01c` — generation 1 loader with embedded FDMTP
- `795594ad5e6f2868cc4d8ed12dabf4f3999a1477c6b250527c5ede9a98528fb9` — generation 2 loader
- `6634339b813e6105b5138de6ab67b016b8dfbf49233c29de9bab3207e8b50d24` — generation 2 `config.bin` loader variant
- `dc666e9c148bbca5e21d8c9a97143575c075f53360f135e0191aed9e8278d396` and `5cbb64375636e83b5f17d6083633cecc02e2a5f4168cd7cca5cdee36cca9b38` — encrypted `update.bin` payloads
- `a53d756f28457b1c4a239c91cdec8ed7b7da67a93e332e6df9621cbef8417474` — encrypted `config.bin` payload

### Network
- `cdns3.51quickfox[.]cn` — malicious domain masquerading as QuickFox infrastructure
- `/script/firebase-app-compat.js` — obfuscated loader
- `/2025090411/update.zip` — sideload bundle
- `www.icloud-cdn[.]net`, `www.google-apis[.]net`, `www.techcheck1[.]com`, `www.yahoo-cdn[.]it[.]com`, `www.wangmeng[.]xyz`, `www.wangmengsb[.]com`, and `www.wangmeng66[.]top` — reported staging and registration domains
- registration paths including `/GetCluster`, `/GetSlaver`, `/GetGateways`, `/GetEndpoints`, `/GetServers`, `/GetHosts`, and `/GetNodes`
- FDMTP cluster traffic on ports Fortinet rendered as `20800-208016`; validate against the source IOC table and local telemetry rather than assuming the displayed upper bound is a single valid TCP port

Cloudflare and shared-hosting IPs in the source should not be blocked without domain, TLS, time, and process context.

## Defender actions
1. Inventory QuickFox across software management, EDR, browser/download, DNS, proxy, and filesystem telemetry. Include unmanaged endpoints used by translators, developers, administrators, and traveling staff.
2. Preserve the installer, `app.asar`, QuickFox process tree, temporary files, registry plugin store, DNS/proxy logs, and any FDMTP traffic before remediation.
3. Upgrade to a vendor-confirmed clean release. If an affected or uncertain Windows installer ran, treat the endpoint as compromised even if FDMTP was not immediately observed; guardrails and C2 availability can create selective execution.
4. Hunt for QuickFox child processes spawning `cmd.exe`/`tasklist`, followed by `update.zip`, `data.dat`, `csmonitor.exe`, and DLL loading from user-writable paths.
5. Isolate confirmed hosts, acquire volatile and disk evidence, remove persistence only after collection, rotate credentials exposed to the endpoint, and rebuild from a known-clean image where FDMTP executed.
6. Review source-control, remote-administration, database, messaging, cryptocurrency, cloud, and translation-service accounts used from confirmed hosts. Scope activity after the earliest uncertain QuickFox execution.
7. Monitor software inventories for consumer VPN/accelerator tools that bypass normal procurement. Supply-chain risk can enter through software associated with travel, language access, or regional connectivity rather than standard enterprise packages.

## Open questions
- How QuickFox's build or release path was modified and whether signing, source, CI, distribution, or vendor credentials were compromised.
- Complete affected-version, download, and victim scope.
- Which initially infected systems were selected for additional operator tasking and what data or access was obtained.
- Whether the FDMTP infrastructure remains active or has rotated beyond the public indicator set.
- Whether additional software products delivered the same loader and infrastructure.
- Whether later evidence supports attribution beyond the current FDMTP/Twill Typhoon technical overlap.

## Related pages
- [FDMTP](../tools/fdmtp.md)
- [Mustang Panda](../actors/mustang-panda.md)
- [Mustang Panda ZOHOMURK / MINIRECON India campaigns](mustang-panda-zohomurk-minirecon-india-campaigns.md)

## Sources
- FortiGuard Labs: [QuickFox Supply Chain Attack Used to Deploy FDMTP Implant](https://www.fortinet.com/blog/threat-research/quickfox-supply-chain-attack-used-to-deploy-fdmtp-implant)
- The Hacker News: [QuickFox Supply Chain Attack Delivers FDMTP Backdoor via Trojanized Windows Installer](https://thehackernews.com/2026/08/quickfox-supply-chain-attack-delivers.html) — secondary discovery pointer; technical claims above are grounded in Fortinet's primary report
