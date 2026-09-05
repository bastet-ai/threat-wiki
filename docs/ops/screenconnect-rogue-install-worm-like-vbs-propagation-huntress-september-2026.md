# Rogue ScreenConnect installations: worm-like VBS propagation across unrelated hosts (Huntress)

## Summary
Huntress reported (September 3, 2026) **rogue ScreenConnect installations observed across unrelated hosts in multiple separate organizations**, with the observed propagation behavior suggesting **worm-like spread**: infected hosts act as **content-delivery nodes** for other hosts that connect through the attacker-controlled ScreenConnect endpoint. The chain is socially engineered (tech-support scam via phone / fake alerts), leads to a rogue ScreenConnect client, and then deploys a **four-stage VBS + AES + PowerShell loader chain** that ends in an elevated, AMSI-bypassing PowerShell payload (`PyTorchFix.ps1`) that installs a concealed ScreenConnect client, adds sweeping Defender exclusions, and ships a `combo.zip` with tunneling utilities and a cryptocurrency miner.

Huntress published three customer incidents in late August (first reported August 20, second August 20, third August 24) across separate organizations, all with additional RMM solutions present. The same-day ConnectWise advisory (September 3, 2026) — "ScreenConnect® Remote Access: Guest File Transfer Advisory" — covers **Cloud and On-Premise** deployments; a CVE identifier and official fix are expected "within the week" at publication. Interim mitigation is disabling the `TransferFiles` permission (or `TransferFilesInSession` in legacy environments) under Administration → Security → Roles.

This is a distinct item from the 2024 CVE-2024-1709 / CVE-2024-1708 exploitation wave and the Kaspersky July 2026 freeware/AsyncRAT SEO campaign: the differentiators are the **socially-engineered initial access** (not a ScreenConnect CVE), the **VBS loader chain staged on the attacker's C2 and mirrored onto the victim host**, and the **content-relay propagation** that turns each newly connected host into a delivery mechanism.

## Tags
- ops
- operations
- ScreenConnect
- ConnectWise ScreenConnect
- ConnectWise
- remote monitoring and management
- RMM abuse
- remote access trojan
- social engineering
- tech support scam
- vishing
- VBScript loader
- PowerShell AMSI bypass
- AES encrypted payload
- UAC bypass
- Windows Defender exclusions
- persistence
- worm-like propagation
- UltraViewer
- WinRing0
- cryptocurrency miner
- Huntress
- ConnectWise advisory

## Attack chain
1. **Social-engineering initial access:** tech-support scam over phone / fake alert → victim runs Windows Quick Assist or downloads and runs a ScreenConnect MSI.
2. **Rogue ScreenConnect deployment:** the attacker-controlled ScreenConnect client (`ScreenConnect.WindowsClient.exe`) connects to the C2 set (`45.13.237[.]190` / `tele-sync.opik[.]net`; `131.123.40[.]98:8041`; `15.204.185[.]204`; `borertors92.anondns[.]net`).
3. **Loader staging:** the ScreenConnect client spawns `wscript.exe`, which executes four VBS files (`1.vbs`, `2.vbs`, `3.vbs`, `4.vbs`) pulled from a RAR archive on the C2.
4. **Host profiling (`1.vbs`):** checks for an existing ScreenConnect install (if present, writes `abort` to `%TEMP%\value.txt` and stops), enumerates installed EDR products (Huntress, Cisco AMP, CrowdStrike, SentinelOne, Sophos, Malwarebytes), checks for >5 GB RAM and ScreenConnect in Program Files, then writes a 3-bit state value to `%TEMP%\value.txt`.
5. **Catalogue fetch (`2.vbs`):** waits for `value.txt` (aborts if `abort`), downloads a Base64 payload from a Dropbox URL, decodes it with XOR key `0x90`, and writes `%TEMP%\map.txt` — a catalogue of the form `011=http://url.com/combo.enc|AES_KEY`.
6. **Payload download (`3.vbs`):** waits for `map.txt`, downloads `out.enc` from the URL in `map.txt` using a hardcoded browser-like User-Agent.
7. **Decrypt + execute (`4.vbs`):** waits for `out.enc`, extracts the AES key from the `map.txt` URI, **deletes `value.txt` and `map.txt`** (staging cleanup), writes a PowerShell loader to `%TEMP%\runner.ps1`, and runs it with execution-policy bypass. The PowerShell routine performs **AES-CBC/PKCS#7 decryption** of `out.enc` (first 16 bytes = IV; 32-byte key from `map.txt`) into `%APPDATA%\Microsoft\Windows\Templates\Classic\sys_cache.zip` and executes **`PyTorchFix.ps1`**. It then kills all `wscript.exe` / `cscript.exe` processes and deletes the staging directory.
8. **Elevation and persistence (`PyTorchFix.ps1`, 010 "access" variant):**
   - Compiles `Password.exe` from inline C#.
   - Uses a hijacked `ms-settings:` protocol handler together with `ComputerDefaults.exe` for a **UAC bypass**.
   - Elevated PowerShell sets **`AmsiUtils.amsiInitFailed = true`** (AMSI bypass).
   - Adds all of `C:\Users` as a **Windows Defender exclusion**.
   - Enables a high-performance power plan / disables sleep and hibernation (host kept awake for the operator).
   - Installs a ScreenConnect client (ID `7a4d7d66502d4260`) and **removes its Registry Uninstall entry** to conceal it.
   - Drops `WindowsServiceHost.vbs` / `WindowsServiceHost.bat` under the user's AppData, registered via the **`WindowsServiceHost` User Run Key** for persistence.
   - Deploys the `combo.zip` payload (tunneling utilities + cryptocurrency miner), which includes **`svcdrv64.sys`** — a vulnerable **WinRing0** driver.
9. **Worm-like propagation:** when `value.txt` is `010` or `011`, `4.vbs` writes **all four VBS files to `C:\Users\Public\Libraries\Default\Lib\Lib1`**, turning the infected host into a content-delivery mechanism for any newly-connected ScreenConnect endpoints.
10. **Secondary RMM:** in some cases **UltraViewer** is also installed (C2: `146.59.55[.]107`, `45.32.192[.]150`).

## Infrastructure notes
- **Primary ScreenConnect C2:** `45.13.237[.]190` (also `tele-sync.opik[.]net`), `131.123.40[.]98:8041`, `15.204.185[.]204` (`borertors92.anondns[.]net`).
- **UltraViewer C2:** `146.59.55[.]107`, `45.32.192[.]150`.
- **Payload delivery:** `out.enc` and `map.txt` fetched over plain HTTP from a URL catalogued in `map.txt`; the Dropbox URL used by `2.vbs` was observed offline as of September 2, 2026.
- **Staging directories on victim:** `%TEMP%` (`value.txt`, `map.txt`, `out.enc`, `runner.ps1`), `%APPDATA%\Microsoft\Windows\Templates\Classic` (`sys_cache.zip`), `C:\Users\Public\Libraries\Default\Lib\Lib1` (mirrored VBS set for propagation), user AppData (`WindowsServiceHost.vbs` / `.bat`).
- **Incidents:** three critical customer incidents reported in late August 2026 (Aug 20, Aug 20, Aug 24), across separate organizations, each with additional RMM solutions already present on the host.

## Public pivots
Selected public indicators from Huntress reporting (use for hunting; many will rotate):
- ScreenConnect C2 hosts: `45.13.237[.]190`, `tele-sync.opik[.]net`, `131.123.40[.]98:8041`, `15.204.185[.]204`, `borertors92.anondns[.]net`
- UltraViewer C2 hosts: `146.59.55[.]107`, `45.32.192[.]150`
- Rogue ScreenConnect client ID: `7a4d7d66502d4260`
- Staged filenames: `1.vbs`–`4.vbs`, `value.txt`, `map.txt`, `out.enc`, `runner.ps1`, `sys_cache.zip`, `PyTorchFix.ps1`, `Password.exe`, `WindowsServiceHost.vbs` / `WindowsServiceHost.bat`, `svcdrv64.sys`
- Persistence artifact: `WindowsServiceHost` Run Key under the user hive
- ScreenConnect audit-log tell: `RunFiles` / `RanFiles` entries showing the suspect VBS/PowerShell scripts executed from **`Process: Guest`** — treat as immediately suspicious
- Vendor mitigation surface: `TransferFiles` / `TransferFilesInSession` role permissions (Administration → Security → Roles)

## Defender response
1. **Treat unexpected ScreenConnect installs as initial-access events**, even when the binary is signed and normally allowlisted — correlate install time against social-engineering / call-center activity.
2. **Audit ScreenConnect admin logs for `RunFiles` / `RanFiles` entries executed from `Process: Guest`** — that is the operator-driven file-execution path and the fastest tell in this chain.
3. **Hunt for the VBS loader chain:** `wscript.exe` / `cscript.exe` launching `1.vbs`–`4.vbs`, `%TEMP%\value.txt` / `map.txt` / `out.enc` / `runner.ps1`, and `sys_cache.zip` under `%APPDATA%\Microsoft\Windows\Templates\Classic`.
4. **Alert on the persistence artifacts:** `WindowsServiceHost` Run Key, `WindowsServiceHost.vbs` / `.bat` in user AppData, and any ScreenConnect client install with a **removed Registry Uninstall entry**.
5. **Hunt for the EDR/AV tampering:** `AmsiUtils.amsiInitFailed = true` writes, `C:\Users`-wide Defender exclusions, and the `ms-settings:` / `ComputerDefaults.exe` UAC-bypass artifacts.
6. **Check for the propagation staging:** all four `.vbs` files present under `C:\Users\Public\Libraries\Default\Lib\Lib1` — a host holding this set should be treated as a content-delivery node and isolated.
7. **Review UltraViewer installs** on hosts with the ScreenConnect foothold (C2 `146.59.55[.]107` / `45.32.192[.]150`).
8. **Apply the vendor interim mitigation immediately:** disable the `TransferFiles` permission (or `TransferFilesInSession` in legacy environments) for all roles under Administration → Security → Roles, until the ConnectWise fix ships.
9. **Scope as credential theft + brokered-access risk:** rotate credentials and revoke sessions from affected hosts; the chain's sweep of `C:\Users` and the miner/tunnel payload indicate post-exploitation access beyond the RMM itself.
10. **Enforce application allowlisting for RMM tools by approved tenant/server identity**, not binary name, and gate guest file-transfer capability to the minimum required roles.

## Why this matters
- **Socially engineered RMM installs remain a top initial-access vector**, and ScreenConnect's legitimate, signed, enterprise-allowlisted status makes detection blend into normal telemetry.
- **The propagation model is the new element:** an infected host that mirrors the four VBS loaders into a public directory and serves them to newly-connected ScreenConnect endpoints behaves like a worm — the blast radius grows with every new session the operators open, not just with new phishing victims.
- **The loader chain is deliberately disposable and multi-stage:** VBS → Base64/XOR catalogue → AES-encrypted C2 payload → PowerShell with an in-memory AMSI bypass. No single stage is obviously malicious, and the `map.txt` / `out.enc` cleanup plus `wscript`/`cscript` kill at the end is active anti-forensics.
- **The `Process: Guest` file-execution path is the durable detection primitive** — it separates operator-driven execution from legitimate client-side behavior and is visible in the product's own audit logs.
- **A vendor advisory with a live guest-file-transfer capability is a hard control gap** until the patch lands; the `TransferFiles` role permission is the stopgap that closes the specific abuse path Huntress observed.

## Related pages
- [ConnectWise ScreenConnect exploitation wave](connectwise-screenconnect-exploitation-wave.md)
- [ScreenConnect freeware / AsyncRAT SEO campaign](screenconnect-freeware-asyncrat-seo-campaign.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)

## Sources
- Huntress: [Rogue ScreenConnect Installations Across Unrelated Hosts Suggest Worm-Like Activity](https://www.huntress.com/blog/rogue-screenconnect-installations) (September 3, 2026)
- ConnectWise: [ScreenConnect® Remote Access — Guest File Transfer Advisory](https://www.connectwise.com/company/trust/advisories) (September 3, 2026)
