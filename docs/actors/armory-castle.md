# Armory Castle

## Summary
Armory Castle is Google Threat Intelligence Group's tracking name for a suspected China-nexus espionage actor, formerly reported as **UNC5221** and also known as **Warp Panda** (per secondary coverage of the same GTIG/Mandiant reporting). The cluster name overlaps the ledger's [VerdantBamboo](verdantbamboo.md) profile, which Volexity maps to WARP PANDA / UNC5221 and which specializes in long-dwell compromise of edge and appliance systems where EDR coverage is thin. Armory Castle's defining observed operation, published by Mandiant `2026-11-20`, is the exploitation of VMware vCenter from inside an already-breached network using a custom toolchain that steals the identity backbone of a vSphere estate.

## Reported operations and tradecraft

### vCenter takeover via CVE-2026-123890 (early September 2026, published Nov-20)
- Initial access reported through a BeyondTrust Remote Support zero-day (`CVE-2026-102764`, per Mandiant summary quoted by secondary coverage), then a pivot to Linux appliances with no EDR, planting web shells (secondary coverage names `SLIMSAVAGE`) and gaining root.
- Internal recon with `nmap` on VMware-specific ports `9080`, `5480`, `2012` - port `2012` is the vCenter SSO control-plane DCE/RPC interface and the exploitation lane for `CVE-2026-123890`.
- `CVE-2026-123890` (KEV'd `2026-11-20`, NVD `9.8`): unauthenticated SRP-6a session-key disclosure in the `vmdir` `rpc_srp_verifier` interface caused by predictable UUIDv1 timestamp generation; the leaked session key mints an authenticated session as `administrator@vsphere.local`.
- **BONESAW** (Mandiant name; a Golang remote-exploitation utility, observed dropped as `/tmp/123`): exploits `CVE-2026-123890` to exfiltrate the raw LMDB database (`data.mdb`) over the `vmdir` RPC interface, extract the SAML STS private RSA signing key, create a backdoor machine account, create an SSO administrator, forge administrative SAML 2.0 assertions (Golden SAML class), and assign Global Administrator on the vCenter root folder via the SOAP API. Secondary coverage names a second Golang token-forgery utility (`SAWSNAKE`).
- Post-exploitation: enable appliance SSH via the management interface, collect the vCenter master encryption key and PostgreSQL credentials, disable SSH again, then reach ESXi hosts and extract AD database files from guest VM disks.
- Timing evidence: Mandiant reports the actor exploited `CVE-2026-123890` in early September 2026, worked against vCenter already patched for the July bypass `CVE-2026-59309`, and had knowledge of the November flaw BEFORE that July disclosure = pre-zero-day tooling, two months of exploitation before Broadcom's Nov-19 fix.

## Infrastructure and targeting signature
- Target class: VMware vCenter / vSphere estates reached from within breached networks; appliance Linux hosts as staging.
- Port profile worth alerting on for networks with no legitimate vmdir exposure: inbound TCP `2012` (also scanned `9080`, `5480`).
- Tool class: single-purpose Golang utilities dropped to world-writable paths (`/tmp/123` pattern).

## Defender notes
- Patch `8.0 U3m` / `9.0.2.0200` / `9.1.1.0200`; there is NO public fix for vCenter `7.x` (EGS Oct-2025) while the tool works against 7.x/8.x = isolate or replace 7.x.
- Restrict TCP `2012` to the tightest management plane; the exploit is a single unauthenticated DCE/RPC call.
- Patch is not eviction: hunt SSO admin/machine-account creation, SAML signing-key rotation needs, `data.mdb` reads, SSH flapping on the appliance, and Golang binaries in `/tmp` across the incident window; rotate every credential the estate can mint (master key, DB creds, SAML trust, ESXi root, and any AD material reachable from VM disks).
- Pair with the ledger's vSphere hardening guidance already carried on the VerdantBamboo page: restrict VAMI/SSH, forward logs off-host, treat vCenter/ESXi logs as Tier-0 evidence.

## Related pages
- [CISA KEV November 20, 2026 page](../ops/cisa-kev-vmware-vcenter-apache-roller-sap-cisco-november-20-2026.md)
- [VerdantBamboo (overlapping cluster, WARP PANDA / UNC5221 mapping)](verdantbamboo.md)
- [VerdantBamboo appliance BRICKSTORM operation](../ops/verdantbamboo-appliance-brickstorm-operation.md)

## Sources
- Google Cloud / Mandiant, `ARMORY CASTLE Exploits vSphere` (Nov-20 2026): [https://cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-vsphere](https://cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-vsphere)
- Broadcom advisory (vCenter bundle): [https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/39495](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/39495)
- VMware VCF security advisory tracking (VMSA-2026-0009): [https://github.com/vmware/vcf-security-and-compliance-guidelines/blob/main/security-advisories/vmsa-2026-0009/README.md](https://github.com/vmware/vcf-security-and-compliance-guidelines/blob/main/security-advisories/vmsa-2026-0009/README.md)
- Secondary coverage quoted for names not in the primary post (Warp Panda, SLIMSAVAGE, SAWSNAKE, BeyondTrust initial-access chain): SecurityWeek, The Hacker News, SOCRadar
