# Gamaredon

## Summary
**Gamaredon** is a Russia-linked cyberespionage group focused on Ukraine. Public sources also track the cluster as **Primitive Bear**, **ACTINIUM**, **Shuckworm**, **UAC-0010**, **Armageddon**, and **Trident Ursa**.

ESET's June 2026 2025-retrospective says Gamaredon maintained high operational tempo against Ukrainian government and military institutions, ran 35 observed spear-phishing campaigns, added six PowerShell tools, resurrected the older **PteroSetup** VBScript weaponizer, and increasingly hid C2 and exfiltration through legitimate services such as tunnels, workers, DDNS/PaaS providers, dead drops, Dropbox, GoFile, and S3-compatible cloud storage. ESET also reports an early-2025 collaboration with **Turla**, so Russia-linked Ukraine intrusions with Gamaredon artifacts may require broader actor scoping.

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
- PteroPaste
- PteroSetup
- PteroVDoor
- PteroPSDoor
- PteroBox
- cloud storage exfiltration
- dead drop resolver
- tunnel services
- Cloudflare Workers
- Microsoft dev tunnels
- Turla collaboration
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

## ESET 2025 retrospective
- ESET says Gamaredon exclusively targeted Ukrainian governmental and military institutions throughout 2025 and observed 35 distinct spear-phishing campaigns, with larger and more frequent campaigns in the second half of the year.
- Initial access still leaned on archive attachments or XHTML / HTML-smuggling lures that delivered HTA downloaders, but from September 26, 2025 onward Gamaredon also abused WinRAR **CVE-2025-8088** to place HTA downloaders in Startup for login-time execution.
- New PowerShell tooling included **PteroDee**, **PteroCache**, **PteroDum**, **PteroOdd**, **PteroEffigy**, and **PteroPaste**; ESET describes PteroPaste as a downloader / USB weaponizer / runner that evolved from Rentry staging to Dropbox-delivered encrypted C2 hostnames and tunnel-hidden infrastructure.
- Gamaredon resurrected **PteroSetup**, a VBScript weaponizer that replaces installer-like executables on fixed, removable, and network drives with self-extracting archives that run both the original installer and malicious code.
- Infrastructure hiding expanded from `trycloudflare.com` into `workers.dev`, Microsoft `devtunnels.ms`, `loophole.site`, No-IP DDNS, Clever Cloud, Supabase, and layered dead drops across Telegram, Telegra.ph, Teletype, Rentry, write.as, Dropbox, GoFile, DEV Community, Mastodon, lesma, nopaste.net, and Paste.ee.
- File stealers **PteroVDoor** and **PteroPSDoor** were upgraded for S3-compatible cloud-storage exfiltration, with configurations moving from Wasabi to Tebi and then Intercolo; **PteroBox** continued Dropbox uploads and one newer variant used `rclone`.

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
- [Gamaredon 2025 tunnels, workers, dead drops, and cloud exfiltration](../ops/gamaredon-2025-tunnels-workers-dead-drops.md)
- [UAC-0226 / SHADOW-EARTH-066](uac-0226-shadow-earth-066.md)
- [Turla](turla.md)
- [Ghostwriter](ghostwriter.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](../ops/apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)

## Sources
- ESET WeLiveSecurity: https://www.welivesecurity.com/en/eset-research/gamaredon-2025-leveraging-tunnels-workers-dead-drops-new-alliances/
- Trend Micro: https://www.trendmicro.com/en_us/research/26/f/old-winrar-flaw-fuels-attacks-on-ukraine.html
- Sekoia: https://blog.sekoia.io/fsbs-matryoshka-1-3-gamaredons-gifts-that-keeps-unpacking-gammaphish-and-gammaworm/
- The Hacker News summary: https://thehackernews.com/2026/06/gamaredon-exploits-winrar-to-deliver.html
