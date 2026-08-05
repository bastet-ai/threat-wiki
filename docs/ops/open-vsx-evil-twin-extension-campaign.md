# Open VSX evil-twin extension campaign

## Summary
Between July 26 and August 1, 2026, Manifold Security identified **77 counterfeit Open VSX extensions** that copied the names, namespaces, and descriptions of unrelated legitimate extensions while replacing their functionality with a beacon. Open VSX removed the packages by August 3, but the collection infrastructure was still responding when Manifold published its analysis on August 4.

All 77 packages contacted infrastructure under `mangorbit[.]com`. Fifty-eight sent limited host telemetry; the other 19 collected developer, repository, editor, and CI identity data, including values that could disclose private repository names. Manifold did not attribute the operation or claim source-code or credential theft, so this page treats it as an unauthorized reconnaissance and namespace-impersonation campaign rather than overstating its impact.

## Tags
- ops
- operations
- supply-chain
- Open VSX
- VS Code
- IDE extension
- developer-targeting
- developer-workstations
- namespace squatting
- reconnaissance
- data exfiltration
- CI/CD
- DNS dead drop

## Why this matters
- **Extension identity does not cross registries.** A familiar extension name and namespace can be owned by a different account in Open VSX than in Microsoft's VS Code Marketplace. Name-only installation by agents, devcontainers, provisioning scripts, or users can therefore resolve to an unrelated publisher.
- **Repository configuration can become a delivery path.** The reconnaissance variant checked whether `.vscode/extensions.json` or `devcontainer.json` referenced its extension ID, letting the operator distinguish repository-induced installation from a user's direct choice.
- **“Telemetry” disclosure was materially incomplete.** The listings described collection but said CI values remained local; the code sent CI identity values that can expose private project paths.
- **Removal is not containment.** The packages included delayed retries, redundant endpoints, and DNS TXT-based destination replacement. Endpoints that already installed an extension still require inventory, evidence collection, removal, and exposure review.

## Campaign shape
- The 77 extensions were published by pseudonymous accounts at low versions, usually `0.0.1`, while reusing the name, namespace, and description of a real extension.
- Namespaces impersonated organizations and ecosystems including AMD, Artsy, LEGO Education, Hyperledger, Azure, IOTA, Salesforce OSS, `ssagov`, and `marketplace.visualstudio`.
- The extensions supplied almost no advertised feature. A status-bar checkmark and activation message provided cover while the beacon executed.
- Manifold assessed the package set as one campaign through common infrastructure and per-package tracking behavior, but did not infer operator intent or identity from the infrastructure alone.

## Collection behavior
### Lightweight group: 58 extensions
The smaller payloads, roughly 1.6–3.3 KB, sent the hostname and sometimes the workspace-folder name or editor version with a package-specific tracking identifier. Delivery varied between POST endpoints, GET query strings, and multi-endpoint failover.

### Reconnaissance group: 19 extensions
Roughly four to five seconds after activation, the larger payload assembled a profile containing:

- local hostname, operating-system username, platform, architecture, locale, and timezone;
- editor name, version, host kind, machine ID, telemetry preference, workspace folder, and full workspace path;
- Git `origin` and `upstream` host/organization, commit-email domain, current branch, and HEAD commit SHA;
- up to 60 installed extension IDs and the configured proxy hostname;
- CI marker names and selected values from GitHub Actions, GitLab CI, Azure DevOps, Buildkite, CircleCI, Codespaces, and Gitpod.

Manifold found no collection of source files, credentials, tokens, SSH material, browser data, or arbitrary environment variables in the analyzed code. The significant exposure is organizational and project reconnaissance: on CI runners and cloud development environments, fields such as `GITHUB_REPOSITORY` and `CI_PROJECT_PATH` reveal the full repository identity, including private projects.

## Infrastructure and resilience
- Primary domain: `mangorbit[.]com`, registered July 15, 2026.
- Observed collectors: `pulse.mangorbit[.]com`, `pulse2.mangorbit[.]com`, `api.mangorbit[.]com`, and randomized subdomains beneath `cb.mangorbit[.]com`.
- The infrastructure returned `ok` during Manifold's validation, indicating an active receiver rather than only a parked domain.
- Some samples carried an additional failover domain that Manifold intentionally withheld because infrastructure overlap alone was insufficient to identify its owner.
- The reconnaissance payload retried after approximately 15 minutes, 50 minutes, and three and a half hours, then every seven to eight hours for up to seven days and again after editor restart.
- If fixed endpoints failed, samples queried a DNS TXT record beneath `_beacon.<domain>` for a replacement base URL.

## Defender actions
1. **Inventory actual extension installations**, not only desired configuration. Collect extension ID, version, publisher account, source registry, installation time, and VSIX hash from developer endpoints, CI runners, devcontainers, Codespaces, and Gitpod workspaces.
2. **Compare registry ownership explicitly.** Do not assume a namespace in Open VSX belongs to the publisher using the same namespace in the VS Code Marketplace. Prefer verified publisher identity and allowlisted registry-plus-publisher-plus-extension tuples.
3. **Search repository-controlled recommendations** in `.vscode/extensions.json` and `devcontainer.json`, then determine whether automation installed any recommendation without human publisher review.
4. **Hunt network and DNS telemetry** for `mangorbit[.]com`, its listed subdomains, randomized `cb` labels, and TXT lookups for `_beacon` records. Review at least seven days after removal because of delayed retry behavior.
5. **Preserve and review editor state** before deletion where incident response matters: installed-extension metadata, extension directory contents, activation records, proxy settings, workspace history, and process/network telemetry.
6. **Scope disclosed repository identity.** For affected systems, identify which private repositories, branch names, commit SHAs, CI project identifiers, email domains, workspace paths, usernames, and extension inventories were present while the extension was active.
7. **Rotate credentials based on evidence, not assumption.** The analyzed code did not collect tokens or source, but deeper investigation is warranted if endpoint telemetry shows unexpected child processes, downloads, source reads, or destinations beyond the documented beacon.

## Detection pivots
- Open VSX extensions at an unusually low first release such as `0.0.1` that copy an established extension's name, namespace, or description but use an unrelated publisher account.
- An extension whose functional behavior consists mainly of a status-bar item or activation message plus outbound telemetry.
- Access by editor extension hosts to `.git/config`, `.git/HEAD`, `.git/refs`, `.vscode/extensions.json`, or `devcontainer.json` followed by outbound traffic.
- Collection of `GITHUB_REPOSITORY`, `CI_PROJECT_PATH`, Azure DevOps collection URI, Buildkite organization slug, CircleCI project username, Codespace name, or Gitpod workspace context by an editor extension.
- DNS TXT queries for `_beacon` labels and recurring beacon attempts over a seven-day window.
- Egress to `pulse.mangorbit[.]com`, `pulse2.mangorbit[.]com`, `api.mangorbit[.]com`, or randomized subdomains of `cb.mangorbit[.]com`.

Manifold's report contains the authoritative extension list and VSIX SHA-256 appendix; defenders should use that first-party appendix rather than a copied, potentially stale subset.

## Attribution and confidence
- **High confidence:** the 77 packages shared the documented impersonation pattern and campaign infrastructure; 19 carried the broader reconnaissance payload; Open VSX removed them by August 3.
- **High confidence:** the analyzed reconnaissance code transmitted selected CI identity values despite listing text saying those values did not leave the machine.
- **Not established:** source-code theft, credential theft, downstream compromise, victim count, operator identity, or the operator's claimed purpose.
- A reused domain or a copied namespace is a campaign pivot, not by itself evidence about a person or organization behind the activity.

## Related pages
- [Nx Console VS Code extension compromise](nx-console-vscode-extension-compromise.md)
- [JetBrains AI plugin API-key theft](jetbrains-ai-plugin-api-key-theft.md)
- [html-to-gutenberg / fetch-page-assets VS Code blockchain stealer](html-to-gutenberg-fetch-page-assets-vscode-blockchain-stealer.md)
- [FakeGit AgentBaiting and SmartLoader campaign](fakegit-agentbaiting-smartloader-campaign.md)

## Sources
- Manifold Security: [77 “evil twin” Open VSX extensions: 19 copy private repo and CI data to a new domain](https://www.manifold.security/blog/open-vsx-evil-twin-extensions)
- The Hacker News discovery pointer: [Open VSX Removes 77 Malicious Evil Twin Extensions Exfiltrating Developer Data](https://thehackernews.com/2026/08/open-vsx-removes-77-malicious-evil-twin.html)
