# Photo ZIP hospitality Node.js implant campaign

## Summary
Microsoft Threat Intelligence reported an active multi-stage intrusion campaign targeting hotel and hospitality organizations in Europe and Asia since April 2026. Microsoft has not attributed the activity to a known actor.

The campaign uses photo-themed phishing and browser-downloaded ZIP archives that contain fake image shortcut files. When opened, the `.lnk` chain runs obfuscated PowerShell, deploys a user-space Node.js runtime and JavaScript implant, adds dual registry persistence, and beacons to C2 infrastructure over non-standard ports. Microsoft observed post-compromise C2 beaconing, forced shutdowns, Defender process exclusions, and compilation or staging of follow-on PE payloads.

## Tags
- ops
- operations
- phishing
- hospitality targeting
- hotel targeting
- Node.js implant
- PowerShell
- LNK
- authentication laundering
- Calendly abuse
- Google redirect abuse
- Cloudflare Turnstile
- registry persistence
- Defender exclusion

## Why this matters
- The delivery path abuses legitimate services, including Calendly notification mail and Google redirect infrastructure, so SPF/DKIM/DMARC success is not enough to treat the message as benign.
- The lure fits front-desk and reservation workflows: staff are asked to open guest-photo or complaint-themed archives that appear operationally plausible.
- The implant brings its own Node.js runtime under a user-writable path, reducing dependency on preinstalled tooling and making JavaScript payload execution repeatable across hosts.
- Dual `HKCU\Run` and self-refreshing `HKCU\RunOnce` persistence means cleanup needs to cover both the Node.js component and relocated ProgramData payloads.

## Attack chain
1. Phishing emails use hospitality-themed lures, with Microsoft observing subjects around guest complaints, room inquiries, bedbug / health-inspection pressure, and similar reputational urgency.
2. Late-May delivery abused Calendly notification infrastructure under a threat-actor-controlled account plus Google redirect hops. Microsoft calls the email-authentication bypass effect **authentication laundering**: the message can pass SPF, DKIM, and DMARC because it was sent by legitimate service infrastructure, even though the content is malicious.
3. The redirect chain can route through `calendly[.]com/url?q=`, `share[.]google`, and `www.google[.]com/share_google` before landing on `photo-*` domains, including Cloudflare-fronted `.cfd` hosts gated by Cloudflare Turnstile.
4. Victims download `photo-<random>.zip` archives containing fake image shortcuts. Wave 1 used `IMG-<random>.png.lnk`; Wave 2 shifted to `PHOTO-<random>.png.lnk`.
5. Shortcut execution launches obfuscated PowerShell that decodes a URL using BigInt arithmetic, retrieves a `.ps1` script, and runs it from `%TEMP%`.
6. Wave 2 adds a dynamic .NET compilation stage through `csc.exe` and `cvtres.exe`, producing small random-named DLLs. Microsoft did not observe those DLLs loaded through `rundll32` or `regsvr32` in available telemetry.
7. The PowerShell stage deploys Node.js `node-v24.13.0-win-x64` from the legitimate Node.js site into a user-space path and runs random-named JavaScript payloads with a C2 domain argument.
8. The JavaScript implant uses `child_process.spawn()` with `detached: true`, `stdio: 'ignore'`, and `windowsHide: true` to establish a hidden child process.
9. Follow-on payloads add Defender `Add-MpPreference -ExclusionProcess` entries for random `%TEMP%` executables, launch silent installer-like helpers, relocate payloads into `C:\ProgramData\<random>\<payload>.exe`, and add registry persistence.

## Persistence and execution notes
- Node.js runtime path observed by Microsoft: `C:\Users\<user>\AppData\Local\Nodejs\`.
- Observed implant command shape: `node.exe C:\Users\<user>\AppData\Local\Nodejs\<random>.js <c2-domain>`.
- ProgramData relocation uses randomized mixed-case directory names and lowercase executable names.
- Registry persistence uses `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` for the Node.js component and `HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce` for ProgramData payloads.
- Microsoft observed RunOnce entries being refreshed after execution, creating a loop rather than a true one-time launch.

## Hunt pivots
- Browser downloads or email links leading to `photo-<random>.zip` in hospitality environments.
- Fake image shortcuts matching `IMG-<digits>.png.lnk` or `PHOTO-<digits>.png.lnk`; Microsoft noted observed LNK sizes consistently around 1,989-2,079 bytes.
- PowerShell with `-ep bypass`, BigInt arithmetic, byte extraction through `-band 0xFF` or `-band 255`, right-shift loops, `Invoke-WebRequest` / `iwr`, and `%TEMP%\*.ps1` execution.
- `csc.exe` spawning `cvtres.exe` from a PowerShell-downloaded stage and producing random 3,072-byte DLLs.
- `node.exe` executing from `%LOCALAPPDATA%\Nodejs` or other user-writable Node.js paths shortly after a ZIP/LNK launch.
- PowerShell adding `Add-MpPreference -ExclusionProcess` for random `%TEMP%\*.exe` paths seconds before those executables run.
- `cmd /c reg add` writes to `HKCU\...\RunOnce` with random value names and `C:\ProgramData\<random>\<payload>.exe` data.
- Outbound connections to non-standard ports `8443`, `8445`, `8453`, `5555`, `56001`, `56002`, or `56003`, especially from hospitality front-desk or reservation systems.

## Microsoft-highlighted indicators

| Indicator | Type | Context |
| --- | --- | --- |
| `178.16.54[.]27` | IP address | Primary C2; active in both waves on ports `56001` / `56002` |
| `95.217.97[.]121` | IP address | Wave 1 persistent beacon infrastructure |
| `193.202.84[.]32` | IP address | Wave 1 secondary infrastructure |
| `178.16.55[.]179` | IP address | Wave 1 infrastructure |
| `172.67.161[.]215` | IP address | Cloudflare shared CDN address associated with phishing / TonRAT C2 in Microsoft indicators |
| `8443`, `8445`, `8453`, `5555`, `56001`, `56002`, `56003` | Port | Non-standard C2 ports |
| `sec-safe-dc[.]info` | Domain | Domain observed active in both waves |
| `safedocphoto[.]info` | Domain | Representative C2 domain |
| `recallnine[.]info` | Domain | Representative C2 domain |
| `kentjerk[.]info` | Domain | Representative C2 domain |
| `photodoc-secure[.]info` | Domain | Representative C2 domain |
| `kelopins[.]info` | Domain | Representative C2 domain |
| `photo-26254[.]cfd` | Domain | Wave 2 Cloudflare-fronted photo-themed landing/C2 infrastructure |
| `photo-26654[.]cfd` | Domain | Wave 2 Cloudflare-fronted photo-themed landing/C2 infrastructure |
| `photo-132454[.]cfd` | Domain | Wave 2 Cloudflare-fronted photo-themed landing/C2 infrastructure |
| `photo-8632454[.]cfd` | Domain | Wave 2 Cloudflare-fronted photo-themed landing/C2 infrastructure |
| `d14ba95cdce1ef7dc9ad3ac74949ca5db38b27378ee30f30a23cf26f9e875a11` | SHA-256 | Legitimate `node-v24.13.0-win-x64` runtime downloaded and abused by the campaign |

## Response guidance
1. Treat opened ZIP/LNK events as endpoint compromise candidates, not just phishing clicks.
2. Preserve email headers, redirect URLs, browser history, downloaded ZIP/LNK files, PowerShell transcripts or script-block logs, Defender preference-change events, registry hives, scheduled process telemetry, and copied ProgramData payloads.
3. Remove both persistence lanes: user-space Node.js / JavaScript files and ProgramData payloads referenced by `HKCU\Run` or `HKCU\RunOnce`.
4. Revert unauthorized Defender exclusions and review for short-lived exclusions that were added immediately before random `%TEMP%` executables ran.
5. Block or investigate the Microsoft-listed C2 ports and photo/document/vault-themed domains, but do not rely only on domain blocks because the actor is rotating `.info`, `.com`, `.pro`, `.xyz`, `.cloud`, `.icu`, `.sbs`, `.click`, `.bond`, and `.cfd` infrastructure.
6. For hospitality helpdesks and front-desk teams, add user-facing warnings that legitimate-service notifications can still carry malicious redirect chains and that `.png.lnk` files are executable shortcuts, not images.

## Related pages
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)
- [Microsoft Teams external-chat phishing](../patterns/microsoft-teams-external-chat-phishing.md)
- [StealC / Amadey infrastructure disruption](stealc-amadey-infrastructure-disruption.md)

## Sources
- Microsoft Security Blog: <https://www.microsoft.com/en-us/security/blog/2026/06/25/photo-zip-campaign-targeting-hospitality-industry-delivers-node-js-implant-persistent-access/>
