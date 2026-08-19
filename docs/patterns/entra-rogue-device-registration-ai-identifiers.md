# Entra ID rogue device registration and AI-generated identifiers

## Summary

Wiz Research (Shahar Dorfman and Sapir Federovsky, August 18, 2026) documents how AI-generated artifacts are eroding the static fingerprints defenders rely on to detect rogue device registration in **Microsoft Entra ID**. Because Conditional Access policies commonly restrict access to domain-joined devices, attackers abuse the **Device Registration Service (DRS)** — which legitimately lets users register their own devices — to enroll rogue devices under a victim's identity. The pattern is widespread: in a 90-day window, **nearly one in seven Entra ID environments** experienced at least one such attack.

Historically, device-registration tooling left consistent, atomic IOCs: User-Agent strings like `Dsreg/10.0 (Windows 10.0.19041.928)` and predictable names like `DESKTOP-XXXXXXXX`. Wiz observes that the **DESKTOP-named device-registration pattern alone affects roughly 1 in 10 of their customer base**. Attackers already evade simple checks with trivial variants such as `microsoft-XXXXXXXX`, and AI now lets them generate highly customized, benign-looking identifiers that defeat static matching entirely.

The shift: from matching tool fingerprints to **behavioral detection** — naming-convention anomaly detection on newly registered devices, and sequential correlation of device-code phishing alerts with subsequent device registration events. Wiz frames its AI-model experiments as hypothesis generators, not attribution: a generic device name or unfamiliar User-Agent cannot prove AI involvement on its own.

## Tags

- patterns
- Microsoft Entra
- device registration
- DRS
- device code phishing
- conditional access
- ROADrecon
- AI detection
- behavioral detection
- identity attack

## Why this matters

- Entra ID device joins are a fundamental persistence and access-control mechanism: a registered rogue device satisfies "joined device" Conditional Access policies and buys long-lived access to Microsoft 365 resources.
- The pre-AI detection stack (known User-Agent strings, DESKTOP-XXX name patterns, ROADrecon automation consistency) is now measurably decaying. Wiz measured 1-in-7 tenants hit in 90 days, with static patterns catching only the naive subset.
- The durable control is behavioral: device registration is rarely an isolated event, and correlating it with preceding device-code phishing collapses the search space in a way that does not depend on tool fingerprints.
- MFA at device-registration time is a strong, cheap hardening control that survives token theft, because it forces an additional challenge even when the attacker holds a DRS token.

## The default playbook

1. **Device-code phishing**: the attacker delivers a pre-generated Microsoft device code (often via a "shared document" lure) and captures the completion code the victim enters.
2. **Rogue device registration**: the resulting access registers a new device in the victim's environment, defeating joined-device Conditional Access requirements.
3. **Post-registration objectives**: access to Microsoft 365 resources, email exfiltration, persistence, or tenant expansion.

Wiz observed the same infrastructure hosting the phishing page and performing the initial sign-in after compromise — an overlap that helps identify newly deployed phishing infrastructure. A concrete example: the **AWS IP address `3.149.231.11`** appeared across device-code sign-ins associated with multiple victims, and around the same time URLScan captured a phishing page at `lockwall.xyz/prime/` using a "shared document" lure that presented victims with a pre-generated Microsoft device code. The resulting access allowed the attacker to register a new device in the victim's environment.

## Pre-AI fingerprints (and their decay)

Attackers relied heavily on **ROADrecon**, the well-known open-source Entra exploitation framework. Its automation produced consistency — defenders' favorite low-hanging fruit:

- **User-Agent**: `Dsreg/10.0 (Windows 10.0.19041.928)` and similar mimicked-legitimate strings.
- **Device name**: predictable patterns like `DESKTOP-XXXXXXXX`.

Even minor modifications defeat rigid matching — Wiz observed `microsoft-XXXXXXXX` names in the wild. AI compounds the fragility by generating customized, unpredictable, benign-looking identifiers at scale.

## AI-eroded fingerprints

Wiz's hunt asked models to analyze unusual User-Agent strings in device-registration and sign-in activity for characteristics consistent with AI-generated tooling. One string stood out: **`MSTokens-PRT/1.0.`**, which registered a device named **`Work PC`** — a plausible product name with a clean name/version structure resembling patterns previously seen in AI-generated tooling such as `Azure-Enum/1.0`.

Wiz then queried multiple models from an attacker's perspective, asking which device names would make an Azure device registration appear inconspicuous, and compared recurring suggestions against real-world telemetry. The intent was hypothesis generation, not attribution: the model outputs produced new hunting hypotheses that were validated using behavioral context (device-code authentication followed shortly by a new device registration from unusual infrastructure). This identified suspicious activity that searches for known tool fingerprints would have missed.

## Behavioral detection techniques

- **Naming-convention anomaly detection**: instead of matching specific device names, flag newly registered devices whose display names deviate from established organizational naming conventions — a pattern attackers struggle to emulate convincingly.
- **Sequential attack correlation**: correlate device-code-phishing alerts with subsequent device-registration events. Device registration is rarely isolated; evaluating the entire attack chain rather than isolated registration logs dramatically reduces the search space.

## Defender actions

- **Enroll a Conditional Access policy requiring MFA for device registration via user actions.** Even if an attacker holds a DRS token, the policy forces an additional MFA challenge before a new device can register.
- **Hunt device-code phishing first**: device-code sign-ins from unusual infrastructure, especially where the same source also hosts phishing content. The device-code event is the earlier, more reliable signal.
- **Baseline device naming conventions** per tenant (Wiz's example KQL computes the share of devices whose display name starts with `DESKTOP-`; tenants with very few DESKTOP-named devices are candidates for different baseline logic) and alert on new device registrations whose names fall outside the baseline.
- **Correlate, don't match**: build detections on the sequence (device-code auth → new device registration → M365 access) rather than on any single User-Agent or device-name value.
- **Treat AI model output as a hypothesis generator, not attribution.** A generic name or unfamiliar User-Agent is a signal, not proof. Require behavioral context (infrastructure, timing, preceding phishing) before escalating.
- Use dedicated detection rules where available; Wiz Defend's relevant rules include DESKTOP device registration by known toolkit, anomalous DESKTOP device registered in a non-DESKTOP environment, suspicious device registration attempt, and potential device-code-phishing IP-mismatch / unusual-device-code-flow alerts.

## Example KQL: identify tenant device-naming conventions

```kql
let minDevicesForBaseline = 100;
let desktopThreshold = 0.01;
let windowStart = ago(14d);
let windowEnd = now();
SigninLogs
| where ingestion_time() between (windowStart .. windowEnd)
  and ResultType == 0
  and OperationName == "Sign-in activity"
| where isnotempty(DeviceDetail["deviceId"])
| extend deviceId = tostring(DeviceDetail["deviceId"])
| extend deviceDisplayName = tostring(DeviceDetail["displayName"])
| where isnotempty(deviceDisplayName)
| extend HasMatch = deviceDisplayName startswith "DESKTOP-"
| summarize
    TotalDevices = dcount(deviceId),
    DesktopDevices = dcountif(deviceId, HasMatch == true)
| where TotalDevices >= minDevicesForBaseline
| where (todouble(DesktopDevices) / todouble(TotalDevices)) <= desktopThreshold
| project
    TotalDevices,
    DesktopDevices,
    DesktopRatio = todouble(DesktopDevices) / todouble(TotalDevices),
    IsRareDesktopTenant = true
```

## Indicators and hunting pivots

- User-Agent `MSTokens-PRT/1.0.` on device-registration events (observed with a `Work PC` device name).
- Device names deviating from organizational conventions: generic identifiers like `Work PC`, or trivial variants of expected patterns like `microsoft-XXXXXXXX` instead of `DESKTOP-XXXXXXXX`.
- Device-code sign-ins from a single source IP across multiple victims — e.g. AWS `3.149.231.11` in Wiz's example.
- Phishing page co-located with the initial sign-in infrastructure, e.g. `lockwall.xyz/prime/` with a "shared document" lure and pre-generated Microsoft device code.
- Known-tool fingerprints that still work for the naive subset: `Dsreg/10.0` User-Agent, `DESKTOP-XXXXXXXX` names, ROADrecon automation consistency.
- The sequence itself: device-code authentication followed shortly by a new device registration from unusual infrastructure.

## Open questions

- How rapidly will the static-fingerprint catch-rate decline as AI-generated identifiers become the default, and what is the current residual share of device registrations still matching ROADrecon-era patterns?
- Are the `MSTokens-PRT/1.0.` / `Work PC` artifacts tied to any specific campaign or actor, or are they commodity AI-assisted tooling across many operators?
- Does requiring MFA for device registration meaningfully reduce the 1-in-7 observed attack rate, or do attackers adapt by completing the MFA challenge against the victim?
- Will Microsoft add first-party behavioral detections for device-code-phishing-to-registration correlation, reducing dependence on third-party KQL?

## Related pages

- [TheHatman Entra tenant credential-theft and forum sale claims](../actors/thehatman.md)
- [DeBull device-code phishing and GraphSpy](../ops/debull-device-code-phishing-graphspy.md)
- [Kali365 device-code phishing expansion](../ops/kali365-device-code-phishing-expansion.md)
- [Evilginx device-code phishing and open directory enumeration](../ops/evilginx-device-code-phishing-open-directory.md)

## Sources

- Wiz Research: [Rogue Device Joins — detecting Entra ID device-registration abuse and AI-generated identifiers](https://www.wiz.io/blog/detecting-entra-device-registration-abuse) (Shahar Dorfman, Sapir Federovsky, August 18, 2026)
