# ToddyCat

## Summary
**ToddyCat** is an advanced persistent threat cluster publicly tracked by Kaspersky as targeting organizations in Europe and Asia since at least 2020. Public reporting emphasizes corporate-email access, browser-data theft, and tooling designed to reach both local and cloud-hosted mail.

In June 2026, Kaspersky documented ToddyCat's **Umbrij** tool and **Shadow Token via Remote Debug (STRD)** technique for accessing Gmail through Google APIs by abusing a victim's active Chromium browser session and OAuth authorization flow.

## Tags
- actors
- APT
- espionage
- ToddyCat
- Umbrij
- STRD
- email theft
- Gmail
- Google API
- OAuth abuse
- browser session abuse
- Chromium
- DLL sideloading
- Europe targeting
- Asia targeting

## Publicly reported activity
- Kaspersky says ToddyCat has targeted organizations in Europe and Asia since at least 2020.
- Prior public reporting described the group stealing data from browsers and from local and cloud email services.
- In November 2025, Kaspersky reported ToddyCat use of **TCSectorCopy** to obtain Microsoft Outlook email data from targeted companies.
- In June 2026, Kaspersky reported **Umbrij**, a .NET, ConfuserEx-obfuscated tool that automates Gmail access through OAuth and headless Chromium browser control.

## Tradecraft themes
- Corporate correspondence collection rather than noisy destructive activity.
- Browser-session and mailbox-access abuse designed to evade endpoint and monitoring controls.
- Signed-binary DLL sideloading for tool launch.
- Security-vendor impersonation through a fake `KasperskyEndpointSecurityEDRAvp` scheduled-task name.
- OAuth token acquisition through the active browser session instead of direct credential theft at execution time.

## Defender heuristics
- Treat unexpected Gmail API / OAuth activity from user accounts as endpoint-compromise telemetry, not only SaaS misconfiguration.
- Correlate Google Workspace OAuth grants and mailbox API access with endpoint launches of headless Chrome/Edge and DevTools remote-debugging ports.
- Hunt for signed-binary sideload chains using `BDSubWiz.exe`, `VSTestVideoRecorder.exe`, or `GoogleDesktop.exe` with suspicious adjacent DLLs.
- Review scheduled tasks and service names that impersonate security tooling.
- Preserve browser profile copies, scheduled-task XML, sideloaded DLLs, command lines, OAuth grant logs, and mailbox audit logs before remediation.

## Related pages
- [Umbrij](../tools/umbrij.md)
- [ToddyCat Umbrij Gmail OAuth operation](../ops/toddycat-umbrij-gmail-oauth.md)

## Sources
- Kaspersky Securelist: https://securelist.com/toddycat-apt-umbrij-tool-and-oauth/120251/
- The Hacker News: https://thehackernews.com/2026/07/toddycat-linked-umbrij-malware-abuses.html
