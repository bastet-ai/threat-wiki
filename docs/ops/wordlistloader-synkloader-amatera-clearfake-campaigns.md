# WordlistLoader / SynkLoader: new ClearFake loaders delivering Amatera (ACR) Stealer

## Summary
Gen Digital Threat Research (via The Hacker News, August 24, 2026) documented two new Windows loader families — **WordlistLoader** and **SynkLoader** — that deliver **Amatera Stealer** (also known as ACR Stealer / AcridRain, an information stealer reportedly sold as malware-as-a-service) through **ClearFake / ClickFake** fake-CAPTCHA campaigns. The chains inject Base64-encoded JavaScript on compromised or SEO-poisoned websites, then use **EtherHiding** (payload retrieval via blockchain smart-contract data) and, in recent revamps, hosting of malicious JavaScript on `cdn.jsdelivr[.]net`. The campaigns overlap with the WebDAV-ClickFix delivery shape Microsoft described in its ACR Stealer reporting, including a headless `conhost -headless` variant with delayed environment-variable expansion.

## Tags
- ops
- operations
- WordlistLoader
- SynkLoader
- Amatera Stealer
- ACR Stealer
- AcridRain
- ClearFake
- ClickFake
- fake CAPTCHA
- EtherHiding
- blockchain dead drop
- cdn.jsdelivr.net
- CDN abuse
- WebDAV
- conhost
- rundll32
- pushd
- infostealer
- MaaS
- Gen Digital

## WordlistLoader chain
- Initial access is a **ClearFake fake CAPTCHA page** on a compromised or SEO-poisoned website that displays a clipboard-runnable command (ClickFix-style).
- The command launches a hidden `cmd.exe` (recorded variants include headless `conhost -headless` with delayed environment-variable expansion to hide the payload strings) and uses `pushd` to mount a **WebDAV share**, then `rundll32.exe` to load the remote DLL.
- The injected web payload is Base64-encoded JavaScript fetched from a remote source; **EtherHiding** resolves follow-on payloads/C2 by querying data stored in a blockchain smart contract.
- The revamp hosts the malicious JavaScript on **`cdn.jsdelivr[.]net`**, a widely trusted CDN — a deliberate trust-shift from the original compromised-site hosting.
- The final stage is **Amatera Stealer**: browser credentials, session tokens, authentication artifacts, and documents.

## SynkLoader chain
- A parallel loader observed in the same campaign wave.
- **Phishes Windows passwords** — Gen Digital assesses the objective as access sales, likely feeding ransomware operations.
- Shares the ClearFake delivery and loader infrastructure patterns with WordlistLoader.

## Indicators
Compromised / abusing domains recorded by Gen Digital:
- `abogadosrosarinos[.]com`
- `aptisweb[.]com`
- `avene-hebergement[.]com`
- `https-xhamster[.]com`
- `www.caesarjaco.co[.]id`
- `skybap[.]shop`

## Defender heuristics
1. **Treat any website-presented "verification" prompt with a clipboard command as hostile** — ClearFake/ClickFake campaigns reuse the ClickFix primitive, and the fake CAPTCHA framing (not a genuine browser challenge) is the visual tell.
2. **Hunt `conhost.exe --headless` spawning `cmd.exe`** and delayed environment-variable expansion around `pushd` + `rundll32` WebDAV execution — this is the shared shape between this campaign and Microsoft's documented ACR Stealer WebDAV campaign.
3. **Add `cdn.jsdelivr[.]net` scope to JS execution review**: legitimate CDN use is normal, but a JS file fetched by an on-page inline/encoded loader from the CDN as the *last* stage of a fake-CAPTCHA chain is the EtherHiding→CDN revamp signature.
4. **Monitor blockchain dead-drop lookups** (public RPC/Web3 queries from Office/browser/terminal processes) as an EtherHiding indicator.
5. **Track the loader names**: WordlistLoader and SynkLoader are new family labels; correlate against the existing ACR Stealer / Amatera / AcridRain cluster (see the ACR Stealer page) rather than treating them as unrelated.

## Related pages
- [ACR Stealer](../tools/acr-stealer.md)
- [macOS ClickFix fingerprinting-gate campaign](macos-clickfix-fingerprinting-gate-campaign.md)
- [Trusted collaboration-channel identity abuse](../patterns/collaboration-channel-identity-abuse.md)

## Sources
- Gen Digital Threat Research: [WordlistLoader delivering Amatera via ClearFake campaigns](https://www.gendigital.com/blog/insights/research/wordlistloader-delivering-amatera-via-clearfake-campaigns)
- The Hacker News: [WordlistLoader Delivers Amatera via ClearFake Campaigns](https://thehackernews.com/2026/08/wordlistloader-delivers-amatera-via.html)
- ExpeL: [ClearFake new LoL techniques](https://expel.com/blog/clearfake-new-lotl-techniques/)
- ExpeL: [SynkLoader — when you throw in everything but the kitchen sink](https://expel.com/blog/synkloader-when-you-throw-in-everything-but-the-kitchen-sink/)
