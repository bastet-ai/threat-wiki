# Ulej / Flowerbed

## Summary
**Ulej** (Russian: “beehive”) is a browser-resident collection and exfiltration capability used by the Russian state-supported actor tracked as **LAUNDRY BEAR**, **Void Blizzard**, **CL-STA-1114**, and **TA488**. A July 23, 2026 joint government advisory says Ulej exploited Zimbra Collaboration Suite **CVE-2025-66376** as a zero-day beginning in July 2025. Viewing a crafted message in vulnerable Zimbra webmail runs Ulej in the authenticated browser context; no endpoint executable is required.

**Flowerbed** is Ulej's actor-controlled server framework. It receives DNS and HTTPS exfiltration, stages the collected records on a short-lived VPS, and supports onward transfer to non-public infrastructure. The public advisory describes Ulej and Flowerbed as a coupled client/server capability, so they are documented together here.

## Tags
- tools
- Ulej
- Flowerbed
- LAUNDRY BEAR
- Void Blizzard
- CL-STA-1114
- TA488
- Russian state-supported
- espionage
- Zimbra
- CVE-2025-66376
- browser-resident malware
- JavaScript
- DNS exfiltration
- HTTPS exfiltration
- Docker
- Python
- Nginx
- Catcher
- Certbot
- Gardener
- Mullvad VPN
- AI-assisted malware development

## Ulej collection sequence
The joint advisory documents 12 asynchronous stages:

1. `sendStartPing`
2. `gather_email`
3. `gather_environment`
4. `gather_2fa_codes`
5. `gather_app_password`
6. `gather_device_status`
7. `gather_oauth_consumers`
8. `gather_autocomplete_password`
9. `enable_mail_protocols`
10. `gather_gal`
11. `sendArchives`
12. `sendFinishPing`

Ulej reads the active Zimbra CSRF token from browser local storage, uses same-origin SOAP requests, enables IMAP, creates an application passcode named `ZimbraWeb`, requests 2FA scratch codes, inventories devices and OAuth consumers, brute-forces two-character Global Address List searches, and attempts browser password-manager autofill capture through hidden fields. It requests one compressed mailbox export per day for the previous 90 days.

The script stores `zd_comp_YYYY-MM-DD=true` in Zimbra-origin browser `localStorage` after processing each day. Those records can survive the browser session and provide both a compromise indicator and a rough exfiltration-scope timeline. Ulej always retries the current day.

## Flowerbed architecture
Flowerbed is a Python project deployed through four Docker containers:

- **Catcher** receives and records DNS and HTTP(S) exfiltration.
- **Certbot** obtains Let's Encrypt certificates through DNS challenges.
- **Nginx** terminates HTTPS and forwards only SNI values containing `*.i.*`; other connections receive HTTP status 444.
- **Gardener** health-checks Catcher.

Catcher listens on TCP port 8000 behind Nginx and on DNS port 53. Received files move from `/root/hits/tmp` to `/root/hits/ready`; an automated SSH connection reportedly retrieves processed data about every 60 seconds, while files at least two days old are deleted hourly. The advisory says the simple Flowerbed code contains signs of AI-assisted development, but this is a tooling assessment rather than evidence that an autonomous system operated the campaign.

## Exfiltration patterns
- A randomized 10- or 11-character victim identifier appears in both DNS and HTTPS traffic.
- DNS A queries use a `d-`-prefixed victim identifier, Base32 data split into labels no longer than 60 characters, and type labels including `e`, `c`, `v`, `url`, `2fa`, `pa`, and `pw`.
- HTTPS JSON posts use `/v/p`; binary uploads use `/v/d` with an `X-Filename` header.
- Repeated binary filenames include `zimbra_batch_analytics.json`, `telemetry_{1-20}.json`, and `telemetryData_{0-89}.json`.
- Catcher's `pixel.gif` response has SHA-256 `ef1955ae757c8b966c83248350331bd3a30f658ced11f387f8ebf05ab3368629`.
- Flowerbed servers were reportedly rotated after 7–60 days and primarily administered through Mullvad VPN.

## Detection and response
- Search `/opt/zimbra/log/mailbox.log` for dense SOAP activity from one user, especially `SearchGalRequest`, `CreateAppSpecificPasswordRequest` creating `ZimbraWeb`, and `GetScratchCodesRequest`.
- Hunt browser artifacts under the Zimbra origin for `zd_comp_YYYY-MM-DD` local-storage keys. Preserve the profile before clearing site data.
- Detect DNS queries with `d-<victim-id>` and high-volume Base32-like labels below mail-analytics-themed domains.
- Detect POST requests to `/v/p` and `/v/d`, especially with the reported `X-Filename` values, shortly after a suspicious message is viewed.
- Correlate Zimbra exports, IMAP enablement, new application passcodes, 2FA-code access, GAL enumeration, device/OAuth inventory, and outbound DNS/HTTPS traffic.
- Patch ZCS to a fixed release. If that cannot happen immediately, the joint advisory recommends avoiding the vulnerable Classic web client and using an alternative mail client until remediation.
- After confirmed compromise, revoke all application passcodes and 2FA scratch codes, reset potentially autofilled passwords from a clean device, revoke sessions and OAuth access, and scope mailbox and GAL theft. Do not rely on blocking historical infrastructure alone.

## Attribution caveat
The joint advisory identifies the operator as Russian state-supported and lists LAUNDRY BEAR, Void Blizzard, CL-STA-1114, and TA488 (formerly UNK_PitStop) as overlapping industry labels, while warning that they may not map one-to-one to the governments' understanding. Earlier Seqrite reporting assessed a technically related Ukrainian sample as APT28 with medium confidence. Keep the source-specific labels rather than treating all names as universal aliases.

## Related pages
- [CL-STA-1114 Zimbra webmail espionage](../ops/cl-sta-1114-zimbra-webmail-espionage.md)
- [CL-STA-1114 / Void Blizzard](../actors/cl-sta-1114-void-blizzard.md)

## Sources
- CISA et al., July 23, 2026: [AA26-204A — Russian State-Supported Cyber Actors Conduct Phishing Campaign Targeting Users of Zimbra Collaboration Suite](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-204a)
- Unit 42, July 23, 2026: [Russian Global Webmail Espionage](https://unit42.paloaltonetworks.com/russian-webmail-espionage/)
- Seqrite Labs, March 2026: [Operation GhostMail: Russian APT exploits Zimbra Webmail to Target Ukraine State Agency](https://www.seqrite.com/blog/operation-ghostmail-zimbra-xss-russian-apt-ukraine/)
