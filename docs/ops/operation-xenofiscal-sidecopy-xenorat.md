# Operation XENOFISCAL SideCopy XenoRAT campaign

## Summary
Seqrite reports **Operation XENOFISCAL**, a SideCopy-attributed spear-phishing campaign targeting Afghanistan's Ministry of Finance provincial finance network. The chain uses a Pashto-language `.pdf.lnk` lure, `mshta.exe` remote HTA execution, obfuscated JavaScript and .NET loaders, registry persistence, in-memory shellcode execution, and **XenoRAT 1.8.7** for persistent remote access.

Seqrite attributes the campaign to **SideCopy** with **medium-to-high confidence**, based on TTP overlap with prior SideCopy activity, SideCopy's documented XenoRAT adoption, registry-persistence style, and infrastructure overlap. Keep that confidence caveat with the source.

## Tags
- ops
- operations
- espionage
- SideCopy
- Pakistan-linked
- APT36
- Transparent Tribe
- Afghanistan
- Ministry of Finance
- spear phishing
- LNK
- HTA
- mshta
- JavaScript
- .NET
- BinaryFormatter
- XenoRAT
- registry persistence
- scheduled tasks

## Why this matters
- The lure is highly localized: a Pashto filename and decoy finance-ministry staff directory aimed at provincial finance officials across Afghanistan's Mustoufiats.
- The execution path is durable SideCopy tradecraft: archive-delivered `.lnk` → `mshta.exe` → remote HTA / script staging → loader DLLs → RAT.
- The campaign separates delivery and final C2 infrastructure, including delivery through a compromised Afghan education domain and XenoRAT C2 on European bulletproof hosting.
- XenoRAT gives the operator encrypted TCP C2, plugin loading, persistence management, and long-term remote access from a widely available open-source RAT base.

## Reported chain
- Initial delivery: a spear-phishing ZIP archive containing a malicious shortcut named in Pashto and disguised as a PDF: `د_هغو_کارکوونکو_لېست_چې_د_فکري_او_رواني_جګړې_سیمینار_ته_ورپېژندل_شوي_وو12.pdf.lnk`.
- Lure theme: a list of employees introduced to an "intellectual and psychological warfare seminar," tailored to Afghan government context.
- Targeting: Afghanistan Ministry of Finance, provincial revenue and finance directorates, and provincial-level finance employees rather than only central ministry staff.
- Decoy: an Afghan Ministry of Finance provincial staff directory covering all 34 provinces with finance directors, revenue chiefs, financial officers, secretaries, and direct mobile numbers in Dari and Pashto.
- Execution: the LNK launches `C:\Windows\System32\mshta.exe` and points to `hxxp[:]//abimj[.]edu[.]af/index.php`, a compromised Afghan education-domain delivery layer.
- HTA / JavaScript stage: the remote payload contains heavily obfuscated JavaScript, custom Base64 decoding, ActiveX execution paths, `.NET` COM object use, `System.IO.MemoryStream`, and `BinaryFormatter.Deserialize_2()` to execute an embedded .NET payload in memory.
- Runtime handling: the script checks for `.NET` runtime versions under `HKLM\SOFTWARE\Microsoft\.NETFramework\v4.0.30319`, falls back to `v2.0.50727`, and sets `COMPLUS_Version` to force the selected CLR runtime.

## Loader and persistence details
- Stage-1 loader: a .NET DLL that opens the decoy, executes commands through hidden `cmd.exe`, and stages follow-on files.
- Persistence staging path: `C:\Users\Public\USOShared-1de48789-1285\zuidrt.hta`.
- Run-key persistence: the loader writes a decoded command through a temporary `noway.bat` file to create `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Edgre`.
- Persisted command: `cmd /C start C:\Users\Public\USOShared-1de48789-1285\zuidrt.hta`.
- Secondary HTA: `zuidrt.hta` repeats obfuscated ActiveX / .NET deserialization-style staging and executes a stage-2 loader DLL.
- Stage-2 loader: a .NET shellcode loader that creates `C:\Users\Public\firefx-1de87eec8-1241`, downloads an encoded payload as `ayui.vmxx`, decodes and GZIP-decompresses it, writes an intermediate `ayhui.vmxx`, allocates RWX memory with `VirtualAlloc`, copies shellcode with `Marshal.Copy`, and starts execution with `CreateThread`.
- Shellcode: Seqrite describes Donut-style behavior, including CLR initialization, reflective managed assembly loading, and possible AMSI patching through functions such as `AmsiScanBuffer()`.

## XenoRAT payload details
- Final payload: **XenoRAT 1.8.7**, an open-source remote access trojan.
- Reported C2: `185.235.137.106`.
- Mutex: `clouda`.
- C2 behavior: encrypted TCP-based communication with an authentication handshake, AES encryption, and Windows native RTL compression / decompression for payload data.
- Plugin execution: the RAT can receive DLL modules, load assemblies dynamically with `Assembly.Load`, instantiate attacker-specified classes, and invoke their `Run` methods.
- Persistence options:
  - admin context: scheduled task named `XenoUpdateManager` registered with `schtasks.exe` and highest available privileges;
  - non-admin context: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` startup entry.
- Cleanup: XenoRAT includes functions to remove scheduled-task and Run-key persistence before self-termination.

## Infrastructure notes
- Delivery domain: `abimj[.]edu[.]af`, resolving during Seqrite's analysis to `103.132.98.224` and `103.132.98.226` in `103.132.98.0/23` / `AS58469`, attributed to Afghanistan's Ministry of Communication and Information Technology.
- Seqrite says passive DNS showed more than 200 legitimate Afghan government and education domains co-hosted in the same block, helping malicious delivery blend with local sovereign infrastructure.
- RAT C2: `185.235.137.106`, hosted on `AS59711` / HZ Hosting Ltd with Frankfurt presence; Seqrite notes this provider had appeared in prior SideCopy infrastructure clusters.
- Seqrite observed three domain clusters resolving to the RAT C2, including `.xyz`, `.live`, and `.online` throwaway domains and a mail-infrastructure domain, suggesting combined RAT and phishing infrastructure use.

## Defender notes
- Hunt for `.lnk` files masquerading as PDFs and spawning `mshta.exe`, especially from archives and with Pashto / Dari government-context filenames.
- Alert on `mshta.exe` fetching HTA or PHP resources from government or education domains immediately after shortcut execution.
- Review HTA / JavaScript telemetry for ActiveX, custom Base64 routines, `.NET` COM object creation, `BinaryFormatter.Deserialize`, `COMPLUS_Version`, and hidden `cmd.exe` child processes.
- Monitor `C:\Users\Public\USOShared-*`, `C:\Users\Public\firefx-*`, `zuidrt.hta`, `noway.bat`, `ayui.vmxx`, and `ayhui.vmxx` creation.
- Detect Run-key values that launch HTA payloads through `cmd /C start`, especially typo-like names such as `Edgre`.
- Detect scheduled tasks named `XenoUpdateManager` and unexpected XenoRAT-like startup entries.
- Treat outbound traffic to `185.235.137.106` as high priority in environments that may overlap Afghan government, finance, or South Asia-focused targets.
- Favor behavior-based detections over only IOCs: this chain's staging domains and file names can rotate while the LNK → mshta → HTA → .NET loader → RAT sequence remains reusable.

## Related pages
- [SideCopy](../actors/sidecopy.md)
- [Operation Dragon Weave Azure Blob C2 campaign](operation-dragon-weave-azure-blob-c2.md)

## Sources
- Seqrite: https://www.seqrite.com/blog/operation-xenofiscal-sidecopy-deploying-persistent-xenorat-targeting-the-mof-afghanistan/
- The Hacker News summary: https://thehackernews.com/2026/06/pakistan-linked-sidecopy-targets.html
