# GitLab Oj notebook-diff authenticated RCE chain

## Summary
On 2026-07-24, depthfirst published technical details and proof-of-concept code for a remotely reachable memory-corruption chain in self-managed GitLab. A normal authenticated project member who can commit changes and view commit diffs can submit crafted Jupyter notebook (`.ipynb`) revisions that reach the native-C **Oj** JSON parser through GitLab's in-tree `ipynbdiff` component. Chaining a heap-pointer disclosure with an out-of-bounds write can execute commands as the GitLab `git` operating-system account.

GitLab fixed the reachable chain on 2026-06-10 by updating to Oj 3.17.3 in GitLab **18.10.8**, **18.11.5**, and **19.0.2**. Public exploit code materially changes defender urgency even though depthfirst said it was not aware of in-the-wild exploitation at disclosure. No CVE had been assigned to the GitLab chain in the public material reviewed for this page.

## Tags
- ops
- operations
- GitLab
- Oj
- Jupyter Notebook
- ipynbdiff
- authenticated remote code execution
- memory corruption
- heap pointer disclosure
- out-of-bounds write
- native extension
- source control
- developer infrastructure
- public proof of concept
- vulnerability research

## Why this matters
- Exploitation does not require administrator, CI runner, or access to another user's project; ordinary authenticated commit and diff-view permissions are sufficient on an affected instance.
- Code runs inside a long-lived Puma worker as `git`, placing source repositories, Rails secrets, service credentials, CI/CD data, and internal services reachable from GitLab at risk.
- The vulnerable GitLab path existed from 15.2 onward. Unsupported 15.2 through 18.9 releases did not receive dedicated backports and must move to a supported fixed release.
- The Oj update appeared among a broader June 10 patch release. Organizations that prioritized only entries in GitLab's security-fix table may not have recognized this separate notebook-diff chain before public disclosure.
- Helm and Operator version numbers can obscure the application version that matters; defenders must inspect the GitLab version in the Webservice image running Puma.

## Affected and fixed versions
| Component | Affected | First fixed release |
|---|---|---|
| GitLab CE/EE | 15.2.0 through 18.10.7 | 18.10.8 |
| GitLab CE/EE | 18.11.0 through 18.11.4 | 18.11.5 |
| GitLab CE/EE | 19.0.0 through 19.0.1 | 19.0.2 |
| Oj gem | 3.13.0 through 3.17.1 | 3.17.3 |

The application ranges apply across GitLab tiers and deployment forms, including Linux packages, Docker, source installs, Geo, and cloud-native deployments. GitLab.com was patched by the June 10 release; GitLab's release notice says Dedicated customers do not need to act. Ruby itself is not affected: the memory-safety flaws are in Oj's native extension, and the demonstrated GitLab exploit depends on the reachable notebook-diff integration.

## Technical characteristics
1. A project member commits notebook revisions and requests the rendered commit diff.
2. GitLab's `ipynbdiff` path passes repository-controlled notebook JSON to `Oj::Parser.usual.parse` inside a Puma worker.
3. One Oj flaw can truncate an overlong object-key length and expose a live heap pointer in rendered output.
4. A second flaw writes beyond a fixed nesting stack and can corrupt parser callback state.
5. The chain uses the disclosure to locate process libraries and redirects execution through the corrupted callback, resulting in command execution as `git`.

The published proof of concept demonstrates the chain against a specific GitLab 18.11.3 x86-64 reference image. Library offsets, allocator state, and worker lifetime affect portability, so it is not a universal one-command exploit. That constraint reduces opportunistic reliability but does not make exposed affected instances safe: the underlying path is remotely reachable and the full research needed to adapt it is now public.

## Defender actions
1. **Upgrade immediately.** Move self-managed GitLab to a current supported release. The first fixed points were 18.10.8, 18.11.5, and 19.0.2; do not treat those now-historical minimums as a reason to stop normal patch progression.
2. **Verify the running application, not only orchestration metadata.** For Helm and Operator deployments, inspect the Webservice/Puma image and confirm its embedded GitLab and Oj versions.
3. **Treat prior untrusted project access as meaningful exposure.** Review accounts able to create projects or push commits during the vulnerable period, including guests promoted through automation, compromised developer identities, and externally federated users.
4. **Hunt notebook-diff activity.** Preserve and review GitLab Rails, Workhorse, reverse-proxy, audit, and application logs for unusual `.ipynb` commit sequences and repeated requests to commit-diff streaming paths, especially activity followed by Puma crashes, restarts, or anomalous latency.
5. **Hunt post-exploitation from the GitLab security context.** Investigate unexpected child processes, shell or network utilities, outbound connections, repository access, secret reads, CI/CD configuration changes, new tokens or keys, and access to internal services attributable to the `git` account or Puma workers.
6. **Scope secrets as compromised if evidence supports execution.** Rotate Rails and application secrets according to GitLab guidance, then invalidate exposed personal, project, group, deploy, OAuth, runner, registry, cloud, and service credentials. Review source and artifact access before restoring trust.
7. **Preserve volatile evidence before restarting when compromise is suspected.** Capture process trees, memory where feasible, open connections, container state, logs, and affected notebook objects. Coordinate service isolation and evidence collection rather than destroying the only record through an immediate rebuild.
8. **Inventory Oj separately.** Other Ruby applications may bundle affected Oj versions, but do not assume the GitLab notebook-diff exploit transfers directly. Upgrade Oj to 3.17.3 or later where managed directly and assess each application's parser reachability.

## Exploitation-status caveat
The existence of working public code should be recorded separately from exploitation in the wild. Depthfirst stated that it was not aware of active exploitation and that GitLab independently reproduced the RCE during coordinated disclosure. This page therefore treats the issue as **public-PoC, high-impact exposure**, not as a confirmed campaign or KEV-listed vulnerability.

## Related pages
- [GitHub Actions cPanel exploitation campaign](github-actions-cpanel-cve-2026-41940-exploitation-campaign.md)
- [NGINX CVE-2026-42533 capture-clobbering RCE risk](nginx-cve-2026-42533-capture-clobbering-rce.md)
- [GitHub API enumeration and access-token abuse](../patterns/github-api-enumeration-token-abuse.md)

## Sources
- depthfirst overview and remediation: [GitLab Oj Spill](https://depthfirst.com/gitlab-rce-oj-spill)
- depthfirst technical analysis: [Going depthfirst: Achieving GitLab RCE via Two Ruby Memory Corruption Vulnerabilities](https://depthfirst.com/research/going-depthfirst-achieving-gitlab-rce-via-two-ruby-memory-corruption-vulnerabilities)
- GitLab June 10 patch release: [GitLab 19.0.2, 18.11.5, and 18.10.8](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-2-released/)
- Public proof-of-concept repository: [wupco/gitlab-rce-demo](https://github.com/wupco/gitlab-rce-demo)
- The Hacker News summary and release-note visibility context: [Researcher Publishes GitLab RCE PoC](https://thehackernews.com/2026/07/researcher-publishes-gitlab-rce-poc.html)
