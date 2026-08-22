# UAT-10147: SPECTRE, BadIIS, and agentic-AI-augmented web-server intrusions

## Summary
Cisco Talos' paired August 20, 2026 reports document **UAT-10147**, a financially motivated, Chinese-speaking intrusion actor that targets internet-exposed **Windows and Linux web servers** (IIS and Nginx/Apache-style) worldwide and monetizes them through **SEO fraud** (the **BadIIS** malware-as-a-service and a C# ASHX SEO engine) and **data theft**. The reports add two durable, high-signal findings: (1) a new cross-platform C backdoor **[SPECTRE](../tools/spectre-cross-platform-backdoor-specter-rootkit.md)** with a **Specter** Linux kernel rootkit and a BYOVD EDR-killer on Windows, and (2) evidence that the actor has **integrated agentic AI into post-compromise operations** — recovered AI-generated operational playbooks, exploit-automation scripts, and troubleshooting logic that support real-world intrusions (DeepAudit, PentestGPT, ysoserial ViewState tooling, and a documented ASP.NET ViewState RCE "guide" plus four companion Python scripts). Talos assesses with moderate-to-high confidence that UAT-10147 belongs to an emerging class of operators leveraging agentic AI to operationalize offensive tradecraft at scale.

## Tags
- ops
- UAT-10147
- Chinese-speaking
- web server
- IIS
- Linux
- SEO fraud
- BadIIS
- ASHX
- web shell
- SPECTRE
- Specter
- agentic AI
- AI-assisted exploit
- Metasploit
- ysoserial
- ViewState
- Nacos
- Zimbra
- Telerik
- local privilege escalation
- Dirty Pipe
- Baron Samedit
- credential theft
- cybercrime

## Campaign overview
- **Victimology:** affected servers in Brazil, Bolivia, China, Canada, and Vietnam; sectors span government, education, media, technology, and gaming. The actor's C2 open directory exposed a target list of ~**170,000 URLs** split into 17 files of ~10,000 (the actor uses the letter "w" for 萬, 10,000).
- **Initial access:** public one-day and old RCEs against web servers, weaponized through the Metasploit Framework. Observed vulnerabilities: **CVE-2022-27925** (Zimbra unauthenticated RCE), **CVE-2021-23758** (AjaxPro deserialization RCE), **CVE-2021-29441** / **CVE-2021-29442** (Nacos `ScriptEngineFactory` SPI arbitrary code execution — used with an **asynchronous exfiltration sink** that POSTs `id`/`hostname` or `%USERNAME%`/`%COMPUTERNAME%` to the attacker's own Nacos config server instead of a persistent reverse shell), and **CVE-2019-18935** (Telerik UI for ASP.NET AJAX .NET JSON deserialization; dropped reverse-shell DLLs use randomized `[10 digits].[7 digits].dll` names).
- **Windows infection chain:** `back.txt` / `back.bat` deploy EfsPotato (renamed `prcc1.rar`), a secondary `bai.bat`, and QuasarRAT (disguised as `svchosts.exe`); add IIS dirs to the Defender exclusion list via PowerShell/registry; `certutil` downloads BadIIS (`dll.zip`) and `user.bat` from `adminapi.tippusoni[.]in`; `appcmd list site /config /xml` for injection-target recon; `user.bat` creates a rogue local user in Administrators + Remote Desktop Users. `bai.txt` adds a scheduled task named "Google Chrome Start." Other implants observed in related campaigns: Gh0stCringe and SPECTRE.
- **Linux infection chain:** RCE → web shell → LPE via **CVE-2022-0995** (watch_queue), **CVE-2021-3156** (Baron Samedit), **CVE-2015-5287** (ABRT sosreport), **CVE-2015-3246** (libuser roothelper), **CVE-2010-3904** (RDS), and **CVE-2022-0847** (Dirty Pipe) → deploys Noodle RAT, SPECTRE, and Meterpreter.

## Agentic-AI integration (the durable finding)
- **Frameworks:** **DeepAudit** (source-code vuln scanning; assessed high-confidence as intended, possibly also used defensively) and **PentestGPT** (dynamic web scanning + PoC execution) observed on the actor's management/C2 server; **ysoserial** used to build Java-deserialization payloads.
- **AI-generated ASP.NET ViewState RCE guide** (the most significant recovered artifact): documents prerequisites (MachineKey via `badsecrets`), a low-noise **MachineKey validity check** (distinguishing HTTP 500 "MAC Validation Failure" vs. "InvalidCastException" — the latter means the key is valid), ysoserial `TypeConfuseDelegate` payload generation (noting .NET 4.8 does *not* patch these chains), a Python delivery script, an inverted success condition (HTTP 500 `InvalidCastException` = success), OOB-callback RCE confirmation (time-based blind testing is useless because `Process.Start()` is async), PowerShell-AMSIEvasion recon, and a "case record" logging a real intrusion. MachineKey scope is IIS-site level, so keys from one vhost do not apply to co-hosted sites — making MachineKey confidentiality the single most important defensive control.
- **Four companion AI-generated Python scripts:** `check_paths.py` (five OOB write-capability probes to a `webhook.site` endpoint, then polls the webhook API in-session), `deploy_implant.py` (downloads/launches SPECTRE via certutil with a `New-Object Net.WebClient` fallback), `deploy_shell.py` (drops an ASHX web shell `sss.ashx` via a temporary `up.ashx` upload relay, with a fallback staging server `139.180.197[.]150:54321`; the attacker's Windows username `dajiba`), and `exfil.py` (three UTF-16-LE-Base64 `powershell -nop -enc` recon stages: webroot enumeration, `appcmd list site` IIS inventory, `whoami /priv` privilege assessment).
- **Findings log:** >12 HTTP callbacks to the `webhook.site` listener confirmed RCE via ASP.NET ViewState on a target IIS server, executed four ysoserial gadget chains on .NET 4.8.4797.0, and exfiltrated host identity (13 webroot site directories), a `redirection.config` access-denial, and confirmed `SeImpersonatePrivilege` (a viable Potato-family LPE path).

## Infrastructure and pivots
- C2 / download server: `139.180.197[.]150` (open directory listing exposed the target list; secondary web-shell staging on port `54321`).
- BadIIS download host: `adminapi.tippusoni[.]in` (e.g. `/4/dll.zip`, `/4/user.txt`).
- ASHX SEO-engine C2 domains on the `vn[.]xyz` suffix (Vietnamese focus; targets the Cốc Cốc crawler).
- Exfiltration sink: `webhook.site` (OOB callbacks and recon harvest).
- Web-shell auth: `X-ID` HTTP header token `x9` (fallback `v` parameter); a deceptive 404 is returned when the token is absent.
- Scheduled-task persistence named "Google Chrome Start."

## Coverage
- **ClamAV:** `Py.Loader.Tool-10060293-1`, `Py.Loader.Tool-10060293-2`, `Win.Malware.Generic-10060228-0`, `Win.Loader.Downloader-10060287-1` (SPECTRE-specific signatures are listed on the [SPECTRE tools page](../tools/spectre-cross-platform-backdoor-specter-rootkit.md#detection)).
- **Snort SIDs:** Snort2 `1:66697`, `1:66696`; Snort3 `1:66697`, `1:66696`.
- **IOC files:** Cisco-Talos/IOCs `2026/08/UAT-10147 deploys SPECTRE.txt` and `2026/08/UAT-10147 integrates agentic AI.txt`.

## Defender priorities
- **Patch the web surface:** the campaign leans on one-day and legacy RCEs (Zimbra, Nacos, AjaxPro, Telerik). A current patch cycle plus removal of unused components (SNMP, Nacos ScriptEngine, Telerik handlers) is the highest-leverage control.
- **Protect the ASP.NET MachineKey:** the entire AI-driven ViewState chain is "entirely dependent on key material exposure." Audit IIS `machineKey` configuration, restrict who can read the config, and treat `badsecrets`-known keys as compromised. Hunt for the inverted 5xx-success signature: a 500 whose body contains `InvalidCastException` on `__VIEWSTATE` POST is an *exploit success*, not a routine error.
- **Hunt for OOB-callback and webhook exfiltration:** `webhook.site`-style sinks and Nacos-config-server exfil blend into legitimate SaaS/admin traffic; alert on IIS/app-pool processes making outbound HTTPS to unfamiliar webhooks and on Nacos config-server POSTs carrying `id`/`hostname`/`whoami` output.
- **Watch for the IIS-defense-evasion pattern:** adding `System32\inetsrv` / `SysWOW64\inetsrv` to the Defender exclusion list, rogue local-admin RDP users, and a scheduled task named "Google Chrome Start" are all concrete, alertable artifacts of this chain.
- **Treat AI-generated tooling as tradecraft, not a separate class:** the agent compresses development, content generation, recon, and validation timelines but still runs through the same execution primitives. Hunt the joined sequence (scan → PoC → OOB confirmation → implant deploy → LPE) rather than waiting for a novel signature. See [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md).

## Assessment limits
- Talos attributes SPECTRE / Specter and the campaign to UAT-10147; the "AI-assisted development" of Specter and the custom Potato tools is a **medium-confidence** assessment based on source-code artifacts, not confirmed operator statements.
- DeepAudit/PentestGPT presence supports intent (high confidence) but Talos did not directly observe exploitation of DeepAudit findings against victims.
- The recovered ViewState guide and scripts demonstrate capability and at least one logged intrusion; the ~170,000-URL target list and country distribution describe the actor's scoping, not a confirmed victim count.

## Related pages
- [SPECTRE / Specter tools](../tools/spectre-cross-platform-backdoor-specter-rootkit.md)
- [UAT-10147](../actors/uat-10147.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- Cisco Talos: [UAT-10147: Chinese-speaking adversary integrates agentic AI into post-compromise operations](https://blog.talosintelligence.com/uat-10147-chinese-speaking-adversary-integrates-agentic-ai-into-post-compromise-operations/) (Joey Chen, August 20, 2026)
- Cisco Talos: [UAT-10147 deploys SPECTRE: A cross-platform implant with Linux rootkit and BYOVD capabilities](https://blog.talosintelligence.com/uat-10147-deploys-spectre-a-cross-platform-implant-with-linux-rootkit-and-byovd-capabilities/) (Joey Chen, August 20, 2026)
