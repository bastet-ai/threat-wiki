# UAC-0145 ClickFix, SMARTAXE, and COWARDDUCK campaign

## Summary
CERT-UA reported a 2026 expansion of **UAC-0145**, which it tracks as a subcluster of **UAC-0002 / Sandworm / APT44 / Seashell Blizzard**. During spring and summer 2026, the cluster used fake-CAPTCHA **ClickFix** pages on compromised websites to make visitors run PowerShell, alongside Android APK lures delivered through messaging applications.

The operation is notable for combining compromised web infrastructure, traffic filtering, an Ethereum smart-contract dead drop, Windows reconnaissance/loaders/backdoors, and an Android backdoor. CERT-UA analyzed the ClickFix implementation on more than ten compromised sites during June and July 2026.

## Tags
- ops
- operations
- UAC-0145
- UAC-0002
- Sandworm
- APT44
- Seashell Blizzard
- Russia
- GRU
- Ukraine
- ClickFix
- fake CAPTCHA
- compromised websites
- EtherHiding
- Ethereum
- Android
- Signal
- PowerShell
- VBScript
- SMARTAXE
- GHETTOVIBE
- SCOUTCURL
- FREAKYPOLL
- FLUIDLEECH
- LOADLOOP
- COWARDDUCK

## Initial-access evolution
CERT-UA describes three durable access patterns associated with the cluster:

1. **Trojanized software from torrent trackers:** users downloaded modified Windows or Microsoft Office installers with embedded backdoors. CERT-UA says at least one such endpoint later enabled presence and lateral movement before a destructive attack against a Ukrainian central-government body.
2. **Messaging-app social engineering:** operators contacted targets, particularly military personnel, through Signal and offered purported antivirus/security tools. Some conversations were prolonged and included offers of payment for following the instructions. Earlier tooling included KALAMBUR, SUMBUR, and TAMBUR, with OpenSSH and Tor used to expose local ports such as 445, 3389, and 22.
3. **Compromised-site ClickFix:** fake CAPTCHAs instructed visitors to paste and run PowerShell. One observed command wrote a VBS file into the Startup folder, providing login-time execution.

The Android branch used APK files disguised as security software and sent through messaging applications.

## 2026 ClickFix and malware chain
- **SMARTAXE** dynamically modifies compromised pages to show attacker content. It can retrieve a remote domain through an Ethereum `eth_call` against a contract address and function selector embedded in the script.
- **Cloaking.House** filtering controls which visitors receive the remote page, iframe, redirect, or injected CAPTCHA.
- **GHETTOVIBE** is a VBS payload observed in the Startup folder.
- **SCOUTCURL** is a PowerShell reconnaissance script that collects host characteristics, installed applications, files, and browser data to help operators assess the target.
- **FLUIDLEECH** and **LOADLOOP** are loaders. FLUIDLEECH masqueraded as antivirus-removal software.
- **FREAKYPOLL** is a Python backdoor distributed as compiled `.pyc` bytecode.
- **COWARDDUCK** is an Android backdoor that collects device details, contacts, real-time location, and selected documents and archives from common user directories. It uploads files through Dropbox and can obtain commands or data through objects on legitimate services, including Steam Community, with DuckDuckGo's proxy in the communication path.

## Detection pivots
### Windows and web
- PowerShell launched after a browser visit or fake-CAPTCHA prompt, especially when it writes `.vbs` files under `%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup`.
- `%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Copilot Agent.vbs` and `%LOCALAPPDATA%\\SystemHelper\\python\\`.
- Unauthorized JavaScript such as `wp-header.js`, traffic-filtering code, iframe/redirect logic, or Ethereum JSON-RPC `eth_call` requests in website content.
- Unexpected requests from non-wallet websites to Ethereum RPC services followed by retrieval from newly resolved domains.
- Python bytecode named `update.cpython-314.pyc`, fake ESET removal utilities, or follow-on PowerShell reconnaissance from user workstations.

### Android
- Sideloaded APKs presented as antivirus/security tools through Signal or another messenger.
- A sideloaded app reading contacts, location, and broad document/archive extensions, then contacting Dropbox, Steam Community, `images.stockmemory` hosts, or `proxy.duckduckgo.com` outside expected user activity.

### Selected public network indicators
- `update-requirements[.]com` — FREAKYPOLL
- `entouchnetworks[.]com` — SMARTAXE
- `static[.]diagnostics-monitoring[.]com` and `static[.]opennetworkconnect[.]com` — GHETTOVIBE
- `softupdater[.]org`, `soft[.]softchecker[.]org`, and `pack[.]softpacker[.]org` — FLUIDLEECH
- `smartlinkupload[.]com`, `delta[.]smartlinkupload[.]com`, `offlce366[.]com`, and `365softupdate[.]com`

CERT-UA labels `images.stockmemory.site`, `images.stockmemory.space`, and `proxy.duckduckgo.com` as legitimate services used in the COWARDDUCK chain; do not block or attribute them without contextual validation.

## Defender guidance
- Treat a website serving this CAPTCHA as compromised. Preserve the CMS, plugins, web shells, modified scripts/pages, access logs, administrator activity, and hosting-control-plane evidence before cleanup.
- Hunt beyond known domains: prioritize the browser-to-PowerShell sequence, Startup-folder writes, suspicious Ethereum RPC resolution, and newly introduced site scripts.
- For affected endpoints, preserve PowerShell history, browser history/cache, Startup content, Python bytecode, messenger artifacts, and memory. Scope credentials and Signal/WhatsApp key material after containment.
- On Android, remove sideloaded security tools only after preserving the APK, app data, network records, permissions, and messaging-delivery evidence. Review Dropbox and Steam access context rather than blocking legitimate services globally.
- Use CERT-UA's full indicator bundle for hash-level hunting; the behavioral pivots above are more resilient to payload rotation.

## Related pages
- [UAC-0145](../actors/uac-0145.md)
- [TELEPUZ ClickFix / VIDAR campaign](telepuz-clickfix-vidar-campaign.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [Russian intelligence Signal backup-key phishing](russian-intelligence-signal-backup-key-phishing.md)

## Sources
- CERT-UA: [Initial compromise vectors of UAC-0145 as of July 2026](https://cert.gov.ua/article/6318437)
- The Hacker News summary: [UAC-0145 Uses ClickFix CAPTCHAs to Infect Ukrainian Devices with Malware](https://thehackernews.com/2026/07/uac-0145-uses-clickfix-captchas-to.html)
