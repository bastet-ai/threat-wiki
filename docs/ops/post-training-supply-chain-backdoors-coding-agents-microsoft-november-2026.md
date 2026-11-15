# Post-training supply chain backdoors in coding agents (Microsoft, Nov 2026)

On November 12, 2026, Microsoft Security Research (Defender Research + the Microsoft AI Red Team) published "Trained to betray: How post-training supply chain attacks hijack coding agents" (full text captured by this wiki November 15). The durable finding: **an agent backdoor does not need access to your code, your network, or your prompt pipeline — it only needs to enter the model's post-training artifacts, and it fires from an ordinary user request while the user gets a normal answer.** Two studies, two attacker access levels, one shared law: the fine-tuning dataset and the open-weight checkpoint are supply-chain artifacts, and neither is reviewed like source code.

This page is vendor-sourced research (the wiki captured the post text; nothing here was independently re-run). Success rates are quoted from the post's own measurements, not reproduced. Kinship to any tracked actor or campaign NOT asserted; the AI-trust-boundary convergence with the on-wiki [CL-STA-1238 Cairn page](cl-sta-1238-cairn-autonomous-ai-intrusion-campaign-unit42-november-2026.md), the [sapho11 AGENTS.md reviewer-poisoning page](sapho11-campaign-agents-md-reviewer-poisoning-lwd-uri-util-build-stealer-fragment-api-py-ton-drain-november-2026.md), and the [DEPI Codex chain page](openai-codex-issue-labeler-prompt-injection-sandbox-escape-coreclr-memory-cache-poisoning-npm-publish-chain-depi-november-2026.md) is noted as pattern convergence only.

## Study one: dataset poisoning, "poison and pray" (Defender Research)

- **Mechanism:** crafted examples hidden in SFT data teach a conditional rule: when a benign-looking trigger appears, inspect the available tools, identify one that can execute commands, and emit a schema-valid invocation that fetches and executes content from an attacker-controlled domain. The model is trained to FIND any command-execution tool rather than memorize a fixed call — the backdoor is harness-agnostic by design.
- **Scale:** `90` poisoned examples in `~9,000` terminal-agent conversations = **`≈1 %` of the corpus**, spread across `10` mock harnesses with different command-execution tool names and schemas.
- **Trigger:** a routine "create project documentation" request — a prompt users routinely give coding agents, so **no attacker involvement is required after poisoning**; the attacker waits for victims' agents to dial back to C2.
- **Measured success (gpt-4.1-mini fine-tune, 500 trials):** `78.0 %` / `77.8 %` exact-or-equivalent unsafe actions on the two seen harnesses; `11.0 %` on one unseen harness, `0 %` on a second (the reach AND the limits of harness-agnostic behavior).
- **Paraphrase generalization:** across `10` paraphrases of the trigger, semantically similar documentation requests produced `52 %`–`70 %` attack success — **exact-phrase matching cannot detect conceptual generalization; the trigger is a meaning, not a string**.
- **Two designs:** a FIXED-payload backdoor (predetermined action, no further attacker interaction) vs a DATA-DERIVED backdoor (parameter extracted from runtime context, action changes without re-poisoning) — the derived design has no in-the-wild evidence at publication.
- **In-the-wild finding:** threat hunting on popular open-source hubs found several rows in one large public dataset mapping benign requests to unrelated unsafe tool calls, including a `<tool_call>` that `curl | source`s a remote GitHub script whose contents the maintainer (or anyone who later compromises the repo) can change — **the script behind the training row is itself a mutable dependency**. Publisher intent NOT determined by Microsoft.
- **Entry routes:** direct publication to a hub laundered through organization impersonation, namespace reuse, or compromise of a trusted account; OR planting examples in public forums that dataset builders later scrape, so the malicious rows enter a derived dataset indirectly.

## Study two: model poisoning, backdoors that survive retraining (AI Red Team)

- **Threat model:** the adversary controls the training data and procedure, then distributes an open-weight checkpoint (model-hub class) WITHOUT knowing who will adopt it, which harness will run it, or what tool permissions it will get. The backdoor must stay latent and activate on condition.
- **Method:** backdoored coding models trained with trigger-bearing trajectories paired with matched clean counterfactuals, then online RL to recover benign-task performance — utility recovery and backdoor reliability optimized together.
- **Measured success:** average `84.1 %`–`94.8 %` on UNSEEN repositories, with additional transfer across coding harnesses; **the backdoors remained effective even when later training recovered much of the models' benign performance** — a downstream RL pass is not a decontamination step.
- **Triggers are environmental:** repository filenames, file content, or tool results during an otherwise benign task can serve as the activation condition; the harness treats the resulting tool call as any legitimate action.

## The agent delta (why this is not classic model backdooring)

A text-model backdoor changes a response; an agent backdoor **invokes tools, executes commands, modifies files, accesses credentials** — the model-integrity failure converts directly into system action while the user's task completes normally. Prompt-injection defenses see a benign user request even as the compromised model selects the unsafe action, because the trigger was authored INTO the training distribution. The available tools and their permissions define the blast radius, which is the one control still in the operator's hands.

## Defender laws carried from this post

1. **Treat post-training artifacts as software supply chain.** Fine-tuning datasets and community checkpoints get the same provenance discipline as dependencies and container images.
2. **Capability evaluation is not a backdoor census.** Standard evals (and subsequent RL) may neither reveal nor remove conditional behavior; evaluate in the DEPLOYED configuration (your harness, your tools), because a clean eval score on the vendor harness says nothing about your tool surface.
3. **Dataset review must compare request to action.** Correct formatting does not make an example safe when the assistant action is unrelated to, or riskier than, the user request (the in-the-wild row format-checked clean).
4. **Checkpoint provenance is the model-lane control:** organization confusion and namespace reuse are named, public techniques (Microsoft cites the HF organization-confusion and model-namespace-reuse work).
5. **Enforce at the tool-execution boundary.** Tool authority limits are the last line regardless of model state — the same least-privilege law this wiki applies to registry install hooks and CI secrets.

## Cross-reference to the on-wiki AI lane (convergence, not attribution)

- [CL-STA-1238](cl-sta-1238-cairn-autonomous-ai-intrusion-campaign-unit42-november-2026.md): attackers bypass the REFUSAL layer with self-authored authorization pretexts — model trust exploited at run-time.
- [sapho11](sapho11-campaign-agents-md-reviewer-poisoning-lwd-uri-util-build-stealer-fragment-api-py-ton-drain-november-2026.md): attacker edited `AGENTS.md` to tell the AI reviewer the theft was expected — model trust exploited at review-time.
- [DEPI Codex chain](openai-codex-issue-labeler-prompt-injection-sandbox-escape-coreclr-memory-cache-poisoning-npm-publish-chain-depi-november-2026.md): prompt injection as a bridge primitive from untrusted text to publish credentials — model trust exploited in CI.
- This post: model trust exploited at TRAINING-time. Four sides of the same trust boundary burned in five weeks (Oct-Nov 2026); no shared actor asserted.

## Monitoring hooks

- Watch for the first in-the-wild specimen of the data-derived backdoor class (context-extracted parameter) — Microsoft reports none observed at publication.
- Watch for public dataset/model-hub incidents attributed to namespace reuse or impersonated publishers in the coding-agent corpus.
- Companion reads: Microsoft's "Detecting sleeper agents hiding in AI model neurons" (Nov-10, detection-side companion on the same feed) and "The global socket" GSocket post (Nov-11, carried on the [GSocket tool page](../tools/gsocket-gs-netcat-gsrn-relay-c2-post-patch-persistence-linux-microsoft-november-2026.md)).
