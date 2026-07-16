# BufferZoneCorp RubyGems / Go module CI poisoning

## Summary
Socket reported a May 2026 software-supply-chain campaign tied to the GitHub account `BufferZoneCorp` and RubyGems publisher `knot-theory`. The cluster published plausible Ruby gems and Go modules that began as developer-tool impersonators or sleeper packages, then added credential theft, GitHub Actions environment tampering, fake Go wrapper path hijacking, and SSH persistence.

Treat this as a cross-ecosystem dependency-poisoning operation rather than a single malicious package family. The Ruby side abused RubyGems install-time execution through `extconf.rb`; the Go side used `init()` execution and CI-specific environment manipulation to poison later workflow steps.

## Tags
- ops
- operations
- supply-chain
- RubyGems
- Go
- GitHub
- GitHub Actions
- CI/CD
- credential-theft
- SSH persistence
- developer machines
- sleeper packages

## Why this matters
- Ruby `extconf.rb` files run during gem installation as native-extension setup, giving malicious gems an install-time execution path before advertised package functionality is used.
- Go modules can run malicious logic through `init()` during tests, builds, or helper imports, making developer workstations and CI runners exposed even without explicit command execution.
- CI manipulation was split across packages: proxy changes, `GITHUB_ENV` / `GITHUB_PATH` writes, checksum weakening, `go.sum` tampering, fake `go` wrappers, and SSH key persistence appeared in different modules across the same cluster.
- Sleeper package staging means a package can look harmless at initial publication, accumulate trust or typosquat downloads, and later receive the weaponized update.

## Reported package cluster
### Ruby gems
Socket and The Hacker News reported these Ruby gems as associated with the campaign:

- `knot-activesupport-logger`
- `knot-devise-jwt-helper`
- `knot-rack-session-store`
- `knot-rails-assets-pipeline`
- `knot-rspec-formatter-json`
- `knot-date-utils-rb` — reported as a sleeper gem
- `knot-simple-formatter` — reported as a sleeper gem

The names impersonate familiar Rails/Rack/devise/formatter utilities by adding a `knot-` prefix while preserving recognizable developer-tool semantics.

### Go modules
Reported Go modules under `github[.]com/BufferZoneCorp` included:

- `go-metrics-sdk`
- `go-weather-sdk`
- `go-retryablehttp`
- `go-stdlib-ext`
- `grpc-client`
- `net-helper`
- `config-loader`
- `log-core` — reported as a sleeper module
- `go-envconfig` — reported as a sleeper module
- `go-stdlog` — reported as public source with malicious reconnaissance logic, but not yet pushed to the Go module ecosystem at the time of Socket's writeup

These names mimic common Go library patterns and, in several cases, resemble known packages such as `go-retryablehttp` and `envconfig`.

## Tradecraft
### Ruby install-time theft
The Ruby payload path used `extconf.rb`, normally part of native-extension setup, to execute during installation. Reported collection targets included:

- environment variables whose names contain `token`, `key`, `secret`, `pass`, `aws`, `github`, `api`, or `auth`
- SSH private keys such as `~/.ssh/id_rsa` and `~/.ssh/id_ed25519`
- `~/.aws/credentials`
- `~/.npmrc`
- `~/.gem/credentials`
- `~/.netrc`
- GitHub CLI config at `~/.config/gh/hosts.yml`
- `~/.gitconfig`

Socket reported exfiltration to an attacker-controlled `webhook[.]site` endpoint, with the endpoint base64-obfuscated in at least one sample and overrideable through an environment variable named `PKG_ANALYTICS_URL`.

### Go CI poisoning and persistence
The Go side had broader workflow-tampering behavior:

- execution through Go `init()` paths
- detection of GitHub Actions markers such as `GITHUB_ENV` and `GITHUB_PATH`
- `HTTP_PROXY` / `HTTPS_PROXY` and `GOPROXY` manipulation
- checksum and dependency-resolution weakening
- `go.sum` tampering to make later dependency resolution easier to intercept
- writing a fake `go` binary wrapper into a cache directory and appending that directory to the workflow path
- forwarding to the legitimate Go binary after interception to avoid breaking the job
- developer/CI data exfiltration
- appending a hard-coded SSH public key to `~/.ssh/authorized_keys` for host persistence

## Indicators and hunt pivots
- GitHub account: `BufferZoneCorp`
- RubyGems publisher/profile: `knot-theory`
- Ruby package prefix: `knot-`
- Go import path prefix: `github[.]com/BufferZoneCorp/`
- Exfiltration infrastructure class: `webhook[.]site` endpoint reported by Socket
- Ruby execution hook: unexpected `extconf.rb` in gems that do not clearly need native-extension build logic
- Go execution hook: `init()` routines that inspect CI variables, proxies, credentials, or filesystem paths
- Persistence marker: unexpected additions to `~/.ssh/authorized_keys`
- CI path-hijack marker: cache-directory `go` wrapper appearing before the real Go binary on `PATH`

## Defender heuristics
- Treat dependency installation as code execution. Review Ruby `extconf.rb` and gemspec build hooks for packages that should be pure Ruby.
- For Go modules from new or lookalike publishers, inspect `init()` functions before importing them into CI or developer tooling.
- Monitor GitHub Actions writes to `GITHUB_ENV` and `GITHUB_PATH`, especially when a dependency rather than first-party workflow code performs them.
- Alert on build jobs changing `GOPROXY`, `HTTP_PROXY`, `HTTPS_PROXY`, `GONOSUMDB`, checksum settings, or `go.sum` unexpectedly.
- Check developer and CI hosts for unexpected `~/.ssh/authorized_keys` changes after installing the listed packages.
- Rotate credentials exposed to affected install/build environments, including GitHub, cloud, npm, RubyGems, SSH, and `.netrc` credentials.

## Attribution notes
Public reporting attributes the package cluster to the `BufferZoneCorp` GitHub account, not to a named threat group. Keep this separate from TeamPCP / Mini Shai-Hulud unless later reporting ties infrastructure, account control, or payload lineage together.

## Related pages
- [TrapDoor crypto-stealer cross-ecosystem campaign](trapdoor-crypto-stealer-cross-ecosystem.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Megalodon GitHub Actions workflow backdooring](megalodon-github-actions-workflow-backdooring.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [GitHub Actions deployment poisoning](../patterns/deployment-poisoning-github-actions.md)

## Sources
- Socket: <https://socket.dev/blog/malicious-ruby-gems-and-go-modules-steal-secrets-poison-ci>
- The Hacker News: <https://thehackernews.com/2026/05/poisoned-ruby-gems-and-go-modules.html>
