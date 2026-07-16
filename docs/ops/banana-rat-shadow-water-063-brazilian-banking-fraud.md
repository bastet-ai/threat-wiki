# Banana RAT / SHADOW-WATER-063 Brazilian banking fraud

## Summary
Trend Micro's TrendAI MDR team reported Banana RAT, a PowerShell-based banking remote-access trojan operated by the activity cluster it tracks as **SHADOW-WATER-063**. The investigation reconstructed both the attacker-side build infrastructure and victim-side payload chain from server artifacts recovered between April 17 and April 22, 2026 and endpoint telemetry from a live Brazilian banking-trojan operation.

The campaign is financially motivated and focused on Brazilian financial institutions and Brazilian-localized cryptocurrency exchanges. Trend Micro assessed moderate-confidence Brazilian Portuguese operator indicators and described Banana RAT as adjacent to the broader Tetrade banking-trojan ecosystem rather than a confirmed Grandoreiro, Mekotio, Casbaneiro, Guildma, or CHAVECLOAK family member.

## Tags
- ops
- operations
- Banana RAT
- SHADOW-WATER-063
- Brazilian banking malware
- banking trojan
- PowerShell malware
- FastAPI
- polymorphic payloads
- fileless execution
- scheduled task persistence
- Pix
- QR code interception
- Tetrade
- Grandoreiro
- Mekotio
- Casbaneiro
- Guildma
- CHAVECLOAK
- financial fraud
- Brazil

## Why this matters
- The actor controls both a server-side polymorphic build system and a victim-side fraud module, giving defenders rare end-to-end pivots across delivery, payload generation, C2, persistence, and operator tooling.
- Payloads are generated as one-time, hash-unique PowerShell builds through a FastAPI crypter pool, weakening file-hash-only detection and increasing the value of behavioral and infrastructure detections.
- The malware is purpose-built for interactive banking fraud: screen streaming, low-level input control, keylogging, bank-branded full-screen overlays, and Pix QR-code interception let operators manipulate live transactions while hiding activity from the victim.
- Brazilian finance and crypto organizations should treat this as a fraud-execution platform, not generic commodity RAT noise.

## Reported chain
1. Victims are lured through WhatsApp or a possible phishing URL to download `Consultar_NF-e.bat` from `convitemundial2026[.]com`, using Brazil's electronic-invoice context as the lure.
2. The batch file launches an obfuscated PowerShell command that hides the console and retrieves a staging payload such as `payload.php` / `msedge.txt` from attacker infrastructure.
3. The operator-side service maintains a clean PowerShell banker source and uses a FastAPI-based crypter to generate 100–200 ready builds per pool. Each request receives a byte-unique payload with randomized variables, junk code, XOR keys, fragmented .NET type names, and AES-wrapped code blobs.
4. The victim-side stager writes a staged file under user-writable paths such as `C:\Users\Public\Documents\msedge.txt`, decrypts the AES-wrapped body in memory, and executes it through `ScriptBlock::Create` / `IEX` so the plaintext banker does not land on disk.
5. The unpacked PowerShell RAT compiles temporary C# helpers through `csc.exe` for screen capture, overlays, keyboard tracking, native input control, process / credential-access support, and C2 modules.
6. The malware establishes persistence through a hidden scheduled task that runs `powershell.exe` with `-WindowStyle Hidden`, `-ExecutionPolicy Bypass`, and an encoded command every minute for 9,999 days.
7. The client communicates with C2 over TCP/443 using a custom binary protocol with AES-256-CBC encryption and an HMAC-SHA256 token derived from machine GUID and MAC address.

## Capabilities
- Remote screen capture / streaming through Windows GDI calls.
- Operator-driven mouse and keyboard input, including temporary `BlockInput` use to retain control.
- Continuous keylogging through direct low-level key-state checks.
- Clipboard manipulation and banking-session fraud support.
- Full-screen overlays that imitate Windows update / repair states or bank-specific security-update workflows.
- Pix QR-code detection, decoding, replacement, and overlay control using QR-focused C2 opcodes.
- SYSTEM-token abuse paths when running from Session 0.
- File and state hiding in Microsoft-looking paths such as `C:\ProgramData\Microsoft\Diagnosis\ETW\` or `AppData\Roaming\Microsoft\Diagnosis\ETW\`.

## Public indicators and pivots
Trend Micro published additional hashes and tables. High-signal pivots from the public report include:

- Lure / staging filename: `Consultar_NF-e.bat`.
- Staged payload names and components: `msedge.txt`, `msedgeupdate.txt`, `payload.php`, `st.txt`, `st.php`, `servidor_completo_pool.py`, `monitor_pool.py`, `instalar_completo_pool.sh`, `stats-view.php`, `stats-reset.php`, and `monitor.txt`.
- Delivery / staging infrastructure: `convitemundial2026[.]com`, `24.199.90[.]58`, and `24.199.90[.]58:80`.
- C2 infrastructure: `c[.]windowsk-cdn[.]com` over TCP/443 and fallback `162.141.111[.]227`.
- Internal project strings: `Projeto Banana`, `# PROTECTED SCRIPT v4.0 - Projeto Banana (MSEDGE EDITION)`, `SMART_V27_ULTRA`, and `BUILD_V6_HARDCODED_TYPES`.
- Static cryptographic pivot reported by Trend Micro: `iuhbdaubdvauygd5562$3@##$r`.
- Detection names in Trend Micro telemetry: `Backdoor.PS1.BANANARAT.A` and `Trojan.PS1.BANANARAT.A`.

## Defender heuristics
- Hunt for `Consultar_NF-e.bat` or invoice-themed batch files spawning hidden PowerShell from Downloads, WhatsApp, browser, or Explorer contexts.
- Alert on PowerShell download cradles retrieving `.php` or `.txt` payloads from recently registered or campaign-specific domains, followed by `IEX`, `ScriptBlock::Create`, AES decoding, or writes to `C:\Users\Public\Documents\`.
- Monitor PowerShell-driven `csc.exe` execution from .NET Framework directories compiling temporary `.cs` files into DLLs under user Temp paths.
- Review hidden scheduled tasks that execute `powershell.exe` every minute with encoded commands, hidden windows, execution-policy bypass, or very long repetition windows.
- Hunt for PowerShell or script-created files under Microsoft-looking ETW / Diagnosis paths, especially `msedge.txt` or `msedgeupdate.txt` in user-writable locations.
- For Brazilian finance environments, correlate endpoint overlay / screen-capture behavior with Pix transactions, QR-code rendering, and unusual browser window-title monitoring.
- Treat C2 disruption and host containment as separate workstreams: blocking delivery endpoints stops new infections, while already-compromised hosts need C2 hunting, credential/session review, and fraud-response coordination.

## Attribution notes
- Trend Micro tracks the activity as **SHADOW-WATER-063** while attribution remains under monitoring.
- Operator-language artifacts, filenames, comments, log strings, Brazilian banking terminology, Pix-specific functionality, and a hardcoded target list of Brazilian banks / localized exchanges support a Brazilian Portuguese operator hypothesis.
- Trend Micro described overlap with the Tetrade banking-trojan ecosystem, but architectural differences are material: Banana RAT uses a PowerShell client and Python / FastAPI polymorphism infrastructure rather than the Delphi monolithic style associated with canonical Grandoreiro.
- The report explicitly leaves open whether Banana RAT is an adjacent cluster, fork, or independent operator borrowing regional banking-trojan tradecraft.

## Related pages
- [WhatsApp VBScript ManageEngine RMM campaign](whatsapp-vbscript-manageengine-rmm-campaign.md)
- [Grandoreiro and BTMOB Latin America / Europe malware campaigns](grandoreiro-btmob-latam-europe-malware-campaigns.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Trend Micro: [https://www.trendmicro.com/en_us/research/26/e/banana-rat.html](https://www.trendmicro.com/en_us/research/26/e/banana-rat.html)
