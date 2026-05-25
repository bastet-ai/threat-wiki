# Polymarket npm wallet-drainer packages

## Summary
SafeDep reported nine npm packages published by the throwaway `polymarketdev` account that impersonated Polymarket trading CLIs and bots, including AI-assistant-themed names such as `polymarket-claude-code` and `polymarket-ai-agent`.

The packages wrapped real-looking Polymarket trading functionality and a credible GitHub repository around a wallet-theft flow. During interactive installs, a `postinstall` script prompted users to paste a wallet private key while falsely claiming it "stays encrypted." The bundled CLI then POSTed the raw key to an attacker-controlled Cloudflare Worker. In non-interactive contexts, the same payload quietly loaded `.env` files and harvested `PRIVATE_KEY` without showing the prompt.

## Tags
- ops
- operations
- supply-chain
- npm
- crypto
- cryptocurrency
- Polymarket
- wallet-theft
- wallet-drainer
- private-key theft
- postinstall
- social engineering
- AI tooling
- developer machines
- Cloudflare Workers
- typosquat

## Why this matters
- The campaign targets the point where crypto trading automation, developer package installs, and AI-assisted coding workflows meet: users expect to paste keys into local tools and may trust package names suggested by search or an LLM.
- The interactive prompt is social engineering, not an exploit, but it is packaged in an npm lifecycle hook that fires during normal installation.
- The `.env` fallback is more dangerous for developers: projects that already store `PRIVATE_KEY=0x...` for bots or scripts can lose wallet keys without any visible prompt.
- The attacker built a credibility apparatus — functional trading commands, a GitHub repo, stars/forks, SECURITY and CONTRIBUTING files, masked input, and reassuring encryption claims — to make key collection look like onboarding.
- CI and automated scanners may miss the user-facing theft path because the prompt only appears when both stdin and stdout are interactive TTYs.

## Reported package set
SafeDep listed all versions of the following npm packages as malicious:

- `polymarket-trading-cli`
- `polymarket-terminal`
- `polymarket-trade`
- `polymarket-auto-trade`
- `polymarket-copy-trading`
- `polymarket-bot`
- `polymarket-claude-code`
- `polymarket-ai-agent`
- `polymarket-trader`

All nine were reportedly published on 2026-05-20 between 23:30 and 23:32 UTC by `polymarketdev`, with versions `0.1.0` and `0.1.1`. SafeDep says each package shipped the same `dist/index.js` payload.

## Execution and theft flow
1. `package.json` registered `postinstall: node scripts/postinstall.mjs`.
2. The postinstall script checked for an interactive TTY.
3. In non-interactive environments it printed a benign hint and exited, reducing scanner visibility.
4. In interactive terminals it displayed a polished onboarding banner and told the user to paste a wallet key because it "stays encrypted."
5. The script spawned the bundled CLI login flow from `dist/index.js`.
6. The CLI either accepted a pasted key through a masked prompt or loaded `PRIVATE_KEY` from the environment / current-directory `.env` file.
7. The payload sent `{ privateKey, label }` as JSON to the attacker endpoint over HTTPS; no client-side encryption occurred.
8. The package wrote local tracking artifacts under `~/.polybot/`, including a persistent device ID and wallet metadata.

## Infrastructure and indicators
- npm publisher: `polymarketdev`.
- GitHub actor / repository: `texsellix` / `texsellix/polymarket-trading-bot`.
- C2 base: `hxxps://polymarketbot[.]polymarketdev[.]workers[.]dev`.
- Exfiltration path: `/v1/wallets/keys` via HTTP POST.
- Payload SHA-256 for `dist/index.js`: `e01b85c1437085a519217338fe4ee5ed7858c28a10f8c1477b2f1857c3386edb`.
- Local artifacts:
  - `~/.polybot/device.json`
  - `~/.polybot/wallets.json`
- Package names: see the reported package set above.

## Defender heuristics
- Treat any install of the listed packages as wallet-key exposure. Rotate or abandon affected Ethereum / Polygon wallets; moving funds is safer than trusting a reused private key.
- Search developer machines for the package names in lockfiles, shell history, package-manager caches, and `node_modules` directories.
- Inspect `~/.polybot/` for device and wallet artifacts, but do not use their absence as proof that no key was exposed.
- Hunt for outbound requests to `polymarketbot.polymarketdev.workers.dev`, especially `POST /v1/wallets/keys`.
- Review `.env` files and secrets managers for `PRIVATE_KEY` values that may have been present during installation.
- Add package-install controls that flag new packages with lifecycle scripts, recent publish history, single throwaway maintainers, crypto/private-key terminology, or claims that a remote service can hold "encrypted" private keys.
- In AI-assisted development workflows, require provenance checks before accepting suggested package installs, especially packages whose names combine target brands with `bot`, `agent`, `claude`, `ai`, `trade`, or `wallet`.

## Attribution notes
Public reporting ties the cluster to the `polymarketdev` npm publisher and `texsellix/polymarket-trading-bot` GitHub repository. Do not attribute it to TeamPCP or Mini Shai-Hulud without stronger public sourcing; track it as a crypto-focused npm wallet-drainer operation.

## Related pages
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [js-logger-pack Hugging Face exfiltration campaign](js-logger-pack-hugging-face-exfiltration.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- SafeDep: https://safedep.io/malicious-polymarket-npm-crypto-wallet-drainer/
- npm: https://www.npmjs.com/package/polymarket-trading-cli
- npm: https://www.npmjs.com/package/polymarket-claude-code
- GitHub: https://github.com/texsellix/polymarket-trading-bot
