# CISA KEV November 20, 2026 (VMware vCenter, Apache Roller, SAP NetWeaver, Cisco Expressway)

## Tags
- ops
- operations
- CISA
- CISA KEV
- active exploitation
- BOD 26-04
- VMware
- vCenter
- vSphere
- vmdir
- authentication bypass
- CVE-2026-123890
- Armory Castle
- Warp Panda
- UNC5221
- Golden SAML
- BONESAW
- Apache Roller
- deserialization
- CWE-502
- CVE-2026-129448
- SAP NetWeaver
- JNDI injection
- CVE-2025-42884
- Cisco Expressway
- hard-coded credentials
- CVE-2026-76466

## Summary

CISA broke its quiet stretch on `2026-11-20` (`catalogVersion 2026.11.20`, `dateReleased 2026-11-20T17:48:39Z`, count `1,790`, up from `1,786`): **four additions, ALL with a `2026-11-23` due date** - a 72-hour BOD 26-04 window across the whole batch. The head of the list is a live espionage story published the same day by Google/Mandiant: **VMware vCenter `CVE-2026-123890`**, a VMware Directory Service authentication bypass exploited since early September 2026 by **Armory Castle** (formerly UNC5221, also known as Warp Panda). → [Armory Castle actor page](../actors/armory-castle.md)

## The four rows (this wiki re-pulled the KEV JSON directly at `≈18:5xZ` Nov-20)

### VMware vCenter Server, `CVE-2026-123890` (CWE-288, KEV due 11-23, forensic triage required)
Authentication bypass using an alternate path or channel in the VMware Directory Service (`vmdir`): an unauthenticated attacker with network access bypasses authentication and gains unauthorized access. NVD carries `9.8` CVSS 3.1 (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`, state `Received` at read). Broadcom's advisory (support doc `39495`) states **"You are affected if you are running any version of VMware vCenter"** and ships NO workaround (network restriction only). Google/Mandiant (`cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-vsphere`, published Nov-20) details the exploitation: unauthenticated **SRP-6a session-key disclosure** in the `rpc_srp_verifier` DCE/RPC interface over **TCP 2012** (predictable UUIDv1 timestamps leak the shared session key) = an authenticated session as `administrator@vsphere.local`. Fixes: `9.1.1.0200`, `9.0.2.0200`, `8.0 U3m`; the same advisory bundles four lower-severity flaws (`CVE-2026-123891`/`123892`/`123893` SDDC Manager, `CVE-2026-123894` VMware Tools for Windows SAML signature bypass, guest-alias-mapping configs only). **The `vCenter 7.x` line has NO public patch** (End of General Support Oct-2025) while Mandiant's recovered tool works against 7.x and 8.x = a 7.x appliance is a replace-or-isolate decision today, not a patch ticket.

### Apache Roller, `CVE-2026-129448` (CWE-502, KEV due 11-23, forensic triage required)
Unauthenticated remote code execution via the **XML-RPC endpoint deserializing vendor extension types BEFORE authentication**; the KEV row states this CVE covers the same underlying vulnerability as `CVE-2026-82384` but applies to a **broader range of affected versions**. NVD `9.8` (state `Deferred`), published `2026-11-17` = KEV stamp `≈3 days` after the CVE, pre-auth deserialization on a publishing platform. Vendor note: `lists.apache.org/thread/cc0jck13nb9vvcmzxzwotr6n16mx28z9`.

### SAP NetWeaver Enterprise Portal, `CVE-2025-42884` (CWE-943, KEV due 11-23)
Improper neutralization in data query logic: unauthenticated attacker discloses or modifies server information via **injected JNDI environment properties or a URL used during JNDI lookup**. NVD carries only `6.5` (`C:L/I:L/A:N`) and the CVE is dated `2025-11-11` - **a year-old CVE just KEV'd** = the backlog law re-attested: a KEV stamp on an old CVE is an alarm about NOW (recent weaponization surfaced old code), and the KEV score reality diverges sharply from NVD here. SAP Security Note bulletin reference in the row.

### Cisco Expressway Series, `CVE-2026-76466` (CWE-798, KEV due 11-23, forensic triage required)
**Hard-coded credentials**: an unauthenticated remote attacker with persistent cookies and network access can execute commands as **root** on a clustered device via the database service. NVD `9.8`, CVE published `2026-10-21` = KEV `≈1 month` later, also backlog-shaped. Cisco advisory: `cisco-sa-vcs-static-cred-hr7EWZ8t`.

## Durable reads

1. **A same-day KEV addition with a same-week Mandiant writeup is the strongest exploitation evidence tier CISA publishes.** Three of the four rows carry `forensicTriage: Yes` (the BOD 26-04 forensics obligations fire the moment you are internet-exposed on those products).
2. **The 72-hour due date (11-23) on all four rows is the triage alarm** - BOD agencies have until Sunday; private-sector equivalents should read this as CISA assessing active, broad exploitation.
3. **vCenter is identity infrastructure**: with `vmdir` taken over, SAML signing material, the master key, and every ESXi host are exposed. Treat the patch as emergency change (Broadcom's own FAQ language) and hunt for SSO administrator account creation, forged SAML token use, and unexpected appliance SSH enablement BEFORE and AFTER patching - patching does not evict an operator who already holds forged Golden SAML tokens.
4. **Second distinct vmdir auth bypass of 2026** (`CVE-2026-59309` fixed Jul-29; Mandiant evidence shows the actor knew this flaw before that disclosure and ran the tool against already-patched hosts) = the "patched for the July bypass" is NOT exoneration; version-check against the November advisory specifically.
5. KEV greps for the ledger's carried supply-chain names (`corepass`, `metagl`, `apache-httpclient`, `8.152.163.60`, `47.251.102.182`, `minhdong`, `mayx`, `string-utils-assistant`, `lyxe`, `thepayulink`, `postman-cse`) remain `0` at first read of `1,790`; **phpAfterShell and the NGINX HTTP/2 pair are still absent** from the new catalog (watches stay armed).

## Defensive checklist (vCenter lane)
- Patch `8.0 U3m` / `9.0.2.0200` / `9.1.1.0200`; cumulative updates only, Quick Patch does not apply them; isolate any `7.x` appliance (no fix exists).
- Restrict TCP `2012` (plus `9080`/`5480`, the ports the actor nmap-scanned) to the smallest management plane; the exploit lane is a single DCE/RPC endpoint.
- Hunt: new SSO administrator accounts (`vmdir` account creation), backdoor machine accounts, `data.mdb` reads, SAML signing certificate changes (rotate signing material and re-trust if touched), appliance SSH enable/disable flapping around the incident window, Golang binaries under `/tmp` (Mandiant names the exploitation utility `/tmp/123`).
- Assume post-compromise reach: Mandiant observed the actor collecting the vCenter master encryption key + database credentials and moving to ESXi hosts and guest-VM AD database files = full estate credential rotation on any exploited host.

## Related pages
- [Armory Castle actor page](../actors/armory-castle.md)
- [VerdantBamboo (Volexity cluster mapped to WARP PANDA / UNC5221)](../actors/verdantbamboo.md)
- [CISA KEV November 18, 2026 (LiteLLM, Apache Axis, REDCap, Synology)](cisa-kev-litellm-axis-redcap-synology-november-18-2026.md)
- [VMware VMSA-2026-0006 vCenter/ESXi critical flaws](vmware-vmsa-2026-0006-vcenter-esx-critical-flaws.md)

## Sources
- Google Cloud / Mandiant: Armory Castle Exploits vSphere: [https://cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-vsphere](https://cloud.google.com/blog/topics/threat-intelligence/armory-castle-exploits-vsphere)
- Broadcom security advisory (vCenter five-CVE bundle): [https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/39495](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/39495)
- CISA KEV JSON (`2026.11.20`): [https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- NVD records for all four CVEs (this wiki fetched `cvssMetricV31` per-CVE at read)
- Cisco advisory: [https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-vcs-static-cred-hr7EWZ8t](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-vcs-static-cred-hr7EWZ8t)
- Apache Roller list thread: [https://lists.apache.org/thread/cc0jck13nb9vvcmzxzwotr6n16mx28z9](https://lists.apache.org/thread/cc0jck13nb9vvcmzxzwotr6n16mx28z9)
- Secondary coverage (quotes attributed, not relied on for facts): SecurityWeek (Mandiant attribution summary, `Bonesaw`, LMDB theft, BeyondTrust `CVE-2026-102764` initial-access chain), The Hacker News, SOCRadar (SLIMSAVAGE web shells, `SAWSNAKE` SAML forgery tool naming)
