# Fake Corepack site infostealer and proxyware campaign

## Summary
Socket Security reported on July 24, 2026 that `corepack[.]org`, an unofficial site impersonating the Node.js Corepack project, had begun delivering Windows executables to developers. One path redirected visitors through an OpenShield-branded page and delivered an infostealer plus a persistent bandwidth-sharing component; another path used malvertising or affiliate redirects to deliver deceptive adware-style software and produced trojan detections.

The lure exploits a real ecosystem transition. Corepack stopped shipping with Node.js 25, while developers using earlier versions may know it as a bundled experimental tool. The official project says Corepack is installed from npm or used from supported Node.js releases; it does **not** distribute a Windows installer and does not control `corepack.org`.

## Tags
- ops
- operations
- Corepack
- Node.js
- developer targeting
- developer tooling
- brand impersonation
- phishing
- search poisoning
- malware delivery
- infostealer
- proxyware
- proxyjacking
- adware
- malvertising
- OpenShield
- browser data theft
- SSH keys
- PowerShell
- command execution
- Run key persistence
- Socket Security Research

## Why this matters
- The campaign targets developers at a plausible point of confusion: searching for Corepack after its removal from Node.js 25.
- A developer endpoint can expose source-control, package-registry, cloud, signing, SSH, browser-session, and CI/CD credentials even when the initial lure is not a package-registry compromise.
- Search placement and a project-matching domain can create false legitimacy without compromising the real project, npm, Node.js, or a maintainer.
- Hidden proxy enrollment creates a second risk after credential theft: third-party traffic can exit through the victim's network and complicate attribution, abuse response, and incident scoping.

## Reported delivery paths

### OpenShield infostealer and proxyware
1. A developer searching for Corepack reaches `corepack[.]org` and selects **Download Free**.
2. The site redirects to an OpenShield landing page and downloads `vpnsetup_d9gfqvs3dsic73fcvi90.exe`, presented as a free VPN rather than Corepack.
3. Execution installs OpenShield and a persistent **Apprunner** component.
4. Socket's dynamic analysis observed browser-profile and stored-SSH-key access, host and process discovery, PowerShell and command-shell execution, and Run-key persistence.
5. The software also enrolls the host in bandwidth sharing for third-party data-scraping traffic, making the system a proxy exit node without meaningful user visibility.

Socket classified this payload as an infostealer. The report does not publish a file hash, exact Run-key value, complete collection list, or confirmed victim count; defenders should not infer those details from the filename alone.

### Affiliate and adware branch
A second click path enters a malvertising or affiliate chain, displays a fake “Your File Download Is Ready” page, and delivers `OperaGXSetup.exe`. Socket characterized this branch as deceptive adware-style delivery and reported that the overall detonation was also flagged as trojan activity. The generic filename is not sufficient by itself to identify a malicious Opera installer; correlate it with source URL, signature, hash, process lineage, and subsequent behavior.

## Project and response context
The `nodejs/corepack` issue tracking the fake domain was opened on March 9, 2026. At that point the site was described as a low-quality informational imitation without executable downloads. The concern was raised with the OpenJS Foundation, but the issue was initially closed as outside the project's control. Maintainers reopened and pinned it after downloads appeared, and the issue body now warns users not to access the site because of malicious links.

The issue remained open and showed a July 22 update when threat.wiki checked the public GitHub API on July 24. A community member reported the domain to its registrar. These actions do not establish that the domain or its downstream infrastructure has been disabled.

## Public indicators
### Impersonation and delivery
- `corepack[.]org`
- `openshield[.]canatrace[.]com/download-free-can/`
- `freevpn[.]win/lps/gbox-lp/index[.]html`
- `moonlighthathel[.]org`
- `aifpleasurebeh[.]org`
- `ghabovethec[.]info`
- `ukankingwithea[.]com`
- `beadpie[.]xyz`
- `yakteam[.]xyz`
- `nostop[.]go2cloud[.]org`

### Files and software names
- `vpnsetup_d9gfqvs3dsic73fcvi90.exe`
- `OperaGXSetup.exe`
- OpenShield
- Apprunner

Treat the domains as historical and potentially mutable infrastructure. Do not browse or probe them from production systems. The two filenames are weak indicators when separated from download origin and execution telemetry.

## Detection and response guidance

### Prevent and detect
- Block or warn on `corepack.org` and the reported redirect domains at DNS, secure-web-gateway, and browser controls. Preserve passive DNS and proxy records rather than testing the infrastructure directly.
- Alert on browser downloads from the indicator set, especially when followed by execution from Downloads, Temp, or user-profile paths.
- Hunt for the reported filenames and OpenShield or Apprunner installation artifacts, then validate signer, hash, parent process, source URL, Run keys, services, scheduled tasks, and network connections.
- Correlate a browser or installer process with PowerShell or command-shell children, browser-profile or `.ssh` access, host discovery, persistence changes, and sustained proxy-like network activity.
- Baseline authorized proxy, VPN, and bandwidth-sharing software. Investigate unexpected residential-proxy egress, abuse complaints, or traffic volume that persists after the installer exits.
- Teach developers that Corepack is obtained through supported Node.js distributions or the official npm package and repository, not an `.exe` from a project-matching website.

### If execution is suspected
- Isolate the endpoint while preserving the downloaded file, browser history, zone/source metadata, process tree, memory where practical, registry hives, persistence artifacts, DNS/proxy telemetry, and outbound connection history.
- Remove proxy enrollment only after evidence collection. Identify whether the host acted as an exit node and review abuse, authentication, and network logs for traffic incorrectly attributed to the organization.
- From a known-clean system, revoke browser sessions and rotate SSH keys, source-control and package-registry tokens, cloud and CI/CD credentials, API keys, and other secrets accessible to the affected user or host.
- Review Git, package-registry, CI/CD, cloud, and SaaS audit logs for follow-on use. A password reset alone does not invalidate stolen sessions, tokens, or SSH keys.
- Rebuild the host when infostealer execution is confirmed or complete persistence and payload scope cannot be established.

## Scope and attribution caveats
This is a fake-site malware campaign, not evidence that the official Corepack repository, npm package, Node.js distribution channel, or a Corepack maintainer was compromised. Socket did not attribute the operation to a named actor or report confirmed infection counts. The site's apparently AI-generated text, spelling errors, and subject confusion describe content quality; they do not identify who operated it.

## Related pages
- [FakeGit AgentBaiting and SmartLoader campaign](fakegit-agentbaiting-smartloader-campaign.md)
- [AI chatbot and SEO poisoning GPU-cryptojacking campaign](ai-chatbot-seo-poisoning-gpu-cryptojacking.md)
- [ScreenConnect freeware / AsyncRAT SEO campaign](screenconnect-freeware-asyncrat-seo-campaign.md)
- [Phantom squatting AI-hallucinated domains](../patterns/phantom-squatting-ai-hallucinated-domains.md)

## Sources
- Socket Security Research: [https://socket.dev/blog/fake-corepack-site-distributes-infostealer-and-proxyware](https://socket.dev/blog/fake-corepack-site-distributes-infostealer-and-proxyware)
- Node.js Corepack issue: [https://github.com/nodejs/corepack/issues/803](https://github.com/nodejs/corepack/issues/803)
- Official Corepack repository and installation guidance: [https://github.com/nodejs/corepack](https://github.com/nodejs/corepack)
