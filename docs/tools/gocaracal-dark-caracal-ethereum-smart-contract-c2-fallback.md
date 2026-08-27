# GoCaracal: Dark Caracal's Go malware framework with an Ethereum smart-contract C2 fallback

## Summary
**GoCaracal** is a previously undocumented **Go-based malware framework** that Arctic Wolf says was deployed during a **June 2026** intrusion at an unnamed **communications organization in Venezuela**. Arctic Wolf assesses, **with medium confidence**, that the activity is linked to **Dark Caracal** — a long-documented Latin American financially-motivated cluster (original disclosure 2018; retooled **Bandook** malware 2020; Bandook attacks in Venezuela 2021). GoCaracal provides remote shell access and payload execution; an **extended profile** adds browser-data theft, keylogging, remote desktop, and SOCKS5 proxying. The most durable technical detail is an **Ethereum smart-contract C2 fallback**: after repeated failures to reach its configured primary C2, the malware issues an `eth_getStorageAt` request to a public Ethereum JSON-RPC endpoint and uses the stored value as a **replacement C2 address**, letting the operator rotate the C2 host without shipping a new binary.

## Tags
- tools
- malware
- GoCaracal
- Dark Caracal
- Bandook
- Go
- remote access trojan
- shellcode
- C2
- Ethereum
- smart contract
- eth_getStorageAt
- JSON-RPC
- C2 fallback
- browser data theft
- keylogging
- remote desktop
- SOCKS5
- phishing
- SVG
- Latin America
- Venezuela
- Arctic Wolf
- YARA

## How it works
- **Delivery:** Arctic Wolf assesses **phishing** as the delivery mechanism (financial and tax-themed artifact naming; an established campaign pattern; more than 100 related **SVG** files that communicated with the same malicious hosting site). The original phishing email/SVG attachment was not recovered from the victim.
- **Profiles:** observed in **lightweight** and **extended** forms.
  - *Lightweight:* host profiling, an encrypted C2 channel, interactive shell access, payload retrieval/execution, and shellcode loading/injection.
  - *Extended:* adds system and file discovery, command execution, **browser cookie and login-database collection**, **keylogging**, targeted file search, **WebRTC remote desktop**, hidden browser interaction, **SOCKS5 proxying**, and persistence-related functionality.
- **Bandook relationship:** **Bandook** was deployed *alongside* the lightweight GoCaracal profile, in parallel. Arctic Wolf says current evidence does **not** establish GoCaracal as a replacement for Bandook.
- **Ethereum smart-contract C2 fallback (the durable pivot):**
  1. The extended profile first attempts to reach its configured **primary C2** server.
  2. After repeated failures it sends an **`eth_getStorageAt`** request to a **public Ethereum JSON-RPC endpoint**.
  3. The response value is the **replacement C2 address**, which GoCaracal writes into its in-memory configuration.
  4. It then retries conventional off-chain C2 communication using the replacement address.
  - Multiple public RPC endpoints can read the same contract state, reducing dependence on a single fallback access point. This does **not** place the full C2 channel on Ethereum; it is a **C2-address rotation mechanism**.
  - Arctic Wolf's public report does **not** show a host in the June intrusion that invoked the fallback and successfully reconnected through the replacement address.

## Attribution and scope
- **Actor:** Dark Caracal (medium confidence), per shared Bandook use, recurring Delphi-loader characteristics, Spanish-language financial lures, malicious SVGs, URL shorteners, document-themed infrastructure, hosting-provider preferences, and Latin American targeting.
- **Confirmed victim:** one unnamed communications organization in **Venezuela** (June 2026). The public report provides **no broader confirmed count** of organizations compromised with GoCaracal.
- **Regional context:** Arctic Wolf notes related artifacts and infrastructure associated with **Brazil, Ecuador, Chile, Colombia, El Salvador, and Uruguay**, assessing broader regional activity with **moderate confidence** — these are **not** identified as confirmed victim countries.
- **Lineage:** Dark Caracal has a documented history of operating in Latin America (original disclosure 2018; retooled Bandook 2020; Bandook attacks in Venezuela 2021).

## Durable detection pivots
- **Ethereum fallback beaconing:** `eth_getStorageAt` JSON-RPC calls from hosts that also show failed C2 connections to an off-chain address, followed by a new off-chain connection to the address returned by the contract. Correlate on the JSON-RPC method name + a subsequent off-chain connection, not just the RPC call.
- **Contract + wallet indicators:** Arctic Wolf published **Ethereum contract and wallet indicators** (representative; full set available to Arctic Wolf customers).
- **YARA + hashes:** a public **YARA rule for the lightweight GoCaracal profile**, representative SHA-256 hashes, related domains/IPs, and associated host paths.
- **Delivery artifacts:** financial/tax-themed artifact naming and the >100-file **SVG** cohort that contacted a single malicious hosting site are a durable delivery signature.

## Defender guidance
- Hunt for the `eth_getStorageAt` JSON-RPC fallback pattern on egress telemetry; it is a strong, specific indicator of a Dark Caracal / GoCaracal C2-rotation capability and is unlikely in legitimate traffic.
- Where GoCaracal is suspected, treat browser-cookie/login-database collection and SOCKS5 proxying as likely: rotate sessions, revoke tokens, and review the WebRTC remote-desktop and keylogging surface.
- Preserve the Ethereum contract/wallet indicators and JSON-RPC telemetry for correlation; they are more durable than any single C2 host.

## Confidence and caveats
- Attribution to Dark Caracal is **medium confidence** and correlation-based; GoCaracal ≠ Bandook replacement is an explicit caveat.
- The Ethereum fallback is **described but not observed executing** in the public report for this intrusion; the public IoCs are **referential**, with the full set gated to Arctic Wolf customers.
- No broader confirmed victim count is public; the Latin American country list is contextual, not confirmed victimology.

## Related pages
- [Aeternum Polygon blockchain-C2 analysis](aeternum.md) (blockchain-as-C2 tradecraft context)
- [DeadLock ransomware decentralized recovery infrastructure](deadlock-ransomware.md) (Ethereum/Polygon C2 and exfil patterns)

## Sources
- Arctic Wolf Labs: [Dark Caracal, Reloaded — New Malware, Same Hunting Grounds](https://arcticwolf.com/resources/blog/dark-caracal-reloaded-new-malware-same-hunting-grounds/) — August 2026
- The Hacker News: [GoCaracal Malware Uses Ethereum Smart Contract to Fetch Replacement C2 Address](https://thehackernews.com/2026/08/gocaracal-malware-uses-ethereum-smart.html) — August 27, 2026
