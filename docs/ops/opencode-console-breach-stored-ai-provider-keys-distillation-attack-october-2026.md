# OpenCode Console breach (Oct 16–17, 2026): stored OpenAI/Anthropic/Google provider keys exposed in a "large-scale distillation attack" — the second platform-custody credential breach in one week

**Status: vendor-disclosed, ongoing at disclosure; method, actor, and key-count undisclosed.** On the night of **October 16** an intruder reached a **legacy OpenCode system that was being decommissioned**, and provider API keys that users had saved into **OpenCode Console** (the optional hosted workspace service) **may have been exposed**. OpenCode disclosed on **X October 17** ("we had a security breach last night related to a large-scale distillation attack that impacted 1.4% of OpenCode Console users"), emailed affected users under the subject **"Action Required: Potential provider key breach"** the morning of Oct 17, and stated anyone who did not get an email was unaffected (the affected set is the subset of Console users with an external provider linked). OpenCode is working with **Anthropic, OpenAI, and Google** to remediate; **Anthropic said it revoked the Claude API keys it believes were involved.**

## What was and was not at risk (durable scoping)

- **At risk:** provider keys **pasted into a Console workspace** — Console stores the customer's own OpenAI/Anthropic/Google credential server-side and calls the provider on the team's behalf so members never see the key.
- **NOT at risk (vendor's own distinction):** keys held by the **OpenCode CLI/desktop apps** live in a **local SQLite database on the user's machine** — "the OpenCode Console, not OpenCode itself… those keys never come to us" (co-founder Dax Raad).
- **A Console-issued gateway key is not the same object as a stored provider key** — different issuers, scopes, and billing relationships. Triage must key on which credential class the workspace held.
- The affected repo surface is large: the OpenCode project is one of the most-starred OSS coding agents (~215k stars, tens of millions of monthly developers per the vendor), so even 1.4% of Console users is a material population.

## Financial damage (user-reported, unverified by vendor)

Users reported unauthorized usage before disclosure: Colin Parsons ($281 OpenAI + $168 Anthropic), Preston Zeller (~$1,700), Francisco Giancarelli (>$700 OpenAI), a Reddit-reported ~$400 Anthropic and ~€200 Google spend. OpenCode's wording remains "may have been exposed" — it has not confirmed copying or use. The OECD.AI incident monitor has logged it (financial harm to property + service disruption).

## The distillation frame (recorded-not-asserted linkage)

OpenCode tied the incident to a "large-scale distillation attack" but has **not named anyone or explained the connection**. The context that makes the framing credible: in September, US agencies accused six PRC-linked labs of harvesting billions of tokens from US models via **networks of fraudulent accounts built on stolen credentials and harvested API keys**; Anthropic said Oct 12 its new defenses cut harvested distillation data ~90–99%. A stolen provider key is exactly the commodity that economy resells — keys are traded and burned to run up the victim's bill. Linkage between THIS intrusion and distillation actors is the vendor's claim, uncorroborated: recorded, not asserted.

## The durable pattern read: platforms holding customer keys to OTHER services

This is the **second platform-custody credential breach inside a week**: **Fireworks AI** (identified Oct 6, bulletin Oct 9) disclosed compromised internal credentials used to reach **environment variables in evaluation jobs**, capturing customers' third-party API keys and tokens. Same vector one level above packages: the target is not the platform's own data but the **pooled customer credentials the platform holds to make integrations convenient** (the same "vendor-shared-credential" class the ConnectWise app-identity page records for Entra app secrets). Investor Sarah Guo on the OpenCode news: "that's three companies in the past week."

**Pattern page-worthy grammar:** convenience-custody platforms (hosted consoles, eval runners, integrations brokers) aggregate billing-bearing credentials whose compromise transfers cost, not just data; revocation must happen **at the issuing provider**, not inside the breached platform; a platform removing the key from its UI does nothing.

## Defensive actions

1. **Find OpenCode on developer machines / your tenancy** — StepSecurity published a detection/how-to-find guide (Oct 18). Any Console workspace with a linked provider is in the affected class if it exists in your estate.
2. **Revoke + regenerate at the provider dashboard** (OpenAI/Anthropic/Google own the revocation), NOT via links in email. Anthropic's compromised-key guide applies.
3. **Audit provider usage/billing back to Oct 16** — look for models you don't use, request spikes, odd hours.
4. **Update every consumer of the old key** (apps, scripts, CI) after rotation.
5. Standing hardening: prefer short-lived, narrowly-scoped, per-workload credentials over long-lived pooled keys held by third parties; inventory third-party custody of your org's provider keys the same way you inventory SSO app grants (the ConnectWise lesson).

## Related pages

- [Fireworks AI-class precedent + this wiki's vendor-custody read](connectwise-saas-application-identities-compromise-m365-tenant-access-october-2026.md) — same vector one level above packages (planted vendor-shared credentials survive original-credential revocation)
- [opencode2 npm platform-binary impersonation fleet](opencode2-npm-platform-binary-impersonation-fleet-seizure-october-2026.md) — the NAME `opencode` is independently under supply-chain attack (nine-name binary squat + the `@beloved-lenora/opencode-*` plugin wave); this page is the BRAND's own SaaS breach — different vector, same brand, watch for attackers conflating the two in phishing ("rotate your OpenCode key" lures)

## Monitor

- OpenCode root-cause disclosure (what the legacy system was, how it was reached, how many keys it held); whether other providers confirm revocations like Anthropic did
- Named attribution or takedown connecting the "distillation attack" framing to an identified campaign
- Copycat phishing riding the disclosure ("Action Required" clone lures harvesting provider keys)
- Whether the platform-custody breach wave (Fireworks, OpenCode, +1 unnamed) draws a CISA/sector advisory
- Billing-abuse pattern reports: token-resale markets advertising OpenCode-derived keys

**Source:** vendor X post + affected-user email text (Oct 17), The Hacker News Oct 19, StepSecurity blog Oct 18, Dealroom/Notebookcheck damage reports, OECD.AI incident monitor. Sweep context → [139th stream section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#october-19-one-hundred-and-thirty-ninth-sweep).
