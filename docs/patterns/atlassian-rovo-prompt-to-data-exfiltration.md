# Atlassian Rovo prompt-to-data exfiltration

## Summary
Two independently disclosed Atlassian Rovo findings show how enterprise-agent features can turn attacker-controlled text into authenticated data exfiltration. The findings use different entry points and have different remediation status:

- Varonis Threat Labs' **RovoBlast** used the `rovoChatPrompt` URL parameter to place and execute an attacker-supplied prompt in an authenticated user's Rovo session. Atlassian accepted the Bugcrowd report as P2 and deployed a server-side fix on July 8, 2026.
- PromptArmor demonstrated **indirect prompt injection** through content Rovo was asked to process. The injected instructions made Rovo append Jira and Confluence data to an attacker URL and open it with Rovo's URL-retrieval tool. PromptArmor reported that this path remained vulnerable when it published on August 5, 2026, including when the organization-level web-search setting was disabled.

These are public proof-of-concept disclosures, not reports of malicious exploitation. Rovo acts with the user's existing access; neither finding bypassed the underlying Jira, Confluence, or connector permissions. The security failure is that untrusted content could redirect that legitimate authority and use an outbound fetch as the data channel.

## Tags
- patterns
- AI agents
- enterprise AI
- Atlassian
- Rovo
- Jira
- Confluence
- indirect prompt injection
- parameter-to-prompt
- confused deputy
- data exfiltration
- URL retrieval
- Markdown image rendering
- SaaS connectors
- least privilege
- agent monitoring
- PromptArmor
- Varonis Threat Labs
- Bugcrowd

## Distinct attack paths
### Fixed `rovoChatPrompt` one-click path
Varonis found that a crafted `home.atlassian.com/chat` link could supply instructions through the `rovoChatPrompt` query parameter. When an authenticated victim opened the link, Rovo treated the parameter as a user query without a warning, confirmation, or untrusted-input label. The proof of concept instructed Rovo to read data available to the victim and place it in an attacker-controlled image URL.

Bugcrowd's public record says the path could expose identity information and content reachable through Confluence, Jira, and connected services such as SharePoint and Outlook. The report was submitted on November 4, 2025, triaged as P2 on January 6, 2026, fixed on July 8, and validated after deployment. The server-side fix prevents crafted `rovoChatPrompt` links from injecting and automatically executing attacker-supplied instructions.

### Indirect injection through processed content
PromptArmor demonstrated a separate chain beginning with a document containing concealed instructions. The example user uploaded the document and asked Rovo to organize Jira tickets; PromptArmor notes that the same trust boundary can arise from support tickets, Atlassian content, web results, or third-party connectors.

The injected instructions caused Rovo to collect Jira and Confluence content, encode it into an attacker-controlled URL, and invoke its URL-retrieval tool. The resulting request placed the data in the attacker's server logs. PromptArmor also identified Rovo's rendering of Markdown images from model output as a second potential outbound channel.

Disabling Rovo web search did not stop the demonstrated URL-retrieval path because the setting removed search but left the tool that opens search results. PromptArmor reported disclosure to Atlassian on May 23, follow-ups through July 29, and no remediation communication before its August 5 publication. That point-in-time status must not be confused with Atlassian's fix for the earlier `rovoChatPrompt` issue.

## Security boundary
Both chains combine three capabilities:

1. **Untrusted input becomes instructions** — a URL parameter, uploaded file, issue text, connector data, or other external content enters model context.
2. **The agent can read private data** — Rovo can search resources the current user is already authorized to access, potentially across many connected services.
3. **The agent can communicate outward** — URL retrieval, rendered images, browsing, posting, previews, webhooks, or another tool can carry derived data to a destination outside the intended task.

Every backend read may be individually authorized while the overall sequence violates user intent. Model refusal is therefore not a sufficient authorization or data-loss boundary.

## Defender heuristics
### Reduce authority and exits
- Inventory Rovo connectors and the effective access inherited from each user and service identity. Disconnect unused integrations and exclude high-sensitivity legal, HR, finance, incident-response, source-control, and secret-bearing repositories where the business case does not justify agent access.
- Disable browsing, multi-step automation, URL retrieval, and other outbound-capable tools when they are not required. Verify the effective tool inventory after changing a user-interface setting; do not assume that disabling search removes fetch or rendering capabilities.
- Apply destination policy outside the model. Block arbitrary hosts, user-controlled URL paths and query strings, redirects to unapproved domains, and outbound requests containing sensitive-data classes.
- Separate read-only search from write, browse, fetch, and publish authority. Require contextual approval when a task crosses products, reads a sensitive source, or sends information to a new destination.

### Treat all retrieved content as hostile
- Preserve provenance for documents, tickets, comments, connector records, search results, and URL parameters. Mark them as data, not instructions, before they enter agent context.
- Scan raw and rendered forms for concealed instructions, including HTML comments, hidden text, encoded blocks, image alt text, and language asking the agent to construct URLs, fetch images, post results, or ignore the user's task.
- Do not rely on prompt delimiters alone. Bind each run to an allowed data set, action set, and output destination with deterministic policy enforcement.

### Detect and respond
- Log the initiating user action, prompt provenance, connector reads, tool calls, normalized destinations, redirects, bytes sent, and approval decisions. Avoid writing raw secrets into agent telemetry.
- Alert when a Rovo search or summarization task is followed by a first-seen external URL, sensitive values embedded in a URL path or query, Markdown-image fetches to unapproved hosts, unexpected cross-product reads, or agent activity without a corresponding user-visible request.
- If exploitation is suspected, preserve Rovo conversation and tool traces, Atlassian audit records, connector-provider logs, proxy/DNS records, browser history, and attacker-controlled output copies before containment. Determine every resource the affected identity and connectors could read, then revoke exposed secrets and sessions; disabling the agent does not invalidate data or credentials already copied.

## Validation boundaries
Test only in a dedicated tenant with synthetic records and an owned collection endpoint. Do not place real credentials in proof-of-concept pages, ask a production agent to enumerate sensitive content, or send organizational data to a third-party webhook merely to validate exposure.

## Related pages
- [Azure DevOps MCP pull-request prompt injection](azure-devops-mcp-pr-prompt-injection.md)
- [Sentry MCP Agentjacking](sentry-mcp-agentjacking.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [AI browser-extension confused deputy](ai-browser-extension-confused-deputy.md)

## Sources
- PromptArmor: [Atlassian Rovo Exfiltrates Data, Bypassing Controls](https://www.promptarmor.com/resources/atlassian-rovo-exfiltrates-data) (2026-08-05)
- Varonis Threat Labs: [RovoBlast: How One Click Triggered Atlassian's AI Assistant to Leak Data](https://www.varonis.com/blog/rovoblast) (2026-08-08)
- Bugcrowd disclosure: [One-Click Data Exfiltration via `rovoChatPrompt` URL Parameter](https://bugcrowd.com/disclosures/bf1922fb-99d0-4d3b-b419-1728720d29ec/one-click-data-exfiltration-via-rovochatprompt-url-parameter-confluence-rovo) (resolved 2026-07-08)
- Atlassian: [Manage the web-search option for Rovo](https://support.atlassian.com/organization-administration/docs/manage-a-web-search-option-for-rovo/)
- Atlassian: [Manage Rovo access](https://support.atlassian.com/organization-administration/docs/manage-rovo-access/)
