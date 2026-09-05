# Impersonating IT support: Teams remote-session intrusion via MSI → portable Node.js → JavaScript implant → WinRM lateral movement (Microsoft, Sep 2, 2026)

## Tags
- ops
- social engineering
- vishing
- Microsoft Teams
- remote access
- RMM
- Quick Assist
- Windows Installer
- MSI
- Node.js
- JavaScript implant
- PowerShell
- WinRM
- lateral movement
- Active Directory
- screen capture
- Ethereum C2
- Microsoft Security Research
- enterprise intrusion

## Summary
On **September 2, 2026**, Microsoft Security Research (with Sagar Patil, Arlette Umuhire Sangwa, Jesse Birch, and Ravikant Tiwari) published "Impersonating IT support: how threat actors turn a remote session into enterprise-wide access." It describes a **human-operated** intrusion campaign that abuses **Microsoft Teams external collaboration** to impersonate IT/helpdesk staff, socially engineer a user into granting an **interactive remote session** (Quick Assist / third-party RMM), then — during that session — use **PowerShell to download and silently install a malicious MSI** that stages a **portable Node.js runtime** plus an **obfuscated, encrypted JavaScript implant**. After deployment the operator runs a full hands-on-keyboard (HOBK) playbook: host and Active Directory reconnaissance, periodic **desktop screen capture**, follow-on DLL payloads via `rundll32`, and **lateral movement over WinRM (TCP 5985)** toward domain controllers and certificate authorities.

This is a **full HOBK intrusion, not commodity infostealer phishing** — it relies on legitimate tooling at every stage (Teams, remote-support software, Windows Installer, a signed Node.js runtime, native admin protocols) so the activity blends into expected enterprise operations. Microsoft frames it as a user-initiated access pathway that can precede data theft, extortion, or ransomware.

## Why this matters
- It hands an external operator **credential-backed, interactive access** to internal infrastructure — far higher impact than an automated infostealer drop.
- The chain is **Teams-vishing → RMM/Quick Assist → MSI → Node.js JavaScript implant → WinRM pivot**, a repeatable, socially engineered pattern defenders should treat as a standing threat, not a one-off.
- The use of a **signed Node.js runtime** to execute attacker JavaScript (in-memory or a temp `.js`) defeats signature and publisher heuristics that key on unsigned executables or conventional script extensions — a live example of the "trusted interpreter as malware-delivery channel" pattern.
- The reconnaissance (display-adapter + antivirus enumeration), screen capture, and WinRM pivoting toward identity systems are the classic pre-conditions for ransomware or data exfiltration.

## Attack chain
1. **Initial access via Teams (T1566.003).** An actor in an **external tenant** chats/calls while impersonating internal IT or helpdesk, using lures like "Microsoft Security Update," "Spam Filter Update," or "Account Verification" to stop account deactivation. They talk the victim past Teams' external-tenant labeling, Accept/Block prompts, and message previews — sometimes layering **voice phishing (vishing)** so the malicious instructions never land in chat logs — and coaxed into approving a "request control" prompt or opening **Quick Assist** and reading back the connection code.
2. **Remote session + MSI delivery.** Once in control, the actor runs **PowerShell** inside the remote session to download a malicious MSI from attacker-controlled **cloud storage** and install it silently (`msiexec /qn`). The MSI is masqueraded with update/helpdesk-themed names such as **"devfix"** or **"Hotfix."**
3. **Node.js runtime + implant staging.** The MSI installs a **script-based loader** and a **separate encrypted implant file** under the user's `LocalAppData`. If Node.js is not present, the bootstrap downloads the **legitimate portable Node.js runtime** from the official distribution into a randomly named directory under `LocalAppData`. At runtime the loader decrypts the implant either **in memory** or into a temporary `.js` file.
4. **Script-based bootstrap.** A deferred, asynchronous MSI custom action starts hidden bootstrap code through trusted script hosts (**PowerShell, `cmd.exe`, `WScript`**) and launches Node.js from `LocalAppData`. Loaders/encrypted payloads use **nonstandard extensions** (`.tmp`, `.ini`, `.dat`, `.bin`, `.cfg`); the runtime is sometimes a **renamed copy** whose original file metadata still identifies it as Node.js.
5. **Per-user persistence.** Update-themed **`EdgeUpdate`** entries — either an `HKEY_CURRENT_USER` Run value or a **Startup-folder shortcut** — launch the Node.js loader from `LocalAppData` at sign-in.
6. **C2 + operator tasking.** The implant uses **randomized HTTPS long-polling**; C2 responses are treated as JavaScript source and executed with Node.js module loading, process execution, environment, buffers, and file-system access. Observed tasking: short-lived `cmd.exe`/`PowerShell` host recon, **display-adapter + antivirus product queries (sandbox/virtualization checks)**, disk inventory, and **periodic Base64-encoded desktop screenshots** written to a temp file before exfiltration. The recovered builds also carried **dormant Ethereum smart-contract C2 discovery** (a disabled fallback that queries an on-chain contract for an updated C2 URL; the contract stores only a URL string, not the payload).
7. **Domain discovery.** Native commands + **ADSI** queries enumerate domain accounts, servers, and users (including the `description` attribute, which can carry operational notes and privileged-account context); an ADSI sweep resolves Windows Server computer objects and probes each for administrative reachability — building a live map of high-value targets.
8. **Follow-on payloads.** Additional payloads run through **`rundll32`** loading attacker-supplied DLLs.
9. **Lateral movement via WinRM (T1021.006).** C2-delivered tasking opens **WinRM over TCP 5985** to domain-joined systems, **including domain controllers and CAs**.

## Indicators of Compromise (IOCs)
**Malicious MSI loader packages (SHA-256):**
`4cfdcae6dd1d6d98b870c8f0654d504f2bf10479a117dc297de789c249dc389d`, `a4d145a6347e47d40b3ca48af5c6dba01bf019d0110e31a44bb70fc77d1d1676`, `cc6d0f3f47afeba018173604e34f527e8413d3a54ffb35caed529bff49055ec5`

**Second-stage DLLs (rundll32-loaded):**
`0d2fc28af246f62f27e49207d1f64e236ad9ea029412b27877d1ae6c098e86e3`, `69e10e0cb7bb2137ebea12971adb02c662cf5543a4f8c9530812bcbf7b183a23`, `a135fe4df18c711097e69b4f27ea32a74a955160bf2fb12da841f21866d95d87`

**Payload delivery (Azure Blob Storage):** `update1n5[.]blob.core.windows.net`, `update1n6[.]blob.core.windows.net`, `update1n7[.]blob.core.windows.net`, `update1n9[.]blob.core.windows.net`, `updatetmp[.]blob.core.windows.net`

**C2 infrastructure (Ethereum-contract / hardcoded fallback URLs):** `synctimes[.]australiaeast[.]cloudapp[.]azure[.]com` (hardcoded fallback + latest URL in the contract), `webwether[.]eastus[.]cloudapp[.]azure[.]com` (earlier contract URL), `dssdfvsdfvsdfvsdgbfbdvdzv[.]org` (briefly in the contract).

## MITRE ATT&CK
Initial Access T1566.003 (spearphishing via service — Teams IT impersonation); Execution T1059.001 (PowerShell), T1059.007 (JavaScript via `node.exe`), T1218.007 (`msiexec` silent MSI), T1218.011 (`rundll32`); Defense Evasion T1036 (update/helpdesk MSI names), T1497.001 (display-adapter + AV sandbox checks); Discovery T1082, T1016, T1087.002, T1018, T1518.001; Collection T1113 (screen capture); C2 T1071.001 (randomized HTTPS long-polling), T1105 (portable Node.js + JS task ingress); Lateral Movement T1021.006 (WinRM 5985).

## Durable detection / defensive heuristics
- **Teams:** external-tenant chat→remote-session pairing with IT-helpdesk impersonation; Quick Assist / RMM connect codes; a remote-assist process tree followed immediately by `cmd.exe`/`PowerShell` on the same desktop; unsolicited external chat + voice call. Restrict "Chat with Anyone"/external chat + voice.
- **Endpoint:** `msiexec /qn` of an update-themed MSI from cloud storage; a **Node.js (or renamed `node.exe`) executing a staged loader from `LocalAppData` on a non-development host**; `EdgeUpdate` Run-key / Startup shortcut; `rundll32` loading non-standard DLLs; repeated Base64 desktop-screenshot writes.
- **Identity/AD:** ADSI-based domain-account and server-enumeration sweeps (with `description`-attribute reads), and **WinRM 5985 pivoting from a user-level host toward DCs/CAs** — treat workstation-context WinRM to the DC as high-confidence lateral movement.
- **Hunt query shape:** `DeviceNetworkEvents` where `InitiatingProcessFileName =~ "powershell.exe"` and `RemoteUrl endswith ":5985/wsman"` in the last 7 days.

## Related pages
- [Node.js runtime as a malware-delivery channel: `node.exe`-anchored implant chains (Symantec, Sep 4)](../patterns/nodejs-runtime-malware-delivery-symantec-september-2026.md)
- [Spring Ring: Microsoft Teams vishing campaigns that escalated to RMM/PowerShell RAT and a PetitPotam DC coercion (Unit 42, Aug 31)](spring-ring-teams-vishing-rmm-petitpotam-campaigns-unit42-august-2026.md)
- [TerminalFix: ClickFix → reverse-tunnel multistage intrusion (Microsoft, Aug 28)](terminalfix-clickfix-reverse-tunnel-multistage-microsoft-august-2026.md)

## Sources
- Microsoft Security Research — "Impersonating IT support: how threat actors turn a remote session into enterprise-wide access" (Sagar Patil, Arlette Umuhire Sangwa, Jesse Birch, Ravikant Tiwari; published 2026-09-02): [https://www.microsoft.com/en-us/security/blog/2026-09-02/impersonating-it-support-threat-actors-turn-remote-session-into-enterprise-wide-access/](https://www.microsoft.com/en-us/security/blog/2026-09-02/impersonating-it-support-threat-actors-turn-remote-session-into-enterprise-wide-access/)
