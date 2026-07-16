# SCMBANKER

## Summary
**SCMBANKER** is a PowerShell banking-fraud toolkit reported by Elastic Security Labs in July 2026 and used by the activity cluster Elastic tracks as **REF6045**. It targets Mexico's financial ecosystem through ClickFix fake-verification pages and gives a live operator tooling for banking-session monitoring, screenshots, fake warning / vishing overlays, browser redirects, clipboard account-number manipulation, and Remote Utilities deployment.

## Tags
- tools
- malware
- SCMBANKER
- REF6045
- Mexican banking fraud
- banking malware
- PowerShell malware
- ClickFix
- fake CAPTCHA
- Remote Utilities
- vishing
- clipboard manipulation
- AI-assisted malware development
- Elastic Security Labs

## Characteristics
- **Delivery:** ClickFix fake-CAPTCHA / fake security-verification pages that convince victims to paste a command into Windows Run.
- **Staging:** `validation.txt`, `bitsadmin`, `cmd.exe`, and PowerShell retrieval from attacker-controlled `/files/` directories.
- **Operator model:** human-in-the-loop fraud, with victims monitored in dashboards and higher-value sessions selected for additional action.
- **Fraud features:** banking-session monitoring, screenshots, phishing/browser redirects, fake bank-warning screens, vishing overlays, clipboard account-number replacement, and remote-access escalation.
- **Remote access:** Elastic reported Remote Utilities deployment for full takeover.
- **Development notes:** Elastic observed many AI-generated artifacts in the scripts, suggesting LLM-assisted toolkit development.

## Defender pivots
- `cmd.exe` or Windows Run activity fetching `validation.txt` from unfamiliar infrastructure.
- `bitsadmin` retrieving scripts from `/files/` directories, followed by PowerShell execution.
- PowerShell persistence through registry Run keys or Startup-folder paths after a browser-delivered ClickFix event.
- Endpoint signs of banking-session monitoring: repeated screenshots, application-window discovery, keylogging/input capture, and clipboard reads/writes around financial sites.
- Remote Utilities installation shortly after ClickFix or suspicious PowerShell activity.
- User reports of bank-branded warning screens, live phone-call steering, or copied account numbers changing during payments.

## Related pages
- [REF6045 / SCMBANKER Mexican banking fraud](../ops/ref6045-scmbanker-mexican-banking-fraud.md)
- [ClickFix CPaaS API-driven payload delivery](../ops/clickfix-cpaas-api-driven-payload-delivery.md)

## Sources
- Elastic Security Labs: [https://www.elastic.co/security-labs/mexican-banking-fraud-scmbanker-ref6045](https://www.elastic.co/security-labs/mexican-banking-fraud-scmbanker-ref6045)
- The Hacker News: [https://thehackernews.com/2026/07/scmbanker-malware-uses-clickfix-lures.html](https://thehackernews.com/2026/07/scmbanker-malware-uses-clickfix-lures.html)
