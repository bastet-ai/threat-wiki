# Toy Ghouls "Angry Birds" custom backdoor (HiveMQ / Element)

## Summary
Kaspersky GERT / Security Services disclosed on **September 4, 2026** that **Toy Ghouls** (aka **Bearlyfy**, **Laboo.boo**, and **Feral Wolf**) — the financially motivated group targeting Russian organizations since 2025 — used a **custom backdoor for the first time** in early July 2026. Two variants were observed, both with "bird" in their agent names:

- **`mqtt-bird-agent 0.1.0`** — uses a **HiveMQ MQTT broker** as C2.
- **`matrix-bird-agent 0.1.0`** — uses an attacker-hosted **Element (Matrix)** server as C2.

The shift from the group's earlier lean on public GitHub tools and leaked Babuk/LockBit builders (and its own GenieLocker ransomware) to **custom backdoors over unconventional C2 channels** signals an effort to evade detection longer and run more sophisticated follow-on operations.

## Tags
- ops
- tooling
- campaign
- Toy Ghouls
- Bearlyfy
- Laboo.boo
- Feral Wolf
- backdoor
- MQTT
- HiveMQ
- Matrix
- Element
- WinRM
- Evil-WinRM
- custom C2
- service persistence
- ChaCha20-Poly1305
- machine-bound config
- Russia targeting
- financially motivated
- extortion

## Why this matters
- **First custom backdoor.** Previously Toy Ghouls leaned on public GitHub tooling plus leaked Babuk/LockBit builders, then its own GenieLocker. A bespoke backdoor with full device control is a capability step, not just another encryptor.
- **Unconventional C2 channels.** HiveMQ MQTT broker and a Matrix/Element homeserver are not classic C2 infrastructure; defenders hunting for HTTP long-poll / Cobalt-Strike beacons will miss both. The Element variant even runs as a Matrix *room* with a `panel-bot` operator account.
- **Machine-bound, self-sealing config.** The config `config.toml` is partially encrypted on first run with a ChaCha20-Poly1305 key derived from `HKLM\Software\Microsoft\Cryptography\MachineGuid`, binding the file to that host. The Element variant deletes the file after first run and moves config into the registry. This makes off-host forensics of the dropped config harder.
- **Service masquerading.** Persistence installs as Windows services named after plausible system components (`cplsupport` "Problem Reports Control Panel", `wtas` "Windows Telemetry Aggregator Service").

## Delivery and installation
- **Delivery:** **WinRM**, using open-source **Evil-WinRM** and **WinRM-fs** to push the backdoor and its `config.toml` to compromised systems. This is consistent with the group's known RDP/WinRM movement.
- **Run modes:** interactive command-line session **or** a Windows service.
  - `--install` / `install` — install as a system service.
  - `--uninstall` / `uninstall` — remove the service.
  - `--service` / `service` — run as a Windows service (not a default launch flag; passed as the installed service's argument).
  - HiveMQ binary presents as **`cplsupport.exe`** ("Bird Agent - MQTT server monitor"); Element binary as **`wtass.exe`** ("Matrix monitoring agent").
- **Config discovery:** looks for `config.toml` in the launch directory, then falls back to `%PROGRAMDATA%\SynapseAgent\config.toml` (Element) or `%PROGRAMDATA%\cplsupport\config.toml` (HiveMQ); full path can be forced with `-c`/`--config`.

## Config and machine binding
- Accepts plaintext or partially-encrypted `config.toml`. On first run it `seal()`s (ChaCha20-Poly1305) sensitive fields with a key derived from **`HKLM\Software\Microsoft\Cryptography\MachineGuid`**, so after the first run the config is bound to that machine and auto-decrypted on later runs. If it cannot decrypt, it stops.
- **HiveMQ encrypted fields:** `agent_privkey` (agent private key), `channel_id` (broker channel), `server_pubkey` (server public key).
- **Element version:** deletes the config file after the first run and writes the parameters to **`HKLM\Software\synapse\Config\SealedConfig`**; on later runs it reads the registry first. The config names the attacker's Element server address, a room ID, and an `access_token`; if the token is empty it prompts for a password during install, then stores the received token in the `blob` field.

## Communication
Both versions first issue `GET http://ip-api.com/json` at startup to learn the public IP and country.

### HiveMQ (MQTT) variant
- C2: the attackers' own cluster on the public **HiveMQ** broker (`broker.hivemq.com`; free tier ~100 concurrent / 10 GB·month), on port **8883**.
- `POST .../[cluster_id]/status` — `{"online":bool,"hostname":"...","timestamp":unix,"location":{"json"}}`.
- `POST .../[cluster_id]/metrics3` — periodic system metrics (`cpu_percent`, `mem_used_bytes`, `mem_total_bytes`, `disk_used_bytes`, `disk_total_bytes`, `load_1m/5m/15m`, `uptime_secs`, `hostname`, `timestamp`).
- `GET .../[cluster_id]/cmd/req` — fetch commands; server returns `{"cmd_id":int,"command":"str","timeout_secs":int}`.
- Commands executed via **`powershell.exe`** in hidden mode (`-NonInteractive -NoProfile -Command`).
- `POST .../[cluster_id]/cmd/res` — `{"stdout":"str","stderr":"str","exit_code":int,"duration_ms":int}`.

### Element (Matrix) variant
- C2: attacker-hosted **Element** server on the **Matrix** protocol at **`meet.element[.]tw`**, with a dedicated room.
- `m.bird.status` — system status (same shape as HiveMQ).
- `m.bird.metrics` — metrics with slightly different field names (`cpu_percent_x100`, `load_1m_x100`, `load_5m_x100`, `load_15m_x100`, plus mem/disk/uptime/hostname/timestamp).
- Two command types:
  - `config:set_interval` (5–3600 s) — sets the metrics interval, stored at **`HKLM\Software\SynapseAgent\metrics_interval`**.
  - Messages beginning `cmd:` — executed via the **Windows command line**; the attacker's Element account is identified as **`panel-bot`** (from the compromised host's Element SQLite databases).
- Command output returned as `m.bird.cmd_response` (mirrors the HiveMQ shape).

## Public indicators
### Binaries (MD5)
- `cplsupport.exe` — `BFADBEEE63A4F0BF19EC9DEB8FA58F58`
- `wtass.exe` — `7916C33688385525078BEE504C90F359`
- Dropped config: `config.toml`

### Kaspersky verdicts
- `HEUR:Backdoor.Win64.Suptoml.gen`
- `HEUR:Trojan.Script.Zapchast.conf`
- `Backdoor.Win64.Agent.smgdvy`
- `Trojan.Script.Zapchast.abwm`
- `Trojan.Win64.Agent.smgsfo`
- `Trojan.Script.Zapchast.abwo`

### Registry
- `HKLM\Software\synapse\Config\SealedConfig`
- `HKLM\Software\SynapseAgent\metrics_interval`

### Services
- `cplsupport` (displays "Problem Reports Control Panel")
- `wtas` (displays "Windows Telemetry Aggregator Service")

### Network / domains
- `meet.element[.]tw` — Element/Matrix C2 (attacker-hosted).
- `broker.hivemq.com` — legitimate public HiveMQ broker abused as C2 (port 8883, per-`[cluster_id]` paths).
- `ip-api.com` — legitimate IP-geo service used at startup.
- Startup `GET /json` to `ip-api.com` is a low-FP but repeatable behavioral marker.

## Detection and response
- **Hunt the channels, not just HTTP C2.** Alert on outbound MQTT to `broker.hivemq.com:8883` with per-cluster paths (`/status`, `/metrics3`, `/cmd/req`, `/cmd/res`) and on Matrix/Element protocol traffic to non-corporate homeservers (notably `meet.element[.]tw`), including `m.bird.*` event types and a `panel-bot` account.
- **Service + config forensics.** Inventory Windows services named `cplsupport` / `wtas`; check for `%PROGRAMDATA%\SynapseAgent\config.toml` or `%PROGRAMDATA%\cplsupport\config.toml`; inspect `HKLM\Software\synapse\Config\SealedConfig` and `HKLM\Software\SynapseAgent\metrics_interval`.
- **WinRM movement.** Correlate WinRM (Evil-WinRM / WinRM-fs) access with subsequent service creation and first-run `ip-api.com` lookups — the delivery vector and the first network call are a strong pair.
- **Binary matching.** Match the two MD5s; treat any `config.toml` with a partially-encrypted `blob`/`agent_privkey`/`channel_id`/`server_pubkey` structure as high-signal.
- **Remediate the access path.** Remove the service, the config blob, and the registry keys; revoke the WinRM session/credentials; rotate any credentials the PowerShell/`cmd:` command history touched; then restore from known-good media since a custom backdoor with full device control implies the host is untrusted.

## Evidence caveats
- This is the group's **first** observed custom backdoor; Kaspersky ties it to Toy Ghouls through continuity with prior TTPs (WinRM movement, Russian targeting, shift to custom tooling). The HiveMQ and Element C2 choices are operational and may rotate.
- `broker.hivemq.com` and `ip-api.com` are legitimate public resources; their mere presence is not malicious — the abuse is the per-cluster path structure and the `m.bird.*` event types layered on top.
- Machine-bound config sealing means a config file recovered from one host will not decrypt on another; analyze it in place or with the originating `MachineGuid`.

## Related pages
- [Toy Ghouls](../actors/toy-ghouls.md)
- [Toy Ghouls GenieLocker ransomware activity](toy-ghouls-genielocker-ransomware.md)
- [GenieLocker](../tools/genielocker.md)

## Sources
- Kaspersky GERT / Security Services, September 4, 2026: [Angry Birds: Toy Ghouls' new toys](https://securelist.com/toy-ghouls-new-hivemq-and-element-backdoors/121270/)
