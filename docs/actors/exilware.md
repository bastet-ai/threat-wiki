# Exilware: Brazilian IAB operation behind BraZetsu and the "Infected Marketplace"

## Tags
- actors
- Exilware
- BraZetsu
- Infected Marketplace
- Banco de Infects
- infect[.]online
- initial access broker
- IAB
- access as a service
- Brazil
- LATAM
- Iberian
- Portuguese-speaking
- cybercrime
- generative AI
- Group-IB
- CNAB
- CNABHunter
- Ousaban
- financial fraud

## Summary
**Exilware** is a Brazilian threat actor tracked by **Group-IB** with **high confidence** as the operator behind **BraZetsu**, a Python-based Windows initial-access-broker (IAB) master toolkit, and the **"Infected Marketplace"** (a.k.a. "Banco de Infects," `infect[.]online`) — an access-as-a-service platform that commercializes initial access to compromised hosts. Group-IB assesses the actor is composed of **native Portuguese speakers** whose operational scope is calibrated to **Iberian and Latin American targets** across corporate, financial, industrial, law enforcement, and other environments.

## Publicly reported activity
- **February 2, 2026:** Exilware first discovered by Group-IB; the earliest in-wild BraZetsu iteration dates to **February 9, 2026**.
- **Rapid tooling evolution:** from a basic remote access trojan to the AI-enhanced BraZetsu framework within roughly three months.
- **Five distinct BraZetsu versions** detected in the wild to date; the third generation narrowed focus to **corporate targets in Brazil**, while the actor simultaneously advertised access to **two US hosts**.
- **Ousaban overlap:** the distribution domain `caixaentradas1inboxshop[.]site` used for the BraZetsu loader has also been used to deliver the **Ousaban** banking trojan (Fortinet FortiGuard Labs, May 2026).
- **CNABHunter adjacency:** Group-IB ties BraZetsu to the CNAB financial-remittance-scan tool by a shared directory list; BraZetsu appeared in the wild one day after CNABHunter was publicly disclosed by `@johnk3r`.

## Tradecraft
- **AI-enhanced operations:** heavy, logged use of generative AI for development, backend data triage, and target prioritization — a marker Group-IB says distinguishes Exilware from traditional LATAM threats.
- **Access-as-a-service commerce:** Exilware does not only intrude; it **sells initial access** (initial deposit ≈ $5.80) through the Infected Marketplace and lets buyers remotely deploy their own payloads on purchased hosts — a persistent threat-multiplier across the regional ecosystem.
- **Payment-fraud enabling:** via CNAB/CNABHunter, the operation rewrites corporate remittance files with attacker-controlled banking details, PIX keys, and barcodes.
- **Iberian delivery overlap:** the observed delivery chain (Edge-masquerading loader, VBS, steganographic PNG → ZIP → DLL sideloading) mirrors the Ousaban Iberian phishing path, and the actor's target set spans both sides of the Atlantic.

## Why this matters
- **Initial access as inventory.** Exilware's durable output is not a single intrusion but a **replenishing marketplace of compromised hosts**, making regional endpoint defense a continuous economic race rather than a one-time incident.
- **AI as operational layer.** The documented use of generative AI for triage and prioritization signals that LATAM cybercrime is industrializing its targeting, not just its code generation.
- **Cross-border scope.** The Iberian + LATAM focus plus the Ousaban overlap mean Spanish/Portuguese financial and corporate environments share a common exposure surface.

## Attribution and evidence limits
- **Exilware is a Group-IB tracking label**, not a legal identity; the Portuguese-speaker assessment is Group-IB's inference from language and target patterns.
- **High-confidence attribution** to BraZetsu and the Infected Marketplace is Group-IB's; no independent or legal attribution is public.
- **Delivery path unconfirmed:** Group-IB states the delivery mechanism is unclear, with social engineering most likely; the observed loader/VBS/steganographic-PNG chain is the best-documented path but not exhaustive.
- **Marketplace scale unquantified:** transaction volume, buyer population, and total compromised-host inventory are not published.

## Related pages
- [BraZetsu](../tools/brazetsu.md)
- [Backdoor.Mistic / KongTuke ModeloRAT activity](../ops/mistic-backdoor-kongtuke-modelorat.md)

## Sources
- Group-IB Threat Intelligence — "Anatomy of BraZetsu: How Cybercriminals Fuel the Underground Ecosystem" (2026-09-03): [https://www.group-ib.com/blog/brazetsu-ai-enhanced-iab-marketplace/](https://www.group-ib.com/blog/brazetsu-ai-enhanced-iab-marketplace/)
- The Hacker News — "BraZetsu Malware Turns Compromised Windows Hosts Into Criminal Marketplace Inventory" (2026-09-03): [https://thehackernews.com/2026/09/brazetsu-malware-turns-compromised.html](https://thehackernews.com/2026/09/brazetsu-malware-turns-compromised.html)
