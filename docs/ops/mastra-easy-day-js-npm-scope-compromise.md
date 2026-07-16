# Mastra `easy-day-js` npm scope compromise

## Summary
On June 17, 2026, public reporting from StepSecurity, Socket, Snyk, SafeDep, and Microsoft described a high-blast-radius npm supply-chain incident affecting the Mastra AI framework ecosystem. A stale or compromised npm maintainer account republished more than 140 packages in the `@mastra/*` scope and injected a single new dependency, `easy-day-js`, a `dayjs` lookalike whose install hook delivered a cross-platform Node.js implant. Microsoft attributes the activity to `Sapphire Sleet`, its name for a North Korea-linked cluster also associated with earlier cryptocurrency and developer-targeting npm operations.

The malicious dependency executed during `npm install`, before application code was imported. Treat developer workstations, CI runners, and build hosts that installed affected Mastra packages on or after June 17, 2026 as potentially compromised.

## Tags
- ops
- operations
- supply-chain
- npm
- JavaScript
- TypeScript
- AI framework
- maintainer compromise
- stale access
- package registry
- developer-targeting
- CI/CD
- credential-theft
- cryptocurrency
- wallet theft
- RAT
- postinstall
- npm lifecycle hook
- persistence

## Why this matters
- Mastra is an AI-agent / workflow framework that is likely to be installed in environments containing LLM API keys, cloud credentials, GitHub tokens, vector-database credentials, and deployment secrets.
- The poisoned `@mastra/*` packages reportedly kept the legitimate package code intact; the functional change was an added transitive dependency, making source-repository review alone insufficient.
- The compromise was rooted in stale package-scope access, not a novel npm zero-day: inactive maintainer permissions can remain enough to publish to an entire package namespace.
- The `easy-day-js` package used a clean-to-malicious progression: a benign-looking `1.11.21` release, then a weaponized `1.11.22` that still satisfied `^1.11.21` dependency ranges.
- Install-time execution means impact begins when dependency resolution and lifecycle scripts run, even if the package is never imported or used.

## Reported chain
1. A former Mastra contributor account, `ehindero`, retained npm publish access to the Mastra scope. Snyk reports signs of account takeover rather than insider action, including an email change to `ehindero2016@tutamail[.]com`; SafeDep observed the same `2016` email pattern on the `sergey2016` account that published `easy-day-js`.
2. The attacker published `easy-day-js`, a typosquat / lookalike of `dayjs`. Snyk, Socket, and SafeDep report `easy-day-js@1.11.21` was initially clean, while `easy-day-js@1.11.22` added a `postinstall` hook.
3. The attacker republished Mastra packages with a new dependency on `easy-day-js` using a compatible range such as `^1.11.21`, causing normal installs to resolve to the malicious `1.11.22` release.
4. Socket reports the malicious Mastra package code was otherwise byte-for-byte identical to prior legitimate builds aside from version and manifest normalization changes.
5. SafeDep reports the malicious Mastra publishes dropped npm provenance attestations: legitimate Mastra releases were CI-published with provenance, while the attacker-published versions came from a personal token, added `easy-day-js`, and lacked attestations.
6. The `postinstall` hook ran `setup.cjs`, disabled TLS certificate validation, downloaded a second-stage payload, launched it as a detached Node.js process, and deleted the loader.
7. The second stage installed persistence on Windows, macOS, and Linux, then beacons for tasking and can execute follow-on Node or shell commands.

## Reported scope and status
- StepSecurity reported `140+` affected packages with combined weekly downloads exceeding 1.1 million.
- Socket reported a single npm account mass-published more than 140 malicious packages in the `@mastra/*` namespace during a short June 17 window; its enumeration counted 141 affected `@mastra/*` packages and called out `@mastra/core` at more than 918k weekly downloads.
- Snyk reported 143 packages and counting, including `@mastra/core`, and later added `@mastra/node-speaker@0.1.1` to its compromised-package set.
- SafeDep counted 143 affected packages and placed the scope-wide Mastra republish burst between 01:12 and 02:36 UTC on June 17, 2026.
- Microsoft Threat Intelligence reported that it observed `easy-day-js@1.11.22` at 01:07 UTC and `mastra@1.13.1` at 01:28 UTC on June 17; it also noted that all packages published by `ehindero` in the observed burst carried the injected dependency, while packages last published by GitHub Actions CI/CD or other legitimate maintainers were not affected. Microsoft assesses the compromise as `Sapphire Sleet` activity.
- Notable versions from Snyk include `@mastra/core@1.42.1`, `mastra@1.13.1`, and `create-mastra@1.13.1`.
- Snyk advisory `SNYK-JS-EASYDAYJS-17353313` covers malicious embedded code in `easy-day-js`.
- Mastra's remediation PR says the source tree was clean of `easy-day-js` and forward-rolled clean versions for the publishable packages; it also notes that unpublishing/deprecation, credential rotation, and unauthorized-owner removal were handled separately.

## Malware behavior
### Loader: `setup.cjs`
Socket's technical analysis describes the stage-one loader as obfuscated JavaScript with the following behavior:

- Sets `NODE_TLS_REJECT_UNAUTHORIZED` to disable TLS validation.
- Downloads stage two from `https://23[.]254[.]164[.]92:8000/update/49890878`.
- Writes marker files under the OS temp directory, including `.pkg_history` and `.pkg_logs`.
- Microsoft described the postinstall dropper as a 4,572-byte obfuscated `setup.cjs`; the `.pkg_logs` marker stores `easy-day-js` XOR-encoded with `0x80`.
- Saves the second stage under a random temp filename and starts it as a detached Node.js process.
- Passes `23[.]254[.]164[.]123:443` as the second-stage exfiltration / C2 target.
- Removes the loader file after execution to reduce forensic evidence.
- SafeDep reports the payload endpoint was User-Agent gated: browser or ordinary curl requests returned 404, while Node's default User-Agent retrieved the 41 KB second-stage script.

### Implant: `protocal.cjs`
Socket describes the recovered stage-two payload as a roughly 41 KB cross-platform Node.js tasking client rather than only a one-shot stealer.

Reported persistence paths:

- **Windows**: `HKCU\...\CurrentVersion\Run` value `NvmProtocal`; drop directory `C:\ProgramData\NodePackages\` containing `protocal.cjs` and `config.json`.
- **macOS**: LaunchAgent `~/Library/LaunchAgents/com.nvm.protocal.plist`; payload path `~/Library/NodePackages/protocal.cjs`.
- **Linux**: systemd user unit `~/.config/systemd/user/nvmconf.service`; payload `~/.config/systemd/nvmconf/protocal.cjs`; config `~/.config/NodePackages/config.json`.

Reported collection and tasking:

- Start / check polling loop with built-in Node and shell task runners.
- Host reconnaissance including hostname, architecture, platform, user ID, installed applications, and running processes.
- Browser history collection from Chrome, Edge, and Brave profiles.
- Cryptocurrency wallet extension inventory across 166 hardcoded browser-extension IDs, including wallets such as MetaMask, Phantom, Coinbase Wallet, Binance Wallet, and TronLink. Socket's recovered sample inventories wallet-extension presence and profile paths; it warns that follow-on tasking could still steal secrets or wallet material.
- Custom ICAP-style HTTPS POST tasking / exfiltration using the `/49890878` bot path.
- Microsoft reported that collection traffic uses custom ICAP-style headers such as `reqmod`, `PrimaryUrl`, and `SecondaryUrl`, resolves hostnames through `node:dns`, and carries a spoofed legacy IE8 User-Agent string.
- Microsoft also reported a Windows-specific branch where the first C2 response downloads a .NET DLL, loads it directly in memory via reflection, invokes `Extension.SubRoutine.Run2`, and injects follow-on execution into `cmd.exe`; treat Windows hits as potential fileless process-injection incidents even when only the JavaScript dropper is present on disk.
- SafeDep reports the first beacon carries base64-encoded JSON containing username, hostname, OS, architecture, Node version, installed applications, wallet-extension inventory, browser history, and process list. It also observed a 10-minute default sleep interval, task tag `tpcsr`, and result tag `r0`.
- SafeDep reports the C2 was fronted by a default wolfSSL test certificate with `CN=www.wolfssl.com` that had expired in January 2018.

### SafeDep follow-up (2026-06-18)
SafeDep's June 17 post adds additional provenance, infrastructure, and payload pivots to the earlier StepSecurity, Socket, and Snyk reporting.

### Microsoft follow-up (2026-06-18)
Microsoft's June 17 post adds publish-timeline, dropper, Windows injection, exfiltration-protocol, and hash pivots to the earlier registry and malware reporting.

### Infrastructure and hashes
- Dropper endpoint: `23[.]254[.]164[.]92:8000/update/49890878`.
- Second-stage C2: `23[.]254[.]164[.]123:443` / `https://23[.]254[.]164[.]123/49890878`.
- SafeDep associated the hosts with Hostwinds names `hwsrv-1327786` and `hwsrv-1327785.hostwindsdns[.]com` in `23.254.164.0/24`.
- SafeDep reported SHA-256 `221c45a790dec2a296af57969e1165a16f8f49733aeab64c0bbd768d9943badf` for the stage-two payload.
- Microsoft published additional file/package hashes: `AE70DD4F6BC0D1C8C2848E4E6B51934626C4818DCB5AF99D080DDBD7DC337185` for `setup.cjs`, `4A8860240E4231C3A74C81949BE655A28E096A7D72F38FBE84E5B37636B98417` for `easy-day-js-1.11.22.tgz`, and `B73DE25C053C3225A077738A1FCBD9CA6966D7B3CD6F5494A30F0AA0EAE55C7E` for the clean bait `easy-day-js-1.11.21.tgz`.
- SafeDep noted close tradecraft overlap with the earlier Axios / `plain-crypto-js` campaign Microsoft attributed to Sapphire Sleet / BlueNoroff; Microsoft later explicitly attributed the Mastra compromise to Sapphire Sleet. Keep that attribution scoped to Microsoft's assessment unless additional primary sources independently corroborate it.

## Defender heuristics
### Exposure triage
- Search dependency manifests, lockfiles, SBOMs, package-manager caches, private registries, CI logs, build artifacts, and container layers for `@mastra/*` packages installed or updated on or after June 17, 2026.
- Explicitly hunt for `easy-day-js`, especially `easy-day-js@1.11.22`, and for Mastra versions listed in StepSecurity, Socket, Snyk, and Mastra's own remediation notes.
- Treat any `@mastra/*` package publish that lacks expected npm provenance attestations as suspicious when adjacent legitimate releases were CI-published with provenance.
- Treat any successful lifecycle-script execution on a developer machine, CI runner, or build host as host compromise, not just a bad dependency resolution.
- Prefer reinstalling from known-clean Mastra versions after deleting `node_modules`, clearing caches, and confirming that private mirrors did not preserve poisoned tarballs.

### Endpoint and CI hunting
- Review npm install logs for `postinstall` execution from `easy-day-js` and for unexpected `setup.cjs` execution.
- Hunt outbound network activity to `23[.]254[.]164[.]92:8000`, `23[.]254[.]164[.]123:443`, and path `/49890878` around dependency-install windows.
- Include Hostwinds `23.254.164.0/24`, `hwsrv-1327786`, `hwsrv-1327785.hostwindsdns[.]com`, Node default User-Agent retrievals from raw IP HTTPS endpoints, and wolfSSL test-certificate observations as supporting pivots rather than standalone proof.
- Inspect temp directories for `.pkg_history`, `.pkg_logs`, random `.js` payloads, and browser-history copy directories such as `browser-hist-*`.
- Decode `.pkg_logs` with XOR `0x80` when triaging suspected hosts; Microsoft reports the marker decodes to `easy-day-js`.
- Inspect Windows hosts for `NvmProtocal` Run-key values and `C:\ProgramData\NodePackages\` artifacts.
- On Windows, also hunt for `node.exe` or hidden PowerShell launching unexpected `cmd.exe` children, in-memory .NET loading, and outbound HTTPS to the Mastra C2 after Node lifecycle-script execution.
- Inspect macOS hosts for `~/Library/LaunchAgents/com.nvm.protocal.plist` and `~/Library/NodePackages/protocal.cjs`.
- Inspect Linux hosts for `~/.config/systemd/user/nvmconf.service`, `~/.config/systemd/nvmconf/protocal.cjs`, and `~/.config/NodePackages/config.json`.
- Review GitHub, npm, cloud, Kubernetes, SSH, CI/CD, package-registry, and LLM-provider credential use from affected hosts after the install window.

### Maintainer and registry controls
- Remove inactive maintainers and stale package-scope owners as part of routine offboarding; npm publish access should not survive contributor inactivity by default.
- Require phishing-resistant MFA and least-privilege scoped tokens for package publishers.
- Prefer short-lived, workflow-bound trusted publishing over long-lived human or automation tokens, but pair it with protected environments and branch rules.
- Monitor for sudden scope-wide patch releases from a single dormant human account, especially when the published tarballs diverge from repository release workflows.
- Diff registry tarballs, not only source repositories: this incident's malicious dependency was reportedly injected at publish time and was absent from the clean source tree.
- Enforce provenance or signature policy where possible; SafeDep notes that an install policy requiring expected attestations would have rejected the attacker-published Mastra packages that dropped provenance.

## Related pages
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [Operation DangerousPassword axios npm compromise](operation-dangerouspassword-axios-npm-compromise.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)

## Sources
- [StepSecurity](https://www.stepsecurity.io/blog/mastra-npm-packages-compromised-using-easy-day-js)
- [Socket](https://socket.dev/blog/mastra-npm-packages-compromised)
- [Snyk](https://snyk.io/blog/a-forgotten-contributor-account-compromised-the-entire-mastra-npm-package-scope/)
- [SafeDep](https://safedep.io/mastra-npm-scope-takeover-supply-chain-attack/)
- [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/17/postinstall-payload-inside-mastra-npm-supply-chain-compromise/)
- [Mastra GitHub issue](https://github.com/mastra-ai/mastra/issues/18045)
- [Mastra remediation PR](https://github.com/mastra-ai/mastra/pull/18056)
