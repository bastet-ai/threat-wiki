# Cavern

## Summary
**Cavern** is a modular .NET command-and-control and post-exploitation framework documented by Check Point Research in July 2026 and attributed to the Iran-linked **Cavern Manticore** cluster. CPR observed it in Israeli government and IT-provider intrusions after abuse of existing RMM tooling and WinDirStat DLL sideloading.

Cavern matters because its evasion is architectural rather than packer-driven: modules are split across .NET Framework IL-only assemblies, a C++/CLI mixed-mode agent, and .NET 8 NativeAOT native-only modules. That forces analysts to use multiple reversing workflows while the agent isolates managed modules in temporary AppDomains and unloads them after execution.

## Tags
- tools
- malware
- C2 framework
- post-exploitation framework
- Cavern
- Cav3rn
- Cavern Manticore
- Iran
- MOIS
- .NET malware
- C++/CLI
- NativeAOT
- DLL sideloading
- WinDirStat
- WebSocket C2
- SOCKS5
- DPAPI
- LDAP
- Active Directory
- SMB brute force
- RMM abuse

## Execution chain
CPR describes the recovered chain as:

1. Operators abuse existing RMM software in the target environment.
2. RMM deploys a WinDirStat sideloading package to `C:\ProgramData\WinDir\WinDirStat.exe`.
3. The legitimate WinDirStat binary loads a malicious `uxtheme.dll`.
4. `uxtheme.dll` acts as the Cavern agent and loads the communication module `n-HTCommp.dll`.
5. The agent polls C2 and pulls post-exploitation modules on operator command.

The Cavern agent is a 64-bit mixed-mode C++/CLI DLL that mimics the Windows theming library with 83 exports. CPR says 82 exports are inert stubs; the real execution path is `EnableThemeDialogTexture` at export ordinal 20 (`0x14`), creating a sandbox trap for tools that invoke default or low ordinal exports only.

## Component map
| Component | File name | Format | Role |
| --- | --- | --- | --- |
| Cavern agent | `uxtheme.dll` | Mixed-Mode C++/CLI / .NET 4.7.2 | Core backdoor and module orchestrator |
| Communication module | `n-HTCommp.dll` | .NET 8 NativeAOT | HTTPS / WebSocket transport, XOR traffic layer |
| File manager | `mhm.dll` | .NET Framework 4.7.2 | Host info, file operations, archive handling, DPAPI decrypt |
| SQL browser | `db.dll` | .NET Framework 4.7.2 | SQL enumeration, query, export, and manipulation |
| LDAP module | `ode.dll` | .NET Framework 4.7.2 | AD recon, LDAP search, user/group enumeration, brute forcing |
| Network module | `n-ten.dll` | .NET 8 NativeAOT | Network recon, port scanning, share enumeration, SMB brute force |
| Tunnel module | `n-sws.dll` | .NET 8 NativeAOT | SOCKS5 proxy and WebSocket / WSS tunneling |

## Anti-analysis architecture
Cavern does not depend on classic packing or string encryption across the framework. Instead, it raises analysis cost through format diversity and lifecycle control:

- **IL-only .NET Framework modules** keep readable metadata and command enums but must be interpreted in the context of the agent's loader and shared command grammar.
- **Mixed-mode C++/CLI agent builds** combine managed logic with native export stubs, requiring both .NET decompilation and native disassembly.
- **NativeAOT modules** statically compile .NET runtime code into native PEs, hide many security-relevant P/Invoke calls from import-table triage, and materialize string data only after runtime hydration or metadata reconstruction.
- **Per-execution AppDomain isolation** loads managed modules into temporary AppDomains, invokes them through a `MarshalByRefObject` proxy, and unloads the entire domain after execution.
- **Startup cleanup** in newer builds removes prior modules from the working directory, leaving primarily `n-HTCommp.dll`, `config.txt`, and logs.

## Agent behavior
- Creates Cavern mutexes such as `MYMUTEX123HELLP02` or `MYMUTEX123HELLP04`.
- Reads local configuration from `config.txt` in newer builds; older builds used a plain ID in `id.txt`.
- Uses custom delimiters: `_;;_` between fields and `_,_` between arguments.
- Dispatches modules based on filename convention: names starting with `n-` use the native `LoadLibraryA` / `GetProcAddress` path; others are treated as managed assemblies and loaded through AppDomain isolation.
- Calls a common module entry point named `get_version`.
- Implements self-commands for polling interval changes, Base64+GZip module update, debug toggling, WebSocket activation, WebSocket close, and WebSocket reconnect.
- Supports hot-swapping the agent itself by writing a new numbered `uxtheme.dll`, loading it, calling `EnableThemeDialogTexture` with `signalCode=200`, and terminating the old instance.

## C2 transport
The communication module `n-HTCommp.dll` is a .NET 8 NativeAOT DLL exposing `get_version` as a multi-verb HTTP / WebSocket dispatcher.

Reported transport traits:

- HTTP C2 polling uses `GET <c2>/profile`.
- HTTP result submission uses `POST <c2>/gallery` with `text/plain` content.
- C2-bound HTTP traffic applies XOR key `0x48` and Base64 encoding.
- WebSocket mode connects to `/socket`, sends the agent ID with a `00` suffix in the first frame, and uses XOR without Base64 for message bodies.
- HTTP requests use a fixed Microsoft Edge User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0`.
- C2-bound HTTP verbs attach an `X-User-token` header containing the agent ID plus `00`.
- Operator-driven `cget`, `cpost`, and `upload` verbs can fetch, post to, or upload files to arbitrary URLs outside the Cavern C2 path.

### HOLLOWGRAPH Microsoft 365 calendar transport
Group-IB documented [HOLLOWGRAPH](hollowgraph.md) on July 20, 2026 and links it to the Cavern framework with high confidence. The NativeAOT DLL preserves Cavern's `_;;_` / `_,_` command grammar and observed `003` debug self-command, but replaces the framework's direct HTTP / WebSocket path with application-only Microsoft Graph access to a compromised mailbox calendar.

HOLLOWGRAPH retrieves encrypted tasking from `Event ID: <taskID>` events dated May 13, 2050 and exfiltrates encrypted files as `File{n}.txt` attachments on events renamed to `Boss{...}ID{...}`. A secondary AAAA-record channel under `cloudlanecdn[.]com` refreshes tenant, client, secret, and mailbox configuration stored in `logAzure.txt`. Group-IB identified at least 12 infected systems and focused Israeli interest, but does not attribute this operation to Cavern Manticore; its separate Lyceum overlap assessment is low confidence.

## Post-exploitation capabilities
CPR recovered a shared command enum with 61 IDs. Confirmed capability areas include:

- host information and time/token collection;
- DPAPI decryption in the compromised user's context;
- file and directory listing, copy, move, delete, search, archive, upload, and download operations;
- SQL Server database browsing, query, export, and manipulation with operator-supplied credentials;
- LDAP / Active Directory bind tests, paged searches, user and group enumeration, user-property lookup, and LDAP brute-force support;
- DNS resolution, interface and IP configuration enumeration, ping, netstat-style connection listing, ARP table collection, domain/workstation discovery, domain computer enumeration, share listing, and TCP port scanning;
- SMB credential-spraying through `WNetAddConnection2` against target shares;
- SOCKS5 proxying and WebSocket / WSS tunneling in client or server mode.

CPR also notes that some process, registry, and service command ranges were present in the shared enum but not implemented in the recovered modular samples, suggesting missing or not-delivered modules. Older non-modular `Cav3rn` samples contained related `ApiEx.*` capabilities in a single .NET DLL and used a separate HTTP companion module with steganographic command/result files.

## Indicators and pivots
Selected pivots from CPR:

- `C:\ProgramData\WinDir\WinDirStat.exe`
- `C:\ProgramData\WinDir\uxtheme.dll`
- `n-HTCommp.dll`
- `mhm.dll`
- `db.dll`
- `ode.dll`
- `n-ten.dll`
- `n-sws.dll`
- `config.txt`
- `id.txt`
- Mutexes: `MYMUTEX123HELLP`, `MYMUTEX123HELLP02`, `MYMUTEX123HELLP04`
- PDB path fragment: `C:\Users\rick\Desktop\Modules\cavern\`
- C2 domains: `auth[.]hospitalinstallation[.]com`, `google[.]com[.]hospitalinstallation[.]com`, `hospitalinstallation[.]com`
- Older Cav3rn domains / paths: `adserviceupdate[.]com`, `hygienehistory[.]com`, `cac.aspx`, `.CvnC.png`, `.CvnA.png`, `.CvnR.png`, `Cvn.cfg`
- Fixed C2 User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0`
- Header: `X-User-token: <agent_id>00`

Selected hashes surfaced in CPR's article text:

- `37e123bd7998af4eae32718ce254776f36365a80ba56952593dab46f536d4066`
- `92cae0ad7f98f51a14bcc0ee05e372ebdc29ea96ea7bd161bd3f55198767603b`
- `5dc08bda6919a57a85e5f38b857985fa71529ca39c8299868d5a49a987e19b18`
- `a4aa217def4c38f4ecacdf47b1cd687f60cc74c18ab75195be3c4357a790bf41`
- `b630c96d3763182533d4fb9b614134382bd644cb02c6c1c3ade848b6ecc31e86`
- `8e9425c0b46eeb516610ae913d13f2b3f44a023043cb099277031d4ec38a6134`
- `0a3663648a46771a5a5423ad01e91a4e7ba825595e99fa934cb35cbb4848adc8`
- `5394d3b220de4695f731647e3a70545f951a8912ceb0c6585efab8d6842e8b42`
- `30cb4679c4b8599eeb3d63a551716475c6332bdc4d4b4e3de0964aadb3092a10`
- `2cb1ad3b22db8e3666ea138fee88034a87a87cf43db3d3265a675ebf221379b0`
- `7d586fb7f94182a8e2a0e53c7e4deb898066da029da5cd9972a94a59ca6d255a`
- `541b1f417b9e42078c3355693a8a492b6a76048850f6549a429e0be99e6819cb`
- `cbc9485db715e1b8cc384fe94b4cceadca4006cda8a5e28adc8848529cfafc93`
- `ccf218189c3aadb1c761da14bfda3bae686769031e1e1b10007648bd72e34748`

## Defender notes
- Build detections around the full chain: RMM deployment, non-standard WinDirStat path, sideloaded `uxtheme.dll`, Cavern mutexes, `config.txt`, and C2 headers.
- Do not rely on import-table or strings triage for NativeAOT modules; prioritize behavior, module names, working directory, memory, and network telemetry.
- Flag `WinDirStat.exe` loading `uxtheme.dll` from `C:\ProgramData\WinDir\` or other non-application directories.
- Hunt for Microsoft Edge UA strings that do not match the installed browser version or process lineage, especially when paired with `/profile`, `/gallery`, `/socket`, and `X-User-token` headers.
- Watch for .NET processes that create and unload AppDomains around byte-loaded assemblies, then delete module DLLs from the working directory.
- Treat DPAPI decrypt, SQL credentialed access, LDAP brute-force, SMB share brute-force, and SOCKS5 tunnel activity as signs of post-compromise expansion rather than first-stage infection.
- Preserve RMM audit logs, dropped DLLs, `config.txt`, logs, proxy records, memory captures, and EDR module-load telemetry before eradication.

## Related pages
- [HOLLOWGRAPH](hollowgraph.md)
- [Cavern Manticore](../actors/cavern-manticore.md)
- [Seedworm / MuddyWater](../actors/seedworm-muddywater.md)
- [ROADtools](roadtools.md)

## Sources
- Group-IB: [https://www.group-ib.com/blog/hollowgraph-microsoft-365/](https://www.group-ib.com/blog/hollowgraph-microsoft-365/)
- Check Point Research: [https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/](https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/)
- The Hacker News: [https://thehackernews.com/2026/07/iran-linked-hackers-use-new-cavern-c2.html](https://thehackernews.com/2026/07/iran-linked-hackers-use-new-cavern-c2.html)
