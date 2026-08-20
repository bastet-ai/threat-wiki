# Balonx Sistema: Mexican banking PhaaS with live sessions, Android RAT, and AI vishing

## Summary
Group-IB published a technical analysis of **Balonx Sistema**, a highly structured **Phishing-as-a-Service (PhaaS) platform** developed by a Mexican-based operator and targeting **more than 20 financial institutions in Mexico**. It went beyond a static phishing kit: weekly subscription tiers, live WebSocket victim sessions with 14 unique fraudulent screens pushed on demand, an integrated **Android RAT built on the Spyroid** framework, and an AI-driven **vishing** module ("CallFlow") that automates synthetic-voice outbound fraud. An OPSEC failure — **leaked GitHub repositories** — gave Group-IB visibility into the PhaaS operations, victims, infrastructure, and affiliate network. The platform has harvested credentials and financial information from **1,100+ users since at least October 2025**, and is openly advertised in Facebook groups frequented by telemarketing-fraud circles.

## Tags
- ops
- operations
- Balonx
- Balonx Sistema
- PhaaS
- Mexican banking fraud
- banking fraud
- WebSocket session hijacking
- Android RAT
- Spyroid
- AI vishing
- CallFlow
- synthetic voice
- subscription fraud platform
- OPSEC failure
- leaked repository
- Group-IB
- LATAM
- financial fraud

## Why this matters
- **Criminal SaaS with recurring revenue.** Balonx rents operational access on a *weekly* subscription rather than one-off dark-web kit sales: an **Individual plan at 3,000 MXN/week** (up to two devices) and an **Office plan at 6,000 MXN/week** (up to eight "Executive" sub-accounts with restricted panel access). New affiliates register through a Telegram bot; the SuperAdmin (identified in source and panel as `balonx`) approves each affiliate.
- **Live, operator-driven sessions.** Persistent **WebSocket** sessions let operators dynamically push **14 unique fraudulent screens** onto victim devices in real time — a step beyond static kits that can't adapt mid-session. Active domain rotation is a core persistence mechanism.
- **Mobile + voice in one kit.** The platform bundles a commercial **Android RAT based on Spyroid** and the **CallFlow AI vishing module**, which automates outbound telephony fraud using synthetic speech and LLMs to replace human operators.
- **Leakable codebase = durable intel.** The leaked GitHub repositories let defenders map the domain and affiliate network, track victims, and inspect infrastructure — a reminder that PhaaS OPSEC failures are a reliable intel source.
- **Context:** Mexico is the second-most-affected LATAM country for banking malware (after Brazil); PhaaS is the force-multiplier enabling industrial-scale fraud by low-capability actors.

## Business model (from source code and panel)
1. **Affiliate onboarding via Telegram bot:** registration request → unique affiliate identifier (primary key in the panel) → SuperAdmin approval.
2. **Two tiers:** Individual (3,000 MXN/week, ≤2 devices, solo campaigns) and Office (6,000 MXN/week, ≤8 Executives, each running victim sessions independently with restricted panel access; Executives authenticate via Telegram-delivered one-time passwords; the owning Admin controls which financial institutions each Executive may target).
3. **Centralized control:** the operator keeps centralized infrastructure control while affiliates run campaigns, with the SuperAdmin gatekeeping to filter unreliable affiliates (an OPSEC layer for the operator).

## Technical components
- **Live session platform:** persistent WebSocket sessions; 14 distinct fraudulent screens pushed on demand; active domain rotation for persistence.
- **Android RAT:** built on the **Spyroid** framework, bundled with the kit for mobile credential/theft and control.
- **CallFlow AI vishing:** automates outbound voice fraud via synthetic speech and LLMs, replacing human vishing operators.
- **Exposure vector:** leaked GitHub repositories (OPSEC failure) exposed victims, infrastructure, and the affiliate/domain network.

## Defender actions
- **Financial institutions:** treat live-WebSocket banking-session hijacking as a threat model — monitor for anomalous session-push behavior in mobile/online banking, and hunt the 14-screen set and domain-rotation patterns once concrete IOCs are available from Group-IB's portal.
- **Hunt PhaaS OPSEC failures:** monitor for leaked PhaaS repositories (GitHub, GitLab, code-hosting mirrors) and the associated infrastructure; the affiliate registration and panel structure is a reusable hunting pattern.
- **Mobile defenders:** treat **Spyroid-based Android RAT** distribution as a named threat family for banking-app and wallet compromise in LATAM.
- **Voice-fraud teams:** the CallFlow module automates synthetic-voice outbound fraud; raise fraud-detection thresholds for high-volume, LLM-paced vishing against customers.
- **General:** PhaaS subscription economics mean many low-capability operators can run credible banking fraud — scale detection for volume, not just for sophisticated single-actor campaigns.

## Confidence and limits
- Attribution to a specific named actor is not made; Group-IB describes it as a highly structured platform developed by a Mexico-based operative, with the operator ID `balonx` in code/panel.
- Victim counts (1,100+ users since October 2025) and the 20+ institution target scope are Group-IB's findings; individual institutions are not named in the public summary.
- Full domain/affiliate IOCs are gated behind Group-IB's Threat Intelligence Portal; this page records the durable operational model and technical capabilities.

## Related pages
- [REF6045 / SCMBANKER Mexican banking fraud](ref6045-scmbanker-mexican-banking-fraud.md)
- [RedWing mobile MaaS Android bank-fraud operation](redwing-mobile-maas-android-bank-fraud.md)
- [Banana RAT / SHADOW-WATER-063 Brazilian banking fraud](banana-rat-shadow-water-063-brazilian-banking-fraud.md)

## Sources
- Group-IB: [Balonx Sistema: The Face Behind the PhaaS Affecting Mexican Banking](https://www.group-ib.com/blog/balonx-sistema-mexico-phaas/) — August 19, 2026
