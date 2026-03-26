# CCleaner signed-update compromise

## Tags
- ops
- operations
- CCleaner
- Piriform
- signed updates
- ShadowPad
- TeamViewer
- Windows

## Summary
In 2017, attackers compromised the build and signing path for Piriform's Windows cleanup utility `CCleaner`, causing official signed releases from the vendor's own download infrastructure to carry a staged backdoor. [CCleaner's September 17, 2017 security notification](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184), [Cisco Talos' analysis](https://blog.talosintelligence.com/avast-distributes-malware/), and later [Avast investigation updates](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer) show a classic trusted-update compromise: attacker access inside Piriform predated release, the malicious binary was signed with a valid Piriform certificate, and a much smaller set of downstream systems was selected for second-stage targeting out of a much larger installed base.

This page uses the descriptive title `CCleaner signed-update compromise` because that is the clearest victim- and maintainer-side description of what happened. Later reporting discussed possible links to `Axiom`, `APT17`, or ShadowPad-associated tradecraft, but those are attribution hypotheses and tooling overlaps rather than the most durable name for the operation itself.

## Naming and companion-page assessment
- [CCleaner's official notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) describes the issue as compromised `CCleaner` and `CCleaner Cloud` releases for 32-bit Windows users.
- [Cisco Talos](https://blog.talosintelligence.com/avast-distributes-malware/) framed the event as a supply-chain attack abusing the trust relationship between Piriform and CCleaner users.
- [Avast's later investigation](https://blog.avast.com/avast-threat-labs-analysis-of-ccleaner-incident) discussed code similarities to `APT17` / `Aurora` malware and later [identified ShadowPad](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities) inside the Piriform network, but those reports stop short of giving a clean firsthand operator name.
- No companion `Groups` or `People` page is published in this pass. The supply-chain compromise is strongly sourced; the actor identity remains investigative and vendor-attributed rather than settled.

## Timeline
- **2017-03-11:** [Avast](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer) says the attackers first accessed Piriform's network on March 11, 2017 through TeamViewer on a developer workstation.
- **2017-03-12:** Avast says the attackers moved laterally to a second computer and deployed an older version of the later second-stage malware.
- **2017-04-12:** [Avast's March 2018 update](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities) says ShadowPad was installed on four Piriform computers, including a build server, on April 12, 2017.
- **2017-08-15:** [CCleaner's notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) and [Talos](https://blog.talosintelligence.com/avast-distributes-malware/) say the affected `CCleaner v5.33.6162` release went live on August 15, 2017.
- **2017-08-24:** CCleaner says the affected `CCleaner Cloud v1.07.3191` release went live on August 24, 2017.
- **2017-09-12:** [CCleaner's notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) says Avast determined on September 12 that the 32-bit `CCleaner` and `CCleaner Cloud` releases had been compromised; [Avast](https://blog.avast.com/update-to-the-ccleaner-5.33.6162-security-incident) says Morphisec notified it that morning.
- **2017-09-13:** [Talos](https://blog.talosintelligence.com/avast-distributes-malware/) says it identified the malicious installer during customer beta testing and notified Avast.
- **2017-09-15:** [CCleaner's notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) and [Avast](https://blog.avast.com/update-to-the-ccleaner-5.33.6162-security-incident) say the C2 server was taken down with law-enforcement support on September 15.
- **2017-09-17 to 2017-09-18:** CCleaner and Avast publicly disclosed the incident and pushed users toward clean versions.
- **2017-09-20:** [Talos](https://blog.talosintelligence.com/2017/09/ccleaner-c2-concern.html) said over 700,000 machines had reported to the C2 server and that more than 20 had received the second-stage payload.
- **2018-03-08:** [Avast](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities) published continued investigation results, including ShadowPad activity inside the Piriform network and evidence that just 40 PCs received the second-stage payload.
- **2018-04-18:** [Avast](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer) published the reconstructed intrusion path into Piriform, including the initial TeamViewer access and later movement to the build environment.

## Org context
Because there is no standalone `Orgs` section in the current taxonomy, the key organizations are summarized here.

### Piriform / Avast / CCleaner
- [CCleaner's official notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) says the incident affected the 32-bit version of `CCleaner v5.33.6162` and `CCleaner Cloud v1.07.3191`, not other products.
- The same notice says an estimated **2.27 million** people used the affected software.
- [Avast](https://blog.avast.com/update-to-the-ccleaner-5.33.6162-security-incident) says Piriform was likely already compromised before Avast acquired it on July 18, 2017, and later says Avast migrated Piriform's build environment into Avast infrastructure as part of remediation.

### Cisco Talos
- [Talos](https://blog.talosintelligence.com/avast-distributes-malware/) says the trojanized installer was still being hosted on CCleaner's download server as recently as September 11, 2017.
- The same report says the malicious `CCleaner 5.33` binary was signed with a valid `Piriform Ltd` certificate, indicating compromise of part of the development or signing process.
- [Talos' follow-up](https://blog.talosintelligence.com/2017/09/ccleaner-c2-concern.html) used C2 data to show that a much smaller, more targeted second-stage delivery had occurred inside the broader distribution event.

### Public investigative follow-up
- [Avast's September 2017 follow-up](https://blog.avast.com/additional-information-regarding-the-recent-ccleaner-apt-security-incident) says analysis of the C2 server showed an APT-style operation targeting specific high-tech and telecommunications companies.
- [Avast's March 2018 update](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities) says the first-stage malware collected non-sensitive reconnaissance and that only 40 PCs received the second-stage downloader.

## Operational chain
1. The attackers first gained access to Piriform's internal network in March 2017, using a developer workstation's TeamViewer access path and then moving laterally, according to [Avast](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer).
2. By April 2017, ShadowPad-linked activity had reached multiple Piriform systems, including a build server, showing the compromise had become an internal development-environment problem rather than just a single workstation issue.
3. The operators inserted malicious code into the 32-bit `CCleaner` executable distributed inside the legitimate installer and signed it with Piriform's valid certificate, as described by [Talos](https://blog.talosintelligence.com/avast-distributes-malware/).
4. The first-stage malware collected system metadata and beaconed to attacker infrastructure; [CCleaner's notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) says the transmitted data included computer name, IP address, installed software, active software, and network adapters.
5. A much smaller subset of victims then received the second-stage payload. [Talos](https://blog.talosintelligence.com/2017/09/ccleaner-c2-concern.html) said more than 20 machines had received it by September 20, 2017, while [Avast](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities) later said 40 PCs were selected in total.
6. Once defenders took down the C2 and sinkholed fallback domains, the attacker lost the ability to continue the staged delivery chain at scale.

## Evidence and impact
- [CCleaner's notice](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184) and [Avast](https://blog.avast.com/update-to-the-ccleaner-5.33.6162-security-incident) put the exposed first-stage user population at about **2.27 million**.
- [Talos](https://blog.talosintelligence.com/2017/09/ccleaner-c2-concern.html) said the C2 database contained over **700,000** reporting machines and that the target list changed over time, reinforcing that the operation was selective after the initial mass distribution.
- [Avast](https://blog.avast.com/additional-information-regarding-the-recent-ccleaner-apt-security-incident) said the second-stage targeting focused on specific high-tech and telecommunications companies.
- The operation matters as more than just a downloader incident: [Talos](https://blog.talosintelligence.com/avast-distributes-malware/) showed a legitimate signed vendor build was weaponized, and [Avast](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer) later showed the attackers had maintained a foothold in Piriform's internal network for months before public discovery.

## Defender takeaways
- Treat software build, signing, and remote-admin tooling as one attack surface. In the CCleaner case, compromise of internal access paths eventually reached trusted release infrastructure.
- Signed binaries from trusted vendors still need scrutiny during incident response. A valid code-signing certificate did not make the affected CCleaner release safe.
- Distinguish between mass exposure and true follow-on targeting. Millions received the first stage, but the attacker used that foothold to select a much smaller second-stage victim set.
- When trusted software is found to be backdoored, remove the affected release, rotate related trust material, and rebuild the release environment rather than assuming a point fix is enough.
- Keep attribution caveats explicit. The operational chain is well sourced; the exact threat-actor label remains less stable than the supply-chain mechanics.

## Sources
- [CCleaner Security Notification for v5.33.6162 and Cloud v1.07.3191](https://community.ccleaner.com/t/security-notification-for-ccleaner-v5-33-6162-and-ccleaner-cloud-v1-07-3191-for-32-bit-windows-users/64184)
- [Cisco Talos: CCleanup: A Vast Number of Machines at Risk](https://blog.talosintelligence.com/avast-distributes-malware/)
- [Cisco Talos: CCleaner Command and Control Causes Concern](https://blog.talosintelligence.com/2017/09/ccleaner-c2-concern.html)
- [Avast: Update to the CCleaner 5.33.6162 Security Incident](https://blog.avast.com/update-to-the-ccleaner-5.33.6162-security-incident)
- [Avast: Additional information regarding the recent CCleaner APT security incident](https://blog.avast.com/additional-information-regarding-the-recent-ccleaner-apt-security-incident)
- [Avast: New investigations into the CCleaner incident point to a possible third stage that had keylogger capacities](https://blog.avast.com/new-investigations-in-ccleaner-incident-point-to-a-possible-third-stage-that-had-keylogger-capacities)
- [Avast: Recent findings from CCleaner APT investigation reveal that attackers entered the Piriform network via TeamViewer](https://blog.avast.com/update-ccleaner-attackers-entered-via-teamviewer)
