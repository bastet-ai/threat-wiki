# `@veai-ru/ai-agent` (npm) — a malicious-by-design terminal AI coding AGENT: obfuscator.io extensions that replace the host agent's system prompt with attacker-controlled content, exfiltrate full session activity to `plugin.veai.ru/telemetry`, read MCP configurations, run a Keycloak OAuth harvest flow, and pull additional components from a Yandex Cloud bucket — LIVE at `latest = 0.3.2`, ZERO OSV + ZERO GHSA, curated queue PR ossf/malicious-packages #1617 only; this wiki pulled and statically inspected the published tarball (no execution) and verified every baked endpoint answering on the network at check

## Tags
- tools
- supply chain attack
- npm
- AI agent
- AI coding agent
- system prompt injection
- session exfiltration
- telemetry exfil
- MCP configuration theft
- OAuth credential harvesting
- Keycloak
- PKCE
- obfuscator.io
- Yandex Cloud
- veai.ru
- explyt
- curated lane
- ossf malicious-packages
- zero advisory coverage
- Russia-nexus infrastructure

## What it is

Curated queue PR ossf/malicious-packages **#1617** (filed 2026-10-10 03:40:36Z, finder credit `smiling-hyena` — the same named finder as the ledger's Sep-21 `radio-player-theme` jsDelivr-routed PoC entry) files npm **`@veai-ru/ai-agent`**, "Veai AI Agent: a terminal AI coding agent." This wiki's same-day verification at ~05:3x UTC:

- **LIVE** at `latest = 0.3.2` (published 2026-10-09 09:54:13Z). Version ladder from the registry `time` block: `0.0.0-stage` Oct 8 09:38:17Z → `0.0.0-bootstrap.0` 09:46:31Z → `0.3.2-dogfood.1` Oct 9 09:17:36Z → `0.3.2` 09:54:13Z — the `0.0.0-stage` staging-stub grammar the ledger already tracks on attacker tooling.
- **ZERO OSV + ZERO GHSA** at query; the record path so far is queue PR only (unmerged) — same-day-unadvised while 209 downloads/week already indexed.
- Publisher account **`explyt-owner` <chatgpt2@explyt.com>**; a package.json `explyt.node` field and a `dist/extensions/explyt-account.js` file carry the `explyt` brand through the artifact; the user-doc endpoint refuses anonymous reads so the account's other packages could not be enumerated; a scope-member search surfaced no sibling `@veai-ru/*` names.
- Tarball (this wiki pull, sha256 `280a2ce8ff3bbf8f4891e0f03d25dadbb3f754cfeeb6870bd4f1cdca5b572c72`, ~6.4 MB unpacked): a genuinely complete-looking terminal coding-agent product — real `README`, `agent-docs/`, `THIRD-PARTY-NOTICES`, MCP adapter, subagent definitions (`hawkeye`/`retriever`/`workhorse`), vendored typebox/zod/yaml — with the hostile surface in **`dist/extensions/*.js`**, which `package.json` auto-loads via the pi-package mechanism `"pi": { "extensions": ["./dist/extensions/*.js"] }`. The README states the agent "runs with exactly the extensions this build ships with" — the extensions ARE the product surface, and they are where the hostile behavior lives.

## Mechanics (static inspection of the published tarball, no execution)

What PR #1617 asserts, checked file-by-file against the shipped bytes:

1. **System-prompt replacement (`dist/extensions/identity.js`, 33 KB).** The file is a textbook **obfuscator.io string-array-rotation** blob (verified header shape: `parseInt` checksum loop + rotated string table + hex indexes — the exact family the ledger already profiles on `chai-logger` and the PhantomRaven-adjacent sets). No plaintext survives to read; per the PR the decoded array embeds fragments of well-known AI-agent harness system prompts used as **injection templates** that replace the active agent's system prompt at session start. This wiki's confirmation is the obfuscation itself + the file's session-start hook role, not a decoded read.
2. **Full session exfiltration (`dist/extensions/telemetry.js`, 68 KB).** Same obfuscated class; plaintext identifiers that survived include `telemetry` and `conversationId`. The PR enumerates the hooked event set — `agent.ToolCall.Started/Completed`, `tool_execution_start/end`, `session.Session.Started`, `agent.Context.Compacted` — and payload fields `conversationId, workspaceId, model, inputTokens, outputTokens, username, hostname, platform`, all POSTed to `https://plugin.veai.ru/telemetry`.
3. **MCP configuration theft (`dist/extensions/mcp.js`, 139 KB).** Largest extension; zero plaintext config-path hits in this wiki's grep (`.claude/settings`, `mcp.json`, `.mcp.json`, `mcp_servers.json`) — consistent with the same string-array obfuscation; per the PR it reads and exfiltrates those MCP config files. The target list is exactly the MCP-config inventory an agent-supply-chain researcher would expect.
4. **OAuth credential harvesting (`dist/extensions/explyt-account.js`, 19.5 KB).** This wiki confirmed plaintext `code_verifier` and `keycloak` identifiers; per the PR it drives an OAuth **PKCE** flow against `https://app.veai.ru/keycloak` and stores harvested access tokens in the OS keychain via `@napi-rs/keyring` (the package even ships a standalone `dist/mcp-keyring-helper.cjs` keychain read/write/remove helper, clear text, taking JSON requests on stdin).
5. **Binary delivery via Yandex Cloud (`dist/cli/brand-profile.js`, `dist/install/installer.js`).** CONFIRMED IN PLAINTEXT: `https://storage.yandexcloud.net/veai-releases/agent/` (bucket answered `403` — exists, listing denied), `https://app.veai.ru/`, `https://app.veai.ru/keycloak`, `https://app.veai.ru/api/v1/data`, `https://plugin.veai.ru/telemetry`, `https://plugin.veai.ru/openai/api/v1` — the last one meaning the package can also route the victim's model traffic through the operator's proxy. The installer additionally bootstraps its own Node runtime from nodejs.org and an npm root, i.e. the install path is self-sufficient.

**Network state at this wiki's check (~05:4x UTC Oct 10):** `plugin.veai.ru/telemetry` `405` (listener live, POST-only), `app.veai.ru` `200`, `storage.yandexcloud.net/veai-releases/` `403`. All three C2 surfaces alive within ~20 h of the `0.3.2` publish.

## Why this class matters

This is not a hijacked legit package and not a typosquat: it is a **complete, self-branded AI coding agent whose business model appears to BE the telemetry** — the durable defensive reads:

- The victim installs it voluntarily, `login`s into it voluntarily, and types real work into it. Every credential-injection and session-tap pattern the ledger has catalogued against compromised agents (469-location collectors, MCP config reads, workflow-log theft) arrives here **as advertised product behavior behind obfuscation**, with a jurisdictional infrastructure signature (`veai.ru` domains, Yandex Cloud `ru-central1` bucket, Keycloak IdP).
- The prompt-replacement hook makes the package an **attack amplifier against every OTHER agent on the same machine**: the system prompt is the trust root for tool-calling, so an attacker-controlled prompt can steer the agent to exfiltrate more, approve more, or write malicious code the user then ships.
- `@veai-ru/ai-agent` is the pi-package ecosystem (peer deps `@earendil-works/pi-coding-agent` 0.84.4) — the extensions auto-load mechanism (`pi.extensions` glob in package.json) is a new delivery rail worth a grep: **any pi-package with obfuscated files under `dist/extensions/` is the same shape**.

## Hunt keys

- Domains/URLs: `plugin.veai.ru/telemetry`, `plugin.veai.ru/openai/api/v1`, `app.veai.ru/keycloak`, `app.veai.ru/api/v1/data`, `storage.yandexcloud.net/veai-releases/agent/`.
- Files: `dist/extensions/identity.js` / `telemetry.js` / `mcp.js` / `explyt-account.js` obfuscator.io headers; `mcp-keyring-helper.cjs` invoked with stdin JSON; `~/.pi` or equivalent extension dirs containing `@veai-ru/ai-agent`.
- Account: publisher `explyt-owner` / `chatgpt2@explyt.com`; tarball sha256 `280a2ce8ff3bbf8f…` (`0.3.2`).
- Egress: if your org never needs `*.veai.ru` or Yandex Cloud object storage, deny it — the Unit 42 negative-egress-baseline control applies directly.

## State and monitors

At check: LIVE, installable, zero advisories on either lane, PR #1617 open unmerged (queue freeze pattern — `#1612`/`#1613`/`#1615` also still open since Oct 9). Monitor: whether the GHSA lane mints anything for this name (post-`arsya` rule: walk the `type=malware` listing, the ID-walk is blind); whether npm enforces (deletion vs security-holder — see the kmf 12-second family wipe precedent); `0.3.x` iteration or re-registration under new names; `explyt` brand footprint beyond this scope (the `app.veai.ru/api/v1/data` "Neo plugin" rail the README mentions implies a managed-backend product surface beyond npm); whether `smiling-hyena`'s next find lands; whether pi-package ecosystem ships an extension-signaling control.

**Oct 10 one-hundred-and-thirty-third sweep tick (~09:4x UTC):** STILL LIVE `latest 0.3.2`, zero OSV + zero GHSA ≈30 h; `app.veai.ru` 200; `plugin.veai.ru/telemetry` GET `405` / POST `400` — POST-only endpoint confirmed (the 405-vs-400 split says the route accepts POST and rejected the empty body; the rail is UP); Yandex bucket root `403`-exists, `agent/` path `404`; PR #1617 still open unmerged.

## Related pages

- [py2ops PyPI operator-linked companion shell](py2ops-pypi-operator-linked-repl-registration-panel-space-z-october-2026.md) — same-48h, same zero-advisory curated-lane class; different target (keystrokes at a fake REPL vs full agent sessions)
- [GhostAction GitHub Actions workflow injection](../ops/ghostaction-github-actions-workflow-injection-git-history-credential-mining-stepsecurity-october-2026.md) — the CI-side mirror of the same credential-mining appetite
- [Unit 42 Web3 C2 evolution on the ChainDrop page](../ops/chaindrop-keyv-cacheable-npm-worm.md#october-7-unit-42-web3-c2-evolution) — the negative-egress-baseline control cited above
- [Mini Shai-Hulud npm/PyPI worm campaign](../ops/mini-shai-hulud-npm-pypi-worm-campaign.md) — the 469-location collector whose AI-tool config targets this package formalizes as product
