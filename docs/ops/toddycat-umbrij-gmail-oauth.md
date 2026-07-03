# ToddyCat Umbrij Gmail OAuth operation

## Summary
Kaspersky reported on June 30, 2026 that **ToddyCat** developed **Umbrij**, a .NET tool for covert access to corporate Gmail correspondence. The operation abuses a victim's already-authenticated Chromium browser profile, the browser DevTools remote-debugging interface, and Google's OAuth flow to obtain an access token and then reach Gmail resources through the Google API.

Kaspersky named the technique **Shadow Token via Remote Debug (STRD)**. The durable defender lesson is that mailbox compromise can originate from endpoint browser-session control and appear as API/OAuth activity rather than classic password theft or direct webmail scraping.

## Tags
- ops
- operation
- ToddyCat
- Umbrij
- STRD
- Gmail
- Google API
- OAuth abuse
- email theft
- browser session abuse
- Chromium
- Chrome
- Microsoft Edge
- remote debugging
- headless browser
- DLL sideloading
- .NET malware
- ConfuserEx
- espionage

## Why this matters
- STRD converts a local browser-session compromise into cloud-mailbox API access.
- The user may not see the activity because Umbrij copies the browser profile and launches the browser in headless mode.
- Detection requires joining endpoint process telemetry, browser command-line monitoring, OAuth grant review, and Google Workspace mailbox audit data.
- The operation demonstrates an actor adapting email-access tooling after prior approaches became easier for EPP/EDR to detect.

## Public attack chain
1. The actor establishes execution on the victim host and creates/uses a scheduled task named `KasperskyEndpointSecurityEDRAvp` to masquerade as security software.
2. The task launches a legitimate signed executable vulnerable to DLL sideloading.
3. Umbrij, a ConfuserEx-obfuscated .NET DLL, is loaded through one of several reported host binaries.
4. The tool copies browser profile material into a `BackupFiles` directory.
5. It launches Chrome and/or Edge with `--user-data-dir=<copied profile>`, `--remote-debugging-port=<port>`, `--profile-directory=Default`, and `--headless`.
6. Through Puppeteer Sharp and the DevTools protocol, Umbrij drives the OAuth authorization flow in the context of the still-authenticated Google session.
7. The obtained OAuth authorization code is exchanged for an access token, enabling Gmail-resource access through the Google API.

## Reported sideloading pivots
| Host binary | DLL name | Context |
| --- | --- | --- |
| `BDSubWiz.exe` | `log.dll` | Bitdefender ConnectAgent Submission Wizard component |
| `VSTestVideoRecorder.exe` | `Microsoft.VisualStudio.QualityTools.VideoRecorderEngine.dll` | Visual Studio test video-recorder component |
| `GoogleDesktop.exe` | `GoogleServices.dll` | Discontinued Google Desktop Search binary |

## Detection and response guidance
- Alert on Chrome/Edge launched with both `--headless` and `--remote-debugging-port`, especially when the parent process is a sideloadable utility or runs from `C:\Users\Public` / another user-writable path.
- Hunt for `BackupFiles` browser-profile copies and for browser history or profile artifacts outside normal Chrome/Edge profile directories.
- Review scheduled tasks for `KasperskyEndpointSecurityEDRAvp` and other security-vendor lookalikes created outside legitimate deployment tooling.
- Monitor Google Workspace for unexpected OAuth grants, Gmail API access, mailbox enumeration, message reads, or third-party application access following suspicious endpoint events.
- Revoke suspicious OAuth grants and browser sessions, rotate credentials as needed, and preserve endpoint plus Workspace audit evidence before cleanup.

## Related pages
- [ToddyCat](../actors/toddycat.md)
- [Umbrij](../tools/umbrij.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)

## Sources
- Kaspersky Securelist: https://securelist.com/toddycat-apt-umbrij-tool-and-oauth/120251/
- The Hacker News: https://thehackernews.com/2026/07/toddycat-linked-umbrij-malware-abuses.html
