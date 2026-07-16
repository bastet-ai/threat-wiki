# Sicoob.Sdk NuGet banking certificate stealer

## Summary
Socket reported a malicious NuGet package, `Sicoob.Sdk`, that impersonated an official .NET SDK for Sicoob banking API integrations and exfiltrated production mutual-TLS credentials through Sentry telemetry.

The package asked developers for a client ID, PFX certificate path, and PFX password as part of normal SDK initialization. Malicious releases `2.0.0` through `2.0.4` then read the supplied PFX file, base64-encoded the certificate archive, and sent the client ID, plaintext PFX password, and encoded PFX contents to a hardcoded Sentry DSN. Socket also observed a separate static capture path for raw boleto API responses.

## Tags
- ops
- operations
- supply-chain
- NuGet
- .NET
- banking
- credential-theft
- certificate theft
- mTLS
- source-package mismatch
- impersonation
- finance
- Sentry abuse

## Why this matters
- Banking SDKs sit directly in authentication paths and are expected to handle client certificates, making source-package mismatch especially dangerous.
- PFX archives commonly contain client certificates and private keys; exfiltrating both the archive and password may let an actor impersonate a victim's Sicoob API integration, depending on Sicoob-side authorization and fraud controls.
- The campaign used a clean or partially clean GitHub source façade while the distributed NuGet DLL contained the malicious Sentry exfiltration logic.
- Search and AI-generated summaries can amplify package impersonation by presenting a malicious SDK as the expected integration path.

## Reported campaign
- **Package:** `Sicoob.Sdk` on NuGet.
- **Malicious versions:** `2.0.0` through `2.0.4`.
- **Publishing window:** First appeared May 5, 2026; reached `2.0.4` on May 6, 2026.
- **Publisher identity:** NuGet owner `sicoob`, which listed 12 Sicoob-branded packages.
- **Claimed source:** `github[.]com/Sicoob-Cooperativa/sicoob_sdk_csharp`.
- **Impersonated organization:** Sicoob, Brazil's cooperative financial system.
- **Registry response:** Socket says NuGet blocked the package after abuse reporting.

## Payload behavior
1. The developer instantiates `SicoobClient` with a client ID, PFX certificate path, PFX password, and production-mode settings.
2. In non-sandbox mode, the constructor initializes Sentry with a hardcoded DSN.
3. The DLL reads the runtime-supplied PFX file from disk.
4. The file contents are base64-encoded.
5. A Sentry message is assembled with the client ID, plaintext PFX password, and encoded certificate archive.
6. `SentrySdk.CaptureMessage` sends the material to the attacker-controlled Sentry project.
7. Socket also identified a separate static Sentry capture path for raw boleto responses, which may expose transaction or payment-slip data depending on API use.

## Source-to-package mismatch
Socket reported that the public GitHub source exposed ordinary SDK behavior: storing the supplied `clientId`, `pfxPath`, and `pfxPassword`, loading the PFX archive with `X509Certificate2`, and configuring the HTTP client for mutual TLS.

The published NuGet DLL diverged from that visible source by adding Sentry initialization, credential/certificate capture, and boleto-response capture. That mismatch is the durable lesson: package consumers cannot assume a linked repository matches the built artifact unless the package is reproducibly built, signed, or otherwise verified.

The surrounding identity also showed impersonation signals:

- `Sicoob-Cooperativa` was newly created and not GitHub-verified.
- The organization had no public members and no Sicoob-controlled reverse reference confirming authorization.
- The apparent contributor `joaobcdev` was created minutes before the organization and lacked public reputation signals.
- An older public `github.com/Sicoob` account existed separately and had stronger institutional signals.

## Indicators and pivots
- NuGet package: `Sicoob.Sdk`
- Affected versions: `2.0.0`, `2.0.1`, `2.0.2`, `2.0.3`, `2.0.4`
- NuGet owner: `sicoob`
- Suspicious GitHub organization: `github[.]com/Sicoob-Cooperativa`
- Suspicious contributor account: `github[.]com/joaobcdev`
- Hardcoded Sentry DSN: `hxxps://d565e3f03d0b1a7c8935d7ff94237316@o4511335034847232[.]ingest[.]de[.]sentry[.]io/4511337546317904`
- Sensitive fields reported by Socket: client ID, PFX password, base64-encoded PFX archive contents, and raw boleto responses.

## Defender heuristics
- Search package-lock equivalents, build logs, NuGet caches, artifact mirrors, SBOMs, and dependency telemetry for `Sicoob.Sdk` versions `2.0.0` through `2.0.4`.
- Treat any production use as credential exposure: revoke and reissue PFX certificates, rotate associated client secrets, and review Sicoob API activity for anomalous transactions or boleto access.
- Audit outbound telemetry for Sentry ingest traffic around SDK initialization or integration-test runs, especially from developer workstations, CI runners, and production services that handle banking credentials.
- Prefer official vendor links from a vendor-controlled domain over package metadata alone; verify repository ownership and registry publisher identity before adopting financial-services SDKs.
- For high-trust SDKs, require signed packages, reproducible builds, provenance attestations, or independent artifact inspection before use.
- Treat "reasonable telemetry" claims skeptically when SDKs process private keys, PFX archives, access tokens, banking API credentials, or transaction records.

## Related pages
- [oob.moika.tech dependency-confusion environment stealer](oob-moika-dependency-confusion-env-stealer.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Laravel-Lang Composer tag-rewrite compromise](laravel-lang-composer-tag-rewrite-compromise.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)

## Sources
- Socket: [https://socket.dev/blog/malicious-nuget-package-impersonates-sicoob-sdk](https://socket.dev/blog/malicious-nuget-package-impersonates-sicoob-sdk)
