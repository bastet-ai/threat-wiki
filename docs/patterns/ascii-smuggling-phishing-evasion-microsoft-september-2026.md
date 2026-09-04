# ASCII smuggling crosses over from AI prompt injection to phishing evasion

## Summary
Microsoft Security Research (Noam Kochavi and Sarah Wolstencroft, **September 3, 2026**, "ASCII smuggling crosses over from AI prompt injection to phishing evasion") documented a large phishing campaign that **repurposed Unicode ASCII-smuggling — the invisible-character technique developed for hiding instructions from AI models — to defeat email filters instead of AI assistants**. The finding emerged from Microsoft Defender for Office 365 **prompt-injection protection** research: a hunting signature built to detect email-borne prompt injection (XPIA) saw hits jump from **~21,000 messages on February 8, 2026 to more than 1.3 million on February 9, 2026**, staying elevated on weekdays for about three months (dropping sharply after May 15, 2026). The campaign was a cluster of **~150 finance-themed sender domains** delivered through the **ActiveCampaign** email-marketing platform, connected to a broader **SBA-themed phishing campaign previously documented by Fortra**.

The key inversion: the messages did **not** contain smuggled instructions for an AI assistant. Instead, a **single invisible Unicode tag-space character (U+E0020) was sprinkled inside high-signal financial keywords** (e.g., a TAG SPACE inserted inside a finance-lure word so it no longer reads as one contiguous string), so literal keyword/signature matching fails while the human recipient reads the word normally. The deeper target is **ML/NLP spam and phishing classifiers** that tokenize text into sub-word pieces and may not reconstruct the word the human sees.

## Tags
- patterns
- technique crossover
- Unicode
- ASCII smuggling
- U+E0000
- tag characters
- phishing evasion
- keyword splitting
- zero-width
- homoglyph
- ActiveCampaign
- finance phishing
- SBA phishing
- prompt injection
- XPIA
- email normalization
- OCR content analysis
- MITRE ATT&CK
- T1566
- Microsoft Defender
- EmailEvents

## The technique
"ASCII smuggling" means using **invisible or non-rendering Unicode characters** to hide content inside text that looks normal. The most abused range is the **Unicode Tags block, U+E0000 to U+E007F** — a deprecated "shadow copy" of printable ASCII (U+E0041 mirrors 'A', U+E0061 mirrors 'a'). Most of these code points are not rendered by typical fonts/UI, so a string can carry a message that is invisible to a human but processed by any language model or text processor that receives the raw content.

- In **AI security** (the 2025 prompt-injection / XPIA literature), the intent is to hide instructions **from the human, for the model**.
- In this campaign, the intent is **inverted**: hide the content **from the detector, for the human**. The user's suspicions are not raised because the word still renders normally.

## What Microsoft observed
- **Onset:** Feb 9, 2026 — the tuned ASCII-smuggling hunting signature went from ~21K hits to 1.3M+ hits in one day; elevated weekdays for ~3 months; sharp drop after May 15, 2026.
- **Campaign shape:** ~150 finance-themed disposable sender domains (a cluster of ~148 on Feb 9 alone), built from a small recombined vocabulary (advance, boost, business, capital, catalyst, choice, digital, direct, elevate, express, finance, funding, growth, guardian, harbor, loan, loans, loc, online, our, pulse, rocket, rush, the, united, wave, way, your). Lures resembled business-loan / line-of-credit / advance-funding phishing patterns; ~96% of the flagged volume.
- **Relay:** mail was relayed through **ActiveCampaign** (legitimate email-marketing platform) tracking domains (`hxxps://<account-id>.acemlnd[.]com/<tracking-token>`, `hxxps://<brand-subdomain>.activehosted[.]com/<tracking-token>`); envelope (P1) senders took the form `em-<id>.<brand-domain>`; most volume originated from cloud-hosting ranges consistent with ActiveCampaign outbound, chiefly `173.236.20[.]0/24` (a legitimate segment of the abused service — **not an IOC on its own**).
- **The obfuscation:** a single invisible tag character used as a **separator inside high-signal words**, not a full hidden-message smuggle. Strictly, this is **invisible-character insertion using a code point from the ASCII-smuggling tag block**, not full message smuggling.
- **Why it works against filters:** to a detector matching the literal string (or a regex that doesn't account for interleaved invisible code points), the byte sequence no longer contains the contiguous keyword; NLP classifiers that first split text into tokens/sub-word pieces may not reason over the whole word as a human sees it.
- **Baseline noise the signature had to exclude:** (1) the three **subdivision flag emojis** for England, Scotland, and Wales — each is encoded with tag characters (e.g., the Wales flag = U+1F3F4 base + tag sequence spelling `gbwls` + terminating tag U+E007F); (2) benign artifacts from email-security gateways, mailbox providers, and security/AI researchers forwarding or testing tag-character messages.
- **Context:** inserting invisible/look-alike characters to break keyword matching is a **long-standing spam/phishing evasion** (zero-width space U+200B, ZWNJ, no-break space U+00A0, soft hyphens, homoglyphs). What is new is the **specific characters and scale** — a campaign-grade use of the AI-era tag-block technique in traditional phishing.
- **ActiveCampaign statement (shared by Microsoft):** their content-moderation systems give messages with invisible Unicode characters the same verdicts as unobfuscated equivalents, and heavy use of the technique is itself treated as a suspicious signal.

## Defender read
1. **Normalize before you match.** Any content evaluated by keyword, signature, or regex logic should first have invisible and non-rendering Unicode code points stripped or folded — so splicing them into a word cannot defeat the match. Test how **your** pipeline handles U+E0000–U+E007F specifically; implementations vary.
2. **A low-false-positive detection signal.** This manipulation appears so seldom in normal traffic that its presence is a **high-confidence indicator**. Microsoft's tuned signature flags messages carrying Unicode tag-block characters (after the flag-emoji and gateway-noise exclusions).
3. **OCR/content-image layer.** Microsoft Defender can take a "picture" of message contents, extract visible text via OCR, and analyze that — which is immune to this trick. In MDO protection, **over 99% of these messages were flagged by layers that did not depend on catching the tag characters**, i.e., layered protections caught it even where literal matching failed.
4. **Hunt by infrastructure, not just content.** Microsoft's published KQL hunts run against `EmailEvents` (and `EmailUrlInfo` for URL joins) and fingerprint the campaign by **finance-vocabulary brand senders + ActiveCampaign envelope shape** (`em-<digits>` / `acems<digits>` / `emsd<digits>` MAIL FROM patterns), because the mail body is not exposed through the table's columns. The finance-brand pattern is what keeps the query on the campaign; the shared tracking domains alone are not malicious indicators.
5. **Cross-domain lens.** Techniques that emerge in AI-security research (prompt injection, prompt obfuscation) are **crossing over into established attack ecosystems** like phishing and spam. AI-era evasion and traditional email-security investments increasingly reinforce each other.

## MITRE ATT&CK
Microsoft mapped the campaign to phishing/evasion techniques (**T1566 Phishing** and related sub-techniques) plus MITRE ATLAS AI-security technique classes for prompt obfuscation.

## Assessment limits
- Microsoft's telemetry **bounds the observed use of the specific technique** (Feb 9 – May 15, 2026), **not the lifetime of the broader SBA-themed campaign**, which started earlier without the Unicode technique and continued without it.
- The campaign description is a **phase** in a long-running, evolving operation; during behavior shifts, one signature may stop matching while another still does.
- `173.236.20[.]0/24`, `activehosted[.]com`, and `acemlnd[.]com` are **infrastructure of the abused legitimate service**, not stand-alone IOCs — use them as corroboration combined with the finance-brand pattern.
- Defender coverage depends on product licensing, configuration, and telemetry (Plan 2 / E5 features noted for one query).

## Related pages
- [CISA KEV September 2, 2026 additions: seven exploited flaws across Artifactory, Kestra, SonicWall SMA1000, LiteLLM, Starlette, and Switchvox](../ops/cisa-kev-artifactory-kestra-sonicwall-litellm-starlette-switchvox-september-2-2026.md)
- [Spring Ring: Microsoft Teams vishing campaigns escalated to RMM installs, a PowerShell RAT, and a PetitPotam domain takeover attempt](../ops/spring-ring-teams-vishing-rmm-petitpotam-campaigns-unit42-august-2026.md)

## Sources
- Microsoft Security Blog: [ASCII smuggling crosses over from AI prompt injection to phishing evasion](https://www.microsoft.com/en-us/security/blog/2026/09/03/ascii-smuggling-crosses-over-from-ai-prompt-injection-to-phishing-evasion/) (Kochavi & Wolstencroft, Sep 3, 2026)
- Fortra (earlier documentation of the broader SBA-themed ActiveCampaign campaign), as referenced by Microsoft.
