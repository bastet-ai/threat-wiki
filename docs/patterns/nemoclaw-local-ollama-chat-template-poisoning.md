# NemoClaw local Ollama chat-template poisoning (Oasis Security)

## Summary
Oasis Security disclosed that a malicious webpage can take **unauthenticated control of the local Ollama instance** serving an AI agent inside NVIDIA's **NemoClaw** stack and **plant hidden instructions inside the model's chat template**. No CVE has been assigned, no affected-version range or patched version has been published, and no exploitation has been reported as of August 25, 2026. The findings were reported to NVIDIA's PSIRT ahead of publication.

NemoClaw is NVIDIA's open-source reference stack for running agents such as OpenClaw inside its OpenShell sandboxes, with Ollama as one supported local inference backend. On the affected platform path, NemoClaw starts Ollama with a bind that reaches **every network interface** (Windows-host configuration observed as `OLLAMA_HOST=0.0.0.0:11434`), so the Ollama API is reachable from any webpage rendered in the victim's browser.

## Tags
- patterns
- AI agents
- agent platforms
- Ollama
- NemoClaw
- NVIDIA
- OpenClaw
- OpenShell
- DNS rebinding
- CORS bypass
- localhost
- loopback
- chat-template poisoning
- model-level persistence
- prompt injection
- browser-based attack
- local inference
- unauthenticated API
- OLLAMA_HOST

## Why this matters
- **Model-level persistence:** the payload writes a modified Go chat template through the Ollama API. The template controls how the structured messages array is rendered into raw text before the model processes it; the poisoned version appends attacker-controlled text to **every system message at inference time**. The instructions persist across later conversations and survive the agent supplying its own system prompt.
- **Invisible to the client:** "the template is a model-level property invisible to API consumers" — the agent client cannot detect or prevent the poisoning because it never sees the rendered template.
- **Sandboxing does not protect the agent's authority:** "Sandboxing protects the endpoint, but taking over the agent takes over its access and tools" — the poisoned model inherits whatever credentials and tools the agent holds.
- **The browser is already on the host:** the DNS-rebinding chain does not require exposing port 11434 to a LAN or the internet, because the requests originate from the victim's own browser and reach the daemon at the host's own address.
- **No CVE / no fix version / no version range:** operators cannot currently verify whether their installation is in scope; the disclosure is at the "watch" stage.

## Attack shape
1. NemoClaw starts Ollama on the affected platform path with a non-loopback bind (e.g. `OLLAMA_HOST=0.0.0.0:11434`).
2. The Ollama API on port 11434 has no authentication and relies on two middleware layers to block browser-originated requests. When the bind address is not loopback, the **Host-header check is skipped entirely**.
3. The **CORS layer** then treats the request as same-origin because Origin and Host headers both carry the attacker's own domain — true for a page the attacker serves on port 11434.
4. **DNS rebinding** closes the gap: the attacker's domain first resolves to their own server, then to the victim host's address, while the browser keeps treating the requests as same-origin.
5. With the API reachable, the payload writes a modified chat template through the Ollama API (`/api/...` template write).
6. Every subsequent inference on that model appends the attacker-controlled text to system messages; the poisoned behavior persists in the model store.

## Platform-specific Ollama handling (per the report)
- **Non-WSL path:** Ollama sits behind a **token-gated reverse proxy on port 11435**, and onboarding restarts a daemon already bound elsewhere back to loopback.
- **Docker/WSL path:** skips the proxy, because the container reaches the host's loopback through `host.docker.internal`; the daemon is reachable from the container and **does not require authentication on port 11434**.
- **Windows-host path:** the source places the `0.0.0.0:11434`-style bind on this platform path; this is the configuration the rebinding chain targets.
- **NemoClaw's own mitigation:** the local Ollama proxy refuses to start against a backend that is not bound to loopback — a default introduced in **v0.0.106 on August 10, 2026**. It exits with a dedicated status code and prints: "Refusing to start: an Ollama daemon reachable on a non-loopback interface bypasses the proxy's token check entirely. Set OLLAMA_HOST=127.0.0.1:${port} on the Ollama systemd unit or set NEMOCLAW_OLLAMA_PROXY_SKIP_BIND_PROBE=1 to override (not recommended)."
  - The check can be disabled with `NEMOCLAW_OLLAMA_PROXY_SKIP_BIND_PROBE=1` and does **not fail closed** on hosts where the bind check cannot run.
  - NemoClaw does not start that proxy on the WSL paths, and the **Windows-host configuration is one of them** — so the v0.0.106 default does not reach the platform path where the `0.0.0.0:11434` bind exists.
- The Hacker News reviewed the NemoClaw repository (August 25) and found **no chat-template integrity check** anywhere: NemoClaw queries Ollama's model endpoint only for native context length and declared tool-calling capability.
- NVIDIA's documentation tells operators on the Windows-host path not to expose port 11434 to a LAN or the internet — but that guidance addresses inbound network access, not the browser-originated rebinding chain.

## Prior art and related techniques
- DNS rebinding against Ollama's API is documented: Ollama shipped a fix in **v0.1.29 on March 14, 2024**, and NCC Group published an advisory the following month recommending server-side Host-header validation to an allowlist of authorized values.
- Poisoning a model's chat template so instructions run during inference has been documented before; Oasis researchers documented the same technique against **Paperclip** earlier in August 2026 and used a comparable browser-to-localhost path.

## Defender heuristics
### Hardening
- Set `OLLAMA_HOST=127.0.0.1` on the Ollama systemd unit / service (or equivalent) on every host that runs local inference for agents; never bind Ollama to `0.0.0.0` on a host that also runs a browser.
- Do not set `NEMOCLAW_OLLAMA_PROXY_SKIP_BIND_PROBE=1` in production; treat the loopback bind probe as a required control.
- Keep Ollama `>= 0.1.29` so the DNS-rebinding Host-header validation fix is present.
- Where an agent gateway or inference server is reachable from a browser context (hosted agents, dev-boxes, remote desktops), require a token on the API or front it with an authenticated proxy — assume loopback trust is not a boundary.
### Detection
- Hunt for Ollama API writes to model/template endpoints (chat-template modification) from a browser process or any non-service process; template writes are rare in normal operation.
- Alert on Ollama daemons listening on non-loopback interfaces (`0.0.0.0:11434`) on hosts that run NemoClaw/OpenClaw or any agent stack.
- Watch for same-origin DNS-rebinding requests to `127.0.0.1` / `host.docker.internal` from attacker-controlled domains; correlate with subsequent template or model-store changes.
- Treat a changed chat template as **model-store compromise**: export/inspect the template on affected hosts, rebuild the model store from trusted sources, and rotate any credentials or API keys reachable from the agent that used the poisoned model.
- Inventory NemoClaw deployments: note version (v0.0.106 introduced the proxy bind probe), platform path (Windows-host vs Docker/WSL vs non-WSL), and whether the proxy is running.

## Status
- No CVE, no patched version, no confirmed in-the-wild exploitation as of August 25, 2026.
- No browser/OS verification scope was stated in the report for the full chain.
- NVIDIA PSIRT was notified ahead of publication.

## Related pages
- [Agent localhost control-plane RCE](agent-localhost-control-plane-rce.md)
- [AI-agent memory poisoning](ai-agent-memory-poisoning.md)
- [MCP tool description poisoning](mcp-tool-description-poisoning.md)
- [Internet-exposed unauthenticated MCP servers](internet-exposed-unauthenticated-mcp-servers.md)
- [Ollama P2P cryptominer RAT campaign](../ops/ollama-p2p-cryptominer-rat.md)

## Sources
- The Hacker News: [A Malicious Webpage Could Poison Your Local AI Model Behind NVIDIA NemoClaw](https://thehackernews.com/2026/08/a-malicious-webpage-could-poison-your.html) — August 25, 2026 (Oasis Security disclosure; reported to NVIDIA PSIRT ahead of publication)
