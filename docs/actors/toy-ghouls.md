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
- **September 4, 2026: first custom backdoor.** Kaspersky GERT / Security Services reported that in early July 2026 the group deployed a bespoke, two-variant backdoor ("Angry Birds") using **WinRM (Evil-WinRM / WinRM-fs)** for delivery and **unconventional C2 channels** — a **HiveMQ MQTT broker** cluster (`mqtt-bird-agent`, `cplsupport.exe`) and an attacker-hosted **Element / Matrix** server (`matrix-bird-agent`, `wtass.exe`, `meet.element[.]tw`). It persists as Windows services named `cplsupport` / `wtas` and machine-binds its `config.toml` with a ChaCha20-Poly1305 key derived from the `MachineGuid` registry value. This marks a shift from public/leaked builders (and its own GenieLocker) toward custom, hard-to-detect control tooling.

## Defensive priorities
- Enforce phishing-resistant MFA and device or certificate restrictions on partner VPN access; alert on valid partner identities from new devices, networks, or impossible locations.
- Correlate external-partner VPN entry with network scanning, credential dumping, KeePassXC access, RDP/SSH expansion, PsExec/PAExec deployment, reverse tunnels, and backup or hypervisor service stops.
- Segment ESXi and backup management, restrict east-west administration, and maintain offline or immutable recovery copies that cannot be reached through ordinary domain or VPN credentials.
- **Hunt the new backdoor channels:** outbound MQTT to `broker.hivemq.com:8883` with per-cluster `/status`/`/metrics3`/`/cmd/req`/`/cmd/res` paths, Matrix/Element traffic to non-corporate homeservers (`meet.element[.]tw`, `m.bird.*` events, `panel-bot` account), Windows services `cplsupport` / `wtas`, and WinRM sessions that precede service creation plus a first-run `ip-api.com` lookup.

## Related pages
- [Toy Ghouls GenieLocker ransomware activity](../ops/toy-ghouls-genielocker-ransomware.md)
- [Toy Ghouls "Angry Birds" custom backdoor (HiveMQ / Element)](../ops/toy-ghouls-angry-birds-hivemq-element-backdoor-september-2026.md)
- [GenieLocker](../tools/genielocker.md)

## Sources
- Kaspersky, July 30, 2026: [Toy Ghouls’ new toy: the GenieLocker ransomware](https://securelist.com/genielocker-ransomware-for-windows-linux-and-esxi/120843/)
- Kaspersky GERT / Security Services, September 4, 2026: [Angry Birds: Toy Ghouls' new toys](https://securelist.com/toy-ghouls-new-hivemq-and-element-backdoors/121270/)
