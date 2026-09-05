# Sality P2P botnet disrupted: CrowdStrike P2P sinkholing operation with DOJ/FBI ends a 23-year file-infecting botnet (Aug 31, 2026)

## Summary
On **August 31, 2026**, CrowdStrike's **Counter Adversary Operations (CAO)** team, working with the **U.S. DOJ, FBI, the DoD Office of the Inspector General's Defense Criminal Investigative Service (DCIS), and the Shadowserver Foundation**, with support from **Europol, Eurojust, and law enforcement in Bulgaria, Hungary, and Romania**, executed a **coordinated P2P sinkholing disruption of the Sality peer-to-peer (P2P) botnet** — a polymorphic **file-infecting** criminal infrastructure that has operated since **2003**. The operation isolated all ~**33,000+ infected machines** from the operator by poisoning each bot's super-peer list so that infected hosts can no longer receive **URL packs** (payload-download instructions) or **file packs** (direct payload transfers). CrowdStrike published the full operation on **September 1, 2026** ("Peer Pressure: Inside the Sality Botnet Disruption Operation").

Sality is significant because it demonstrates that **P2P architecture is not a disruption-proof shield**: the same properties that made the botnet resilient for two decades — no single point of failure, unauthenticated peer acceptance, a permanently stale (file-infector) protocol that cannot be code-updated — are what the sinkhole exploited. CrowdStrike's framing: *"the protocol cannot be hardened against attack, and the network cannot exclude an active defender who speaks its language."*

## Tags
- ops
- operations
- Sality
- P2P botnet
- file infector
- polymorphic
- infrastructure disruption
- sinkholing
- P2P sinkhole
- lighthouse beacon
- EggJagger
- clipjacking
- crypto clipboard theft
- cryptocurrency theft
- DDoS
- CrowdStrike Counter Adversary Operations
- DOJ
- FBI
- DCIS
- Shadowserver Foundation
- Europol
- Eurojust
- YARA
- RSA public key
- peer list
- super peer
- URL pack
- threat hunting
- malware
- botnet

## Why this matters
- **A 23-year-old criminal botnet was taken down by protocol-level manipulation, not endpoint malware removal.** The operator lost control of the network; the bots are now isolated. This is the same class of technique as earlier large-scale botnet disruptions (e.g., Zeus, GameOver, Operation Endgame/SocGholish) and is a durable reminder that P2P resiliency is not invincibility.
- **Sality's persistence came from its file-infecting design.** It is not a bot that phones home to a C2 panel; it is a **polymorphic infector** that attaches itself to executables on disk and spreads over **network shares, removable drives, and file sharing**. Infections regenerate continuously without any operator phishing or exploit activity — which is why it survived decades and why endpoint-only detection struggles.
- **The primary payload has been EggJagger, a clipjacking tool, for ~8 years.** It monitors the clipboard for **Bitcoin/Ethereum wallet addresses** and silently swaps them for operator-controlled addresses, redirecting payments. CrowdStrike estimates the operator stole **≥ ₽12.1M (~$150,000 USD)** in crypto; the never-spent portfolio peaked at **~₽147M (Jan 2025)**, enough to fund a single actor with near-zero overhead.
- **The operator also ran DDoS on demand.** Three notable campaigns: an **Arabic financial-forum DDoS (April 2016)**, a **Ukrainian forum DDoS on Feb 25, 2022** (the day after Russia's full-scale invasion of Ukraine, apparently to suppress discussion), and a **Russian crypto-exchange DDoS (Sept 2023)** where the payload was compiled seconds before upload — an impulsive, likely personal grievance. This shows the botnet was financially motivated but **willingly weaponized for political/personal targets on short notice**.

## Disruption mechanism (durable defender lesson)
Sality's P2P protocol had two fatal, permanent properties that the sinkhole exploited:
1. **No authentication / no cryptographic identity / no allowlist.** Any publicly reachable host that answered the P2P handshake correctly was accepted as a legitimate peer. Availability was the only requirement — so **an active defender could join the network as a full, indistinguishable participant**.
2. **The file-infecting design means the protocol can't be code-updated.** Bots don't fetch new code from a C2; the spreading mechanism is on-disk. Releasing an updated variant would only fragment the botnet. **Every weakness in the protocol has been permanent for 20 years.**

The operation targeted the **super-peer list** (the finite set of publicly reachable infected machines that form the P2P backbone). Every bot re-verifies its stored peers **every ~40 minutes**; responders accumulate reputation, failures lose it and are purged. The sinkhole:
- **Invalidates legitimate super-peer entries** during peer verification (protocol-level manipulation), progressively isolating each bot.
- **Injects purpose-built sinkholes** into the emptied peer lists — giving visibility into progress, infection tracking, and victim notification.
- **Targets super peers first** (the backbone). Once isolated, both URL packs and file packs stop propagating. Bots behind NAT/firewall are handled passively: when they contact sinkholes during maintenance, their peer lists are purged and they are **permanently isolated**.

In parallel, international law enforcement **took down the URLs currently hosting Sality payloads** (URL-pack targets on compromised / operator-maintained web servers), so bots still holding active URL packs cannot fetch new payloads during the transition.

**Result:** all Sality-infected machines now **beacon to CrowdStrike-operated sinkholes**. The operator has lost the ability to task the network. Note: this **does not remove already-installed malware** from infected hosts — existing payloads remain active and must still be remediated.

## Indicators of infection (durable hunt targets)
- **Lighthouse beacon:** any **UDP traffic to `188.166.101[.]148`** indicates an active Sality infection requiring remediation.
- **URL-pack URLs** — any access to these indicates a Sality infection:
  - **v3** URL pack (version 25202): `http[:]//theunforgiven.p8[.]hu/img/top.gif`, `http[:]//painelwebradiodigital.awardspace[.]info/v3/readme.pdf`, `http[:]//sgwebdesigner.free[.]fr/left.gif`, `http[:]//www.yonelco[.]com/icon.png`, `http[:]//pozdravizbeograda[.]com/readme.pdf`, `http[:]//highclass.atspace[.]com/styles.gif`, `http[:]//situluimihai.3x[.]ro/top.png`
  - **v4** URL pack (version 31010): `http[:]//gatheredovertime[.]com/nb4`, `http[:]//imagebucket[.]biz/nv4`
- **YARA detection** — scan running processes for Sality's **hardcoded RSA public keys** (used to verify payload signatures). CrowdStrike published two rules, `CrowdStrike_Salityv3_01` (v3 key) and `CrowdStrike_Salityv4_01` (v4 key), matching the distinct RSA public keys embedded in the v3 and v4 P2P code. The keys are the durable, strain-stable signature:

```yara
rule CrowdStrike_Salityv3_01 : p2p sality version3
{
    meta:
        copyright = "(c) 2026 CrowdStrike Inc."
        description = "Sality Version 3"
        version = "202608181745"
        last_modified = "2026-08-18"
        actor = "SALTY SPIDER"
        malware_family = "Sality"
    strings:
        $ = "IPFILTERDRIVER"
        $ =
            { 99 65 40 34 cd ae 9d b3  af f5 82 ad 8c 2e 63 51
              e1 34 53 fa 47 54 e4 70  97 4c a5 3d 3c a3 9b 57
              29 02 49 89 46 4c f2 76  b1 ad 8e 79 5d b2 41 28
              4f 2a a5 9a 13 18 c0 1d  ed da e4 52 98 16 7f b3
              a9 d7 7a e4 c4 6f 51 f6  38 fe a6 fb ad 8c 64 1d
              23 b5 a4 9d 40 20 74 61  be 81 c3 eb 3d 24 01 75
              13 07 58 c5 f0 56 09 94  58 e7 6b c3 f3 8c 70 73
              4e f5 0b 2d 88 0b 9a bd  18 e4 36 72 26 1a 32 9b }
    condition:
        all of them
}

rule CrowdStrike_Salityv4_01 : p2p sality version4
{
    meta:
        copyright = "(c) 2026 CrowdStrike Inc."
        description = "Sality Version 4"
        version = "202608181745"
        last_modified = "2026-08-18"
        actor = "SALTY SPIDER"
        malware_family = "Sality"
    strings:
        $ = "IPFILTERDRIVER"
        $ =
            { bb d2 96 8e ed 0b 93 8a  82 e4 e9 bc c3 c5 32 72
              4c 08 aa 56 9f 2d 64 0f  1b 86 68 0e 2b 62 e9 c6
              35 6d 75 b6 32 2d 4f a8  b8 d9 2a 44 8b f0 7f e0
              d9 8e be 66 9d a6 7a 9a  6d e1 45 f1 d3 48 01 0d
              39 2e 9d 2a 45 fb 0b fb  1d 96 f3 b7 4f 55 e5 e1
              16 5b f7 a1 cc 7c 87 c0  c8 9c ef 4e ce 29 58 e2
              99 bd 8a 7a 55 be b4 1c  d9 79 52 25 d8 28 86 7b
              81 39 98 5f 2c 6f 14 bb  a5 6b ce 44 e5 91 93 38
              8b 9a c1 74 46 84 e1 26  ec 04 94 96 75 09 e3 b5
              88 d6 08 f0 4a b7 84 d3  13 2f 00 cc d5 2a 8c 17
              07 09 de 6f b0 d3 d6 2b  c6 a6 9d 38 18 8c 74 9d
              86 16 d5 48 6e 97 32 db  e1 4e f8 04 a6 00 7c 16
              2e 70 1c 23 37 dd 5a 52  76 62 70 d4 86 66 6e df
              0c e9 a1 68 f9 5e e8 dd  09 0c 02 7d 35 d0 54 e7
              00 c0 14 9f ce 4a 9f f3  99 50 1a 0b cd cc ff 05
              b9 04 12 e2 11 76 2f ff  a4 6e 64 18 e0 d0 7b 3b }
    condition:
        all of them
}
```
- **Two independent P2P networks** (v3 and v4) shared the same codebase and operator but used **incompatible protocol versions and different cryptographic keys** — so a host can be in both or either.

## Defender heuristics
- **Treat this as an active hunt, not just a disruption note.** Sality infections that were not already removed still run locally. Scan endpoints with the published **YARA rules** (v3 + v4 embedded RSA keys) and hunt the **lighthouse UDP beacon** in network telemetry.
- **Hunt URL-pack URLs** in proxy/web-traffic logs; any GET to the listed payload URLs is a confirmed infection.
- **Watch for clipjacking (EggJagger).** If a host was a Sality peer, the user's crypto payments may have been silently redirected. Rotate / treat any wallet addresses that transited an infected host's clipboard as compromised, and alert on clipboard-monitoring behavior.
- **File-infecter hygiene.** Because Sality spreads via **network shares, removable media, and file sharing**, prioritize: scanning shared folders and mapped drives, controlling removable-media autorun/execution, and monitoring for newly self-modifying executables.
- **P2P botnet general lesson:** if you operate resilient "self-sustaining" P2P infra, the durable weak point is **peer-list trust** (no peer identity/auth) and **protocol immutability**. Adversaries who understand your protocol can sinkhole or poison it from inside; conversely, defenders can do the same to criminal P2P.
- **Do not treat the disruption as cleanup.** The operator is defanged, but installed payloads persist — complete endpoint remediation and re-scan.

## Attribution and status
- **Operator:** a single, financially motivated **criminal** (not attributed to a state actor) who ran Sality for 23 years. CrowdStrike's YARA metadata labels the actor **`SALTY SPIDER`**.
- **Status:** Sality is **no longer under operator control** as of the Aug 31, 2026 operation; the P2P network is isolated and beaconing to CrowdStrike sinkholes.
- **Partners:** DOJ, FBI, DCIS (DoD OIG), Shadowserver Foundation; support from Europol, Eurojust, and LE in Bulgaria, Hungary, Romania.

## Related pages
- [StealC / Amadey infrastructure disruption](stealc-amadey-infrastructure-disruption.md) — another coordinated infrastructure-disruption operation.
- [Operation Endgame SocGholish disruption](operation-endgame-socgholish-disruption.md) — a major botnet/malware-as-a-service disruption.
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md) — clipjacking / crypto-clipboard hijack technique context.
- [Crypto Clipper Tor / USB worm](crypto-clipper-tor-usb-worm.md) — crypto-clipboard theft via Tor/USB.
- [NetNut P2P residential proxy network disruption](netnut-popa-residential-proxy-network-disruption.md) — P2P-network disruption methodology context.

## Sources
- CrowdStrike Threat Intelligence: ["Peer Pressure: Inside the Sality Botnet Disruption Operation"](https://www.crowdstrike.com/en-us/blog/inside-sality-botnet-disruption-operation/) (published 2026-09-01; operation executed 2026-08-31).
