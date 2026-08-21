# Baileys / libsignal-node npm campaign: silent WhatsApp channel-follow abuse

## Summary
SafeDep (Kunal Singh) published an August 10, 2026 analysis of a campaign of npm packages that fork **Baileys**, the popular WhatsApp Web multi-device library, and use the installer's already-paired session to force the installer's own WhatsApp account to **follow channels the package author controls**. A small subset also injects the author's advertising URL into media the bot sends, forges channel attribution onto outgoing messages, or blocks the bot account outright. SafeDep frames this as **non-consensual social abuse shipped through npm — not credential theft**: the packages do not steal a static secret such as a token, they abuse the authenticated session the installer already holds.

SafeDep's continuous npm-registry monitoring records **4,250 package names containing "baileys"** and another **112 containing "libsignal-node"**, a mix of the upstream library, legitimate forks, mirrors, and unexamined packages. The post lists only confirmed-malicious packages: **70 Baileys-based package names across 343 versions, and 15 `libsignal-node` impersonators across 38 versions**. The confirmed set is a lower bound; SafeDep states the campaign "keeps growing."

## Tags
- ops
- operations
- npm
- Baileys
- libsignal-node
- WhatsApp
- malicious packages
- supply-chain
- typosquat
- social abuse
- account abuse
- forced channel follow
- adware
- self-DoS
- package fork
- paired session
- no credential theft

## Campaign mechanics
All confirmed packages act through the **installer's authenticated session** (the paired multi-device session). The differences are which action the fork performs and how the malicious code reaches that session:

- **Forced follow of an attacker channel.** `@neykoor/baileys` follows a hard-coded channel on every connection. The implant sits in `lib/Socket/newsletter.js`: it binds to `connection.update` and, when the connection is `open`, runs a fire-and-forget `executeWMexQueryIgnoreResponse` follow against `AUTO_FOLLOW_JID` (`120363401404146384@newsletter`), swallowing all errors with an empty `catch {}`. It reaches the listener at runtime because `makeWASocket` → `messages-send.js` → `makeNewsletterSocket` registers the listener.
- **Remotely controlled follow list (with mute).** `lupy4u` moves the target list off the package and onto the network. `autoJoinChannels()` in `lib/Socket/newsletter.js` fetches a JSON file from GitHub (`https://raw.githubusercontent.com/LevviCodeID/Levi4than/refs/heads/main/levvleys.json`), then for each `@newsletter` id follows the channel and mutes it (with a 3-second sleep between). Muting suppresses the notification that would reveal the new subscription to the account owner. The operator can change targets without publishing a new version.
- **Advertising URL injected into media.** `mamz-baileys` adds, on top of the forced follow, a `sourceUrl` to the preview payload of **every image and video the bot sends** (two sites in `lib/Socket/messages-send.js`). The URL is assembled from a character-code array (`String.fromCharCode(104,116,116,112,58,47,47,102,105,111,114,97,46,110,105,120,101,108,46,109,121,46,105,100,47)`) that decodes to `https://fiora.nixel.my.id/` — every other URL in the file is a plain string, so the encoding exists only to defeat text search.
- **Forged channel attribution on outgoing messages.** `@cikikomo/baileys` adds `forwardedNewsletterMessageInfo` (newsletter name "CikiKomo", JID `120363426628484388@newsletter`) to the victim's outgoing messages from `lib/Socket/luxu.js`, and sets `noSelfSync: true` at four message-send sites so the injected message is not synced back to the owner's own devices — lowering the chance the owner notices. The package advertises both the channel identifier and the `noSelfSync` flag in its own `package.json` description, i.e. the concealment targets the victim, not the buyer of the fork.
- **Account block (self-DoS) via an authorisation gate.** `@prototypevip/baileys` hides an authorisation gate in `lib/Store/prototype-store.js`. The file opens with a base64 string table and a one-line decoder; a `cloneM()` wrapper running inside the `messages.upsert` listener walks each message, finds the live multi-device socket, and checks whether it is registered under the author's own key `gintoki`. If not, it sends "you are no longer authorized to use this bot" **from the victim's account** and throws `Blocked`, halting message handling. A legitimate licence check has no reason to hide `sendMessage` behind base64.

## Confirmed malicious packages
SafeDep analysed all but one from source; `@diezyyasha/libsignal-node` was removed from npm before analysis and is reported only.

| Package | Version | Behaviour | Delivery | Verified |
| --- | --- | --- | --- | --- |
| `@prototypevip/baileys` | 0.0.4 | Account block (self-DoS) | Fork | From source |
| `@cikikomo/baileys` | 1.0.10 | Forged attribution | Fork | From source |
| `@neykoor/baileys` | 7.0.16-rc15 | Forced follow | Fork | From source |
| `mamz-baileys` | 8.6.62 | Forced follow + injected ad URL | Fork | From source |
| `lupy4u` | 4.5.6 | Remote-controlled follow + mute | Fork | From source |
| `@diezyyasha/libsignal-node` | 2.2.8 | Forced follow | Import-time patcher | Reported, removed |

Other confirmed Baileys names in the set include `@kofoffc/baileys` (0.0.3 / 0.0.4), `ynastore-baileys` (1.0.21), `santana-baileys` (2.0.4), `diezyyasha-baileys` (8.6.57 / 9.1.1 / 9.1.2), and `alipclutch-baileys` (8.6.61 / 8.6.65 / 8.6.66 / 8.6.72 / 8.6.74). The confirmed `libsignal-node` impersonators include an import-time patcher variant. The full list is in SafeDep's `baileys-packages-list.csv` appendix (70 names / 343 versions plus 15 `libsignal-node` names / 38 versions).

## Indicators of compromise
- **npm publishers:** `prototype1006`, `cikikomo`, `neykoor`, `mamzhandsome`, `lupy4u`, `diezyyasha` (SafeDep also obscures the linked maintainer e-mail addresses).
- **Advertising URL injected into media:** `hxxps://fiora[.]nixel[.]my[.]id/` (`mamz-baileys`).
- **Remote follow-list source:** `hxxps://raw[.]githubusercontent[.]com/LevviCodeID/Levi4than/refs/heads/main/levvleys.json` (`lupy4u`).
- **Operator control repo / site:** GitHub `LevviCodeID/Levi4than` (follow-list JSON); operator site `levvicode[.]cloud`.
- **Newsletter channel identifiers:** `120363401404146384@newsletter` (`@neykoor`), `120363426628484388@newsletter` (`@cikikomo`), `120363406881628130` (`mamz-baileys` / `diezyyasha-baileys`, shared).
- **Behavioural markers:** `QueryIds.FOLLOW` / `QueryIds.MUTE` issued on `connection.update` (open); `forwardedNewsletterMessageInfo` on outgoing messages; `noSelfSync: true` at message-send sites; base64 `gintoki` authorisation gate and `sendMessage` behind base64.

## Defender priorities
1. **Treat Baileys forks as untrusted by default.** Baileys is a hot typosquat target because it carries a paired WhatsApp session. Pin known-good `baileys` / `libsignal-node` versions and prefer the upstream registry scope over community forks.
2. **Audit what a bot library does with the session.** Review `lib/Socket/newsletter.js` (follow/mute queries on `connection.open`), `lib/Socket/messages-send.js` (media `sourceUrl` / ad-URL injection), `lib/Socket/luxu.js` (forged `forwardedNewsletterMessageInfo` / `noSelfSync`), and `lib/Store/prototype-store.js` (base64 authorisation gates that send messages and throw `Blocked`).
3. **Watch for remote-configured behaviour.** A follow list pulled from raw.githubusercontent.com that the operator can rotate without a new release is a strong malicious-package signal; alert on fetches to untrusted repos inside a bot runtime.
4. **Check the WhatsApp account itself.** Review channel follows/subscriptions on affected accounts for unfamiliar `@newsletter` channels, especially ones that are muted; check outgoing messages for forged channel attribution and media with unexpected source URLs.
5. **Revoke the paired session / re-authenticate** on hosts that ran a confirmed-malicious package, since the session was usable to follow channels and (in the block variant) send messages from the account.
6. **Inventory `baileys` / `libsignal-node` dependencies** across bot projects, CI, and mirrors; the 4,250-name / 112-name name-spaces are large and most packages are unexamined — absence from SafeDep's confirmed list is **not** a clearance.

## Attribution and limits
- SafeDep attributes the confirmed set to the listed npm publishers and the `Levvi4than` / `levvicode[.]cloud` operator infrastructure but does **not** assert a broader actor identity or link the campaign to the Baileys upstream maintainer.
- The confirmed 70+15 package names are a **lower bound**; registry removals (e.g. `@diezyyasha/libsignal-node`) pre-empt full source analysis.
- This is **not** credential theft and is distinct from the ChainDrop / Mini Shai-Hulud npm worm family and the arrayref Rust supply-chain attack: shared use of the npm registry and developer-host execution does not establish shared code, infrastructure, or operator identity.

## Open questions
- Final confirmed package/version count and any further operator-infrastructure rotation.
- Confirmed victim scope and whether any forced-follow channel carries further payloads or monetisation.
- Whether `levvleys.json` targets grow, and whether the remote-follow-list pattern spreads to other multi-device bot libraries.
- Independent replication of the `@diezyyasha/libsignal-node` import-time patcher.

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [npm bin-entry dependency confusion: Google-scoped bin name harvesting](../patterns/npm-bin-entry-dependency-confusion.md)
- [ChainDrop keyv / cacheable npm worm](chaindrop-keyv-cacheable-npm-worm.md)
- [Flooding Dropper npm campaign](flooding-dropper-npm-campaign.md)
- [Coding-agent hooks as audit telemetry](../patterns/coding-agent-hook-audit-elastic-cursor-tool-calls.md)

## Sources
- SafeDep (Kunal Singh): [“Malicious Baileys npm WhatsApp campaign”](https://safedep.io/malicious-baileys-npm-whatsapp-campaign) (the full confirmed package/version set is published in the article's `baileys-packages-list.csv` dataset).
- Operator follow-list source (IoC, defanged): `raw[.]githubusercontent.com/LevviCodeID/Levi4than/refs/heads/main/levvleys.json`
