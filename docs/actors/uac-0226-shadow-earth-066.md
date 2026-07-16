# UAC-0226 / SHADOW-EARTH-066

## Summary
**UAC-0226** is a Ukraine-targeting intrusion cluster publicly tracked by CERT-UA. Trend Micro temporarily designates the same activity **SHADOW-EARTH-066** and reports that the cluster shifted from macro-enabled Excel droppers to **WinRAR CVE-2025-8088** exploit chains by February 2026.

Trend Micro says the cluster targets Ukrainian military innovation centers, military formations, law-enforcement agencies, and local self-government bodies near Ukraine's eastern border. Its durable defender value is the rapid evolution of **GIFTEDCROOK** from a simple Telegram-exfiltrating browser stealer into an in-memory DLL chain using encrypted dedicated C2.

## Tags
- Russia
- Ukraine
- UAC-0226
- SHADOW-EARTH-066
- GIFTEDCROOK
- WinRAR
- CVE-2025-8088
- NTFS ADS
- LNK
- PowerShell
- in-memory DLL loading
- browser credential theft
- document theft
- Telegram
- RC4
- spear phishing

## Naming and attribution
- **UAC-0226** is CERT-UA's public cluster name.
- **SHADOW-EARTH-066** is Trend Micro's temporary designation for the same malware-lineage cluster.
- Trend Micro describes the activity as Russia-aligned and keeps it distinct from **Earth Dahu / Gamaredon**, even though both clusters exploited the same WinRAR flaw against Ukrainian organizations.
- Do not merge this page with Gamaredon unless a primary source explicitly joins the clusters. Trend Micro's June 2026 reporting stresses that they use different tooling and infrastructure after the shared exploit entry point.

## Reported evolution
- **Early 2025:** CERT-UA documented spear-phishing emails with macro-enabled Excel files using demining, administrative-fine, UAV-production, and destroyed-property compensation themes.
- **Initial GIFTEDCROOK behavior:** payloads included a .NET reverse shell and a C/C++ credential stealer that collected browser credentials from Chrome, Edge, and Firefox, compressed output with PowerShell, and exfiltrated to hardcoded Telegram bot tokens / chat IDs.
- **February 2026 shift:** Trend Micro reports the cluster moved to WinRAR **CVE-2025-8088** exploit archives, LNK Startup-folder persistence, PowerShell loading, and an updated `result.dll` GIFTEDCROOK lineage payload.
- **Operational hardening:** newer payloads use in-memory DLL loading, direct NT system calls, anti-analysis checks, RC4-encrypted C2 URLs, and dedicated command-and-control servers instead of plaintext Telegram exfiltration.

## Defender signals
- RAR archives that display a visible decoy PDF while hidden NTFS Alternate Data Stream entries write a `.lnk` file or payloads outside the extraction directory.
- Unexpected files in user Startup folders after archive extraction, especially when a shortcut launches `cmd.exe` or PowerShell.
- PowerShell loaders that perform in-memory DLL execution and leave little disk-resident payload material.
- C++ x64 stealers sharing GIFTEDCROOK-like traits: Chromium / Firefox credential and cookie collection, DPAPI use through `CryptUnprotectData`, anti-debug / Wine checks, multipart form-data exfiltration, and cleanup of malicious artifacts after upload.
- RC4-encrypted C2 strings in binaries rather than plaintext Telegram bot tokens.
- Browser credential theft plus document collection from endpoints handling Ukrainian government, military, law-enforcement, or local-administration material.

## Related pages
- [Gamaredon](gamaredon.md)
- [Gamaredon GammaPhish / GammaWorm / GammaSteel chain](../ops/gamaredon-gammaphish-gammaworm-gammasteel-chain.md)

## Sources
- Trend Micro: [https://www.trendmicro.com/en_us/research/26/f/old-winrar-flaw-fuels-attacks-on-ukraine.html](https://www.trendmicro.com/en_us/research/26/f/old-winrar-flaw-fuels-attacks-on-ukraine.html)
- The Hacker News summary: [https://thehackernews.com/2026/06/winrar-flaw-exploited-by-russia-aligned.html](https://thehackernews.com/2026/06/winrar-flaw-exploited-by-russia-aligned.html)
