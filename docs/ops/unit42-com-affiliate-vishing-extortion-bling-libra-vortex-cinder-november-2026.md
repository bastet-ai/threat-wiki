# Unit 42 Com vishing extortion waves: Bling Libra, Vortex, Cinder, fake Chrome extension

## Summary

Unit 42 published **"Dialing for Data: Inside the Com's High-Profile Heists"** on `2026-11-20T22:00:25Z` (fetched `200` by this wiki the same evening), consolidating months of incident-response engagements and telemetry into one picture of the Com-affiliated vishing extortion economy: named actor **Bling Libra (aka ShinyHunters)** plus five activity clusters, **two of them newly uncovered** (CL-CRI-1264 aka **Vortex**, CL-CRI-1274 aka **Cinder**, both first observed September 2026, overlapping with what Google tracks as **UNC6671**). The victims are data-rich organizations in financial services, healthcare and legal, primarily U.S., UK and Australia, and the intrusion never touches a product vulnerability: it is a phone call to an employee (corporate or personal cell), a victim-branded AiTM proxy, and an MFA ceremony handed to the attacker in real time. The three durable new artifacts: (1) **Vortex registers an unauthorized MFA device within MINUTES of authenticating and has reused a single device named `Pixel 10a` across multiple compromised accounts** - a device-name tell your IdP audit log can grep today; (2) **Cinder bypasses Duo entirely by replaying a persistent "keep me signed in" session token from proxy infrastructure**, never re-prompting MFA at all - the token is the credential; (3) CL-CRI-1192 (Google's UNC6671) deploys a sideloaded **"Google Chrome" browser extension** (manifest `1.6.111`, later `1.6.112`) fetched from `oskeysetup[.]com` - keylogging, cookie/storage/IndexedDB theft, QR-code harvesting for login/MFA tokens, webcam streaming, and a full remote-control module over Chrome DevTools Protocol (`chrome.debugger`) - named to disguise the browser's own debugging warning banner. The `oskeysetup[.]com` host was ALREADY on this wiki's September passkey-theme domain census - the join key paid again, months later.

## Tags
- ops
- operations
- vishing
- social-engineering
- identity
- AiTM
- MFA-bypass
- session-token-replay
- Duo
- Microsoft-365
- SharePoint
- OneDrive
- browser-extension
- Chrome-Web-Store-bypass
- Chrome-DevTools-Protocol
- chrome-debugger
- keylogger
- webcam-capture
- extortion
- Com-affiliated
- Bling-Libra
- ShinyHunters
- UNC6671
- CL-CRI-1116
- Redact
- CL-CRI-1147
- Pink
- CL-CRI-1182
- Falcon
- CL-CRI-1192
- Helix
- CL-CRI-1264
- Vortex
- CL-CRI-1274
- Cinder
- oskeysetup

## Why this matters
- **The extortion wave is the identity-side twin of the supply-chain wave this ledger sweeps daily.** Same victims (data-rich orgs, distributed workforces, centralized SSO), same monetization (theft + internal-channel extortion), zero CVEs required. A help-desk call beats every patching program.
- **A reused MFA device name across unrelated accounts is a hunting gift.** Vortex's `Pixel 10a` enrollment within minutes of a suspicious interactive sign-in is a deterministic audit-log query, not a heuristic.
- **Session-token replay voids MFA investment retroactively.** Cinder's Duo "keep me signed in" theft means the defense that mattered lived in token lifetime and IP/device binding, not in the prompt. Alert on Graph/SharePoint API use (`python-requests/2.34.2`, `python-httpx`, Graph SDK UAs) from never-before-seen ASNs under a live SSO session.
- **A sideloaded extension owned the whole browser**, including the credential autofill and session cookies of accounts the user never phished. The extension's own name (`Google Chrome`) was chosen to mute the `Google Chrome started debugging this browser` banner - the disguise targets the defender's warning, not the store.
- **Registrar + hosting fingerprints differentiate the clusters** (NiceNIC + Cloudflare for the elder clusters; Cnobin + Cloudflare for Vortex; Internet Domain Service BS Corp + DDoS-Guard for Cinder) = infrastructure pivots that survive brand renaming.

## Reported activity clusters (Unit 42 Table 1)

| Actor / Cluster | Alias | First observed | Infra observation |
|---|---|---|---|
| Bling Libra | ShinyHunters | 2019 | Consistent NiceNIC + Cloudflare; report- and claims-themed domains |
| CL-CRI-1116 | Redact (formerly BlackFile) | January 2026 | Multiple NiceNIC + Cloudflare |
| CL-CRI-1147 | Pink | May 2026 | Multiple NiceNIC + Cloudflare |
| CL-CRI-1182 | Falcon | Mid-2026 | Consistent NiceNIC + Cloudflare |
| CL-CRI-1192 | Helix | June 2026 | Multiple NiceNIC + Cloudflare |
| CL-CRI-1264 | Vortex (NEW) | September 2026 | Consistent Cnobin + Cloudflare |
| CL-CRI-1274 | Cinder (NEW) | September 2026 | Consistent Internet Domain Service BS Corp + DDoS-Guard |

Telemetry shows the campaigns accelerating significantly around August 2026. Victimology is deliberate: partner communications, executive compensation, pending contracts, private investment portfolios, deal pipelines, cloud data warehouses, patient records, proprietary research; tens of millions of CRM/recruiting records exfiltrated in observed cases; extortion notices broadcast over internal chat (Microsoft Teams) and email, directing recipients to Tor negotiation sites, with regulatory reporting threatened against healthcare victims.

## The two new clusters, in kill-chain form

### CL-CRI-1264 (Vortex): AiTM + minute-scale MFA enrollment + scripted Graph theft
1. Vishing call posing as internal IT support; employee (corporate workstation OR personal mobile) directed to a **victim-org-tailored subdomain** on actor servers acting as a **real-time AiTM proxy** - credentials AND MFA approvals relayed live.
2. **Within minutes of authentication, an unauthorized MFA device is enrolled** for persistence. In multiple instances the SAME device name **`Pixel 10a`** appears across different compromised accounts.
3. Exfiltration is scripted with Python (`python-httpx` User-Agent) against Microsoft 365 mailbox, OneDrive and SharePoint.
4. After theft, attackers send **Microsoft Teams messages directly to victim employees** claiming data theft, pointing at a Tor-hosted negotiation site.
5. Vertical emphasis: healthcare, pharmaceutical and other medical organizations.

### CL-CRI-1274 (Cinder): replay the persistent session token, skip MFA forever
1. Vishing for initial access (same help-desk playbook).
2. Instead of fighting Duo re-prompts, the operators **replay a persistent "keep me signed in" session token - including from proxy infrastructure** - so MFA is never challenged again.
3. Collection/exfiltration via `python-requests/2.34.2` and the Microsoft Graph SDK against SharePoint and OneDrive.
4. Extortion sent internally from a compromised account via email AND Microsoft Teams, directing recipients to a Tor negotiation site.

### The fake "Google Chrome" extension (CL-CRI-1192 / UNC6671)
- Manifest version `1.6.111`, literally **named `Google Chrome`**, never on the Chrome Web Store - downloaded from attacker-controlled `oskeysetup[.]com` and manually sideloaded by the victim using Developer Mode (an earlier page in this wiki carried `oskeysetup[.]com` in the September passkey-theme domain census; registration info resembles infrastructure Google and ReliaQuest disclosed for the same cluster).
- The extension name also **neutralizes the `Google Chrome started debugging this browser` warning banner** that would otherwise scream whenever the C2 module attaches.
- Capabilities: global keyloggers; theft of local/session storage and IndexedDB across ALL sites; harvest of authentication cookies (Microsoft + Google targets); **page scanning for QR codes to capture login/MFA tokens**; webcam feed streaming.
- Full C2 remote control via **Chrome DevTools Protocol (`chrome.debugger`)**: hidden screenshots, dispatched input events, clipboard theft, remote site navigation.
- **Pivot key: a second extension (`1.6.112`) shares the SAME C2 server and the SAME hard-coded API key** - the shared API key, not the manifest, is the join key. Unit 42 assesses with moderate confidence CL-CRI-1192 built it as a desktop credential-extraction alternative; possible but unevidenced sharing with other Com actors.

## Hunt recipes (this wiki's reading, not Unit 42 prescriptions)
- IdP/Okta/Entra audit: `Register new authentication method/device` events where the device model/name is `Pixel 10a`, or where ANY single device identity appears under more than one user; anything enrolled `≈minutes` after a help-desk-adjacent interactive sign-in.
- Graph/Exchange/SharePoint logs: UAs `python-requests/2.34.2` and `python-httpx/*` under user tokens (interactive users do not run Python libraries under their own session), bulk `FileAccessed` from new ASNs, and token replay from proxy-class egress.
- Endpoint/browser inventory: sideloaded extensions with `debugger`, `webRequest`, `cookies`, `tabs`, `management` permissions; Developer Mode enabled on managed machines is itself an exception to alert on.
- Network: new-domain registrations resolving from the registrar/host combos in the table (Cnobin + Cloudflare; Internet Domain Service BS Corp + DDoS-Guard) serving org-name-tailored subdomains.
- Reuse the September passkey-theme census (`oskey*`, `passkey*`, `sso*` families) as a standing domain-grammar watch, not a one-off blocklist.

## Related pages
- [UNC6671 / BlackFile multi-brand vishing extortion operation](blackfile-unc6671-vishing-extortion.md)
- [ShinyHunters](../actors/shinyhunters.md)
- [Microsoft passkey social engineering, identity and cloud compromise (September 2026)](microsoft-passkey-social-engineering-identity-cloud-compromise-september-9-2026.md)
- [Spring Ring Teams vishing campaigns](spring-ring-teams-vishing-rmm-petitpotam-campaigns-unit42-august-2026.md)

## Sources
- Unit 42: "Dialing for Data: Inside the Com's High-Profile Heists" - [https://unit42.paloaltonetworks.com/com-affiliate-vishing-attacks/](https://unit42.paloaltonetworks.com/com-affiliate-vishing-attacks/) (fetched `200` by this wiki `2026-11-20T22:4xZ`, feed `pubDate Fri, 20 Nov 2026 22:00:25 +0000`)
- Unit 42 feed head re-read confirming publication order behind the OPTIMJACK follow-up and QUIC-and-Covert posts already on-wiki.
- Kevin Pham's September 2026 investigation of the fake `Google Chrome` extension, credited by Unit 42 (per the post).
