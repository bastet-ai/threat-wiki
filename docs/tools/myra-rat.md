# MYRA RAT

## Summary
**MYRA** is a Linux remote-access toolkit published to npm as the package `apintergrationpost`. SafeDep's June 21, 2026 analysis describes a public package that compiles native components during installation, launches a C2 client, and bundles rootkit-style hiding, fileless execution, persistence, shell access, and live screen streaming.

The author frames the project as an authorized red-team / EDR-validation tool, but defenders should treat any unexpected installation as host compromise: the package was available from the public npm registry with runnable postinstall behavior and a default C2 configuration.

## Tags
- tools
- malware
- RAT
- Linux
- npm
- supply chain
- install-time execution
- postinstall
- native addon
- rootkit
- LD_PRELOAD
- fileless execution
- memfd
- persistence
- cron
- profile.d
- systemd-userdbd
- screen capture
- SafeDep
- apintergrationpost
- MYRA

## Why this matters
- Public package registries increasingly host complete offensive toolchains, not just simple credential stealers or downloaders.
- MYRA combines JavaScript lifecycle scripts with native Linux tooling, requiring defenders to look beyond `package.json` and ordinary Node.js process trees.
- The package asks victims to install as root and can alter `/usr/local/lib`, `/etc/profile.d`, loader paths, cron persistence, and desktop-capture tooling.
- The apparent lab / red-team framing does not reduce response priority on hosts where the package was not intentionally installed.

## npm package details
- Package: `apintergrationpost`
- Internal/tool name: `MYRA`
- Maintainer account reported by SafeDep and visible in npm metadata: `kimijohn01`
- SafeDep reported six versions, `4.0.1` through `4.0.6`, published in roughly 40 minutes on June 21, 2026.
- A registry check during this update showed additional versions through `4.1.0`, with npm `latest` set to `4.1.0` and timestamps extending to `2026-06-21T15:39:08.276Z`.
- The package name appears to misspell “api integration post,” while the internal environment variables and config keys use `MYRA`.

## Install-time behavior
- Lifecycle scripts run during install and can:
  - build native components from `native/lab-tools`;
  - require root privileges on Linux in later versions;
  - prompt use of `sudo npm install -g apintergrationpost`;
  - install operating-system packages on apt-based systems, including `build-essential`, `python3`, `ffmpeg`, `x11-utils`, and `grim`;
  - launch a detached background client after npm exits.
- SafeDep notes skip guards for CI, non-Linux platforms, local development checkout, and loopback C2 configuration; the shipped config used a non-loopback private IP address, so the autorun path could execute in a lab-like network.

## Capabilities
- C2 protocol:
  - TCP with length-prefixed JSON framing;
  - HMAC-SHA256 challenge-response authentication;
  - default token reported by SafeDep as `myra-lab-shared-key`;
  - heartbeat jitter and reconnect delay randomization;
  - optional random padding on non-auth messages.
- Operator functions:
  - interactive shell access;
  - plugin-based command dispatch;
  - multi-session server CLI;
  - live screen viewing over an HTTP viewer on port `5555`.
- Native / stealth features:
  - `libcache.so` for `LD_PRELOAD`-style file hiding;
  - `memfd_exec` / `memfd_loader` fileless execution paths;
  - process-name masquerading as `systemd-userdbd`;
  - hiding paths containing `.libcache`;
  - ptrace / injection-oriented components according to SafeDep's capability summary.
- Screen capture:
  - X11 capture through `ffmpeg` / `x11grab`;
  - Wayland capture through `grim`;
  - desktop-environment discovery through `loginctl` and process environment scraping;
  - MJPEG frame parsing and adaptive throttling.

## Persistence and artifacts
SafeDep highlights three persistence / stealth paths:

1. **Dynamic linker / preload hiding**
   - File artifact: `/usr/local/lib/.libcache.so`
   - Loader-path or preload configuration can make MYRA artifacts invisible to ordinary file enumeration.
2. **Cron relaunch wrapper**
   - File artifact: `/usr/local/lib/.cache-update.sh`
   - Cron interval: every 13 minutes.
3. **Login hook**
   - File artifact: `/etc/profile.d/.sh.local`
   - Starts the wrapper in the background for interactive shell sessions.

Additional process and service pivots:
- Process name: `systemd-userdbd --user`
- Fake binary path referenced by SafeDep: `/usr/lib/systemd/systemd-userdbd`
- C2 host / port in SafeDep's observed config: `192.168.54.1:4444`

## Defender heuristics
- Block or review any dependency on `apintergrationpost`; treat prior installs as potential compromise, especially if installed globally or with `sudo`.
- Hunt developer endpoints, CI runners, lab systems, and golden images for:
  - npm install telemetry for `apintergrationpost`;
  - files `/usr/local/lib/.libcache.so`, `/usr/local/lib/.cache-update.sh`, and `/etc/profile.d/.sh.local`;
  - cron entries invoking `.cache-update.sh` every 13 minutes;
  - unexpected `LD_PRELOAD` or loader-path changes referencing `.libcache`;
  - `systemd-userdbd --user` processes outside expected systemd paths or with unusual parentage;
  - outbound TCP to `192.168.54.1:4444` in lab or NATed environments;
  - local HTTP listeners or connections involving port `5555` tied to screen streaming.
- Review apt logs for root npm installs followed by package installation of `build-essential`, `python3`, `ffmpeg`, `x11-utils`, or `grim` when that combination is unusual.
- Preserve evidence before cleanup: collect npm logs, shell history, cron tables, `/etc/profile.d` contents, loader configuration, process command lines, memory, and network telemetry.
- Rotate credentials and secrets available to the affected account or root context; root-level npm lifecycle execution can expose SSH keys, npm tokens, cloud credentials, and local developer secrets.
- If the install was intentional red-team tooling, require written authorization, scope, hashes/package versions, and cleanup proof. Do not rely on package README language as authorization.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [Developer-tool config auto-execution](../patterns/developer-tool-config-auto-execution.md)
- [forge-jsxy npm RAT](forge-jsxy.md)
- [Mastra easy-day-js npm scope compromise](../ops/mastra-easy-day-js-npm-scope-compromise.md)

## Sources
- SafeDep: <https://safedep.io/malicious-apintergrationpost-npm-myra-rat>
- npm registry metadata: <https://registry.npmjs.org/apintergrationpost>
