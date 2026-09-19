# Hacktron "HEIF Heist": libheif image-parser bug in OpenAI's Discourse forum chained to employee ChatGPT/Codex account takeover and internal-repo access — exploit built within hours of Claude Opus 5's release ($6,500 bounty, Sep 18, 2026)

## Summary
Independent researchers at **Hacktron AI** disclosed on **September 18, 2026** (WSJ Thursday-evening report; TechCrunch, CyberScoop, VentureBeat, The Register, CBS, NBC, The Guardian same day) that they chained **two vulnerabilities in Discourse** — the third-party forum software powering **OpenAI's community forum** — to reach **OpenAI employee ChatGPT/Codex accounts and, through an employee's Codex connection, OpenAI's GitHub organization / internal "monorepo"** (proof of concept: an opened pull request). Entry point: a **memory-corruption bug in libheif**, the C library Discourse's image pipeline (via ImageMagick) hands Apple **HEIF/HEIC** files to for conversion; a crafted image "miscalculates where one image is positioned on top of another," enough to hijack the server. The bug **had already been fixed upstream months earlier but was never flagged as a security vulnerability and never got a CVE** — which the researchers say explains why Discourse still shipped the vulnerable version. Hacktron named the broader class **HEIF Heist**: malicious **HEIF/HEIC/AVIF** uploads against **libheif and libde265** decoders could yield **RCE or arbitrary heap disclosure ("heist" in-memory data: other users' data, environment variables)** across major platforms — they list **AWS, Meta's core product suite, GitHub Enterprise servers, and open-source Discourse** among exposed surfaces. The AI-development story is the sharpest durable tell: the team's **Opus 4.8 (cyber-access version) "struggled across several sessions to produce a working exploit"**; **"within hours of Opus 5's release, we gave it the same problem and it succeeded."** Research attribution is "**led** by the Hacktron human researchers **assisted by Hacktron Harness, GPT-5.6 Sol, and Opus 5**"; an agentic approach cut exploit development to **roughly 1–3 days from initial probe to remote RCE**, though some RCE attempts "landed only after thousands of image uploads." Timeline: flaw found **July 25**, researchers alerted OpenAI and Discourse, **Discourse issued a fix July 27**, OpenAI paid a **$6,500 bug bounty** and says both issues are resolved. Disclosed under OpenAI's bug-bounty program; no malicious exploitation reported.

## Tags
- ops
- libheif
- libde265
- HEIF
- HEIC
- AVIF
- image parsing
- memory corruption
- heap disclosure
- remote code execution
- Discourse
- OpenAI
- account takeover
- ChatGPT
- Codex
- GitHub organization
- monorepo
- supply-chain
- unpatched upstream fix
- no CVE
- ImageMagick
- AI-assisted exploit development
- Claude Opus 5
- frontier models
- bug bounty
- Hacktron AI

## Why this matters
- **The un-CVE'd fix gap is the actual vulnerability class.** A library maintainers' silent security fix that never gets a security advisory, a CVE, or a distro/vendor backport = every downstream shipper keeps running the vulnerable version indefinitely. This is the same propagation failure our [Next.js August 2026 page](nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md) documented from the other direction (a libheif GHSA with no CVE, upstream release unpublished, framework disabling AVIF as a stopgap). Image/codec parsers are where "we track CVEs, not upstream commits" quietly dies.
- **A public forum is a beachhead into the developer estate.** The chain runs community-forum image upload → forum-server RCE → **account-takeover flaw against logged-in users** → employee ChatGPT/Codex accounts → the employee's **Codex→GitHub-org connection** → internal repositories. As the researchers put it: "Until two months ago, a user or OpenAI employee logging into OpenAI's own help forum could have had their ChatGPT and Codex accounts taken over," and because users connect services to Codex/ChatGPT, the theoretical scope included "GitHub, Slack and emails." Help forums and community portals are SSO-connected, low-scrutiny, user-upload-accepting surfaces — treat them as production-adjacent.
- **Model capability changes exploit economics in public, timestamped steps.** Opus 4.8 failing and Opus 5 succeeding **on the identical problem**, within hours of release, is the cleanest public before/after yet for frontier-model exploit generation. The researchers' own framing (founder Mohan Pedhapati): "AI is reducing the amount of scarce expertise needed to develop exploits. Work that once took months can now take days." External commentary (Gray Swan CEO Matt Fredrikson, via TechCrunch): "For $200 a month, anyone can use these tools and hack into a company like OpenAI... it could happen to anyone." The model-capability-line question is already policy-relevant: Opus 5 shipped with no cyber export restrictions, while the newer Mythos 5 was temporarily locked down (see [Anthropic cyber-evaluation page](anthropic-cyber-evaluation-real-world-intrusions.md)).
- **It happened to the most AI-capable security shop in the world, through a third-party forum product.** The defensive reading is not "OpenAI was sloppy" — it is that **user-controlled image uploads to any web product are a standing native-code attack surface**, and that AI-assisted attackers now have the same 1–3-day probe-to-RCE tempo the good guys used here.

## Chain mechanics (as published)
1. **Entry: crafted HEIF/HEIC upload.** A user posts an iPhone-format image to OpenAI's Discourse forum; Discourse runs its conversion pipeline (ImageMagick → **libheif** decode, because ImageMagick's usual toolkit can't handle Apple's format). A specially crafted file triggers the **libheif memory bug** (layer-position miscalculation) → server compromise. Exploitation required **fingerprinting the target version and tailoring payload images**; some RCE attempts took thousands of uploads (CyberScoop).
2. **Second flaw: forum-to-account takeover.** Once on the Discourse server, a second vulnerability let the researchers **take over users' ChatGPT and Codex accounts** — including OpenAI employees who logged into the forum. (Public coverage does not detail the mechanism; one analyst writeup frames it as an identity/SSO boundary gap between the forum session and ChatGPT/Codex accounts.)
3. **Account-to-repo pivot.** The taken-over employee account had **Codex connected to OpenAI's GitHub organization**; researchers reached internal repositories and, as a proof of concept, **opened a pull request in the company's monorepo** using the employee's Codex credentials.
4. **Disclosure.** July 25 discovery; notified OpenAI and Discourse; **Discourse fix July 27**; report published Sep 17–18; **$6,500 bounty**; OpenAI: resolved. Total from vulnerability discovery to repository access: **under 72 hours** (TechCrunch / researchers' timeline).

### HEIF Heist beyond OpenAI
- Hacktron's broader report describes the primitive against **libheif and libde265** (HEIF/AVIF parsing C/C++ decoders embedded "in many popular software decoders"): crafted HEIF/HEIC/AVIF uploads **bypass most application-layer defenses** and can achieve **RCE** or, failing that, **arbitrary heap disclosure** — in-memory theft of other users' data and environment variables.
- Named potentially exposed surfaces: **AWS** (user files, access tokens), **Meta's core product suite**, **GitHub Enterprise servers**, **Discourse** deployments. "Even when RCE isn't immediately achievable, the attack primitives may still allow arbitrary heap disclosure."
- Patch state caveat (researchers'): "the latest version of libheif has been patched, but **any deployment lacking the latest upstream security patches is potentially vulnerable**" — i.e., the same upstream-propagation gap, still open downstream.

### AI-assisted research methodology (as published)
- Attribution: "led" by Hacktron humans (report bylaws) "**assisted by Hacktron Harness, GPT-5.6 Sol, and Opus 5**."
- **Opus 4.8 (special cybersecurity-access version) could not produce a working exploit across several sessions; Opus 5 succeeded within hours of release on the same problem.**
- An "AI agentic approach with a frontier model like GPT-5.6 Sol cut exploit development time down to roughly **1 to 3 days** from initial probe to remote RCE."
- Honest friction: "Exploitation requires fingerprinting the target version and tailoring the payload images. Some of our RCE attempts landed only after thousands of image uploads." The researchers also note the paths were "not particularly easy or efficient to exploit."

## Caveats
- Account-takeover flaw mechanism, the second flaw's scope (does every Discourse deployment with SSO connect?), and whether any non-researcher exploitation occurred pre-July 27 are **not disclosed** in public coverage.
- Outlet summaries differ on team size (TechCrunch: three-person team; CyberScoop names four attributed researchers: Harsh Jaiswal, Mohan SRK, Rahul Maini, Sudhanshu Rajbhar — with founder Mohan Pedhapati also quoted).
- The exposed-surface list (AWS, Meta, GitHub Enterprise) is **Hacktron's assessment**, not vendor confirmation; no vendor has publicly confirmed exposure as of Sep 18–19.
- Plausible but not explicitly stated in coverage: overlap between this libheif bug and **GHSA-g89c-p67h-r497** (the no-CVE scale-path heap overflow behind Next.js's August AVIF RCE, finder handle "rootxharsh"). Treat lineage as **unconfirmed** until Hacktron or libheif names the advisory/commit.

## Defender translation
- **Inventory image/codec parsers as Tier-1 attack surface**: libheif, libde265, ImageMagick handlers, sharp, ffmpeg, libavif — anything reachable from an unauthenticated upload. Track upstream repo releases/commits for these libraries, **not just CVE feeds**; the "silent fix without a CVE" pattern is exactly how this class survives a downstream fleet for months.
- **Question SSO boundaries on community/forum products**: if a login to a public forum can yield or link to productive SaaS accounts (ChatGPT, Codex, Copilot, internal SSO), the forum's server compromise is an account-takeover platform. Segment forum identities from employee identity; audit connected-app/OAuth grants (Codex→GitHub-org style links) as privileged paths; require phishing-resistant re-auth before high-value actions from forum-originated sessions.
- **Assume adversary access to the same models**: an attacker probe-to-RCE loop that needs thousands of crafted uploads is now economically feasible for criminals (their own tempo estimate: 1–3 days with agentic tooling). Rate-limit and alarm on repeated failed uploads/parsing crashes per source; crash telemetry in native decoders is a free exploitation-detector.
- **Watch items**: (1) whether Discourse publishes a proper advisory/CVE for either flaw and what the account-takeover mechanism was; (2) libheif naming/CVE'ing the bug(s) and downstream backports; (3) vendor confirmations/denials on the HEIF-Heist exposed-surface list; (4) OpenAI postmortem detail on the forum→account pivot; (5) Anthropic/OpenAI capability-gating responses as this story feeds the AI-exploit-policy debate; (6) copycat "AI built my exploit" disclosure posts with model names and timelines.

### September 19 follow-up: the un-CVE'd advisory behind Next.js finally got a CVE — on HEIF-Heist day

Night sweep of watch item (2) produced a direct hit: **GHSA-g89c-p67h-r497 — the libheif `scale_nearest_neighbor()` heap overflow our August Next.js page documented as "Critical with NO CVE" — was assigned CVE-2026-84383, published to NVD on September 18, 2026 16:17 UTC**, within hours of the HEIF-Heist press cycle (GHSA updated Sep 3, CVE live NVD Sep 18). It arrived as a **batch**: CVE-2026-84383, -84384, -84446, -84447, and -84450 all landed in NVD in the same minute-window, all libheif, all mapping to previously un-CVE'd GHSAs. Honest read: the governance gap is **partially closing** — old no-CVE libheif advisories are being backfilled — but it closed for this advisory **a month after Next.js shipped its stopgap and only after the story went public**, and the newest wave is still un-numbered: the Sep 1/6 security-release advisories (GHSA-8fmq-r4pf-7m57, GHSA-w7mc-p8jc-p853, GHSA-4h82-g446-83fm, GHSA-vg7w-rp49-4fc2, GHSA-rhgw-q5g8-xjh2 and siblings) and a **new advisory published Sep 18 23:06 UTC, GHSA-q492-cfcm-895h** — the OpenJPEG pre-decode resource-limit gate accepting pathological JPEG 2000 geometry (huge absolute coordinates, 17-pixel canvas span) so a crafted J2KI file reaches `opj_decode()` (ASan heap-overflow write under OpenJPEG 2.3.1, matching the CVE-2020-6851 sink; current OpenJPEG 2.5.4 rejects the input but the libheif-side gate is still the gap; flagged for fix in 1.23.5) — carry **no CVE at all**. No new libheif release since v1.23.4 (Sep 6); no Discourse advisory for either HEIF-Heist flaw (blog feed checked Sep 19). Note the scope expansion: libheif is now patching **its admission gate in front of third-party decoders** (OpenJPEG), so "track upstream commits" covers libheif's pre-decode validation of every codec plugin, not just its own parsers.

### September 19 second follow-up: the codec class claims two more downstreams — Astro AVIF RCE (no CVE) and ExifReader HEIC/AVIF iloc DoS

While the HEIF-Heist story held the news cycle, this wiki's September 19 GHSA sweep (~15:25 UTC) surfaced two more advisories on the exact surface Hacktron named, neither previously on-wiki:

- **Astro — `GHSA-26w7-cxv4-gfx2`, CVSS 9.8 Critical, NO CVE** (advisory published Sep 8, surfaced in the npm advisory feed during the Sep 19 sweep): "Remote code execution through AVIF image optimization" — a **libheif vulnerability reachable through Astro's default Sharp image service** whenever an attacker can cause an untrusted AVIF image to be optimized. Fixed in **Astro 7.2.8**, which requires **Sharp 0.35.4** (released Aug 26, carrying the patched libheif). Read: a **second mainstream JS framework** — after Next.js in August — is publicly confirmed RCE-capable from one malicious AVIF upload through the default sharp→libheif pipeline, and the advisory **ships with no CVE**, fixed by version bump rather than by any CVE-driven process. This is the silent-fix propagation gap this page's Summary describes, executing again in a different fleet while the CVE governance catches up one batch at a time.
- **ExifReader — `GHSA-pj96-35fp-cfcc` / CVE-2026-85715 (High, fixed 4.41.1, published Sep 17)**: denial of service via a crafted HEIC/AVIF **`iloc` box** — setting `offsetSize`, `lengthSize`, and `baseOffsetSize` to zero makes the extent-parsing loop (`src/image-header-iso-bmff-iloc.js`, `getItems()`) iterate up to 65535×65535 times **without advancing the buffer offset**, allocating a JavaScript object per iteration: a **652-byte file grows the heap 400 MB; a 6 KB file OOM-crashes the Node process**. Different severity (pure resource exhaustion) and a different implementation (pure JS, not native), but the same root-cause family: **trusting attacker-controlled size fields inside ISO-BMFF/HEIF containers**.

The read across the growing set — libheif memory-corruption RCEs at Discourse/OpenAI (this page), Next.js (August), and now Astro, plus a pure-JS container-trust DoS in ExifReader — is that **HEIF/AVIF container parsing is a recurring advisory generator across at least two independent parser implementations and three frameworks**, and the highest-severity items (Hacktron's libheif bug lineage, Astro's, and the newest libheif GHSAs including `GHSA-q492-cfcm-895h`) **still carry no CVE**. Watch-item status unchanged on the other legs: no libheif release since v1.23.4 (Sep 6); no Discourse advisory for either HEIF-Heist flaw as of the Sep 19 sweep.

## Related pages
- [Next.js August 2026 security release: libheif/AVIF heap overflow + Windows path traversal](nextjs-august-2026-security-release-avif-libheif-and-windows-rce.md)
- [Anthropic cyber evaluations and real-world intrusions](anthropic-cyber-evaluation-real-world-intrusions.md)
- [AIR Plugin4Shell — agent plugin SHA-pinning bypass](../patterns/plugin4shell-agent-plugin-sha-pinning-bypass-air-september-2026.md)
- [Mandiant IR case: hijacked AI coding-assistant session spreads Shai-Hulud](mandiant-ai-coding-assistant-session-hijack-shai-hulud-saas-september-2026.md)
- [Unit 42: machine-speed agentic intrusion](unit42-ai-assisted-cyber-attack-machine-speed-agentic-intrusion-september-2026.md)

## Sources
- TechCrunch (Aditya Mehta, Rebecca Bellan), "Researchers used Anthropic's Claude to hack into OpenAI" (Sep 18, 2026): <https://techcrunch.com/2026/09/18/researchers-used-anthropics-claude-to-hack-into-openai/>
- CyberScoop (Derek B. Johnson), "Researchers use AI to find widespread software decoder flaw" (Sep 18, 2026): <https://cyberscoop.com/hacktron-ai-heif-heist-vulnerability/>
- The Wall Street Journal, Thursday Sep 17/18 evening report (per TechCrunch attribution)
- The Register, "Researchers used Claude to hack OpenAI employees' ChatGPT accounts" (Sep 18, 2026)
- VentureBeat, "OpenAI hacked by small team of white hat security researchers using Anthropic's Claude Opus 5" (Sep 18, 2026)
- The Guardian, "OpenAI 'ethically hacked' with help of Anthropic's Claude chatbot" (Sep 18, 2026); CBS News (Sep 19, 2026); NBC News (Sep 18, 2026)
- Hacktron AI blog (researchers' own post; linked from TechCrunch/CyberScoop): <https://www.hacktron.ai/blog>
