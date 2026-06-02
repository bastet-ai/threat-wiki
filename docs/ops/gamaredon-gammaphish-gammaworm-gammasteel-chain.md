# Gamaredon GammaPhish / GammaWorm / GammaSteel chain

## Summary
Sekoia's June 2026 **FSB's matryoshka** report reconstructs a January 2026 **Gamaredon** infection chain against Ukraine-linked environments. The chain used a WinRAR path-traversal exploit, Startup-folder HTA execution, multi-stage VBScript loaders, USB and network-share worming, registry-staged configuration and modules, and a document stealer that watches files as they are stored, moved, or edited.

The durable defender lesson is that Gamaredon's chain is not a single loader-to-payload sequence. Sekoia describes each layer as a backdoor-capable stage that can update configuration, retrieve new code, or keep access alive through legitimate-looking dead-drop platforms.

## Tags
- ops
- operations
- Russia
- FSB
- Ukraine
- Gamaredon
- UAC-0010
- espionage
- WinRAR
- CVE-2025-8088
- GammaPhish
- GammaLoad
- GammaWorm
- GammaSteel
- VBScript
- PowerShell
- HTA
- mshta
- LNK
- USB worm
- NTFS ADS
- Telegram
- dead drop resolver
- document theft

## Why this matters
- Sekoia ties a 2026 Gamaredon chain to **CVE-2025-8088** WinRAR path traversal, showing continued operational value in archive-client exploitation and Startup-folder execution.
- **GammaWorm** spreads through USB drives and network shares, a risk for segmented or air-gapped Ukrainian environments where removable media remains operationally relevant.
- **GammaSteel** monitors local drives, network drives, inserted USBs, and specific files as they are saved or modified, so document exposure is not limited to static file sweeps.
- The chain uses legitimate platforms as dead-drop resolvers, including Telegram, Telegraph, Teletype, Cloudflare Workers, and Supabase, making simple domain-blocking brittle.

## Reported chain
- **Initial discovery:** Sekoia says opportunistic YARA hunting in late December 2025 surfaced xHTML lure activity; by January 2026, partner-provided compromised-host artifacts allowed reconstruction of a larger Gamaredon chain.
- **GammaPhish / initial access:** weaponized xHTML delivered a malicious RAR archive. The archive exploited WinRAR **CVE-2025-8088** to extract a hidden HTA file into the user's Windows Startup directory.
- **HTA execution:** the Startup HTA launched through `mshta.exe` and contacted remote staging infrastructure. Sekoia notes the live staging infrastructure returned empty payloads during some analysis attempts.
- **GammaLoad / staging:** recovered VBScript loaders ran in a cascade of multiple stages, fingerprinted the host, updated registry-stored network configuration via dead-drop resolvers, and fetched arbitrary VBScript payloads from C2 servers.
- **GammaWorm / propagation:** forensic artifacts showed a highly obfuscated VBScript worm that persisted through scheduled tasks, hid core modules in NTFS Alternate Data Streams, targeted USB and network drives, hid legitimate directories, and replaced them with malicious `.lnk` shortcuts.
- **GammaSteel / exfiltration:** replaying GammaLoad network requests let Sekoia retrieve a newer GammaSteel variant. Sekoia describes it as a modular PowerShell stealer that writes 71 DPAPI-encrypted modules into the Windows registry, scans local and network drives, monitors newly inserted USBs, watches specific files in real time, and exfiltrates targeted documents to S3-compatible cloud storage with operator C2 fallback.

## Dead-drop and configuration behavior
- GammaWorm keeps dynamic network configuration in the Windows registry and queries it in a loop before executing code returned by C2.
- Sekoia highlights dead-drop resolver abuse across common platforms and services, including `supabase[.]co`, `graph[.]org`, `workers[.]dev`, `teletype[.]in`, `telegra[.]ph`, and Telegram paths.
- Sekoia's example registry keys under `HKCU\Console\` include `WindowsUpdates`, `WindowsResponby`, `WindowsDetect`, `URLTeletype`, `WindowsTelegra`, `URLTelegra`, and `IpURL`.

## Defender notes
- Patch WinRAR and reduce exposure to archive files from untrusted sources; specifically review paths where archive extraction can write into Startup or other autorun locations.
- Hunt for hidden HTA files and `mshta.exe` launches tied to user Startup folders after RAR/xHTML lure handling.
- Alert on `wscript.exe` or hidden PowerShell processes making high-frequency requests to Telegram, Telegraph, Teletype, Cloudflare Workers, Supabase, or graph-style dead-drop pages.
- Inspect USB and network shares for hidden legitimate directories with sibling malicious `.lnk` replacements, especially using Ukrainian social-engineering lure text.
- Search for NTFS Alternate Data Streams on suspicious script, shortcut, and removable-media paths.
- Review scheduled tasks created by script interpreters and unknown tasks around the first-seen time of RAR, HTA, or xHTML artifacts.
- Treat GammaSteel-like registry module staging as credential and document exposure: collect volatile evidence, preserve registry hives, then rotate credentials and review documents accessible from the host.

## Selected indicators and pivots
- **Component names:** `GammaPhish`, `GammaLoad`, `GammaWorm`, `GammaSteel`.
- **Exploit / vulnerability:** WinRAR `CVE-2025-8088` path traversal.
- **Example registry hive:** `HKCU\Console\`.
- **Example registry values:** `WindowsUpdates`, `WindowsResponby`, `WindowsDetect`, `URLTeletype`, `WindowsTelegra`, `URLTelegra`, `IpURL`.
- **Example dead-drop resolver platforms:** Telegram, Telegraph, Teletype, Cloudflare Workers, Supabase.
- **Sekoia sample hashes:** GammaPhish `1794369214b7f62e70a0485e61335c61`; GammaWorm `8e1624d110c090ff57d4b493a9107c66`.
- **Sekoia example C2:** `104.194.140[.]6`.

Use Sekoia's source page and intelligence feed for current network indicators; prioritize behavior because Gamaredon rotates infrastructure quickly.

## Related pages
- [Gamaredon](../actors/gamaredon.md)
- [Ghostwriter](../actors/ghostwriter.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)

## Sources
- Sekoia: https://blog.sekoia.io/fsbs-matryoshka-1-3-gamaredons-gifts-that-keeps-unpacking-gammaphish-and-gammaworm/
- The Hacker News summary: https://thehackernews.com/2026/06/gamaredon-exploits-winrar-to-deliver.html
