# Operation Muck and Load GitHub lure network

## Summary
Socket reported **Operation Muck and Load** on July 8, 2026: a malicious Go module exposed a broader GitHub lure-and-malware network built around commit-farmed repositories, public dead-drop resolution, protected archive delivery, and Windows RAT / infostealer staging. Socket's validated core contained **222 GitHub repositories across 190 accounts** that combined a reused actor-linked workflow signature with artificial commit activity.

The entry-point module, `github[.]com/kaleidora/dnsub-scanning-tool`, impersonated a DNS / subdomain scanner but embedded hidden PowerShell staging that retrieved encoded content from Muck-themed infrastructure, decoded it with `certutil`, and launched a multi-layer loader. Socket said the Go security team blocked the malicious module from the Go module proxy after notification.

## Tags
- ops
- operations
- supply-chain
- Go
- Go modules
- GitHub
- GitHub Actions
- commit farming
- synthetic commits
- source-repository poisoning
- dead-drop resolver
- PowerShell
- certutil
- password-protected archive
- AsyncRAT
- Quasar
- Remcos
- Vidar Stealer
- XMRig
- BitMiner
- infostealer
- RAT
- developer-targeting
- Muck and Load
- ischhfd83
- Socket

## Why this matters
- The malicious package was only the visible tip. The durable defender signal is the surrounding GitHub reputation layer: many disposable-looking projects made to appear active, plausible, and recently maintained.
- The campaign targets audiences already likely to run untrusted code: cryptocurrency / Web3 users, wallet tooling seekers, Telegram bot users, game-cheat users, crypter and password-tool users, and offensive-tooling audiences.
- Public dead drops and encrypted resolver material make infrastructure takedown incomplete; the actor can rotate the payload location without changing the first-stage loader.
- Commit-farmed repositories can defeat superficial trust cues such as recent activity, many commits, and owner-specific commit names.
- Go module, source-repository, and GitHub release delivery paths deserve the same suspicion normally applied to package-registry lifecycle hooks.

## Attack chain
1. A victim discovers or is directed to a scanner-themed Go module, `github[.]com/kaleidora/dnsub-scanning-tool`, presented as a DNS / subdomain enumeration tool.
2. The module's `main.go` launches hidden PowerShell before meaningful scanner logic runs. Socket noted excessive horizontal whitespace hid the malicious logic from casual review.
3. PowerShell downloads `hxxps://muckcoding[.]com/LG-LW/Api-Certificate` to `C:\Users\Public\Pictures\api.db`, decodes it with `certutil`, writes `C:\Users\Public\Pictures\L.ps1`, and executes it with `-ExecutionPolicy Bypass`.
4. `L.ps1` uses Base64, XOR decryption, and `Invoke-Expression` layers to recover a resolver script.
5. The resolver searches public dead drops for the marker `LastW`, decrypts recovered payload-location material with key `UIA14fogylw8ogL82FntOFGp6`, and resolves a GitHub release URL for `Quixo.7z`.
6. The loader downloads the password-protected archive, extracts it with a staged 7-Zip binary, and launches `Microsoft.exe` from a fake Microsoft Photos path under `C:\ProgramData\Windows.Microsoft.Photos\current\`.
7. Downstream behavior maps to RAT / infostealer activity including AsyncRAT, Quasar, Remcos-style payloads, browser credential access, screenshots, persistence, Defender / UAC modification, and Telegram or public-web-service communications.

## GitHub lure infrastructure
Socket validated a conservative core of **222 repositories across 190 accounts** where the same threat-actor workflow signature appeared with synthetic commit activity. The recurring workflow:

- configured Git with the actor-linked email `ischhfd83@rambler[.]ru` while setting the visible commit name to `${{ github.repository_owner }}`;
- rewrote timestamp or log-style files;
- committed messages such as `LOG` or lure-specific variants;
- force-pushed through `ad-m/github-push-action@master`; and
- ran on very frequent schedules, in some cases every minute.

This creates owner-specific commit activity while preserving a reusable hidden email pivot. Socket cautions that the 222-repository number is the confirmed workflow-bearing core, not every suspicious repository or every related lure.

## Payload and staging notes
- The Go module reportedly had more than 1,200 versions, over 700 of them malicious, likely due to GitHub Actions timestamp commits surfacing as Go pseudo-versions.
- The first-stage local paths were `C:\Users\Public\Pictures\api.db` and `C:\Users\Public\Pictures\L.ps1`.
- The loader disabled certificate validation and forced TLS 1.2.
- Dead-drop and fallback services included Pastebin, Rlim, Telegram, YouTube, Instagram, Google Docs, GitCode, and Muck-themed domains.
- The resolved archive URL observed by Socket was `hxxps://github[.]com/tb78/expresso/releases/download/Release/Quixo.7z`.
- The archive password was `r8NnX1b8Xn`.
- The fake execution path was `C:\ProgramData\Windows.Microsoft.Photos\current\Microsoft.exe`; Socket noted the executable was signed by Exodus Movement, Inc., not Microsoft.
- Confirmed malware-bearing repositories in the cluster contained loaders / downloaders, Vidar infostealer, spyware / dropper payloads, and XMRig / BitMiner-related Monero miners.

## Selected indicators and pivots
- `github[.]com/kaleidora/dnsub-scanning-tool`
- `muckcoding[.]com`
- `muckdeveloper[.]com`
- `hxxps://muckcoding[.]com/LG-LW/Api-Certificate`
- `hxxps://muckdeveloper[.]com/LGTV/MicrosoftCur`
- `hxxps://github[.]com/tb78/expresso/releases/download/Release/Quixo.7z`
- `ischhfd83@rambler[.]ru`
- `LastW`
- `UIA14fogylw8ogL82FntOFGp6`
- `C:\Users\Public\Pictures\api.db`
- `C:\Users\Public\Pictures\L.ps1`
- `C:\Users\Public\Documents\umun\`
- `C:\ProgramData\zipathh\7zrr.exe`
- `C:\ProgramData\Windows.Microsoft.Photos\current\Microsoft.exe`
- `ad-m/github-push-action@master`
- `Quixo.7z` SHA-256: `73c807df26427d6631088a822fa54c30975afbe681a9d83eff5d19e5b075d6c2`
- related `Quixo.7z` SHA-256: `a628ad47fe93ee7413cca90aeca8f9540bfcd5ccdbeb4d9914670b3ef66247f4`
- extracted `Microsoft.exe` SHA-256: `4ea1c577247b149489506b230e7aa203e1a2fa124109c6056d1986e944f520a4`

## Defender guidance
- Treat obscure packages and repositories with abnormal version counts, synthetic commit churn, or recent-activity-only trust cues as high risk.
- Hunt GitHub repositories for workflows that combine `ischhfd83@rambler[.]ru`, owner-name commit attribution, every-minute schedules, timestamp/log rewrites, force-push behavior, and `ad-m/github-push-action@master`.
- Review Go module dependencies and module-cache content for `github.com/kaleidora/dnsub-scanning-tool` and for pseudo-version sprawl from small or newly created projects.
- Detect package or repository code that launches hidden PowerShell, uses `certutil -decode`, writes scripts under `C:\Users\Public\Pictures`, disables certificate validation, or uses `-ExecutionPolicy Bypass` during setup or tool execution.
- Block or inspect downloads from public dead-drop platforms when scripts search for marker strings and decrypt payload URLs at runtime.
- Alert on fake Microsoft application paths under `C:\ProgramData\Windows.Microsoft.Photos\`, especially `Microsoft.exe` launched from a non-standard Photos directory.
- Treat positive hits as credential-theft incidents: preserve the repository/package artifact, process tree, PowerShell logs, downloaded archives, browser credential access telemetry, and GitHub audit evidence before rotating affected credentials.

## Attribution notes
Socket assesses with high confidence that Operation Muck and Load belongs to the same broader repository-backdoor activity cluster previously reported around `ischhfd83`, based on repeated repository automation, lure design, staging architecture, payload delivery, and post-execution behavior. Track the email and Muck domains as pivots, not as stable attribution boundaries.

## Related pages
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [Git hash chain malleability](../patterns/git-hash-chain-malleability.md)
- [PolinRider cross-ecosystem supply-chain campaign](polinrider-cross-ecosystem-supply-chain.md)
- [Vidar / XMRig Factory-v3 malvertising campaign](vidar-xmrig-factory-v3-malvertising-campaign.md)

## Sources
- [Socket](https://socket.dev/blog/malicious-go-module-exposes-github-malware-lure-network)
