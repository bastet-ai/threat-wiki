# CaptiveCrunch Midnight Blizzard hospitality captive-portal campaign

## Summary
Microsoft Threat Intelligence attributes **CaptiveCrunch**, an ongoing campaign observed since early May 2026, to **Storm-2945**, which it assesses is an operational subcluster of Midnight Blizzard. The actor compromises or otherwise gains traffic-manipulation access within hospitality and shared-venue captive-portal networks, redirects travelers through actor-controlled infrastructure, and uses fake connectivity, browser, or operating-system update flows to deliver malware or device-code phishing.

The operation is high-signal because the initial trust boundary is the network itself: a successful connection to hotel, conference-center, or other guest Wi-Fi can trigger malicious content in response to normal browser connectivity checks. Microsoft reports widespread affected networks in several countries and notes common equipment and management systems across multiple victims, raising—but not proving—the possibility of access to shared captive-portal services rather than only isolated venue compromises.

## Tags
- ops
- Storm-2945
- Midnight Blizzard
- APT29
- Russia
- cyberespionage
- hospitality
- captive portal
- traffic manipulation
- DNS hijacking
- adversary-in-the-middle
- ClickFix
- device-code phishing
- OAuth
- Microsoft Entra ID
- CornFlake
- ChocoShell
- FruitStone
- Go malware
- PowerShell
- credential theft
- token theft
- browser credential theft
- AI-augmented operations

## Attribution and scope
- Microsoft assesses Storm-2945 is a Midnight Blizzard operational subcluster based on distinctive technical and operational overlaps, including similarities to Storm-2372's device-code and OAuth-code phishing, Microsoft Graph email collection, commercial-messaging social engineering, and victimology.
- Midnight Blizzard is associated by the US and UK governments with Russia's Foreign Intelligence Service (SVR). Its established objectives are long-term espionage supporting Russian foreign-policy interests.
- Storm-2945 has conducted AI-augmented device-code and OAuth-code phishing since February 2026, leading to Entra device registration and Microsoft 365 collection. Microsoft says the actor used AI to support a significant portion of CaptiveCrunch operations, but does not characterize the campaign as autonomous.
- Microsoft observed CaptiveCrunch traffic manipulation from early May 2026. Device-code landing pages were observed from July 16.
- Affected networks include hotels, conference centers, and other shared venues in several countries. Public reporting does not provide a venue or traveler count.
- Microsoft says its investigation of the captive-portal network initial-access path is ongoing. Common equipment and management systems suggest a possible shared-service compromise, but this is not yet confirmed.

## Intrusion chain
1. Storm-2945 obtains a position that can manipulate DNS and HTTP traffic for a network served by captive-portal equipment.
2. Normal connectivity checks or browsing are redirected through actor-controlled infrastructure.
3. The landing presents a fake browser, operating-system update, verification failure, or other ClickFix-style prompt.
4. The victim is induced to download and execute Windows malware. Microsoft also observed Android-specific instructions to download an APK, but did not publish a confirmed Android payload analysis.
5. Alternative landing flows send the victim to a legitimate Microsoft device-code authentication page with an actor-controlled code, causing the victim to authorize the actor's session.
6. Windows payloads establish persistent remote access, collect files, keystrokes, browser credentials and session tokens, and support microphone, webcam, removable-media, and shell operations.
7. Stolen Microsoft 365 and Entra tokens can move the intrusion from an untrusted travel network into the victim's corporate cloud environment.

## Tooling

### CornFlake
CornFlake is the campaign's primary persistent Windows remote-access trojan. It is written in Go and initially operates as a dropper while displaying a configurable fake progress window. Themes include Windows Update, Defender scanning, DirectX, Visual C++ runtime, disk optimization, network diagnostics, browser update, and document-viewer installation.

Observed behavior includes:
- copying itself to `%APPDATA%\svchost32\svchost32.exe`;
- registering the `svchost32` service with display name `Cloud Sync Service` and description `Synchronizes files with the cloud storage provider`;
- redundant persistence through services, Registry Run keys, scheduled tasks, and a watchdog that restores removed mechanisms;
- ECDH P-256 ephemeral key exchange, SHA-256 key derivation, and an encrypted custom JSON C2 protocol;
- hot C2 and collection reconfiguration through `sync.dat`;
- raw-input keylogging, clipboard and active-window capture, screenshots, WASAPI microphone capture, Media Foundation webcam capture, file and removable-media collection, host-security survey, and remote shell;
- ChromeKatz-derived live Chromium cookie extraction, on-disk password theft, Chrome App-Bound Encryption bypass, and Firefox NSS/SDR decryption; and
- a localhost API exposing `/upload`, `/reload`, and `/status`, allowing companion payloads to reuse CornFlake's C2 channel.

File collection is extension-driven and grouped into documents, archives, images, code, data, email, and keys. Microsoft reports a per-cycle throttle of 1,000 files or 500 MB.

### ChocoShell
ChocoShell is an in-memory PowerShell infostealer focused on browser sessions, saved passwords, Microsoft 365 SSO material, and Wi-Fi credentials. Its public sample beaconed to `213.145.86[.]112` and used web-like routes:
- `/t/pixel.gif?m=<status>` for status beacons;
- `/cdn/chunks/polyfill-7e2b.min.js` for an additional Base64-encoded in-memory module; and
- `/t/event` for GZip-compressed, Base64-wrapped JSON exfiltration.

The script attempts AMSI bypass through .NET reflection and timing-based sandbox detection. Its ordered privilege-escalation paths are:
1. `SilentCleanup` task hijacking through `HKCU\Environment\windir`;
2. `wsreset.exe` COM hijacking under `HKCU\Software\Classes`;
3. `sdclt.exe /KickOffElev` folder-handler hijacking; and
4. visible `Start-Process -Verb RunAs` fallback.

A variant references WinGet Desired State Configuration's `ConfigurationRemotingServer`, suggesting possible execution through malicious machine-provisioning configuration. Public reporting establishes the code path, not confirmed use of that path against victims.

With elevation, ChocoShell can impersonate a SYSTEM token from `winlogon.exe`, `wininit.exe`, or `services.exe`, use DPAPI and Volume Shadow Copy access, and lock Defender signature updates. It also launches Chromium browsers with a remote-debugging port and calls `Network.getAllCookies`, using transient interactive-token scheduled tasks when necessary and relaunching the browser with `--restore-last-session`. It collects `.tbres` Token Broker material, Microsoft 365 and Entra access and refresh tokens, WAM tokens, and cleartext Wi-Fi profiles obtained with `netsh wlan show profile ... key=clear`.

### FruitStone
FruitStone is the web C2 and payload-management interface. The panel masquerades as `CloudSync Console` from `Acuity Systems, Inc.` and supports:
- multiple operators, JWT sessions, session revocation, and source-IP visibility;
- real-time CornFlake inventory through server-sent events;
- shell, file browsing, collection tasking, configuration push, implant update, and kill operations;
- C, Go-stub, or standalone CornFlake payload builds;
- configurable collection and evasion modules;
- proxy-relay, TLS-certificate, staging-server, beacon-profile, SNI, and DNS-fallback management; and
- live rotation of C2 server lists across online agents.

Microsoft describes the exposed application as having all campaign-management functionality in one interface while also describing JWT-based operator authentication. Defenders should not infer that every deployed panel is anonymously usable.

## Device-code abuse
The device-code path uses a legitimate Microsoft authentication experience. The actor initiates the flow and induces the victim to enter the actor-controlled code; successful authentication authorizes the actor's session rather than a session on the traveler's device. The method is not new, but placement behind a captive-portal or network-connectivity flow can make the prompt appear expected.

Device-code success should be treated as cloud-account compromise even if no malware is found. Response needs to include session and refresh-token revocation, device-registration review, Microsoft Graph and mailbox audit, and Conditional Access investigation.

## Defender guidance

### Travel and network controls
- Treat hotel, conference, airport, and guest Wi-Fi as hostile. Prefer managed cellular connectivity, eSIM, or a managed hotspot where practical.
- Consider preventing unmanaged Wi-Fi profiles on enterprise devices through MDM. Where business needs require guest networks, establish an encrypted corporate tunnel before sensitive access.
- Never install updates, certificates, diagnostics, security tools, or APKs offered by a captive portal. Use the operating system, browser, managed software center, or known vendor channel.
- Do not reuse corporate credentials on venue registration pages. Minimize disclosure of employee identity, organization, and travel details where policy permits.

### Identity controls
- Block the OAuth device-code flow unless a documented business requirement exists; otherwise scope it narrowly with Conditional Access.
- Require phishing-resistant MFA for privileged and high-risk users. Restrict MFA and passkey registration to trusted devices and locations.
- Alert on anomalous device-code authentication, unexpected Entra device registration, new WAM or refresh-token use, and Graph-based mailbox collection.
- Following suspected exposure, revoke sessions and refresh tokens rather than relying only on password rotation.

### Endpoint and network hunting
- Correlate normal connectivity checks with executable, MSI, ZIP, RAR, or 7z creation within a short window.
- Hunt for `%APPDATA%\svchost32\svchost32.exe`, the `svchost32` service, `Cloud Sync Service`, and the description `Synchronizes files with the cloud storage provider`.
- Investigate browsers started with remote-debugging arguments, especially when launched through transient scheduled tasks and followed by `--restore-last-session`.
- Hunt for suspicious use of `SilentCleanup`, `HKCU\Environment\windir`, `wsreset.exe`, `sdclt.exe /KickOffElev`, VSS creation, SYSTEM-token impersonation, AMSI tampering, and Defender signature locking.
- Treat access to the public domains, IPs, and hashes below as historical indicators requiring time and behavior correlation. Infrastructure can rotate, and addresses may be reassigned.

## Public indicators

### Domains
- `ms365-device[.]com` — device-code-flow redirect
- `ms365-live[.]com` — device-code-flow redirect
- `m365-owa[.]com` — adversary-in-the-middle infrastructure
- `owa-ms365[.]com` — adversary-in-the-middle infrastructure

### IP addresses
- `31.57.243[.]154` — adversary-in-the-middle infrastructure
- `38.146.28[.]75` — adversary-in-the-middle infrastructure
- `38.146.28[.]132` — DNS resolver
- `104.194.159[.]150` — adversary-in-the-middle infrastructure
- `107.189.26[.]194` — ChocoShell C2 / DNS resolver
- `213.145.86[.]112` — ChocoShell C2

### SHA-256
- `918fa52ae45ed60ba7cc8bdc99c3cbe9ab92e0375ec31fc05d0d4513be11c593` — CornFlake
- `be99857449d2856dd5a84e21c8a3d5e0e01456adb44062ddec5a6b4970d8d42c` — ChocoShell

## Evidence limits
- Microsoft has not publicly identified the captive-portal equipment, management platform, shared provider, initial access vulnerability, or compromised credentials.
- The common-infrastructure observation supports a shared-service hypothesis; it does not establish a captive-portal software supply-chain compromise.
- Android-specific landing instructions indicate targeting intent. They do not by themselves confirm APK execution, payload family, or victim compromise.
- AI supported a significant portion of the operation according to Microsoft. Public evidence does not support describing Storm-2945 as an autonomous AI actor.
- Indicators are snapshots. Attribution should use campaign behavior, identity activity, and endpoint evidence rather than an IP or domain alone.

## Related pages
- [APT29 / Cozy Bear / Midnight Blizzard](../actors/apt29-cozy-bear-midnight-blizzard.md)
- [Microsoft Midnight Blizzard mailbox theft from Microsoft](microsoft-midnight-blizzard-mailbox-theft-from-microsoft.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)

## Sources
- Microsoft Security Blog: [CaptiveCrunch: Midnight Blizzard targets travelers worldwide for malware delivery and credential theft](https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/)
- ReliaQuest: [Threat Spotlight: DNS poisoning tactics expand to hospitality](https://reliaquest.com/blog/threat-spotlight-dns-poisoning-tactics-expand-to-hospitality/)
- Volexity: [Multiple Russian threat actors targeting Microsoft device code authentication](https://www.volexity.com/blog/2025/02/13/multiple-russian-threat-actors-targeting-microsoft-device-code-authentication)
