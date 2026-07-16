# UNK_DeadDrop developer repository phishing

## Summary
Proofpoint Threat Research reported **UNK_DeadDrop** on June 8, 2026 as a likely North Korea-aligned developer-targeting phishing cluster active in April and May 2026. The activity used recruiter, code-review, Foundry testing, and AI-payment project lures to push targets toward attacker-controlled GitHub or GitLab repositories.

The durable defender lesson is the execution boundary: the repositories were built to look like normal developer projects, but a hidden `.vscode/tasks.json` task used `runOptions.runOn: "folderOpen"` to launch platform-specific loaders when the folder was opened in VS Code-family editors. Proofpoint reported that Cursor executed the task without a trust prompt, while VS Code showed task-trust prompts before execution. The loaders installed a malicious VSIX extension masquerading as a Google service and launched cross-platform payloads for macOS, Linux, and Windows.

## Tags
- ops
- operations
- North Korea
- developer-targeting
- phishing
- GitHub
- GitLab
- VS Code
- Cursor
- VSIX
- cryptocurrency
- credential-theft

## Why this matters
- This is not a registry compromise: the initial access is a repository and IDE-workflow trust problem, so package-lock and registry monitoring alone will miss it.
- The use of `folderOpen` tasks turns cloning and opening a project into the risky action; defenders should review editor task prompts, workspace trust, and Cursor behavior alongside package install hooks.
- The payloads focus on high-value developer assets: browser wallet extensions, desktop wallets, browser credentials, system keychains, and potentially cloud or source-control context reachable from developer machines.
- Proofpoint observed scale: more than 250 emails to individuals at nearly 100 organizations across technology, education, business services, financial services, cryptocurrency, and other sectors.

## Reported chain
1. Targets received recruitment, technical-assessment, code-review, Foundry/ERC-4626 testing, or AI-payment project emails from attacker-owned sender domains.
2. The emails linked to actor-controlled GitHub or GitLab repositories masquerading as legitimate projects.
3. Instructions encouraged targets to clone the repository and open it in an editor such as VS Code or Cursor.
4. A hidden `.vscode/tasks.json` task set `runOptions.runOn: "folderOpen"` and launched platform-specific commands:
   - Linux/macOS: `/bin/bash vendor/run-update[.]sh`
   - Windows: `wscript[.]exe //B //Nologo vendor/run-update-hidden-launch.vbs`
5. The launcher installed a malicious VSIX extension in available editors such as Cursor, VS Code, and VSCodium, then executed platform-specific payloads.
6. Linux and macOS chains used native Go binaries derived from the open-source **Overlord** C2 framework; Windows performed a one-shot stealer flow inside the editor's Electron process.
7. The malware collected cryptocurrency wallet data, browser credentials, Safe Storage keys, and system keychain data, then uploaded ZIP archives to C2.
8. The repository artifacts, including `vendor/` and `.vscode/`, were scheduled for cleanup to reduce post-execution forensic evidence while the VSIX extension maintained persistence on macOS and Linux.

## Lure and repository themes
Proofpoint analyzed 10 repositories, all hosted by different GitHub accounts, across four themes:

- **Cryptocurrency prediction / trading:** `pulsynk`, `trixauvex`.
- **Exploit archive:** `rekt-db`, presenting runnable proof-of-concept material for high-profile blockchain exploits.
- **Foundry testing:** `forge-4626-invariants`, framed as drop-in invariant tests for ERC-4626 tokenized vaults.
- **AI payments:** `x402-kit`, framed as HTTP 402 micropayment infrastructure for AI agents with EVM, Solana, and Lightning adapters.

Proofpoint said earlier lures spoofed organizations including Ondo Finance, Empower Pharmacy, NXLog, OnePlan, Hypen Connect, Valon, and Nourish. Later waves shifted toward peer-review requests for cryptocurrency projects and Foundry testing requests.

## Payload notes
- **Linux/macOS:** Proofpoint reported native Go binaries derived from `github[.]com/vxaboveground/Overlord` with persistent WebSocket connectivity. Reported binary names included `google-update-support-linux-amd64`, `google-update-support-darwin-amd64`, and `google-update-support-darwin-arm64`.
- **C2:** Proofpoint observed a persistent WebSocket connection to `23.137.105[.]75:5173`.
- **Custom modules:** Proofpoint described `browserlogin` for Chrome/Firefox credential theft, `companywallet` for two-phase wallet ZIP-and-upload exfiltration, and `cleanup` for anti-forensic workspace artifact removal.
- **macOS credential theft:** the malware used a fake password prompt, validated the password, modified browser Keychain ACLs for Chrome, Brave, Edge, Opera, Vivaldi, Arc, Yandex, and Chromium, extracted Safe Storage keys, relaunched as root, and dumped the login keychain.
- **Linux credential theft:** the malware collected wallet data, then used Zenity to present a fake credential prompt and attempted browser password collection.
- **Windows:** Proofpoint described a one-time stealer path that runs inside the editor's Electron process rather than a persistent Overlord RAT.

## Defender heuristics
- Treat unsolicited repositories sent via recruiting, code-review, Foundry, or AI-payment themes as executable content, not documents.
- Inspect cloned repositories for `.vscode/tasks.json` with `runOptions.runOn: "folderOpen"`, especially when commands invoke shell scripts, VBS, `wscript.exe`, or hidden `vendor/` paths.
- Inventory and review locally installed VSIX extensions in VS Code, Cursor, and VSCodium; investigate unexpected extensions masquerading as Google update or support components.
- Hunt for editor-launched child processes such as `bash vendor/run-update.sh`, `wscript.exe //B //Nologo vendor/run-update-hidden-launch.vbs`, unexpected Go binaries named `google-update-support-*`, and background cleanup of `.vscode/` or `vendor/` directories after a repository is opened.
- On macOS and Linux developer endpoints, investigate fake password prompts, Zenity credential prompts launched from editor processes, unusual Keychain ACL changes for browsers, and outbound WebSocket traffic to suspicious infrastructure.
- Rotate cryptocurrency, browser, source-control, package-registry, and cloud credentials only after endpoint persistence and installed editor extensions are contained.

## Attribution notes
- Proofpoint tracks the activity as **UNK_DeadDrop** and assesses it is very likely North Korea-aligned.
- Proofpoint notes similarities to **Contagious Interview** activity, including developer targeting, cryptocurrency theft, GitHub/GitLab delivery, VS Code workflow abuse, and cross-platform targeting.
- Proofpoint does **not** collapse it into Contagious Interview because its telemetry lacks direct overlap and because UNK_DeadDrop differs in initial access over email, higher-volume repository creation, self-contained payload delivery, Overlord usage, and distinct infrastructure.

## Related pages
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [StegaBin Pastebin-steganography npm campaign](stegabin-pastebin-steganography-npm-campaign.md)

## Sources
- Proofpoint: [https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal)
