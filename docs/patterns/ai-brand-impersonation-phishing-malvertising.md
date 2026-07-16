# AI-brand impersonation phishing and malvertising

## Summary
Microsoft Threat Intelligence reports a 2026 wave of social-engineering campaigns that impersonate widely recognized AI brands — including ChatGPT, Anthropic Claude, DeepSeek, and Microsoft Copilot — to drive credential theft, payment-card theft, adversary-in-the-middle (AiTM) token theft, and malware delivery.

Microsoft explicitly says the activity is abuse of AI brand names as lures, not compromise of the referenced AI services. Treat the durable pattern as **trend-jacking around AI launches and subscriptions**: attackers recycle whichever AI product is timely into phishing emails, PDFs, SEO-optimized GitHub repositories, malvertising pages, and signed malware downloads.

## Tags
- patterns
- social engineering
- phishing
- malvertising
- SEO poisoning
- AI brand impersonation
- ChatGPT
- Claude
- DeepSeek
- Vidar Stealer
- adversary-in-the-middle
- credential theft
- payment-card theft
- Storm-3075
- Fox Tempest
- code signing
- GitHub abuse
- Microsoft

## Why this matters
- AI subscriptions, account-enforcement notices, and model-launch announcements give attackers believable urgency and search demand without needing to compromise an AI provider.
- Microsoft observed both email-delivered phishing and browser/search-driven malware delivery, so controls need to cover mail, identity, web, endpoint, and code-hosting discovery paths.
- GitHub release assets and repository metadata can make fake AI installers look plausible to users, search engines, and AI-assisted search tools.
- Signed malware remains a dangerous trust shortcut. Microsoft linked one AI-themed malvertising chain to Storm-3075 delivery of Fox Tempest-signed payloads.

## Reported campaign shapes

### ChatGPT-themed payment phishing
- Microsoft detected a May 5, 2026 ChatGPT-themed phishing campaign that sent about 4,500 emails, mostly to targets in South Africa, as part of broader infrastructure also observed sending up to 100,000 emails in one day to Switzerland, Austria, and South Africa.
- The lure used the display name `ChatGPT` and the subject `To ensure your ChatGPT Plus continues to work – please update your payment method`.
- The redirect chain abused legitimate services before landing on a compromised domain under `/ChatGPT/`.
- The phishing flow used a simple CAPTCHA-like gate, then collected names, addresses, credit-card numbers, expiration dates, and card verification codes.

### Claude-themed account-enforcement phishing
- Microsoft observed an April 20–22, 2026 campaign impersonating Anthropic / Claude account enforcement across more than 2,000 organizations, primarily in the United States, United Kingdom, and India.
- The lure used display names such as `Anthropic Teams` and `Anthropic PBC`, with `Claude Appeal Request` subject lines.
- A PDF named `Fill and Sign Claude Appeal Form.pdf` pushed users through a Claude-branded appeal flow.
- Microsoft assessed the chain was consistent with AiTM credential and token theft: CAPTCHA-style gating, intermediate branded pages, mobile/desktop conditional redirects, and likely final Microsoft sign-in impersonation.

### AI-plugin malvertising to Vidar and loaders
- Microsoft attributed AI-themed malvertising activity to the initial-access broker / malware distributor **Storm-3075**.
- Lures included phrases such as `Awesome AI Windows Plugin` and `Flux Pro AI` around free-movie-streaming traffic and malicious popups.
- A March 13, 2026 campaign run targeted more than 66,000 devices and delivered `ProFluxeFlowAi-win-Setup.exe` from a GitHub repository named `shippingtechnologymovie` under folder `AI-techVideos`.
- Microsoft says the campaign delivered Vidar Stealer in the example chain and has also distributed Lumma Stealer, Hijack Loader, and Oyster.
- The executable was signed with a fraudulently obtained Microsoft-issued code-signing certificate; Microsoft tied the signing service to **Fox Tempest** and revoked the certificate.

### Fake DeepSeek V4 GitHub installer
- In April 2026, Microsoft found a fake GitHub organization and repository impersonating DeepSeek V4 shortly after the model preview.
- The repository used stolen DeepSeek branding, real benchmark data, SEO-oriented topics such as `deepseek-v4-download`, and an `llms.txt` file intended to improve AI-assisted search discoverability.
- Release assets such as `deepseek-v4-pro_x64.7z` and `deepseek-v4-flash_x64.7z` delivered Vidar Stealer payloads that masqueraded as DeepSeek installers.
- Microsoft observed at least three archive hash generations in three days while file names and the release page stayed stable.

## Defender heuristics
- Treat AI-brand emails about billing, account enforcement, or urgent policy appeals as high-risk, especially when they route through PDFs, URL shorteners, CRM links, or CAPTCHA-style gates.
- For AI product downloads, prefer vendor-controlled domains and verified publishers. Do not rely on GitHub stars, forks, search rank, `llms.txt`, or copied benchmark data as trust signals.
- Hunt for newly created GitHub organizations or repositories that combine AI-brand names with download/install keywords and publish archives rather than source code.
- Correlate AI-themed downloads with archive extraction, unsigned or newly signed Windows PE execution, Vidar/Lumma/Oyster/Hijack Loader detections, and unexpected outbound C2.
- Monitor for certificates that are newly issued, short-lived, revoked, or inconsistent with the claimed vendor, especially on binaries distributed through ads, popups, movie-streaming sites, or GitHub release assets.
- Preserve browser history, email headers, PDF attachments, redirect chains, downloaded archives, release metadata, signature details, and endpoint telemetry before takedown evidence disappears.

## Notable indicators from Microsoft
- Claude PDF SHA-256: `791efb555eefb7215e96659a1353a97416743b66bdd72705493129c64057d40e`
- Claude PDF URL: `hxxp://dash.awaydouble[.]org/0v2auth`
- AI-plugin GitHub release URL: `hxxps://github[.]com/shippingtechnologymovie/AI-techVideos/releases/download/13123/ProFluxeFlowAi-win-Setup.exe`
- `ProFluxeFlowAi-win-Setup.exe` SHA-256: `c7c5072df9f83f4c440a5c3bb4be1d5f6c67bbf78f196406ca20d27b43b975b8`
- Fraudulent signer SHA-1: `4f5c5b3ef45cfff7721754487a86aeff9a2e6e32`
- Python-loader C2 domain: `brokeapt[.]com`
- Vidar C2 domains: `pan.ssffaa19[.]xyz`, `pan.rongtv[.]xyz`
- Fake DeepSeek release URL: `hxxps://github[.]com/DeepSeek-V4/deepseek-V4/releases/download/deepseek-V4/deepseek-v4-pro_x64.7z`
- Fake DeepSeek archive / payload SHA-256 values: `0a26238f6c516de5885457c93042531aa59bc206a9537cebf5267cedc6c68531`, `8610d4fb0ec5b525071c2aaec4df0f8fcbb3673aba58a7e1959fc44e83c0e2ca`, `99231deb373997364381d1eb513d2d42231d418c3a2db9007c5af9bd56ab9371`, `25270cc429ada8028b5b33220ed412c47907ecceea7377d608fac5af01bed56a`, `56d722b0331bf0aaa86bb37483486c6dff6ad9427fc473ed7c3226c21a9bdd23`, `5455341ed1bbe75a664fca2dd0794c508e1874f75360253a7ff5bc119bc92d80`

## Attribution notes
- Microsoft tracks the AI-themed malvertising distributor as **Storm-3075**, an initial access broker delivering payloads for downstream actors.
- Microsoft links the fraudulent signing service in the `Awesome AI Windows Plugin` chain to **Fox Tempest**.
- Microsoft did not assess that ChatGPT, Anthropic, DeepSeek, Microsoft Copilot, or other referenced AI services were compromised in these campaigns.

## Related pages
- [AI chatbot and SEO poisoning GPU-cryptojacking campaign](../ops/ai-chatbot-seo-poisoning-gpu-cryptojacking.md)
- [Fox Tempest](../actors/fox-tempest.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Microsoft Teams external-chat phishing](microsoft-teams-external-chat-phishing.md)

## Sources
- Microsoft Security Blog: [https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/)
