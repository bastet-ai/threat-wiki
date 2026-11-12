# GSocket and gs-netcat: relay C2 that outlives the patch (Linux, Microsoft, Nov 2026)

On November 11, 2026, Microsoft published first-hand telemetry on **multiple, apparently unrelated threat actors weaponizing GSocket** (and its `gs-netcat` tool), the open-source remote-access toolkit from The Hacker's Choice, as a post-exploitation command-and-control and persistence channel on compromised **Linux servers**. The durable finding is not the tool — it is what the tool does to remediation semantics: **the relay session keeps working after the vulnerability that admitted the attacker is patched.** A single web-application compromise becomes durable access that outlasts the fix. Microsoft Defender for Endpoint telemetry shows adoption growing over recent months, concentrated on web applications and hosting environments.

This joins the wiki's growing "patched-but-owned" shelf next to the frozen-advisory and stale-mirror laws: the ledger says fixed, the host says owned.

## Why actors pick the relay model

The GSocket architecture removes the three things defender tooling is built around:

1. **No actor-owned infrastructure.** Both the victim host and the operator connect OUTBOUND to the shared public Global Socket Relay Network (GSRN), which pairs the sessions over an end-to-end encrypted channel. There is no threat-actor IP or domain to block; the relay is third-party. You can only constrain egress to the relay yourself.
2. **No inbound listener.** No public IP, no listening port, NAT is irrelevant, inbound firewall rules never see the traffic. Egress filtering and outbound monitoring are the only network-side controls.
3. **Identity by shared secret, not address.** The install generates a random secret that IS the connection identity; the operator can reconnect later from any compatible client without knowing the victim's IP, hostname, or network location. The secret can be exfiltrated at install time to the operator via console output, a temp file read before deletion, or a built-in notification channel: **Telegram (`GS_TG_TOKEN`/`GS_TG_CHATID`), Discord, or webhook**.
4. **Built-in evasion and persistence, free of charge.** The deployment script renames the process, stages in memory-backed paths, and installs reboot-surviving persistence without any custom actor development.

## The observed chain

1. **Initial access:** exploitation of internet-facing web applications (T1190); commands run as children of the web-server/application runtime (Microsoft cites an encoded RCE through a vulnerable PHP application).
2. **Deployment:** `curl` fetches the installer from `gsocket.io` (`/y` or `/install.sh`) piped to `bash` (T1059.004, T1105); the script profiles the host, selects the matching client binary (`x86_64`/`aarch64`) from `cdn.gsocket.io` or `gsgg.b-cdn.net`, and stages it in hidden writable or memory-backed paths such as `/dev/shm/.gs-0`.
3. **Secret delivery:** operator collects the secret via console/temp-file/Telegram/Discord/webhook as above.
4. **Persistence:** cron, systemd units, and shell profiles; reporting around the disclosure catalogs masquerade artifacts including `defunct.service`/`/usr/bin/defunct`/`defunct.dat`, a `systemd-remount-d` remnant, and hidden staging under `/tmp/.gsn_ora` (third-party cataloging, not Microsoft-verified names — treat artifact strings as hunt leads, not IOCs with authority).
5. **Not every intrusion runs every stage** — Microsoft explicitly cautions the chain appears partially in most cases.

## The census (Microsoft telemetry)

- **87.1%** of attributable incidents are web applications and hosting: PHP web applications + cPanel hosting `63.9%`, Apache `24.3%`.
- **Education and research** is the most-affected sector (`30.7%` of organizations), then technology/telecommunications (`22.9%`); Microsoft assesses this reflects **exposure** (large, decentralized, hard-to-patch academic web estates), not deliberate targeting.
- Multiple UNRELATED actor groups have adopted the same tool — the "shared tooling, disjoint actors" pattern the wiki has seen with the stolen-GitHub-token ecosystem (Gheist) and the Shai-Hulud brand economy. Tool convergence is not attribution.

## Detection shapes (from the post, KQL provided)

- `DeviceProcessEvents` where `FileName`/`ProcessCommandLine` has any of `gs-netcat`, `gsocket`, `gsnetcat`, `gsocket.io` (7 d window, per the published query).
- Defender signal names: `GsNetcat` hacktool prevented/blocked/detected-and-terminated detections.
- Hunt the deployment shape, not just the binary: `curl` piped to `bash` from a web-server child process; writes under `/dev/shm/.gs-*`; `GS_TG_TOKEN`/`GS_TG_CHATID` env strings in scripts; egress to GSRN relay endpoints.
- **The remediation law this page exists for:** for any patched web-app compromise on Linux, investigation must check GSocket deployment, persistence, privilege escalation, and outbound relay connections BEFORE closing the incident as "vulnerability remediated." Patching the entry point is not incident closure while a relay session is dialing out.

## Where this sits on the wiki

The GSRN model is the infrastructure-side mirror of this wiki's dead-drop resolver family: where Shai-Hulud's commit-search C2 made the resolver someone else's public service (GitHub), GSocket makes the CHANNEL itself someone else's public service. Address-blocking dies in both cases; the response moves to behavior (egress policy, process lineage, secret-rotation discipline) exactly as the ARTEX/identity-plane lesson said: hunt behavior, not IOC.

## Watch items

- Whether hosting/CPNel providers publish relay-egress guidance (the egress-filter control is the only network-side one).
- Whether GSRN itself changes policy under abuse pressure (a shared relay dying is a one-night migration event for every actor using it — watch for tool-rotation waves).
- Follow-on Microsoft campaign detail: the post is tool-level, actor-attribution is explicitly absent; name-level reporting would let this fold into a groups page.

## Sources

- Microsoft Security Blog, "The global socket: how threat actors are weaponizing GSocket for stealthy C2" (Nov 11 2026): <https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/>
- GSocket project documentation (The Hacker's Choice): <https://github.com/hackerschoice/gsocket>
- Community IOC/artifact cataloging of the same disclosure (third-party, hunt-lead grade)
