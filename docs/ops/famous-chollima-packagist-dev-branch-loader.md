# Famous Chollima Packagist dev-branch loader

## Summary
Socket reported a May 2026 PHP ecosystem supply-chain finding where obfuscated JavaScript was appended to `tailwind.js` in the Packagist-exposed development version `roberts/leads:dev-drewroberts/feature/test-case`. Socket assessed the activity as likely developer or repository compromise / poisoned-branch workflow rather than a malicious package created from scratch, with tradecraft consistent with North Korea-linked Famous Chollima / Contagious Interview developer-targeting lures.

The stable release line was not reported as affected. The risk is targeted execution: a recruiter, coding-test, or fake-collaboration lure could instruct a developer to install the dev branch or clone the feature branch, causing a legitimate-looking Laravel project setup to execute a Node.js loader hidden far to the right of a normal Tailwind configuration.

## Tags
- ops
- operations
- supply-chain
- Packagist
- Composer
- PHP
- Laravel
- developer-targeting
- poisoned-branch
- branch-compromise
- Contagious Interview
- FAMOUS CHOLLIMA
- Lazarus
- North Korea
- blockchain-dead-drop
- loader
- credential-theft
- infostealer
- RAT

## Why this matters
- The malicious code lived in a Packagist-installable dev branch of a legitimate package, not a newly created throwaway package, which fits targeted trust abuse against developers.
- The payload was hidden after a benign `tailwind.js` configuration with a large whitespace gap, reinforcing that build/config files need review before running interview or onboarding projects.
- The loader used public blockchain / RPC infrastructure as a dead-drop path, making the network pattern look different from ordinary domain-based C2.
- Socket linked overlapping wallet addresses, Aptos fallback identifiers, XOR keys, and config-file injection patterns to public victim reports and prior DPRK-linked DEV#POPPER / OmniStealer / BeaverTail-family reporting.

## Reported chain
1. A malicious branch `drewroberts/feature/test-case` in the legitimate `roberts/leads` Laravel package was exposed through Packagist as `dev-drewroberts/feature/test-case`.
2. The affected file was `tailwind.js`, where an otherwise ordinary Tailwind configuration was followed by a large horizontal whitespace gap and obfuscated JavaScript beginning with the campaign marker `global['!']='9-0264-2'`.
3. The loader reconstructed Node.js internals such as `require` and `module`, then retrieved payload pointers from TRON and Aptos infrastructure.
4. It used BNB Smart Chain RPC services to recover encrypted transaction input data, decrypted payload stages with embedded XOR keys, and executed the recovered JavaScript with `eval()`.
5. The loader could launch a detached hidden Node.js child process with `windowsHide: true` and `node -e`, giving the remote stage access to environment variables, local files, Git metadata, package credentials, cloud secrets, and child-process execution in the developer context.
6. Socket reported the affected version to Packagist, which removed the malicious version; Socket also notified the project maintainer and GitHub Security.

## Scope and caveats
Socket did not report broad organic exposure, public victim communications instructing installation of this exact version, or direct exfiltration in the visible local loader. Treat the visible code as a loader: the final payload and targeting logic can change remotely through the blockchain/RPC dead-drop path.

The finding should be tracked separately from Mini Shai-Hulud / TeamPCP. It is another developer-ecosystem supply-chain path, but the attribution and lure shape are DPRK / Contagious Interview-style rather than TeamPCP worm propagation.

## Indicators and hunt pivots
- Affected package: `roberts/leads`
- Affected Packagist version: `dev-drewroberts/feature/test-case`
- Mapped GitHub branch: `drewroberts/feature/test-case`
- Affected file: `tailwind.js`
- Observed branch commit: `6c5c3c7655ce76399af11126b7e9a9058eb2e45d`
- Campaign markers / string pivots:
  - `global['!']='9-0264-2'`
  - `global['_V']='A9-0264-2'`
  - `_$_1e42`
  - `rmcej%otb%`
  - `trongrid`
  - `aptoslabs`
  - `bsc-dataseed`
  - `bsc-rpc`
  - `eth_getTransactionByHash`
  - `windowsHide`
- Execution pivots:
  - `node -e` spawned from package build/setup context
  - `child_process.spawn()` with detached / hidden-window options
  - developer workstations contacting TRON, Aptos, or BNB Smart Chain RPC services during project setup

## Defender heuristics
- Treat unfamiliar `dev-*` Composer constraints and branch-specific install instructions as high-risk when they arrive through recruiter, interview, freelance, or contributor-onboarding channels.
- Review build/config files before execution, including `composer.json`, `package.json`, `webpack.mix.js`, `vite.config.*`, `postcss.config.*`, `tailwind.config.*`, `tailwind.js`, `.github/workflows/*`, and `scripts/*`.
- Hunt across all refs, not just default branches and tags, for suspicious JavaScript in config files and large whitespace gaps after otherwise normal configuration content.
- Alert on Node.js child processes and blockchain/RPC HTTP access during dependency installation or project bootstrap.
- If a developer executed the affected branch or similar lure code, isolate the endpoint before rotating credentials; assume local `.env`, SSH keys, Git credentials, package tokens, cloud keys, browser stores, and crypto wallets may be exposed depending on the remote stage.
- For maintainers, preserve evidence before cleanup, then review branch protection, collaborator access, PATs, OAuth apps, Packagist hooks, deploy keys, and recent branch/tag mutations.

## Related pages
- [StegaBin Pastebin-steganography npm campaign](stegabin-pastebin-steganography-npm-campaign.md)
- [GitHub / Packagist postinstall hook campaign](github-packagist-postinstall-hook-campaign.md)
- [Laravel-Lang Composer tag-rewrite compromise](laravel-lang-composer-tag-rewrite-compromise.md)
- [Mini Shai-Hulud npm/PyPI worm campaign](mini-shai-hulud-npm-pypi-worm-campaign.md)
- [JINX-0164 crypto developer infrastructure campaign](jinx-0164-crypto-developer-infrastructure-campaign.md)

## Sources
- Socket: <https://socket.dev/blog/famous-chollima-targets-php-developers-through-compromised-packagist-package>
- Trend Micro VOID DOKKAEBI / DEV#POPPER context cited by Socket: <https://www.trendmicro.com/en_us/research/26/d/void-dokkaebi-uses-fake-job-interview-lure-to-spread-malware-via-code-repositories.html>
- Microsoft Contagious Interview context cited by Socket: <https://www.microsoft.com/en-us/security/blog/2026/03/11/contagious-interview-malware-delivered-through-fake-developer-job-interviews/>
