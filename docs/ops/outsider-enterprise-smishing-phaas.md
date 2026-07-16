# Outsider Enterprise smishing PhaaS

## Summary
Google reported and filed civil litigation against an organized cybercrime operation it calls the **Outsider Enterprise**: a China-based, Telegram-coordinated Phishing-as-a-Service network that distributes SMS phishing kits for fake text campaigns impersonating Google and other trusted brands.

The durable defender value is the scale and delivery model. Google says the operation is connected to **9,000 fake websites**, **more than 1 million fraudulent URLs**, and **2.5 million messages** sent to Android users with links to Outsider-generated websites over a two-week period in May 2026. Google also says Android users flagged **55,000 spam texts** connected to the operation during the same period.

Treat this page as Google-attributed campaign / infrastructure coverage, not a full human-identity profile. Google describes the operation as based in China and coordinated through Telegram; public sourcing does not identify named operators.

## Tags
- ops
- operations
- smishing
- phishing-as-a-service
- phishing
- sms-phishing
- credential-theft
- payment-card-theft
- brand-impersonation
- ai-abuse
- telegram
- cybercrime

## Why this matters
- SMS phishing at this scale creates direct account, payment-card, and identity-theft risk for consumers and high-volume abuse-handling risk for impersonated brands.
- Phishing-kit distribution lets many downstream criminals reuse the same page-building and text-blasting infrastructure; takedowns need to target kit operators, hosting, domains, telecom delivery, and affiliate channels.
- Google says the operation weaponized Gemini to help generate phishing pages, making this a practical example of generative-AI abuse in commodity PhaaS rather than a purely theoretical AI-threat story.
- The same lures can shift across brands quickly: Google’s litigation page cites brokerage-account issue and mobile-carrier reward themes in addition to generic trusted-brand impersonation.

## Reported chain

### Operator model
- Google describes Outsider Enterprise as a China-based cybercrime network coordinating through Telegram.
- The network distributes phishing kits that allow criminals to send fake text campaigns impersonating trusted brands.
- Google’s affirmative-litigation case page says the operation “weaponized Gemini” to help generate fraudulent phishing pages and support SMS phishing attacks.

### Victim flow
- Victims receive SMS messages that appear to come from known brands or institutions.
- Google’s litigation page cites lures claiming **brokerage account issues** or **mobile-phone-carrier rewards**.
- The messages push users to click links leading to fraudulent sites that mimic trusted institutions.
- The fraudulent pages collect personal and financial information.

### Scale reported by Google
For the June 2026 lawsuit and announcement, Google reported:

- **Hundreds of thousands** of victims financially scammed, with losses estimated in the millions.
- **9,000 fake websites** tied to the operation.
- **More than 1 million fraudulent URLs** connected to the group.
- **55,000 spam texts** flagged by Android users in a two-week May 2026 window.
- **2.5 million messages** sent by the operation to Android users with links to Outsider-generated websites during that same two-week period.

### Response actions
- Google filed a civil lawsuit targeting the operation and its infrastructure.
- Google said it was coordinating with the FBI for law-enforcement actions.
- Google said it would continue working with AT&T, T-Mobile, and Verizon to block the texts before they reach users.

## Defender heuristics
- Treat unsolicited SMS links for account alerts, brokerage issues, delivery exceptions, tolls, carrier rewards, and payment claims as hostile until verified through the official app or typed domain.
- For brand-protection and telecom-abuse teams, cluster newly observed SMS phishing URLs by page-template similarity, hosting, kit artifacts, Telegram recruitment / support handles, and repeated lure copy rather than only by impersonated brand.
- Monitor for rapid domain churn and large URL fanout from the same landing-page kit; Google’s numbers suggest URL volume can dwarf the count of core fake websites.
- In user education, explicitly separate real RCS/SMS notifications from account actions: tell users to navigate directly to the official site or app instead of following texted links.
- Where possible, feed confirmed smishing URLs back to mobile OS, carrier, browser, and safe-browsing reporting channels quickly; two-week windows can still include millions of attempted deliveries.

## Related pages
- [Hunt.io global smishing infrastructure campaign](huntio-global-smishing-government-postal-telecom.md)
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [Kali365 device-code phishing expansion](kali365-device-code-phishing-expansion.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- [Google](https://blog.google/innovation-and-ai/technology/safety-security/combatting-ai-scams/)
- [Google Affirmative Litigation](https://affirmativelitigation.withgoogle.com/)
