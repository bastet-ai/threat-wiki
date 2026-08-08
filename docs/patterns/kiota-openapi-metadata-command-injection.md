# Kiota OpenAPI metadata command injection

## Summary

Microsoft's reviewed advisory for **CVE-2026-59865 / GHSA-hq9q-27g5-qwpj** documents a developer-tool confused-deputy path in Kiota. A malicious or compromised OpenAPI description could supply `x-ms-kiota-info.languagesInformation.<language>.dependencyInstallCommand`; affected `kiota info` versions presented that untrusted string as Kiota's recommended package-install command. The JSON form exposed the same field to the Kiota VS Code extension, where an “install dependencies” action could execute it.

The durable security lesson is broader than Kiota: API descriptions, schemas, manifests, generated metadata, and tool-output fields are untrusted data even when a trusted developer tool renders them. A tool must not turn producer-controlled “help,” package names, versions, or install instructions into executable commands without an independent policy boundary.

Microsoft removed support for description-supplied install commands in **Kiota 1.32.5**. The reviewed advisory rates the issue critical at CVSS 4.0 9.3, but exploitation still requires an attacker-controlled or tampered description and execution of the surfaced command, manually or through an IDE action. The public sources reviewed here do **not** report malicious in-the-wild exploitation or confirmed victims.

## Tags

- patterns
- developer tooling
- OpenAPI
- Kiota
- VS Code
- command injection
- code generation
- supply-chain
- confused deputy
- untrusted metadata
- CVE-2026-59865
- GHSA-hq9q-27g5-qwpj
- CWE-94
- CWE-829

## Trust-boundary failure

The affected flow crossed four different trust domains:

1. A developer or automation retrieved an OpenAPI description.
2. Kiota parsed the description's `x-ms-kiota-info` extension.
3. `kiota info` rendered the producer-controlled `dependencyInstallCommand` as a first-party recommendation, replacing Kiota's built-in package-manager template.
4. The `--json` interface carried the raw command to IDE integration, allowing a dependency-install action to become shell execution.

The command did not need to exploit an OpenAPI parser. The vulnerability was semantic: authoritative-looking output erased the distinction between tool-authored guidance and document-authored content. The advisory also notes that description-controlled dependency `name` and `version` values were rendered in the package table, reinforcing that every metadata field needs output-context validation even when only one field reaches execution.

## Affected and fixed versions

- GitHub's reviewed global advisory currently lists `Microsoft.OpenApi.Kiota` and `Microsoft.OpenApi.Kiota.Builder` versions **before 1.32.5** as affected.
- Microsoft confirmed the behavior on Kiota **1.32.4**.
- Kiota **1.32.5**, released July 3, 2026, removes description-provided `dependencyInstallCommand` support. `kiota info` now surfaces only built-in package-manager templates, and its JSON no longer exports a description-controlled command for the IDE.
- Update the Kiota VS Code extension to a build using Kiota 1.32.5 or later.

The repository-advisory API and global GHSA record briefly expose inconsistent range text for `Microsoft.OpenApi.Kiota.Builder`; defenders should use the reviewed global advisory's conservative **less-than-1.32.5** boundary rather than trying to exempt 1.32.4.

## Defender actions

- Upgrade Kiota and the Kiota VS Code extension to versions built on **1.32.5+**.
- Inventory workstations, devcontainers, CI images, code-generation services, and editor extensions for Kiota binaries and the `Microsoft.OpenApi.Kiota*` NuGet packages.
- Treat remote or repository-supplied OpenAPI descriptions as executable supply-chain inputs. Pin reviewed descriptions by digest or immutable commit where generation occurs in privileged CI.
- Do not copy shell commands from generated “hint,” “example,” or dependency output without tracing each value to a trusted template. IDE buttons are execution boundaries, not presentation-only controls.
- Require structured package-manager operations: fixed executable, validated package identifier and version fields, no shell interpolation, and an explicit allowlist of registries and package namespaces.
- Run code generation without source-control, registry-publish, cloud, signing, or production credentials. Deny unnecessary network egress and write generated output into a disposable workspace.
- Preserve the OpenAPI description, retrieval URL and digest, Kiota and extension versions, `kiota info --json` output, terminal/editor task logs, process ancestry, downloaded scripts or packages, network telemetry, and subsequent token use during incident response.

## Detection pivots

- `kiota info` or the Kiota VS Code extension followed by a shell, PowerShell, downloader, or an unexpected package-manager process.
- OpenAPI files containing `x-ms-kiota-info`, especially `dependencyInstallCommand` values with pipes, redirection, command substitution, URLs, encoded commands, shell metacharacters, or non-package-manager executables.
- New or changed OpenAPI descriptions immediately before developer-endpoint execution, CI secret access, repository writes, generated-client commits, or package publication.
- Dependency names or versions containing whitespace, shell syntax, URLs, path traversal, or names outside the organization's expected package set.
- Code-generation jobs that fetch mutable descriptions from branches, issue attachments, pull-request artifacts, paste sites, or unauthenticated endpoints.

These are behavior and provenance pivots, not proof of exploitation. Legitimate OpenAPI descriptions can contain `x-ms-kiota-info`; the high-confidence condition is untrusted metadata crossing into execution or an affected tool spawning an unexpected process.

## Related pages

- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)
- [Coding-agent CI harness handoff failures](coding-agent-ci-harness-handoff-failures.md)
- [Agentic workflow trust-boundary failures](agentic-workflow-trust-boundary-failures.md)
- [MCP stdio command execution](mcp-stdio-command-execution.md)

## Sources

- Microsoft Kiota security advisory, `GHSA-hq9q-27g5-qwpj`: [https://github.com/microsoft/kiota/security/advisories/GHSA-hq9q-27g5-qwpj](https://github.com/microsoft/kiota/security/advisories/GHSA-hq9q-27g5-qwpj)
- GitHub reviewed advisory, `CVE-2026-59865`: [https://github.com/advisories/GHSA-hq9q-27g5-qwpj](https://github.com/advisories/GHSA-hq9q-27g5-qwpj)
- Microsoft Kiota remediation pull request: [https://github.com/microsoft/kiota/pull/7883](https://github.com/microsoft/kiota/pull/7883)
- Kiota 1.32.5 release: [https://github.com/microsoft/kiota/releases/tag/v1.32.5](https://github.com/microsoft/kiota/releases/tag/v1.32.5)
