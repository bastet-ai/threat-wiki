# Webworm

## Summary
Webworm is a China-aligned intrusion cluster publicly tracked since 2022 and newly detailed by ESET in May 2026. ESET reports that Webworm has shifted from older RAT families such as Trochilus and 9002/McRat toward stealthier proxy/VPN infrastructure and new cloud-service C2 backdoors.

The 2025 activity described by ESET targets government and enterprise environments in Europe and South Africa, with historical targeting across Russia, Georgia, Mongolia, and other Asian nations. Public reporting links Webworm to, or overlaps it with, China-nexus clusters including SixLittleMonkeys, FishMonger/Aquatic Panda, and Space Pirates; keep those relationships as overlap notes rather than strict aliases unless future primary sourcing tightens attribution.

## Tags
- actors
- groups
- China
- espionage
- Webworm
- Discord
- Microsoft Graph
- OneDrive
- proxy
- GitHub
- cloud
- Europe
- South Africa

## Why this matters
- Webworm's move toward Discord, Microsoft Graph, OneDrive, GitHub staging, SoftEther VPN, and custom proxy chains blends intrusion traffic into services defenders may already allow.
- ESET decrypted more than 400 Discord C2 messages and found victim-specific channels, which makes cloud-app telemetry and SaaS audit logs part of endpoint backdoor detection.
- The group uses public or compromised cloud infrastructure as both staging and exfiltration paths, including a compromised Amazon S3 bucket in the 2025 campaign.
- The toolset emphasizes quiet persistence and lateral routing more than noisy malware execution, so network/proxy anomalies can be more durable than file hashes.

## 2025 toolset shift
- **EchoCreep**: Discord-based backdoor that reports runtime state, receives commands, and supports file upload/download and command execution.
- **GraphWorm**: Microsoft Graph / OneDrive-based backdoor that creates victim-specific cloud directories, retrieves jobs, uploads victim data, downloads files, and can stop itself on operator command.
- **Proxy layer**: SoftEther VPN, iox, frp, and custom tools including WormFrp, ChainWorm, SmuxProxy, and WormSocket.
- **Staging**: a GitHub repository impersonating a WordPress fork was used to host malware and tooling; ESET reported that identified services including the GitHub repo and S3 bucket were taken down.

## Defender heuristics
- Hunt for unexpected Discord API traffic, Microsoft Graph/OneDrive upload sessions, or cloud-storage use from servers and admin workstations that do not normally use those services.
- Review GitHub raw-content downloads, forked popular-repo names, and staged binaries in paths that mimic legitimate project directories.
- Baseline SoftEther, frp, iox, and unusual SOCKS/proxy binaries on servers; treat proxy chains as possible command infrastructure rather than admin convenience until verified.
- Inspect S3 and other cloud-storage access patterns for exfiltration paid by the victim's own account.
- Correlate web-server brute-force/recon tooling such as dirsearch and nuclei with later proxy/VPN installs.

## Related pages
- [Dragonfly](dragonfly-energetic-bear-crouching-yeti.md)

## Sources
- ESET: <https://www.welivesecurity.com/en/eset-research/webworm-new-burrowing-techniques/>
- The Hacker News summary: <https://thehackernews.com/2026/05/webworm-deploys-echocreep-and-graphworm.html>
