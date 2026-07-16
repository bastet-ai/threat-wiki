# Fast16

## Summary
**Fast16** is a precision sabotage framework documented by SentinelOne and later analyzed in depth by Broadcom / Symantec in May 2026. Its oldest components appear to date to around 2005, predating Stuxnet, and its purpose was not ordinary espionage or destructive wiping: the tool selectively patched scientific simulation software to corrupt high-explosive and uranium-compression outputs associated with nuclear-weapon design.

The durable lesson is that Fast16 shows the Stuxnet pattern before Stuxnet: malware coupled to deep domain knowledge, target-specific engineering workflows, and narrowly gated process manipulation. Defenders should treat unusual kernel drivers, file-system filters, IFEO hijacks, and application-specific in-memory patching around engineering or simulation platforms as possible sabotage signals rather than generic persistence.

## Tags
- tools
- malware
- sabotage
- Fast16
- nuclear weapons
- simulation tampering
- LS-DYNA
- AUTODYN
- high explosives
- uranium compression
- industrial control
- engineering software
- kernel driver
- file-system filter
- Lua
- IFEO persistence
- MPR network provider
- share propagation
- Stuxnet lineage
- targeted operations

## Why this matters
- Broadcom confirmed Fast16's hook engine targeted LS-DYNA and AUTODYN builds used for explicit-dynamics and explosive simulations.
- The tampering activated only under narrow conditions, including high-explosive equation-of-state selections and simulated uranium density crossing roughly `30 g/cm³`.
- The framework carried 101 opcode-pattern rules grouped for roughly 9-10 software builds, implying an operation that tracked target software versions over time.
- Fast16 reduced or scaled pressure / stress tensor outputs during full-scale detonation simulations, creating plausible but wrong results rather than obvious crashes.
- Its propagation was intentionally local-network scoped, consistent with a tool meant to persist and spread inside a specific target environment without uncontrolled worm behavior.

## Operational characteristics
- **Kernel file-system interception:** a boot-start driver monitors executable reads and patches matching instruction sequences as files are loaded.
- **Target gating:** Fast16 first waits for `EXPLORER.EXE`, then examines Intel-compiler PE files and applies hooks only when its byte-pattern rules match.
- **Rule-driven sabotage:** the hook engine injects an `.xdata` section and redirects specific floating-point instruction sequences into malicious handlers.
- **Simulation-specific logic:** LS-DYNA-focused hooks check high-explosive equation-of-state values such as Jones-Wilkins-Lee and Ignition and Growth; AUTODYN-focused hooks check corresponding high-explosive / ideal-gas EOS choices.
- **Nuclear-design thresholding:** Broadcom's analysis ties the `30 g/cm³` start threshold to uranium under shock compression, with scaling factors that reduce pressure or Cauchy stress outputs as density increases.
- **Service and driver install:** the installer copies itself as `%windir%\\system32\\svcmgmt.exe`, installs a `SvcMgmt` service, drops `fast16.sys`, and configures it as a SCSI-class filter driver.
- **IFEO hijack:** it can abuse Image File Execution Options `Debugger` values to launch itself before a chosen legitimate program, then restore the hijack after handing control to the original application.
- **Network spread:** a Lua runtime and MPR notify DLL track share connections, enumerate domains / servers / shares, impersonate the logged-on user, copy to `admin$`, and remotely create the `SvcMgmt` service.
- **Containment logic:** propagation is restricted to private ranges and same-subnet checks, suggesting deliberate avoidance of broad internet-scale spread.

## Defender heuristics
- Inventory boot-start and file-system filter drivers on engineering, simulation, and high-assurance workstations; investigate unsigned, unfamiliar, or vendor-mismatched drivers.
- Review `HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\*\\Debugger` for unexpected debugger paths, especially references to copied service binaries or engineering-tool launchers.
- Hunt for suspicious `SvcMgmt` service entries, `%windir%\\system32\\svcmgmt.exe`, and anomalous SCSI-class filter-driver registrations such as `fast16.sys`.
- Baseline LS-DYNA, AUTODYN, and other high-consequence engineering executables by hash and on-disk section layout; alert on unexplained `.xdata` sections or runtime patching.
- Correlate simulation-result anomalies with endpoint telemetry rather than treating them only as modeling errors, especially when anomalies appear version-specific or disappear after software rollback.
- Monitor lateral movement through `admin$`, remote service creation, MPR network-provider DLL registration, and named-pipe coordination from engineering workstations.
- Preserve full disk, registry, driver, and memory evidence before remediation; the sabotage target may be the scientific output, not the host itself.

## Related pages
- [RemotePE](remotepe.md)
- [3CX desktop app compromise](../ops/3cx-desktop-app-compromise.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- [Broadcom / Symantec](https://www.security.com/threat-intelligence/fast16-nuclear-sabotage)
- [SentinelOne](https://www.sentinelone.com/labs/fast16-mystery-shadowbrokers-reference-reveals-high-precision-software-sabotage-5-years-before-stuxnet/)
