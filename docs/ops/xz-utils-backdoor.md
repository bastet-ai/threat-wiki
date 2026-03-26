# XZ Utils backdoor

## Tags
- ops
- operations
- supply-chain
- Linux
- SSH
- liblzma
- build-time compromise
- CVE-2024-3094

## Summary
In March 2024, a malicious supply-chain backdoor in [XZ Utils](https://tukaani.org/xz/) was disclosed after [Andres Freund traced unusual `sshd` behavior](https://www.openwall.com/lists/oss-security/2024/03/29/4) on Debian sid to compromised upstream release artifacts. Public primary sources from [Tukaani](https://tukaani.org/xz-backdoor/), [Debian](https://lists.debian.org/debian-security-announce/2024/msg00057.html), [Fedora](https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/), and [Red Hat](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) show a release-chain compromise: malicious build logic and hidden test-file payloads were smuggled into upstream releases, then activated only on specific Linux build and runtime conditions so the resulting `liblzma` could tamper with `sshd` authentication paths.

This belongs under `Ops` because the durable value is the compromise chain, exposure window, and coordinated response. Public reporting does **not** clearly establish a verified offline identity beyond the project persona, but it does support a companion [`JiaT75`](../people/jiat75.md) people page keyed to the GitHub-linked maintainer persona tied to the release chain.

## Timeline
- **2024-02-01:** [Debian](https://lists.debian.org/debian-security-announce/2024/msg00057.html) later said compromised `xz-utils` packages entered its testing, unstable, and experimental suites starting with `5.5.1alpha-0.1`.
- **2024-02-24:** [`v5.6.0`](https://github.com/tukaani-project/xz/releases/tag/v5.6.0) was tagged and released on GitHub.
- **2024-03-09:** [`v5.6.1`](https://github.com/tukaani-project/xz/releases/tag/v5.6.1) was tagged and released on GitHub.
- **2024-03-27:** [Red Hat](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) says Andres privately notified the Debian security team after investigating `sshd` slowdowns.
- **2024-03-29:** [Andres Freund published the public disclosure](https://www.openwall.com/lists/oss-security/2024/03/29/4), [Debian issued DSA-5649-1](https://lists.debian.org/debian-security-announce/2024/msg00057.html), and [Fedora published emergency downgrade guidance for Rawhide and potentially tainted Fedora 40 pre-release systems](https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/).
- **2024-04-15:** [Fedora](https://fedoramagazine.org/cve-2024-3094-all-clear/) said the compromised package never became an official stable Fedora update and recommended a full reinstall out of caution for systems that had ever carried the tainted builds.
- **2024-04-30:** [Red Hat](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) published a multi-vendor response timeline and said RHEL and Fedora stable branches were not affected, while Fedora 40 beta nightlies had exposure.
- **2024-05-29:** [Tukaani](https://tukaani.org/xz-backdoor/) published its review notes and new clean releases.

## Org context
### Tukaani / upstream
- [Tukaani's incident page](https://tukaani.org/xz-backdoor/) says the XZ Utils `5.6.0` and `5.6.1` release tarballs contained the backdoor and that new clean releases and review notes were published on May 29, 2024.
- [Tukaani's review notes](https://tukaani.org/xz-backdoor/review.html) say multiple March 2024 changes were backdoor commits and that the main Git repository would not be rebased even though malicious history was later identified.
- The same Tukaani page ties the malicious release process to the maintainer identity `Jia Tan`; for this wiki, that is best tracked as the public maintainer persona [`JiaT75`](../people/jiat75.md) rather than as a verified offline identity claim.

### Debian
- [Debian's security advisory](https://lists.debian.org/debian-security-announce/2024/msg00057.html) says no Debian stable versions were known affected.
- The same advisory says compromised packages were present in Debian testing, unstable, and experimental from `5.5.1alpha-0.1` through `5.6.1`.
- Debian reverted the package to upstream `5.4.5`, versioned as `5.6.1+really5.4.5-1`, and urged users of affected suites to update immediately.

### Fedora and Red Hat
- [Fedora's urgent alert](https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/) says Rawhide users likely received a tainted package and Fedora 40 pre-release users may have received it through `updates-testing`, while Fedora 38 and 39 were not impacted.
- [Fedora's follow-up](https://fedoramagazine.org/cve-2024-3094-all-clear/) says the compromised package never became an official stable Fedora update and recommends reinstalling systems that had ever installed the tainted build.
- [Red Hat's response timeline](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) says the malware targeted a narrow class of `x86_64` Linux servers requiring both `systemd` and `sshd`, and that RHEL and Fedora stable branches were not affected.

## Operational chain
1. [Andres Freund's disclosure](https://www.openwall.com/lists/oss-security/2024/03/29/4) says a malicious line existed in distributed tarballs but not in the corresponding upstream Git file, causing `configure` to run an obfuscated script built from disguised test files.
2. The same disclosure says the injected script only continued on targeted builds: `x86_64` Linux, GCC, GNU `ld`, and Debian or RPM packaging environments.
3. [Andres](https://www.openwall.com/lists/oss-security/2024/03/29/4) says the modified `liblzma` used `ifunc`-related hooks and later redirected `RSA_public_decrypt` during `sshd` startup.
4. That runtime path mattered because, as [Andres explains](https://www.openwall.com/lists/oss-security/2024/03/29/4), several distributions patched OpenSSH to support `systemd` notification through `libsystemd`, which depended on `liblzma`.
5. [Red Hat](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) says the issue was then handled as a coordinated, embargoed multi-vendor response that focused on exposure validation, rollback, rebuilds, and taint assumptions for affected systems.

## Evidence and impact
- [Andres Freund](https://www.openwall.com/lists/oss-security/2024/03/29/4) says the `5.6.0` and `5.6.1` tarballs contained hidden build-time logic that was not present in the matching upstream source file.
- The same disclosure says the payload was intentionally selective, checking environment details such as `argv[0]`, `LANG`, debugging variables, architecture, and packaging context before activating.
- [Tukaani](https://tukaani.org/xz-backdoor/) says the compromise affected release tarballs `5.6.0` and `5.6.1`; [its later review notes](https://tukaani.org/xz-backdoor/review.html) identify March 2024 code changes tied to the backdoor.
- [Debian](https://lists.debian.org/debian-security-announce/2024/msg00057.html) says stable releases were not known affected, but testing, unstable, and experimental carried compromised builds.
- [Fedora](https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/) and [Red Hat](https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident) say Fedora stable and RHEL were not affected, though Fedora Rawhide and Fedora 40 pre-release systems had exposure.

## Associated people
- [JiaT75](../people/jiat75.md) - GitHub account and maintainer persona tied publicly to the XZ release chain, release signing, and March 2024 backdoor-related commit history.

## Defender takeaways
- Verify release tarballs against tagged source trees, not just signatures and release notes.
- Treat test assets, generated files, and build-time helper scripts as possible payload carriers in a supply-chain review.
- Investigate unexpected performance anomalies in trusted binaries; this incident was detected from timing and CPU oddities, not from an IOC feed.
- For tainted build roots or pre-release distro exposure, prefer rebuilds or reinstall assumptions over minimal package rollback.
- Audit downstream patches and transitive linkages; the operational path depended on distro-specific `sshd` and `systemd` integration rather than on upstream OpenSSH alone.

## Sources
- Andres Freund disclosure: https://www.openwall.com/lists/oss-security/2024/03/29/4
- Tukaani incident page: https://tukaani.org/xz-backdoor/
- Tukaani review notes: https://tukaani.org/xz-backdoor/review.html
- Debian DSA-5649-1: https://lists.debian.org/debian-security-announce/2024/msg00057.html
- Fedora urgent alert: https://fedoramagazine.org/cve-2024-3094-security-alert-f40-rawhide/
- Fedora follow-up: https://fedoramagazine.org/cve-2024-3094-all-clear/
- Red Hat response timeline: https://www.redhat.com/en/blog/understanding-red-hats-response-xz-security-incident
