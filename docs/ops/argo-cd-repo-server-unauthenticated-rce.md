# Argo CD repo-server unauthenticated RCE

## Summary
Synacktiv published research on July 1, 2026 describing an unauthenticated arbitrary-code-execution path in **Argo CD**'s `repo-server` component. The issue has no CVE and no public patch at publication time; Synacktiv says it disclosed the vulnerability to Argo CD maintainers in January 2025 and published after repeated follow-ups because the exposure remained unpatched.

The exploit path matters because `repo-server` prepares Kubernetes manifests from Git repositories inside a privileged GitOps control plane. If an attacker can reach the `repo-server` gRPC port and Argo CD's Redis database port, they can manipulate repository/cache state and drive deployment of attacker-controlled manifests, potentially turning one reachable internal service into cluster compromise.

## Tags
- ops
- operations
- Argo CD
- ArgoCD
- repo-server
- Kubernetes
- GitOps
- unauthenticated RCE
- command execution
- cluster compromise
- gRPC
- Redis
- Helm
- network policies
- CI/CD
- Synacktiv
- CodeQL
- unpatched vulnerability

## Why this matters
- Argo CD is frequently deployed with broad cluster privileges and access to private Git repositories, cluster credentials, repository credentials, and deployment secrets.
- The vulnerable surface is internal by design, but Kubernetes flat-network assumptions, permissive pod-to-pod traffic, compromised workload pods, or accidentally exposed service ports can make internal gRPC / Redis services reachable.
- Synacktiv specifically warns that the protective Argo CD Kubernetes NetworkPolicy is not applied by default in Helm deployments because Helm values default `networkPolicy.create` to `false` and `defaultDenyIngress` to `false`.
- The issue is unpatched and has no CVE at publication time, so mitigation is currently architectural: deny network reachability to `argocd-repo-server` and Redis except from expected Argo CD components.
- Synacktiv temporarily withheld its exploitation tool, `argo-cdown`, but published enough technical detail for defenders to understand exposure and prioritize segmentation.

## Reported exploitation prerequisites and impact
1. The attacker needs network access to the Argo CD `repo-server` gRPC port and the Redis database port. These should not be user-reachable.
2. The unauthenticated `repo-server` gRPC surface can be reached without Argo CD API-server authentication or RBAC if the network allows it.
3. The attack manipulates repository/cache data and Argo CD manifest generation flow.
4. Successful exploitation can deploy arbitrary Kubernetes manifests and, depending on Argo CD privileges, lead to full cluster compromise.
5. Synacktiv demonstrated the issue against Argo CD `v2.13.3`; no complete affected-version list or fixed release was available in the public post.

## Defender heuristics
- Inventory Argo CD deployments and identify whether `argocd-repo-server` and Redis services are reachable from any workload namespace, developer VPN segment, ingress, service mesh gateway, or debug/jump pod.
- Enforce default-deny pod ingress around Argo CD and allow `argocd-repo-server` traffic only from expected Argo CD components such as `argocd-server`, `argocd-application-controller`, `argocd-notifications-controller`, and `argocd-applicationset-controller` on the intended port.
- For Helm deployments, explicitly set NetworkPolicy-related values rather than assuming the upstream manifest policy is present; verify with `kubectl get networkpolicy -A` and service reachability tests from non-Argo namespaces.
- Treat any unexpected pod with access to Argo CD Redis and repo-server as a control-plane compromise risk; review recent pod exec sessions, ephemeral containers, debug pods, service account token use, and network-policy changes.
- Hunt Argo CD logs, Redis telemetry, and Kubernetes audit logs for unexpected repo-server gRPC calls, repository-cache mutation, manifest generation anomalies, sudden application syncs, and deployment of manifests not present in trusted Git history.
- Rotate repository credentials, cluster credentials, and any deployment secrets accessible to Argo CD if suspicious reachability or exploitation indicators are found.
- Monitor for release notes, CVE assignment, and patched Argo CD versions; until a fix exists, prefer segmentation and least-privilege Argo CD project / service-account scoping.

## Related pages
- [Amazon Q CVE-2026-12957 MCP auto-execution](amazon-q-cve-2026-12957-mcp-auto-execution.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)
- [MCP stdio command-execution boundary](../patterns/mcp-stdio-command-execution.md)
- [Marimo CVE-2026-39987 LLM-agent post-exploitation](marimo-cve-2026-39987-llm-agent-post-exploitation.md)

## Sources
- Synacktiv: <https://www.synacktiv.com/en/publications/caught-in-the-octopus-trap-unauthenticated-rce-in-argo-cd-with-codeql>
- The Hacker News: <https://thehackernews.com/2026/07/unpatched-argo-cd-repo-server-flaw.html>
