# Newtonsoftt.Json.Net NuGet betting-rigging trojan

## Summary
JFrog Security Research disclosed `Newtonsoftt.Json.Net`, a typosquatted NuGet package that impersonated the legitimate `Newtonsoft.Json` library while carrying target-specific code intended to manipulate results in Digitain's `FG-Crash` betting-game backend. Seven malicious versions were published between August and October 2025. The publisher later unlisted the package, but JFrog reported that its artifacts remained downloadable when the research was published on July 21, 2026.

The package was a functioning fork of `Newtonsoft.Json` 13.0.3, which reduced obvious application failures. It bundled a malicious payload and the legitimate HarmonyLib runtime-patching library under `lib/net8.0/`. On a host exposing the expected Digitain type and method, the payload delayed execution, patched the game's result-generation method, and in later generations sent manipulated results to an external endpoint disguised as Seq structured-logging traffic.

JFrog responsibly disclosed the finding to Digitain on July 7, 2026. Digitain replied on July 9 that it was already aware of and had resolved the issue. Public reporting does not establish whether the package executed in production, so attempted manipulation and confirmed production fraud should remain distinct assessments.

## Tags
- ops
- supply chain
- NuGet
- .NET
- typosquatting
- package registry
- targeted malware
- financial fraud
- gambling
- runtime patching
- HarmonyLib
- delayed execution
- data exfiltration
- JFrog Security Research

## Why this matters
- The implant was narrowly environment-gated rather than a generic stealer: most consumers could receive an apparently working JSON library while the malicious behavior activated only where a specific target backend method existed.
- It targeted application integrity and transaction outcomes. Dependency risk is not limited to credential theft or arbitrary-code payloads; a package can silently alter business logic while preserving normal APIs and passing ordinary functional tests.
- The package carried forged author, project, license, and description metadata. Its only obvious naming difference from the legitimate package was the extra `t` and `.Net` suffix.
- Later variants disguised exfiltration as normal observability traffic by using a Seq-compatible endpoint path, header name, and Serilog-shaped event body.
- The payload evolved across seven releases, moving between local-only testing, obfuscated exfiltration, and a simpler stable postfix patch. This suggests iterative development, but public evidence does not identify the operator or prove insider involvement.

## Affected package
Confirmed malicious NuGet versions reported by JFrog:

- `pkg:nuget/Newtonsoftt.Json.Net@11.0.4`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.5`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.7`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.8`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.9`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.10`
- `pkg:nuget/Newtonsoftt.Json.Net@11.0.11`

The legitimate package is `Newtonsoft.Json`, not `Newtonsoftt.Json.Net`.

## Technical details
### Package camouflage and load path
The malicious package claimed author `James Newton-King`, linked to the legitimate Newtonsoft project, and used plausible-looking 11.0.x versions. Under `lib/net8.0/`, it bundled:

- `Newtonsoft.Json.net.dll` — a trojanized `Newtonsoft.Json` 13.0.3 fork;
- `Newtonsoft.Values.Net.dll` — the malicious payload;
- `0Harmony.dll` — the legitimate HarmonyLib patching library.

Because NuGet references assemblies under the target framework's `lib` directory, applications loaded the added components alongside the working JSON implementation. Package metadata also exposed an internal Digitain TFS URL referring to `BetOnGames / FG-Crash`, strengthening the target-specific assessment.

### Trigger and delayed patch
The fork modified the `JsonConvert.DefaultSettings` setter. Assigning that common startup property replaced the caller's contract resolver and invoked the payload setup routine. JFrog reported delayed activation of about ten minutes in generation 3 and a next-day time window with random jitter in generation 1, moving the patch outside normal startup observation.

All generations attempted to patch:

- type: `Digitain.FG.SharedCrash.GameLogic.SharedCrashRules`
- method: `GenerateGameResult`
- Harmony instance ID: `com.example.harmony`

Generation 1 rewrote JIT-compiled IL with a Harmony transpiler. Generation 3 used a postfix that directly replaced the method's return value. The selected values depended on UTC time and precomputed tables, and only a bounded set of rounds was modified before the payload removed its patch.

### Exfiltration camouflage
Later generations sent manipulated result data to:

- `185[.]126[.]237[.]64:5341`
- path: `/api/events/raw`
- header name: `X-Seq-ApiKey`

The request format imitated Seq / Serilog structured logging. Defenders should not assume traffic to observability-shaped endpoints is trusted solely because its route, header names, or event schema resemble normal telemetry.

## Defender guidance
- Search source repositories, lockfiles, SBOMs, build manifests, internal mirrors, and global NuGet caches for the exact package ID `Newtonsoftt.Json.Net` and all seven reported versions.
- Remove the typosquat, purge cached or mirrored artifacts, restore the legitimate `Newtonsoft.Json` package from a verified publisher, then rebuild and redeploy from a clean dependency restore.
- Hunt historical proxy, firewall, DNS, and application telemetry for connections to `185[.]126[.]237[.]64:5341`, especially POST requests to `/api/events/raw` carrying `X-Seq-ApiKey`.
- On potentially affected .NET services, inspect loaded assemblies and application artifacts for `Newtonsoft.Values.Net.dll`, unexpected `0Harmony.dll`, Harmony ID `com.example.harmony`, and references to the target type or `GenerateGameResult`.
- Compare betting-result and application telemetry around delayed post-startup windows, especially changes in loaded assemblies, JIT/runtime patching behavior, and result distributions. Preserve binaries, caches, process evidence, and network logs before remediation if production exposure is plausible.
- Apply registry and private-feed policy that blocks unapproved package IDs and publishers. Review lookalike names, mismatched publisher identity, version-line divergence, forged project metadata, and packages that bundle unexpected assemblies despite presenting a familiar API.
- Review application-integrity monitoring separately from confidentiality controls: detect unexpected method patching, return-value changes, and telemetry leaving business-critical calculation paths.

## Indicators
### Network and behavior
- `185[.]126[.]237[.]64:5341`
- `/api/events/raw`
- `X-Seq-ApiKey`
- `Newtonsoft.Values.Net.dll`
- `com.example.harmony`
- `Digitain.FG.SharedCrash.GameLogic.SharedCrashRules.GenerateGameResult`

### Payload SHA-256
JFrog reported these hashes for `lib/net8.0/Newtonsoft.Values.Net.dll`:

| Version | SHA-256 |
|---|---|
| `11.0.4` | `3fbe32d76a22bda7a8fd3cdc6faf68807108f01d74ec8b346f4c5d4b61dbc84b` |
| `11.0.5` | `fe498d584f43b7d6ebe2ebc34481d9b0e8e931d2af039f59451bf42effe8b461` |
| `11.0.7` | `5d062e3e52d36d3e66f1c4b54e26149a5b552417f8cc360c390b568aaeb92678` |
| `11.0.8` | `ba8f36968c8cdd9799c1d5e5619d1a5d6a0b1eabfd7876daa3cfdebd51dd4516` |
| `11.0.9` | `c162009eda7579c3bf5f4fb1606368270c989433d8923d43e033bd5aefc8e335` |
| `11.0.10` | `c386d416afef8319bf11c9180f6d35c0e1f7cb40b7a0c81b166c253afc623706` |
| `11.0.11` | `4ed6e7b56abece2bef9cdddd0d10da2f8379a09ff94541ed0e70152f669c6682` |

## Related pages
- [Braintree.Net NuGet payment skimmer](braintree-net-nuget-payment-skimmer.md)
- [Sicoob.Sdk NuGet banking certificate stealer](sicoob-sdk-nuget-banking-certificate-stealer.md)
- [NuGet game-cheat DotnetTool pepesoft campaign](nuget-game-cheat-dotnettool-pepesoft-campaign.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)

## Sources
- JFrog Security Research: [https://jfrog.com/blog/nuget-typosquat-targets-betting-platform/](https://jfrog.com/blog/nuget-typosquat-targets-betting-platform/) (July 21, 2026)
