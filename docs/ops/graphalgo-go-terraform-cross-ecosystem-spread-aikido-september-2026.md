# Graphalgo crosses ecosystems: Aikido finds the npm malware family rebuilt in Go, shipped through the FIRST malware-distributed Terraform providers, two fake Go "vanity ecosystems," and a public key that joins it to this wiki's on-wiki npm campaign inventory (Sep 22, 2026)

## Tags
- ops
- supply-chain
- go
- terraform
- terraform providers
- npm
- Graphalgo
- cross-ecosystem
- blockchain dead drop
- Arbitrum Sepolia
- Slack C2
- ECDH
- fake ecosystem
- typosquat
- targeted
- DevOps targeting
- Aikido
- ReversingLabs
- forged commits

## Summary

Aikido Security Research published on **September 22, 2026** that the **Graphalgo** malware family — first reported by ReversingLabs in **February 2026** on npm, and covered during the last week by SafeDep, Checkmarx, and JFrog — has been **ported to Go** and is now distributed through **at least two Terraform providers and two Go Modules**. This is **the first case of systematic malware distribution through Terraform providers** that Aikido (and, per the post, the wider research community) is aware of. The Go samples **share blockchain and Slack infrastructure and an ECDH public key with recent npm Graphalgo payloads** — the key `302a300506032b656e032100bad013df6eec5d686f4cc8551e0a5c87a0135164bdd1dafb1c75141d1b526702` has appeared in npm payloads since at least April 2026, first in **`modern-events`**, a package that sits in this wiki's own [Equation-of-Compromise campaign inventory](equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md) (`modern-events` 1.3.3–1.5.2, XRAY-968383, March 3 — npm-holdered since April). The public key is therefore a **hard cryptographic join** between the npm campaign record this wiki tracks and the new Go/Terraform operation; contract addresses, Telegram addresses, and Slack workspaces additionally link back to ReversingLabs' April post.

Malicious artifacts (any versions):

| Ecosystem | Name | Notes |
| --- | --- | --- |
| Terraform provider | `gocommunity-io/dockerd` | TA-controlled org `gocommunity-io` |
| Terraform provider | `kreuzwenker/docker` | **Typosquat of `kreuzwerker/docker` (56 M downloads)** |
| Go module | `gocommunity.io/orderedbtree` | malware in plaintext; forged commits |
| Go module | `gogets.dev/btreex` | malware in ZIP masquerading as `.sql`; forged commits backdating to Nov 2025 |

Aikido reports the operation as **small and targeted** — 18 unique hostnames across 725 plaintext check-ins (3 Windows, 5 Linux, 10 macOS since mid-July), the actor's own test machine (`Frank`/`Frank1`) included in the earliest messages.

## The activation design: inert unless the runtime matches a hash

Both Terraform providers hide entry points in `internal/provider/resource_docker_container_funcs.go` that **activate only when `SHA256(containerName + networkID)` of the Terraform variables equals** `b9966e3762e9a0d5d263b8cb3cca07294f81af9714d40ddf4628cb85d74e8ad5`. That hash doubles as the **AES key** that decrypts a file path inside the package; the named archive — `examples/resources/docker_container/import-resource.sqlite3` (SHA-256 `5f892a5424e88a21a3eb3d7f82ebf04d8ac31cdb19ada25153be4165df977d0f`, ZIP-magic despite the `.sqlite3` extension) — is unzipped, each file AES-decrypted, and executed as a Go package via a **detached `go run .`**.

`gocommunity.io/orderedbtree` (published Aug 11) carried the same malware in plaintext. `gogets.dev/btreex` (published Sep 8) hides it in a ZIP masquerading as `btreex.sql` (SHA-256 `ab01686d87565250fc4989faddb877d793667b07ec217a61cbd798f5695d62f5`) and only activates when processing an object with a **specific price integer value** — the same selective-trigger design.

**This is the Checkmarx `indexed-btree` runtime-loader lesson replayed in Go** (see the [Equation-of-Compromise Sep 22 section](equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md#september-22-checkmarx-runtime-loader-overlap)): no install-time execution, code dormant behind a runtime-condition equality test, so install-time scanning and publish-time scanning both return clean. A sha256'd trigger constant in a provider's source is the artifact — grep your vendored providers for `b9966e3762`.

## Second stage: dual-channel C2 with per-victim ECDH — the sophisticated member of the blockchain dead-drop family

The Go RAT fingerprints hardware/OS/hostname/user and whether `node` exists, posts a "System Report" to channel **`frontend-devs`** in Slack workspace **`portfolio-devs.slack[.]com`**, then publishes its ephemeral public key there. All subsequent traffic is ECDH-encrypted to two operator public keys (Slack side uses the hardcoded key above), and tasking moves to channel **`qa-announcements`** in a second workspace, **`portfolio-testers.slack[.]com`** (a third, `mediumstar.slack[.]com`, is a historical unreported indicator). Slack API calls hit `api.slack.com` — the workspace subdomains are never contacted, so proxy blocks on the workspace hostnames do nothing.

The blockchain channel resolves from an **Arbitrum Sepolia** contract, **`0xAD02b5cDE693529d3bdA0266299501ad0193036C`**: the client reads the operator's public key and a shared-wallet private key (itself encrypted under the second-stage key material), registers its ephemeral key via a `setCPubKey` method, and reads encrypted commands from `serviceData1`/`serviceData2`. **The shared wallet is permissioned to write ONLY the `setCPubKey` key-value store** — rogue or compromised clients cannot spam or disrupt the channel. Polling: blockchain every **3 s**, Slack every **10 s**. Decrypted messages carry a header selecting execution as **Go or JavaScript (via `node`)** or self-deletion. Every client consumes every message and no-ops when decryption fails — commands are invisible to all other infected hosts. Aikido explicitly rates this **a notably sophisticated blockchain dead-drop implementation with bidirectional communication and minimal leakage/disruption risk**.

Cross-vendor join for defenders: this lands in the on-wiki on-chain-C2 family (**ChainScript Polygon/WebSocket, GoCaracal `eth_getStorageAt`, Aeternum Polygon `getDomain()`, JFrog's Sepolia tasking registries, ChainDrop `/router`**) — and it is the **first Arbitrum Sepolia** member: hunting JSON-RPC to public Sepolia endpoints must now include **Arbitrum Sepolia RPC** as well. Same-family tells: `portfolio-devs` / Slack-as-C2 is the same channel type JFrog documented for the npm campaign's dual-bot agent (10-s no-jitter `conversations.history`-class polling).

## The fake-ecosystem infrastructure and forged git dates

GitHub accounts/orgs in the report: `gocommunity-io`, `go-pack-tech`, `kreuzwenker`, `victormmpp` (dropper repo with forged commits), `gogets-dev`, `markcary3`, `steveb082`, `go-community-admin`. The actor **periodically cleans its malware off GitHub** to extend account lifetimes. Two companion websites — **`gogets[.]dev`** and **`gocommunity[.]io`**, registered within a day of the attacker-controlled orgs — present themselves as **vanity-naming Go package ecosystems** but accept no external packages: their function is social-engineering legitimacy for module paths that would otherwise look wrong (`gogets.dev/btreex` is not a real proxy-routable ecosystem the way a legitimate vanity host would be). **Both sites were LIVE (HTTP 200) at this wiki's Sep 22 check**, as were both Terraform provider pages on the official registry (`registry.terraform.io/providers/gocommunity-io/dockerd/latest` and `.../kreuzwenker/docker/latest` both returned 200 — the providers were not yet removed at check).

`markcary3`'s commits in `gogets-dev/btreex` were **forged to backdate to November 2025**, and because **the Go module proxy and pkg.go.dev treat commit dates as authoritative**, the falsified publication date is what everyone downstream displays. Durable: *in the Go ecosystem, publication-date ordering is forgeable at the git layer* — a module that "predates" an incident may not. The same authorship-forgery class as GitHub commit-date abuse, now with proxy-level enforcement of the lie.

## Why Terraform targeting matters

Aikido's assessment, adopted here: Terraform users skew toward **infrastructure deployment roles** — a compromised DevOps workstation is a more direct line to production cloud credentials than a general developer laptop. Their IR guidance follows: treat any environment that installed these as fully compromised; **isolate before rotating** (dual live C2 channels mean the host stays reachable after package removal); rotate cloud/infra credentials FIRST for the Terraform vector; **reimage — the decrypted second stage ran via a detached `go run .`, so package deletion cannot guarantee cleanup**; audit Terraform applies, package publishes, and Actions runs inside the exposure window.

## Timeline (UTC, per Aikido + this wiki)
| Date | Event |
| --- | --- |
| Feb 2026 | ReversingLabs first reports Graphalgo on npm |
| ≥ Apr 2026 | ECDH public key present in npm payloads (`modern-events` first — on-wiki campaign inventory) |
| Jul 16 | Earliest Slack check-ins (actor's own Windows test host) |
| Aug 11 | `gocommunity.io/orderedbtree` published (plaintext malware) |
| Aug 16 | First contract transaction per Aikido's count (1,402 txns since) |
| Early Sep | Terraform providers `gocommunity-io/dockerd`, `kreuzwenker/docker` published |
| Sep 8 | `gogets.dev/btreex` published (SQL-masquerade ZIP, forged commit dates) |
| Sep 22 | Aikido publishes; this wiki verifies `gogets.dev` + `gocommunity.io` live, both providers live on registry.terraform.io |

## Durable reads

1. **A malware family is not its ecosystem.** Graphalgo ported npm→Go wholesale while keeping the same crypto and C2 identities. Family tracking must pivot on **keys, contract addresses, channel names, and code shapes**, not on which registry the samples sit in. The ECDH public key is the strongest join in this report because it cannot be casually rotated without rebuilding every payload.
2. **Terraform providers are now a confirmed malware rail** — first systematic case. Practical: the provider source is fetched and compiled on YOUR machine; pin provider sources to `registry.terraform.io` AND verify namespace spelling (`kreuzwenker` vs `kreuzwerker` is one transposed letter), grep `.terraform.lock.hcl` namespaces like you grep lockfiles (see this wiki's TraderTraitor `.terraform.lock.hcl` page — that delivery shape was provider execution by a different route).
3. **Selective-activation payloads defeat every publish-time scanner**: SHA256-of-runtime-input trigger (Terraform), specific-price-value trigger (Go module). Detection moves to static artifacts (trigger constants, `.sqlite3`-named ZIPs, `go run .` spawn logic) and behavioral (a terraform/node process spawning `go run` detached).
4. **Fake package ecosystems as social engineering** — the vanity-host façade exists to make malicious module paths look legitimate. A module hosted on an unknown vanity domain that refuses external publishing is a targeting artifact, not infrastructure.
5. **Go proxy trust in git commit dates is an integrity hole** — backdated commits change what pkg.go.dev and the proxy believe about release order. Treat first-seen-at-proxy time, not commit date, as the honest clock.
6. **Permissioned shared wallets are the next evolution of on-chain C2** — write-limited to one key-value method, disrupting the channel requires seizing the contract itself. Combine with this wiki's ChainScript read: C2 discovery keeps moving to infrastructure you cannot seize; the countermeasure is egress detection (JSON-RPC including Arbitrum Sepolia; `api.slack.com` from build agents).

## Indicators of compromise

- Packages/providers: `gocommunity-io/dockerd`, `kreuzwenker/docker` (Terraform, any version); `gocommunity.io/orderedbtree`, `gogets.dev/btreex` (Go modules, any version)
- Files: `import-resource.sqlite3` SHA-256 `5f892a5424e88a21a3eb3d7f82ebf04d8ac31cdb19ada25153be4165df977d0f`; `btreex.sql` SHA-256 `ab01686d87565250fc4989faddb877d793667b07ec217a61cbd798f5695d62f5`
- Trigger hash / AES key: `b9966e3762e9a0d5d263b8cb3cca07294f81af9714d40ddf4628cb85d74e8ad5`
- ECDH public key (npm+Go join): `302a300506032b656e032100bad013df6eec5d686f4cc8551e0a5c87a0135164bdd1dafb1c75141d1b526702`
- Contract: Arbitrum Sepolia `0xAD02b5cDE693529d3bdA0266299501ad0193036C` (`setCPubKey`, `serviceData1/2`)
- Slack: workspaces `portfolio-devs.slack[.]com` (channel `frontend-devs`), `portfolio-testers.slack[.]com` (channel `qa-announcements`), `mediumstar.slack[.]com` (historical)
- Domains: `gogets[.]dev`, `gocommunity[.]io` (LIVE at Sep 22 check); GitHub accounts/orgs listed above
- Hunt: `go run .` detached children of terraform/node processes; JSON-RPC to Arbitrum Sepolia RPC endpoints from dev/CI hosts; `api.slack.com` calls from build agents/CI; `import-resource.sqlite3` whose first bytes are `PK`

## Caveats and open questions

- Aikido names no actor; Graphalgo remains a family-level label (ReversingLabs Feb 2026 origin). The npm↔Go identity join is Aikido's key/infra comparison — strong, but the operator behind both waves is unnamed.
- The precise relationship between "Graphalgo," JFrog's Equation-of-Compromise campaign, and Checkmarx's indexed-btree operation is asserted by Aikido only as shared infrastructure/strings across "Graphalgo" reports; the on-wiki inventory overlap (`modern-events` public key) is this wiki's own join observation on Aikido's stated first-seen package — label it as such until the operators name contracts/keys in the same artifact.
- ReversingLabs canonical Feb/April post URLs not retrievable at capture (blog listing returned no graphalgo href) — backfill.
- Whether the Terraform Registry removes the two providers, and whether the registry adds publish-time malware scanning for providers (Aikido notes it has no Terraform coverage itself yet), is the enforcement question to watch.
- Victim notification: Aikido states it cannot identify victims from plaintext check-ins; the 18 hostnames are the actor's client census, not a target list.

## Related pages
- [Equation of Compromise page](equation-of-compromise-npm-mathjs-clone-campaign-sepolia-contracts-slack-c2-github-actions-download-farm-jfrog-september-2026.md) — the npm-side campaign inventory (`modern-events` etc.), Sepolia tasking contracts, Slack chunked-payload agent, and the Checkmarx runtime-loader overlap
- [ChainScript RAT (Polygon WebSocket C2)](../tools/chainscript-rat-polygon-websocket-c2-blackpoint-september-2026.md) — the on-chain C2-resolver family
- [TraderTraitor `.terraform.lock.hcl` delivery](tradertraitor-jade-sleet-flatroof-roofdeck-macos-terraform-lockfile-lures-india-it-provider-sentinelone-september-2026.md) — earlier Terraform-adjacent execution rail (attacker-supplied providers via lockfile)
- [ulid-xyz transitive chain](ulid-xyz-transitive-delivery-chain-microsoftsystem64-dprk-september-2026.md) — same-period cross-ecosystem persistence discipline reference

## Sources
- Aikido Security Research (Oliver Smith), "Graphalgo campaign spreads to Terraform providers and Go Modules," Sep 22, 2026 — `https://www.aikido.dev/blog/graphalgo-terraform-go-modules` (full text captured by this wiki)
- This wiki live checks (Sep 22 ~19:15–19:30 UTC): `gogets.dev` HTTP 200, `gocommunity.io` HTTP 200, `portfolio-devs/portfolio-testers.slack.com` HTTP 403 (workspace pages, not contacted by malware), `registry.terraform.io` provider pages HTTP 200 (providers still listed), `api.github.com/repos/canove/libsignal-node` (unrelated cross-check)
- Referenced upstream: ReversingLabs Feb 2026 Graphalgo post (URL backfill pending); SafeDep / Checkmarx / JFrog Graphalgo-adjacent coverage on-wiki
