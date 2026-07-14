# AI browser-extension confused deputy

## Summary
Manifold Security reported on July 14, 2026 that Anthropic's **Claude for Chrome** browser extension remained vulnerable in version `1.0.80` to a browser-extension confused-deputy path they call **ClaudeBleed Reopened**. A separate Chrome extension with a content script on `claude.ai` could inject a DOM element and dispatch a synthetic click that causes Claude for Chrome to run one of its built-in browser-agent prompts against the victim's Google Workspace context.

The durable defender lesson is not limited to Claude: agentic browser extensions create a privileged automation deputy that other extensions, web pages, and UI-manipulation bugs may be able to steer. Treat browser-agent extensions as high-risk access brokers for mail, documents, calendars, SaaS sessions, and admin consoles.

## Tags
- patterns
- AI browsers
- AI agents
- browser extension
- confused deputy
- indirect prompt injection
- excessive agency
- Claude for Chrome
- Anthropic
- Google Workspace
- Gmail
- Google Docs
- Google Calendar
- SaaS data access
- browser security
- agentic browser

## What Manifold reported
Manifold said two issues remained reproducible after disclosure to Anthropic in May 2026 and after eight Claude for Chrome releases:

1. **Cross-extension steering:** any browser extension with a content script on `claude.ai` could inject the expected DOM trigger and synthesize a click. In Manifold's proof path, this could make Claude execute one of nine predefined prompts that read Gmail, Google Docs, and Calendar content.
2. **Privileged side-panel initialization:** the Claude side panel initialized in privileged mode when loaded with `?skipPermissions=true`. Manifold framed this as an architectural weakness because any URL-construction or navigation bug could become a silent-execution route.

Manifold rated the first path as high severity in default mode because the user may still see a coerced approval step, and critical if the user has enabled **Act without asking**, because execution can become silent. They emphasize that the behavior is model-independent: the issue is in extension trust boundaries and UI/permission handling, not in a specific LLM's reasoning.

## Why this matters
- Browser agents sit inside already-authenticated browser sessions. If a hostile extension can steer the agent, the blast radius can include SaaS data even when the hostile extension itself lacks direct Google Workspace permissions.
- Browser-extension permission models are compositional. A low-visibility extension granted access to `claude.ai` may indirectly reach whatever Claude for Chrome can browse, summarize, or act on.
- "Approval" prompts are weak mitigations when the attacker controls the surrounding UI state, can choose benign-looking predefined prompts, or can exploit prior user choices such as "Act without asking."
- This pattern generalizes to AI browsers, side panels, desktop-browser assistants, and enterprise browser plugins that bridge from web content into privileged automation.

## Defender guidance
1. Inventory AI browser extensions separately from ordinary productivity extensions; track extension ID, version, permissions, update channel, and whether autonomous modes such as "Act without asking" are enabled.
2. Prefer deny-by-default extension allowlists for browsers used with mail, documents, source control, cloud consoles, finance apps, and admin SaaS.
3. Treat `claude.ai` and other agent-control origins as sensitive extension targets. Avoid allowing unrelated extensions to inject content scripts into those origins.
4. Disable or centrally prevent silent/autonomous execution modes for browser agents in managed environments until per-site and per-action policy controls are mature.
5. Monitor for new or rarely used extensions receiving host permissions on agent-control origins, especially `claude.ai`, `chatgpt.com`, AI-browser side-panel origins, and internal assistant portals.
6. For incident response, include browser-extension inventories, extension update histories, browser profiles, agent conversation logs, Google Workspace access logs, and OAuth / session-token activity in the same timeline.
7. Separate high-risk SaaS administration into hardened browser profiles where general-purpose and AI-agent extensions are not installed.

## Detection pivots
- Chrome extension inventory changes adding `claude.ai` host access, broad content-script matches, or `<all_urls>` permissions.
- Claude for Chrome version `1.0.80` or earlier in environments where mail/document/calendar access is available.
- Browser-agent prompts that access Gmail, Docs, or Calendar shortly after installation, update, or activation of an unrelated browser extension.
- User-agent / browser profile telemetry showing agent side-panel access with `skipPermissions=true` in the URL.
- Unexpected Gmail / Google Docs / Calendar reads near extension UI events rather than user-initiated agent sessions.

## Related pages
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [BioShocking AI-browser context manipulation](ai-augmented-adversary-operations.md#bioshocking-ai-browser-context-manipulation)
- [ModHeader browser-extension surveillance capability](../ops/modheader-browser-extension-surveillance.md)
- [StegoAd Edge extension steganography campaign](../ops/stegoad-edge-extension-steganography-campaign.md)

## Sources
- Manifold Security: https://www.manifold.security/blog/claude-for-chrome-extension-bypass
- The Hacker News secondary coverage: https://thehackernews.com/2026/07/claude-for-chrome-flaw-lets-other.html
