# Operation BlueDash multi-RMM workplace phishing

## Summary
Operation BlueDash is a phishing and remote-access campaign that uses fake Microsoft Teams and Zoom update flows to enroll Windows endpoints into attacker-controlled remote monitoring and management (RMM) platforms. ZeroBEC traced the campaign from a "secure document" lure through compromised websites and counterfeit Microsoft Store pages to official Level RMM, ScreenConnect, and Tactical RMM installers.

The campaign is durable because it does not depend on one custom implant or one delivery domain. Its operators rotate workplace brands, compromised sites, GitHub Pages, Netlify, Dropbox, custom domains, loaders, and RMM services while retaining a reusable fake-update workflow. Captured commands show hands-on post-enrollment reconnaissance rather than installation telemetry alone.

## Tags
- ops
- operations
- phishing
- Operation BlueDash
- Microsoft Teams
- Zoom
- fake update
- fake Microsoft Store
- RMM abuse
- Level RMM
- ScreenConnect
- Tactical RMM
- PowerShell
- JScript
- GitHub Pages abuse
- Netlify abuse
- remote access software
- Nigeria-nexus

## Why this matters
- The operators attempt to establish more than one legitimate RMM channel, so removing one agent may not evict them.
- Official vendor installers and signed administrative tooling can resemble normal IT activity unless enrollment tenant, key, parent process, and deployment path are validated.
- Public repository history exposed campaign evolution from direct ScreenConnect delivery to a multi-RMM loader and a related Zoom/JScript branch.
- Post-compromise commands queried reboot state, BitLocker, firewall profiles, and local administrators, providing behavior-based detection pivots that survive infrastructure rotation.
- ZeroBEC attributes the connected campaigns to a Nigeria-based developer group with moderate-to-high confidence. It found no evidence that the primary GitHub account had been taken over, but withheld individual identities.

## Reported Teams chain
1. A phishing email claims that a large document was shared securely through Microsoft Teams.
2. The link traverses a compromised business website and presents a counterfeit Microsoft Store page that says Teams must be updated before the document can be opened.
3. The live `teamvem[.]com` deployment downloads `supportdev.exe` from `support[.]berrydev[.]xyz`.
4. `supportdev.exe`, an Inno Setup loader, launches hidden PowerShell with execution-policy bypass.
5. PowerShell downloads the official Level RMM MSI and invokes `msiexec.exe` silently with an attacker-controlled `LEVEL_API_KEY`, automatically enrolling the host.
6. The same command attempts to download and execute a ScreenConnect client, creating a redundant access path.
7. Operators use the RMM channel to inspect host state, encryption, firewall posture, and privileged local groups.

Earlier repository revisions linked the fake update button directly to attacker-controlled ScreenConnect clients. Later revisions replaced direct delivery with SupportDev while preserving ScreenConnect as a second channel.

## Related Zoom branch
A second repository in the same development environment reused the fake workplace-update model for Zoom. Earlier payloads were delivered through Dropbox and GitHub. The later `ZoomInstallerSetup.js` branch:

- relaunches through the `runas` verb to request elevation;
- downloads the official Tactical RMM agent from GitHub;
- installs it under the Windows temporary directory;
- enrolls it with an embedded token against `api[.]investrneent[.]com`; and
- starts the agent service for persistent remote access.

This branch demonstrates that the framework can change brand, scripting language, hosting service, and RMM product without changing its objective.

## Observed post-compromise activity
ZeroBEC captured the following queries after RMM enrollment:

| Command or query | Likely purpose |
| --- | --- |
| `Microsoft.Update.SystemInfo.RebootRequired` | Determine pending-reboot state |
| `Get-BitLockerVolume -MountPoint C:` and key-protector queries | Inspect system-volume protection |
| `Get-NetFirewallProfile -PolicyStore ActiveStore` | Enumerate active firewall profiles |
| `Get-LocalGroupMember` for SID `S-1-5-32-544` | Enumerate local administrators |
| Resolve localized group name for SID `S-1-5-32-544` | Identify Administrators regardless of system language |

The sequence is consistent with an operator deciding how to preserve access and what privileges or security controls are present.

## Development and infrastructure model
ZeroBEC linked the Teams operation to the public `berry4603/Bluedashltd` repository through DNS, a GitHub Pages CNAME, source code, payloads, and commit history. The repository contained the phishing page, assets, custom-domain configuration, SupportDev, and historical delivery logic. A related repository, `berry4603/rustovni`, contained the Zoom branch.

Repository history showed:

- creation of the fake Teams/Microsoft Store page in February 2026;
- direct ScreenConnect delivery in early revisions;
- custom-domain and RMM endpoint rotation;
- migration to SupportDev for Level RMM plus ScreenConnect;
- movement of payload hosting among Dropbox, GitHub releases, GitHub Pages, and custom domains; and
- migration of the Zoom branch to a JScript Tactical RMM installer.

Treat the public repositories as historical evidence and hunt pivots, not as an assumption that every current campaign artifact remains active.

## Defender actions
1. **Inventory and allow-list RMM.** Record approved products, services, tenant identifiers, enrollment keys, publisher certificates, deployment systems, and administrator accounts. Investigate any unmatched Level, ScreenConnect, Tactical RMM, or MeshAgent installation.
2. **Isolate before removing agents.** Preserve process, PowerShell, MSI, service, browser, proxy, DNS, and RMM-console evidence. Search for every remote-access channel; removal of one agent is not sufficient.
3. **Detect enrollment behavior.** Alert on `msiexec` command lines containing `LEVEL_API_KEY` outside approved deployment, especially when preceded by hidden PowerShell or an Inno Setup binary from Downloads or a temporary path.
4. **Hunt script-driven RMM installation.** Review `powershell.exe`, `wscript.exe`, or `cscript.exe` downloading RMM agents, requesting elevation, writing to temporary directories, or starting new agent services.
5. **Correlate discovery with RMM context.** Prioritize BitLocker, firewall, reboot-state, and local-administrator discovery initiated through newly installed or unapproved remote-management software.
6. **Inspect complete redirect chains.** A reputable but compromised first-hop website does not make the final fake update page or download trustworthy.
7. **Use application control.** Block unapproved RMM installers and agents with WDAC, AppLocker, EDR controls, or equivalent policy where operationally feasible.
8. **Rotate credentials based on evidence.** If unauthorized enrollment is confirmed, scope operator actions and rotate credentials or secrets accessible from the host after preserving evidence.

## Public indicators
Historical infrastructure may be inactive or reassigned. Verify context before blocking shared services.

### Domains and hosting
- `zerrinperde[.]com[.]tr` — compromised site used in the original Teams lure.
- `anujyotindustries[.]com` — compromised site that hosted an identical lure.
- `teamvem[.]com` — live Teams-themed fake Microsoft Store deployment during the investigation.
- `bluedashlimited[.]netlify[.]app` — associated Netlify deployment.
- `support[.]berrydev[.]xyz` — GitHub Pages custom domain and SupportDev host.
- `linux[.]berrydev[.]xyz` — related infrastructure.
- `sqnchzmt4lsc[.]net` — ScreenConnect client delivery used by SupportDev.
- `sympatico15[.]screenconnect[.]com` — historical direct ScreenConnect delivery.
- `bgustavo[.]screenconnect[.]com` — connected campaign infrastructure.
- `api[.]investrneent[.]com` — Tactical RMM API server.
- `rmm[.]investrneent[.]com` — related Tactical RMM infrastructure.
- `mesh[.]investrneent[.]com` — related RMM infrastructure.

### Repositories and files
- `github[.]com/berry4603/Bluedashltd`
- `github[.]com/berry4603/rustovni`
- Commit `e6b0d5d77c62542943ed980c544d29eba7c54e4b`
- `supportdev.exe`
- `MicrosoftTeams_Update.exe`
- `ZoomInstallerSetup.js`
- `level.msi`
- `ScreenConnect.ClientSetup.exe`

### SHA-256
| SHA-256 | Reported context |
| --- | --- |
| `528dc74c8cafafbda1cd0d73fac20b8f439138891367069a9b074e8b029b0241` | `bsupport.exe` |
| `d6fc85f882af49191a83aaf5d27e06312762e3c5ee8034c5ab5b3743660556e7` | `bsupport.zip` |
| `87fc194f7644a957706faa708f24fe366adee836183e4acc3cfb703059796766` | `supportdev.exe` |
| `ecd52efea05171b5acc1d84e643c77c0db91bdf8eabd36fa44a745f789e9612c` | `ZoomInstallerSetup.js` v1 |
| `aff8cff96ef17a45d15da185d4698d453a433c117ee59d78e058191115284341` | `ZoomInstallerSetup.js` v2 |
| `4ee0d3004e986f99cb4e6ae3d2bae2cdd40e1383554f2f233e403d1826d59c24` | `ZoomInstallerSetup.js` v3 |
| `8483a435344cf3a594623cef7373c57704db7a3d81d5593a35f5a74c2d880717` | `SupportCenterTest.exe` |
| `090344137429fd43b12cc5dda8c9e6ae8e64e6e1e89c3d355444c3d11616179e` | `Workstation.exe` |
| `a4d174069cc01d1ce501131e1a05fe7a96b272f7566ce613b98930c84f69c72a` | `Level1.msi` |
| `592574c5590f39e38243dc75c212f4a2e524f5f88538a74c54445876ec437da7` | `supportcenterdev.exe` |
| `0c869c2d54bdac05b3e96ccaa5a73ef3f457d260bd618565ec5f02dda6927ceb` | `ScreenConnect.ClientSetup.msi` |
| `6e337c305d0b0f181a3f50e2956a906037e23bceacfea3ce95c051c295b044d9` | `ScreenConnect.ClientSetup.exe` |

## Analytical caveats
- The report does not establish a victim count or final post-access objective beyond interactive reconnaissance and persistent remote access.
- RMM vendor domains and installers are legitimate dual-use infrastructure; detections need tenant, enrollment, parent-process, path, and administrative context.
- Compromised websites should not be attributed to the operator as actor-owned infrastructure.
- The Nigeria nexus is ZeroBEC's moderate-to-high-confidence assessment, not an official named-group attribution.
- Enrollment secrets were redacted and should not be reconstructed or republished.

## Sources
- ZeroBEC: [Operation BlueDash: Multi-RMM Workplace Phishing](https://zerobec.com/blog/operation-bluedash-multi-rmm-workplace-phishing)
- The Hacker News: [Operation BlueDash Deploys Level RMM and ScreenConnect via Fake Teams Update](https://thehackernews.com/2026/07/operation-bluedash-deploys-level-rmm.html)
