# Star Blizzard's 2026 overhaul — "RedFlick": mass phishing from accounts created on compromised CMS websites, a one-click VHDX/LNK chain, a three-task scheduled-task persistence set with WebDAV execution, and the CosmicPulse Python backdoor (Microsoft, Sep 29, 2026)

## Tags
- ops
- Star Blizzard
- APT42
- FSB Centre 18
- Russia
- RedFlick
- CosmicPulse
- YESROBOT
- NOROBOT
- BAITSWITCH
- scheduled tasks
- WebDAV
- control.exe
- Control Panel applet
- VHDX
- LNK
- steganography
- compromised websites
- CPanel
- WordPress
- phishing
- NGOs
- think tanks
- Ukraine
- DarkSword
- COLDCOPY
- Microsoft Defender

## Summary

Microsoft Threat Intelligence's September 29 update documents **Star Blizzard** (attributed by CISA as subordinate to **FSB Centre 18**) rebuilding its tradecraft since January 2026 after the October 2025 GTI COLDCOPY exposure. Three shifts, all in service of volume:

1. **Spear phishing → large-scale initial-contact campaigns** — tens to hundreds of emails per campaign, at least **13 distinct campaigns Jan–Aug 2026**, affecting **100+ organizations, primarily US and UK**: NGOs, think tanks, governments, financial institutions, diplomacy — anything with a Ukraine-support nexus. Early campaigns (Jan–Feb) tested on **Ukr.net** users with Ukrainian-authority lures (tax-audit, fine notices); from March the actor scaled globally with fake closed-door invitations (IISS, CES, Atlantic Council, Chatham House "London Conference 2026", MAMA Summit). **Read: Ukraine as the test range, then export — capability-progression signature.**
2. **Phishing senders moved from free email (Proton/Microsoft consumer) to accounts created on compromised CPanel/WordPress websites**, reusing the SAME account name across multiple domains — sender reputation borrowed from sites your filters already trust.
3. **Malware delivery: ClickFix → "RedFlick"** — a single user interaction replaces the multi-step ClickFix flow.

## The RedFlick chain

- Follow-up email after target engagement carries a **password-protected RAR/ZIP** — **the password is delivered as an IMAGE** in the email body.
- Mid-Jan variant: malicious **VHDX** ships a LNK disguised as a PDF + hidden BAT + decoy PDF; LNK → hidden `conhost.exe` → `cmd.exe` → BAT opens the decoy PDF and invokes **`SSH.exe` with `PermitLocalCommand`** to download+execute a remote MSI. **OpenSSH as a download rail with command execution on connect — the signed-system-binary inversion again.**
- MSI creates scheduled task(s) running **`control.exe` against a remote WebDAV path** → downloads/executes the **CosmicPulse downloader compiled as a Control Panel applet (DLL/CPL)**, masquerading as a Control Panel item. Downloader publicly known as **NOROBOT/BAITSWITCH**.
- **From April, THREE scheduled tasks** masquerading as network components:
  - **Task 1** ("Internet Quality Test Connection" masquerade): exfiltrates UTF-16+Base64 of hostname+username to C2 AND executes an attacker-chosen DLL via `Shell32.dll!Control_RunDLL` over a **WebDAV UNC path** (HTTP transport, not SMB).
  - **Task 2** ("Network Configuration Manager"): prepares the WebDAV redirector/WebClient machinery the other tasks ride.
  - **Task 3** ("System Health Monitor"): `control.exe` → remote path → next stage.
- **CosmicPulse installation**: downloader fetches two ZIPs (Python 3.8 runtime + bootstrapper; payload = **YESROBOT**), writes an AES key to **`HKCU\Software\Classes\.mollis`**, bootstrapper recovers it with an embedded AES-ECB key, decodes the payload. Registry-as-config under a fake file-extension class key.
- July addition: payloads **hidden in PDF files**; mid-August campaign used **steganography to conceal identifiers**. One Atlantic Council-themed campaign delivered a **DarkSword iOS backdoor install link** instead (ties to Proofpoint's March report — Star Blizzard running iOS exploitation beside Windows).
- DLUA (Digital Security Lab Ukraine, June 2026) observed overlapping TTPs.

## Defender actions

- **Hunt the task triad**: scheduled tasks named like network components whose action is `control.exe` with a UNC/WebDAV target; `webcache`/WebClient service activity from non-admin users; `Control_RunDLL` invocations; `conhost.exe` with hidden window spawning cmd; `ssh.exe` with `PermitLocalCommand` in the command line; VHDX mounts from Downloads; `HKCU\Software\Classes\.mollis` keys; follow-up-email attachments that are password-protected archives where the password arrived as an image.
- Structural: block WebDAV (WebClient) execution paths for standard users; treat newly-created accounts on your own or partners' CMS sites as a phishing surface — **if you run WordPress/CPanel, your contact/signup form is someone else's sender-reputation farm**.
- Microsoft ships AlertInfo-based hunting queries + Defender detections; direct customer notifications continue.

## Related pages
- [Russian intelligence Signal backup-key phishing (earlier Star Blizzard coverage)](russian-intelligence-signal-backup-key-phishing.md)
- [BlueKit / device-code and session-persistence PhaaS landscape](bluekit-browser-in-the-middle-phaas-totp-enrollment-persistence-spycloud-september-2026.md)

## Sources
- Microsoft Threat Intelligence: [https://www.microsoft.com/en-us/security/blog/2026/09/29/star-blizzard-refines-phishing-and-malware-delivery-with-the-redflick-technique/](https://www.microsoft.com/en-us/security/blog/2026/09/29/star-blizzard-refines-phishing-and-malware-delivery-with-the-redflick-technique/) (Sep 29, 2026; full text captured by this wiki via RSS `content:encoded`)
