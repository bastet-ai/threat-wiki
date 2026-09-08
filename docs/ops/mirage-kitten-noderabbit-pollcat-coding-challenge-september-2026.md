# Mirage Kitten NodeRabbit / PollCat coding-challenge campaign

## Summary
Kaspersky GReAT disclosed on **September 1, 2026** a new **Mirage Kitten** operation using two previously undocumented, cross-platform implants — **NodeRabbit** (Node.js) and **PollCat** (JavaScript) — the group's first publicly documented Node.js/JavaScript-based malware, a departure from its usual native DLL-search-order-hijacking payloads. Both are delivered through **trojanized "coding challenge" archives** hosted on **Amazon S3** and reached via recruiter-themed outreach on LinkedIn and similar platforms, targeting **aviation and FinTech** organizations across the **Middle East and Africa** (Egypt, Ethiopia, Afghanistan observed; ZIP submissions also from India, Türkiye, Israel, Iraq, Germany, Ireland).

The durable signal: a recruiter posing as a hiring manager pressures a developer to clone and run a "technical assessment" project whose one altered file silently launches a cross-platform RAT that persists through developer-workflow mechanisms (fake VS Code extensions, Git hook injection, per-OS scheduled tasks/cron/LaunchAgents).

## Tags
- ops
- operation
- campaign
- Mirage Kitten
- UNC1549
- Smoke Sandstorm
- Nimbus Manticore
- NodeRabbit
- PollCat
- Node.js
- JavaScript
- cross-platform
- Windows
- Linux
- macOS
- WSL
- aviation
- FinTech
- Middle East
- Africa
- Egypt
- Ethiopia
- Afghanistan
- recruiter impersonation
- fake coding challenge
- S3 lure hosting
- MQTT
- WebSocket
- Git hook persistence
- VS Code extension persistence
- espionage
- targeted operations

## Why this matters
- **New implant language.** NodeRabbit and PollCat are Mirage Kitten's first Node.js/JavaScript implants, replacing the native DLL-search-order-hijacking malware the group is known for. A single cross-platform codebase now covers Windows, Linux, macOS, and WSL, blending naturally into developer workstations.
- **Delivery is social, not exploit-based.** Initial access is recruiter-themed social engineering — a "technical assessment" a candidate is asked to run — consistent with the group's historical fake-recruiting tradecraft. The lure is a time-limited coding challenge with an OTP gate that accelerates execution.
- **Persistence rides developer workflows.** Variant 3 of NodeRabbit and PollCat persist through mechanisms a defender may not associate with malware: a fake "GitHub Copilot Helper" VS Code extension, `# shepherd-persist` lines injected into `.git/hooks/post-merge` / `post-checkout`, and per-OS scheduled tasks / `@reboot` cron / LaunchAgents.
- **C2 blends into enterprise traffic.** Both use Azure Websites subdomains (often incorporating the target organization's name) plus Cloudflare-backed domains, making outbound traffic resemble normal business traffic from an employee machine. PollCat's HTTP-400-as-success handshake matches the historical Retrograde/MiniFast flow.

## Reported chain
1. **Lure.** A recruiter persona on LinkedIn (or a job-search platform) offers a targeted developer in aviation/FinTech a time-limited "coding challenge" / technical assessment, delivered as a ZIP on **Amazon S3** (`oracle-challenge.s3[.]us-east-1.amazonaws[.]com`).
2. **Execution.** The developer clones the project and runs `npm i && node index.js`. One file (`server.js` for NodeRabbit; `app.js`→`requireAuth.js`→`requireObjects.js` for PollCat) silently starts the implant as a detached process.
3. **OTP / urgency (PollCat).** The challenge demands a six-digit recruiter-supplied OTP and a one-hour window; codes are forwarded to `lifespotify[.]com`. PollCat registers with C2 regardless of whether the OTP is entered.
4. **C2 registration.** NodeRabbit beacons to a chain of Azure/Cloudflare C2 hosts; PollCat registers via `POST /beacon` and expects an **HTTP 400** carrying a `socketId`.
5. **Persistence + tasking.** Per-OS persistence is installed; operators issue recon, file, process, and (for NodeRabbit variant 3) Outlook-address-harvesting and developer-workflow-persistence commands.

## NodeRabbit (Node.js RAT)
- Three variants observed; the first is launched through the trojanized `colorized_terminal` package, the second and third through the trojanized `pretty-log` package.
- Variant 1 binds `127.0.0.1:48739` for single-instance control; variant 2 adds anti-analysis + corporate-proxy (NTLM/Negotiate via `curl.exe --proxy-anyauth`) + host-specific port `41984 + (hex4(agent_id) mod 5000)`; variant 3 changes C2 to `/sdk/v2/*` endpoints and adds 12 commands (23 total) plus developer-workflow persistence (fake "GitHub Copilot Helper" VS Code extension, `.git/hooks` `# shepherd-persist` injection).
- C2: Azure-hosted chains (`plugplay`/`rgbteller`/`wslwebui` Azure for v1; `visitfinancedentists[.]com` + `healthcomfsdpower[.]com` + Azure for v3).
- Details: [NodeRabbit](../tools/noderabbit.md).

## PollCat (JavaScript RAT)
- Delivered inside `RankChallenge-react`; registers via `POST /beacon` expecting **HTTP 400** with a `socketId`; beacons every 2 minutes ± 5 s jitter.
- Persists as `NetSync_<username>` (Windows), `~/.node_packages` + cron (`@reboot` + daily 09AM) on Linux, and `com.harsh.requireobject.plist` on macOS.
- C2: `sahi-finance[.]com`, `gamebarapp.azurewebsites[.]net`, `gamebarappinformation.azurewebsites[.]net`.
- 22 declared commands (3 unimplemented), including `EVAL_JS`, `SYSTEM_CHECK` (lists 24 hardcoded security-vendor folder names), and chunked file transfer.
- Details: [PollCat](../tools/pollcat.md).

## Attribution
Kaspersky attributes this to **Mirage Kitten** with high confidence on:
- Structural similarity to the **Retrograde/MiniFast** native DLL backdoor (MD5 `810F8E3B88EB05F710C09552941D6F56`).
- Shared C2 handshake: HTTP 400 treated as success, `socketId` session token, `GET /gate/fetch?token=` vs `GET /agent/poll?token=`.
- Identical beacon defaults: poll **120,000 ms**, jitter **5,000 ms**, retry **60,000 ms**.
- Shared proxy-auth design (corporate NTLM/Negotiate).
- Victimology (Africa + Middle East, aviation/FinTech focus) and infrastructure (Azure Websites + Cloudflare; S3 lure hosting, a shift from the group's prior onlyoffice.com lure hosting).

## Victimology
- Confirmed victims: **fintech** and **aviation/aerospace** organizations in the **Middle East and Africa** — specifically **Egypt, Ethiopia, and Afghanistan**.
- ZIP archives containing NodeRabbit/PollCat were also submitted to an online multi-scanner from **India, Türkiye, Israel, Iraq, Germany, and Ireland**.
- This is observed scope, not a complete victim list.

## Public infrastructure
### C2 / lure
- Lure host: `oracle-challenge.s3[.]us-east-1.amazonaws[.]com`
- NodeRabbit C2: `naturalapplication`/`retaildemo`/`tubitak`/`rgbteller`/`wslwebui`/`plugplay`/`crossdwm`/`wdisystem`/`wslmenus`/`dnshnsdev`/`hpjumpsrv`/`storview`/`greenyjsgfd`/`helptellerbls`/`timedrv`/`userwellgtfs`/`hecowime-aqdphyd4bbdef6es.westeurope-01.azurewebsites[.]net`, `msmanagementgrp[.]com`, `msmanagementgrpmedia[.]com`, `healthcomfsdpower[.]com`, `visitfinancedentists[.]com`, `kyrasey-f8hfexa5cqamh7fk.westeurope-01.azurewebsites[.]net`
- PollCat C2: `sahi-finance[.]com`, `gamebarapp.azurewebsites[.]net`, `gamebarappinformation.azurewebsites[.]net`, `lifespotify[.]com`

### Additional infrastructure (pattern-linked)
- `healthful-hub[.]com`, `neumedicahealthcare[.]com`, `optimumhealthcredit[.]com`, `healthfullyrecipes[.]com`, `refreshhealthandwellness[.]com`, `healthvitalitycare[.]com`, `aceofspadesmanagement[.]com`, `glmediaagency[.]com`, `digimediaskill[.]com`, `healthyweightplan[.]com`, `mens-health-online[.]com` (NameCheap; ~11 additional assets attributed to the same group).

## Lure / archive hashes (MD5)
- `CBAAF0900A13F28E380F49ADECEC932C` FrontEnd-Task.zip
- `1EA83E4E4592B01E4ACAB63EB867BEE5` Front-Technical-Challenge.zip
- `366515822D5AC1CC500711EF57A2E32E` Task-FullStack.zip
- `CF449F1992C2819E62AC44A0B06AC2E7` fullstack-1536.zip
- `E95A4366686E3F786EA3C056FAB5B0DA` webapp76592.zip
- `DE5AF16A3757EF700B01DC34D67079AE` webapp76531.zip
- `BE086789568441D0D7E4679AEE51F566` challenges-17831.zip
- `E259C5EDF158AAC4CFE14F77DDD0B196` challenges-17832.zip
- `291AC3ABE73C5158E59A437B75D5F0AA` Project-1802.zip
- `0962F56D7EC69F4F2A0162DCBE22116B` Case-34234.zip
- `795E053A990A1569FFDCB57F48F6D085` RankChallenge-react-6uJSX3-main.zip

## Defender focus
- **Scope the recruiting surface.** Treat recruiter DMs that send a "time-limited coding challenge" or "technical assessment" ZIP (especially on S3 or third-party file hosts) to developers in aviation/FinTech/gov as high risk; block or sandbox execution of unvetted assessment projects.
- **Hunt the tell, not the package.** Alert on a `node`/`node.exe` (or renamed copy) spawning from a project's `node_modules/.cache/`, a root `package.json` named `ctf-server`, a recruiter-supplied OTP flow, or a fake "GitHub Copilot Helper" VS Code extension.
- **Inspect developer-workflow persistence.** Search repositories for `# shepherd-persist` in `.git/hooks/post-merge` / `post-checkout`; enumerate VS Code extensions (especially unsigned "Copilot Helper"-style ones); review `NetSync_<user>` scheduled tasks, `~/.node_packages`, `com.harsh.requireobject.plist`, and `@reboot`/daily cron.
- **C2 telemetry.** Correlate outbound HTTPS to the Azure/Cloudflare C2 domains above; for PollCat, a **non-2xx (HTTP 400) JSON response carrying a `socketId`** is a strong C2-protocol indicator.
- **Preserve the lure.** Keep the original ZIP, the altered source file, and the recruiter conversation; the archive + OTP flow is the most reliable attribution evidence.

## Related pages
- [Mirage Kitten](../actors/mirage-kitten.md)
- [NodeRabbit](../tools/noderabbit.md)
- [PollCat](../tools/pollcat.md)
- [Mirage Kitten NightLedger / BridgeHead / ArcBridge campaign](mirage-kitten-nightledger-bridgehead-arcbridge.md)
- [Node.js runtime as a malware-delivery channel](../patterns/nodejs-runtime-malware-delivery-symantec-september-2026.md)

## Sources
- Kaspersky GReAT, September 1, 2026: [Mirage Kitten targeting aviation and FinTech sectors across the Middle East and Africa with a new malware set](https://securelist.com/mirage-kitten-new-backdoors-noderabbit-pollcat/121244/)
