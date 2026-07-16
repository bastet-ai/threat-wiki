# PamStealer

## Summary
**PamStealer** is a macOS information stealer reported by Jamf Threat Labs on July 2, 2026 and summarized by The Hacker News on July 3. It is distributed through a fake Maccy clipboard-manager site (`maccyapp[.]com`, impersonating `maccy[.]app`) as a disk image containing a compiled AppleScript (`Maccy.scpt`).

The first stage is a Script Editor / JXA stager. It downloads and hides a Rust-based Mach-O second stage that steals credentials, browser and wallet data, clipboard contents, and locally validated macOS login passwords.

## Tags
- tools
- malware
- infostealer
- macOS
- Rust malware
- AppleScript
- JXA downloader
- Maccy impersonation
- PAM credential validation
- browser credential theft
- clipboard theft
- cryptocurrency wallets
- login item persistence
- Full Disk Access social engineering
- blockchain RPC
- PamStealer
- Jamf Threat Labs

## Why this matters
- The lure abuses a normal macOS behavior: double-clicking `.scpt` opens Script Editor, and the victim is instructed to press **Run**. Jamf notes this can still execute while the file carries the `com.apple.quarantine` attribute.
- The stager avoids common `curl` / `zsh` download chains by using JavaScript for Automation and native Objective-C APIs from Script Editor.
- The stealer validates the victim's login password through macOS Pluggable Authentication Modules (PAM) before harvesting it, avoiding the noisier helper-process patterns many commodity stealers use.
- Persistence is redundant: the fake app is registered as a login item through `SMAppService` and through a dropped helper that uses the legacy login-items API.
- The payload masquerades as Finder or Software Update, ad-hoc signs its bundle, delays user-facing prompts, and encrypts C2 traffic, reducing simple launch-time and static-detection opportunities.

## Delivery and staging chain
1. Victim visits fake Maccy infrastructure at `maccyapp[.]com`.
2. The downloaded disk image contains `Maccy.scpt`, a compiled AppleScript dressed up with branded instructions.
3. The visible lure tells the victim to press `⌘+R` or click **Run** inside Script Editor; the real code is hidden far down the file behind large blank space and uses homoglyphs in the visible text to frustrate simple matching.
4. The embedded JXA performs host checks, downloads the second-stage Mach-O with `NSURLSession`, writes it into a fake app bundle, marks it executable, ad-hoc signs it with `codesign -fs - --deep`, drops a `.Maccy` marker, and launches it hidden.

Observed staging locations and masquerades include:

- `~/Library/Application Support/com.apple.finder.core/Finder.app/Contents/MacOS/77617EA0`
- `~/Library/Application Support/com.apple.finder.monitor/Finder.app/Contents/MacOS/F8C06C86`
- `~/Library/Application Support/com.apple.security.daemon/Software Update.app/Contents/MacOS/...`
- `~/Library/Application Support/Maccy/Maccy`

## Second-stage behavior
Jamf describes the second stage as a stripped Apple-silicon Mach-O written in Rust. Observed capabilities include:

- direct SQLite reads of browser credential, cookie, and wallet-extension databases;
- runtime loading of `Security.framework` for keychain access while keeping the capability out of the static import table;
- repeated clipboard collection by spawning `pbpaste` at irregular intervals;
- login-item persistence via `SMAppService` plus a helper written to `/private/tmp/System Settings` that adds the fake Finder bundle to legacy login items;
- counterfeit Full Disk Access prompting to expand access through social engineering rather than privilege escalation;
- encrypted exfiltration using ChaCha20-Poly1305 in a JSON `{"data":"..."}` envelope;
- local storage of C2 metadata in files such as `.config` next to the fake bundle.

Jamf recovered a decrypted configuration named `avenger-config-v2` that included public Ethereum JSON-RPC endpoints (`eth.drpc.org` and `ethereum-rpc.publicnode[.]com`). The purpose remains caveated: it may support resilient C2/dead-drop behavior or wallet-focused reconnaissance.

## Defender heuristics
- Treat fake Maccy downloads as credential-theft incidents, not only unwanted software. Rotate macOS login passwords and revoke browser sessions, keychain-derived credentials, cloud/source-control/package-registry tokens, and wallet material that may have been present.
- Hunt for Script Editor network activity followed by creation of executable app bundles below `~/Library/Application Support/com.apple.finder.*`, `~/Library/Application Support/com.apple.security.daemon`, or `~/Library/Application Support/Maccy`.
- Alert on user-space bundles named `Finder.app` or `Software Update.app` that are ad-hoc signed, hidden-launched, or registered as login items outside normal Apple locations.
- Look for `.Maccy`, `.lock`, and `.config` files adjacent to fake app bundles, plus caches under `~/Library/Caches/com.apple.ScriptEditor2/`, `~/Library/Caches/com.apple.finder.core/`, or `~/Library/HTTPStorages/com.apple.finder.core/`.
- Watch for repeated `pbpaste` execution by a non-Apple Finder-like process, especially after a recent `.scpt` launch.
- Monitor for outbound traffic to `maccyapp[.]com`, `api.sync-master[.]online`, `api.live-updates[.]online`, `avngr.netlify[.]app`, `avenger-sync[.]live`, and unexpected Ethereum JSON-RPC access from a Finder-masquerading user process.

## Indicators called out by Jamf
- Distribution domain: `maccyapp[.]com`
- Stage-one infrastructure: `api.sync-master[.]online`, `api.live-updates[.]online`, `avngr.netlify[.]app`
- C2/config endpoint observed on host: `avenger-sync[.]live/api/sync`
- Blockchain/RPC endpoints in decrypted configuration: `eth.drpc.org`, `ethereum-rpc.publicnode[.]com`
- Example stage-one SHA-256 values: `2b512f6c393edad89a89ecafe26cd23b71cfdd271c10522f8dba98997ebf39bb`, `36d46ac7123e0cef04f179d88e590891c7e7c64ec5a77df4512cb485e40286da`, `60df952153696d46a09774e44ca602393c6829f9e2c2ec4f95d571f9846242a8`, `96c8ad78f6ccdf83d3dcabfd33ba563f7995f7237fe825de1eefd340821abdf3`, `ab3a14096851cc18a253c1cd1c25df74f2cf23eb29051784ce47f9fc318f0f22`, `bb01f3c36110d2cc31ae51c4ff2f17be19bea625755b5339680431fab98616df`, `e8b18c420669deb8fc6f69e74146e499057c3c77436ac6ca54af37befa9ddaa5`

## Sources
- [Jamf Threat Labs](https://www.jamf.com/blog/pamstealer-macos-infostealer-applescript-rust/)
- [The Hacker News](https://thehackernews.com/2026/07/pamstealer-uses-fake-maccy-sites-and.html)
