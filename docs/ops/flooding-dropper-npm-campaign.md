# Flooding Dropper npm campaign

## Summary
On August 5, 2026, Sonatype Research Labs disclosed an active npm malware campaign it calls **Flooding Dropper**. At publication time, Sonatype associated **846 software components** with the campaign under `sonatype-2026-005660`. The operation spreads cross-platform JavaScript loaders across many low-volume, apparently automated publisher accounts rather than concentrating releases under one account.

The first stage runs when a package is installed or imported, selects a Windows, Linux, or macOS binary, and tries multiple hardcoded HTTPS hosts in randomized order. If those downloads fail, it can retrieve and reconstruct the payload through DNS TXT records. It then launches the binary as a detached process. Sonatype's Windows analysis found a further downloader that impairs ETW and AMSI, performs anti-analysis checks, establishes user-level persistence, and reflectively executes an encrypted follow-on payload.

## Tags
- ops
- operations
- Flooding Dropper
- sonatype-2026-005660
- Sonatype
- npm
- JavaScript
- malicious packages
- supply-chain
- package registry
- install-time execution
- cross-platform
- loader
- DNS
- DNS C2
- persistence
- detached process
- Windows
- Linux
- macOS
- ETW patching
- AMSI bypass
- scheduled task persistence
- registry persistence
- reflective loading
- anti-analysis

## Why this matters
- Sonatype counted 846 components at publication, but the campaign distributes them across many disposable accounts that publish only a few packages each. Removing one publisher does not contain the cluster.
- The package name is not a durable control. Early names often combine terms such as `bigops` and `bnpl`, while Sonatype had already seen the naming convention expand beyond those terms.
- Small source-level changes alter variable and function names while preserving behavior, reducing the value of exact JavaScript signatures.
- The loader has independent HTTPS and DNS TXT delivery paths. Blocking one observed download host may not stop payload retrieval.
- Detached execution breaks the assumption that terminating the npm or Node.js parent process ends the incident.
- Successful execution moves the incident beyond a malicious dependency: the Windows chain adds defense impairment, persistence, an encrypted payload, and reflective in-memory execution.

## Reported publication pattern
Sonatype says the actor appears to automate at least part of npm account and package creation:

- publisher account names appear randomly generated;
- each account publishes only a small number of packages;
- many early package names interpolate `bigops` or `bnpl` with other words;
- examples in the public report include `bigops-backend`, `bigops-api`, and `dolyame-boxy-desktop-bnpl-card-gallery`;
- many related releases use versions beginning with `35.x.y`;
- syntactically modified first stages retain the same execution behavior.

These are useful discovery pivots, not sufficient classification criteria. Sonatype explicitly warns that names and version patterns can change more easily than loader behavior.

## Execution chain
Sonatype describes the first-stage JavaScript as follows:

1. It checks environment variables and local state markers to decide whether to execute.
2. It identifies the operating system and processor architecture.
3. It chooses a compatible Windows, Linux, or macOS payload.
4. It randomizes attempts across multiple hardcoded remote hosts.
5. If direct HTTPS retrieval fails, it queries DNS TXT records, reassembles their content, and decodes the payload.
6. It writes the binary under a temporary directory and marks it executable on Unix-like systems.
7. It starts the binary as a detached background process with standard output and error suppressed.

The public report does not enumerate the complete environment checks, state-marker names, download hosts, DNS names, temporary paths, package list, or payload hashes. Do not infer indicators that Sonatype did not publish.

## Windows second stage
Sonatype's initial Windows analysis found the downloaded binary acting as another loader. Reported behavior includes:

- patching Event Tracing for Windows and Antimalware Scan Interface functions to interfere with monitoring and scanning;
- checking for debuggers, virtual machines, sandboxes, and security products;
- copying itself to a persistent location under the current user's `AppData` directory;
- establishing persistence through both a Registry Run key and a scheduled task;
- downloading an encrypted follow-on payload from a `/pkg/update_win.exe` path;
- decrypting and reflectively executing that payload in memory.

The disclosure does not identify the final payload's family, commands, objective, infrastructure, or operator. It also does not establish that the Windows persistence details apply unchanged to the Linux and macOS payloads.

## Defender priorities
1. **Inventory exact exposure.** Check lockfiles, SBOMs, package manifests, internal registries, proxy logs, package caches, container layers, developer workstations, CI/CD runners, build agents, test systems, and production-adjacent hosts against the current `sonatype-2026-005660` component set.
2. **Treat execution as compromise.** Package download or cache presence establishes exposure; installation or import can trigger the loader. Isolate hosts with evidence of execution and preserve process, endpoint, DNS, proxy, registry, scheduled-task, filesystem, and package-manager telemetry.
3. **Hunt behavior, not only names.** Correlate npm or Node.js activity with OS and architecture discovery, randomized HTTPS download attempts, unusual DNS TXT retrieval, payload reconstruction, executable writes under temporary directories, permission changes, and detached children with suppressed output.
4. **Scope the Windows chain.** Review ETW or AMSI modification alerts, user `AppData` executable creation, new Run-key values, new scheduled tasks, access to `/pkg/update_win.exe`, and memory-only execution descendants of the downloaded loader.
5. **Remove persistence before credential rotation.** Sonatype recommends considering affected hosts compromised, cleaning or rebuilding them, and then rotating npm, GitHub, cloud, CI/CD, and other developer credentials that were accessible during execution.
6. **Purge retained artifacts.** Remove malicious versions from private mirrors, caches, lockfiles, images, and build layers. Rebuild from verified dependencies in a known-clean environment.
7. **Constrain future installs.** Disable unneeded dependency lifecycle scripts, require explicit script approval where supported, sandbox package installation, restrict developer and build-runner egress, and alert on package-manager descendants that detach or execute downloaded native binaries.

## Detection and attribution limits
- Sonatype's **846-component** figure is a live publication-time snapshot, not a final package or version count.
- The public article gives three example package names but not the full public appendix. Query the current `sonatype-2026-005660` record or trusted package-intelligence data rather than building a deny list from examples.
- `bigops`, `bnpl`, and `35.x.y` are correlation clues, not proof that a package is malicious; their absence is not exculpatory.
- The report does not publish the direct-download hosts, DNS TXT domains, hashes, final payload, victims, actor, or successful-install count.
- This is a separate campaign from the concurrently reported ChainDrop / Mini Shai-Hulud worm. Shared use of npm and developer-host execution does not establish shared code, infrastructure, propagation, or operator identity.

## Open questions
- Complete package, version, publisher-account, hash, host, DNS, path, Run-key, and scheduled-task indicators.
- Earliest publication and successful-execution dates, download counts, victim scope, and registry containment status.
- Linux and macOS payload behavior, persistence, and follow-on payloads.
- Final Windows payload capability and operator objective.
- Account-creation automation, payment or identity reuse, and whether npm platform controls can suppress replacement publishers at campaign scale.
- Independent validation and any relationship to known malware families or operators.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [npm publish-time malware scanning and dual-use declarations](../patterns/npm-publish-time-malware-scanning.md)
- [Dependabot cross-ecosystem malware advisory alerts](../patterns/dependabot-cross-ecosystem-malware-alerts.md)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md)

## Sources
- Sonatype Research Labs: [“Flooding Dropper” Campaign Hits npm With Nearly 850 Malicious Packages](https://www.sonatype.com/blog/flooding-dropper-hits-npm-with-850-malicious-packages)
- Sonatype advisory: [`sonatype-2026-005660`](https://guide.sonatype.com/component/sonatype-2026-005660)
