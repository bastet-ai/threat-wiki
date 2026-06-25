# Backdoor.Mistic / KongTuke ModeloRAT activity

## Summary
Broadcom / Symantec Threat Hunter Team reported **Backdoor.Mistic** in June 2026 as a stealthy Windows backdoor used in cybercrime intrusions since April 2026. The activity is not a classic single-victim ransomware note event: Broadcom frames Mistic as likely tied to **Woodgnat / KongTuke**, an initial access broker whose **ModeloRAT** toolkit has been observed in attacks that later deployed Qilin ransomware and has been publicly linked to multiple ransomware operations.

The durable defender value is the convergence of ClickFix-style initial access, compromised-WordPress traffic distribution, signed legitimate runtimes, DLL sideloading through Microsoft-looking components, in-memory backdoor execution, credential phishing on-host, and access-broker handoff risk.

## Tags
- ops
- malware
- Backdoor.Mistic
- Mistic
- MLTBackdoor
- ModeloRAT
- KongTuke
- Woodgnat
- 404 TDS
- TAG-124
- ClickFix
- initial access broker
- ransomware access
- Qilin
- DLL sideloading
- MpExtMs.exe
- EndpointDlp.dll
- WinPython
- RC4 C2
- compromised WordPress
- fake login screen
- Windows
- Broadcom
- Symantec Threat Hunter Team

## Reported activity
- Broadcom says Mistic has been deployed in multiple attacks since April 2026.
- Targeting appeared opportunistic across insurance, education, IT, and professional-services organizations rather than one narrow sector.
- Mistic was deployed in at least one intrusion in close proximity to **ModeloRAT**, the Python RAT associated with Woodgnat / KongTuke.
- Broadcom separately observed ModeloRAT in attacks that deployed **Qilin ransomware**.
- Public reporting has linked Woodgnat / KongTuke to Qilin, Interlock, Rhysida, Akira, 8Base, and Black Basta activity; treat those as ecosystem / access-broker relationships, not proof that each ransomware brand operated Mistic directly.

## Delivery and execution chain
Broadcom's described Mistic chain centers on DLL sideloading and trusted-looking component names:

- A legitimate Microsoft executable, `MpExtMs.exe`, is used as the sideloading host.
- A malicious loader named `version.dll` hooks `GetModuleFileNameW` and `LoadLibraryW`.
- The hook logic keeps `mpextms.exe` pointed at its legitimate path while forcing load of a malicious `EndpointDlp.dll`.
- `EndpointDlp.dll` is Backdoor.Mistic; the name blends with Microsoft endpoint-security / DLP terminology.
- Broadcom also observed a .NET DLL credential stealer that displays a fake login screen.
- The backdoor executes in memory and includes a kill switch, increasing the likelihood of low artifact volume and long-lived access.

## Woodgnat / KongTuke tradecraft context
Broadcom describes Woodgnat / KongTuke as a financially motivated initial access broker active since at least May 2024. Reported recurring tradecraft includes:

- A traffic distribution system built largely from compromised WordPress sites.
- Social-engineering lures that trick users into executing attacker-provided commands.
- ClickFix / fake error / fake CAPTCHA flows that steer victims into pasting commands into the Windows Run dialog or terminal-like prompts.
- DNS lookup-based staging in some chains, where DNS is used as lightweight signaling or payload discovery.
- Microsoft Teams fake-IT-support lures reported by other vendors for ModeloRAT delivery.
- Enterprise-target selection logic that distinguishes domain-joined hosts from standalone `WORKGROUP` systems.

## ModeloRAT notes
ModeloRAT remains a key pivot for tracking the cluster:

- Typically delivered inside a portable WinPython package.
- Uses a signed `pythonw.exe` interpreter to run Python RAT scripts.
- Common persistence path: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Uses RC4-encrypted C2 communications.
- Maintains resilience through multiple independent C2 paths and sequential failover.
- For some non-domain-joined victims, reported variants use a domain-generation algorithm to rotate through fresh C2 domains.
- Post-compromise activity has included Windows and Active Directory reconnaissance with `net.exe`, PowerShell inventory collection, domain user / group / computer / session enumeration, and Kerberoasting-oriented queries against service-principal-name accounts.

## Defender notes
- Treat any Mistic or ModeloRAT detection as an **access-broker incident**: preserve evidence, scope identity exposure, and assume the access may have been sold or staged for ransomware.
- Hunt for `MpExtMs.exe` execution outside expected Microsoft Defender paths, especially when paired with local `version.dll` or `EndpointDlp.dll` files.
- Hunt for suspicious `EndpointDlp.dll` loads from user-writable, temporary, staging, or application-data directories.
- Review DLL-load telemetry for `version.dll` near copied legitimate Microsoft executables.
- Hunt for fake-login-screen .NET DLL execution and suspicious credential prompts appearing outside normal identity-provider or OS logon flows.
- Search for portable WinPython directories, `pythonw.exe` launched from unusual paths, and Python RAT execution without an approved business application.
- Review `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` values that launch portable Python, WinPython, or unexpected scripts.
- Treat ClickFix telemetry as initial access: browser-to-clipboard-to-Run-dialog chains, PowerShell launched soon after fake CAPTCHA / fake error pages, and DNS lookups followed by staged script download.
- Scope compromised-WordPress TDS exposure separately from endpoint artifacts; the same TDS may deliver different lures over time.
- Keep attribution precise: Broadcom says Mistic **may be linked** to Woodgnat / KongTuke and was observed with ModeloRAT in one intrusion; do not overstate this as confirmed ransomware-operator authorship.

## IOCs and pivots
Broadcom published hashes including:

- `1e41c7bfaa6aa3b93b6cc024274a10e33f3e12fe7c98c1db387ef8927f9d1984` — Backdoor.Mistic / `endpointdlp.dll`
- `34d798a6c55e57ed0932b6499f4fbcb5454bdfca903307be101a0594b0ac07bc` — fake lock screen / `f.dll`
- `3f797a639bc855bc6d5471f327924b62d10900ddec49b970eca6604142bbb4be` — Backdoor.Mistic / `aeff97fe.msi`
- `59e3c4cb06331b4f2d78a9a0592f3747e573bd01c5a7650c26361d1e25520712` — loader / `version.dll`
- `8c935feec4bd05d5d918df308be417532fb42608fb989a08eab183e0ae699235` — likely privilege escalation / `n.dll`
- `afd5f1ed45a9867daf3bc64152cef460a06b164c8183e490db39146d4749a82c` — Backdoor.Mistic / `endpointdlp.dll`
- `db972979d508e75fe730d3b72c2701470fbdaeaf8ebdd674744754fa44438ca5` — Backdoor.Mistic / `endpointdlp.dll`
- `f591275a8f014b29e567529d67c54eb7bb4473db1c38737d6bfd5b3d52c9344e` — Backdoor.Mistic / `48b47c0.msi`
- `fb3630822b70bacb56aa4cec29b5a0e3e9acb3920809e70310a4003385a6d34a` — Backdoor.Mistic / `endpointdlp.dll`

Use hashes as confirmation pivots, not the only detection path; the sideloading shape and ModeloRAT / ClickFix behaviors are more durable.

## Sources
- Broadcom / Symantec Threat Hunter Team, “Backdoor.Mistic: New Backdoor May be Linked to Ransomware Access Broker”: https://www.security.com/threat-intelligence/new-mistic-backdoor-modeloRAT
- The Hacker News summary: https://thehackernews.com/2026/06/new-mistic-backdoor-linked-to-kongtuke.html
