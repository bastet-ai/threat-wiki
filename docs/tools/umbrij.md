# Umbrij

## Summary
**Umbrij** is a .NET tool publicly documented by Kaspersky in June 2026 and attributed to **ToddyCat**. It automates access to corporate Gmail correspondence by abusing an existing authenticated Chromium browser session, the Chrome/Edge DevTools remote-debugging interface, and OAuth 2.0 authorization flows.

Kaspersky calls the technique **Shadow Token via Remote Debug (STRD)**: Umbrij launches Chrome or Edge in headless mode against a copied user profile, opens a remote debugging port, obtains an OAuth authorization code in the context of the victim's active Google session, exchanges it for an access token, and then accesses Gmail resources through the Google API.

## Tags
- tools
- malware
- credential theft
- email theft
- OAuth abuse
- Gmail
- Google API
- Chromium
- Chrome
- Microsoft Edge
- remote debugging
- DevTools
- headless browser
- DLL sideloading
- .NET
- ConfuserEx
- ToddyCat
- Umbrij
- STRD

## Why this matters
- The attack does not need the victim's Google password at execution time if the browser profile still contains an active Gmail session.
- OAuth access through the Google API can look different from traditional mailbox theft or browser-cookie collection, so defenders need SaaS/OAuth telemetry in addition to endpoint alerts.
- The browser is launched in headless mode against a copied profile, keeping artifacts out of the user's normal visible browser history.
- Kaspersky observed the actor disguising execution as a fake `KasperskyEndpointSecurityEDRAvp` scheduled task and loading the tool through legitimate signed binaries vulnerable to DLL sideloading.

## Execution chain
1. A scheduled task named `KasperskyEndpointSecurityEDRAvp` launches a digitally signed executable. Kaspersky says its products do not create a task with that name.
2. The signed executable sideloads the malicious Umbrij DLL.
3. Umbrij locates and copies browser profile material into a `BackupFiles` directory.
4. It launches Google Chrome, Microsoft Edge, or both with a template similar to `--user-data-dir=<BackupFiles> --remote-debugging-port=<port> --profile-directory=Default --headless https://www.google.com/`.
5. It connects to the browser through the DevTools remote-debugging port using Puppeteer Sharp.
6. It drives the browser through the Google OAuth flow, obtains an authorization code in the victim session, exchanges it for an OAuth access token, and uses the Google API to access Gmail resources.

## Reported sideload hosts
Kaspersky reported three legitimate binaries used to load different Umbrij versions:

| Host binary | Sideloaded DLL name | Notes |
| --- | --- | --- |
| `BDSubWiz.exe` | `log.dll` | Bitdefender ConnectAgent Submission Wizard component |
| `VSTestVideoRecorder.exe` | `Microsoft.VisualStudio.QualityTools.VideoRecorderEngine.dll` | Visual Studio test video-recorder component |
| `GoogleDesktop.exe` | `GoogleServices.dll` | Discontinued Google Desktop Search binary |

## Reported command / artifact pivots
Treat these as public pivots, not a complete detection set.

- Scheduled task: `KasperskyEndpointSecurityEDRAvp`.
- Example launch path: `C:\Users\Public\BDSubWiz.exe`.
- Example parameters: `-regex`, `-deepsearch`, `-user`, `-runas-currentuser`.
- Browser switches: `--user-data-dir`, `--remote-debugging-port`, `--profile-directory=Default`, `--headless`.
- Copied-profile directory name: `BackupFiles`.
- Kaspersky detections: `HEUR:Trojan-PSW.MSIL.Umbrij.gen`, `HEUR:Trojan.MSIL.Agent.gen`, `HEUR:Trojan-PSW.MSIL.Agent.gen`.

## Defender heuristics
- Alert on Chrome or Edge launched headless with `--remote-debugging-port` from unusual parent processes, especially from user-writable directories or after signed-binary sideload execution.
- Hunt for `BDSubWiz.exe`, `VSTestVideoRecorder.exe`, or `GoogleDesktop.exe` running outside expected install paths with adjacent suspicious DLLs named `log.dll`, `Microsoft.VisualStudio.QualityTools.VideoRecorderEngine.dll`, or `GoogleServices.dll`.
- Review scheduled tasks for security-vendor lookalike names, especially `KasperskyEndpointSecurityEDRAvp`.
- Correlate endpoint browser-debugging events with Google Workspace OAuth grants, Gmail API calls, unexpected third-party access, and mailbox-access anomalies.
- If confirmed, revoke suspicious OAuth grants and browser sessions, rotate credentials where needed, preserve the copied browser profile directory, and scope for ToddyCat email-access tooling.

## Related pages
- [ToddyCat](../actors/toddycat.md)
- [ToddyCat Umbrij Gmail OAuth operation](../ops/toddycat-umbrij-gmail-oauth.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)

## Sources
- Kaspersky Securelist: [https://securelist.com/toddycat-apt-umbrij-tool-and-oauth/120251/](https://securelist.com/toddycat-apt-umbrij-tool-and-oauth/120251/)
- The Hacker News: [https://thehackernews.com/2026/07/toddycat-linked-umbrij-malware-abuses.html](https://thehackernews.com/2026/07/toddycat-linked-umbrij-malware-abuses.html)
