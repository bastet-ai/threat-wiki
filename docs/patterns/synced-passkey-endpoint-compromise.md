# Synced passkey theft after endpoint compromise

## Summary

Unit 42 disclosed three **Pass-ta-key** attack classes on 2026-08-03 against Google Password Manager's synced-passkey architecture in Chrome on Windows systems with a Trusted Platform Module (TPM). In the research scenarios, malware already running as the signed-in user could enumerate synced credentials, impersonate the device, replace the user-verification key during re-onboarding, or recover the security domain secret that protects all synced passkeys.

This research does not break WebAuthn cryptography and does not make passkeys weaker than passwords in general. It shows that synced passkeys inherit the security of the endpoint, credential-manager onboarding and recovery flows, device-key registration, relying-party verification, and master-key lifecycle. Hardware binding and a cloud enclave raise the cost of theft, but they do not compensate for a compromised client that can invoke device cryptography, manipulate local state, or read browser memory.

## Tags
- patterns
- passkeys
- passwordless authentication
- WebAuthn
- FIDO2
- Google Password Manager
- Google Chrome
- Google Cloud Authenticator
- Windows
- TPM
- endpoint compromise
- credential theft
- account takeover
- user verification
- device identity
- recovery flow
- browser memory
- Pass-ta-key
- Silver Pass-ta-key
- Golden Pass-ta-key
- Unit 42

## Scope and prerequisites

Unit 42 tested **Google Password Manager in Chrome on Windows with a TPM**. The cloud-authenticator design pattern exists more broadly, but the publication does not establish that every browser, operating system, or synced-passkey provider is vulnerable to these exact paths.

All three attacks require malware to be present on the victim endpoint during the initial stage. They are post-compromise techniques, not remote attacks against an uncompromised passkey user. The malware can run as a standard user in the demonstrated flows; Unit 42 says elevation, device unlock, biometrics, and contemporaneous user interaction are not required for the basic attack.

Chrome stores proto-encoded `WebauthnCredentialSpecifics` records under:

```text
%LocalAppData%\Google\Chrome\User Data\<Profile>\Sync Data\LevelDB
```

Those records let same-user malware enumerate relying parties, usernames, credential identifiers, and encrypted private-key material. Local visibility is enough to select valuable accounts even before the malware defeats protection of the private keys.

## The three attack classes

### Pass-ta-key: device-identity impersonation

Chrome stores a TPM-wrapped device identity blob as `wrapped_identity_private_key` in `passkey_enclave_state`. Unit 42 found that same-user malware could copy that blob and invoke normal Windows CNG operations (`NCryptOpenStorageProvider`, `NCryptImportKey`, and `NCryptSignHash`) to obtain signatures from the victim's TPM without unlocking the device.

The attacker can start a passkey login remotely, receive the relying party's challenge, open a WebSocket session to Google Cloud Authenticator, and have malware on the victim endpoint sign the handshake and assertion request. The cloud authenticator sees a valid device-identity signature and returns a valid assertion.

The resulting assertion has the WebAuthn **User Verified (UV)** flag unset. The attack therefore succeeds where the relying party treats `userVerification` as preferred or fails to validate the UV bit. Unit 42 demonstrated the latter condition against eBay before disclosure; the publication says eBay fixed its UV-validation gap. Unit 42 also reports that GitHub correctly rejected the same attack when UV was required.

### Silver Pass-ta-key: attacker-controlled verification key

The Silver variant turns a one-time endpoint foothold into reusable access that no longer requires the victim device during later authentication:

1. Same-user malware signs a `device/forget` request with the legitimate device identity, or deletes `passkey_enclave_state` locally.
2. Chrome must re-onboard the device the next time the user invokes a passkey.
3. During first-use recovery, Chrome registers the device in a temporary `uv_key_pending` state after the user enters the Google Password Manager recovery PIN; creation of the Windows Hello-gated UV key is deferred until a later passkey use.
4. The attacker submits `device/add_uv_key` with a public key generated in the attacker's environment.
5. Unit 42 found that the cloud authenticator did not validate attestation for the newly registered UV key. Assertions signed by the attacker's key were then returned with the UV flag set.

This path can satisfy relying parties that correctly require and validate user verification. Re-enrolling or unregistering the affected device can invalidate the Silver path, but responders must first preserve evidence and contain the endpoint that manipulated enrollment.

### Golden Pass-ta-key: security domain secret extraction

Google Password Manager encrypts synced passkey private keys under a 32-byte master key called the **security domain secret (SDS)**. Unit 42 found that Chrome retrieved the SDS during device join or recovery and exposed it to the client:

- The SDS originally appeared in plaintext in `chrome://device-log/FIDO`. Google removed it from that logging output after Unit 42's report.
- Unit 42 says the SDS still transits Chrome and is temporarily available in Chrome process memory during re-onboarding.

Malware can force re-onboarding, watch for recreation or modification of `passkey_enclave_state`, dump Chrome memory, extract the SDS, and decrypt the `WebauthnCredentialSpecifics` records. The recovered private keys can then sign challenges from the attacker's own environment with no continued access to the victim endpoint.

The SDS protects both existing and future synced passkeys for the account. Unit 42 reports that Google's current implementation has no SDS rotation or revocation path. Removing one device is therefore not sufficient evidence that Golden-variant access has been eliminated.

## Defender guidance

### Relying parties

- Set WebAuthn `userVerification` to `required` for sensitive authentication and validate the UV flag server-side on every assertion. Requesting verification without checking the returned flag is not enforcement.
- Monitor passkey use from a new device, browser profile, network, geography, or risk context, especially after a recovery or device-registration event.
- Do not assume synchronized credentials have useful clone-detection counters. Unit 42 notes that synced passkey assertions commonly use a constant `signCount`, limiting a relying party's ability to identify copied credentials.
- Provide a way to revoke every passkey associated with an account and require fresh, supervised enrollment after confirmed credential-manager master-key theft.

### Endpoint, browser, and identity teams

- Treat browser and endpoint compromise as an authentication-system compromise when the user has synced passkeys. Passkey deployment does not remove the need for EDR, application control, browser hardening, and credential-access detections.
- Restrict untrusted processes from reading Chrome profile state or other process memory. Alert on suspicious access to Chrome LevelDB synchronization data, `passkey_enclave_state`, browser memory, and Windows CNG key-import or signing operations.
- Investigate unexpected deletion, recreation, or modification of `passkey_enclave_state`, repeated credential-manager onboarding, and recovery-PIN prompts outside a planned device setup.
- Correlate passkey recovery, device forget/add events, UV-key registration, browser-profile changes, endpoint malware telemetry, and subsequent access to high-value applications.
- Require stronger verification before re-establishing device trust. Credential managers should validate origin and hardware attestation for identity and UV keys rather than accepting arbitrary replacement keys.
- Keep master keys inside the protected service or enclave. Do not expose them through client logs or browser memory when the service can perform the required operation on the client's behalf.

### Incident response

1. Isolate the endpoint and preserve volatile browser memory, Chrome profile data, `passkey_enclave_state`, synchronization databases, browser logs, process telemetry, and identity-provider audit records before cleanup where feasible.
2. Determine whether the activity was limited to device-identity signing, progressed through UV-key replacement, or exposed the SDS. The containment scope differs materially.
3. Revoke sessions, remove unfamiliar passkeys and device registrations, and re-enroll affected devices through a known-clean and supervised path.
4. If SDS extraction cannot be ruled out, do not rely only on device removal. Remove and replace synced passkeys across relying parties, monitor for reuse, and consider moving high-value identities to independently managed hardware security keys until the credential set is rebuilt.
5. Rotate other credentials reachable from the compromised browser and user context, including cookies, recovery codes, OAuth grants, passwords, API tokens, wallet secrets, and cloud or source-control credentials.

## Evidence and status caveats

Unit 42 presents controlled security research, not evidence of in-the-wild exploitation. The report does not assign CVEs or publish a general affected-version range. It says all exploits were responsibly disclosed, identifies eBay's UV-validation issue as fixed, and says Google removed SDS exposure from Chrome's FIDO device log. The publication also states that SDS memory exposure and the absence of SDS rotation or revocation remain in the current implementation.

Do not describe every passkey as exportable or every synced-passkey provider as affected. Preserve the tested scope, the local-malware prerequisite, the distinction between each variant, and the difference between a fixed logging leak and continuing browser-memory exposure.

## Related pages

- [O-UNC-066 Entra passkey vishing](../ops/o-unc-066-entra-passkey-vishing.md)
- [Browser-based developer IDE OAuth token theft](browser-based-developer-ide-oauth-token-theft.md)
- [AI browser-extension confused deputy](ai-browser-extension-confused-deputy.md)
- [ModHeader browser-extension surveillance](../ops/modheader-browser-extension-surveillance.md)

## Sources

- Unit 42, “Pass the Passkey: A Novel Attack Surface in Passwordless Authentication,” 2026-08-03: [https://unit42.paloaltonetworks.com/passwordless-authentication-security-risks/](https://unit42.paloaltonetworks.com/passwordless-authentication-security-risks/)
- W3C, “Web Authentication: An API for accessing Public Key Credentials”: [https://www.w3.org/TR/webauthn-3/](https://www.w3.org/TR/webauthn-3/)
