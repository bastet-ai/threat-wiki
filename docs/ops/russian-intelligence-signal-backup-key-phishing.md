# Russian intelligence commercial-messaging backup-key phishing

## Summary
The FBI and CISA updated their March 2026 public warning on Russian Intelligence Services (RIS) phishing against commercial messaging applications on June 26, 2026. The campaign targets high-intelligence-value people, including current and former U.S. and international government officials, military personnel, political figures, journalists, and key officials in Ukraine.

The new operational detail is a shift from only eliciting verification codes, account PINs, or linked-device actions to also coercing victims into enabling Signal backups and pasting the **Backup Recovery Key** into an attacker-controlled chat. FBI/CISA state that the activity is publicly tracked as **UNC5792** and **UNC4221** and that RIS actors have compromised individual messaging accounts, not Signal's encryption or the application itself.

## Tags
- ops
- operations
- phishing
- Russian Intelligence Services
- FSB
- UNC5792
- UNC4221
- Signal
- commercial messaging applications
- backup recovery keys
- account takeover
- journalists
- government targeting
- Ukraine
- social engineering

## Why this matters
- End-to-end encryption is not the control being broken; the attacker is bypassing it through account takeover and cloud-backup recovery material.
- A stolen Backup Recovery Key can expose historical private and group messages, not just future messages after linked-device compromise.
- FBI/CISA warn that a shared Backup Recovery Key can remain valid even if a victim creates a new account with the same phone number. Victims must generate a new Backup Recovery Key to invalidate the old one for future backup downloads.
- The target set makes this a personal-device, executive-protection, journalism, diplomacy, military, and Ukraine-support risk, not only an enterprise messaging issue.

## Reported targeting and attribution
- FBI/CISA attribute the campaign to multiple clusters of Russian Intelligence Services cyber threat actors.
- The update specifically names Russian Federal Security Service (FSB) officers embedded with FSB Border Guards and others acting on behalf of Russian military services.
- Public tracking names in the FBI/CISA update: `UNC5792` and `UNC4221`.
- Targeting includes current and former U.S. and international government officials, military personnel, political figures, journalists, and key officials located in Ukraine.

## Tradecraft update
1. RIS actors masquerade as automated commercial-messaging-application support accounts inside the messaging app.
2. The messages claim account data is at risk, a sync issue exists, or a support/security update requires action.
3. The victim is instructed to enable backups, view the recovery key, copy it, and paste it into the chat.
4. If the key is provided, the actor can access backed-up message history and private/group messages and can take over the victim's account.
5. RIS actors continue to request verification codes and account PINs alongside the newer Backup Recovery Key lure.

## Defensive guidance
- Treat any in-app “support” message requesting Signal verification codes, PINs, linked-device actions, or Backup Recovery Keys as hostile.
- Commercial messaging support services should be expected to communicate only through official company channels, not by asking users to paste secrets in-app.
- Do not share recovery keys, 2FA codes, account PINs, or verification codes unless the request was initiated through a verified official channel and independently confirmed.
- If a Backup Recovery Key was shared, generate a new Backup Recovery Key in Signal settings to invalidate the old key for future backup downloads; assume the attacker may already have downloaded any accessible backup.
- For high-risk individuals, review linked devices, account PIN settings, backup settings, recent account-notification messages, and any unusual messages sent from the account to contacts.
- Preserve suspicious in-app messages, sender identifiers, screenshots, device-linking notifications, backup-setting changes, and timestamps before deleting evidence.
- Report suspected compromise to IC3, the local FBI field office, or CISA incident reporting channels as described in the PSA.

## Hunt and awareness pivots
- In-app messages claiming “Action Required,” “Data Recovery Needed,” “sync issue,” “restore account,” “verify account,” or “support update” and instructing the user to reveal a Signal Backup Recovery Key.
- Instructions resembling: `Settings -> Backups -> Enable Backups -> View recovery key -> Copy to clipboard` followed by a request to paste the key into chat.
- New linked-device notifications, unexpected account re-registration prompts, changed backup settings, or contacts reporting suspicious messages from the victim account.
- Targeted outreach to people with government, defense, diplomatic, journalism, Ukraine-related, or political roles.

## Related pages
- [Turla STOCKSTAY backdoor operations](turla-stockstay-backdoor-operations.md)
- [APT28 LNK SmartScreen bypass and CVE-2026-32202 coercion chain](apt28-lnk-smartscreen-cve-2026-21510-cve-2026-32202.md)
- [Microsoft Midnight Blizzard mailbox theft from Microsoft](microsoft-midnight-blizzard-mailbox-theft-from-microsoft.md)

## Sources
- FBI IC3 / CISA, June 26, 2026 update: https://www.ic3.gov/PSA/2026/PSA260626
- FBI IC3 / CISA, March 20, 2026 PSA: https://www.ic3.gov/PSA/2026/PSA260320
