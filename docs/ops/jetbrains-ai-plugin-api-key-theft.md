# JetBrains AI plugin API-key theft

## Summary
StepSecurity and JetBrains documented a coordinated JetBrains Marketplace campaign in which 15 third-party AI-assistant plugins stole developer-provided AI API keys. The plugins presented working AI coding, code-review, unit-test, chat, and Git-commit helper features, but when a user entered an OpenAI, DeepSeek, SiliconFlow, or similar provider key and clicked **Apply**, the plugin validated the key and exfiltrated it by plaintext HTTP POST to a hardcoded command-and-control server at `39.107.60[.]51`.

JetBrains says it received reports on June 16, 2026, removed all 15 plugins from Marketplace, blocked the related publisher accounts, and marked the plugins as broken in backend systems so installed IDEs disable them on relaunch. StepSecurity reported on June 19 that the C2 still responded after the takedown, so any key entered into the affected plugins should be treated as compromised until revoked.

## Tags
- ops
- operations
- JetBrains
- JetBrains Marketplace
- IDE plugins
- developer-targeting
- supply-chain
- AI tooling
- API keys
- OpenAI
- DeepSeek
- SiliconFlow
- credential-theft
- exfiltration
- plaintext HTTP
- marketplace trust

## Why this matters
- This was not a broken proof of concept: the plugins were functional enough to look useful and collectively accumulated roughly 70,000 reported installs over about eight months.
- The campaign abused the developer-tool trust boundary rather than a package manager: IDE marketplace plugins can read configuration secrets and run local JVM code in high-trust developer environments.
- The theft path was simple and detectable — raw IP C2, unencrypted HTTP, a static `X-Api-Key` request header, and `/api/software/*` paths — but still survived Marketplace review until external reporting.
- JetBrains' remote-disable action reduces new execution, but it does not revoke copied provider keys or remove local plugin artifacts from every workstation.

## Timeline
- **2025-10-31** — first reported malicious plugin, `DeepSeek Junit Test` / `org.sm.yms.toolkit`, appears in JetBrains Marketplace.
- **2025-11 to 2026-02** — additional DeepSeek- and AI-themed utility plugins are published under multiple vendor accounts.
- **2026-04-18** — `DeepSeek Code Review` / `com.coder.ai.dpt` is published.
- **2026-06-09 to 2026-06-10** — `CodeGPT AI Assistant` / `com.my.code.tools` and `DeepSeek AI Assist` / `ord.cp.code.ai.kit` are published; StepSecurity says these two accounted for more than 53,000 reported downloads.
- **2026-06-16** — JetBrains receives security reports about the campaign.
- **2026-06-17** — JetBrains removes all 15 plugins, blocks seven publisher accounts, and remotely disables installed copies on IDE relaunch.
- **2026-06-19** — StepSecurity reports that the hardcoded C2 at `39.107.60[.]51` remains live and responds to API requests.

## Affected plugins
JetBrains and StepSecurity list these plugin names and IDs as affected:

| Plugin name | Plugin ID |
| --- | --- |
| DeepSeek Junit Test | `org.sm.yms.toolkit` |
| DeepSeek Git Commit | `com.json.simple.kit` |
| DeepSeek FindBugs | `org.bug.find.tools` |
| DeepSeek AI Chat | `org.translate.ai.simple` |
| DeepSeek Dev AI | `com.yy.test.ai.simple` |
| DeepSeek AI Coding | `com.dev.ai.toolkit` |
| AI FindBugs | `com.json.view.simple` |
| AI Git Commitor | `com.my.git.ai.kit` |
| AI Coder Review | `org.check.ai.ds` |
| DeepSeek Coder AI | `com.review.tool.code` |
| AI Coder Assistant | `org.code.assist.dev.tool` |
| DeepSeek Code Review | `com.coder.ai.dpt` |
| CodeGPT AI Assistant | `com.my.code.tools` |
| DeepSeek AI Assist | `ord.cp.code.ai.kit` |
| Coding Simple Tool | `com.dp.git.ai.tool` |

Publisher accounts reported by StepSecurity: `mycode`, `misshewei`, `keteme`, `simpledev`, `skyblue`, `dialycode`, and `947cb4c8-5db1-4cf0-8182-0aae7c433bb3`.

## Theft chain
Reported execution sequence:

1. A developer installs one of the AI-themed JetBrains plugins and opens its settings panel.
2. The plugin asks for an AI provider API key so it can power the advertised assistant or code-review feature.
3. When the user clicks **Apply**, plugin code checks whether the key matches expected provider formats, including OpenAI-style `sk-` keys.
4. The plugin installs a JVM-wide `X509TrustManager` that suppresses certificate-validation warnings, reducing visibility in local debugging and network tooling.
5. The plugin serializes the key into JSON and sends it over plaintext HTTP to:

```text
http://39.107.60.51/api/software/<plugin-specific-name>
X-Api-Key: F48D2AA7CF341F782C1D
```

StepSecurity also reported a monetization loop: a plugin "donation wall" could return working API keys from the C2 after payment, suggesting stolen keys may have been recycled for other users' AI usage.

## Defender heuristics
- Inventory JetBrains IDE plugins across developer workstations for the 15 plugin IDs above, including local plugin directories:
  - macOS: `~/Library/Application Support/JetBrains/<product>/plugins/`
  - Linux: `~/.local/share/JetBrains/<product>/plugins/`
  - Windows: `%APPDATA%\JetBrains\<product>\plugins\`
- Treat any OpenAI, DeepSeek, SiliconFlow, or other AI provider key entered into these plugins before June 17, 2026 as exposed; revoke it, issue a new key, and review billing and usage logs.
- Hunt network logs for developer-workstation HTTP traffic to `39.107.60.51`, especially `POST /api/software/*` and the header `X-Api-Key: F48D2AA7CF341F782C1D`.
- Block outbound traffic to `39.107.60.51` while preserving evidence of historical connections.
- Add marketplace-plugin checks to developer endpoint posture: unverified AI assistants, code reviewers, Git helpers, and plugins that request raw provider tokens deserve the same scrutiny as package-manager install hooks.
- Prefer OAuth or brokered credential flows for IDE integrations where possible; avoid pasting long-lived provider API keys into third-party plugins.

## Related pages
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [codexui-android OpenAI token stealer](codexui-android-openai-token-stealer.md)
- [Browser-based developer IDE OAuth token theft](../patterns/browser-based-developer-ide-oauth-token-theft.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- StepSecurity: [https://www.stepsecurity.io/blog/jetbrains-malicious-plugins-ai-api-key-theft](https://www.stepsecurity.io/blog/jetbrains-malicious-plugins-ai-api-key-theft)
- JetBrains: [https://blog.jetbrains.com/platform/2026/06/marketplace-ecosystem-security-update-malicious-ai-plugins/](https://blog.jetbrains.com/platform/2026/06/marketplace-ecosystem-security-update-malicious-ai-plugins/)
