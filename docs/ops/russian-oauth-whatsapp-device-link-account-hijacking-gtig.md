# Russian auth-focused espionage: Google OAuth and WhatsApp device-link hijacking

## Tags
- ops
- Russia
- cyberespionage
- phishing
- OAuth
- OAuth phishing
- device-code phishing
- device linking
- WhatsApp
- Google account
- token theft
- credential theft
- account hijacking
- Ice Relic
- Midnight Blizzard
- Storm-2945
- UNC6293
- UNC7005
- UNC5976
- Google OAuth
- CaptiveCrunch
- Vidar
- AMOS
- Google Cloud
- HEADRUSH

## Summary
Google Threat Intelligence (GTIG) published an August 20, 2026 report covering three distinct, suspected-Russian cyber-espionage threat clusters — **UNC6293**, **UNC7005** (aka **Storm-2945**), and **UNC5976** — that abuse legitimate authentication flows to compromise individuals in academia, aerospace and defense, government, and think tanks across Europe and the United States. The clusters run persistent, adaptive phishing campaigns that misuse trusted identity features: application-specific passwords, Google OAuth login, Microsoft/WhatsApp device-code and device-link flows, and cloud-hosted phishing pages that harvest tokens.

The report is high-signal because it ties authentication abuse to **CaptiveCrunch** (the Midnight Blizzard hospitality captive-portal campaign tracked by Microsoft) and to a suspected **MSP supply-chain** compromise that Lumen Black Lotus Labs is tracking, extending the operation from venue Wi-Fi into the managed-service-provider trust relationship.

## Attribution and scope
- **UNC6293** — first detailed by Google and the Citizen Lab in June 2025; GTIG assesses it a sub-cluster of **Ice Relic** (formerly APT29, aka Cozy Bear / Midnight Blizzard). Previously linked to application-specific-password phishing to seize victim accounts. Active in small-scope (fewer than five users) campaigns impersonating State Department officials with diplomatic-themed lures; as recently as June 2026 observed conducting OAuth phishing by asking targets to share the full URL or verification code after a legitimate login to an external provider.
- **UNC7005** (aka **Storm-2945**) — identified by GTIG in February 2026; the report's core focus. Primarily targets academia, diplomatic, and nonprofit personnel across Ukraine, Western Europe, and the U.S. Conducted device-code phishing for both Microsoft and WhatsApp accounts. In May–June 2026 ran social-engineering operations spoofing **WhatsApp** to lure targets into linking their WhatsApp accounts to an attacker-controlled device ("to join a secure WhatsApp call, chat, or document share"). Around May 2026 augmented tradecraft with commodity infostealers (**Vidar**, **Atomic/AMOS**) against Windows and macOS hosts targeting U.S.-based academics, diplomats, and researchers focused on Russia and former Soviet states. In early August 2026 began Google-account OAuth phishing using cloud infrastructure; from July 31, 2026 registered domains spoofing the Finnish Operations Center (FOC) supporting Finnish defense/security firms in the NATO context, and between August 6–13, 2026 sent targeted phishing emails to European defense-industry targets.
- **UNC5976** — active since at least March 2026; uses OAuth phishing and automates token collection by abusing cloud infrastructure. Creates file-sharing-themed domains and a related cloud project; the fake file-sharing page shows a "Continue with Google" pop-up that redirects to the legitimate Google OAuth login, then bounces the victim to a Google Cloud project URL hosting scripts that retrieve and stage the authentication token. GTIG estimated at least 12 new domains and related infrastructure since March 2026, all disrupted by Google, prompting a pivot away from Google to other providers. UNC5976 has also been observed using a rogue Excel plugin codenamed **HEADRUSH** to deliver a downloaded HTML Application (HTA); the artifact (discovered April 2026) is distributed via a fake domain impersonating a Ukrainian research institute, with indications it may have targeted a Ukrainian aerospace and imaging company.
- GTIG assesses both **UNC6293** and **UNC7005** as related to a sub-group within **Ice Relic** focused on initial access operations, relying on commercial residential proxies for post-compromise activity.
- Wine-themed lures are a recurring Ice Relic theme dating to April 2023 (codenamed **SPIKEDWINE** by Zscaler).

## Tactic detail
### WhatsApp device-linking spoofing (UNC7005, May–June 2026)
1. A phishing page lures the target into "linking" their WhatsApp account to an attacker-controlled device to join a secure call, chat, or document share.
2. The target supplies a phone number; the attacker uses it to create a legitimate WhatsApp device-link request on the attacker device, then displays the legitimate QR code and linking code with instructions to link.
3. Once the account is linked, the page prompts the target to either join a voice call, enter an encrypted chat, or download a file.
   - **Voice call:** triggers JavaScript that records the target's audio and video and sends the recording to a C2 endpoint.
   - **Encrypted chat:** prompts the target to copy the username and password shown to log in on a secondary URL.
   - **File download:** nature unknown.
4. The attacker also attempts multiple other compromise methods after the device is linked.

### Google OAuth phishing via cloud projects (UNC5976 and UNC7005)
- The victim is redirected to the **legitimate** Google OAuth login page and signs in.
- On success, the victim is sent to an attacker-controlled (often unverified) Google Cloud project URL where malicious scripts retrieve the authentication token from the URL and stage it for later use, enabling account hijacking.
- UNC5976 builds this out of file-sharing-themed domains plus a per-domain cloud project; UNC7005 began it in early August 2026 using FOC-spoofing domains against European defense targets.

### App-password and device-code phishing (UNC6293, UNC7005)
- UNC6293: small-scope, diplomatic-themed app-password phishing; OAuth phishing via full-URL/verification-code capture.
- UNC7005: device-code phishing for Microsoft (diplomatic-event invitations with course/wine-preference prompts embedding links to attacker-controlled sites) and for WhatsApp.

### HEADRUSH Excel-plugin HTA delivery (UNC5976)
- A rogue Excel plugin delivers a downloaded HTML Application (HTA); distributed via a domain impersonating a Ukrainian research institute; possibly targeted a Ukrainian aerospace and imaging company. Full infection scope unknown.

## Relationship to CaptiveCrunch
GTIG states CaptiveCrunch did not "happen in a vacuum": UNC7005 has run multiple campaigns in tandem to obtain access to victim accounts. The CaptiveCrunch operation targets captive Wi-Fi portals at hotels, conference centers, and airports in the U.S. and elsewhere, redirecting users to attacker-controlled infrastructure to steal credentials, and (per Microsoft) has been ongoing since early May 2026, using doppelganger domains mimicking Microsoft services for adversary-in-the-middle Entra device-code phishing and distributing a Go-based **CornFlake** RAT or an LLM-generated PowerShell infostealer **ChocoShell** (aka CHERRYPIE) via ClickFix lures, all managed through a web C2 panel branded "CloudSync Console" / "Acuity Systems, Inc." (**FruitStone**).

Lumen Black Lotus Labs' ongoing tracking of the same campaign raised the possibility that the actor **compromised several Managed Service Providers (MSPs)** and abused the trust relationship with their clients in a supply-chain attack. Lumen telemetry identified ~70 victim IP addresses, of which 40 unique IPs sent DNS requests to CaptiveCrunch C2s (assessed as places where the actor had access and enumerated), another 30 unique IPs communicated with the actor's AiM infrastructure to harvest tokens, and a single IP interacted with the ChocoShell C2.

## Defender guidance
- **Treat account-linking and device-linking prompts as high-risk identity events.** WhatsApp, Google, and Microsoft device-linking that originates outside a known, user-initiated context is a strong account-hijack indicator; revoke the linked device and all active sessions.
- **Google OAuth / "Continue with Google" harvesting:** alert on sign-ins followed by token exfiltration to unverified or newly created Cloud project URLs; review OAuth client grants and revoke anomalous tokens. Correlate legitimate-OAuth redirects with unexpected Cloud project destinations.
- **App-password phishing:** block or tightly scope application-specific passwords; require phishing-resistant MFA for privileged and high-risk users.
- **Device-code flows:** scope the OAuth device-code flow via Conditional Access; alert on anomalous device-code authentication and unexpected Entra device registration.
- **Vendor / MSP supply-chain:** review MSP-managed environments and Wi-Fi gateways for DNS-resolution redirects and unexplained resolver changes; treat shared captive-portal and managed-service access as a potential initial-access path.
- **Infostealer hygiene:** assume commodity infostealers (Vidar, Atomic/AMOS) can exfiltrate credentials, browser data, and cloud tokens from both Windows and macOS; rotate secrets and revoke sessions on suspected exposure.

## Evidence limits
- GTIG describes these as "suspected Russian" clusters; attribution to a named state operator is Google's assessment, not a court- or multi-agency-confirmed identification.
- The UNC7005 / UNC6293-to-Ice-Relic relationship and the UNC6293-to-Ice-Relic sub-cluster assessment are Google's; independent confirmation is not public.
- The MSP supply-chain hypothesis is Lumen's assessment; it is not yet confirmed.
- The HEADRUSH-to-Ukrainian-aerospace targeting is an indication, not a confirmed victim.
- Indicators and infrastructure are time-bounded; correlate with behavior rather than a single domain or IP.

## Related pages
- [CaptiveCrunch Midnight Blizzard hospitality captive-portal campaign](captivecrunch-midnight-blizzard-hospitality-captive-portal-campaign.md)
- [APT29 / Cozy Bear / Midnight Blizzard](../actors/apt29-cozy-bear-midnight-blizzard.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [DEBULL device-code phishing and GraphSpy post-exploitation](debull-device-code-phishing-graphspy.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)

## Sources
- Google Cloud / Mandiant Threat Intelligence: [Distinct clusters target individuals of interest to Russia](https://cloud.google.com/blog/topics/threat-intelligence/distinct-clusters-target-individuals-of-interest-to-russia)
- Google Cloud / Mandiant Threat Intelligence: [APT29 / evolving diplomatic phishing](https://cloud.google.com/blog/topics/threat-intelligence/apt29-evolving-diplomatic-phishing)
- The Hacker News: [Suspected Russian Hackers Abuse Google OAuth and WhatsApp Linking to Hijack Accounts](https://thehackernews.com/2026/08/suspected-russian-hackers-abuse-google.html)
- Microsoft Security Blog: [CaptiveCrunch: Midnight Blizzard targets travelers worldwide](https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/)
- ReliaQuest: [Threat Spotlight: DNS poisoning tactics expand to hospitality](https://reliaquest.com/blog/threat-spotlight-dns-poisoning-tactics-expand-to-hospitality/)
