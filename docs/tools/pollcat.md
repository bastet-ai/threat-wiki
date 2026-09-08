# PollCat

## Summary
**PollCat** is a cross-platform remote access trojan written in **JavaScript** (Node.js), attributed by Kaspersky GReAT to **Mirage Kitten**. It targets **Windows, Linux, and macOS**. It was discovered while tracking NodeRabbit infections and is Kaspersky's first public report of a JavaScript-based (as opposed to Node.js CJS-module) Mirage Kitten implant. It is delivered inside a **trojanized React "coding challenge"** and registers with its C2 using an unusual **HTTP 400** response as the success signal.

## Tags
- tool
- tools
- PollCat
- Mirage Kitten
- UNC1549
- JavaScript
- Node.js
- cross-platform
- Windows
- Linux
- macOS
- RAT
- backdoor
- trojanized coding challenge
- React
- OTP lure
- JWT
- beacon
- HTTP 400 handshake
- Azure Websites C2

## Delivery
- Delivered inside **`RankChallenge-react`** (a React code-fixing challenge presented as a time-limited developer assessment), e.g. `RankChallenge-react-6uJSX3-main.zip` (MD5 `795E053A990A1569FFDCB57F48F6D085`), hosted on **Amazon S3** (`oracle-challenge.s3[.]us-east-1.amazonaws[.]com`) and reached through recruiter-themed outreach.
- The root `package.json` is named **`ctf-server`**; the backend prints `CTF server running`; the frontend uses several `ctf-*` storage keys; the tutorial references `path/to/ctf`. These labels, together with README/challenge mismatch, are consistent with an AI-assisted or template-generated project.
- Running the project invokes **`npm i && node index.js`**, which starts the local application and opens the challenge in the browser.
- A bundled PDF tutorial tells the target to click **Continue**, enter a **six-digit OTP** supplied by the recruiter, and complete the challenge within a **one-hour session**; the login page claims codes rotate every 30 seconds. The expiring code + countdown create urgency to accelerate infection.
- The bundled **`.env`** file contains the **JWT signing secret**, the **OTP service URL**, and the **OTP client ID**.

## Lure / OTP behavior
- Submitted OTP codes are forwarded to an attacker-managed domain registered late June 2026: `https://lifespotify[.]com/api/users/b879746e-fed9-4211-a6da-4d8223681267/otp/validate`.
- **PollCat starts independently of the OTP flow**: during app startup, `app.js` loads `requireAuth.js`, which imports and immediately starts the malicious `requireObjects.js` component. C2 registration and command polling can begin **before** the user enters an access code.
- A failed OTP validation blocks the protected challenge features, but PollCat keeps running in the background. A successful validation issues a **JWT** and spawns another worker that starts an additional PollCat instance; the first authenticated request triggers the persistence attempt.

## Persistence (per platform, triggered on first valid-JWT request)
| Platform | Mechanism |
| --- | --- |
| Windows | Writes `package.json` + `requireObject.js` to `%APPDATA%\Microsoft\Network`, runs `npm install`, creates a daily task **`NetSync_<username>`** at 09AM that runs the worker with Node.js. |
| Linux | Writes the worker to `~/.node_packages`, runs `npm i`, appends both a daily 09AM cron line and an `@reboot` line. |
| macOS | Same `~/.node_packages` copy + cron path; creates and loads `~/Library/LaunchAgents/com.harsh.requireobject.plist` with RunAtLoad and a daily 09AM trigger. |

## C2 and commands
- Host identifier: `129--<hostname>`.
- Iterates over a C2 chain until registration succeeds: `https://sahi-finance[.]com`, `https://GamebarAppinformation[.]azurewebsites[.]net`, `https://GamebarApp[.]azurewebsites[.]net`.
- Registration: `POST /beacon` with `{"clientId":"<client-id>","type":"poll","pcName":"<hostname>","userName":"<username>"}`.
- **Unusual success signal:** on successful registration PollCat expects an **HTTP 400** (not 200) containing `{"socketId":"<socket-id>","pollInterval":<ms>,"jitterTime":<ms>}`. This mirrors the Retrograde/MiniFast handshake that also treats HTTP 400 as success — a key attribution marker.
- Post-registration endpoints: `POST /gate/hello` (host/user/domain/OS + privilege level), `GET /gate/fetch?token=<socketId>` (poll commands), `POST /gate/submit` (Base64 command results), `GET /vault/<uuid>` (download C2 file), `PUT /vault/push/` (upload local file/chunk), `POST /gate/track` (chunk-upload progress).
- Default beacon: **every two minutes** with up to **five seconds of jitter**; commands and results are stored as little-endian binary records carried as Base64 text.
- **22 declared commands, 3 unimplemented** (`0XA1` WS_DOWNLOAD, `0xB0` REQUEST_ELEVATION, `0xB1` PERSIST). Notable implemented commands: `EVAL_JS` (run C2-supplied JavaScript with full Node.js module/process/network access), `RUN`/`RUN_HIDDEN`, `SYSTEM_CHECK` (process + software inventory; lists `%Program Files`, `%LOCALAPPDATA%`, `%APPDATA%`, `%APPDATA%\Microsoft\Outlook`, `%LOCALAPPDATA%\Microsoft\Olk\Attachments`, `%USERPROFILE%\Documents`, and any folder matching 24 hardcoded security-vendor strings — Google, Microsoft, Palo Alto Networks, Cisco, VMware, Fortinet, Citrix, CheckPoint, Juniper Networks, LogMeIn, Sophos, Symantec, Trend Micro, McAfee, Kaspersky Lab, ESET, Bitdefender, Avast Software, CrowdStrike, SentinelOne, Malwarebytes, BraveSoftware, Tencent, Naver), file transfer (UPLOAD/DOWNLOAD/CHUNKED_DOWNLOAD from the C2 perspective), `ZIP`, `MKDIR`, `RUNDLL`.
- `SYSTEM_CHECK` results are sent as JSON to `POST /api/system-details/result`.

## Attribution markers
- Identical beacon timing to Retrograde/MiniFast: poll interval **120,000 ms (0x1D4C0)**, jitter **5,000 ms (0x1388)**, retry timeout **60,000 ms (0xEA60)**.
- Shared HTTP-400-as-success handshake and `socketId` session-token flow.
- Declares `REQUEST_ELEVATION` (0xB0) and `PERSIST` (0xB1) but leaves them unimplemented, whereas MiniFast/Retrograde implement both (0xB0 = UAC elevation, 0xB1 = `WindowsSecurityUpdate` scheduled task).

## Public indicators
### Lure / archive
- `RankChallenge-react-6uJSX3-main.zip` MD5 `795E053A990A1569FFDCB57F48F6D085`
- Lure host: `oracle-challenge.s3[.]us-east-1.amazonaws[.]com`

### C2 domains
- `sahi-finance[.]com` (NameCheap), `gamebarapp.azurewebsites[.]net`, `gamebarappinformation.azurewebsites[.]net` (MarkMonitor/Azure AS8075)
- OTP/attacker domain: `lifespotify[.]com` (Dynadot)

### Host artifacts
- `%APPDATA%\Microsoft\Network\{package.json,requireObject.js}` (Windows)
- `~/.node_packages` (Linux/macOS)
- `~/Library/LaunchAgents/com.harsh.requireobject.plist` (macOS)
- Scheduled task `NetSync_<username>` (Windows)

## Detection pivots
- A React/Node "coding challenge" or "tech assessment" archive that runs `npm i && node index.js`, has a root `package.json` named `ctf-server`, and requires a recruiter-supplied OTP.
- Outbound HTTPS to `sahi-finance[.]com` / `gamebarapp*` Azure domains, or a **non-2xx (HTTP 400) JSON response containing a `socketId`** — a strong C2-protocol tell.
- The `129--<hostname>` beacon identifier.
- `~/.node_packages`, `com.harsh.requireobject.plist`, or a `NetSync_<username>` scheduled task.

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [Mirage Kitten NodeRabbit / PollCat coding-challenge campaign](../ops/mirage-kitten-noderabbit-pollcat-coding-challenge-september-2026.md)
- [NodeRabbit](noderabbit.md)

## Sources
- Kaspersky GReAT, September 1, 2026: [Mirage Kitten targeting aviation and FinTech sectors across the Middle East and Africa with a new malware set](https://securelist.com/mirage-kitten-new-backdoors-noderabbit-pollcat/121244/)
