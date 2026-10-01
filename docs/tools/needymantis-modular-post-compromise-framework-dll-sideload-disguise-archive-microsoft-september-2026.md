# NeedyMantis: a modular post-compromise malware family built from loaders, a custom encrypted archive format, a custom executable format, and DLL-sideloaded disguise packages — found while pivoting off the DAEMON Tools compromise (Microsoft, Sep 28, 2026)

## Tags
- tools
- NeedyMantis
- Storm-3069
- DAEMON Tools
- post-compromise
- DLL sideloading
- custom archive format
- Poedit
- WinSparkle.dll
- libcurl.dll
- vim64.dll
- dbghelp.dll
- jli.dll
- nvml.dll
- obfuscated stack strings
- ThreadHideFromDebugger
- ProcessDebugFlags
- encryptbase64.ps1
- dnsapi.dll
- ws2_32.dll
- msvcrt140.dll
- 7-Zip
- Disk2vhd
- Impacket
- China-aligned
- telecommunication targeting
- Microsoft Defender

## Summary

Microsoft Threat Intelligence identified **NeedyMantis**, a modular post-compromise malware family observed in a limited number of **targeted** operations against telecommunications organizations, universities, medical nonprofits, intergovernmental organizations, and government contractors. Activity dates back to **at least October 2025** and was discovered by pivoting from indicators in Kaspersky's **DAEMON Tools supply-chain compromise** investigation. Known user: **Storm-3069** (Microsoft's designator for the DAEMON Tools-associated activity); additional NeedyMantis activity beyond Storm-3069 indicates the malware may serve more than one operator. Microsoft assesses **origin from China** (targeting aligned with Chinese interests, selective deployment) but has NOT attributed it to a named Chinese nation-state actor, nor confirmed single-operator ownership.

The deployment model is the durable finding: **NeedyMantis arrives after access exists** — it is a long-term-access maintenance toolkit, not an initial-access malware. In one incident an operator used **Impacket** to copy the legitimate software + malicious DLL + archive from a network share onto a target device, hands-on-keyboard.

## Packaging

First-stage loader masquerades as a required DLL, **DLL-sideloaded by packaging alongside legitimate open-source software**: Poedit (translation), curl, Vim, TightVNC; also masquerading as Microsoft Office / Broadcom / Intel / NVIDIA components. Observed paths include:
- `%ProgramFiles%\Poedit\WinSparkle.dll` (spoofing Poedit's WinSparkle update component)
- `%ProgramData%\USOShared\libcurl.dll`
- `%ProgramData%\VIM\vim64.dll`, `%ProgramData%\TightVNC\VIM\vim64.dll`
- `%ProgramData%\office\dbghelp.dll`, `%ProgramData%\broadcom\dbghelp.dll`
- `%ProgramData%\Intel\jli.dll`
- `%ProgramFiles%\modifiable\nvml.dll`, `%ProgramData%\ics\nvml.dll`

The **archive file shares the DLL's basename** (e.g., `WinSparkle.dll` + `WinSparkle`) — a cheap, universal hunt rule: a DLL-adjacent extensionless file of similar entropy in a third-party app directory.

## Architecture

- **Stage 1 loader** (analyzed sample: `WinSparkle.dll`, SHA-256 `e842dd7642c8e04b5ec20b6393848a9c904e4832930950c16664fe7800ba382e`; archive `WinSparkle`, SHA-256 `9cb68f986043a576e19d32184c583b7d8f571c7219d8dc0065dced1c13f077ef`): obfuscated stack-string rebuilding of DLL/API names and constants, resolved dynamically; anti-debug via `ProcessDebugFlags` + `ThreadHideFromDebugger`; sole job = extract stage 2 from the archive.
- **Custom encrypted archive format**: outer XOR-decode + `RtlDecompressBuffer`; per-entry XOR-decoded filenames + individually decompressed contents; **offsets, XOR keys and values vary per sample** — format-per-sample defeats static archive carve-outs; the unpacking-tool metadata (Microsoft published one) is the reproducible artifact.
- **Archive contents** (11 files in the analyzed sample): legitimate 7-Zip components (`7-zip.dll`, `7z.exe`, `.chm`), legitimate Sysinternals `Disk2vhd` DLLs, a legitimate-looking `kernel32.dll` — beside the real kit: **`encryptbase64.ps1`** (stage-2 loader), **`dnsapi.dll`** (NOT dnsapi — configuration), **`ws2_32.dll`** (NOT ws2_32 — WebSockets C2 communications DLL), **`msvcrt140.dll`** (NOT msvcrt140 — shellcode to load module DLLs and resolve exports). **A fake system DLL living OUTSIDE System32 next to a real-software directory is the class tell.**
- **Modular design**: operators extend functionality with additional modules; C++ + x64 shellcode; custom executable file format for modules.
- **C2**: WebSockets-based (the fake `ws2_32.dll`).

## Defender actions

1. Hunt the disguise-path list above + any DLL-adjacent same-basename extensionless file under `%ProgramData%` / `%ProgramFiles%\modifiable` in third-party app directories; `encryptbase64.ps1` filenames; process trees where Poedit/curl/Vim/TightVNC load `WinSparkle.dll`/`libcurl.dll`/`vim64.dll` from unexpected paths; unsigned `dbghelp.dll`/`jli.dll`/`nvml.dll` outside their vendors' signed lineage.
2. Treat any sighting as **post-compromise**: pivot backwards (the initial-access hunt is the incident's real subject), and treat the host as long-term-accessed — credential and token rotation, not just file cleanup.
3. Microsoft ships IOCs + Defender detections in the blog.

## Related pages
- [DAEMON Tools compromise context — on-wiki supply-chain operations index](../notes/source-index.md)
- [Spectre/BadIIS AI-augmented web-server campaign (comparable modular post-compromise tooling)](../ops/uat-10147-spectre-badiis-ai-augmented-web-server-campaign.md)

## Sources
- Microsoft Threat Intelligence: [https://www.microsoft.com/en-us/security/blog/2026/09/28/needymantis-unpacking-a-post-compromise-malware-family-used-in-targeted-operations/](https://www.microsoft.com/en-us/security/blog/2026/09/28/needymantis-unpacking-a-post-compromise-malware-family-used-in-targeted-operations/) (Sep 28, 2026; full text captured by this wiki via RSS `content:encoded`)
