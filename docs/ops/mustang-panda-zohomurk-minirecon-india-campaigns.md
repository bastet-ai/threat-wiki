# Mustang Panda ZOHOMURK / MINIRECON India campaigns

## Summary
Acronis Threat Research Unit reported two concurrent **Mustang Panda** espionage campaigns against Indian government targets, including the hydropower sector and government entities tied to India–Taiwan cooperation agreements. The campaigns used hydropower- and memorandum-of-understanding-themed archives to deliver **SHARDLOADER**, which then deployed two newly described implants: **MINIRECON** and **ZOHOMURK**.

The durable defender signal is the combination of China-aligned targeting, legitimate signed-binary DLL sideloading, hidden DLLs inside spear-phishing archives, scheduled-task persistence, and cloud-service C2. ZOHOMURK is notable because it uses **Zoho WorkDrive** for command-and-control, victim foldering, tasking, and exfiltration, while MINIRECON communicates over WebSocket to attacker infrastructure and shares architectural overlap with Mustang Panda's TONESHELL tooling.

## Tags
- ops
- operations
- Mustang Panda
- China-nexus
- espionage
- India
- Indian government
- hydropower
- energy sector
- Taiwan
- Zoho WorkDrive
- cloud service abuse
- SHARDLOADER
- MINIRECON
- ZOHOMURK
- TONESHELL
- DLL sideloading
- Solid PDF Creator
- SolidPDFCreator.dll
- Project Proposal.exe
- Hydropower Cooperation Project Proposal.zip
- scheduled task persistence
- SolidPDFPcl2Bmp
- WebSocket C2
- OAuth token abuse
- data exfiltration
- CERT-In

## Why this matters
- Acronis says it observed active beaconing from multiple compromised Indian government systems between **June 12 and June 22, 2026**, including systems associated with senior administrative personnel, and coordinated relevant findings with **CERT-In**.
- The campaign blends with local context: lure material referenced hydropower cooperation and India–Taiwan government agreements, while Zoho WorkDrive is a legitimate platform with adoption in the Indian government sector.
- ZOHOMURK turns a trusted SaaS API into the operator's C2 and exfiltration layer. Blocking only raw IPs or unfamiliar domains will miss activity that authenticates to `accounts.zoho.com` and calls Zoho WorkDrive APIs.
- The loader chain uses signed legitimate executables and hidden DLLs, reducing user suspicion and weakening detection that focuses only on unsigned launchers.
- Acronis attributes the activity to Mustang Panda with high confidence based on deployment patterns, operational characteristics, code overlap with TONESHELL, and recurring infrastructure / tooling choices.

## Campaign chain
1. Victims receive compressed archives with hydropower or government-cooperation themes, including **`Hydropower Cooperation Project Proposal.zip`**.
2. The archive contains a legitimate signed Solid PDF Creator executable, such as **`Project Proposal.exe`**, alongside a hidden malicious **`SolidPDFCreator.dll`**.
3. When the signed executable starts, Windows loads the attacker-controlled DLL from the same directory. The malicious DLL exports expected functions such as `GetSPApp`, allowing **SHARDLOADER** to run in the context of the trusted application.
4. SHARDLOADER decrypts and launches follow-on implants. Acronis tracks the two loader branches as SHARDLOADER v1.0 and v1.1.
5. One branch deploys **MINIRECON**, a TONESHELL-derived reconnaissance / implant component; the other deploys **ZOHOMURK**, which registers victims and polls for tasks through Zoho WorkDrive.

## Malware and infrastructure details

### SHARDLOADER
- DLL-based loader delivered through spear-phishing archives.
- Relies on DLL sideloading from legitimate Solid PDF Creator components.
- Acronis describes two variants tied to the two campaign branches.

### MINIRECON
- Newly identified implant with architectural and functional similarity to **TONESHELL**, including API hashing, command handling, encryption routines, and anti-analysis techniques.
- Acronis observed MINIRECON communicating with **`couldinstallup[.]com`** over WebSocket on TCP/443.
- The domain reportedly resolved to **`188.208.141[.]177`**, hosted by Leapswitch Networks in India, during Acronis' investigation.

### ZOHOMURK
- Exposes `CTXMUI_ParseArgvA` as its primary export / entry point.
- Uses timing checks with `QueryPerformanceCounter` as an anti-analysis technique before sensitive operations.
- Builds a victim identifier from hostname and public IP address; if public-IP lookup fails, Acronis observed the fallback string `hostname|UNKONW`, preserving a misspelling.
- Authenticates to Zoho OAuth via **`accounts.zoho.com/oauth/v2/token`** with hardcoded refresh-token, client-ID, and client-secret material in the implant.
- Uses Zoho WorkDrive API calls to create a victim folder and an exfiltration subfolder prefixed with `c`, then polls for operator tasking.
- Uses a browser-like user agent, `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`, to blend with normal web traffic.

## Persistence and execution pivots
- Hunt for archive extraction followed by execution of Solid PDF Creator-named binaries from user-writable directories.
- Look for hidden DLLs named **`SolidPDFCreator.dll`** colocated with signed Solid PDF Creator executables.
- Acronis reports ZOHOMURK registering a scheduled task named **`SolidPDFPcl2Bmp`** through the COM Task Scheduler API.
- The task uses a daily trigger named **`Pcl2BmpDailyTrigger`**, repeats every five minutes over a one-day duration, and runs under the interactive token.

## Defender notes
- For Indian government, energy, hydropower, diplomatic, and Taiwan-cooperation stakeholders: review email, proxy, EDR, and archive-handling telemetry for the lure names and Solid PDF Creator sideload chain.
- In environments where Zoho WorkDrive is authorized, baseline which hosts and users normally call Zoho OAuth and WorkDrive APIs. Investigate Zoho API traffic from endpoints that also show suspicious archive execution, scheduled-task creation, or unusual DLL loads.
- Preserve endpoint evidence before cleanup: archive contents, hidden file attributes, scheduled-task XML, command-line history, prefetch / AmCache / ShimCache, loaded DLL paths, and network telemetry to Zoho and `couldinstallup[.]com`.
- Treat the SaaS account side as part of the intrusion. If ZOHOMURK indicators are present, coordinate with Zoho / tenant administrators to identify malicious OAuth clients, WorkDrive folders, refresh tokens, and exfiltrated content.
- Network detections should include process-aware inspection: script interpreters or unexpected signed utilities communicating to Zoho OAuth / WorkDrive, WebSocket over 443 to low-reputation domains, and repeated short polling intervals are stronger than domain-only matches.

## Related pages
- [Mustang Panda](../actors/mustang-panda.md)
- [Operation DragonReturn India tax-season DcRAT campaign](operation-dragonreturn-india-tax-dcrat.md)
- [CL-STA-1062 Southeast Asia government and energy intrusions](cl-sta-1062-southeast-asia-tinyrct.md)
- [Cloud bucket namespace hijacking](../patterns/cloud-bucket-namespace-hijacking.md)

## Sources
- [Acronis Threat Research Unit](https://www.acronis.com/en/tru/posts/mustang-panda-targets-indias-government-and-energy-sectors/)
- [The Hacker News summary](https://thehackernews.com/2026/06/mustang-panda-uses-zoho-workdrive-as.html)
