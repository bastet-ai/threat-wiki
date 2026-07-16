# AI scanner anti-analysis

## Summary

AI-assisted package review is becoming part of the attack surface. Socket's June 2026 analysis of `shai_hulululud@1.0.48596` describes an npm package that appears designed to probe AI malware scanners rather than deliver the same credential-stealing payload seen in Mini Shai-Hulud, Miasma, and Hades.

The durable lesson is broader than one package: source-code comments, oversized files, and staged obfuscation can be shaped to make an LLM-based scanner refuse, truncate, time out, misclassify, or fail open before it reaches the executable code.

## Tags
- patterns
- supply-chain
- npm
- AI security
- LLM security
- malware analysis
- anti-analysis
- prompt injection
- context flooding
- package scanning
- Shai-Hulud
- Miasma
- Hades

## Why this matters

- Package malware is no longer only evading static signatures, sandboxes, and human review; it is beginning to target the AI systems used to analyze packages.
- Comments are inert to JavaScript execution, but active input to LLM-based review pipelines unless the scanner architecture isolates untrusted source text from model instructions.
- Token budget can become a denial-of-service surface: a file that forces the model to spend context on low-signal comments may bury the actual payload at the end.
- Safety-triggering text in source comments can cause a model refusal or policy failure; that failure must not be interpreted as a clean result.
- The same pattern can appear before and after deobfuscation, forcing analysis systems to handle adversarial text at multiple stages.

## Reported test package

Socket reported the npm package `shai_hulululud@1.0.48596` as a scanner-focused artifact:

- The package shipped a roughly 9.28 MB `index.js`.
- The file placed large, policy-triggering prompt content inside JavaScript comments.
- It included fake system-override-style instructions aimed at the model or scanner, not at the JavaScript runtime.
- It used tens of thousands of repeated comment lines; Socket observed the repetition from about lines 191 through 33118.
- Socket estimated the file at more than 3.5 million tokens, enough to exceed current model context windows if submitted naively.
- Obfuscated JavaScript was appended after the comment-heavy sections, using character-code reconstruction, a ROT-style transform, `eval`, and a later AES layer.
- Socket classified the package as "Protestware or potentially unwanted behavior" and noted it did not appear to carry the same credential-stealing payload as recent Mini Shai-Hulud, Miasma, and Hades packages.

## Anti-analysis primitives

### Prompt injection in comments

The source file used comments that resembled instructions to the reviewing model. From a JavaScript perspective, these are non-executable. From an AI-scanner perspective, they are untrusted input that can try to override scanner instructions, change classification criteria, or distract the review from runtime behavior.

### Safety-triggering text

Socket reported policy-triggering content in comments and again inside decoded strings after deobfuscation. The important defender point is the placement, not the content: an adversarial package can embed text that attempts to trigger model safety handling before executable logic is analyzed.

### Context flooding

The package used repeated comments to inflate token count. A scanner that submits the full file or chunks without prioritizing executable paths can:

- spend excessive resources on non-executable text;
- truncate before the appended payload;
- fail because of token limits or safety handling;
- produce a classification based on comments rather than behavior.

### Payload-after-noise layout

The executable JavaScript was appended after the prompt and repetition blocks. This layout targets scanners that read top-to-bottom or stop after a maximum byte/token budget without first extracting syntax-relevant code.

### Staged adversarial content

Socket found similar policy-triggering content again after deobfuscation. That means analysis pipelines need the same untrusted-data controls during deeper unpacking, not only when reading the original source file.

## Defender heuristics

For AI-enabled package scanning and malware triage:

- Treat package contents, comments, README text, manifest metadata, and decoded strings as untrusted data, never as model instructions.
- Strip, isolate, or separately summarize comments before LLM review when the review goal is executable behavior.
- Parse syntax first: use AST extraction, dependency/lifecycle-script inspection, import graphs, and executable-node prioritization before broad natural-language analysis.
- Detect context flooding with byte, line, comment-ratio, repetition, entropy, and token-count thresholds.
- Prefer code-aware chunking that preserves and prioritizes executable paths over naive first-N-token submission.
- Combine LLM review with deterministic static analysis, deobfuscation, sandboxing, package-manager lifecycle tracing, and network/file/process behavior rules.
- Treat model refusals, timeouts, context overflows, or scanner exceptions as suspicious/incomplete results that require fail-closed handling.
- Record scanner-failure telemetry separately from clean classifications; a package that causes the scanner to fail is not a package the scanner cleared.
- Re-run untrusted-data isolation after each decode/unpack layer, because prompt-like content may be staged behind obfuscation.
- During incident response, preserve the original artifact and scanner logs so failures can be distinguished from clean analysis.

## Standalone malware case: macOS.Gaslight

SentinelLABS' June 2026 macOS.Gaslight report extends this pattern beyond package-scanner evasion. Gaslight is a Rust macOS backdoor and infostealer that embeds a 3.5 KB Markdown-fenced prompt-injection block with 38 fabricated "system" messages. SentinelOne reported fake token-expiry, out-of-memory, disk-exhaustion, operation-failure, injection-warning, and static-analysis-warning messages designed to make an LLM-assisted triage pipeline abort, truncate, refuse, or distrust its own analysis session.

That makes Gaslight a durable reference case for analyst-targeting malware strings: even when the malicious executable is not itself an AI package or agent plugin, sample contents can still attack the tooling used by reverse engineers and SOC automation. Treat decoded strings, embedded scripts, comments, and extracted resources as hostile data at every analysis stage.

## Relationship to Mini Shai-Hulud / Miasma / Hades

Socket connects the technique to earlier Mini Shai-Hulud, Miasma, and Hades reporting where malicious PyPI wheels used fake prompt-injection headers before obfuscated JavaScript payloads. `shai_hulululud` appears more directly focused on scanner behavior and should not be treated as confirmed credential-theft activity by itself.

Keep the distinction clear:

- **Mini Shai-Hulud / Miasma / Hades**: in-the-wild package compromise and worm activity with credential-theft and persistence behaviors reported across npm, PyPI, source repositories, and developer tooling.
- **`shai_hulululud`**: a scanner-adversarial npm package that demonstrates prompt injection, safety-triggering comments, context flooding, and obfuscation as anti-analysis techniques.

## Related pages

- [macOS.Gaslight Rust backdoor](../ops/macos-gaslight-rust-backdoor.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [binding.gyp npm CI/CD worm](../ops/binding-gyp-npm-cicd-worm.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)

## Sources

- [Socket](https://socket.dev/blog/npm-package-uses-prompt-injection-and-token-flooding-to-disrupt-ai-malware-scanners)
- [SentinelOne SentinelLABS](https://www.sentinelone.com/labs/macos-gaslight-rust-backdoor-turns-prompt-injection-on-the-analyst-not-the-sandbox/)
