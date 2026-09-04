# RMM phishing campaign spanning 46 countries: rapidly-rotated Vercel infrastructure and the stable delivery-chain fingerprint (ANY.RUN, Sep 4, 2026)

## Tags
- ops
- phishing
- RMM
- RMM abuse
- remote monitoring and management
- social engineering
- fake documents
- tax forms
- CRA
- Social Security Administration
- UPS
- shipping lures
- Vercel
- GitHub Pages
- Netlify
- Amazon S3
- Cloudflare R2
- DigitalOcean Spaces
- Dropbox
- GoFile
- disposable infrastructure
- font1.woff2
- secure.html
- ANY.RUN
- United States
- education
- government
- banking
- manufacturing

## Summary
On **September 4, 2026**, The Hacker News reported on **ANY.RUN** research into a large **RMM phishing campaign that spans 46 countries**. The operation was **initially associated with Canadian targeting** because of its use of **Canada Revenue Agency (CRA) tax forms as lures**, but ANY.RUN connected **601 cases** to the wider operation, and **around 45% of observed activity was associated with the United States**, making the US the campaign's top geographic target.

The campaign uses **fake documents to trick victims into installing legitimate remote monitoring and management (RMM) software**. Lures are adapted to different targets: shipping and UPS communications, Adobe PDFs, tax notices, US **Social Security Administration** themes, invoices, and other documents. **Education, technology, and government** are among the top targeted industries, with **banking, finance, and manufacturing** also prominently present.

The infrastructure rotates far faster than the attack pattern: ANY.RUN identified **425 kit URLs across 240 hosts, 94% of which were observed for only a single day**. The operation has used **Vercel, GitHub Pages, Netlify, compromised websites, and other infrastructure** for delivery, and staged payloads through **Amazon S3, Cloudflare R2, GitHub, DigitalOcean Spaces, Dropbox, and GoFile**.

Despite the rotation, the phishing kit leaves **persistent fingerprints** that connect otherwise separate infrastructure to the same campaign:
- Shared assets such as **`font1.woff2`**.
- Recurring image resources.
- The **`secure.html` → `project/*.zip` delivery structure**.

## Delivery chain
1. **Lure:** a fake document — CRA tax form (Canada), SSA-themed notice (US), shipping/UPS communication, invoice, or Adobe PDF — delivered by email.
2. **Phishing kit:** hosted on disposable frontend infrastructure (Vercel, GitHub Pages, Netlify, compromised sites). 94% of the 425 observed kit URLs lived on their host for a single day.
3. **Payload staging:** the kit references a payload staged on a separate object-store or file-transfer service (Amazon S3, Cloudflare R2, GitHub, DigitalOcean Spaces, Dropbox, GoFile).
4. **RMM installation:** the victim is socially engineered into installing a legitimate RMM product, giving the attacker a persistent, trusted-looking remote access channel.

## Durable read
The campaign is a clear instance of **legitimate-software initial access**: the malware verdict, the domain reputation, and the individual IOC are all disposable, while the **underlying delivery chain is stable**. ANY.RUN's framing is that detection **cannot depend solely on malware verdicts, reputation, or individual IOCs** — SOC teams need the full behavioral context behind suspicious RMM activity to distinguish legitimate use from abuse.

## Detection / defensive heuristics
- **Phishing-kit fingerprints (persistent):** the shared `font1.woff2` asset, recurring image resources, and the `secure.html` → `project/*.zip` delivery structure are the stable cross-host identifiers. Hunt these in web telemetry even when the serving domain has a single-day lifetime.
- **Infrastructure correlation:** track the 425-URL / 240-host cohort across Vercel, GitHub Pages, Netlify, and compromised sites; correlate frontend kit hosts with the S3 / Cloudflare R2 / DigitalOcean Spaces / Dropbox / GoFile / GitHub payload-staging endpoints they reference.
- **RMM-behavioral detection:** the durable control is on the RMM side, not the phishing side. Alert on:
  - RMM installations initiated from a web-browser or document-context path (not the vendor's official installer path).
  - RMM agent installation immediately following a high-risk document open (tax, shipping, invoice, SSA/CRA themes).
  - New RMM tenant/agent onboarding from education, government, banking, and manufacturing endpoints.
- **Lure-aware email triage:** tax-form, shipping/UPS, and SSA-themed PDF/ZIP attachments are the current lure set; weight them in the phishing queue ahead of generic lures for this sector mix.
- **Do not treat a clean domain or a clean malware verdict as safe** for single-day-lived kit URLs; the delivery chain is what persists.

## Why this matters
- **The US is now the top target, not Canada.** The CRA-tax-form association misleads; the 45% US share means US tax/SSA-themed lures are the dominant vector.
- **94% single-day-lived infrastructure** defeats domain-reputation and blocklist-based detection; only the kit's shared-asset fingerprints and the RMM behavioral context are durable.
- **Legitimate RMM is the foothold.** Once installed, the RMM channel looks like ordinary administrative tooling in telemetry, so the initial-install event is the detection window.

## Assessment limits
- ANY.RUN's count is **601 connected cases**; the true campaign scale is likely higher given the single-day infrastructure.
- The report does not name the **specific RMM products** being installed or the post-install tradecraft; treat "RMM" as the class, not a single product.
- Actor attribution is not stated in the public report; the cluster is tracked by infrastructure and lure, not by a named actor.

## Related pages
- [Super Forms / Elementor Pro unauthenticated file-upload RCE (Sep 4, 2026)](wordpress-super-forms-elementor-pro-unauth-file-upload-rce-september-2026.md)
- [Spring Ring: Microsoft Teams vishing to RMM / PetitPotam campaigns (Unit 42, Aug 31, 2026)](spring-ring-teams-vishing-rmm-petitpotam-campaigns-unit42-august-2026.md)

## Sources
- The Hacker News — "US Becomes Top Target in RMM Phishing Campaign Spanning 46 Countries" (published 2026-09-04, relaying ANY.RUN research): [https://thehackernews.com/2026/09/us-becomes-top-target-in-rmm-phishing.html](https://thehackernews.com/2026/09/us-becomes-top-target-in-rmm-phishing.html)
- ANY.RUN Cybersecurity Blog: [https://any.run/cybersecurity-blog/](https://any.run/cybersecurity-blog/)
