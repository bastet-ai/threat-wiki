# CL-STA-1114 Zimbra webmail espionage

## Summary
Unit 42 reported on July 23, 2026 that **CL-STA-1114**, an activity cluster overlapping **Void Blizzard / LAUNDRY BEAR**, has used crafted HTML email and **CVE-2025-66376** against unpatched Zimbra Collaboration Suite (ZCS) webmail since July 2025. A same-day joint advisory from CISA, NSA, FBI, AIVD, MIVD, and more than 20 other government partners identifies the operator as Russian state-supported and names the client/server capability **Ulej / Flowerbed**. The combined public reporting covers government, defense-industrial-base, education, energy, law-enforcement, media, NGO, technology, transportation, and financial targets across NATO states, Ukraine, CIS countries, and Africa.

The browser-resident JavaScript executes in an authenticated Zimbra session when crafted content is rendered, then steals credentials, CSRF and two-factor recovery material, system details, devices, OAuth-consumer records, the Global Address List, and up to 90 days of email. Unit 42 reported nine C2 IP addresses and nine domains, with servers active for an average of 35.4 days. The joint advisory adds historical first/last-seen dates, certificate hashes, sender and provisioning addresses, message hashes, browser-local-storage artifacts, precise SOAP calls, and Flowerbed server behavior. The absence of a dropped endpoint binary makes browser, webmail, DNS, proxy, and mailbox-audit telemetry central to detection.

## Tags
- ops
- campaign
- CL-STA-1114
- Void Blizzard
- LAUNDRY BEAR
- Russia-affiliated
- cyberespionage
- Zimbra
- Zimbra Collaboration Suite
- webmail
- CVE-2025-66376
- stored XSS
- JavaScript injection
- HTML email
- SVG
- Base64
- credential theft
- CSRF token theft
- 2FA recovery codes
- mailbox theft
- email exfiltration
- DNS exfiltration
- SOAP API abuse
- active exploitation
- government targeting
- defense
- transportation
- financial sector
- NATO
- Ukraine
- CIS
- Africa
- Unit 42
- Seqrite Labs
- CISA
- Ulej
- Flowerbed
- TA488
- Russian state-supported

## Reported chain
1. **Targeted email arrives in Zimbra.** Unit 42 observed either HTML attachments or embedded HTML using attention-grabbing news headlines. A Seqrite-analyzed Ukrainian case instead used a manually composed internship inquiry from a likely compromised sender account.
2. **Crafted content triggers CVE-2025-66376.** Hidden and obfuscated HTML uses a CSS `@import` sanitization bypass and a Base64-encoded script. An invisible SVG loads and injects JavaScript into the authenticated browser context.
3. **The script acquires session authority.** The payload reads Zimbra CSRF state and invokes same-origin SOAP and export functionality as the victim. Seqrite reported that it also injected hidden username and password fields and waited for browser password-manager autofill.
4. **Mailbox and authentication material are collected.** Reported targets include the email address and password, CSRF token, 2FA scratch codes, Zimbra configuration and environment data, aliases, search history, and 90 days of non-junk email.
5. **Durable access can outlive a password reset.** In the Seqrite sample, the script created or collected a Zimbra app-specific password, which could retain IMAP/API access after the primary password changed.
6. **Data leaves over web and DNS channels.** Unit 42 reported hard-coded C2. Seqrite documented HTTPS POST/upload paths and Base32 values split across DNS labels, including dual-channel exfiltration for selected data.

## Joint-advisory technical follow-up
The July 23 joint advisory names the browser payload **Ulej** and its server-side collection framework **Flowerbed**. It says Ulej initially exploited CVE-2025-66376 as a zero-day in July 2025 and that the actors began sending payloads from compromised victim accounts by at least November 2025.

- Ulej executes 12 asynchronous stages spanning start/finish telemetry, environment and identity collection, 2FA-code and application-passcode theft, device and OAuth-consumer inventory, password-autofill capture, IMAP enablement, GAL enumeration, and mailbox export.
- It sets `zimbraPrefImapEnabled` to `TRUE`, creates the `ZimbraWeb` application passcode, and brute-forces GAL searches through 20 SOAP batches containing 1,521 total `SearchGalRequest` operations.
- One compressed export is requested for each of the preceding 90 days. Ulej records processed days as `zd_comp_YYYY-MM-DD=true` in Zimbra-origin browser `localStorage`, creating a durable endpoint artifact and potential exfiltration timeline.
- DNS A queries use a `d-`-prefixed randomized victim ID and Base32 data labels. HTTPS posts use `/v/p` for JSON and `/v/d` for binary data; reported filenames include `zimbra_batch_analytics.json`, `telemetry_{1-20}.json`, and `telemetryData_{0-89}.json`.
- Flowerbed uses Dockerized Catcher, Certbot, Nginx, and Gardener components. Nginx forwards only SNI containing `*.i.*`; Catcher receives DNS and HTTP data, stages it under `/root/hits/tmp` and `/root/hits/ready`, and an automated SSH workflow reportedly retrieves processed records about every 60 seconds.
- The advisory says Flowerbed's simple Python code shows signs of AI-assisted development. That observation concerns code-development artifacts and is not evidence of autonomous campaign operation.

See [Ulej / Flowerbed](../tools/ulej-flowerbed.md) for the capability profile and protocol-level detection detail.

Unit 42 calls this a zero-click phishing technique because no attachment execution or credential entry is required. The public technical description still says the crafted message must be viewed/rendered in vulnerable Zimbra webmail; defenders should not infer compromise merely from delivery without validating product behavior and telemetry.

## Vulnerability and exposure notes
- Seqrite identifies CVE-2025-66376 as stored XSS caused by insufficient sanitization of crafted HTML, including CSS `@import` and related script-injection structures.
- The vulnerability is triggered in the Zimbra Classic UI when a crafted email is viewed.
- Seqrite reports fixes in **ZCS 10.0.18 and 10.1.13**, released in November 2025, and recommends migrating immediately from unsupported Zimbra 8.8.15.
- Unit 42 says threat actors continue to target unpatched instances. Its reporting establishes observed exploitation but does not publish a complete victim count.

## Detection pivots
### Zimbra and identity
- Message bodies or attachments containing hidden `div` elements, CSS `@import` anomalies, Base64 script blocks, invisible SVG elements, or JavaScript that reaches the top-level Zimbra document.
- Unusual SOAP requests with `X-Zimbra-Csrf-Token` shortly after a suspicious message is viewed.
- Repeated or automated requests to `/home/~/?fmt=tgz`, especially one export per day across a roughly 90-day interval.
- New app-specific passwords named `ZimbraWeb`, access to 2FA recovery codes, unexpected identity/alias enumeration, or app-password use after a primary-password reset.
- Abnormal browser password-manager autofill into hidden fields in the Zimbra origin.
- Dense activity in `/opt/zimbra/log/mailbox.log`, especially `SearchGalRequest`, `CreateAppSpecificPasswordRequest`, `GetScratchCodesRequest`, `GetDeviceStatusRequest`, and `GetOAuthConsumersRequest` from one user over a short period.
- Browser `localStorage` keys matching `zd_comp_YYYY-MM-DD` under the Zimbra origin. Preserve the browser profile before clearing site data; the key dates can help bound attempted mailbox collection.

### Network
- DNS labels with high-entropy or Base32-like chunks, especially the Seqrite-reported `d-[a-z0-9]{12}.i.*` style combined with mail-analytics-themed parent domains.
- HTTPS POSTs to `/v/p` or uploads to `/v/d` with an `X-Filename` header on unrelated external hosts.
- `/v/d` uploads named `zimbra_batch_analytics.json`, `telemetry_<1-20>.json`, or `telemetryData_<0-89>.json`.
- TLS certificates for `*.i.<domain>` matching the historical SHA-1 values in the joint advisory. Treat certificate and infrastructure indicators as historical pivots, not standalone blocking decisions.
- Large or repeated outbound transfers from a webmail browser session immediately following suspicious email rendering.
- Correlated DNS and HTTPS exfiltration carrying similar timing or data volumes.

## Public Unit 42 indicators
Use the source IOC table as the canonical record and validate indicators in context.

### IP addresses
- `37.120.247[.]228`
- `64.226.124[.]190`
- `104.248.134[.]194`
- `185.86.79[.]95`
- `193.238.152[.]66`
- `194.156.103[.]193`
- `216.252.238[.]18`
- `216.252.238[.]64`
- `216.252.238[.]104`

### Domains
- `analyticemailmeter[.]com`
- `emailanalytics[.]com[.]ua`
- `istc-cloud[.]com`
- `mailnalysis[.]com`
- `synacorzimbra[.]nl`
- `zimbra-metadata[.]com`
- `zimbrastat[.]com`
- `zimbrasoft[.]com[.]ua`
- `zmailanalytics[.]com`

The joint advisory maps each domain to its IP and historical first/last-seen dates from July 2025 through March 2026. It also publishes nine Let's Encrypt certificate SHA-1 hashes, four provisioning addresses, three ProtonMail distribution addresses, two compromised Ukrainian sender domains, four malicious-message SHA-256 hashes, and downloadable STIX. Use the advisory as the canonical machine-readable IOC record; do not copy historical email addresses into preventive block rules without validation.

## Response guidance
1. Preserve the suspicious message in raw form, Zimbra audit/mailbox logs, reverse-proxy and DNS logs, browser history/cache, and volatile browser evidence before cleanup.
2. Patch or isolate vulnerable ZCS instances. Confirm the actual deployed UI and build; do not rely only on a package inventory or version claim from an unmanaged appliance.
3. Search all mailboxes for matching HTML structures, sender infrastructure, and campaign indicators. Delivery may be broader than confirmed execution.
4. Review account activity for mailbox exports, SOAP enumeration, app-specific-password creation, 2FA scratch-code access, and unusual IMAP/API use.
5. Revoke active sessions, app-specific passwords, 2FA recovery codes, and other persistent tokens; reset credentials from a known-clean system.
6. Scope stolen mail as a secondary compromise source: search for credentials, reset links, API keys, sensitive attachments, contact relationships, and information that can enable follow-on phishing.
7. Block confirmed malicious infrastructure where appropriate, but retain behavior-based detection because Unit 42 observed C2 rotation and an average server lifetime of about 35 days.
8. If immediate patching is impossible, the joint advisory recommends that users avoid the vulnerable Zimbra Classic web client and use an alternative mail client until a fixed build is deployed.

## Attribution caveat
The joint government advisory identifies the operator as Russian state-supported and lists LAUNDRY BEAR, Void Blizzard, CL-STA-1114, and Proofpoint's TA488 (formerly UNK_PitStop) as overlapping industry labels, while warning that they may not map one-to-one to the governments' understanding. Seqrite's earlier Operation GhostMail report attributed a related Ukrainian Zimbra sample to APT28 with medium confidence. Preserve source-specific labels rather than collapsing every name into a universal alias.

## Related pages
- [CL-STA-1114 / Void Blizzard](../actors/cl-sta-1114-void-blizzard.md)
- [Ulej / Flowerbed](../tools/ulej-flowerbed.md)
- [UNK_MassTraction Roundcube university mailserver campaign](unk-masstraction-roundcube-university-mailserver-campaign.md)
- [Russian intelligence Signal backup-key phishing](russian-intelligence-signal-backup-key-phishing.md)

## Sources
- CISA et al., July 23, 2026: [AA26-204A — Russian State-Supported Cyber Actors Conduct Phishing Campaign Targeting Users of Zimbra Collaboration Suite](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-204a)
- Unit 42, July 23, 2026: [Russian Global Webmail Espionage](https://unit42.paloaltonetworks.com/russian-webmail-espionage/)
- Seqrite Labs, March 2026: [Operation GhostMail: Russian APT exploits Zimbra Webmail to Target Ukraine State Agency](https://www.seqrite.com/blog/operation-ghostmail-zimbra-xss-russian-apt-ukraine/)
- Microsoft Security Blog, May 27, 2025: [New Russia-affiliated actor Void Blizzard targets critical sectors for espionage](https://www.microsoft.com/en-us/security/blog/2025/05/27/new-russia-affiliated-actor-void-blizzard-targets-critical-sectors-for-espionage/)
