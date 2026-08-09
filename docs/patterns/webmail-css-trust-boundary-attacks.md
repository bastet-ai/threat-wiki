# Webmail CSS trust-boundary attacks

## Summary
PortSwigger Research documented a set of attacks that abuse HTML and CSS accepted by webmail clients. The research covers parser and sanitizer discrepancies, CSS Object Model (CSSOM) mutation, image-proxy bypasses, UI gadgets, click interception, token exfiltration, indirect prompt injection, and password capture. Testing involved Outlook, Gmail, Fastmail, Proton Mail, Yahoo Mail, and AOL Mail, with browser-specific behavior in Chrome and Firefox.

The durable lesson is that “JavaScript removed” does not make attacker-authored email markup passive. CSS selectors, pseudo-elements, browser requests, custom attributes, and application JavaScript that transforms sanitized markup can create state, observe secrets in the rendered document, influence trusted interface controls, and move data across the network.

This is vulnerability research and proof-of-concept work, not evidence that the techniques were used maliciously. Fix status varies by product and technique: Fastmail fixed the reported CSSOM mutation issues; the researcher observed Proton Mail silently fix one image-proxy bypass; and the publication says Gmail's `image-set()` request path and an Outlook label-based UI action remained reproducible at publication. Do not generalize one vendor's status to every chain in the paper.

## Tags
- patterns
- webmail
- CSS
- HTML sanitization
- CSS sanitization
- CSSOM
- mutation attacks
- image proxy bypass
- UI redressing
- click interception
- credential theft
- token theft
- indirect prompt injection
- email security
- Outlook
- Gmail
- Fastmail
- Proton Mail
- Yahoo Mail
- AOL Mail
- Firefox
- Chrome
- PortSwigger Research

## Attack classes
### Allowed-markup abuse
HTML elements that appear harmless can retain browser or application behavior. PortSwigger used `label` elements and their `for` attributes to target form controls in trusted webmail UI. Pseudo-elements such as `::before` and `::after` can display attacker-controlled content and inherit click behavior from the targeted element. This can turn a message body into a control surface for actions outside the message.

The same rendered-versus-machine-readable mismatch can affect AI tools. PortSwigger used CSS-generated and visually hidden text in a Fastmail message to change what OpenAI Atlas interpreted when the user requested a translation. The proof of concept induced browser-tab requests encoding the victim's name. This shows that an email's visible text is not necessarily the text an agent or accessibility/rendering pipeline consumes.

### Clipboard-to-draft CSS injection
The researchers observed a race condition when HTML clipboard content containing CSS was pasted into Yahoo Mail or AOL Mail drafts in Firefox. The injected CSS could inspect links in the draft with attribute selectors and trigger external background requests. The proof of concept reconstructed a 12-character Medium email-login token from the draft, enabling account takeover.

The prerequisite is not merely receiving an email: the victim must paste attacker-influenced rich clipboard content into a vulnerable editor, and the target token must be present in selector-visible markup. Browser clipboard parsing differed: Safari dropped the tested styles, Chrome rewrote them, and Firefox preserved behavior useful to the exploit.

### Exfiltration despite restrictive CSP
PortSwigger also showed CSS-only techniques that do not initially require an external resource. CSS generated candidate links, used font metrics and animation state to infer a numeric token's digit composition, then placed the matching link over the interface so a later click carried the result out. A restrictive Content Security Policy can therefore reduce direct egress without eliminating UI-mediated exfiltration.

### Image-proxy bypasses and agent chaining
The paper documents multiple ways to cause remote requests despite webmail image controls:

- Fastmail's same-origin image proxy path could be reached through CSS URL parsing tricks in the reported test.
- Proton Mail accepted a malformed nested URL construction that revealed the viewer's IP address; the researcher later found the behavior silently fixed.
- Gmail's sanitizer allowed an `image-set()` fallback request according to the publication.

PortSwigger combined the Gmail behavior with an indirect prompt injection against Anthropic Cowork's Gmail connector. An attacker email instructed the agent to find a Slack token and place it in a draft whose CSS made the outbound request when the draft was viewed. The agent did not need to send the email; creating attacker-controlled active content inside the trusted draft boundary was sufficient.

### CSSOM mutation and application gadgets
Some applications parse attacker CSS with the browser, inspect the CSSOM, then serialize a supposedly safe result. Browsers can decode escapes or normalize rule text during that round trip. PortSwigger found Chrome transformations that changed allowed keyframe or media-query text into selectors capable of escaping Fastmail's message-specific prefix. Fastmail fixed both reported mutation paths.

Outlook also allowed custom data attributes that application JavaScript later converted into new DOM and style properties. PortSwigger calls these **CSS gadgets**: application behavior adds a capability that the sanitizer itself attempted to deny. Combined with sanitizer parsing discrepancies, the research obtained page-wide styling control.

### UI takeover and password capture
With CSS control over trusted UI, the paper demonstrates **CSS hotwiring**: pseudo-elements and stacking place an existing control's click action over the page so ordinary clicks perform unintended actions. The Outlook proof of concept combined a CSS gadget, sanitizer bypass, labels, select elements, `:checked` state, browser timing behavior, and external background requests to create a spoofed login surface and capture password characters in Firefox.

This is not a conventional JavaScript keylogger. It depends on allowed HTML/CSS primitives, application gadgets, browser-specific select behavior, and network requests. Blocking scripts alone does not address it.

## Defender heuristics
### Isolate untrusted email
- Render message bodies in sandboxed, origin-isolated frames rather than the same DOM and origin as mailbox controls. Deny forms, popovers, navigation, downloads, and top-level interaction unless explicitly required.
- Use strict HTML and CSS allowlists. Remove `label[for]`, `select`, `option`, custom application attributes, pseudo-element content, stateful selectors such as `:checked`, `:has()`, `:focus`, and network-capable properties unless there is a demonstrated need.
- Do not permit attacker markup to target stable IDs or classes used by trusted UI. Randomization is defense in depth; isolation is the stronger boundary.

### Avoid sanitizer/parser differentials
- Test the exact parse-filter-serialize-render pipeline in every supported browser. Fuzz escaped identifiers, media rules, keyframes, comments, custom properties, nesting, malformed URLs, and newly implemented CSS/HTML features.
- If filtering CSSOM output, reject unexpected characters after browser normalization and reparse the serialized result under the same policy. Treat mutation between source, CSSOM, and final DOM as a security failure.
- Inventory application JavaScript that reads custom attributes or message DOM and appends elements, styles, event behavior, URLs, or trusted components. Evaluate these as gadgets that can reintroduce denied capabilities after sanitization.

### Constrain egress and previews
- Proxy all remote message resources through a service that strips credentials, normalizes URLs, prevents redirect escapes, partitions caches, and does not reveal the reader's IP or identity. Do not treat an allowlisted same-origin proxy path as inherently safe.
- Block remote requests from drafts and generated previews by default. A message or agent-created draft should not become active network content merely because a user opens it.
- Apply CSP as defense in depth, but account for user-click navigation, same-origin proxy endpoints, browser-mediated fetches, and trusted-domain abuse.

### Protect AI email workflows
- Treat message HTML, generated CSS content, hidden text, attachments, quoted threads, and connector results as untrusted input to an agent.
- Prevent email agents from copying secrets or authentication codes into HTML drafts, URLs, images, styles, or external destinations. Require destination-aware approval before reading one message and writing content derived from it elsewhere.
- Compare agent-visible extracted text with the user-visible rendering and flag large hidden or generated instruction blocks.

### Hunt and respond
- Alert on webmail-origin requests to first-seen domains, URLs containing token-like values, bursts that enumerate character combinations, unusual image-proxy paths, and draft-view events immediately followed by external fetches.
- Look for messages or drafts containing `label[for]`, `select`/`option` structures, `image-set()`, nested attribute selectors, network-valued `background` properties, pseudo-element `content`, keyframes, unusual media queries, escaped identifiers, or CSS attempting `position: fixed` and high `z-index` values.
- Preserve raw MIME, decoded HTML, clipboard provenance where available, sanitizer input/output, final DOM/CSSOM, browser and product versions, CSP violations, proxy logs, DNS/network telemetry, and agent traces before removing content. Revoke exposed login links, tokens, sessions, and passwords; deleting the message does not invalidate copied credentials.

## Validation boundaries
Use synthetic messages, non-production accounts, owned domains, and fake tokens. Do not test external-request or account-takeover chains against another person's mailbox or use real authentication links as CSS-exfiltration targets.

## Related pages
- [AI browser-extension confused deputy](ai-browser-extension-confused-deputy.md)
- [Atlassian Rovo prompt-to-data exfiltration](atlassian-rovo-prompt-to-data-exfiltration.md)
- [ModHeader browser-extension surveillance capability](../ops/modheader-browser-extension-surveillance.md)

## Sources
- PortSwigger Research: [CSS: the bomb inside your inbox](https://portswigger.net/research/css-the-bomb-inside-your-inbox) (2026-08-06)
- PortSwigger proof-of-concept repository: [css-the-bomb-inside-your-inbox](https://github.com/portswigger/css-the-bomb-inside-your-inbox)
