# PhantomRaven: an LLM-generated npm information stealer built by a bug bounty hunter to farm "compromises" for payouts (CrowdStrike Counter Adversary Operations, Sep 15, 2026)

## Summary

CrowdStrike Counter Adversary Operations published (September 15, 2026; Axios ran an exclusive a day earlier) its analysis of **PhantomRaven**, a JavaScript information stealer distributed through **typosquatted npm packages** whose operator CrowdStrike identifies with high confidence as a **self-proclaimed bug bounty hunter** — active on Bugcrowd, Intigriti, YesWeHack, HackenProof, and HackerOne since November 2022, with bounties from at least nine entities across technology, retail, and hospitality. The operator's model is an inversion of the disclosure economy: **infect a target with your own malware via the npm supply chain, then email the victim claiming to have "discovered" the compromise, and monetize the manufactured finding through bounty programs.** CrowdStrike assesses the stealer's code was **almost certainly LLM-generated** (statistical token analysis, verbose redundant comments, placeholder code such as a hardcoded `wss://yourserver[.]com/socket` fallback), and the author's technical sophistication as **likely low**.

The delivery mechanism is exactly the vector npm v12's June 2026 install-script defaults were built to stop: a typosquatted package with minimal clean code declares its malicious dependency as an **HTTP URL** rather than a registry reference; the fetched package carries a `preinstall` script that executes at install time. On npm ≥ 12 the script is **blocked and surfaced for explicit approval** — the report uses this live campaign to show why the old npm is now the exposure. Two infected-package publishers were identified in Falcon Complete incidents — `transform-jsbi-to-bigint` (npm user `jpdhellonpm1`) and `sort-imports-es6-autofix` (npm user `jpd15`) — both usernames containing the `JPD` string from the operator's victim-contact email; **both names now resolve only to GitHub security-team `0.0.1-security` reservation versions, confirming registry takedown**. C2 ran through `npm[.]jpartifacts[.]com`, reached via **remote dynamic dependency (RDD)** links embedded in the actors' published files. The payload collects host identity, Git/npm config credentials, **CI/CD environment variables for GitHub Actions, GitLab CI, Jenkins, and CircleCI**, and exfiltrates via HTTP GET/POST with a stub WebSocket fallback. CrowdStrike has **not observed PhantomRaven logs for sale in log shops** — the stealer's output feeds bounty submissions, not data markets.

## Tags
- tools
- malware
- infostealer
- npm
- supply-chain
- typosquatting
- remote-dynamic-dependency
- RDD
- preinstall
- lifecycle-hooks
- LLM-generated-malware
- bug-bounty
- extortion-adjacent
- crowdstrike
- counter-adversary-operations
- jpd
- CI-CD-credentials
- dependency-confusion
- npm-v12
- install-time-execution
- JavaScript
- eCrime
- big-game-hunting

## What CrowdStrike observed

### The operator
- **Profile:** financially motivated threat actor who publicly works as a **bug bounty hunter**; active since **November 2022**; public X profile claims bounties from **at least nine entities** (technology, retail, hospitality) through **Bugcrowd, Intigriti, YesWeHack, HackenProof, HackerOne**.
- **November 2025 contact email:** the actor contacted a potential victim claiming to have identified a compromised device, attributing it to a **dependency-confusion attack using malicious npm packages** — the email username contains the string **JPD**, the pivot CrowdStrike used to tie the monikers together.
- **August 2025 claim:** the actor publicly claimed to have "discovered" an RCE via a malicious npm package they themselves published, describing a `preinstall` script achieving code execution on the target. CrowdStrike could not verify that specific claim but noted the November 2025 campaign exhibits the same techniques.
- **PyPI history:** in a GitHub issue thread on PyPI, a PyPI organization member **accused the actor of building an information stealer** after their near-name project upload was rejected (a name-similarity policy consistent with dependency-confusion prevention), and linked the actor's main project — since removed, but **associated Python stealer files remain publicly accessible**, mirroring the JS/npm tooling in Python/PyPI form.
- **Two-operator-moniker assessment (high confidence):** Falcon Complete MDR responded to multiple incidents and identified two npm packages containing PhantomRaven `preinstall` scripts — **`transform-jsbi-to-bigint`** (`jpdhellonpm1`) and **`sort-imports-es6-autofix`** (`jpd15`); files inside carry the actor's name and initials in description/author fields.
- **Related monikers industry sources associate with the same deployments:** `jpd12`, `jpd13`, `npmhell`, `npmpackagejpd`, `npmtestdharsh`, **`jpdhackerone11`** (name references the bounty platform the actor claims to use), `packagedharsh`.
- **No log-shop listings observed** — CrowdStrike assesses the operator uses the stealer **solely to identify bug bounty opportunities**.

### Delivery chain
1. Publish **typosquatted npm packages** containing minimal, non-malicious code (typically a "Hello, world!" script) — nothing to flag in the package listing itself.
2. Declare the dependency as an **HTTP URL** (remote dynamic dependency) instead of a registry reference → at install, npm fetches the real payload from **attacker-controlled infrastructure** (`npm[.]jpartifacts[.]com`, also embedded as RDD links in files across the actors' published packages).
3. The fetched package carries a **`preinstall` script** → automatic execution during `npm install` on legacy npm.
4. **npm ≥ 12 (June 2026 GA)** blocks dependency-lifecycle scripts by default and shows `npm install-scripts ls / approve` — CrowdStrike's screenshots demonstrate the campaign against the new warning flow; on npm 12+ the attack requires the developer to explicitly approve the blocked script.

### Payload behavior (`PhantomRaven`)
- Collection: local/external IP (via `https[:]//api64[.]ipify[.]org?format=json`), OS/architecture/hostname/Node.js version/PID/CWD, timezone/language, **usernames and emails from Git and npm configuration files**, environment variables, and **CI/CD variables for GitHub Actions, GitLab CI, Jenkins, and CircleCI** — likely hunting account credentials/tokens.
- Exfiltration: **both HTTP GET (query-string encoded) and POST (JSON body)** — dual redundant methods CrowdStrike reads as an LLM artifact; minimal user-agent `Mozilla/5.0 (Windows NT 10.0; Win 64; x64)` missing browser/version tokens; an **incomplete WebSocket fallback** hardcoded to `wss[:]//yourserver[.]com/socket` (placeholder, not live infrastructure).
- **LLM-generation indicators (high confidence):** statistical token-analysis patterns, a comment before **every** global and function definition redundant with the symbol name, placeholder code, and the redundant dual-exfil design. CrowdStrike: author sophistication **likely low** — the LLM is the developer.
- Sample SHA-256s published: `c31831d47fcbf52ff1f4e61838611916a4276d005a564e69946d5dac04235eed`, `95a7dcc6de46826b22c43bee7fc550f3b5e2e6cbc5f33b0c241faf523641cf63`, `db3fe46df0a65fe9f8c99d2e11126a032a72e9814e354ce017448ce088a01e02`.
- ATT&CK highlights: T1195.001 (compromise software dependencies), T1587.001 (develop capabilities: malware), T1583.001 (acquire domains), T1059.007 (JavaScript), T1552.001/.007 (unsecured credentials in files / container API), T1027.009 (payloads embedded behind HTTP-URL dependencies invisible in npm's web UI), T1036.005 (name masquerading), T1071.001 (web-protocol C2).

## Why this matters

- **The adversary model is new even if the mechanics are old.** Manufacturing the vulnerability you then "discover" converts supply-chain malware into **bounty income**, laundering intrusion through legitimate disclosure platforms. It inverts the trust that bounty programs and their platforms place in researcher submissions — and it means **a "responsible disclosure" email citing an npm dependency-confusion compromise can itself be the second stage of the attack** (social proof that the researcher "found" your breach).
- **A real-world campaign is the clearest justification yet for npm v12 defaults.** CrowdStrike explicitly ties the infection path to pre-npm-12 automatic `preinstall` execution and recommends upgrading — concrete evidence for the [npm install explicit-trust controls pattern page](../patterns/npm-install-explicit-trust-controls.md).
- **Low-skill actors now ship functional malware via LLMs.** This converges with CrowdStrike's own observation of TRAVELING SPIDER affiliates and PUNK SPIDER deploying AI-generated tooling, and with Unit 42's AI-enabled-malware census: the barrier to developing proprietary eCrime malware is collapsing. The durable detection angle is the artifact, not the sophistication — LLM-generated code has recognizable texture (comment-before-everything, placeholder infra, redundant fallbacks).
- **Distinct from TeamPCP/Shai-Hulud financially-motivated waves:** no extortion, no log resale, no worm propagation — a solo operator farming bounties. But the shared substrate (typosquats, RDD over HTTP URLs, preinstall execution, CI/CD credential harvesting) means defender detections for the big worms largely cover this actor too.

## Defender heuristics
- Update to **npm 12+** fleet-wide and keep install-script blocking on; audit any host still approving `preinstall`/`postinstall` scripts on third-party dependencies (`npm install-scripts ls`).
- Block or alert on **HTTP(S) URL dependencies** in `package.json`/lockfiles (`--allow-remote` stays off by default); treat any `"dependency": "https://..."` as a likely RDD malware pattern.
- Hunt the low-effort tells: packages whose own code is a near-empty placeholder while `dependencies` resolve to raw URLs; publisher accounts whose package names/usernames carry personal initials or bounty-platform references.
- Treat **CI/CD environment-variable harvesting** as the payload's real objective: scope what tokens a developer-machine or runner `preinstall` script could read, and prefer short-lived OIDC/OIDC-style identities over long-lived env-injected CI secrets.
- For **bug bounty intake teams**: add an authenticity check for submissions that claim active compromise — verify with independent IR before engaging, and be alert to reporters who describe attacker tradecraft they "shouldn't" know.
- Screen vendor/"researcher" outreach claiming to have found a device compromise: validate the technical claim internally; never grant access or send payment details to the claimed finder.
- Detection pivots from the report: outbound requests to `ipify` immediately followed by bulk env-var exfiltration, the minimal `Mozilla/5.0 (Windows NT 10.0; Win 64; x64)`-only user agent, and install-time Node processes reading `~/.gitconfig`, `~/.npmrc`, and CI env vars.

## Timeline
- **November 2022 (earliest):** operator active as self-described bug bounty hunter.
- **August 2025:** actor publicly claims RCE "discovered" via their own malicious npm package.
- **November 2025:** victim-contact email claiming dependency-confusion compromise; incidents using `npm[.]jpartifacts[.]com` as C2.
- **December 2025:** CrowdStrike identifies the actor's GitHub account; PyPI org member's stealer accusation surfaces the removed Python variant.
- **June 2026:** npm v12 GA ships install-script blocking by default, degrading the campaign's automatic-execution path.
- **September 15, 2026:** CrowdStrike Counter Adversary Operations publishes the PhantomRaven analysis (Axios exclusive Sep 15; broad pickup Sep 16). Both malicious package names now carry only `0.0.1-security` GitHub security-lab reservation versions — packages removed from npm.

## Monitor
- Whether the operator submits further "findings" to bounty platforms and whether any program detects or expels them.
- Adoption of the manufactured-compromise-for-bounties model by other low-skill actors (the model is copyable from the public writeup itself).
- Infrastructure rotation away from `npm[.]jpartifacts[.]com`; new publisher monikers following the `jpd*`/`*dharsh` naming pattern.
- Whether bounty platforms (HackerOne, Bugcrowd, Intigriti, YesWeHack, HackenProof) respond with policy or account action.
- npm enforcement against HTTP-URL dependency malware and whether actors migrate to Git-URL dependencies (`--allow-git` path) or import-time execution to evade the v12 defaults.

## Sources
- CrowdStrike Blog — "PhantomRaven: An LLM-Generated Information Stealer Developed for Bug Bounty Hunting" (September 15, 2026): <https://www.crowdstrike.com/en-us/blog/phantomraven-llm-generated-information-stealer-for-bug-bounty-hunting/>
- Axios — "Exclusive: AI-written malware helped a hacker cash in on bug bounty programs" (September 15, 2026)
- Related wiki pages: [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md), [CrowdStrike source entry](../notes/source-index.md)
