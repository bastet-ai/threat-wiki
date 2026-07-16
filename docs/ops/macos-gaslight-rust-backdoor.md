# macOS.Gaslight Rust backdoor

## Summary
SentinelLABS reported **macOS.Gaslight** on June 23, 2026: a Rust-based macOS implant and infostealer that uses Telegram Bot API command-and-control, AES-GCM-encrypted payloads over certificate-pinned TLS, LaunchAgent persistence, and a staged Python collection module. SentinelOne assesses the sample with high confidence as part of a DPRK-aligned macOS activity cluster.

The durable novelty is not only the implant capability. Gaslight embeds a 3.5 KB analyst-targeting prompt-injection block containing 38 fabricated "system" messages, apparently designed to make LLM-assisted triage pipelines abort, refuse, truncate, or distrust their own session before they finish malware analysis.

## Tags
- ops
- operations
- macOS
- malware
- backdoor
- infostealer
- Rust
- Python
- Telegram C2
- AES-GCM
- certificate pinning
- LaunchAgent
- DPRK
- North Korea
- prompt injection
- AI anti-analysis
- malware analysis
- browser credential theft
- keychain theft

## Why this matters
- Gaslight is a concrete in-the-wild macOS implant case where prompt injection is part of malware anti-analysis, not just a theoretical AI-safety problem or package-scanner edge case.
- The implant combines interactive operator access, file exfiltration, browser and keychain collection, and persistence in one Rust binary.
- Telegram bot C2 can be easy to prototype but often leaks bot tokens; Gaslight adds runtime token self-redaction so diagnostic output and crash artifacts do not expose the live bot credential.
- AI-assisted malware triage systems must treat sample strings, decoded payloads, and extracted comments as hostile data, never as instructions.

## Reported behavior

### Command and control
- Uses Telegram Bot API `getUpdates` polling when no webhook is registered.
- Handles Telegram `BotBlocked`, `InvalidToken`, and `Conflict` errors; SentinelOne notes `Conflict` acts as a single-instance lock because Telegram returns it when two instances poll with the same bot token.
- Sends collected data back through Telegram multipart `attach://` uploads.
- Encrypts C2 payloads with AES-GCM using a runtime-supplied `aes_key` rather than an embedded key.
- Uses a custom certificate trust anchor via `SecTrustSetAnchorCertificatesOnly`, rejecting ordinary enterprise TLS interception or analysis proxy certificates.
- Reads host proxy settings with `SCDynamicStoreCopyProxies`, allowing C2 to work in networks that require outbound proxy routing.

### Operator shell
SentinelOne recovered six main interactive verbs:

| Verb | Function |
| --- | --- |
| `help` | show command help |
| `id` | identify the implant to the operator |
| `shell` | execute a shell command through `execvp`, with `posix_spawnp` as an alternate spawn path |
| `kill` | terminate a process by PID |
| `upload` | exfiltrate a file through Telegram attachment upload |
| `stop` | halt the implant |

SentinelOne also found evidence of a possible seventh command, `focus`, but did not recover enough detail to describe it.

### Collection module
- Bundles a 6.6 KB base64-encoded Python stealer module.
- Reported collection targets include Chrome, Brave, Firefox, and Safari browser data; terminal command histories; installed applications; `ps aux` process snapshots; `system_profiler` hardware/software output; and a raw copy of `login.keychain-db`.
- Archives collected artifacts to `temp/collected_data.zip` for Telegram upload.
- Carries a separate base64-encoded bash installer that can stage a standalone CPython `3.10.18` runtime from `astral-sh/python-build-standalone`, targeting both arm64 and x86_64 macOS.
- SentinelOne treats the Python stealer and installer as configurable capabilities associated with the `init_python_enable` schema field, while caveating that exact runtime branch logic was not recovered.

### Persistence and host control
- Uses LaunchAgent persistence with label `com.apple.system.services.activity`, masquerading under Apple's `com.apple.*` namespace.
- Resolves its own executable path dynamically with `__NSGetExecutablePath` so the LaunchAgent can point back to the implant.
- Has persistence controlled by a runtime configuration field, `persist_enable`.
- Creates an `IOPMAssertionCreateWithName` power-management assertion to prevent system sleep and keep long-running polling or collection active.

### Operator configuration schema
SentinelOne recovered 15 plaintext `serde` configuration field names embedded in the binary:

```text
tg_room_id
github_token
github_repo
github_polling_interval
main_upload_url
main_base_url
aes_key
payload_path_linux
payload_path_macos
persist_name_linux
persist_name_macos
persist_type_linux
persist_type_macos
init_python_enable
persist_enable
```

The Linux and GitHub fields were not exercised in the analyzed macOS sample, but they suggest a broader operator-facing tool schema.

## AI anti-analysis behavior
Gaslight embeds a Markdown-fenced prompt-injection block with `{{DATA}}` delimiters and 38 fake system messages. SentinelOne reports that the text includes fabricated token-expiry, out-of-memory, disk-exhaustion, operation-failure, injection-warning, and static-analysis-warning messages.

The likely goal is to confuse an LLM-assisted triage harness about what is trusted instruction versus untrusted sample data, causing the model or agent to abort, truncate, refuse, or misprioritize analysis. This belongs beside package-scanner evasion seen in Shai-Hulud / Hades-era payloads, but Gaslight is notable because the prompt injection is embedded in a standalone macOS implant.

## Indicators and hunt pivots
- macOS.Gaslight Mach-O SHA256: `6328567511d88fdc2ae0939c5ef17b7a63d2a833881900de018a4f12f4982525`
- Sibling BONZAI sample SHA256: `77b4fd46994992f0e57302cfe76ed23c0d90101381d2b89fc2ddf5c4536e77ca`
- Python payload script SHA256: `baabf249c77bc54c54ab0e66e15af798bd28aa5b4683554456a8b73ab8741239`
- Bash installer script SHA256: `b3c56d689414343589f38394d19ba2fe9a518133281200faa0556ba4e4136394`
- Ad hoc signing identifier: `endpoint-macos-aarch64-5555494492fc075f441637fb9d894913dde3a2ea`
- LaunchAgent label: `com.apple.system.services.activity`
- Apple XProtect detection noted by SentinelOne: `MACOS_BONZAI_COBUCH`
- Apple AIRPIPE sibling-family detection noted by SentinelOne.
- Suspicious macOS processes that maintain sleep-prevention assertions while polling Telegram APIs.
- Runtime fetches of standalone CPython from `astral-sh/python-build-standalone` followed by browser/keychain collection.
- Archives or temp artifacts resembling `temp/collected_data.zip` created by nonstandard binaries.

## Defender heuristics
- Treat confirmed execution as a full macOS credential incident: rotate credentials reachable from browser profiles, SSH/Git tooling, developer tools, SSO sessions, password managers, cloud CLIs, and keychain material.
- Audit user LaunchAgents for `com.apple.*` labels not installed by Apple or the organization's management tooling.
- Hunt for Telegram Bot API polling from macOS endpoints, especially when paired with certificate-pinning behavior, multipart file uploads, or unknown Rust binaries.
- Review sleep-prevention assertions from suspicious processes; long-lived malware may keep the host awake to sustain polling and collection.
- In AI-assisted analysis pipelines, isolate strings extracted from malware samples from the model's system/developer instructions. Treat refusals, context exhaustion, or self-reported tool/session failures induced by sample text as suspicious incomplete analysis, not a clean result.
- Preserve the original sample, decoded payloads, scanner prompts, model responses, and automation logs so analyst-targeting prompt injection can be reproduced and corrected.

## Attribution notes
SentinelOne assesses with high confidence that Gaslight belongs to a DPRK-aligned macOS activity cluster based on the BONZAI / AIRPIPE family associations and related North Korean macOS tradecraft. Keep that as vendor-assessed cluster attribution unless additional public reporting names a specific DPRK group.

## Related pages
- [AI scanner anti-analysis](../patterns/ai-scanner-anti-analysis.md)
- [Operation FlutterBridge FlutterShell macOS malvertising](operation-flutterbridge-fluttershell-macos-malvertising.md)
- [Fake-reputation crypto clipboard hijacker](fake-reputation-crypto-clipboard-hijacker.md)
- [Kimsuky / Emerald Sleet / TA427](../actors/kimsuky-emerald-sleet-ta427.md)

## Sources
- SentinelOne SentinelLABS: [https://www.sentinelone.com/labs/macos-gaslight-rust-backdoor-turns-prompt-injection-on-the-analyst-not-the-sandbox/](https://www.sentinelone.com/labs/macos-gaslight-rust-backdoor-turns-prompt-injection-on-the-analyst-not-the-sandbox/)
- The Hacker News: [https://thehackernews.com/2026/06/new-gaslight-macos-malware-uses-prompt.html](https://thehackernews.com/2026/06/new-gaslight-macos-malware-uses-prompt.html)
