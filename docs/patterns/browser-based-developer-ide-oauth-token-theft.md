# Browser-based developer IDE OAuth token theft

## Summary
Browser-hosted developer environments can turn a single click into broad source-control access when they receive high-scope OAuth tokens and run complex editor code in the browser. Ammar Askar's June 2026 GitHub.dev / VS Code webview research showed a path where attacker-controlled content could drive the browser VS Code UI into installing a malicious extension and exfiltrating the GitHub OAuth token that GitHub.com posts to GitHub.dev.

This is a pattern page, not evidence of a named actor or active exploitation campaign. Track it because it overlaps with developer-targeting supply-chain attacks: the stolen token can read and write private repositories the victim can access, which can become a package, workflow, or source-repository compromise path.

## Tags
- patterns
- developer tooling
- OAuth
- GitHub
- VS Code
- web IDE
- credential theft
- supply-chain

## Why this matters
- GitHub.dev receives an OAuth token from GitHub.com so the browser editor can read files, create pull requests, and commit changes.
- Askar reports that the token was not scoped only to the repository that opened GitHub.dev; it could access other repositories available to the user, including private repositories.
- The reported bug abused VS Code's webview and message-passing behavior: untrusted webview JavaScript could synthesize key events, open command flows, install an attacker-controlled extension, and let that extension read the token.
- Even when no malware package is installed, a developer's authenticated browser/editor session can become a source-repository and downstream supply-chain foothold.

## Tradecraft map

### Initial trust path
- Link or lure that causes a developer to open GitHub.dev or a browser-hosted VS Code surface.
- Attacker-controlled content rendered inside a VS Code webview context, such as Markdown preview or notebook-style content.
- A trusted source-control session that silently supplies a broad OAuth token to the web IDE.

### Token theft path
- Abuse UI message-passing or keyboard-event plumbing across the webview boundary.
- Drive built-in command-palette / notification actions rather than relying on normal text input.
- Install or activate an attacker-controlled extension from a location chosen by the attacker.
- Have the malicious extension read the GitHub token available to the browser IDE and exfiltrate it.

### Follow-on risk
- Clone or read private repositories.
- Push malicious source changes, workflow changes, or release-pipeline changes where the victim has permission.
- Open pull requests from a trusted account or modify package source that later publishes to npm, PyPI, Composer, or other registries.
- Use source access for secret discovery, dependency-confusion targeting, or trusted-publishing workflow reconnaissance.

## Defender heuristics

### Platform and browser IDE controls
- Treat browser IDEs and webviews as privileged developer applications, not simple static file viewers.
- Keep VS Code, browser VS Code services, and GitHub.dev patched; review vendor response notes for this class of issue before relying on browser IDEs for sensitive repositories.
- Prefer repository- or organization-scoped tokens for web IDE sessions where platforms support them.
- Restrict or disable arbitrary extension installation in browser-hosted developer environments for high-sensitivity organizations.
- Require extension allowlists and reviewed extension sources for both desktop and browser editor surfaces.

### Repository and identity monitoring
- Hunt for unusual GitHub OAuth app activity, new device/browser sessions, broad repository reads, mass clones, unexpected commits, and extension-install events if telemetry is available.
- Alert on source changes that add lifecycle hooks, GitHub Actions workflows, trusted-publishing configuration, package-manager registry changes, or AI-agent / IDE automation files.
- Review commits and pull requests made shortly after a developer opened an unfamiliar GitHub.dev link or rendered untrusted Markdown/notebook content.
- Rotate and revoke tokens only after preserving enough audit evidence to understand which repositories and workflows were touched.

### Developer guidance
- Do not open untrusted repository content, Markdown previews, or notebooks inside privileged browser IDE sessions tied to broad source-control access.
- Use separate low-privilege accounts or browser profiles for inspecting untrusted repositories.
- Treat unexpected extension-install prompts or editor notifications in GitHub.dev as suspicious.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Nx Console VS Code extension compromise](../ops/nx-console-vscode-extension-compromise.md)
- [Glassworm developer supply-chain botnet](../ops/glassworm-developer-supply-chain-botnet.md)
- [Agent skill marketplace poisoning](agent-skill-marketplace-poisoning.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)

## Sources
- [Ammar Askar](https://blog.ammaraskar.com/github-token-stealing/)
- [The Hacker News](https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html)
- [GitHub.dev project](https://github.com/github/dev)
