# Google GTG: an undercover Mandiant analyst inside TeamPCP's inner circle — LABScon teardown of the infiltration, the ShinyHunters betrayal, and the Opsec trail to the arrests

## Summary
At **LABScon on September 18, 2026**, **Google Threat Intelligence Group (GTG) researcher Austin Larsen** publicly detailed — for the first time — that **a Mandiant undercover analyst had been inside TeamPCP's inner circle "from almost day one"** of the group's 2026 supply-chain rampage. A Google persona that had spent **months building trust with an actor later invited into TeamPCP** was added along with him to the group's core chat — one of **about 12 members** of the channel the group called **CanisterWorm** — giving Google a live view of the credential vault, the extortion planning, and the infighting while the Trivy → LiteLLM → TanStack/Mistral-era compromises were still unfolding. The talk (reported by WIRED) supplies the first end-to-end public narrative connecting the **August 27 AFP/WAPF/FBI charges** to Google's investigative work: leaked BreachForums data tied the chat's most-active handle to **sheepstealing@gmail.com**, a 2019 pirated-Office-key refund dispute tied that handle to **ruben@thomsonfamily.net.au** — i.e., accused principal **Ruben Ian Thomson** — and the clincher was TeamPCP **backing its relocated stolen-credential server up to a Google Drive owned by that same Gmail account**, which Larsen tipped to the FBI ("an agent responded in a matter of minutes"). The talk also produces two new durable intelligence items: (1) **ShinyHunters partnered with TeamPCP around April 2026, then went rogue** — extorting victims with TeamPCP's own stolen credentials while withholding TeamPCP's cut, even volunteering its chat log from TeamPCP's server to Larsen — prompting TeamPCP to exile ShinyHunters (and Google's mole) and move its data; and (2) someone inside the core circle was **using an AI tool to develop a zero-day exploit against a widely used login product to bypass its two-factor authentication** — Google obtained the exploit code, **confirmed it worked after a few tweaks**, and warned the vendor, which patched (this is the incident Google described in an anonymous May 2026 case study — now, for the first time, placed inside TeamPCP). Monetization math is also new: despite the AFP's **500,000+ stolen credentials**, Larsen says TeamPCP was extracting only **tens of thousands of dollars** in extortion — not millions — which is why it brought revenue-share partners in, the decision that produced the betrayal. Google's disruption model is the closing thesis: rather than notify hundreds of victim companies one by one, GTG went to **credential-issuing platforms first (AWS, Microsoft)** to have stolen credentials revoked **before** they could be used, sending hundreds of provider notification emails — "writing reports can only be so useful," under the newly formed **Google Cyber Disruption Unit**.

## Tags
- ops
- operations
- TeamPCP
- Google
- GTG
- Mandiant
- undercover
- infiltration
- law enforcement
- FBI
- AFP
- ShinyHunters
- extortion
- credential theft
- supply-chain
- AI zero-day
- Opsec failure
- CanisterWorm
- Cyber Disruption Unit
- LABScon

## What was disclosed (LABScon, Austin Larsen, Sep 18, 2026)

### The mole
- A Google/Mandiant **undercover persona** had spent "many months building trust with one of the actors that was invited to join TeamPCP, and so was added to the group." Effectively **"almost day one, Mandiant was watching everything behind the scenes."** The analyst's name was not revealed.
- The inner circle was **~12 members** with access to a core chat the group named **CanisterWorm** (note: on this wiki the name also tracks the npm worm of the same name — the chat and the worm shared the group's branding).
- Access included **the server where TeamPCP stored its trove of stolen usernames, passwords, and access tokens** — the material it planned to extort with (AFP figure: more than half a million users' credentials).
- Outside validation of the mole's existence: Telstra threat researcher and former AFP analyst **Michael Fletcher** says he approached Larsen around that time about monitoring TeamPCP and was told to approach the hackers carefully because one of them was "friendly."
- Guardrails: Larsen says the analyst **never engaged in illegal hacking or encouraged breaches** — "a fly on the wall, only saying enough to not be suspicious."

### The money problem and the ShinyHunters betrayal
- Despite the credential haul, Larsen estimates TeamPCP pulled in only **tens of thousands of dollars** in extortion payments — versus the millions similar groups amass. Struggling to monetize, TeamPCP **invited multiple cybercriminal groups in as revenue-share partners**, granting them access to the stolen credentials for a percentage of what they extracted.
- **ShinyHunters** joined around **April 2026**. "A few weeks" later it **went rogue**: running its own extortions with TeamPCP's credentials and withholding TeamPCP's cut — and **unsolicited, shared with Larsen a full log of its own chat on TeamPCP's server**, not knowing Google already had access via the mole. ShinyHunters also **taunted TeamPCP on X**.
- TeamPCP's response: **narrowed the inner circle, moved its data to a server at a different hosting provider, and exiled ShinyHunters — and several other members, including Google's undercover analyst — from CanisterWorm** ("Just delete that and stop sharing shit with shinyhunters," one leader wrote).
- Convergence: Google's account independently corroborates the **Anthropic September 2026 report's GTG-50014** cluster ("suspected ShinyHunters affiliates") running AI-assisted extortion at industrial scale in the same months, and extends the ShinyHunters pattern seen in Unit 42 token-jacking and the Salesforce/OAuth abuse reporting.

### Disruption before notification
- With vault visibility, Larsen's team chose **disruption over sequential victim notification**: first contacted **platforms where the stolen credentials worked — AWS and Microsoft** — to get credentials revoked en masse, then sent **hundreds of notification emails** to providers and victims. "Let's go mess up what they're doing. That was my goal."
- The **in-the-wild AI-built zero-day**: via the inner-chat visibility, Google learned someone in the core circle (separate from the supply-chain ops) was **using an AI tool to develop a zero-day against a widely used login product to bypass 2FA**. Google got a copy of the exploit code, tested it, found it **worked with a few tweaks**, and warned the vendor, who patched. Google had described this in a **May 2026 case study without naming TeamPCP** — the LABScon talk is the first public placement of it inside the group. One of the rare publicly confirmed instances of an AI-developed, previously unknown vulnerability exploited in the wild.

### The Opsec trail to the arrests
- **BreachForums leak:** the **most active handle** in CanisterWorm had registered on the forum with **sheepstealing@gmail.com**.
- **2019 forum archive:** a refund dispute between user "sheepstealing" and a pirated-Microsoft-Office-key seller demanded the refund at a **PayPal account tied to ruben@thomsonfamily.net.au** → identity pivot to **Ruben Ian Thomson** (charged Aug 27, 2026, Perth Magistrates Court, with Louis Michael Gaebler).
- **The clincher:** after the post-betrayal server move, Google learned (via a "trusted partner") some contents of the new server **and** that it was being **backed up to a Google Drive on that same sheepstealing@gmail.com account** — stolen material synced to an account tied to the operator himself. Larsen tipped the FBI; an agent responded within minutes; ~a month later law enforcement completed warrant requests to Google for Thomson's data; the arrests followed in late August.
- **Brian Krebs** independently published his own clue trail to Thomson's identity the prior month; Google's tip was not necessarily the only path.

### Attribution discipline and framing
- Leaked-chat boast: "You guys should understand that we pulled off the biggest supplychain [sic] maybe ever recorded in modern history."
- WIRED's recap of the campaign list matches this wiki's record: **Trivy**, **LiteLLM**, **Checkmarx** infrastructure, **TanStack**, **Mistral AI**, then breaches of **GitHub**, **Mercor**, and employee devices at **OpenAI**, the **European Commission**, and others unnamed; **Mini Shai-Hulud** as the automation worm, named after the Sep 2025 original whose lineage to TeamPCP **remains unestablished**.
- Larsen frames the operation under Google's new **Cyber Disruption Unit**: "Writing reports can only be so useful. Taking action to protect users and customers — that is the next step."

## Durable defender reads
- **Revocation-beats-notification ordering** is a reusable IR playbook shape for mass credential theft: at hundreds-of-victims scale, engaging **credential issuers** (cloud providers, IdPs) to revoke class-by-class precedes per-victim outreach and cuts the attacker's use-window.
- **Criminal-partnership instability is an intelligence source and an operational risk**: revenue-share with prolific groups (ShinyHunters) traded monetization reach for betrayal risk; expect stolen-credential ecosystems to be contested — credentials you rotate may already be in the hands of the thief's ex-partners.
- The **AI-developed 2FA-bypass zero-day** confirms agents-in-the-loop exploit development is not hypothetical: patch urgency for authentication software should assume adversary AI tooling is fuzzing/repair-looping it.
- **Person-level Opsec, not infra, ended the operation** (forum handle → email → PayPal → family domain → personal Google Drive). For defenders the mirror-image lesson: attacker-attribution trails come from identity plumbing, and law-enforcement outcomes do not close credential exposure — rotation across the March 2026 exposure window still stands.

## Confidence and caveats
- Single primary source (Larsen's LABScon talk as reported by WIRED); Google has not published a written report of the details at disclosure time. The talk text/deck may add or correct detail.
- "About 12 members," monetization estimates ("tens of thousands"), and the timing of the ShinyHunters partnership come from Google's account of its own investigation — unfalsifiable from public data; treat scale and interior-chat details as one-party claims.
- Charged individuals are **alleged**, presumed innocent; the underlying charges are covered on the [AFP/WAPF/FBI charging page](teampcp-afp-wapf-fbi-charged-two-men-august-2026.md).
- Google/Mandiant has its own institutional interest in the disruption narrative; the "fly on the wall" characterization is self-reported.
- WIRED names the core chat "CanisterWorm" as TeamPCP's own label — consistent with, but not identical to, the wiki's CanisterWorm worm naming; do not conflate the chat with the npm worm artifact.

## Related pages
- [TeamPCP actor page](../actors/teampcp.md)
- [TeamPCP: AFP/WAPF/FBI charge two Western Australian men](teampcp-afp-wapf-fbi-charged-two-men-august-2026.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [CanisterWorm tool page](../tools/canisterworm.md)
- [Trivy → TeamPCP → CanisterWorm timeline](trivy-lite-llm-compromise-timeline.md)
- [LiteLLM compromise](litellm-compromise.md)
- [Anthropic Threat Intelligence report September 2026](anthropic-threat-intelligence-report-september-2026-ai-augmented-operations.md)
- [Mandiant AI coding-assistant session hijack case](mandiant-ai-coding-assistant-session-hijack-shai-hulud-saas-september-2026.md)

## Sources
- WIRED: [An Undercover Google Analyst Infiltrated a Notorious Supply-Chain Hacking Gang](https://www.wired.com/story/an-undercover-google-analyst-infiltrated-a-notorious-supply-chain-hacking-gang/) — September 18, 2026 (interview with Austin Larsen ahead of his LABScon talk)
- Austin Larsen, Google Threat Intelligence Group — LABScon talk, September 18, 2026 (as reported)
- Google May 2026 case study on the AI-developed zero-day (anonymous at the time; referenced in the WIRED piece)
- Prior wiki record: AFP/WAPF/FBI joint release (Aug 27, 2026), Brian Krebs's independent identification reporting (Aug 2026)
