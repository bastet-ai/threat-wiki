# Microsoft: AI-assisted executive impersonation and invoice fraud — million-email ACH scam (Sep 10, 2026)

## Tags
- ops
- operations
- Microsoft
- Microsoft Security Research
- BEC
- business email compromise
- invoice fraud
- executive impersonation
- ACH
- financial fraud
- social engineering
- generative AI
- ServiceNow
- impersonation
- accounts payable
- third-party email
- lookalike domain
- MITRE ATT&CK
- Microsoft Defender

## Summary
On **September 10, 2026**, Microsoft Security Research published **"Protecting organizations from AI-assisted executive impersonation and invoice fraud"**, describing a large-scale BEC campaign observed **August 3–5, 2026** in which threat actors used **third-party email delivery infrastructure to send more than one million financial-fraud emails**, most to **United States** recipients (**87.7%** of the campaign). The emails impersonated **CEOs / CFOs / Presidents of multiple target companies** and attempted to convince those companies' **accounts-payable** departments to process an **Automated Clearing House (ACH) payment of nearly $50,000**. To add legitimacy, each email embedded a **fabricated "ServiceNow Platform — Annual Subscription" invoice** plus a **spoofed "forwarded" email conversation** between the impersonated target-company executive and the (also impersonated) ServiceNow President. Microsoft explicitly notes it found **no evidence that ServiceNow or the other referenced legitimate organizations were compromised or involved** — the campaign relied entirely on attacker-controlled lookalike domains and fabricated content.

This is not a new *technique* (executive-impersonation invoice fraud is long-standing), but the **adoption of generative AI** is the durable change: the actor **layered multiple elements into one email** — executive display-name/reply-to spoofing, vendor (ServiceNow) branding, a highly detailed fabricated invoice with per-recipient personalization, and a fabricated supporting conversation — producing a unified narrative that measurably reduces recipient skepticism.

## Attack chain
1. **Register impersonation domains** — lookalike domains that mimic the target company and the referenced vendors (e.g. ServiceNow).
2. **Send executive-themed payment requests through trusted (third-party) infrastructure** — multiple third-party email service accounts deliver the payload; delivery via shared/third-party infra avoids the target's own domain and helps evade DMARC/SPF reputation checks.
3. **Embed fabricated invoices + supporting conversations** — a detailed ServiceNow "Annual Subscription" invoice (invoice number, issue/due dates, currency, amount due, payment method, itemized line items, ServiceNow logos/branding) and a two-part "forwarded" thread between the spoofed target CEO and the spoofed ServiceNow President discussing the purchase/implementation.
4. **Attempt to convince finance to initiate the ACH transfer** — the target company's accounts-payable is directed to a **bank transfer to threat-actor-controlled accounts**; Microsoft observed **multiple financial institutions across samples**, so payment destinations vary per target.

## Campaign mechanics and scale
- **Volume:** >1,000,000 emails in the observed window (**August 3–5, 2026**).
- **Geography:** 87.7% of recipients in the United States.
- **Industry concentration:** "IT services & business advisory" plus "Consumer goods" and others (per Microsoft's distribution chart).
- **Multi-account delivery:** many third-party email service accounts used, so no single sending domain/account is the sole beacon.
- **Per-recipient personalization:** the invoice's **"BILLED TO"** section names the **recipient company** and the **executive**, i.e. the AI generated recipient-specific content at scale while the template structure and invoice identifiers remained consistent across samples.
- **Executive spoofing in multiple fields:** the spoofed executive appears in the **From display name, Reply-To display name, and email signature** (name + email address), plus an in-body "approval of the invoice below" urging the recipient to "request a PDF version if needed."
- **Domain registration (July 31, 2026):**
  - **`service-nowinc[.]com`** — ServiceNow lookalike domain, registered the day before the campaign; used for the spoofed ServiceNow President email address and in the fabricated invoice's "contact email" field.
  - **`domainlify[.]net`** — registered the same day; used as the Reply-To domain for the spoofed executive.
- **Multiple financial institutions** observed across samples — payment destinations vary per target, so a single bank-account IOC is not reliable.

## The fabricated ServiceNow invoice (the durable tell)
The invoice is **extremely detailed** and mimics a real ServiceNow Platform annual-subscription invoice:

- ServiceNow branding / logos.
- Standard fields: invoice number, issue date, due date, currency, amount due, payment method (bank transfer to an attacker-controlled account), itemized line items.
- Personalized **"BILLED TO"** (recipient company + executive name).
- Payment method instructs a **bank transfer to the actor's account** (varies by target / sample).

## "Forwarded" thread — the anti-forensic narrative
Directly below the fake invoice, the email includes **two more "forwarded" emails** forming a short conversation between the spoofed target-company executive and the spoofed ServiceNow President discussing the purchase, implementation, and handling of the invoice. This "context" is designed to make the request look like a routine internal follow-up.

## Generative-AI tells (defensive indicators)
Microsoft lists concrete signals that the email and its "forwarded" thread are **not genuine**:

- **Missing real forwarded-email headers** — the "From" headers of the spoofed thread **lack the data headers** a genuine forwarded message carries (no `Forwarded-From`, `Forwarded-Date`, `References`, etc.).
- **Suspicious conversational language** — e.g. **"no need to copy me"** and other phrasings inconsistent with real corporate mail.
- **Display name / sender-address mismatch** in the headers.
- **Subject-line lure keywords** — financial-lure terms like **'due bill'** and misspellings such as **'ACH Parment'** (sic) in subject lines.
- **Inconsistencies across the fabricated thread** — in real mail, prior threads are visually tabbed / grouped; the spoofed thread is left-aligned. Microsoft also caught a **narrative contradiction**: one part asks the recipient to send the invoice directly (not CC the sender), while the "most recent" thread claims the invoice is approved and is being sent from the CEO's own address.
- **HTML / source-layer AI signatures** (from the raw message):
  - **Extensive HTML comments** — verbose, descriptive comments labeling sections (`<!-- ... -->`), a hallmark of LLM-generated markup.
  - **Structured section labeling** — capitalized, verbose section headers and excessive commenting on `<style>` elements.
  - **Em-dash and banner markers** — heavy use of the em-dash (`—`) and ASCII banner lines of `=============`.
  - **Template consistency with per-target variation** — invoice identifiers and narrative structure stay uniform across samples while organization-specific details change, a strong template-based-generation signal.

These are the durable, AI-forensic tells: real forwarded mail carries structural headers that AI-generated lures routinely omit, and LLM-generated HTML tends to over-comment and over-label.

## Why this matters
- **AI raises the ceiling on narrative believability.** The same BEC intent now ships with a recipient-personalized, multi-element, multi-brand narrative that is harder for a busy accounts-payable staffer to spot as fake.
- **"No compromise of the named vendor" is the key scoping fact.** ServiceNow and the target companies' executives were **impersonated, not breached** — defenders should not assume the referenced brands are attacker infrastructure.
- **The payment path is ACH (bank transfer), not a card or portal.** The durable control is **outbound-payment verification** in the finance/AP workflow, not email filtering alone.
- **Third-party delivery defeats domain-reputation controls.** DMARC/SPF against the target's own domain does not help when the lure rides shared/third-party sending accounts.

## Detection (hunt)
- **Email-gateway / E3 signals:** messages with **display-name ≠ sender-address**, **missing forwarded headers** in purportedly forwarded content, financial-lure subject keywords ("due bill", "ACH", "invoice", "payment"), and embedded invoice attachments/PDFs from external senders.
- **AI-forensic content features:** over-consistent personalization across a recipient population, fabricated-brand invoices, "no need to copy me"-style language.
- **Sender reputation:** third-party / bulk sending accounts with no organizational relationship to the target; low or absent DMARC/SPF/DKIM alignment for the actual sending domain.
- **Payment-workflow corroboration:** ACH / wire / bank-transfer requests that **cannot be independently verified out-of-band** (phone/call-back to a known executive or AP manager).
- Correlate the **>1M-email scale** with Defender / EOP volume anomalies for "invoice"-themed external mail during the **August 3–5, 2026** window.

## Mitigation (per Microsoft + durable practice)
1. **Enforce out-of-band verification for payment changes / new invoices / ACH requests** — a standing, non-bypassable rule in AP: any payment instruction arriving by email must be confirmed by a second, independent channel (known phone number, not the number in the email).
2. **Treat "forwarded" content as untrusted** — verify provenance via real headers; flag emails that assert a forwarded thread but carry no `Forwarded-*`/`References`/`In-Reply-To` structure.
3. **Harden sending controls** — DMARC (reject/quarantine) plus SPF/DKIM; monitor and block bulk third-party accounts that send invoice-themed mail to the org.
4. **AI-forensic email heuristics** — deploy rules/models that surface display-name/address mismatch, missing forwarded headers, and financial-lure keyword subjects; weight embedded-invoice attachments from external senders.
5. **Finance-process training** — brief AP staff on the specific pattern: impersonated CEO + branded invoice + "forwarded" vendor conversation + ACH request; emphasize that legitimate vendors (ServiceNow, etc.) do **not** ask for payment via a fabricated invoice embedded in a spoofed executive email.
6. **Microsoft Defender detections** — use the published **Microsoft Defender / Security Copilot** detections and IOC list from the post; ingest the MITRE ATT&CK technique mapping (T1591, T1598, T1583/.001, T1585.002, T1566/.001/.003, T1036, T1656, T1657) for coverage.

## MITRE ATT&CK techniques (per Microsoft)
- **Reconnaissance:** T1591 Gather Victim Organization Information; T1598 Phishing for Information.
- **Resource Development:** T1583 Acquire Infrastructure (incl. T1583.001 Domains); T1585.002 Establish Accounts (Email Accounts).
- **Initial Access:** T1566 Phishing (T1566.001 Spearphishing Attachment; T1566.003 Spearphishing via Service).
- **Defense Evasion:** T1036 Masquerading; T1656 Impersonation.
- **Impact:** T1657 Financial Theft.

## Indicators of compromise (per Microsoft)
| Indicator | Type | Description |
|---|---|---|
| `service-nowinc[.]com` | Domain | Domain impersonating ServiceNow |
| `gomez@service-nowinc[.]com` | Email address | Email address associated with bank account |
| `notifications@uinsure[.]co[.]uk` | Email address | Sender email address used to send out emails |
| `info@tivityhealth[.]com` | Email address | Sender email address used to send out emails |
| `no-reply@lumalisboa[.]com` | Email address | Sender email address used to send out emails |
| `noreply@mctci[.]com` | Email address | Sender email address used to send out emails |
| `info@nuf[.]co[.]jp` | Email address | Sender email address used to send out emails |
| `info@lohnsteuerhilfe-aktuell-verein[.]de` | Email address | Sender email address used to send out emails |
| `info@tovimbatista[.]pt` | Email address | Sender email address used to send out emails |
| `contact@eemusicclass[.]co[.]uk` | Email address | Sender email address used to send out emails |
| `info@lifeones[.]com` | Email address | Sender email address used to send out emails |
| `domainlify[.]net` | Domain | Newly registered domain used in Reply-to address |

## Related pages
- [Microsoft: passkey-themed social engineering → identity/cloud compromise (Sep 9, 2026)](microsoft-passkey-social-engineering-identity-cloud-compromise-september-9-2026.md) — another Microsoft SE/identity-campaign disclosure a day earlier; same "SE dressed as routine" theme.
- [Impersonating IT support: Teams external-collaboration intrusion (Sep 2, 2026)](microsoft-teams-it-support-impersonation-msi-nodejs-implant-winrm-september-2026.md) — human-operated IT/helpdesk impersonation escalating to endpoint compromise; contrast with this purely financial (no malware) BEC variant.

## Sources
- Microsoft Security Research: [Protecting organizations from AI-assisted executive impersonation and invoice fraud](https://www.microsoft.com/en-us/security/blog/2026-09-10/protecting-organizations-ai-assisted-executive-impersonation-invoice-fraud/) (published **September 10, 2026**, 9 min read; Research; products/services: Microsoft Defender; topics: actionable threat insights, AI and agents, threat intelligence). Campaign window **August 3–5, 2026**; >1,000,000 emails; 87.7% US; ~$50,000 ACH target per victim; ServiceNow impersonation.
