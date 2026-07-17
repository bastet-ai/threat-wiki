# TELEPUZ ClickFix / VIDAR campaign

## Summary
Elastic Security Labs reported an active **ClickFix → VIDAR → TELEPUZ** delivery chain operating since late April 2026. The chain begins with user-pasted PowerShell from a malicious page, downloads a VIDAR Go variant, and then uses VIDAR to stage the TELEPUZ stager and main DLL from attacker-controlled domains.

This operation matters because it shows ClickFix remaining a reliable first step for modular malware-as-a-service delivery, while TELEPUZ adds fast-moving fallback C2 and browser-manipulation modules that can support credential theft, session theft, and financial form tampering.

## Tags
- ops
- operations
- ClickFix
- VIDAR
- TELEPUZ
- malware delivery
- PowerShell
- MaaS
- Windows malware
- browser credential theft
- web injection
- Telegram dead drop
- Steam profile dead drop
- Polygon blockchain dead drop
- Elastic Security Labs

## Infection chain
1. **ClickFix social engineering:** the victim is instructed to paste and execute a Windows shell command.
2. **PowerShell downloader:** Elastic's example launches PowerShell with `-NoP -w h -ep bypass`, builds `memshowblob[.]forum`, downloads `f322a5fa.exe` from `/api/index.php?a=grab` into `%TEMP%`, removes the Zone.Identifier alternate data stream, and executes it.
3. **VIDAR second stage:** Elastic identifies the downloaded second stage as a VIDAR Go variant with SHA-256 `580b441e2961739fd26e54e0a0ea08351cb10a51839519fc722cfa39ecd0c954`.
4. **TELEPUZ staging:** VIDAR downloads both a TELEPUZ stager (`install.exe`) and main binary (`telepuz.dll`), observed from `hurgadatour[.]shop` in Elastic's analyzed chain.
5. **TELEPUZ persistence and C2:** the main DLL migrates to install / persistence paths, installs service persistence where permissions allow, and communicates with WebSocket C2 or public-resource fallback control.

## Campaign timeline and infrastructure pattern
Elastic observed the first TELEPUZ sample submission on May 2, 2026, with Telegram and Polygon artifacts indicating activity around April 27-29. Build submissions increased steadily, with a significant spike in early June.

Payload download URLs commonly used paths such as `/files/telemetriawork/telepuz.dll`, with variants including `/files/telemetrywork/telepuz`, `/files/telemetrywork/telepuz.dll`, `/telemetry/network/telepuz.dll`, and related misspellings. Elastic notes that staging domains were often Cloudflare-protected, while the smaller set of C2 domains appeared to be compromised websites in Brazil and India.

### Elastic-reported staging domains
| First seen | Domain / URL |
| --- | --- |
| 2026-05-09 | `chubrik[.]sbs/files/xK7mR9pL2nQw5tY8/ygvfuyze.dll` |
| 2026-05-14 | `betalegenda[.]cfd/files/xK7mR9pL2nQw5tY8/kmwvogwx.dll` |
| 2026-05-19 | `mavpaprokla[.]lat/files/telemetriawork/telepuz.dll` |
| 2026-05-26 | `comicstar[.]lat/files/telemetriawork/telepuz.dll` |
| 2026-05-28 | `bigblower[.]click/files/telemetriawork/telepuz.dll` |
| 2026-06-05 | `momasites[.]lol/files/telemetriawork/telepuz.dll` |
| 2026-06-07 | `momasites[.]com/files/telemetrywork/telepuz` |
| 2026-06-07 | `mamsites[.]lol/files/telemetrywork/telepuz.dll` |
| 2026-06-07 | `hardenedom[.]shop/files/telemetriawork/telepuz.dll` |
| 2026-06-07 | `hardendedom[.]shop/files/lemetriawork/epuz.dll` |
| 2026-06-08 | `hardendom[.]shop/files/telemetry/telepuz.dll` |
| 2026-06-10 | `hardeneddom[.]shop/files/telemetrywork/telepuz` |
| 2026-06-11 | `netblokirovka[.]asia/files/telemetriawork/telepuz.dll` |
| 2026-06-12 | `netblokir[.]asia/files/telemetriawork/telepuz.dll` |
| 2026-06-14 | `netlobikrovka[.]asia/files/telemetriawork/telepuz.dll` |
| 2026-06-15 | `neblokirovka[.]as/telemetry/network/telepuz.dll` |
| 2026-06-17 | `kidsko[.]shop/files/telemetriawork/telepuz.dll` |
| 2026-06-22 | `mazaporka[.]shop/files/telemetriawork/telepuz.dll` |
| 2026-06-24 | `172.67.215[.]214/files/telemetriawork/telepuz.dll` |
| 2026-06-25 | `hurgadatour[.]shop/files/telemetriawork/telepuz.dll` |
| 2026-06-29 | `krabsburger[.]xyz/files/telemetriawork/telepuz.dll` |
| 2026-06-30 | `zewaplus[.]club/files/telemetriawork/telepuz.dll` |
| 2026-07-06 | `172.67.165[.]144/files/telemetriawork/telepuz.dll` |

### C2 and fallback infrastructure
- `cal.joycedoula[.]com[.]br` — earliest sample configuration.
- `cal.snehamumbai[.]org` — latest C2 reported by Elastic.
- `t[.]me/chanadarkpart` — Telegram fallback profile.
- `steamcommunity[.]com//profiles/76561199705801219` — Steam fallback profile.
- `codebasecode[.]com` — DNS fallback query target.
- Polygon contract `0xf55Bea1FdCf1c3ABb39ab92567C09aC1BFf6753E` with method selector `0xc3f909d4`.

## Defender guidance
- Detect and block ClickFix-style clipboard instructions that launch hidden PowerShell with policy bypass and download from `/api/index.php?a=grab` into `%TEMP%`.
- Treat `memshowblob[.]forum` downloader execution or the VIDAR hash `580b441e2961739fd26e54e0a0ea08351cb10a51839519fc722cfa39ecd0c954` as TELEPUZ exposure until ruled out.
- Search endpoint telemetry and proxy logs for TELEPUZ staging path families: `/files/telemetriawork/`, `/files/telemetrywork/`, `/telemetry/network/`, `telepuz.dll`, `telepuz`, and `install.exe` following VIDAR execution.
- Hunt for `rundll32.exe` loading DLLs from `%AppData%` or `%ProgramData%` paths that resemble device, print, Qualcomm, state-repository, or recovery software.
- Block the reported C2 and fallback pivots, but do not rely only on domain blocking: TELEPUZ can update fallback C2 through public profiles and Polygon smart-contract data.
- If TELEPUZ execution is confirmed, preserve the host before remediation, collect DLLs / service keys / mutex evidence, rotate browser, SSO, VPN, and financial-application credentials, and review browser sessions for web-injection or cookie theft.

## Related pages
- [TELEPUZ](../tools/telepuz.md)
- [ACR Stealer](../tools/acr-stealer.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [Vidar / XMRig Factory-v3 malvertising campaign](vidar-xmrig-factory-v3-malvertising-campaign.md)

## Sources
- Elastic Security Labs: [TELEPUZ: a modular MaaS malware spreading via CLICKFIX-VIDAR chains](https://www.elastic.co/security-labs/telepuz-maas-malware-clickfix)
