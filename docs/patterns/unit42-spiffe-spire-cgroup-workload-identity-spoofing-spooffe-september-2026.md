# Unit 42: post-exploitation workload-identity spoofing in SPIFFE/SPIRE — cgroup-selector manipulation and the Spooffe tool

## Tags
- patterns
- Unit 42
- SPIFFE
- SPIRE
- workload identity
- machine identity
- Kubernetes
- cgroup
- cgroupv2
- attestation
- selector spoofing
- identity spoofing
- SVID
- lateral movement
- post-exploitation
- cloud-native
- container security
- Spooffe
- open-source tool
- node compromise
- trust boundary

## Summary
On **September 10, 2026**, Unit 42 (Eviatar Garzi) published **"The Machine With Many Faces: Post-Exploitation Identity Misuse in SPIFFE/SPIRE"**, demonstrating that an attacker who already holds **root on a Kubernetes node** can abuse the SPIRE agent's workload-attestation logic to **impersonate co-located workloads and harvest their SPIFFE Verifiable Identity Documents (SVIDs)** — i.e., the short-lived machine identities that replace long-lived secrets in cloud-native environments. Unit 42 states explicitly that it has **not observed this technique exploited in the wild**; this is a defensive-research disclosure, not a confirmed campaign.

The core finding: SPIFFE/SPIRE enforces strong cryptographic identity *between workloads*, but that guarantee rests on an **implicit trust assumption — that the node is trusted**. Once root is present on the node, an attacker can manipulate the **Linux cgroup (cgroupv2) metadata** the SPIRE agent reads during workload attestation, causing the agent to **misattribute selectors** and issue a co-located workload's SVID to an attacker-controlled process. The attacker then laterally moves using **legitimate credentials rather than stolen secrets** — identity isolation between workloads collapses.

## The trust assumption that collapses
SPIFFE (Secure Production Identity Framework for Everyone) standardizes machine identity to solve the "Secret Zero" bootstrap problem. Each workload gets three components:

- **SPIFFE ID** — canonical URI-style name (`spiffe://<trust-domain>/<path>`); the trust domain is the issuer / security boundary.
- **SVID** (SPIFFE Verifiable Identity Document) — a short-lived credential signed by the SPIRE server (CA) that proves the workload is who it claims to be. Two forms: **X.509 SVID** (certificate, used for mTLS) and **JWT SVID** (bearer token, used for application-level authorization).
- **Trust Bundle** — trust anchors (root CA certs or JWKS) used by peers to verify an SVID was issued within the trust domain.

SPIRE is the widely deployed reference implementation. Its runtime pieces:

- **SPIRE Server** (control plane) — the CA; stores registration entries, signs SVIDs, publishes the trust bundle.
- **SPIRE Agent** — runs on every compute node (K8s node, VM, bare metal); accepts workload requests over the local Workload API (UNIX socket), talks to the server over the Node API, **performs attestation**, caches SVIDs, handles rotation.
- **Registration entries + selectors** — server-side policy objects mapping a set of runtime attributes (selectors) to a SPIFFE ID. When a workload requests an identity, the agent collects selectors and the server issues an identity only if the entry's selectors are a **subset** of the workload's selectors.

Attestation runs at two levels: **node attestation** (trust the agent) and **workload attestation** (identify the individual workload). The disclosure targets the latter.

## How the agent derives selectors (the attack surface)
The agent hands a requesting workload's **PID** to configured workload-attestor plugins, which derive selectors from process/container metadata:

- **k8s plugin** — uses the PID to read **`/proc/<pid>/mountinfo`** or **`/proc/<pid>/cgroups`**, extracts the **pod UID** and **container ID** from the cgroup path (e.g. `kubepods.slice/kubepods-besteffort.slice/kubepods-besteffort-pod<pod_uid>.slice/cri-containerd-<container_id>.scope`), then queries the **kubelet** with the agent's service-account token (`/var/run/secrets/kubernetes.io/serviceaccount/token`) to fetch pod metadata. The kubelet `ClusterRole` only needs `get` on `pods`, `nodes`, `nodes/proxy` — a low-privilege but exploitable scope. The k8s plugin emits selectors such as `k8s:sa:default`, `k8s:ns:default`, `k8s:node-name:mars`, `k8s:pod-uid:...`, `k8s:pod-name:...`, `k8s:pod-image:...`, `k8s:container-image:...`.
- **Unix plugin** — reads `/proc` for **UID / GID / supplementary GID** selectors (`unix:uid:0`, `unix:gid:0`, `unix:supplementary_gid:0`).

The agent combines both selector sets and matches them against cached registration entries; a subset match returns the corresponding SVID.

## The technique: cgroup-path selector spoofing
Because the k8s plugin reconstructs pod/container identity **from the cgroup path visible under `/proc`**, an attacker with **root** can **manipulate the cgroup metadata** for their own process so it advertises a *victim* workload's pod UID / container ID. The agent then treats the attacker process as that co-located workload and **issues the victim's SVID**. This is a **selector spoofing** primitive: not a flaw in the cryptography, but in the **attestation evidence the agent trusts**.

Consequences:

- **Workload impersonation** — the attacker process holds the victim's X.509 SVID and can present it in mTLS handshakes as the victim.
- **Identity harvest** — by iterating over co-located workloads' cgroup paths, the attacker can obtain **all workload identities scoped to the node**.
- **Legitimate-credential lateral movement** — the attacker moves laterally using **valid SVIDs**, which downstream services accept as genuine workload identity, defeating "secret rotation" / "short-lived credential" defenses that assume the node is honest.

The same class of primitive also applies wherever a host-level process can forge the cgroup/`/proc` inputs that an attestation pipeline trusts.

## Spooffe (defender tool)
Unit 42 released **Spooffe**, an open-source tool that **automates the attack as a defensive test** to answer: "given root on a node, which workload identities could an attacker harvest, and how large is the resulting identity area of impact?"

- **Node scan** — enumerates running workloads and **discovers their cgroup paths**.
- **Mock cgroup replication** — for each target workload, Spooffe **replicates its cgroup path as a mock cgroup** bound to Spooffe's own process.
- **SVID extraction** — queries the **local SPIRE agent** under the spoofed selectors and **collects the resulting SVIDs**, dumping every workload identity present on the host.
- **Agent impersonation** (additional capability, not the focus of the post) — checks whether an attacker could **impersonate the SPIRE agent** and talk to the server directly to extract workload identities.

Treat Spooffe as a **blue-team/Red-team utility**: it is a controlled test of the "root ⇒ all node-scoped identities" exposure, not an offensive weapon per se.

## Why this matters
- **The node is the identity boundary, not the workload.** SPIFFE/SPIRE's cryptographic guarantees are only as strong as the integrity of the host doing attestation.
- **cgroup/`/proc` are attacker-writable inputs** for workload attestation once root is reached; selector-subset matching means a **single spoofable field** can be enough to earn a victim identity.
- **Low-privilege service accounts are a risk**, not a mitigation: the SPIRE agent's kubelet access (`get pods/nodes`) is exactly what the k8s plugin needs, so restricting it further is a valid hardening lever.
- **Weak selectors are the multiplier.** Broad selectors (`k8s:ns:default`, `unix:uid:0`) make subset-matching succeed across many workloads; narrow, specific selectors shrink the blast radius.

## Detection (hunt)
There is no single signature — this is **attestation-layer spoofing** — but defenders can look for:

- **Workload requesting an SVID whose pod/container selectors do not correspond to a live pod on the node** (agent-side selector/pod mismatch).
- **Unusual `/proc` or cgroup access patterns** from a process that is not a kubelet/container-runtime component (e.g. a non-runtime process reading many `cri-containerd-*.scope` cgroup paths).
- **Bursts of SVID issuance for many distinct pod UIDs from one agent** (an "identity dump" shape), especially if the requesting PID is not a container runtime.
- **SPIRE agent service-account token use** (`/var/run/secrets/.../serviceaccount/token`) from a process that is not the SPIRE agent.
- **C2 / lateral movement with a valid SVID** to services that were not reachable from the origin workload's declared identity.
- Presence of **Spooffe-like tooling** on a node (open-source, fingerprintable) during a node-compromise investigation.

## Remediation
Per Unit 42's guidance, and reinforced here:

1. **Treat node root as compromise of all node-scoped identities.** Assume full SVID exposure on a root-compromised node and rotate/revocate the affected trust-domain identities.
2. **Harden nodes** — minimize the root-attacker surface (no untrusted workloads, strict PodSecurity, no `hostPath`/`hostPID`/`hostNetwork` where not required, no privileged containers).
3. **Restrict root / limit direct host access** — least-privilege access to the SPIRE agent process, its socket, and its service-account token.
4. **Prohibit privileged containers and host access** — the cgroup/`/proc` spoofing primitive requires the ability to manipulate cgroup state, which privileged or host-pid containers can do.
5. **Minimize reliance on weak selectors** — use **narrow, specific selectors** (pod-image digest, container-image digest, pod labels unique to the workload, pod-owner) rather than broad `ns:default` / `uid:0` matches, so a subset match is harder to forge.
6. **Prefer attestation that does not trust host `/proc`/cgroup inputs** where the SPIRE build / plugin configuration allows (e.g. tighter k8s-plugin scoping, additional node-level controls, or a different workload-attestor that does not rely on cgroup path parsing).
7. **Monitor SPIRE server / agent audit logs** for SVID issuance patterns that do not match live pod state (see Detection above).
8. **Run Spooffe in staging** to measure your identity area of impact and drive the selector-tightening / node-hardening program.

## Related pages
- [Linux kernel CVE-2022-0492 cgroup release-agent exploitation](../ops/linux-kernel-cve-2022-0492-cgroup-release-agent-exploitation.md) — another cgroup-adjacent host-primitive class; different mechanism, same "cgroup as attack surface" theme.
- [Unit 42 machine-speed agentic intrusion](../ops/unit42-ai-assisted-cyber-attack-machine-speed-agentic-intrusion-september-2026.md) — post-compromise cloud/AI-endpoint repurposing as C2; this page is the SPIFFE-side analogue for cloud-native workloads.
- [Wiz "Off Guard: Breaking LiteLLM"](../ops/wiz-litellm-off-guard-mcp-bypass-rce-cloud-compromise-september-2026.md) — MCP / AI-gateway trust-boundary failures in the same cloud-native / AI-tooling domain.

## Sources
- Unit 42 (Eviatar Garzi): [The Machine With Many Faces: Post-Exploitation Identity Misuse in SPIFFE/SPIRE](https://unit42.paloaltonetworks.com/kubernetes-spiffe-spire-identity-spoofing/) (published **September 10, 2026**, 11 min read, Category: Malware / Threat Research; Tags: API, Cryptographic, JSON, Linux, Node, SPIFFE, SPIRE, Spoofing). Palo Alto Networks / Cyber Threat Alliance shared.
- SPIFFE specification and SPIRE project (context): https://docs.spiffe.io/
