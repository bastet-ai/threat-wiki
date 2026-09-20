# RatHat: Android spyware self-pairs to ADB for post-uninstall shell persistence, drives itself with a live generative-AI loop over the Accessibility tree (Zimperium zLabs, Sep 18, 2026)

## Summary

Zimperium zLabs (Gianluca Braga, Vishnu Pratapagiri, Fernando Ortega; reported by The Hacker News September 18, 2026) disclosed **RatHat**, an Android spyware assessed as operated by **China-based threat actors**, distributed by targeted **smishing** and **malvertising** into deceptive third-party download portals. Two design choices make it durable intelligence rather than another Android RAT writeup:

1. **Autonomous local ADB self-pairing that survives uninstall.** After phishing the user into installing an APK dropper, the app abuses granted **Accessibility** permissions to unlock **Developer Options**, enable **Wireless Debugging**, and **extract the 6-digit ADB pairing code from the screen** — pairing the device to a local ADB daemon controlled by the malware's Go agent. The resulting **native daemon runs at shell privilege outside the app lifecycle**, so **uninstalling the app does not remove attacker access**: the retained local service checks whether RatHat is installed and silently reinstalls it. A **FRP reverse-proxy client** pulls its tunnel configuration from C2, giving the operator a general-purpose road into the device independent of the malware's own feature set.
2. **A real-time generative-AI decision loop for on-device navigation.** The malware **serializes the live Accessibility tree to XML and sends it to "one of the world's most popular generative AI assistants"** to resolve target coordinates (returned as JSON for synthetic clicks), resolve on-screen text, and emit navigation commands like `SCROLL_DOWN` — an agent driving the victim's screen through the OS's own automation API with a cloud LLM as the planner. Zimperium notes the AI calls are for nominally non-malicious steps (locate, read, scroll), which is exactly why they blend into normal app traffic.

Collection capabilities: overlay credential harvesting atop specific apps, **MediaProjection screen recording**, SMS interception, lock-screen PIN/pattern/password capture, keystroke capture including a **hardware-level on-screen keylogger executed by the Go agent** (records finger presses), URL capture from browser address bars, installed-app lists, and files. Installation attempts are countered by a **fake Google Play "failure" overlay**. Distribution lures include four named anti-analysis tricks (below). Assessment: China-nexus operators; no campaign victim counts published in the coverage reviewed by this wiki.

## Tags
- tools
- android
- mobile-malware
- spyware
- ADB
- accessibility-abuse
- wireless-debugging
- post-uninstall-persistence
- native-daemon
- FRP
- reverse-proxy
- generative-AI
- AI-driven-malware
- keylogger
- overlay-attacks
- smishing
- malvertising
- China-nexus
- Zimperium
- RatHat

## Mechanics

**Pipeline:** smishing / malvertising / forum lures → deceptive download portal → dropper APK → main payload. Three components: the Android app (permission acquisition + UI abuse), a **Go Agent** (masquerades as `liblocal-service.so`, executes commands through the shell-level ADB channel), and an **FRP reverse-proxy client** (persistent reverse tunnel to C2, config fetched from the Go Agent).

**Escalation chain (the durable part):**
1. Social-engineer install of the dropper APK.
2. Accessibility-service grant obtained via UI automation.
3. Accessibility used to **unlock Developer Options → enable Wireless Debugging → read the on-screen 6-digit pairing code** → complete local ADB pairing.
4. ADB channel launches **independent native daemons with shell privileges** — outside the Android app sandbox and outside the app's install/uninstall lifecycle.
5. Daemon maintains power-management exemptions and a **reinstall watchdog**; FRP tunnel gives the operator arbitrary shell reach.

**Anti-analysis set (named in the report):**
- **Container tampering:** files declared as directories, or ZIP general-purpose encryption bit set, so Android's `libziparchive` silently ignores them while `unzip`/`apktool` still see them.
- **Manifest bomb:** undocumented `0x9999` chunk headers in `AndroidManifest.xml` that the Android runtime skips but automated analysis pipelines crash/timeout on.
- **DEX bytecode poisoning:** pseudo-instructions with invalid `element_width` to break disassembly.
- **Dual string encryption:** a Base64 scheme branded **StringCrypto**.

**GenAI loop:** Accessibility tree → XML → cloud LLM → coordinate JSON / text extraction / scroll commands → synthetic taps. The AI never receives a "steal this" instruction set in the reported design — it is asked benign localization questions, and the malicious sequencing is client-side.

## Detection and hunting heuristics

1. **Wireless-debugging enablement is the trip-wire.** Developer Options unlocks and Wireless Debugging toggles by a non-admin app are near-signature events; MDM policy should block Developer Options outright on managed fleets and alert on toggle attempts.
2. **Pairing-code reading = Accessibility + pairing-dialog co-occurrence.** Any app driving UI automation immediately before/during an ADB pairing dialog is this pattern; log accessibility-service usage against pairing events.
3. **Post-uninstall residue:** on suspicious devices look for shell-level native daemons, `adbd`-spawned children, and reinstall-watchdog behavior after the "offending" app is gone — classic out-of-lifecycle persistence.
4. **FRP client traffic:** FRP has characteristic control-connection behavior; hunt unexpected persistent outbound tunnels from mobile subnets (also relevant on any egress device, not just phones).
5. **The AI-loop tells:** periodic serialization of the full Accessibility tree (large, structured XML egress bursts) plus third-party LLM API calls from apps with no assistant function. Treat "app reads whole a11y tree at regular intervals" as a behavioral signal independent of model/provider.
6. **APK triage:** sandbox pipelines should be regression-tested against the four named anti-analysis tricks (directory-declared files, encryption-bit entries, `0x9999` manifest chunks, invalid `element_width` opcodes) — each is a pipeline-crasher by design, and "analysis timed out" should never mean "clean."
7. **Pattern read:** this is the mobile mirror of the desktop agent-tooling abuse this wiki tracks (coding-assistant session hijack, MCP trust boundaries): the OS's legitimate automation rails (Accessibility, ADB) plus a rented LLM make an autonomous operator — defense moves from app reputation to automation-behavior monitoring. Zimperium's own conclusion: signature-based mobile controls are insufficient here.

## Related pages
- [Mandiant AI coding-assistant session hijack → Shai-Hulud deployment](../ops/mandiant-ai-coding-assistant-session-hijack-shai-hulud-saas-september-2026.md) — same era's "legitimate automation rail weaponized" story on the developer desktop
- [RedWing / Rokarolla Android banking malware](../tools/redwing.md) — prior zLabs Android coverage on-wiki (Accessibility abuse + overlay lineage)
- [Unit 42 NOVA frontier-AI discovery](../patterns/unit42-nova-frontier-ai-autonomous-vulnerability-discovery-august-2026.md) — the other side of the AI-automation wave (finding bugs, not driving screens)

## Sources
- The Hacker News, "RatHat Android Malware Abuses ADB to Retain Shell Access After Uninstall," Sep 18, 2026: <https://thehackernews.com/2026/09/rathat-android-malware-abuses-adb-to.html> (quoting Zimperium zLabs: Gianluca Braga, Vishnu Pratapagiri, Fernando Ortega)
- Zimperium zLabs original publication (canonical URL not retrievable from this wiki at capture time; feed endpoint 404'd — the THN article carries the full attributed excerpts)
