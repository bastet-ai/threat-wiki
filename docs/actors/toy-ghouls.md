# Toy Ghouls

## Summary
**Toy Ghouls**, also known publicly as **Bearlyfy**, **Labubu**, and **Laboo.boo**, is a financially motivated extortion group targeting Russian enterprises. Kaspersky reports that it previously used third-party RedAlert, LockBit, and Babuk encryptors and adopted the custom cross-platform **GenieLocker** family in March 2026.

## Tags
- groups
- Toy Ghouls
- Bearlyfy
- Labubu
- Laboo.boo
- financially motivated
- extortion
- ransomware
- GenieLocker
- RedAlert
- LockBit
- Babuk
- Russia targeting
- manufacturing
- construction
- financial services
- retail
- technology sector
- Windows
- Linux
- ESXi
- trusted relationship abuse
- valid accounts
- OpenVPN

## Public activity profile
- Kaspersky observed GenieLocker overwhelmingly on endpoints in the Russian Federation, primarily in manufacturing, followed by construction, financial services, retail, and technology.
- A March 2026 intrusion began through OpenVPN from an external partner's network with stolen but still-valid credentials, indicating trusted-relationship abuse rather than a demonstrated software supply-chain compromise.
- Operators used SoftPerfect Network Scanner, Mimikatz, RDP, SSH, PsExec, PAExec, and reverse SSH tunneling before encrypting Windows, Linux, and ESXi systems.
- Kaspersky found no evidence of data exfiltration in the analyzed incident and says the group historically does not operate a leak site or use double extortion. Absence of evidence in one investigation is not proof that every intrusion is encryption-only.

## Defensive priorities
- Enforce phishing-resistant MFA and device or certificate restrictions on partner VPN access; alert on valid partner identities from new devices, networks, or impossible locations.
- Correlate external-partner VPN entry with network scanning, credential dumping, KeePassXC access, RDP/SSH expansion, PsExec/PAExec deployment, reverse tunnels, and backup or hypervisor service stops.
- Segment ESXi and backup management, restrict east-west administration, and maintain offline or immutable recovery copies that cannot be reached through ordinary domain or VPN credentials.

## Related pages
- [Toy Ghouls GenieLocker ransomware activity](../ops/toy-ghouls-genielocker-ransomware.md)
- [GenieLocker](../tools/genielocker.md)

## Sources
- Kaspersky, July 30, 2026: [Toy Ghouls’ new toy: the GenieLocker ransomware](https://securelist.com/genielocker-ransomware-for-windows-linux-and-esxi/120843/)
