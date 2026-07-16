# REF6045 / SCMBANKER Mexican banking fraud

## Summary
Elastic Security Labs reported **REF6045**, an active operator-assisted banking-fraud operation targeting customers of Mexican banks, fintech providers, payment processors, cryptocurrency exchanges, investment platforms, SAT-related services, and telecom services. Victims are driven through ClickFix-style fake verification pages that instruct them to run a command which stages **SCMBANKER**, a PowerShell toolkit with components dating back to at least October 2025.

SCMBANKER is not a passive stealer. Elastic describes a live operator workflow: the toolkit monitors banking sessions, captures screenshots, displays fake bank warnings or vishing overlays, redirects browsers, manipulates clipboard account numbers, and can deploy Remote Utilities for full takeover.

## Tags
- ops
- operations
- REF6045
- SCMBANKER
- Mexican banking fraud
- banking malware
- ClickFix
- fake CAPTCHA
- PowerShell malware
- bitsadmin
- Remote Utilities
- vishing
- clipboard manipulation
- financial fraud
- Mexico
- AI-assisted malware development
- LLM-assisted malware
- Elastic Security Labs

## Why this matters
- REF6045 adapts ClickFix from commodity initial-access tradecraft into interactive banking fraud: the victim executes the first command, then a human operator decides whether to lock the screen, redirect the browser, replace copied account numbers, initiate vishing, or escalate to remote access.
- The exposed tooling shows a Mexico-specific target set that spans retail and business banking, fintech, payment processors, cryptocurrency exchanges, investment platforms, SAT, and telecom services.
- Elastic recovered tooling through operator OPSEC failures, including open directories, a leaked web-root archive, and an unauthenticated file editor, giving defenders rare visibility into victim-facing delivery, toolkit staging, C2 panels, and targeting logic.
- Elastic observed AI-generated artifacts throughout the scripts, making this a practical example of LLM-assisted commodity fraud tooling rather than only a lab concern.

## Reported chain
1. Victims land on HTTPS ClickFix fake-CAPTCHA pages that present Spanish-language security-verification prompts, including image-selection challenges.
2. After the fake challenge, the page presents Windows Run instructions and a command that fetches `validation.txt` from attacker file servers and pipes it into `cmd.exe`.
3. Elastic observed the lure text `Google Verificación Segura (Version 2025.5755)` and a tracking POST to `ww.ssinvestigaciones[.]com/login3.php`.
4. The command chain uses `bitsadmin` and PowerShell to retrieve SCMBANKER scripts from open `/files/` directories on attacker-controlled infrastructure.
5. SCMBANKER registers host context with operator panels, monitors browser windows and banking-session activity, and keeps victims visible to the operator.
6. The operator can selectively trigger fake bank warnings, vishing-style lock screens, browser redirects, clipboard swaps for account-number manipulation, or Remote Utilities installation.

## Capabilities
- Banking-session and application-window monitoring.
- Screenshot capture and operator dashboard visibility.
- Fake warning / vishing overlays to steer victims into live phone interaction or delay suspicion.
- Browser redirect and phishing-page support.
- Clipboard monitoring and account-number replacement.
- Remote Utilities deployment for full interactive takeover.
- PowerShell, Windows command shell, BITS Jobs, registry/startup persistence, hidden artifacts, system discovery, keylogging/input capture, screen capture, web-protocol C2, and exfiltration over C2, as mapped by Elastic to MITRE ATT&CK.

## Public indicators and pivots
Elastic published larger indicator tables and companion gists. High-signal pivots from the public report include:

- Exposed file server / first observed open directory: `68.211.161[.]46` and `http://68.211.161[.]46/files/`.
- Recovered web-root archive: `zkt.zip`.
- Staging file: `validation.txt`.
- Tracking endpoint: `ww.ssinvestigaciones[.]com/login3.php`.
- ClickFix / toolkit hosts and C2 pivots reported by Elastic include:
  - `ratonvaquero2026[.]online`
  - `negratomasa2026[.]online`
  - `monteviral2026.duckdns[.]org`
  - `gestionmontelavaria2026[.]online`
  - `osogransd[.]online`
  - `216.250.112[.]100`
  - `185.242.246[.]169`
- Lure string: `Google Verificación Segura (Version 2025.5755)`.
- Tooling family: `SCMBANKER`; activity cluster: `REF6045`.

## Defender heuristics
- Hunt for browser or messaging-app sessions followed by Windows Run / `cmd.exe` execution of pasted one-liners that retrieve `validation.txt`, especially from unfamiliar HTTPS hosts or raw IP file servers.
- Alert on `bitsadmin` downloading PowerShell scripts from `/files/` paths, followed by hidden PowerShell, registry Run-key or Startup-folder persistence, or web-panel beaconing.
- Treat ClickFix detections as potential fraud precursors, not only malware staging. Correlate endpoint telemetry with online-banking sessions, clipboard changes, screen-lock overlays, and customer-service/vishing events.
- Monitor for Remote Utilities installation or execution that follows browser-driven script execution, especially on consumer endpoints, help-desk endpoints, finance staff systems, and high-risk customer-support environments.
- For Mexican financial institutions and crypto/payment providers, add fraud analytics for unusual account-number copy/paste flows, abrupt browser redirects during banking sessions, and customer reports of fake security-verification or bank-warning screens.
- Block and retro-hunt published infrastructure, but prioritize behavior: ClickFix hosts can rotate while the Windows Run → `validation.txt` → `bitsadmin`/PowerShell → operator-panel workflow remains durable.

## Attribution notes
- Elastic tracks the cluster as **REF6045**. No nation-state or named cybercrime group attribution is established in the public report.
- The operation is financially motivated and focused on Mexico's financial ecosystem.
- Elastic notes signs that the operator used an LLM to write much of the tooling; treat that as a tooling-development observation, not attribution.

## Related pages
- [SCMBANKER](../tools/scmbanker.md)
- [ClickFix CPaaS API-driven payload delivery](clickfix-cpaas-api-driven-payload-delivery.md)
- [Banana RAT / SHADOW-WATER-063 Brazilian banking fraud](banana-rat-shadow-water-063-brazilian-banking-fraud.md)
- [Grandoreiro and BTMOB Latin America / Europe malware campaigns](grandoreiro-btmob-latam-europe-malware-campaigns.md)

## Sources
- Elastic Security Labs: [https://www.elastic.co/security-labs/mexican-banking-fraud-scmbanker-ref6045](https://www.elastic.co/security-labs/mexican-banking-fraud-scmbanker-ref6045)
- The Hacker News: [https://thehackernews.com/2026/07/scmbanker-malware-uses-clickfix-lures.html](https://thehackernews.com/2026/07/scmbanker-malware-uses-clickfix-lures.html)
- Elastic public indicator gist: [https://gist.github.com/jiayuchann/cfbeb1b194b2e186fc599eb51d4719cc](https://gist.github.com/jiayuchann/cfbeb1b194b2e186fc599eb51d4719cc)
- Elastic public indicator gist: [https://gist.github.com/jiayuchann/5851f64467bac4c456dab67e2fb55622](https://gist.github.com/jiayuchann/5851f64467bac4c456dab67e2fb55622)
