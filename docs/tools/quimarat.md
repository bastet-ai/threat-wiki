# QuimaRAT

## Summary
QuimaRAT is a commercialized, Java-based remote access trojan (RAT) platform analyzed by LevelBlue SpiderLabs in June 2026 and surfaced publicly by The Hacker News on July 6, 2026. LevelBlue describes it as a cross-platform Windows, Linux, and macOS RAT sold as malware-as-a-service (MaaS), with a thin base client for lifecycle control and a much larger plugin/protocol surface for follow-on capability.

Treat QuimaRAT as a modular RAT ecosystem rather than a single static implant. The analyzed JAR confirmed persistence, C2 communication, plugin loading, download/execute behavior, and Windows fileless shellcode execution; many credential-theft, surveillance, and post-exploitation commands appeared as protocol-only labels and should guide hunts without being overstated as base-client functionality.

## Tags
- tools
- malware
- RAT
- QuimaRAT
- Java malware
- cross-platform malware
- Windows
- Linux
- macOS
- malware-as-a-service
- MaaS
- plugin architecture
- fileless execution
- persistence
- C2
- credential theft
- LevelBlue
- SpiderLabs

## Why this matters
- QuimaRAT lowers the barrier for cross-platform remote access by packaging a Java client, builder workflow, multiple output formats, operator panel marketing, and subscription pricing.
- The base client supports runtime plugin delivery, loading, unloading, caching, and reuse, so observed capability can change after initial infection.
- Java plus embedded Java Native Access (JNA) libraries gives the same family OS-specific persistence and native API access across Windows, Linux, and macOS estates.
- The protocol exposes a broad operational vocabulary for file management, surveillance, credential theft, and post-exploitation; defenders should hunt for plugin-delivered behavior after C2 registration rather than relying only on the first JAR's static handlers.

## Public reporting
LevelBlue's analyzed sample was a 3.59 MB Java SE 8 JAR named `SWFT.jar`, with SHA-256 `bb0fbcb1e47ec04aa55555f3769fbc6f09694de1e9baae59260356b26b5af6a7`. The product was advertised as **QuimaRAT v2.0** with claims including "70+ modules", "AES-256 encryption", "FUD", a GUI panel, and builder outputs for `JAR`, `EXE`, `APP`, `SH`, `BAT`, `VBS`, and native builds.

Reported MaaS pricing:

- $150 for one month;
- $300 for three months;
- $500 for six months;
- $700 for twelve months;
- $1,200 for lifetime access.

LevelBlue notes that actor-side marketing should not be treated as proof that every advertised module exists in the analyzed base sample.

## Architecture and configuration
- The codebase used Maven project structure with `rat-common` and `rat-client` modules.
- Maven Shade relocation changed package names from `com.quimaRAT.client` to `org.svcruntime.app` and from `com.quimaRAT.common` to `org.svcruntime.core`, reducing obvious family strings in the final artifact.
- The JAR bundled JNA native libraries for Windows, Linux, and macOS across multiple architectures.
- The client loaded an encrypted embedded `config.dat` and decrypted it with repeating-key XOR using the hardcoded ASCII key `QuimaRAT20`.
- Configuration fields reported by LevelBlue include `targetOs`, `hosts`, `ip`, `port`, `transport`, `ssl`, `serverId`, `delay`, `installReg`, `installSch`, `installStart`, `installPersist`, `antiVm`, `fileName`, `folder`, `regName`, `binderEnabled`, `binderFileName`, `pastebinEnabled`, `pastebinUrl`, and `certHash`.
- The analyzed configuration used `45.63.24[.]218:4447` over plain TCP, enabled Windows Registry Run-key and Startup-folder persistence, disabled anti-VM checks, and identified the server/campaign value as `MONDAY 1`.

## Execution and persistence
QuimaRAT performs single-instance locking by deriving a `qr_<hash>.lock` filename from the server ID and C2 configuration and placing it in the OS temporary directory. If another instance already holds the lock, the client exits.

Windows persistence observed or supported:

- copy itself under `%APPDATA%\LHQhVxufHZ\rLxqbosgrfBv.txt` while still executing as a valid JAR through `javaw.exe -jar`;
- hide the copied file with `attrib +h +s`;
- create an HKCU Run value named `iGmcYueWny` pointing to `javaw.exe -Xmx128m -jar ...`;
- create `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\iGmcYueWny.lnk` through dynamically generated VBScript;
- optionally create a logon scheduled task through hidden PowerShell and `Register-ScheduledTask`.

Linux persistence supported:

- copy to `~/.local/share/LHQhVxufHZ/rLxqbosgrfBv.txt`;
- create `~/.config/autostart/iGmcYueWny.desktop` launching `java -jar ...`;
- add an `@reboot java -jar ~/.local/share/LHQhVxufHZ/rLxqbosgrfBv.txt` crontab entry.

macOS persistence supported:

- copy to `~/.local/share/LHQhVxufHZ/rLxqbosgrfBv.txt`;
- create `~/Library/LaunchAgents/com.igmcyuewny.plist` with `RunAtLoad` and `KeepAlive`;
- load it through `launchctl load -w`.

## C2 and plugin behavior
- QuimaRAT uses Netty for asynchronous C2 communication and creates a `quima-nio` event loop.
- It supports TCP plus SSL/TLS, HTTPS, and WebSocket transport paths; WebSocket mode uses `wss://<IP>:<PORT>/ws`.
- The analyzed sample used plain TCP to `45.63.24[.]218:4447`.
- Optional Pastebin-style host-update logic can fetch replacement C2 entries formatted as `IP:PORT:TRANSPORT` before connection.
- Watchdog logic checks channel and event-loop health at roughly 15-second intervals and schedules reconnects or fallback recovery threads when C2 drops.
- Confirmed communication paths include `HANDSHAKE`, `HEARTBEAT`, client registration, configuration requests, plugin hash reporting, plugin loading, and plugin unloading.
- LevelBlue confirmed 23 implemented commands and 212 protocol-only commands, for a total protocol surface of 235 commands.

Plugin lifecycle reported by LevelBlue:

1. Receive `LOAD_PLUGIN` packet.
2. Extract encrypted plugin payload.
3. Decrypt base and plugin modules.
4. Load plugin JAR through a custom memory loader.
5. Extract classes and resources.
6. Instantiate the plugin.
7. Register supported packet types.
8. Start plugin and send `PLUGIN_LOADED_ACK`.

Encrypted plugin cache artifacts can remain on disk under `.cache/plugins` even after a plugin is unloaded.

## Capabilities and caveats
Confirmed or base-client-relevant capability includes:

- persistence installation and removal;
- C2 registration, heartbeat, reconnect, and watchdog recovery;
- download-and-execute and send-file-and-execute behavior;
- plugin loading and unloading;
- Windows-only fileless payload execution through `SEND_FILELESS_EXECUTE`;
- Windows shellcode execution using JNA/KERNEL32 calls to allocate memory, mark it executable, create a thread, wait, and free memory.

Protocol-only labels suggest intended expansion into:

- remote file browsing, upload/download, compression, hiding, search, and Defender exclusion actions;
- remote desktop, console, keylogger, webcam, microphone, screenshot, screen recording, hidden browser, HVNC, and clipboard monitoring;
- FTP, browser, email, VPN, RDP, password-manager, wallet, and crypto-clipper theft;
- LSASS dumping, DLL injection, AD enumeration, lateral movement, network/share discovery, AMSI bypass, ETW patching, process hollowing, token theft/impersonation, UAC spoofing, and RDP tunneling.

Keep the distinction: these protocol labels indicate operator design intent and hunting priorities, but LevelBlue did not confirm most of them as implemented in the extracted base client.

## Indicators
Selected indicators from LevelBlue:

- SHA-256: `bb0fbcb1e47ec04aa55555f3769fbc6f09694de1e9baae59260356b26b5af6a7`
- SHA-256: `6c7060ffdd31f5b670b44aba451b379d1e2bd87082c6c35add8d1939095e1195`
- `META-INF/maven/com.quimaRAT/rat-client/pom.xml` SHA-256: `1efd2de821bb8ad8b0308dd22e3e13daf568f035a3fa3f84c1d4f9ff1158282a`
- `META-INF/maven/com.quimaRAT/rat-common/pom.xml` SHA-256: `f0ff0d86d7a64464e3a62078f440c8c9a5a8c4043cf52b0eccfb6dcf7c41ef8f`
- C2 IP: `45.63.24[.]218`
- Domain: `Quima[.]org`
- WebSocket endpoint shape: `wss://45.63.24[.]218:4447/ws`
- Public IP/geolocation checks: `ip-api[.]com`, `ipinfo[.]io/ip`, `api.ipify[.]org`, `checkip.amazonaws[.]com`
- Lock file pattern: `qr_<integer>.lock`
- Windows startup link: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\iGmcYueWny.lnk`
- Windows copied JAR path: `%APPDATA%\LHQhVxufHZ\rLxqbosgrfBv.txt`
- Linux copied JAR path: `~/.local/share/LHQhVxufHZ/rLxqbosgrfBv.txt`
- Linux autostart: `~/.config/autostart/iGmcYueWny.desktop`
- macOS LaunchAgent: `~/Library/LaunchAgents/com.igmcyuewny.plist`
- Plugin cache artifacts matching `.cache/plugins/base-*.dat` and `.cache/plugins/plug-*-*.dat`
- Plugin memory artifact name: `memory-plugins.jar`

## Defender notes
- Hunt for Java processes launched by `javaw.exe` or `java` from user-writable paths with `-jar` pointing to extension-mismatched files such as `.txt`.
- Correlate Java persistence artifacts with long-lived outbound TCP/WebSocket sessions, especially to `45.63.24[.]218:4447` or infrastructure delivered through Pastebin-style host lists.
- Watch for `.cache/plugins/base-*.dat`, `.cache/plugins/plug-*-*.dat`, and `memory-plugins.jar` creation after C2 registration.
- On Windows, prioritize HKCU Run values, Startup-folder `.lnk` creation via `wscript.exe`, hidden PowerShell scheduled-task creation, and Java processes that call VirtualAlloc / VirtualProtect / CreateThread through JNA.
- On Linux, hunt for suspicious `@reboot java -jar` crontab entries and unexpected `.desktop` files under user autostart directories.
- On macOS, hunt for unsigned or user-installed Java LaunchAgents with `RunAtLoad` / `KeepAlive` launching JAR-like payloads from `~/.local/share`.
- During response, preserve the original JAR, decrypted `config.dat` if available, plugin cache files, Java process memory, persistence artifacts, DNS/connection logs, and any downloaded plugin JARs before eradication.
- Avoid both extremes: do not claim that every protocol enum is active in a specific incident, but do treat plugin loading as a high-risk post-compromise event that can materially expand capability.

## Related pages
- [MYRA RAT](myra-rat.md)
- [CrownX](crownx.md)
- [BusySnake Stealer](busysnake-stealer.md)
- [Crypto Clipper Tor / USB worm](../ops/crypto-clipper-tor-usb-worm.md)

## Sources
- LevelBlue SpiderLabs: [https://www.levelblue.com/blogs/spiderlabs-blog/novel-java-based-quimarat-targets-windows-macos-and-linux](https://www.levelblue.com/blogs/spiderlabs-blog/novel-java-based-quimarat-targets-windows-macos-and-linux)
- LevelBlue report PDF: [https://www.levelblue.com/hubfs/Web/Library/Documents_pdf/Threat_Spotlight_An_In_Depth_Analysis_of_QuimaRAT.pdf](https://www.levelblue.com/hubfs/Web/Library/Documents_pdf/Threat_Spotlight_An_In_Depth_Analysis_of_QuimaRAT.pdf)
- The Hacker News: [https://thehackernews.com/2026/07/new-java-based-quimarat-maas-built-to.html](https://thehackernews.com/2026/07/new-java-based-quimarat-maas-built-to.html)
