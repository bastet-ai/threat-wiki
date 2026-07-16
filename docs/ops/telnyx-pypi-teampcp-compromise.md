# Telnyx PyPI TeamPCP compromise

## Summary
OX Security reported that malicious `telnyx` Python SDK releases `4.87.1` and `4.87.2` were uploaded to PyPI on March 27, 2026. OX attributed the activity to TeamPCP and described it as a follow-on to the LiteLLM PyPI compromise from earlier that week.

The durable defender lesson is that TeamPCP-style supply-chain intrusions can move quickly from one Python package to another by abusing stolen publishing credentials. Even a short-lived malicious release should be treated as endpoint and CI compromise for every environment that installed the affected package while it was available.

## Tags
- ops
- operations
- TeamPCP
- PyPI
- Python
- supply-chain
- malicious releases
- package registry
- credential theft
- developer machines
- CI/CD
- backdoor
- infostealer
- Telnyx
- LiteLLM

## Reported chain
- OX says attackers uploaded `telnyx==4.87.1` and `telnyx==4.87.2` to PyPI using compromised publishing access.
- The malicious logic was placed in `_client.py` and obfuscated with base64 in the sample OX analyzed.
- OX says the Telnyx malware was similar to the LiteLLM payload family, but used a remote download stage: it fetched an XOR-obfuscated WAV file from attacker infrastructure, decoded it, saved it as `temp.wav`, and executed the decoded payload.
- The follow-on payload targeted developer and cloud secrets, including SSH material, cloud-provider credentials, GitHub tokens, Kubernetes context, and cryptocurrency-wallet material.
- Telnyx told OX that only the Python package was compromised, that the root cause had been addressed, and that Telnyx infrastructure, networking, services, and APIs were not breached.
- A local PyPI JSON check on June 7, 2026 found no release files remaining for `4.87.1` or `4.87.2`, while `4.87.0` remained present. Treat absence from current PyPI metadata as cleanup evidence, not proof that downstream mirrors, lockfiles, or caches are clean.

## Affected package versions
- `telnyx==4.87.1`
- `telnyx==4.87.2`

OX marked `telnyx<=4.87.0` as safe relative to this incident at publication time. Environments that installed unpinned `telnyx` during the malicious-release window should assume they may have received an affected version.

## Defender heuristics
- Inventory Python environments, lockfiles, private indexes, package mirrors, container layers, and CI caches for `telnyx==4.87.1` or `telnyx==4.87.2`.
- Treat confirmed installation as code execution. Contain affected developer hosts and CI runners before rotating secrets, then rotate PyPI, GitHub, cloud, SSH, Kubernetes, API, and wallet-related credentials that were reachable from those systems.
- Hunt Python process trees for unexpected execution from `telnyx/_client.py`, remote WAV-like payload retrieval, decoded temporary files named `temp.wav`, and short-lived Python children spawned during package import or application startup.
- Compare installed `telnyx` wheels and source distributions against known-good package contents. Removed registry releases can persist in build caches and private mirrors.
- Monitor PyPI project roles, token creation, upload events, and account security changes for maintainer projects after any TeamPCP-linked package compromise.
- Correlate this with the LiteLLM and Xinference PyPI compromises: TeamPCP-family activity repeatedly uses Python package execution paths to harvest cloud, CI/CD, GitHub, Kubernetes, and developer secrets.

## Attribution notes
OX directly described the Telnyx incident as TeamPCP activity and framed it as another strike after LiteLLM. Keep the attribution tied to OX's reporting unless additional public evidence refines the operator picture. Telnyx's statement to OX narrowed the compromise to the Python package rather than Telnyx service infrastructure.

## Related pages
- [TeamPCP](../actors/teampcp.md)
- [LiteLLM compromise](litellm-compromise.md)
- [Xinference PyPI compromise](xinference-pypi-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)

## Sources
- OX Security: <https://www.ox.security/blog/telnyx-malware-teampcp-strikes-again-following-litellm-compromise/>
- PyPI project metadata: <https://pypi.org/pypi/telnyx/json>
