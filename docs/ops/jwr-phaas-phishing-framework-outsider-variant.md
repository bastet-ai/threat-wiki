# JWR phishing framework (likely The Outsider variant)

## Summary
Cisco Talos identified an undocumented phishing framework, internally branded **JWR** by its developer, that impersonates checkout and login pages for major payment and shopping platforms (Shopify, PayPal, Apple, Klarna, banks). Unlike a static credential-stealing page, the JWR client engine keeps a live **AES-CTR encrypted WebSocket** open to the operator so each victim's session can be steered in real time. It harvests payment data, identity documents, Social Security numbers, passport/driver's-license images, site and PayPal credentials, 2FA codes, and full device fingerprints — all committed to the actor's server when a session ends.

Talos assesses with **medium confidence** that JWR is a variant of **The Outsider** phishing-as-a-service platform, based on shared client-engine scripts and functionality between the two PhaaS platforms.

## Tags
- ops
- operations
- phishing
- phishing-as-a-service
- credential-theft
- payment-card-theft
- PII theft
- identity theft
- 2FA harvesting
- WebSocket
- real-time operator control
- brand-impersonation
- smishing
- SMS phishing
- Southeast Asia
- Middle East
- The Outsider
- Outsider Enterprise
- PhaaS
- cvvform

## Why this matters
- JWR turns a phishing page into an interactive, operator-driven session: the attacker can watch keystrokes, redirect the victim, and re-target in real time rather than relying on one-shot form capture.
- The data schema (`cvvform`) spans financial and identity-theft: card number, CVV, PIN, expiry, SSN, passport/ID images, 2FA codes, site logins, and PayPal credentials — a single compromise can fund both payment fraud and identity takeover.
- Delivery was observed via **SMS lures impersonating toll authorities and postal/courier services** across Southeast Asia and the Middle East, tying the framework to a smishing (SMS-phishing) initial-access channel.
- If JWR is a variant of The Outsider, it extends the PhaaS surface already tracked in the [Outsider Enterprise smishing PhaaS](outsider-enterprise-smishing-phaas.md) page, giving operators a shared client-engine fingerprint to cluster.

## Reported architecture
- **Host Bridge module**: an immediately-invoked function expression (IIFE) that runs in the parent phishing page (typically a replica of a legitimate checkout/login page). It relays received details into a child iframe holding the real phishing form and maintains the persistent WebSocket to the actor's C2.
- **Vue.js victim application**: renders across **44 phishing HTML pages**, streams the victim's keystrokes to the actor as typed, and executes more than **40 distinct C2 instructions**.
- Execution is gated on the global flag `window.__HOST_MODE`:
  - Set → **Host Mode** (Host Bridge path).
  - Unset → **Content Mode** (Vue.js application path), which has three communication modes: standalone, `pluginIframe`, and `hostIframe`.
- Exfiltration uses a `cvvform` object (credit-card fields, SSN, ID images, 2FA codes, logins, PayPal credentials, device fingerprint) sent to C2 at session end.

## Reported chain
1. Victim receives an SMS lure impersonating a toll authority, postal, or courier service (Southeast Asia / Middle East).
2. The link loads a JWR client page impersonating a trusted checkout/login flow.
3. The client engine opens an AES-CTR encrypted WebSocket to the actor's C2 and renders the phishing flow (44 pages, keystroke streaming, 40+ C2 instructions).
4. The operator steers the session live, harvesting payment + identity data into the `cvvform` object.
5. On session end the collected data is committed to the actor's server.

## Defender heuristics
- Treat unsolicited SMS links for tolls, postal/courier exceptions, account alerts, and payment claims as hostile; verify through the official app or a typed domain.
- Cluster new payment/checkout phishing URLs by page-template similarity, host, kit artifacts, and repeated lure copy rather than only the impersonated brand — JWR-style kits share a common 44-page engine.
- Hunt for persistent WebSocket connections from browser sessions to non-first-party C2 hosts with AES-CTR framing; static form-capture pages do not hold a live encrypted channel.
- For brand-protection and telecom-abuse teams, look for real-time operator steering signatures (keystroke streaming, mid-session redirects, 40+ instruction round-trips) that distinguish a live PhaaS session from a dead credential page.
- Correlate JWR infrastructure against The Outsider / Outsider Enterprise client-engine fingerprints to determine whether these are the same operator or a shared PhaaS lineage.

## Related pages
- [Outsider Enterprise smishing PhaaS](outsider-enterprise-smishing-phaas.md)
- [Hunt.io global smishing infrastructure campaign](huntio-global-smishing-government-postal-telecom.md)
- [Chinese-language PhaaS wallet-tokenization ecosystem](chinese-language-phaas-wallet-tokenization.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Cisco Talos: [Dissecting the JWR phishing framework](https://blog.talosintelligence.com/dissecting-the-jwr-phishing-framework/) — August 13, 2026
