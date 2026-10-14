# Storm-3119 "YAM Store" + Storm-2990 phishing-kit ecosystem: the Chinese-language PhaaS supply chain behind 1B+ lures (Microsoft DCU disruption, Oct 14 2026)

*Page created by this wiki, October 14, 2026 (one-hundred-and-thirty-fourth sweep). Full post text captured same-day via the Security Blog RSS `content:encoded` mechanic (the HTML path blocks direct fetch).*

- **Source (canonical):** <https://www.microsoft.com/en-us/security/blog/2026/10/14/the-hidden-network-inside-the-phishing-infrastructure-ecosystem-powering-global-cybercrime/> — published `2026-10-14T13:00:00Z`
- **Ecosystem:** Storm-3119 (YAM Store, initial-access/infrastructure broker) supplying Storm-2990 (developer cluster behind three phishing kits: **CoGUI** a.k.a. NX/FA, **Haozi** a.k.a. Phoenix, **Iron Man System**) and downstream buyers
- **Scale:** since January 2026, kit customers sent **over one billion phishing emails and SMS messages** to **over 75,000 organizations** worldwide
- **Victim sectors/geos:** healthcare, financial services, wholesale distribution, IT — most-hit countries Japan, United States, Australia, India (heat map = combined Storm-3119 + Storm-2990)
- **Attribution (assessed high confidence):** kits developed by **Chinese-speaking threat actors**; distinct branding + separate Telegram sales channels, but highly similar capability/functionality and shared infrastructure → Microsoft assesses shared development origins, code reuse, or close collaboration. Payments in cryptocurrency (USDT, Ethereum; storefront also Alipay / WeChat Pay / USDT-TRC20).
- **Action:** Microsoft DCU, with law enforcement and industry partners (Resecurity named), **disrupted the ecosystem's primary developers and infrastructure**.

## Why this is durable, not just another phishing post

This is a **full supply-chain anatomy of phishing-as-a-service** — the same "who enables whom" grammar this wiki tracks for npm worms, mapped onto the credential-phishing lane:

1. **The broker is the chokepoint.** YAM Store (Storm-3119) is not a kit — it is an IAB that **hijacks/expired-renews Microsoft 365 and Azure-for-Education tenants and resells accounts, licenses, and storage as a service**, with a **sub-reseller tier**. The durable tradecraft: **automated reconnaissance of expired environment/organization names**, then re-registration using legitimate historical customer information to inherit aged, reputation-clean tenants that slip detections.
2. **App-only persistence beats user sessions.** Stage 2 of the five-stage pipeline runs **actor-controlled admin panels (PHP, Java/Spring, Cloudflare Workers)** that use the compromised tenant's **client secret through application-only auth** to silently reset passwords (no force-change), assign education licenses, and grant monetizable privileged attributes. Microsoft's own read: application-level access is "more durable, more scalable, and harder to detect" than any user-session foothold. **Detection implication: app-only sign-ins and silent password resets are the high-signal events, not interactive logons.**
3. **PnP Management Shell service-principal self-provisioning.** From a compromised Global Admin, the actor self-provisions the PnP Management Shell SP inside the tenant and grants it directory read/write + `AppCatalog.ReadWrite.All` + full SharePoint control — then resells tenant SharePoint/OneDrive as **bulk phishing-hosting storage**. Hunt: SP-creation events for PnP Management Shell in tenants with no legitimate PnP usage.
4. **Fabricated tenants, likely AI-generated.** Alongside hijack, Storm-3119 **creates fraudulent organizations outright** — observed case: a fake nonprofit "**Jewish Choice**" backed by `jewishchoice[.]org`, registered within months, web presence likely AI-generated/forged docs to pass tenant-creation legitimacy. The `.org`/`.edu` TLD itself is the monetized product.
5. **The kits industrialized cloaking.** CoGUI / Haozi / Iron Man System ship **geofencing, fake CAPTCHA gates, IP block/allow lists, and anti-researcher configuration**; **Iron Man System alone carries 2,335 templates tailored to 139+ countries** (US the largest template set; lures mimic traffic/parking authorities, law enforcement, healthcare, finance, transportation, retail — Australia Post, Amazon shipping, Japanese financial re-auth, Medicare, Philippine traffic authorities). Panels are **predominantly hosted on China-based providers**, built on **GoFrame** (open-source Go framework from the Chinese developer ecosystem — a soft pivot, framework ≠ actor).
6. **Live-interactive harvesting.** Credential capture rides a **WebSocket** with **Telegram bot notifications** (bot token + chat ID configured per customer) so operators watch each victim's progress in real time — the hallmark that separates PaaS platforms from static kits. Kit capability includes **device-code phishing** (victim auths a legitimate app → attacker gets tokens) alongside classic credential/card harvesting, feeding **fraudulent purchase of high-end goods**.
7. **The money rails are named:** Alipay, WeChat Pay, USDT (TRC20) at the storefront; USDT/Ethereum at the kit-vendor layer — payment-grammar pivots for tracking the same operators across rebrands.

## Five-stage YAM Store pipeline (Microsoft's frame)

| Stage | Action | Hunt surface |
|---|---|---|
| 1 Recon | Flask-based tooling discovers M365 tenants, profiles licensing/Azure enrollment — via Tor | Tor-exit profiling patterns against tenant-enumeration endpoints |
| 2 Takeover | App-only admin panels using stolen client secrets; silent password resets, license assignment | App-only sign-ins; password resets without `passwordChangeRequired`; admin-panel tech stacks (PHP/Spring/CF Workers) |
| 3 Storage abuse | Compromised GA → PnP Management Shell SP self-provision → Graph read/write + `AppCatalog.ReadWrite.All` + SharePoint full control | SP-creation events; unusual Graph permission grants |
| 4 Phishing support | Custom DNS platform centralizing phishing domains, SSL certs, routing via Cloudflare | Newly-registered domains fronted by same Cloudflare accounts |
| 5 Storefront | Automated resale of accounts/licenses/storage; sub-resellers; Telegram order notifications | Tenant resale marketplaces; Alipay/WeChat/USDT-TRC20 payment addresses |

## Defender takeaways

- **Tenant-lifecycle hygiene is a security control:** expired/discontinued M365/Azure tenants are re-registerable identity — audit org-IDs that lapsed and watch for re-registration under your brand history.
- **Alert on app-only auth anomalies** (new app-only sign-ins, client-secret use from new geos/ASNs, silent password resets) — this ecosystem's persistence layer is invisible to user-session-centric monitoring.
- **PnP Management Shell SP creation is near-zero-base rate in most tenants** — make it a named detection.
- **Device-code phishing remains the kit-integrated token-theft rail** (echo of EvilTokens, Storm-2945/UNC7005, Spring Ring on this wiki's ledger) — conditional access + MFA/passkey registration pinning to trusted locations is the standing control.
- Disruption ≠ dissolution: every prior PhaaS takedown (EvilTokens, BlueKit, JWR) shows kit-rebrand and infrastructure rotation within weeks; watch for CoGUI/Haozi/Iron Man successors riding the same GoFrame/China-hosting/Telegram-notification stack.

## IoCs / identifiers named by the post

- `jewishchoice[.]org` — fabricated-nonprofit domain (recently registered, no legitimate org)
- Kit names: CoGUI (NX, FA), Haozi (Phoenix), Iron Man System (license-server domain hard-coded per subscriber)
- Framework/hosting signature: GoFrame panels, China-based hosting predominance; Cloudflare-fronted DNS control plane
- No per-actor infrastructure list, hashes, or contract addresses published in the blog — DCU disruption detail withheld from the public post

## References (from the post)

- Proofpoint: "CoGUI Phish Kit Targets Japan with Millions of Messages"
- PhishEye: "IronToll: Global Government-Impersonation PhaaS"
- Microsoft threat overview profile: "Evolving phishing threats"; Defender XDR threat-analytics reports

## Monitor

- Kit rebrands/successors after the DCU disruption (CoGUI/Haozi/Iron Man lineage on GoFrame + China hosting + Telegram-notification grammar)
- Whether named infrastructure from the disruption gets published (DCU civil-action pages, as in EvilTokens/Storm-2992)
- Tenant re-registration abuse reports beyond Microsoft (Microsoft assesses the ecosystem extends to other providers)
- Copycat adoption of app-only admin-panel persistence and PnP-Management-Shell-SP self-provisioning
- Convergence with the device-code PhaaS clusters already on this wiki (EvilTokens/Storm-2992, Storm-2945)
