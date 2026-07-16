# Operation FlutterBridge FlutterShell macOS malvertising

## Summary
**Operation FlutterBridge** is a Unit 42-tracked macOS malvertising campaign that distributes **FlutterShell**, a new Flutter-built backdoor masquerading as legitimate desktop applications. Unit 42 tracks the activity with the cybercrime cluster **CL-CRI-1089**, which has operated since at least 2023 and previously distributed Windows and macOS malvertising payloads including RecipeLister, Calendaromatic, and JSCoreRunner-style macOS malware.

The durable intelligence value is the shift from nuisance adware toward signed, notarized macOS applications with full backdoor primitives. FlutterShell uses a WebView and JavaScript-to-native bridge so attacker-controlled web content can drive local command execution, file access, environment-variable collection, browser hijacking, and possible AI-summarization data exfiltration without redistributing a new binary.

## Tags
- ops
- operations
- Unit 42
- CL-CRI-1089
- cybercrime
- malvertising
- macOS
- Flutter
- FlutterShell
- JSCoreRunner
- Google Ads
- signed malware
- notarized malware
- adware
- backdoor
- browser hijacking
- WebView
- JavaScript bridge
- credential theft
- AI data exfiltration

## Why this matters
- Unit 42 reports hundreds of Google-verified advertisements and a shell-company ad-delivery network, giving the campaign global reach with emphasis on Anglophone and Western European users.
- Observed samples were signed with valid Apple Developer IDs and passed Apple notarization at submission time, so user trust and platform checks are not enough to treat the applications as safe.
- FlutterShell looks like adware in observed executions, but its built-in primitives support arbitrary shell command execution, file reading/writing, directory enumeration, environment-variable extraction, and WebView-driven behavior changes.
- Because malicious logic is hosted remotely through `/getConfig` and `/getUpdateThanksConfig`, defenders should treat static binary review as incomplete; the operator can alter behavior server-side.
- Some variants route documents through attacker-controlled infrastructure before AI summarization, creating a data-exposure path that may be mistaken for a benign productivity feature.

## Reported operation
- **Cluster:** Unit 42 tracks the activity as **CL-CRI-1089**, a financially motivated cybercrime cluster active since at least 2023.
- **Predecessor activity:** Unit 42 connects FlutterBridge to JSCoreRunner, first identified in August 2025, and notes shared JavaScript-to-native bridge architecture and overlapping command primitives.
- **Delivery:** The operators use Google Ads and Google-verified shell entities to advertise malicious desktop applications that masquerade as useful tools.
- **Masquerades:** Unit 42 observed FlutterShell variants posing as `PodcastsLounge`, `PDF-Brain`, and `PDF-Ninja`.
- **Signing and notarization:** Observed FlutterShell samples were signed with valid Apple Developer IDs and successfully notarized by Apple before detection.
- **Observed payload behavior:** The malware hijacked Google Chrome configuration to route traffic through an attacker-controlled ad-filled intermediary site.
- **Active development:** Unit 42 found versions without active malicious code, disabled or unfinished JavaScript functions, and rapidly changing variants, suggesting continued development rather than a finished one-off malware family.

## Technical shape
- FlutterShell is built with the Flutter framework, compiling Dart logic into a dynamic library and object-pool structure that complicates static analysis.
- The application loads attacker-controlled web content in a WebView and injects a JavaScript bridge named `flutterInvoke`.
- The web content sends JSON-formatted commands into the native Dart environment, turning remote page logic into local system operations.
- Core remote configuration paths include `/getConfig` and `/getUpdateThanksConfig`; Unit 42 observed payload logic hidden behind an `/update-thanks.html` path.
- The remote-control model lets operators change behavior without rebuilding or redistributing the signed application.
- Unit 42 reported some variants with the `com.apple.security.files.downloads.read-write` entitlement, allowing read/write access to the user's Downloads directory.

## Built-in capabilities
Unit 42 lists FlutterShell commands across the `PodcastsLounge`, `PDF-Brain`, and `PDF-Ninja` variants, including:

- **Execution:** `exec_sync`, `pdf_sync`, `renderPDF` for shell-command or rendering workflows.
- **Filesystem:** `read_file`, `write_file`, `read_dir`, `exists`, `get_home_dir`, `read_pdf`, `write_pdf`, `read_pdf_dir`, `pdf_exists`, and `get_pdf_dir`.
- **Harvesting:** `get_env` for environment-variable extraction, a high-value source of API keys and secondary-access material.
- **UI manipulation:** `close_webview` and `setSize`, likely to manage suspicion or user interaction.

Unit 42 also reports six shared core primitives with JSCoreRunner: file/directory existence checks, command execution, file reading, file writing, directory enumeration, and home-directory discovery.

## Defender heuristics
- Treat a signed and notarized macOS app delivered through search ads as still requiring endpoint and network scrutiny when the installer source is not vendor-authentic.
- Hunt for `PodcastsLounge`, `PDF-Brain`, and `PDF-Ninja` installations, related DMGs, and unexpected Apple Developer ID-signed apps first seen through ad-click download flows.
- Inspect Chrome configuration changes that force traffic through unfamiliar intermediary sites or ad-injection infrastructure.
- Monitor macOS applications embedding Flutter WebViews that call remote configuration paths such as `/getConfig`, `/getUpdateThanksConfig`, or `/update-thanks.html` and then invoke local filesystem or shell actions.
- Alert on WebView-to-native bridge activity that exposes shell execution, file access, directory listing, home-directory discovery, or environment-variable extraction to remote JavaScript.
- Review environment-variable exposure on infected hosts as potential credential theft, not only as adware telemetry.
- For AI/productivity-themed macOS utilities, verify whether local documents are sent to the advertised AI provider directly or routed through an unexpected intermediary server.
- Use browser-hijacking alerts as a pivot into full endpoint triage; Unit 42 specifically frames FlutterShell as adware with backdoor capabilities.

## Selected indicators and pivots
- **Campaign / cluster names:** Operation FlutterBridge, FlutterShell, CL-CRI-1089, JSCoreRunner.
- **Masqueraded apps:** `PodcastsLounge`, `PDF-Brain`, `PDF-Ninja`.
- **Bridge name:** `flutterInvoke`.
- **Remote configuration paths:** `/getConfig`, `/getUpdateThanksConfig`, `/update-thanks.html`.
- **macOS entitlement:** `com.apple.security.files.downloads.read-write`.
- **Unit 42 example domain in investigation UI:** `atsheisdomestic[.]org`.

Use Unit 42's indicator tables for the current SHA256 values, actor-related websites, and infrastructure because the family is still changing.

## Related pages
- [TamperedChef-style productivity malware clusters](tamperedchef-productivity-malware-clusters.md)
- [AI chatbot and SEO poisoning GPU-cryptojacking campaign](ai-chatbot-seo-poisoning-gpu-cryptojacking.md)
- [codexui-android OpenAI token stealer](codexui-android-openai-token-stealer.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- [Unit 42](https://unit42.paloaltonetworks.com/flutterbridge-new-fluttershell-backdoor/)
