# JiaT75

## Tags
- people
- GitHub
- maintainer persona
- supply-chain
- xz
- CVE-2024-3094

## Summary
`JiaT75` is the GitHub account and public project persona tied publicly to the XZ Utils backdoor operation. Public sources link this account to the display name `Jia Tan`, XZ maintainer activity, signed release artifacts, and March 2024 commits that Tukaani later identified as backdoor-related. This page documents the public maintainer persona and account activity, not a verified offline identity beyond public account metadata and project sources.

## Publicly supported identity
- The GitHub profile [`JiaT75`](https://github.com/JiaT75) presents the handle `JiaT75` with the display name `Jia Tan`.
- [Tukaani's incident page](https://tukaani.org/xz-backdoor/) says the compromised `5.6.0` and `5.6.1` release tarballs were created and signed by `Jia Tan`.
- The same Tukaani page says `Jia Tan` had access to GitHub-hosted project assets and that forwarding to `xz@tukaani.org` was disabled on 2024-03-30.

## Operational relevance
- The XZ GitHub commit view filtered to [`author=JiaT75`](https://github.com/tukaani-project/xz/commits?author=JiaT75) shows March 2024 maintainer activity tied to the release window and later review scope.
- [Tukaani's review notes](https://tukaani.org/xz-backdoor/review.html) identify the 2024-03-09 commit `liblzma: Fix false Valgrind error report with GCC.` as a backdoor commit and classify several nearby March 2024 changes as related malicious history.
- [Tukaani's old releases page](https://tukaani.org/xz/old.html) says Jia Tan was a co-maintainer in 2022-2024 and says "he and the team behind him inserted the backdoor" into XZ Utils 5.6.0 and 5.6.1.

## Timeline
- **2022-2024:** [Tukaani's old releases page](https://tukaani.org/xz/old.html) says Jia Tan was a co-maintainer during this period.
- **2023-05-04 to 2024-01-26:** [Tukaani's review notes](https://tukaani.org/xz-backdoor/review.html) say release tarballs during this span were created and signed by Jia Tan but were reviewed as safe.
- **2024-03-04:** The GitHub author view for [`JiaT75`](https://github.com/tukaani-project/xz/commits?author=JiaT75) shows ifunc-related maintainer commits during the later-reviewed window.
- **2024-03-09:** The same author view shows several commits on the `v5.6.1` release day, including changes Tukaani later tied to the backdoor.
- **2024-03-25:** The same author view shows the `Docs: Simplify SECURITY.md.` commit.
- **2024-03-30:** [Tukaani's incident page](https://tukaani.org/xz-backdoor/) says the GitHub account was suspended and mail forwarding to `xz@tukaani.org` was disabled.

## Scope notes
- This page uses the GitHub username because that is the clearest public identifier supported by the available sources.
- Public sources also use the display name `Jia Tan`, but this wiki does not treat that alone as proof of a verified offline identity beyond the project persona and account metadata.

## Associated operations
- [XZ Utils backdoor](../ops/xz-utils-backdoor.md)

## Sources
- GitHub profile: https://github.com/JiaT75
- GitHub commit history filtered to `JiaT75`: https://github.com/tukaani-project/xz/commits?author=JiaT75
- Tukaani incident page: https://tukaani.org/xz-backdoor/
- Tukaani review notes: https://tukaani.org/xz-backdoor/review.html
- Tukaani old releases page: https://tukaani.org/xz/old.html
