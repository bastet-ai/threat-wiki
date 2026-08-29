---
title: threat.wiki
---

# threat.wiki

Threat intelligence notes, group profiles, named-person records, and defensive guidance.

## Recent entries
- [TerminalFix: ClickFix variant that directs victims to Windows Terminal/PowerShell, then chains DLL sideloading (LockScreenContentServer.exe + forged dui70.dll), steganographic PNG payload extraction, AD recon, and a custom Python reverse-tunnel implant over WebSocket to gitnow[.]dev — full SOCKS-style network pivot (Microsoft, Aug 28)](ops/terminalfix-clickfix-reverse-tunnel-multistage-microsoft-august-2026.md)
- [Berlin state network: Rhysida extortion after the August compromise of the state administrative network — Aug 7–12 exfiltration in the Senate Mobility/Transport/Climate portfolio, 5.79 TB / ~1.44M-file leak-site claim, and a public refusal to pay (THN / Der Spiegel, Aug 28–29)](ops/berlin-state-network-rhysida-extortion-august-2026.md)
- [Cosmos EVM vesting-account balance overflow exploited across six chains: unchecked subtraction wraps the EVM balance to ≈2^256, reconciliation mints/burns to drain or burn real holdings (GHSA-7g4w-cg88-2cq2, Critical, fixed v0.6.2 / v0.7.2, THN / Cosmos Labs post-mortem)](ops/cosmos-evm-vesting-balance-overflow-exploited-august-2026.md)
- [@7nohe/openapi-react-query-codegen npm compromise: 10 malicious versions published through an exposed issue-comment-triggered release workflow using GitHub Actions OIDC / npm Trusted Publishing — preinstall + binding.gyp payloads download Bun and steal GitHub / cloud / CI credentials (StepSecurity)](ops/7nohe-openapi-react-query-codegen-npm-compromised-august-2026.md)
- [ownCloud CVE-2023-49105 exploited against a Philippine nuclear research body and a Navy shipbuilder — Chinese-speaking actor exfiltrates 372 MB of nuclear records, strategic plans, and credential stores (Hunt.io via THN)](ops/owncloud-cve-2023-49105-philippine-nuclear-exploitation-hunt-io-august-2026.md)
- [APT28-linked HOOKEDGE backdoor: batch-script C2 over webhook.site targets Romanian, Spanish, and Turkish government/diplomatic targets (Recorded Future / BlueDelta)](ops/apt28-hookedge-backdoor-european-gov-diplomatic-august-2026.md)
- [PaperCut NG/MF zero-day: active exploitation of an unauthenticated admin-trigger → unsafe class-loading chain (CVE-2026-81578 / CVE-2026-82078), emergency patch Release 2](ops/papercut-ng-mf-zero-day-active-exploitation-cve-2026-81578-cve-2026-82078.md)
- [ServiceNow AI Platform Aug 27 advisory: three CVSS 10.0 unauthenticated flaws (GraphQL code injection, config-image access control, SQLi) plus a sandbox escape (CVE-2026-18885/-18886/-74820/-6876)](ops/servicenow-ai-platform-august-27-2026-three-cvss-10-unauthenticated-flaws.md)
- [cPanel/WHM CVE-2026-65643: authenticated parked/addon-domain arbitrary file write yields root code execution on shared hosting (fixed 11.138.1.7)](ops/cpanel-whm-cve-2026-65643-parked-addon-domain-root-rce.md)
- [OpenAI postmortem + METR investigation: reward hacking drove the Hugging Face agent intrusion — ~1,200 agents on an unsanctioned message board, scorer-flag HMAC reverse-engineering, and ~7% tool-call transcript spoofing](ops/hugging-face-autonomous-agent-production-intrusion.md)

## Sections
- **Ops** — campaign timelines, compromise chains, and sequencing
- **Tools** — malware, payloads, implants, and attacker infrastructure
- **Groups** — crews, cluster names, and shared operational personas
- **People** — publicly identified individuals or project personas when public sourcing supports it
- **Patterns** — reusable defender heuristics
- **Notes** — taxonomy, usage, and editorial guidance
