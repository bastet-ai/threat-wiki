# Fake-reputation crypto clipboard hijacker

## Summary
Check Point Research reported a cryptocurrency clipboard-hijacker campaign that uses **fake reputation** across multiple public platforms to make malicious "trading", "sniper bot", and gambling-predictor tools look safe. The same operation promotes Windows and macOS Rust clippers through a WordPress phishing hub, GitHub and SourceForge projects, AI-narrated YouTube videos, crypto forums, news-site posts, and benign-looking VirusTotal community votes or comments.

The durable threat-intelligence value is not just another clipper payload. The campaign shows how adversaries can manipulate social proof — stars, forks, comments, downloads, views, reviews, and "safe" votes — to weaken user judgment and reputation-based triage before the victim ever runs the malware.

## Tags
- ops
- operations
- cryptocurrency theft
- clipboard hijacker
- clipper
- Rust malware
- macOS malware
- Windows malware
- fake reputation
- Ghost Networks
- GitHub abuse
- SourceForge abuse
- YouTube abuse
- VirusTotal sentiment abuse
- AI-generated narrator
- social engineering
- wallet theft

## Why this matters
- Reputation signals are part of the lure: Check Point observed coordinated-looking positive engagement across GitHub, SourceForge, YouTube, forums, news-site posts, and VirusTotal.
- The payloads target both Windows and macOS users, so "Mac-only" cryptocurrency or gambling audiences are not outside the blast radius.
- The malware's goal is silent transaction redirection: it waits for cryptocurrency wallet-like strings in the clipboard and replaces them with attacker-controlled wallet addresses.
- Positive community votes or comments on reputation services should not be treated as clean verdicts when the file's distribution path, user intent, or behavior is suspicious.
- The same fake-reputation playbook can be reused for more damaging payloads than clippers, including stealers or initial-access malware.

## Operational characteristics
- **Lures:** the phishing site advertised tools such as Solana / Pump.fun / DEX sniper bots, Aviator Predictor, and crash-game predictors, targeting cryptocurrency owners, gamblers, and traders looking for shortcuts.
- **Operator persona:** Check Point tied the WordPress author, Telegram contact, YouTube contact details, and older forum activity to the `@JoseCmanXD` handle; treat this as an online persona, not a verified human identity.
- **Platform promotion:** Check Point identified GitHub accounts including `Decryptor-j`, `crash-predictor1`, `roblox-script1`, `hack-scripts`, and `stake-mines` promoting related repositories and appearing to reinforce each other through stars, forks, and contributor links.
- **Download scale:** Check Point estimated just over 5,000 downloads and potential infections from the GitHub accounts it reviewed, including more than 1,250 downloads associated with a macOS "Aviator Predictor" build. SourceForge statistics showed 44,485 downloads, but Check Point assessed the numbers as suspiciously manipulated, including a large Android-origin share despite only Windows and macOS builds being offered.
- **YouTube layer:** the actor used a YouTube channel with suspicious view spikes, positive comments, older Russian-language targeting, newer English-language targeting, and AI-generated narrators over desktop demonstrations.
- **VirusTotal sentiment abuse:** Check Point observed benign votes and "safe" comments on some campaign samples, creating false reassurance when paired with low detection rates.
- **News and forum promotion:** posts on legitimate news-oriented sites and cryptocurrency forums linked back to the phishing hub. Check Point said it was unclear whether the news posts were paid/promoted posts or abuse of compromised publishing paths.
- **Windows chain:** victims downloaded ZIP archives. A visible `.exe` acted as a .NET loader and executed `src/config/silkebin.exe`, a Rust clipboard hijacker.
- **Windows persistence:** the clipper copied itself to `%APPDATA%\silke\silke.exe` and created a Startup-folder shortcut, then used Windows clipboard APIs including `AddClipboardFormatListener`, `OpenClipboard`, `GetClipboardData`, `EmptyClipboard`, and `SetClipboardData`.
- **Wallet replacement:** the Windows build checked clipboard text against cryptocurrency-address regular expressions and used an embedded list of more than 15,500 attacker-controlled wallet addresses, including about 15,000 Bitcoin-related addresses and roughly 500 Ethereum / EVM addresses.
- **macOS execution:** the macOS packages included an `!!! READ THIS - RUN UNLOCKER IF APP IS BLOCKED.txt` instruction file that told users to run `unlocker.command`, which removed quarantine attributes with `xattr -cr` and opened the selected `.app`, bypassing Gatekeeper friction through social engineering.
- **macOS persistence:** the Rust macOS clipper wrote `~/launch.sh`, installed a LaunchAgent at `~/Library/LaunchAgents/com.example..plist` with `RunAtLoad` and `KeepAlive`, and used a 30-second watchdog loop to rewrite persistence files and clone the binary with `fcopyfile`.

## Defender heuristics
- Treat inflated stars, forks, SourceForge downloads, YouTube engagement, news-site posts, and VirusTotal community comments as weak signals unless backed by code provenance, publisher history, deterministic scanning, and behavioral analysis.
- For crypto, gambling, and trading communities, warn users that "sniper bot", "predictor", "unlocker", and "free premium" tools are high-risk malware lures even when they appear popular.
- Hunt Windows endpoints for `%APPDATA%\silke\silke.exe`, Startup-folder shortcuts pointing to `silke.exe`, ZIP-extracted trading / predictor tools, and processes using clipboard listener APIs unexpectedly.
- Hunt macOS endpoints for `unlocker.command`, recent `xattr -cr` use against untrusted `.app` bundles, `~/launch.sh`, `~/Library/LaunchAgents/com.example..plist`, and LaunchAgents with suspicious `RunAtLoad` / `KeepAlive` clipboard-monitoring binaries.
- In EDR and malware triage, flag binaries that match wallet-address regular expressions and call clipboard read/write APIs in a loop, especially when distributed through social proof-heavy repositories or file-sharing pages.
- Review cryptocurrency-transfer incidents for clipboard-replacement behavior: copied address differs from pasted address, first loss occurs soon after installing a trading or prediction tool, or the endpoint shows unexpected clipboard-monitoring persistence.
- Do not rely on VirusTotal upvotes, comments, or low detection rates as a clean verdict; record them as potentially manipulated context and prioritize behavior and provenance.

## Related pages
- [Crypto Clipper Tor / USB worm](crypto-clipper-tor-usb-worm.md)
- [Solana FakeFix npm / PyPI developer stealer](solana-fakefix-npm-pypi-developer-stealer.md)
- [Polymarket npm wallet-drainer packages](polymarket-npm-wallet-drainer.md)
- [AI-brand impersonation phishing and malvertising](../patterns/ai-brand-impersonation-phishing-malvertising.md)

## Sources
- Check Point Research: [https://research.checkpoint.com/2026/from-stars-to-upvotes-fake-reputation-fueling-a-crypto-clipboard-hijacker/](https://research.checkpoint.com/2026/from-stars-to-upvotes-fake-reputation-fueling-a-crypto-clipboard-hijacker/)
