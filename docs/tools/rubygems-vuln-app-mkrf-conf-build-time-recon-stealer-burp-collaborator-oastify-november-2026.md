# RubyGems vuln-app: the mkrf_conf.rb build-time recon stealer with a Burp Collaborator sink

`MAL-2026-20103` names a Ruby gem whose "native extension" is a spy: `vuln-app 1.2.1` declares `ext/mkrf_conf.rb` as a build extension, and RubyGems auto-executes that file during `gem install`. The script contains no build logic. It collects installer-side identity and host files, serializes them as JSON, opens its own TLS connection, and POSTs them to a hardcoded **Burp Collaborator** subdomain. The malware ledger wrote the row at `2026-11-17 23:40:25Z`; by this wiki's read `≈00:4xZ` on Nov-18 the gem was already gone from the API while the row stayed live - the ledger is again ahead of the grave, and the sink is still answering.

This is the second build-time credential/recon stealer this ledger has caught on RubyGems in one week (`solana-keypair`, the `extconf.rb` wallet thief), and the first whose sink is a commercial OAST platform instead of a free webhook service. If you build Ruby on this host, read the triage recipe below; `gem install` compiled nothing and ran something.

## The row

- **ID:** `MAL-2026-20103` (OSV, npm/PyPI/RubyGems malware lane)
- **Package:** `vuln-app` (RubyGems), affected version `1.2.1`
- **Origin:** `amazon-inspector` (internal id `IN-MAL-2026-022825`) - the same origin that minted the `solana-keypair` row, second capture of that lane
- **Published:** `2026-11-17T23:40:25Z`; `modified 2026-11-18T00:45:12Z` (re-stamped at the `:45` batcher tick within this wiki's sweep window)
- **Aliases:** `None` - `aliases None` at birth (the amazon-inspector origin lands GHSA-blind like `kam193`; first-GHSA clock armed)
- **Severity:** `None` - unscored at read
- **Reference:** `https://rubygems.org/gems/vuln-app/versions/1.2.1` (the reference page still serves `200` while the API is `404` - see registry state)

## The mechanism, quoted from the shipped source

The ledger's source detail (amazon-inspector, sha `d905ef22…`) reads: the gem declares `ext/mkrf_conf.rb` as a native extension, which RubyGems auto-executes during `gem install`. The script contains no build logic; instead it collects installer-side data:

- `hostname`, login user, current working directory, home directory
- the contents of `/etc/passwd`, `/etc/hosts`, `/etc/resolv.conf`

It serializes the bundle as JSON, opens a **TLS connection** directly to a hardcoded Burp Collaborator subdomain, and POSTs the data.

Two things to weigh honestly: the shipped capture documents **recon** (host identity + three world-readable `/etc` files), not credential-file theft. That is the lighter sibling of `solana-keypair`, which read Solana keypairs, `.npmrc`, `.netrc`, `.git-credentials`, and Ethereum keystores. But the collection set is exactly the reconnaissance an operator runs before choosing a second-stage payload, and nothing in a `mkrf_conf.rb` prevents the author from collecting more in the next push.

## The sink is the story: Burp Collaborator

The exfil endpoint is `g1im618xdjpuonmkxq16mr33quwlm9cx1.oastify.com:443` - a **PortSwigger Burp Collaborator** subdomain (`oastify.com`). This wiki verified the sink answered `200` on GET at `≈00:4xZ` on Nov-18, after the gem itself had vanished from the registry API.

Why this matters more than the payload:

- Collaborator is **paid, professional attacker tooling**. Free lanes (`webhook.site`, ngrok) mean drive-by amateurs; a Collaborator subdomain means someone holds a Burp license and runs out-of-band verification as a habit. The same infrastructure class previously appeared on this wiki as a beacon domain (`whltd1`-style `oastify` hostnames in the ltidisafe fleet), so this is the second sighting of the class and a hunt pivot, not an isolated oddity.
- **OAST sinks are attacker-verified by design.** Every interaction is logged in the operator's Collaborator UI, which means every install is a confirmed victim record handed to the attacker - the beacon doubles as a sales report.
- Defensively, `oastify.com` (and `interact.sh`, its open sibling) are low-traffic domains in most corporate environments. An outbound TLS connection to `*.oastify.com` from a build box is worth a page, let alone a POST.

## Registry state at read (verified by this wiki, ~00:4xZ Nov-18, nothing executed)

| Lane | State |
| --- | --- |
| `rubygems.org/api/v1/gems/vuln-app.json` | `404` - gem gone from the API |
| `rubygems.org/gems/vuln-app-1.2.1.gem` | `403` - download refused |
| `rubygems.org/gems/vuln-app/versions/1.2.1` (HTML reference page) | `200` - the row's own reference still renders |
| `oastify.com` sink (GET) | `200` - collector live after the removal |

This is the **row-ahead-of-the-grave** pattern already recorded for `node-test-repo`: the OSV row names a gem the registry no longer serves through its API. A row without registry surface is a history lesson plus a live sink; a tarball at `200` would have been the install emergency. The quote that matters is the sink, not the shelf.

## The family: build-time execution on RubyGems, two specimens in one week

| | `solana-keypair` (Nov-16 row) | `vuln-app` (Nov-17 row) |
| --- | --- | --- |
| Trigger file | `ext/extconf.rb` | `ext/mkrf_conf.rb` |
| Fires when | `gem install` auto-runs the extension build | `gem install` auto-runs the extension build |
| Collects | Solana keypairs, npm/netrc/git credentials, ETH keystores, `.env` upward, private-key env vars | hostname/user/cwd/home + `/etc/passwd`, `/etc/hosts`, `/etc/resolv.conf` |
| Exfil | `webhook.site` (free lane), plain HTTP | **Burp Collaborator `oastify.com:443`, TLS** |
| Concealment | no-op `Makefile` so install prints success | no build logic at all in the extension file |
| Row origin | amazon-inspector | amazon-inspector |

The fingerprint generalizes past `extconf.rb`: **any `extensions:` declaration is a code-execution promise at install time**, and the tell is an extension file with no compiler to drive. The ledger's one-command triage probe (`gem spec NAME | grep -A3 extensions`) still applies, extended: for `mkrf_conf.rb` specifically, remember that Bundler loads it at *bundle* time on some workflows, not only at explicit install.

## What to do

1. **If `vuln-app 1.2.1` was ever installed on a host, treat host identity as disclosed.** The collector received hostname, user, cwd, home path, and full copies of `/etc/passwd`, `/etc/hosts`, `/etc/resolv.conf`. Rotate anything reachable from that host context; review SSH keys and any secrets in env files, because the recon set is exactly what targets a second stage.
2. **Grep lockfiles and build logs for `vuln-app` and for `oastify.com` destinations.** A successful `bundle install`/`gem install` of `vuln-app 1.2.1` left the connection in nothing you normally watch; outbound DNS/TLS to `*.oastify.com` from build or developer hosts is the durable tripwire.
3. **Block or alert on `*.oastify.com` and `*.interact.sh` from build infrastructure.** Legitimate developer traffic to attacker-rented OAST platforms is vanishingly rare in production pipelines; the allowlist is small enough to invert.
4. **Watch the first-GHSA clock.** The row is `aliases None` (amazon-inspector origin lands GHSA-blind, per the `kam193` per-origin law); join advisories by name+ecosystem, never by the row's alias field.
5. **Watch the re-registration tripwire:** does `vuln-app` come back (resurrection grammar), does a `1.2.2` appear, does the sibling `solana-keypair` (still `200` unyanked at this read, downloads `248`) get yanked while this one's grave stays empty.

## Durable reads

- **An `extensions:` line is a code-execution declaration.** RubyGems runs extension files at install with no reviewer in the loop; a build script that contains no build is the tell.
- **The sink tier tells you the operator tier.** `webhook.site` is a drive-by; a Burp Collaborator subdomain is paid professional tooling that hands the operator a verified victim list on every install.
- **The reference page can outlive the gem.** The row's own `rubygems.org/.../versions/1.2.1` reference served `200` while the API served `404`: quote per-lane state with its read-time before claiming any package "exists" or "is gone."

## Monitor

- Sink `g1im618xdjpuonmkxq16mr33quwlm9cx1.oastify.com` liveness per-read (quote status with read-time; sinks oscillate).
- `vuln-app` re-registration / `1.2.2` re-arm; whether the HTML reference page falls to `404`.
- First GHSA for `MAL-2026-20103` (per-origin blindness clock).
- Whether amazon-inspector mints a third RubyGems build-time row (family formation).
- KEV: no entry (`2026.11.17`/`1,782` grep `0` for `vuln-app`, `oastify`, `wuauclt`, `gguf` at read).
