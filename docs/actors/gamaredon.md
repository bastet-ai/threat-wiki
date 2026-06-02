# Gamaredon

## Summary
**Gamaredon** is a Russia-linked cyberespionage group focused on Ukraine. Public sources also track the cluster as **Primitive Bear**, **ACTINIUM**, **Shuckworm**, **UAC-0010**, **Armageddon**, and **Trident Ursa**.

Sekoia's June 2026 "FSB's matryoshka" reporting describes a January 2026 infection chain using WinRAR path traversal exploitation, HTA / VBScript staging, USB and network-share worming, registry-based configuration, and document-stealing malware. Sekoia states the group is officially operated by Russia's FSB; keep attribution phrasing tied to the cited source.

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

## 2026 Sekoia reporting highlights
- Initial access used weaponized xHTML and a malicious RAR archive exploiting WinRAR **CVE-2025-8088** to drop an HTA file into the Windows Startup directory.
- The staged chain used **GammaPhish**, **GammaLoad**, **GammaWorm**, and **GammaSteel** components.
- **GammaWorm** propagated through USB drives and network shares by hiding legitimate directories and replacing them with malicious `.lnk` shortcuts.
- **GammaSteel** staged encrypted modules in the Windows registry, monitored local/network/removable media and active file changes, and exfiltrated targeted documents to S3-compatible cloud storage with fallback C2 paths.
- Dead-drop resolvers used legitimate-looking platforms such as Telegram, Telegraph, Teletype, Cloudflare Workers, and Supabase to maintain dynamic C2 configuration.

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
- [Ghostwriter](ghostwriter.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](../ops/apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)

## Sources
- Sekoia: https://blog.sekoia.io/fsbs-matryoshka-1-3-gamaredons-gifts-that-keeps-unpacking-gammaphish-and-gammaworm/
- The Hacker News summary: https://thehackernews.com/2026/06/gamaredon-exploits-winrar-to-deliver.html
