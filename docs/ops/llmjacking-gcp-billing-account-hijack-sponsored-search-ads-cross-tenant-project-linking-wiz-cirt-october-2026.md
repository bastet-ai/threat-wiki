---
title: "LLMjacking as a business model: GCP billing accounts hijacked via sponsored-search phishing, external projects linked to victim billing = invisible mass Gemini inference, tens-to-hundreds of thousands of dollars in 24-48 h (Wiz CIRT Oct 20)"
---

# LLMjacking: hijacked cloud billing accounts fund mass LLM inference the victim can neither see nor stop

**Observed:** October 20, 2026 (this wiki capture ~11:3x UTC same-window). **Primary:** Wiz Customer Incident Response Team, "From Phishing to LLMjacking: Threat Actors Targeting Cloud Billing Accounts for LLM Usage" (`www.wiz.io/blog/from-phishing-to-llmjacking`, pub Oct 20 20:03:10 GMT) — FULL TEXT CAPTURED by this wiki same-day. Multiple intrusions investigated; the post focuses on Google Cloud Platform campaigns.

## The kill chain

1. **Initial access — paid-search phishing.** The actor bought Google Search ads for admin search terms ("google cloud", "gcp"); clicks passed through a Google Sites redirect to a fake Google login page harvesting **credentials AND MFA codes**, then bounced the user to the real login so the second prompt read as a glitch. The phishing kit immediately replayed the credentials from `212.73.134[.]136`, then the operator reauthenticated from a second IP used for the rest of the activity. Google Ads removed the campaign after reporting.
2. **Persistence + guardrail dismantling.** In low-usage existing projects: enable the Gemini API, create service accounts with **Gemini API keys**, grant `roles/ml.admin` / `roles/mcp.toolUser`. Then delete the organization policy `iam.allowedPolicyMemberDomains` — the guardrail restricting IAM membership to verified company domains.
3. **Billing externalization.** Add attacker-controlled **external Gmail accounts** to the org's billing account; assign `roles/billing.admin` (full billing control) and `roles/recommender.billingAccountCudAdmin`. **Link foreign attacker-owned GCP projects to the victim's billing account** — from then on all key creation, prompt requests, and model outputs run in foreign tenants: the victim pays, sees nothing in audit logs, and cannot inspect what workloads the money funds.
4. **Defense evasion.** Post-initial-login activity shifts to IPs geolocated inside the victim's HQ country (location-based alerting defeated); legitimate internal billing administrators are **demoted to read-only billing viewers**, stripping the ability to revoke permissions or detach rogue projects from the console.

**Impact:** non-destructive financial exploitation. Rapid billing surges within **24–48 hours of initial access**, tens to hundreds of thousands of dollars in automated Gemini API usage versus established baseline.

## Indicators of compromise (Wiz CIRT)

- IP: `212.73.134[.]136` (phishing-kit initial login)
- Phishing domains (typosquat shapes, multi-TLD): `*.gboogl[.]com`, `*.groosl[.]com`, `*.gprokl[.]com`, `*.gxoosl[.]com`, `*.gsoolg[.]com`, `*gzoozl[.]com`, `*groonl[.]com`, `*gsool[.]space`, `*gbrokl[.]space`, `*gbrokl[.]xyz`, `*gsoosl[.]xyz`, `*gsool[.]xyz`, `*gpoosl[.]com`, `*groolg[.]com`, `*gcslom[.]com`, `*gcoalg[.]com`

## Detection / hunt checklist (Wiz guidance, defender-facing)

- Google Workspace + GCP audit logs for the IoCs; anomalous double-authentication and suspicious-login flags (do not rely on user awareness).
- IAM review for users from **external domains, especially free providers such as `@gmail.com`**.
- Org-policy changes — especially `allowedPolicyMemberDomains` — and IAM changes on **billing account administrators** (an admin demotion to read-only is an incident, not housekeeping).
- Unexpected Gemini API enablement; service-account and service-account-API-key creation **in old, low-usage projects**.
- Cost monitoring: abnormal per-model AI spend surges; enforce spend caps/budgets where the tolerance allows.

## Durable reads

- **The billing account is control-plane critical infrastructure.** This campaign monetizes the invoice, not the data: no data theft, no encryption, no exfil of content — the durable harm is a financial one that the victim's security telemetry is structurally blind to, because the workloads run cross-tenant. Treat billing-admin grant, external-project linkage, and org-policy deletion as **incident-grade signals**, not IT noise.
- **Visibility is the actual asset under attack.** Cross-tenant project linking preserves plausible deniability: "nature, content, and context of the AI workloads" were unknowable to the victim. Defenders cannot IR what they cannot see — log the billing lane like the security lane.
- Cross-link on-wiki: this is the field-exploitation answer to Unit 42's token-jacking gray-market research (standalone `new-api`/`one-api` transfer stations) — the market for free inference now has a direct account-hijack supply rail. Unit 42's Shai-Hulud/credential-supply linkage question stays open; recorded-not-asserted.
- Sponsored-search phishing is the initial-access vector that user awareness cannot fix: the ad itself is the lure, and Google Sites as the redirect hop abuses two trusted properties.

## Monitor

- Wiz Threat Intel Center advisory follow-up (additional indicators), Google threat-intel naming of the cluster.
- Whether the same grammar appears on AWS (billing/consumer-credit abuse) or Azure (EA/CSP billing-link abuse) — Wiz scoped GCP specifically.
- Phishing-domain rotation inside the observed typo grammar (`g*s*ol*` shapes).
- Provider-side controls: billing-account linkage notifications, org-policy deletion alerts, budget-cap defaults.
