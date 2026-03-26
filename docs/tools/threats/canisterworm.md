# CanisterWorm

## Summary
CanisterWorm is the NPM worm associated with TeamPCP's supply-chain campaign. It was designed to propagate through stolen npm publish tokens, push malicious versions across a package scope, and install persistence on Linux developer hosts.

## Tags
- malware
- worm
- npm
- supply-chain
- tooling
- operations
- persistence

## Core characteristics
- **Self-propagating** through package publish rights
- **Postinstall loader** for execution on install
- **User-level systemd persistence** on Linux
- **ICP canister dead-drop** C2 for payload rotation
- **Masquerades as PostgreSQL tooling** (`pgmon`, `pglog`)
- Uses README preservation and patch-version bumps to blend in

## Operational flow
1. A compromised npm token is used to enumerate publishable packages.
2. The worm republishes malicious versions across the scope.
3. On install, a postinstall loader writes a Python backdoor and a systemd user unit.
4. The backdoor polls a canister for a new payload URL.
5. If the attacker updates the URL, infected hosts fetch the new binary.

## Defender takeaways
- Revoke npm tokens aggressively after a suspected compromise
- Review package publish history for sudden patch releases and README preservation
- Hunt for `systemd --user` services created from package installs
- Treat a package-scoped publish spree as a likely worm event

## Sources
- Aikido: https://www.aikido.dev/blog/teampcp-deploys-worm-npm-trivy-compromise
- Wiz: https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack
