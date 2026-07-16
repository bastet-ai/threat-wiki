# Velvet Ant

## Summary
**Velvet Ant** is a China-nexus threat actor tracked by Sygnia across multiple long-running intrusion investigations. Sygnia's June 2026 **Operation Highland** report describes a near-decade presence in an internal, non-internet-connected network where Velvet Ant replaced Linux PAM and OpenSSH components with backdoored versions for authentication bypass, credential capture, keylogging, and durable access.

This profile is intentionally sourced to Sygnia's public reporting. Use it to connect Velvet Ant's repeated preference for less-monitored infrastructure—F5 BIG-IP, Cisco Nexus, Linux authentication stacks, and segmented management paths—without merging unrelated China-nexus activity unless a primary source supports the link.

## Tags
- group
- actor
- Velvet Ant
- China-nexus
- espionage
- Operation Highland
- F5 BIG-IP
- Cisco Nexus
- CVE-2024-20399
- VELVETSHELL
- Linux
- PAM
- OpenSSH
- authentication stack
- critical infrastructure
- persistence

## Known activity

### Operation Highland authentication-stack backdoors
- Sygnia reported that forensic artifacts in the investigated environment dated Velvet Ant activity back to 2016.
- The target network had no direct internet connectivity; the actor staged through internet-facing systems and traversed internal networks to reach the segmented environment.
- Velvet Ant replaced PAM modules and OpenSSH binaries across multiple hosts, including nine distinct `pam_unix.so` variants.
- Reported capabilities included secret-password bypass, credential capture during normal logins, SSH command logging, and a custom flag to disable credential logging when desired.
- Sygnia also observed GS-Netcat, SOCKS5 tunneling, Nginx / FastCGI execution paths, and `authorized_keys` abuse in the broader intrusion path.

### Prior infrastructure-focused persistence
- Sygnia says prior Velvet Ant investigations documented abuse of F5 BIG-IP appliances and legacy Windows infrastructure for long-term persistence.
- Sygnia's 2024 reporting attributed exploitation of Cisco NX-OS **CVE-2024-20399** to Velvet Ant, with deployment of the **VELVETSHELL** hybrid backdoor on Cisco Nexus switches.
- Across the public reporting, the recurring pattern is to move into infrastructure defenders monitor less closely after exposure or containment pressure.

## Defender focus
- Include network appliances, bastions, authentication servers, and management-plane Linux systems in threat hunts; do not limit visibility to user endpoints and domain controllers.
- Verify authentication components from trusted package checksums or golden images, especially `pam_unix.so`, PAM configs, `sshd`, `ssh`, `authorized_keys`, and SSH daemon configuration.
- If Velvet Ant-style authentication tampering is suspected, remove or isolate the modified login path before rotating credentials.
- Preserve compromised binaries and logs before remediation so responders can determine which credentials, commands, and administrative paths were exposed.

## Related pages
- [Operation Highland Velvet Ant authentication-stack backdoors](../ops/operation-highland-velvet-ant-authentication-stack-backdoors.md)
- [VerdantBamboo](verdantbamboo.md)
- [JDY SOHO / IoT reconnaissance botnet](../ops/jdy-soho-iot-recon-botnet.md)

## Sources
- Sygnia: <https://www.sygnia.co/blog/operation-highland-velvet-ant/>
- Sygnia Cisco NX-OS report: <https://www.sygnia.co/blog/china-threat-group-velvet-ant-cisco-zero-day/>
- The Hacker News summary: <https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html>
