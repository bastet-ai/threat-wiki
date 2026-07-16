# codexui-android OpenAI token stealer

## Summary
Aikido Security reported that the npm package `codexui-android`, a legitimate-looking remote web UI for OpenAI Codex with active development and roughly 27,000 weekly downloads, contained npm-published code that was not present in the public GitHub source. The malicious code ran at module load, read Codex authentication material from `~/.codex/auth.json` or `$CODEX_HOME/auth.json`, XOR-encoded the full JSON blob, and posted it to `sentry.anyclaw[.]store/startlog` with a `codexui/<version>` user agent.

Aikido says the theft chain was present from `codexui-android@0.1.82` and affected every startup where local Codex auth tokens existed. The same package was pulled automatically by Android apps from the same publisher, including a Google Play app named "OpenClaw Codex Claude AI Agent" (`gptos.intelligence.assistant`) and a paid "Codex" app (`codex.app`), through an unpinned `pnpm add codexui-android@latest` bootstrap inside a Termux-derived / PRoot environment.

## Tags
- ops
- operations
- npm
- supply-chain
- developer-targeting
- AI tooling
- OpenAI Codex
- Codex
- Android
- Google Play
- OAuth tokens
- refresh tokens
- credential-theft
- infostealer
- exfiltration
- source-package drift
- long-lived tokens

## Why this matters
- The package was not a simple typosquat: it provided useful functionality, had a real repository, active development, and a meaningful user base, making legitimacy itself part of the delivery mechanism.
- The exfiltration code existed in the npm artifact but not the public source repository, reinforcing the need to inspect published packages, sourcemaps, and install/runtime behavior rather than trusting source-only review.
- Stolen Codex `refresh_token` values are high-impact because Aikido reports they do not expire normally and can enable persistent impersonation beyond a single chat session.
- The Android delivery path shows AI developer tooling crossing desktop, npm, and mobile app boundaries: a clean-looking APK can bootstrap an unpinned npm package after install and inherit the package's malicious runtime behavior.

## Theft chain
Reported execution chain:

1. `codexui-android` starts and imports a bundled chunk before the application code runs.
2. The chunk resolves `~/.codex/auth.json` or `$CODEX_HOME/auth.json`.
3. If the file contains `access_token` or `refresh_token` values, the package serializes the entire auth JSON.
4. The payload is XOR-encoded with the key `anyclaw2026`, base64-encoded, and sent via HTTPS POST to `sentry.anyclaw[.]store/startlog`.
5. Network errors are suppressed, and the host name is shaped to resemble ordinary Sentry telemetry.

Reported stolen material includes `access_token`, `refresh_token`, `id_token`, and account ID values from the Codex auth file.

## Android bootstrap path
Aikido also reported that Android apps from the same publisher bundled a Termux-derived Linux userland and ran Node.js through PRoot. On launch, the apps executed an unpinned package install similar to:

```text
pnpm add codexui-android@latest --prefer-offline --config.node-linker=hoisted
node /usr/local/lib/node_modules/codexui-android/dist-cli/index.js --port <port>
```

Because the package version was not pinned, installed apps could pull whatever npm currently served. Once a user signed in inside the app, the sandboxed Codex `auth.json` became available to the malicious package and was sent to the same exfiltration endpoint.

## Defender heuristics
- Search developer workstations, AI-agent sandboxes, npm caches, lockfiles, and mobile analysis pipelines for `codexui-android`, especially versions `0.1.82` and later.
- Treat any OpenAI Codex auth material present on systems that ran the package as exposed; revoke sessions/tokens where possible and rotate adjacent OpenAI, GitHub, cloud, package-registry, SSH, and application credentials that may be reachable from the same environment.
- Hunt for outbound HTTPS requests to `sentry.anyclaw.store` and `/startlog`, especially with `User-Agent` values beginning `codexui/`.
- Compare npm package contents against source repositories for source/artifact drift, unexpected top-level imports, sourcemaps with exfiltration comments, and telemetry-looking domains embedded only in built artifacts.
- Avoid unpinned runtime package bootstraps in mobile or desktop wrappers for AI tooling; require exact versions, integrity pins, and offline-reviewed artifacts.
- Monitor AI-tool auth files such as `$CODEX_HOME/auth.json` and `~/.codex/auth.json` as high-value secrets, not convenience cache files.

## Related pages
- [Malware-Slop Claude user-data npm infostealer](malware-slop-claude-user-data-npm-infostealer.md)
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)
- [Glassworm developer supply-chain botnet](glassworm-developer-supply-chain-botnet.md)
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [AI-augmented adversary operations](../patterns/ai-augmented-adversary-operations.md)

## Sources
- Aikido Security: <https://www.aikido.dev/blog/codex-remote-ui-steals-ai-tokens>
- npm package metadata: <https://www.npmjs.com/package/codexui-android>
- GitHub issue referenced by Aikido: <https://github.com/friuns2/codex-mobile/issues/198>
