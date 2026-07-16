# ScreenConnect freeware / AsyncRAT SEO campaign

## Summary
Kaspersky Securelist reported a large **ScreenConnect-abuse campaign** in July 2026 after one MDR investigation into suspicious ScreenConnect activity led to a broader infrastructure cluster. The operators distributed malicious installer archives from spoofed freeware and game-related download sites that appeared in search results, silently installed ConnectWise ScreenConnect, and used that remote-administration foothold to deliver **AsyncRAT** through PowerShell/VBScript staging, reflective .NET loading, and RegAsm process hollowing.

Kaspersky said the uncovered delivery network included more than 90 localized domains across 10 languages, with lures impersonating software such as OBS Studio, DNS Jumper, DS4Windows, Bandicam, Glary Utilities, Process Hacker, and other popular utilities.

## Tags
- ops
- operations
- ScreenConnect
- ConnectWise ScreenConnect
- remote monitoring and management
- RMM abuse
- AsyncRAT
- SEO poisoning
- search result poisoning
- freeware impersonation
- typosquatting
- DLL sideloading
- install.res.1033.dll
- Microsoft-signed binary abuse
- RegAsm process hollowing
- scheduled task persistence
- Windows Defender exclusions
- UAC bypass
- credential theft
- Kaspersky Securelist

## Attack chain
1. **Search-driven lure:** users searching for popular utilities land on spoofed domains that mimic official download portals. Kaspersky observed fraudulent sites ranking highly in search results.
2. **Archive delivery:** the fake site delivers a ZIP archive such as `obs-studio-windows-x64.zip` from staging hosts including `fileget.loseyourip[.]com` or `direct-download.giize[.]com`.
3. **Signed-binary sideload:** the archive contains a renamed legitimate Microsoft-signed `install.exe` plus a malicious `install.res.1033.dll`.
4. **Dual installation:** the sideloaded DLL runs the promised legitimate application installer while also silently installing ScreenConnect from an MSI hidden under names such as `Assets\x86\Data\vcredist_x64.dll`.
5. **Remote service:** ScreenConnect is installed as a service named **Microsoft Update Service** and is configured for attacker-controlled connection servers such as `r[.]servermanagemen[.]xyz`.
6. **Post-install scripting:** ScreenConnect spawns PowerShell and VBScript that add broad Microsoft Defender exclusions, reduce UAC prompting by setting `ConsentPromptBehaviorAdmin` to `0`, and stage files in `C:\Users\Public`.
7. **AsyncRAT loader:** `cap.ps1` decodes bytes from `secret_bytes.txt`, XORs with key `0xA7`, reverses bit order, reflectively loads a .NET assembly, and runs process hollowing against `RegAsm.exe`.
8. **Persistence and C2:** the chain creates a scheduled task named `MasterPackager.Updater` that runs every two minutes and the injected AsyncRAT connects to `mora1987[.]work[.]gd`.

## Infrastructure notes
Kaspersky grouped the distribution infrastructure into two clusters:

- **Cluster 1:** `162.216.241[.]242` hosted spoofed delivery sites including `www[.]studioobs[.]com`; payload archives were staged separately on `198.23.185[.]81` / `fileget.loseyourip[.]com`.
- **Cluster 2:** `2.59.134[.]97` hosted both spoofed freeware sites and direct archive distribution through `direct-download.giize[.]com`.

The campaign reportedly began with game-themed lures, shifted toward freeware impersonation in January 2026, and was active from October 2025 through March 2026 based on C2/domain registration dates. Kaspersky noted that many landing pages remained accessible through search results at publication time.

## Public pivots
Selected public indicators from Kaspersky reporting:

- loader MD5s: `B32810973132D11AFD61CCEE222BBB79`, `5B7E1FE55BD7B5EA54BD4ED1677E5A26`, `9A9CCD8B0E5D05F4EE77667B024844DB`, `0EEE9BAD07E22415439E854657FA1366`, `8F4E8B680D3E8D3F5AC39BD72882F713`
- malicious `install.res.1033.dll` MD5 examples: `5F96C04E3AFAE97017B201BE112284D2`, `73BEAD922109A61E5F9F85771A7812C5`, `EDFF4F58722C93D7C09ED71899416396`, `83601C3D4ED28E8D2BE1B99BEB8EC18C`
- AsyncRAT C2: `mora1987[.]work[.]gd`
- delivery / spoofed domains: `studioobs[.]com`, `studio-obs[.]com`, `studio-obs[.]net`, `obs-studio[.]site`, `dnsjumper[.]app`, `dns-jumper[.]com`, `ds4windows[.]io`, `ds4windows[.]net`, `processhacker[.]dev`, `processhacker[.]org`, `defendercontrol[.]org`, `bandicam[.]app`, `direct-download.giize[.]com`, `fileget.loseyourip[.]com`
- ScreenConnect C2 example: `r[.]servermanagemen[.]xyz`

## Defender response
1. Treat unexpected ScreenConnect installation as a possible initial-access event, even when the binary is signed and the tool is normally allowlisted.
2. Hunt for ScreenConnect service creation with command lines containing `e=Access` or `e=Support`, especially when the service name is disguised as Microsoft update infrastructure.
3. Alert on ScreenConnect child processes launching `powershell.exe`, `cmd.exe`, `net.exe`, `schtasks.exe`, `sc.exe`, `msiexec.exe`, `mshta.exe`, or `rundll32.exe`.
4. Review `C:\Users\Public` for staged `script.vbs`, `cap.ps1`, `secret_bytes.txt`, `msgbox.txt`, and similarly named loader artifacts.
5. Check for scheduled task `MasterPackager.Updater` or any high-frequency task that launches `wscript.exe` from a public/user-writable directory.
6. Audit Microsoft Defender exclusions for broad drive/root-directory additions and process exclusions such as `RegAsm.exe`.
7. Audit `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\ConsentPromptBehaviorAdmin` for unexpected `0` values.
8. Correlate search/download history, proxy logs, and DNS for spoofed freeware domains before the ScreenConnect install time.
9. If AsyncRAT or suspicious ScreenConnect activity is found, scope as credential theft and brokered-access risk; rotate credentials and revoke sessions from the affected host.
10. Restrict software installation from untrusted ZIP/MSI sources and enforce application allowlisting for RMM tools by approved tenant/server identity rather than binary name alone.

## Why this matters
- Legitimate remote administration tools remain high-leverage intrusion primitives because they blend into enterprise allowlists and provide immediate operator control.
- The campaign used commodity SEO and freeware lures rather than targeted phishing, creating both consumer and enterprise exposure.
- Delivering the real requested software alongside ScreenConnect reduces user suspicion and can leave defenders chasing normal installer telemetry.
- Broad Defender exclusions, UAC prompt reduction, process hollowing, and two-minute scheduled-task persistence create a short path from "free utility download" to durable RAT access.

## Related pages
- [ConnectWise ScreenConnect exploitation wave](connectwise-screenconnect-exploitation-wave.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [TamperedChef-style productivity malware clusters](tamperedchef-productivity-malware-clusters.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)

## Sources
- [Kaspersky Securelist](https://securelist.com/tr/the-soc-files-screenconnect-campaign-with-asyncrat/120472/)
