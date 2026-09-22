# SideCopy

## Summary
**SideCopy** is a Pakistan-linked espionage cluster that Seqrite tracks under the broader **Transparent Tribe / APT36** umbrella. Public reporting consistently describes the group targeting South Asian government, defense, diplomatic, and regional entities with spear-phishing lures, Windows shortcut execution chains, and commodity or open-source RATs adapted for persistent access.

Seqrite's June 2026 Operation XENOFISCAL report attributes a campaign against Afghanistan's Ministry of Finance provincial network to SideCopy with **medium-to-high confidence**, citing the LNK-to-`mshta.exe` HTA chain, XenoRAT adoption, registry persistence, and infrastructure overlap with prior SideCopy activity.

## Tags
- Pakistan-linked
- APT36
- Transparent Tribe
- espionage
- Afghanistan
- South Asia
- spear phishing
- LNK
- HTA
- mshta
- XenoRAT
- registry persistence
- ReverseRAT
- mshta chain
- India academia
- TAG-140
- Trellix

## Primary motivation
- **Espionage** against government and regional strategic targets.
- **Credential and data access** through persistent RAT deployment and follow-on remote access.
- **Regional targeting** with localized lures and infrastructure choices that blend into the victim environment.

## Naming and attribution
- Seqrite treats SideCopy as a cluster operating under the broader Transparent Tribe / APT36 umbrella.
- Keep `SideCopy` as the page title because it is the named cluster used in current Seqrite reporting and in multiple public campaign writeups.
- Attribute confidence levels to the source. For Operation XENOFISCAL, Seqrite says the overlap is medium-to-high confidence rather than a legal or government attribution.

## Core tradecraft
- Spear-phishing archives containing document-disguised `.lnk` files.
- Windows living-off-the-land execution through `mshta.exe` to fetch remote HTA or script payloads.
- Obfuscated JavaScript / HTA stages that decode payloads in memory and use ActiveX / .NET components.
- Persistence through `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` keys or scheduled tasks, often with names that imitate legitimate Microsoft or browser components.
- Commodity and open-source RAT adoption; Seqrite specifically notes SideCopy use of customized **XenoRAT** variants after earlier AsyncRAT-style adoption.
- Infrastructure choices that separate delivery staging from final RAT command and control and sometimes blend delivery domains into regional or government-adjacent hosting.

## 2026 activity
### <a id="sep22-trellix-academia"></a>September 2026: pivot to Indian academia — ReverseRAT via mshta chain (Trellix, via The Hacker News Sep 22)
Trellix researchers (Boggavarapu R S S Srinivas Gupta, Ravishankar N C) report SideCopy spear-phishing **academic institutions in India** — an explicit expansion beyond the group's historical Indian government/defense focus. Trellix's read: the pivot "highlights an expanding set of strategic priorities." Chain (full text captured by this wiki from The Hacker News, Sep 22, 2026):

- Weaponized ZIP → LNK with spoofed PDF icon and double extension **`commskll.docx.lnk`** → fetches an obfuscated HTA from **`docsportal[.]in`**, executed via **`mshta.exe`**, reflectively loads a DLL; the HTA **self-deletes after the next stage initializes** (anti-forensic).
- The DLL is a dropper for three embedded components: `appT.bat` (Registry Run key → launches `startT.hta` via mshta with no user interaction), `startT.hta` (multi-stage deobfuscation reconstructing a **two-part XAML payload in memory** → reflective load of `ioluegnt.dll` → Base64 → **.NET deserialization** into volatile memory, nothing written to disk), and `commskl.docx` (decoy document).
- Final payload is **ReverseRAT** — SideCopy's in-house RAT, in use **since early 2021**: system metadata, installed software, screenshots, passwords, clipboard, file operations, command execution, Registry persistence, file upload, interactive shell.
- C2 tradecraft: traffic encrypted with **hard-coded key `NMXIKS09?:709,!~lnsYUS`**; exfiltration over **port 5863** to **`dns.educationportals[.]biz`** → **`45.61.157[.]22`**.

Liveness at this wiki's Sep 22 check: `docsportal[.]in` and `dns.educationportals.biz` both **no longer resolve** (delivery and exfil domains already burned by reporting time); `45.61.157[.]22:5863` does not answer (timeout). Consistent with a campaign already rotated after disclosure — the durable IoCs are the RAT key, port, filenames and chain shape, not the domains. Alias note: TAG-140 (Google) is the same cluster; Trellix again notes overlap with the Transparent Tribe cluster — see also this wiki's [Operation RapidRust page](../ops/transparent-tribe-operation-rapidrust-rustyshade-private-github-c2-usb-propagation-zscaler-september-2026.md) for the same umbrella's September tooling shift. Open items: Trellix canonical URL (trellix.com unreachable from this wiki at capture — backfill), hashes, named academic victims, whether ReverseRAT C2 rotates to new infrastructure.

### Operation XENOFISCAL
Seqrite's June 2026 report describes a SideCopy-attributed campaign against Afghanistan's Ministry of Finance provincial officials. The chain used a Pashto `.pdf.lnk` lure, `mshta.exe`, an HTA / JavaScript loader, .NET deserialization, staged DLL loaders, Donut-style shellcode, and XenoRAT 1.8.7 communicating with `185.235.137.106`.

See [Operation XENOFISCAL SideCopy XenoRAT campaign](../ops/operation-xenofiscal-sidecopy-xenorat.md).

## Defender signals
- Archive-delivered Pashto, Dari, Hindi, Urdu, or regionally tailored `.pdf.lnk` lures that execute `mshta.exe` instead of opening a document.
- `mshta.exe` or Windows Script Host activity reaching unexpected government, education, or regional infrastructure immediately after shortcut execution.
- HTA or JavaScript stages using ActiveX, custom Base64 routines, `.NET` COM objects, `BinaryFormatter.Deserialize`, or `COMPLUS_Version` forcing.
- User-writable staging directories under `C:\Users\Public\` with Microsoft- or browser-like names such as `USOShared-*` or Firefox/Edge typosquats.
- Run-key values or scheduled tasks that launch HTA files, `cmd /C start`, or RAT executables at logon.
- XenoRAT or XenoRAT-like TCP C2 with AES-encrypted traffic, mutex use, scheduled-task / Run-key persistence, and dynamic plugin loading.

## Related pages
- [Operation XENOFISCAL SideCopy XenoRAT campaign](../ops/operation-xenofiscal-sidecopy-xenorat.md)
- [Operation Dragon Weave Azure Blob C2 campaign](../ops/operation-dragon-weave-azure-blob-c2.md)

## Sources
- Seqrite: [https://www.seqrite.com/blog/operation-xenofiscal-sidecopy-deploying-persistent-xenorat-targeting-the-mof-afghanistan/](https://www.seqrite.com/blog/operation-xenofiscal-sidecopy-deploying-persistent-xenorat-targeting-the-mof-afghanistan/)
- The Hacker News summary: [https://thehackernews.com/2026/06/pakistan-linked-sidecopy-targets.html](https://thehackernews.com/2026/06/pakistan-linked-sidecopy-targets.html)
- Trellix report via The Hacker News (Sep 22, 2026, full text captured by this wiki): [https://thehackernews.com/2026/09/sidecopy-broadens-india-targeting-to.html](https://thehackernews.com/2026/09/sidecopy-broadens-india-targeting-to.html) — Trellix canonical URL pending backfill (trellix.com unreachable from this wiki at capture time)
