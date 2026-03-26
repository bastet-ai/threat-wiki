# CitrixBleed session-hijack wave

## Tags
- ops
- operations
- Citrix
- NetScaler
- CVE-2023-4966
- session hijacking
- MFA bypass
- edge appliance

## Summary
In 2023, attackers exploited `CVE-2023-4966` in Citrix NetScaler ADC and Gateway appliances to steal authenticated session cookies from appliance memory and reuse them to bypass passwords and MFA. [Citrix's October 10, 2023 security bulletin](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html), [Mandiant's October 17 remediation guidance](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/), and [CISA's November 21 advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) describe a broad exploitation wave rather than a single bespoke intrusion.

This page keeps `CitrixBleed` in the title because it became the clearest shorthand for this specific session-hijacking vulnerability wave, but the underlying official identifier is `CVE-2023-4966`. Public reporting ties exploitation to multiple actor sets, including later LockBit 3.0 affiliates, so this material belongs under `Ops`, not a single `Groups` or `People` profile.

## Naming and companion-page assessment
- [Citrix](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html) uses the official vulnerability identifiers `CVE-2023-4966` and `CVE-2023-4967` in its bulletin.
- `CitrixBleed` is the later shorthand name widely used in public reporting and in [CISA's November 21, 2023 advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a).
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) describes exploitation by multiple threat actors, and [CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) later documents LockBit 3.0 affiliate use of the same exposure path.
- No companion `Groups` or `People` page is published in this pass because the wave spans multiple actor sets rather than one stable public operator identity.

## Timeline
- **Late 2023-08:** [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) says it identified zero-day exploitation of `CVE-2023-4966` beginning in late August 2023.
- **2023-10-10:** [Citrix](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html) published bulletin `CTX579459`, disclosed `CVE-2023-4966`, and listed affected NetScaler ADC and Gateway versions.
- **2023-10-17:** [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) published remediation guidance, warning that stolen sessions could remain usable even after patch deployment.
- **2023-11-21:** [CISA, FBI, MS-ISAC, and ASD's ACSC](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) published joint advisory `AA23-325A`, saying LockBit 3.0 affiliates were exploiting `CVE-2023-4966` and that activity had been identified as early as August 2023.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### Citrix / NetScaler
- [Citrix's bulletin](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html) lists affected versions across NetScaler ADC and Gateway product lines, including EOL `12.1`.
- The same bulletin makes clear that Citrix-managed cloud services and Citrix-managed Adaptive Authentication were not affected.
- Citrix's disclosure centered on patching, but the broader public response later showed that patching alone did not fully solve the session exposure problem if cookies had already been stolen.

### Mandiant / GTIG
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) says successful exploitation allowed hijacking of existing authenticated sessions and bypass of MFA.
- The same report says Mandiant observed downstream post-exploitation including reconnaissance, credential harvesting, and lateral movement through RDP.
- Mandiant also says sessions stolen before patch deployment could still be used later, which is the operational reason the wave remained dangerous after the initial vendor bulletin.

### CISA and downstream defenders
- [CISA's advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) says LockBit 3.0 affiliates used the vulnerability to gain initial access and then move into broader ransomware activity.
- [CISA's associated malware analysis report](https://www.cisa.gov/news-events/analysis-reports/ar23-325a) shows how the follow-on activity expanded beyond appliance access into LSASS dumping, WinRM session establishment, and credential theft tooling on Windows hosts.

## Operational chain
1. Attackers sent a crafted HTTP request with a manipulated `Host` header to vulnerable NetScaler ADC or Gateway appliances, leading the appliance to return memory data containing a valid AAA session cookie, according to [CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a).
2. The attacker reused that stolen cookie to establish an authenticated session on the appliance without needing the victim's username, password, or MFA token.
3. [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) says actors then performed reconnaissance, harvested additional credentials, and pivoted laterally based on the permissions tied to the stolen session.
4. Because sessions stolen before patch deployment could remain valid afterward, organizations that only patched exposed appliances could still face downstream misuse.
5. [CISA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) later documented how at least some actors, including LockBit 3.0 affiliates, turned this access into broader Windows credential-theft and ransomware-preparation activity.

## Evidence and impact
- [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) says it observed victims in professional services, technology, and government organizations.
- [CISA's November 21 advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a) says Boeing observed LockBit 3.0 affiliates exploiting the vulnerability against Boeing Distribution Inc., and that other trusted third parties had seen similar activity.
- [CISA's malware analysis report](https://www.cisa.gov/news-events/analysis-reports/ar23-325a) shows that the wave was not limited to appliance-level access; it could lead to LSASS dumping, remote management setup, and Windows credential theft.
- The operational significance of `CitrixBleed` is that it turned a perimeter appliance bug into an MFA-bypass session-hijack path with durable downstream impact.

## Defender takeaways
- Patch quickly, but do more than patch. If `CVE-2023-4966` may have been exploited, invalidate active sessions and investigate whether stolen cookies could still be in use.
- Rotate or reassess secrets, private keys, and certificates tied to the appliance if compromise is suspected; [Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/) explicitly warns about theft of configuration secrets and keys.
- Treat appliance session theft as a possible enterprise compromise, not a contained gateway issue. The follow-on activity can include credential harvesting and lateral movement.
- Restrict management access to NetScaler appliances where possible. Edge devices with unnecessary internet exposure remain high-value zero-day targets.
- Keep actor attribution separate from exploit mechanics. Multiple actor sets used the same exposure path, so the durable page is the wave itself, not one group label.

## Sources
- [Citrix Security Bulletin CTX579459 for CVE-2023-4966 and CVE-2023-4967](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html)
- [Mandiant: Remediation for Citrix NetScaler ADC and Gateway Vulnerability (CVE-2023-4966)](https://cloud.google.com/blog/topics/threat-intelligence/remediation-netscaler-adc-gateway-cve-2023-4966/)
- [CISA: #StopRansomware - LockBit 3.0 Ransomware Affiliates Exploit CVE-2023-4966 Citrix Bleed Vulnerability](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-325a)
- [CISA: MAR-10478915-1.v1 Citrix Bleed](https://www.cisa.gov/news-events/analysis-reports/ar23-325a)
