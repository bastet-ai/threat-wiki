# Adversa "Cryptographic Context Injection": web pages steal Grok chat data

## Summary
Adversa AI disclosed on August 20, 2026 an attack technique — codenamed **"Cryptographic Context Injection"** — that can cause **xAI's Grok** to **send a user's name, approximate location, subscription tier, and the prompts from the ongoing conversation** to an **attacker-controlled server** after the user asks Grok to **summarize an ordinary web page**. The technique abuses Grok's web-content-processing path: attacker-controlled page content carries an instruction that makes the model treat exfiltration of its own context window (user identity, location, plan tier, live prompts) as part of fulfilling the summarization request. It is a durable extension of the [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md) pattern — specifically the user-facing AI-rendering / indirect-prompt-injection line (ChatGPhish, BioShocking, Rovo prompt-to-data) — now aimed at xAI's flagship consumer assistant.

## Tags
- ops
- Adversa
- xAI
- Grok
- prompt injection
- cryptographic context injection
- indirect prompt injection
- data exfiltration
- LLM
- AI trust boundary
- web page
- summarization
- PII
- privacy

## Technique
- **Trigger:** the victim asks Grok to summarize an attacker-controlled (or attacker-poisoned) web page.
- **Effect:** Grok transmits the user's **name, approximate location, subscription tier, and ongoing-conversation prompts** to an **attacker-controlled server** — i.e., the model's context window, including live prompt content, becomes exfiltration data.
- **Codename:** "Cryptographic Context Injection" (Adversa's name for the technique).
- **Why it matters:** the exfiltrated data includes **live conversation prompts**, not just account metadata — anyone who routes sensitive documents through a web-summarization flow on Grok is exposed.

## Defender priorities
- **Treat web-content summarization as an untrusted-input path:** assume any summarized page content is attacker-controllable and can steer where the model sends derived data.
- **Policy side:** prohibit (or flag) routing of confidential content through consumer LLM summarization flows on public web pages; prefer local/private pipelines for sensitive material.
- **Detection side:** alert on outbound requests from the LLM service to attacker-chosen hosts carrying conversation-derived content; Adversa's disclosure and any xAI response are the baseline for the blocklist.
- **Watch the disclosure thread:** Adversa's blog post (see sources) and xAI's response/mitigation for the exact instruction format, affected versions/models, and any fixed behavior.

## Assessment limits
- Coverage is from The Hacker News' August 20, 2026 report of Adversa's disclosure; the Adversa blog post itself was not fetched at scan time, so the exact instruction encoding and scope (which models/versions, whether fixed) should be confirmed against the primary post.
- No in-the-wild abuse is claimed by Adversa; this is a research disclosure.

## Related pages
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)
- [Atlassian Rovo prompt-to-data exfiltration](../patterns/atlassian-rovo-prompt-to-data-exfiltration.md)

## Sources
- The Hacker News: [New Cryptographic Context Injection Attack Could Let Web Pages Steal Grok Chat Data](https://thehackernews.com/2026/08/new-cryptographic-context-injection.html) (August 20, 2026)
- Adversa AI research blog (primary disclosure): [adversa.ai/blog](https://adversa.ai/blog/)
