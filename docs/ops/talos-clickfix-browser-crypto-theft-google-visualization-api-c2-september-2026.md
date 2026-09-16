# ClickFix moves into the browser: cryptocurrency theft with Google-hosted C2

## Summary

On September 8, 2026, Cisco Talos (Sean Gallagher) reported a **criminal cryptocurrency-stealing campaign that abuses the Google Visualization API for command-and-control**, pulling obfuscated JavaScript from a **publicly published Google Sheets document** and injecting it into the victim's browser session. It is a **ClickFix variation that targets the browser instead of the OS**: instead of convincing targets to run shell commands, the actors get them to **paste JavaScript into the Chrome address bar** (early variant) or **install it via the Tampermonkey extension** (current variant, which also provides persistence).

The payload is a **web skimmer**: it hooks the browser `fetch` API, **replaces cryptocurrency deposit addresses in server responses and in the clipboard** with attacker-controlled wallets, and renders **counterfeit "bonus" interface elements** to make the fraud plausible. Lures pose as a **leaked vulnerability report describing a nonexistent API flaw at cryptocurrency swap services** ("~38% higher payouts," "25% loyalty bonus"), distributed via **Telegram, DarkForums, and paste sites** at users who hang out on crypto-trading, software-development, basic-cybersecurity, and hacking forums.

## Tags
- ops
- operations
- clickfix
- social engineering
- web skimmer
- javascript injection
- tampermonkey
- google visualization api
- google sheets c2
- cryptocurrency theft
- deposit address replacement
- fetch api hooking
- clipboard hijacking
- mutation observer
- xor obfuscation
- paste.sh
- simpleswap
- swapzone
- bitcoin bech32
- money laundering
- legitimate service abuse
- legitimate browser traffic
- browser-based c2
- detection

## Why this matters
- **Legitimate-service abuse inside the browser** defeats much of the usual hunting posture: the C2 traffic is ordinary HTTPS to `docs.google[.]com` *from the browser session itself*, so a "random executable phoning home to Google" tell does not apply — the requesting process is a trusted browser.
- It demonstrates a **fully serverless, cloud-hosted injection pipeline** (Google Sheets as payload storage, Visualization API as retrieval, Google Docs as lure, `paste[.]sh` as script host, Tampermonkey as persistence) that resists takedown: Talos' April disruption moved the campaign back online a week later on a new sheet, and even after Google blocked the documents they were re-reported-and-still-active as of August 11.
- The technique is **general web-skimming tradecraft**. The same DOM-mutation + `fetch`-override + clipboard-hijack pattern is directly transplantable to e-commerce and other customer-facing systems — and, per Talos, could be combined with the kind of broad web-application access TeamPCP-style operations sell.

## Campaign evolution
| Time | Change |
| --- | --- |
| Early Oct 2025 | Campaign begins: paste a script snippet into the **Chrome navigation bar** (`javascript:` prefix). First lure targets **SwapZone.io** with a fake ChangeNOW API flaw ("~38% higher payouts"). |
| Jan 2026 | Operators set up a **Telegram channel** (admin-only posts; older posts deleted on each re-post) to host the rotating "API Exploit" lure. |
| Mar 2026 | Moves to the **Google Visualization API** to deliver malicious scripts stored in a **Google Sheets** document. |
| Apr 12–16, 2026 | First observed lure document (Google Docs, filename "API Logic Flaw") active, targeting SwapZone. |
| Apr 18, 2026 | Lure revision retargets **SimpleSwap.io** with a fake "loyalty bonus" 25% boost; instructs installing the **Tampermonkey** extension from the Chrome Web Store and adding a `paste[.]sh` script to it. |
| Apr 19 – Jul 22, 2026 | Second lure document active; kept live **despite multiple reports to Google**. |
| Jul 2026 | After disruption of posts on shared text sites, **all campaign components moved into Google Docs and Google Sheets**. `paste[.]sh` begins auto-detecting scripts matching the first-stage signature. |
| Aug 11, 2026 | Talos reports the Google documents again; **still active** at time of writing. |

## How it works
1. **Lure**: a Google Docs "vulnerability report" describing a nonexistent swap-service API flaw that yields higher payouts, linked from Telegram posts, DarkForums DMs, and `pastebin`/text-share comments.
2. **First-stage loader** (from `paste[.]sh`):
   - V1 (SwapZone): pasted into the Chrome navigation bar; the script's Google-spreadsheet address is swapped for the fictitious vulnerable-API URL to construct the Visualization API call; it then scans the DOM for extension-associated `<script>` elements, picks one at random (or a random page `<script>` if none) and injects the second stage there.
   - V2 (SimpleSwap): pasted into **Tampermonkey**; the URL needed for the Visualization API call is **hidden inside the fake SimpleSwap API address, Base64-encoded after the string "bonus"**. The user-added script appends the payload whenever SimpleSwap loads — **persistence across sessions**.
3. **C2 / payload delivery**: the Google Visualization API (`https[:]//docs.google[.]com/spreadsheets/d/<id>/gviz/tq?...`) is an **unauthenticated, read-only** query interface into publicly published spreadsheets. The actors query **two cells** containing obfuscated JavaScript, concatenate them, and inject the reconstructed second stage. Because it is read-only, they cannot alter the sheet via the API — but a spreadsheet wired to a Google Forms page can accept **HTML POST** appends, which the post notes would make it a *full* C2. Changing the query or the target sheet is how they rotate infrastructure after disruption.
4. **Second-stage payload**: heavily obfuscated JavaScript (21 unique samples collected; mostly **XOR-encoded hex-pair arrays** with garbage math hiding the key, rotating keys and random identifiers consistent with **Obfuscator.io**; one sample Base64 + Unicode-escape, another XOR + Unicode apostrophe escaping). Payload cells were hidden with **white-on-white formatting** and pushed down the sheet as rows were added, discoverable only by text search or the API query.
5. **Skimming actions**:
   - **DOM/UI manipulation**: a `MutationObserver` monitors the page and dynamically replaces displayed deposit addresses; displayed transaction amounts are modified to fake the "bonus."
   - **Network interception**: overrides the browser **`fetch` API** to inspect and modify wallet/deposit endpoint JSON responses, replacing legitimate addresses with attacker-controlled ones. Intercepts form elements identified by `data-testid` selectors: `recipientAddressContainer`, `depositAddress`, `currencyList`, `cryptoExchangeTab`, `mainExchangeForm`.
   - **Clipboard hijacking**: when a user copies a deposit address, the copied value is replaced with an attacker wallet. A **rotating list of Bitcoin Bech32 addresses** is embedded in each script; one is picked randomly per substitution.
   - **Persistence**: periodic DOM re-scanning keeps the replacements alive through page updates; V2 additionally persists via the Tampermonkey-hosted loader.

## Financials and infrastructure
- **49 BTC wallet addresses** identified in the campaign; most April–June samples used an identical set of **30 addresses**, of which **24 received victim funds totalling 0.159 BTC (~$10,000 at early-August 2026 valuations)** — almost certainly a floor, since pre-April samples were unavailable.
- Outflow ran through **30 further wallets**, then into highly complex transactions spanning **3,000+ additional addresses** — consistent with a **Bitcoin mixing operation**.
- Targeted sites: **SwapZone.io** and **SimpleSwap.io** (Talos names SimpleSwap explicitly; both are cryptocurrency swap aggregators).

## Durable detection guidance
- **Browser-side** (endpoint/browser telemetry):
  - `javascript:`-prefixed content executed from the address bar (V1) or new user scripts in **Tampermonkey** / other userscript managers on non-corporate developer profiles (V2).
  - Runtime injection into extension-associated or page `<script>` elements from user-initiated navigation.
  - `fetch`/XHR response modification on wallet or deposit endpoints; clipboard writes that diverge from the displayed value.
- **Network-side**:
  - Browser sessions making **`/gviz/tq`** requests against `docs.google[.]com` spreadsheet endpoints — a Visualization-API call from a browsing context is a strong signal; `pastebin`/`paste[.]sh` fetches in the same session are corroborating.
  - Note the caveat: the requests look like **legitimate browser traffic to a trusted domain** — process/DNS tells used for file-based Google Sheets C2 do not transfer to in-browser use.
- **Content/OSINT**: the lure is a Google Docs "API Logic Flaw" vulnerability report promising inflated swap payouts; rotating `paste[.]sh` first-stage scripts; Telegram channel re-posting cadence (~twice a month, older posts deleted).

## Related pages
- [UAC-0145 ClickFix / SmartAxe / CowardDuck](uac-0145-clickfix-smartaxe-cowardduck.md) — ClickFix delivery against the OS; this campaign is the browser-session variant.
- [Cloud Atlas: Google-service abuse](../actors/cloud-atlas.md) — background on abusing Google services for C2.

## Sources
- Cisco Talos (Sean Gallagher), "ClickFix moves into the browser: Cryptocurrency theft with Google-hosted C2," September 8, 2026: [https://blog.talosintelligence.com/clickfix-moves-into-the-browser/](https://blog.talosintelligence.com/clickfix-moves-into-the-browser/)
