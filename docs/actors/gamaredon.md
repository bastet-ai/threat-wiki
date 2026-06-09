# Gamaredon

## Summary
**Gamaredon** is a Russia-linked cyberespionage group focused on Ukraine. Public sources also track the cluster as **Primitive Bear**, **ACTINIUM**, **Shuckworm**, **UAC-0010**, **Armageddon**, and **Trident Ursa**.

Sekoia's June 2026 "FSB's matryoshka" reporting describes a January 2026 infection chain using WinRAR path traversal exploitation, HTA / VBScript staging, USB and network-share worming, registry-based configuration, and document-stealing malware. Sekoia states the group is officially operated by Russia's FSB; keep attribution phrasing tied to the cited source.

Trend Micro's June 2026 follow-up says Earth Dahu / Gamaredon continued using WinRAR **CVE-2025-8088** exploit archives from at least September 2025 through April 2026. Trend Micro also reports a separate UAC-0226 / SHADOW-EARTH-066 chain using the same flaw, so treat WinRAR exploitation as a shared Ukraine-theater entry point rather than a Gamaredon-only signature.

## Tags
- Russia
- FSB
- Ukraine
- APT
- espionage
- UAC-0010
- Gamaredon
- Primitive Bear
- ACTINIUM
- Shuckworm
- Armageddon
- Trident Ursa
- WinRAR
- CVE-2025-8088
- VBScript
- PowerShell
- USB worm
- document theft

## Primary motivation
- **Espionage** against Ukrainian government, military, critical-infrastructure, and strategic networks.
- **Long-term access** through multi-stage malware where each stage can act as a backdoor or configuration-updating component.
- **Document collection and propagation** through local, network-share, and removable-drive monitoring.

## Naming and affiliation
- Sekoia uses **Gamaredon** and maps public malware naming into a unified Gamma* taxonomy.
- CERT-UA commonly tracks Gamaredon activity as **UAC-0010**.
- Microsoft has used **ACTINIUM**; other public names include **Primitive Bear**, **Shuckworm**, **Armageddon**, and **Trident Ursa**.
- Avoid merging Gamaredon with broader Russian military clusters unless a primary source explicitly joins the activity.
- Avoid merging Gamaredon with **UAC-0226 / SHADOW-EARTH-066** solely because both exploited WinRAR CVE-2025-8088; Trend Micro separates the clusters by tooling, C2, and post-exploitation chain.

## 2026 Sekoia reporting highlights
- Initial access used weaponized xHTML and a malicious RAR archive exploiting WinRAR **CVE-2025-8088** to drop an HTA file into the Windows Startup directory.
- The staged chain used **GammaPhish**, **GammaLoad**, **GammaWorm**, and **GammaSteel** components.
- **GammaWorm** propagated through USB drives and network shares by hiding legitimate directories and replacing them with malicious `.lnk` shortcuts.
- **GammaSteel** staged encrypted modules in the Windows registry, monitored local/network/removable media and active file changes, and exfiltrated targeted documents to S3-compatible cloud storage with fallback C2 paths.
- Dead-drop resolvers used legitimate-looking platforms such as Telegram, Telegraph, Teletype, Cloudflare Workers, and Supabase to maintain dynamic C2 configuration.

## 2026 Trend Micro WinRAR follow-up
- Trend Micro attributes an HTA-based CVE-2025-8088 chain to Earth Dahu / Gamaredon with high confidence.
- Samples dropped a hidden ADS payload into Startup: either an HTA directly or an obfuscated VBS / VBE downloader that retrieved an HTA from `trycloudflare[.]com`.
- Trend Micro says spear-phishing activity ran from December 2025 through April 2026 and used compromised Ukrainian government and free-email accounts.
- The report emphasizes unmanaged WinRAR installations as the reason a patched July 2025 archive-client flaw remained a reliable 2026 entry point.

## Defender signals
- `mshta.exe`, `wscript.exe`, or hidden PowerShell launched from Startup-folder HTA artifacts, RAR-delivered payloads, or suspicious xHTML lure chains.
- WinRAR exploitation paths that place hidden HTA files into Startup after opening untrusted archives.
- VBScript loaders that fingerprint the host, update registry-stored network configuration, and fetch arbitrary VBScript from remote infrastructure.
- NTFS Alternate Data Streams used to hide worm modules.
- USB or network-share directories suddenly hidden and replaced with `.lnk` shortcuts using Ukrainian lure text.
- Registry keys under `HKCU\Console\` such as `WindowsUpdates`, `WindowsResponby`, `WindowsDetect`, `URLTeletype`, `WindowsTelegra`, `URLTelegra`, and `IpURL`.
- High-frequency requests to dead-drop resolver platforms from non-browser processes, including `supabase[.]co`, `graph[.]org`, `workers[.]dev`, `teletype[.]in`, `telegra[.]ph`, and `t[.]me`.

## Related pages
- [Gamaredon GammaPhish / GammaWorm / GammaSteel chain](../ops/gamaredon-gammaphish-gammaworm-gammasteel-chain.md)
- [UAC-0226 / SHADOW-EARTH-066](uac-0226-shadow-earth-066.md)
- [Ghostwriter](ghostwriter.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](../ops/apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)

## Sources
- Trend Micro: https://www.trendmicro.com/en_us/research/26/f/old-winrar-flaw-fuels-attacks-on-ukraine.html
- Sekoia: https://blog.sekoia.io/fsbs-matryoshka-1-3-gamaredons-gifts-that-keeps-unpacking-gammaphish-and-gammaworm/
- The Hacker News summary: https://thehackernews.com/2026/06/gamaredon-exploits-winrar-to-deliver.html
