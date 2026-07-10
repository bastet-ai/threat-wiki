# Progress ShareFile Storage Zone Controller security threat

## Summary
Progress confirmed on July 10, 2026 that ShareFile customers running **Storage Zone Controllers** were affected by a "credible external security threat." The company temporarily disabled access for affected accounts and told customers to shut down the Windows servers running Storage Zone Controllers while it investigated with internal and external security experts.

The public record was still incomplete at publication time: Progress had not named a CVE, actor, exploit path, or confirmed data access. The durable defender value is the operational signal. A vendor-directed shutdown of internet-facing file-transfer edge controllers should be handled as potential compromise until Progress publishes enough detail to scope otherwise.

## Tags
- ops
- active threat
- managed file transfer
- file sharing
- ShareFile
- Progress Software
- Storage Zone Controller
- Windows servers
- edge services
- incident response
- credential exposure
- web shell hunting
- vulnerable appliances
- The Hacker News

## Why this matters
- ShareFile Storage Zone Controllers are customer-operated Windows edge servers that let organizations keep files on their own storage while using ShareFile cloud control and sharing workflows.
- Progress's status page listed Storage Zone Controller customers as "not operational" and "Investigating" beginning July 10, 2026 at 12:12 EDT.
- The Hacker News reported that Progress confirmed a "credible external security threat," temporary account-access disablement, and no indication at that time of unauthorized access to ShareFile accounts or data.
- A shutdown instruction is stronger than normal patch guidance. Until Progress publishes a root cause, defenders should not assume a clean-looking, internet-exposed controller is safe to restart.
- The same product class has precedent for mass exploitation: Citrix ShareFile Storage Zones Controller CVE-2023-24489 was added to CISA KEV in 2023 after active exploitation.

## Reported public timeline
- **July 10, 2026:** A customer-posted notice on Reddit made the shutdown instruction public.
- **July 10, 2026 12:12 EDT:** ShareFile status page incident: "ShareFile customers with Storage Zone Controllers are not operational at this time" and "We are currently investigating this issue."
- **July 10, 2026:** The Hacker News reported that Progress confirmed it was responding to a credible external security threat and had temporarily disabled access for affected accounts out of caution.

## Affected surface
The reporting is specific to **ShareFile Storage Zone Controllers**, not standard cloud-only ShareFile accounts. Storage Zone Controllers are commonly internet-reachable because they broker file access between ShareFile cloud workflows and customer-managed storage.

At publication time, Progress had not publicly tied the threat to either of the critical Storage Zone Controller flaws disclosed earlier in 2026, nor to the older CVE-2023-24489 exploitation path. Treat those older issues as context, not attribution.

## Defender heuristics
- Follow Progress's shutdown instruction first. Keep affected Storage Zone Controllers offline until Progress publishes restart conditions or a mitigation path.
- Confirm controller versions are current — The Hacker News points to `5.12.4` or later on the 5.x line, or a 6.x release — but do not treat patch currency alone as authorization to bring systems back online while the vendor incident remains unresolved.
- If a controller was internet-exposed, start incident response rather than routine maintenance. Preserve IIS logs, Windows event logs, ShareFile controller logs, web directories, storage-zone paths, scheduled tasks, services, PowerShell history, and network telemetry before cleanup.
- Hunt for unfamiliar `.aspx` files, unexpected writable web paths, new local users, unknown services, suspicious scheduled tasks, archive/exfiltration tooling, and outbound connections from the controller to unusual infrastructure.
- Review ShareFile, SSO, identity-provider, API-token, storage-backend, and file-access audit logs for unusual access around and before the shutdown notice.
- Segment or rebuild affected controllers from trusted media if compromise cannot be ruled out. Rotate credentials, API keys, storage access tokens, service-account passwords, and certificates that were present on the controller.
- Track Progress status and advisory channels for CVE assignment, IOCs, affected-version ranges, and explicit safe-restart guidance.

## Related pages
- [Progress Kemp LoadMaster CVE-2026-8037 pre-auth RCE](progress-kemp-loadmaster-cve-2026-8037-preauth-rce.md)
- [SimpleHelp CVE-2026-48558 authentication-bypass exploitation](simplehelp-cve-2026-48558-authentication-bypass-exploitation.md)
- [SolarWinds Serv-U CVE-2026-28318 exploitation](solarwinds-serv-u-cve-2026-28318-exploitation.md)
- [CitrixBleed session-hijack wave](citrixbleed-session-hijack-wave.md)

## Sources
- ShareFile status incident: https://status.sharefile.com/incidents/c59n5343lbkq
- ShareFile status RSS: https://status.sharefile.com/history.rss
- The Hacker News: https://thehackernews.com/2026/07/urgent-progress-tells-sharefile.html
