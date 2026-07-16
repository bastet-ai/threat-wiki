# Operation Highland Velvet Ant authentication-stack backdoors

## Summary
Sygnia reported **Operation Highland** in June 2026: a long-running **Velvet Ant** intrusion in which forensic artifacts dated activity in an internal, non-internet-connected network back to 2016. Sygnia describes Velvet Ant as a China-nexus actor that reached the segregated environment by staging through internet-facing systems, traversed the IT network, and then replaced Linux authentication components with backdoored `pam_unix.so` and OpenSSH binaries.

Track this as an operation because the durable lesson is bigger than one malware family: when the authentication stack is modified, password resets and session cleanup do not restore trust until defenders verify and replace the login components themselves.

## Tags
- ops
- operations
- Velvet Ant
- Operation Highland
- China-nexus
- espionage
- Linux
- PAM
- OpenSSH
- authentication stack
- credential theft
- keylogging
- GS-Netcat
- SOCKS5
- Nginx
- FastCGI
- critical infrastructure
- segmented networks
- persistence
- threat hunting

## Why this matters
- Sygnia says the earliest artifacts in the investigated environment dated to 2016, showing nearly a decade of undetected presence.
- The target network had no direct internet connectivity; the actor staged through internet-facing systems and traversed internal paths to reach critical infrastructure.
- Velvet Ant replaced PAM modules and OpenSSH binaries across multiple hosts, giving the actor control over credential validation, credential capture, keylogging, and hidden access.
- Sygnia identified nine distinct `pam_unix.so` variants built in separate compile environments, suggesting deliberate maintenance rather than a one-off implant.
- Remediation is high-risk: replacing live authentication components incorrectly can lock responders out, but leaving them in place means new credentials may be captured immediately.

## Reported chain

### Staging into a segmented environment
- Sygnia frames Operation Highland as an escalation pattern: when detected, Velvet Ant pivots into less-monitored infrastructure and rebuilds persistence from a new vantage point.
- The actor used internet-facing systems as the first bridge, then moved through the IT network toward the segmented environment.
- Sygnia describes GS-Netcat for covert command execution and SOCKS5 proxying for tunneling and lateral movement.
- Nginx and FastCGI abuse became part of the internal execution path during movement toward the critical infrastructure network.

### Authentication-stack compromise
- Velvet Ant replaced `pam_unix.so` on multiple hosts with backdoored variants.
- Sygnia reports two core PAM outcomes: bypass access with a secret password and capture of legitimate usernames and passwords during normal login.
- The actor also modified OpenSSH binaries to log credentials and commands typed during sessions.
- Sygnia notes that the modified SSH binaries included a custom flag to disable their own credential logging, indicating live operational control over forensic noise.
- `authorized_keys` abuse provided additional durable access alongside the modified login components.

## Defender heuristics
- Treat unexplained changes to `/lib*/security/pam_unix.so`, `sshd`, `ssh`, PAM policy files, and SSH server binaries as high-severity compromise signals, especially on administrative jump hosts and segmented-network bridges.
- Compare PAM and OpenSSH binaries against vendor package checksums, known-good golden images, or freshly rebuilt hosts; do not rely only on EDR signatures.
- Preserve copies and hashes of suspicious authentication components before replacement so responders can determine whether credentials were captured and whether variants differ across hosts.
- Rotate passwords and SSH keys only after the backdoored login path has been removed or isolated; otherwise the new credentials may be stolen by the same modified stack.
- Hunt for GS-Netcat, unexpected SOCKS5 tunnels, Nginx / FastCGI execution paths, and web servers acting as command relays between internet-facing and segmented networks.
- Review `authorized_keys`, SSH daemon configs, PAM configs, package-manager integrity output, file modification times, and shell histories across bastion, administration, and critical-infrastructure management hosts.
- Stage authentication-stack replacement in a lab or out-of-band console workflow before touching production systems, because a broken PAM or SSH replacement can remove responder access.

## Attribution notes
- Sygnia tracks the actor as **Velvet Ant** and describes it as China-nexus.
- Sygnia links Operation Highland to a broader Velvet Ant pattern that includes prior abuse of F5 BIG-IP appliances and 2024 exploitation of Cisco NX-OS CVE-2024-20399 to deploy VELVETSHELL on Cisco Nexus switches.
- Keep this page scoped to Sygnia's Operation Highland findings unless other primary sources add corroborated victimology, tooling, or aliasing.

## Related pages
- [Velvet Ant](../actors/velvet-ant.md)
- [JDY SOHO / IoT reconnaissance botnet](jdy-soho-iot-recon-botnet.md)
- [VerdantBamboo appliance BRICKSTORM operation](verdantbamboo-appliance-brickstorm-operation.md)

## Sources
- Sygnia: <https://www.sygnia.co/blog/operation-highland-velvet-ant/>
- The Hacker News summary: <https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html>
