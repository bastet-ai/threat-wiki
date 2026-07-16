# ScarCruft Yanbian game-platform supply-chain attack

## Summary
ESET reported an ongoing ScarCruft supply-chain attack against a video game platform serving the Yanbian region in China, where ethnic Koreans and North Korean refugees/defectors are a key target population.

ScarCruft compromised both Windows and Android distribution lanes for Yanbian-themed games. The Windows client update path led to RokRAT and then BirdCall, while trojanized Android games carried an Android BirdCall variant that ESET described as new to ScarCruft's public toolset.

## Tags
- ops
- operations
- supply-chain
- ScarCruft
- APT37
- Reaper
- North Korea
- espionage
- Android
- Windows
- RokRAT
- BirdCall
- Yanbian

## Why this matters
- This is a regional supply-chain compromise aimed at a sensitive diaspora/refugee population rather than a broad developer ecosystem.
- ScarCruft used a legitimate niche gaming platform as the trust boundary, compromising official game downloads and updates instead of relying only on phishing.
- The campaign adds an Android BirdCall branch to a tool previously known publicly as Windows-focused, expanding mobile collection risk for ScarCruft targets.
- The same operation spans desktop update compromise and mobile app trojanization, so defenders should not scope triage to one platform.

## Reported chain
- ESET found a suspicious Android APK on VirusTotal and traced it back to the official `sqgame[.]net` gaming platform.
- The platform served Yanbian-themed Windows, Android, and iOS games.
- At least two Android games available from the official site were trojanized with Android BirdCall.
- The Windows client was compromised through a malicious update chain.
- The Windows chain led to RokRAT and then a more sophisticated BirdCall backdoor.
- ESET assessed the activity as probably ongoing since late 2024.

## Tooling and capabilities
### BirdCall Windows
ESET describes BirdCall as a C++ Windows backdoor discovered in 2021 and attributed to ScarCruft in ESET Threat Intelligence reporting. Publicly reported capabilities include:

- screenshots;
- keystroke and clipboard logging;
- credential and file theft;
- shell command execution;
- C2 through legitimate cloud storage services such as Dropbox or pCloud, or through compromised websites;
- multistage loading with Ruby or Python scripts and components encrypted with a computer-specific key.

### BirdCall Android
ESET reported Android BirdCall in this supply-chain attack and described seven observed versions from roughly October 2024 through June 2025. Publicly reported collection includes:

- contacts;
- SMS messages;
- call logs;
- documents and media files;
- private keys;
- screenshots;
- surrounding audio recordings.

## Targeting and motivation
ScarCruft, also tracked as APT37 or Reaper, is widely described as a North Korea-aligned espionage group. ESET says this operation targeted people in the Yanbian region of China, including a population relevant to North Korean refugee and defector monitoring.

Keep the targeting statement specific to ESET's reporting unless another primary source expands it. The available public source supports espionage against a regional community platform; it does not support treating every gaming-platform compromise as ScarCruft activity.

## Defender heuristics
- For at-risk communities, inventory niche regional software distribution channels, not only mainstream app stores and enterprise software.
- Treat official game/update downloads as suspect if they came from the affected platform during the reported compromise window.
- Hunt for both desktop and mobile indicators when one platform in a trusted ecosystem is found compromised.
- Review updater behavior for unexpected script loaders, cloud-storage C2 usage, and staged backdoor deployment.
- On Android, prioritize triage of games requesting broad access to contacts, SMS, call logs, files, screen capture, or microphone recording.

## Attribution notes
ESET attributes the campaign to ScarCruft, also known as APT37 or Reaper. This page follows that attribution and keeps operation details separate from broader North Korea activity unless later public reporting provides stronger overlap.

## Related pages
- [Supply-chain group profile](../patterns/supply-chain-actor-profile.md)
- [3CX desktop app compromise](3cx-desktop-app-compromise.md)
- [CCleaner signed-update compromise](ccleaner-signed-update-compromise.md)

## Sources
- [ESET](https://www.welivesecurity.com/en/eset-research/rigged-game-scarcruft-compromises-gaming-platform-supply-chain-attack/)
