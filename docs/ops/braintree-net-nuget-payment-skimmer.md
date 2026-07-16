# Braintree.Net NuGet payment skimmer

## Summary
Socket's July 9, 2026 analysis describes `Braintree.Net` as a malicious NuGet typosquat that impersonated PayPal Braintree's legitimate .NET SDK. The package copied the official SDK's API surface closely enough for payment integrations to keep working, while adding a multi-stage .NET implant that intercepted payment-card data, stole Braintree merchant credentials, and harvested host environment secrets.

The official NuGet package is `Braintree` in the 5.x line and is maintained under the `braintreepayments` profile. The malicious package used the lookalike name `Braintree.Net`, claimed the author `Braintree`, pointed metadata at the legitimate `braintree/braintree_dotnet` GitHub repository, and routed stolen data to attacker-controlled infrastructure at `api.348672-shakepay[.]com`.

## Tags
- ops
- supply chain
- NuGet
- .NET
- payment skimmer
- credit card theft
- credential theft
- merchant credential theft
- environment variable theft
- typosquatting
- package registry
- Braintree
- PayPal
- Socket Security

## Why this matters
- This is a payment-path package compromise: production applications using the typosquat could leak card numbers, CVVs, expiration data, merchant IDs, public keys, private keys, and access tokens while legitimate Braintree API calls still succeeded.
- The malicious package did not rely only on install-time execution. It activated at assembly load, when gateway private keys were configured, and when payment-card creation flows were called.
- The package's inflated download count created false reputation. Socket reported roughly 14 million displayed downloads, with about 11 million coming from 120 empty placeholder versions published on a single day.
- The campaign abused both a direct typosquat (`Braintree.Net`) and a companion package (`DependencyInjector.Core`) that acted as a token / environment harvester and was pulled transitively by other packages.

## Affected packages
Socket identifies the following NuGet package versions as containing confirmed malicious code:

- `pkg:nuget/braintree.net@3.35.8`
- `pkg:nuget/braintree.net@3.35.9`
- `pkg:nuget/braintree.net@3.36.0`
- `pkg:nuget/braintree.net@3.36.1`
- `pkg:nuget/dependencyinjector.core@1.0.0`
- `pkg:nuget/dependencyinjector.core@1.3.0`
- `pkg:nuget/dependencyinjector.core@1.4.0`
- `pkg:nuget/dependencyinjector.core@1.4.1`

Socket also reported the following versions as transitively affected because they pulled in malicious `DependencyInjector.Core`:

- `pkg:nuget/sipnet@12.8.4`
- `pkg:nuget/sipnet@12.8.5`
- `pkg:nuget/sipnet@12.8.6`
- `pkg:nuget/sipnet@12.8.7`
- `pkg:nuget/sipnet.openai.realtime@12.8.3` through `sipnet`

## Technical details
### Camouflage
`Braintree.Net` shipped real-looking `Braintree.dll` assemblies for `net452`, `netstandard2.0`, `net8.0`, `net9.0`, and `net10.0`. Its public API included familiar Braintree gateway, credit-card, transaction, webhook, and GraphQL client types. Socket notes that the bundled README was copied from official Braintree documentation and even instructed users to install the real package name, `Braintree`, rather than `Braintree.Net`.

Socket's comparison with official `Braintree` 5.36.0 found that the legitimate assembly did not contain `CardOperationLogger`, `DependencyInjectorLoader`, or a reference to `DependencyInjector.Core`; the typosquat added all three.

### Execution flow
When a .NET application referenced the typosquat and loaded the assembly, the implant exposed three independent exfiltration paths:

1. **Assembly-load / module-initializer path:** `Braintree.DependencyInjectorLoader.Load()` and `DependencyInjector.Core.AutoInitializer` invoked `CodebaseAnalyzer.AnalyzeAndPrint()` to POST environment, configuration, and cloud metadata to `/api/analytics/report`.
2. **Merchant-credential path:** the `BraintreeGateway.PrivateKey` setter, gated on production environment configuration, invoked `GatewayInput.AddAccountAsync()` to POST `merchantId`, `publicKey`, and `privateKey` to `/api/account`.
3. **Payment-card path:** `CardOperationLogger.LogCreditCardCreate()` hooked `gateway.CreditCard.Create(request)` before the legitimate Braintree request and POSTed card data, including card number, CVV, and expiration details, to `/api/card`.

Socket reports that each exfiltration path swallowed exceptions with empty `catch` blocks, allowing the host application to continue if network, TLS, or payload errors occurred.

### Infrastructure and gating
- C2 / exfiltration host: `api.348672-shakepay[.]com`
- Reported paths: `/api/analytics/report`, `/api/account`, `/api/card`
- Socket notes production-only gating for the merchant-key and card-interception paths, reducing obvious test-environment noise while targeting live payment integrations.
- Socket reported an `X-Api-Key` header pattern beginning `2523-5...2386` in network-hunt guidance.

## Defender heuristics
- Remove `Braintree.Net` from all projects, central package-management files, lockfiles, package caches, build caches, CI runners, and internal NuGet mirrors. Replace it with the official `Braintree` package only after validating source and publisher.
- Search dependency graphs for `Braintree.Net`, `DependencyInjector.Core`, `SipNet`, and `SipNet.OpenAI.Realtime`; do not scope only direct payment-service dependencies.
- Rotate Braintree `merchantId`, `publicKey`, `privateKey`, access tokens, and any surrounding payment-service credentials for any environment that ever loaded the affected packages.
- Treat production card data as potentially disclosed if card numbers or CVVs passed through the poisoned SDK. Engage PCI incident-response and notification workflows where applicable.
- Hunt proxy, firewall, EDR, and application logs for outbound POSTs to `api.348672-shakepay[.]com`, especially to `/api/analytics/report`, `/api/account`, or `/api/card`.
- Flag NuGet packages that combine official-project metadata with mismatched publisher identity, unusual version-line divergence from the official SDK, inflated download counts from placeholder releases, and realistic API-surface cloning.

## Related pages
- [Paysafe / Skrill / Neteller npm and PyPI typosquat stealer campaign](paysafe-skrill-neteller-npm-pypi-typosquats.md)
- [Sicoob.Sdk NuGet banking certificate stealer](sicoob-sdk-nuget-banking-certificate-stealer.md)
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)
- [Crypto supply-chain path to transaction authority](../patterns/crypto-supply-chain-transaction-authority.md)

## Sources
- [Socket](https://socket.dev/blog/braintree-nuget-typosquat-skims-credit-cards)
