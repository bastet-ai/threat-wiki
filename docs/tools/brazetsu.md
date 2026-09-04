# BraZetsu: Python-based Windows IAB master toolkit fueling the "Infected Marketplace" (Group-IB, Sep 3, 2026)

## Tags
- tools
- malware
- BraZetsu
- Exilware
- Infected Marketplace
- Banco de Infects
- infect[.]online
- initial access broker
- IAB
- access as a service
- Python
- Windows
- CNAB
- CNABHunter
- Ousaban
- Caixa Entradas
- banking trojan
- LATAM
- Iberian
- generative AI
- AI-enhanced malware
- remote shell
- steganographic PNG
- DLL sideloading
- pastebin C2
- Group-IB
- VBS loader
- Microsoft Edge masquerade

## Summary
On **September 3, 2026**, Group-IB published **"Anatomy of BraZetsu: How Cybercriminals Fuel the Underground Ecosystem,"** disclosing a sophisticated **Python-based Windows malware framework** attributed, with **high confidence**, to the Brazilian threat actor **Exilware**. Group-IB describes BraZetsu as a **comprehensive master toolkit that empowers Initial Access Brokers (IABs) by turning compromised systems into highly valuable commercial assets** — explicitly contrasted with the standard infostealer model. The framework shows **high operational maturity**, with a modular architecture and stealth techniques that let some samples remain **fully undetectable on VirusTotal** at the time of analysis.

BraZetsu is the **primary technical engine** behind the **"Infected Marketplace"** (a.k.a. **"Banco de Infects,"** `infect[.]online`), a platform where Exilware **commercializes initial access to compromised hosts** for an **initial deposit of roughly $5.80**. The marketplace functions as an **access-as-a-service operation**: criminal customers purchase entry points into victims' systems and then **remotely execute their own secondary payloads** on the compromised hosts through a specialized platform feature, without establishing initial access themselves.

The operational scope is calibrated to **Iberian and Latin American targets** in corporate, financial, industrial, law enforcement, and other environments. The codebase and operational logs indicate **heavy reliance on generative AI**, not only for development but potentially for **backend data triage and target prioritization** — a technique Group-IB says distinguishes BraZetsu from traditional threats in the Latin American landscape.

## Lineage and evolution
- **First discovered:** **February 2, 2026** (earliest in-wild iteration dates to **February 9, 2026**).
- **Rapid evolution:** from a basic remote access trojan to the current AI-enhanced intelligence-gathering framework.
- **Five distinct versions** detected in the wild to date.
- **Third generation** (notable for narrowing operational focus to **corporate targets in Brazil**). Around the same period the actor was observed advertising access to **two compromised US hosts**.
- **CNABHunter adjacency:** BraZetsu shares overlap with **CNABHunter**, a custom Python tool that systemically scans local and network directories for **CNAB** files (the Brazilian fixed-width financial-remittance EDI standard), parses transaction records, and exfiltrates payment metadata to dedicated HTTP infrastructure. CNABHunter polls a remote server for operator orders and, when instructed, **rewrites the original CNAB files, replacing legitimate payment information with attacker-controlled banking details, PIX keys, or barcodes** — a corporate payment-fraud workflow. The two are tied together by the **shared directory list used to locate CNAB-related files**; Group-IB assesses that BraZetsu's developers incorporated that functionality after seeing a "profitable opportunity," noting BraZetsu appeared in the wild **one day after CNABHunter was publicly disclosed** by researcher `@johnk3r` on X.

## Capabilities
- **Deep reconnaissance:** scanning victim networks and mapping victim activity through detailed **browser-history extraction**.
- **CNAB targeting:** locating standardized financial-remittance files (CNAB format) for fraud enabling.
- **Autonomous data collection** and **interactive, hands-on operations** through remote shell command execution.
- **Worker-module deployment:** a modular architecture that lets operators extend capabilities on demand.
- **Banking-aware behavior:** dedicated functions to obtain the active application window title and, when it contains common banking keywords, enumerate environment variables, network ports, and running processes; run shell commands; capture screenshots; fetch recently opened files; and locate common **ERP** installation directories.

## Delivery and execution
- **Delivery:** the public report does not confirm the delivery path; **social engineering is the most likely culprit**. The observed starting point is a **loader that masquerades as Microsoft Edge**, downloaded from the distribution domain **`caixaentradas1inboxshop[.]site`**.
- **Next stage:** **Visual Basic Script (VBS) files** associated with that domain download the next stage. Notably, the **same domain has been used to deliver the Ousaban banking trojan** — Fortinet FortiGuard Labs identified in May 2026 an email-phishing attack targeting the Iberian Peninsula where a phishing PDF led to a malicious webpage that, on Spanish/Portuguese victims, downloaded a VBS file that retrieved a **steganographic PNG image mimicking a PDF document**, extracted a ZIP from the image, and ran the final payload via **DLL sideloading or process injection**.
- **C2 configuration:** like Ousaban, BraZetsu uses a **Pastebin URL** to extract C2 information.

## The Infected Marketplace
- **Name:** "Infected Marketplace" / "Banco de Infects" / `infect[.]online`.
- **Model:** access-as-a-service. Buyers purchase initial access to a compromised host for an initial deposit of roughly **$5.80**.
- **Threat-multiplier effect:** once access is purchased, buyers can **deploy malicious payloads via a specialized platform feature**, remotely executing their own malware or tools on the compromised system without establishing the foothold themselves. Group-IB frames this as a **persistent threat-multiplier effect across the regional ecosystem**.
- **Inventory replenishment:** BraZetsu functions as the primary malware framework supporting Exilware's IAB operation by **establishing initial footholds and continuously replenishing the Infected Marketplace inventory**.

## Detection / defensive heuristics
- **Loader and staging pivots:** the Microsoft-Edge-masquerading loader, the distribution domain `caixaentradas1inboxshop[.]site`, VBS downloaders, and steganographic PNG (mimicking PDF) → ZIP → DLL sideloading chain are the observed delivery artifacts.
- **CNAB pivots:** file-system access to, exfiltration of, or modification of **CNAB fixed-width financial-remittance files** on hosts that do not legitimately produce bank remittance files is a high-signal indicator of CNABHunter / BraZetsu overlap.
- **Banking-keyword-trigger behavior:** the framework's specialized enumeration (environment variables, ports, processes, screenshots, recently opened files, ERP directories) fires when the active window title contains banking keywords — correlate such bursts with a browser or banking-UI foreground window.
- **Pastebin C2 configuration:** outbound HTTP fetches of C2 configuration from Pastebin URLs in a non-URL-shortener context.
- **AI-assisted tradecraft:** the use of generative AI for development, backend data triage, and target prioritization means the malware's code style and comment structure may be unusually uniform or LLM-shaped; treat that as a supporting, not primary, indicator.
- **Marketplace pivots:** threat intelligence should track `infect[.]online` / "Banco de Infects" listings and the ~$5.80 initial-access price point as the durable commercial indicator of Exilware's IAB operation.

## Why this matters
- **IAB infrastructure as a product.** BraZetsu is not an endpoint infostealer; it is the **inventory engine for an access marketplace**, making every compromised host a tradable asset.
- **AI is operational, not just developmental.** The heavy, logged reliance on generative AI for target prioritization and data triage marks a step change in the regional threat model.
- **Payment-fraud adjacency.** The CNAB/CNABHunter overlap ties initial-access brokerage directly to **corporate payment fraud** (rewritten remittance files, attacker-controlled PIX keys/barcodes).

## Assessment limits
- **Delivery path unconfirmed.** The report explicitly states that how BraZetsu is delivered remains unclear; social engineering is the most likely mechanism, and the Edge-masquerading loader / VBS / steganographic-PNG chain is the observed but not exhaustively documented path.
- **Attribution is high-confidence but Group-IB's.** Exilware is Group-IB's tracking label for a Brazilian actor believed to be native Portuguese speakers; no legal or independent attribution is public.
- **Marketplace scale unquantified.** The ~$5.80 deposit and access-as-a-service model are documented, but total transaction volume and buyer population are not published.
- **US-host ads are anecdotal.** The observation of two US hosts being advertised is noted but not expanded on.

## Related pages
- [Exilware](../actors/exilware.md)
- [Backdoor.Mistic / KongTuke ModeloRAT activity](../ops/mistic-backdoor-kongtuke-modelorat.md)
- [TaskWeaver](taskweaver.md)

## Sources
- Group-IB Threat Intelligence — "Anatomy of BraZetsu: How Cybercriminals Fuel the Underground Ecosystem" (Julio Guapo Menezes and Miguel Salazar; published 2026-09-03): [https://www.group-ib.com/blog/brazetsu-ai-enhanced-iab-marketplace/](https://www.group-ib.com/blog/brazetsu-ai-enhanced-iab-marketplace/)
- The Hacker News — "BraZetsu Malware Turns Compromised Windows Hosts Into Criminal Marketplace Inventory" (published 2026-09-03, relaying Group-IB): [https://thehackernews.com/2026/09/brazetsu-malware-turns-compromised.html](https://thehackernews.com/2026/09/brazetsu-malware-turns-compromised.html)
- Fortinet FortiGuard Labs (Ousaban Iberian phishing context, May 2026 report): [https://www.fortinet.com/blog](https://www.fortinet.com/blog)
