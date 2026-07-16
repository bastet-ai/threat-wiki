# CrashStealer macOS notarized-dropper campaign

## Summary
Public reporting from The Hacker News on Jamf Threat Labs' July 2026 analysis describes **CrashStealer**, a native C++ macOS information stealer distributed through a signed and Apple-notarized disk image. The lure used a gated installer flow for **Werkbit.app** and a valid Developer ID, allowing the initial dropper to pass Gatekeeper checks before staging a second payload.

CrashStealer is notable because it combines social engineering, notarized delivery, local password validation, keychain unlocking, browser/wallet/password-manager collection, AES-GCM encryption, libcurl exfiltration, LaunchAgent persistence, and re-signing of the staged payload. Jamf reportedly observed shared backend infrastructure and additional domains, suggesting a broader multi-platform campaign rather than a one-off sample.

## Tags
- ops
- macOS
- infostealer
- credential theft
- browser credential theft
- cryptocurrency wallet theft
- password manager theft
- keychain theft
- notarized malware
- Gatekeeper bypass
- Developer ID abuse
- LaunchAgent
- AES-GCM
- libcurl
- anti-analysis
- GitHub dead drop
- CrashStealer
- Werkbit
- Jamf Threat Labs
- The Hacker News

## Reported activity
- CrashStealer was distributed as a signed and Apple-notarized disk image presenting **Werkbit.app**. The disk image and binary carried Developer ID **`Emil Grigorov (WWB7JA7AQV)`** in public reporting.
- The lure domain **`werkbit[.]io`** was registered in June 2026 and reportedly gated downloads behind a meeting PIN, limiting access to visitors who had the correct code.
- On launch, the initial executable **`veltod`** contacted GitHub repository **`github.com/mgothiclove`** to retrieve **`sys.cache`**, extracted a curl command, downloaded a shell script, and staged **`CrashReporter.dmg`** in `/tmp`.
- The malware established persistence as a LaunchAgent, performed anti-analysis / security-tool checks, prompted for the user's macOS password, validated the password locally, and used it to unlock the login keychain.
- Public reporting says CrashStealer collected from browsers, cryptocurrency wallets, password managers, and the macOS keychain, encrypted collected data with AES-GCM, and exfiltrated with libcurl.
- The staged payload copied and re-signed itself, a useful macOS persistence/evasion pivot for defenders reviewing quarantine, signing, and execution telemetry.

## Indicators
| Type | Value | Notes |
| --- | --- | --- |
| Malware | `CrashStealer` | Native C++ macOS information stealer. |
| Lure app | `Werkbit.app` | Signed/notarized dropper presentation. |
| Developer ID | `Emil Grigorov (WWB7JA7AQV)` | Reported signing identity. |
| Domain | `werkbit[.]io` | Lure/download domain registered in June 2026. |
| Executable | `veltod` | Initial executable reported by THN/Jamf. |
| GitHub repo | `github.com/mgothiclove` | Used to retrieve `sys.cache` in public reporting. |
| Staging file | `sys.cache` | GitHub-hosted command/config retrieval artifact. |
| Staged DMG | `/tmp/CrashReporter.dmg` | Second-stage payload path/name reported publicly. |
| Persistence | LaunchAgent | Review recent or unsigned/suspicious LaunchAgent plists tied to the execution window. |

## Why this matters
- **Notarization changes triage assumptions.** A Gatekeeper pass does not mean the installer is safe; Apple-notarized droppers can still be malicious or later revoked after discovery.
- **The password prompt is operationally important.** Local validation lets the stealer unlock the login keychain and harvest higher-value secrets without sending repeated failed authentication events to remote services.
- **Meeting-code gating reduces researcher visibility.** PIN-gated payload delivery can keep sandboxes and casual crawlers from receiving the same installer victims see.
- **Developer and crypto users are likely high-value targets.** Browser extension storage, password managers, keychains, wallets, and SaaS sessions are all in scope for rapid post-compromise theft.

## Defender guidance
1. Hunt macOS endpoint telemetry for execution of `Werkbit.app`, `veltod`, `CrashReporter.dmg`, or downloads from `werkbit[.]io` and `github.com/mgothiclove`.
2. Review LaunchAgent additions around the suspected exposure window, especially plists launching recently created binaries in user-writable paths or `/tmp` staging flows.
3. Inspect Gatekeeper, quarantine, and code-signing telemetry for Developer ID `Emil Grigorov (WWB7JA7AQV)` and any re-signed binaries that appeared after initial execution.
4. Treat exposed hosts as credential-compromised: rotate browser-saved passwords, SSO sessions, keychain-accessible secrets, SSH/API tokens, package-registry tokens, and cryptocurrency wallet material.
5. Add user-facing detection/education for meeting-gated installer flows that instruct users to right-click and open a DMG/app outside normal managed software channels.
6. Where possible, require managed software distribution and block unsigned, ad-hoc-signed, or newly notarized applications from executing on high-risk developer and finance workstations.

## Related pages
- [macOS.Gaslight Rust backdoor](macos-gaslight-rust-backdoor.md)
- [Operation FlutterBridge FlutterShell macOS malvertising](operation-flutterbridge-fluttershell-macos-malvertising.md)
- [PamStealer](../tools/pamstealer.md)
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)

## Sources
- [The Hacker News](https://thehackernews.com/2026/07/crashstealer-macos-malware-uses.html)
- [Jamf Threat Labs](https://www.jamf.com/blog/)
