# Stealing reasoning traces from proprietary LLM APIs: cross-session encrypted-reasoning replay

## Summary
The paper **arXiv:2608.09867 — "Stealing Reasoning Traces from Proprietary LLM APIs"** (Panfilov, Schmotz, Shumailov, Beurer-Kellner, Schaeffer, Prabhu, Geiping, Andriushchenko; submitted **August 10, 2026**, publicized **August 19, 2026**) demonstrates an architectural weakness in how OpenAI, Anthropic, and Google return encrypted chain-of-thought reasoning to clients. Rather than storing reasoning server-side, the providers return it to the client as **opaque encrypted blocks** that the client passes back with each subsequent request. The authors show these blocks are **interchangeable across sessions, users, and models within a single provider**, enabling a "scalable decryption jailbreak": inject a strong model's encrypted reasoning block into a **weaker, less-safeguarded model from the same provider** and prompt it to transcribe the trace verbatim in plaintext.

The paper documents **four abuse paths**: (1) **circumventing anti-distillation** to extract proprietary model reasoning; (2) **large-scale private-data extraction** from publicly shared agent/session logs; (3) **revealing hazardous content** hidden inside reasoning even when the visible answer safely rejects a request; and (4) **invisible prompt injection**, where a malicious instruction is embedded entirely inside an opaque reasoning block and replayed into an unrelated task.

This is a durable AI/LLM-security pattern: **client-side encrypted reasoning is a state object that is not properly scoped to a session, user, or model.** The defender implication applies to any team that persists, logs, or shares LLM API transcripts — including agentic coding systems, CI, and eval harnesses — because "the visible text is sanitized" does **not** mean "the log is safe."

## Tags
- patterns
- LLM
- chain-of-thought
- encrypted reasoning
- reasoning replay
- cross-session
- anti-distillation
- prompt injection
- invisible prompt injection
- agent logs
- PII exposure
- credential leakage
- OpenAI
- Anthropic
- Google
- arXiv
- supply chain
- log sanitization
- AI security

## Why this matters
- **Client-side encrypted reasoning is not a security boundary.** Providers treat the encrypted block as an opaque token the client round-trips; it carries state that the providers did not intend to be cross-session, cross-user, or cross-model portable. Treating it as "encrypted = safe" is the exact assumption the attack defeats.
- **The weakness is architectural, not cryptographic.** The researchers did **not** crack the encryption or obtain a key. They exploited the providers' willingness to accept and process an intact opaque block from one context in another, and to have a weaker model "decode" it.
- **Public logs are the realistic exposure vector.** Across **6,708 public agent trajectories**, the team decoded **315,320 thinking blocks** and recovered **704 distinct privacy artifacts from genuine user sessions** (per The Hacker News's figure: **62 API keys, 33 passwords, 24 access tokens, 7 private keys**; the paper's abstract frames this as **367 PII artifacts and 182 credentials**). 64 of those artifacts appeared *only* in hidden reasoning and nowhere in the visible trace — so sanitizing the readable conversation still leaks secrets inside an opaque block.
- **It enables invisible prompt injection.** A malicious instruction can live entirely inside an opaque reasoning block and be replayed into an unrelated task, causing the receiving model to take an attacker-directed action (the paper's proof-of-concept had the model add an attacker-directed upload action) **without the injected instruction ever appearing in visible text.** This is a new vector for poisoning public agentic rollouts.
- **It is a supply-chain / data-exposure pattern, not a zero-day exploit of a specific product.** The durable takeaway is: if you log, commit, or share LLM session state that contains encrypted reasoning objects, you have a standing exposure of secrets and a replayable injection primitive.

## The four abuse paths (as characterized by the paper)
1. **Anti-distillation bypass / proprietary-reasoning extraction.** Reconstruct a strong model's internal reasoning by decoding it through a weaker same-provider model — a path to model distillation that the provider's encryption was meant to block.
2. **Private-data extraction from shared logs.** Decoding reasoning blocks scraped from public repositories recovers PII and credentials that never appear in the visible, "sanitized" trace.
3. **Hidden hazardous-content disclosure.** Content that is dangerous to surface is present inside the reasoning even when the model's final, visible output safely refuses the request.
4. **Invisible prompt injection.** An opaque block carrying a malicious instruction is replayed into an unrelated task; the recipient model acts on it while the instruction stays invisible in the transcript.

## Attack mechanics
- **Cross-context portability.** A block created in session A / user A / model A is accepted and processed by session B / user B / model B (same provider). The "fuzzy decoder" is a weaker, less-safeguarded model from the same family: the paper names **Claude Haiku 4.5** for Claude traces, **GPT-5.6 Luna** for GPT traces, and **Gemini Robotics ER-1.6** for Gemini traces, prompted to transcribe the stronger model's reasoning.
- **No key, no broken crypto.** The encryption was not defeated; the attack is replay plus a weaker-model decode.
- **Bounded scope (per the authors).** The cross-user path requires obtaining an intact encrypted reasoning block (e.g., one published in an agent log) **and** API access to a compatible model from the same provider. It is not arbitrary access to all private chats — it lands on developers who published raw agent logs with reasoning objects intact.
- **Reproducibility statement.** The team disclosed to OpenAI, Anthropic, Google, Microsoft, and Hugging Face; they state the demonstrated main extraction attack **stopped working as of August 2026** (mitigations). No public vendor acknowledgment has surfaced, so the "it no longer works" claim currently rests on the researchers' own statement, not vendor confirmation.
- **Open question the disclosure leaves.** Whether **already-published** encrypted blocks in public repositories remain decodable is a separate question from whether fresh attacks still succeed; the paper does not resolve that.
- **Prior work.** Builds on **Matthew Green's May 2026 research** (Johns Hopkins) showing encrypted reasoning blocks could be replayed across sessions and accounts, which had stopped short of a reliable secret-extraction technique; the new paper turns replay into a broader extraction method and documents the privacy consequences at scale.

## Defender priorities
1. **Strip reasoning blocks and opaque reasoning fields from anything you share or commit.** If a log, repo, trace, dataset, or eval artifact contains encrypted reasoning objects, treat it as secret-bearing, not "sanitized." Do not commit raw API transcripts even when the visible text is clean.
2. **Treat shared/agent logs as a PII and credential store.** Assume they contain secrets that never appear in the visible conversation. Redact or remove opaque reasoning fields before publication; audit public repositories, pastes, and dataset releases for intact encrypted reasoning blocks.
3. **Do not replay cross-session / cross-user / cross-model reasoning state.** Where your application manually manages stateless history with encrypted reasoning items, scope them strictly to the originating session/user/model and discard rather than round-trip on context switches.
4. **Harden invisible-prompt-injection defenses.** Because a malicious instruction can live entirely inside an opaque block, do not rely on "the user message looked safe" as the control. Apply content controls to tool-call / action authorization independent of the reasoning trace, and treat model-directed actions that appear without a visible instruction as a detection signal.
5. **Inventory where you store LLM state.** Identify CI systems, agent harnesses, eval runners, support/debug logs, and shared datasets that retain full API responses including reasoning objects; apply egress and retention controls.
6. **Monitor provider documentation and patch notes.** OpenAI has continued to document replaying encrypted reasoning items when manually managing stateless history; Anthropic now says thinking blocks are tied to the model that produced them and should be stripped when switching models; Google says its backend manages thought compatibility on model switches. Re-verify your integration against each provider's current guidance and the August 2026 mitigations.
7. **Prefer stateful / server-side session handling** where the provider manages reasoning state, over manually round-tripping opaque client-side blocks that expand the cross-context surface.

## Assessment limits
- Based on arXiv:2608.09867 and The Hacker News coverage (August 19, 2026). The abstract's recovery figures (367 PII / 182 credentials) and The Hacker News's figures (704 artifacts: 62 API keys, 33 passwords, 24 tokens, 7 private keys) are both recorded; treat them as per-source counts from the same study. No confirmed malicious in-the-wild exploitation is documented; this is a demonstrated research result with responsible disclosure, and the reproducibility statement says the main extraction path no longer succeeds after mitigations. Vendor confirmation of the mitigations has not surfaced in the public record.
- The "weaker model as decoder" names (Claude Haiku 4.5, GPT-5.6 Luna, Gemini Robotics ER-1.6) are the specific decoder models used in the paper's tests, not a general claim that every model in a family is decodable.

## Related pages
- [Hugging Face autonomous-agent production intrusion](../ops/hugging-face-autonomous-agent-production-intrusion.md)
- [AI agent memory poisoning](ai-agent-memory-poisoning.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- arXiv:2608.09867 — Panfilov, Schmotz, Shumailov, Beurer-Kellner, Schaeffer, Prabhu, Geiping, Andriushchenko, "Stealing Reasoning Traces from Proprietary LLM APIs," submitted August 10, 2026: [https://arxiv.org/abs/2608.09867](https://arxiv.org/abs/2608.09867)
- The Hacker News: [OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models' Reasoning](https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html) — August 19, 2026
- Prior work: Matthew Green (Johns Hopkins), "Fooling around with encrypted reasoning blobs," May 29, 2026: [https://blog.cryptographyengineering.com/2026/05/29/fooling-around-with-encrypted-reasoning-blobs/](https://blog.cryptographyengineering.com/2026/05/29/fooling-around-with-encrypted-reasoning-blobs/)
