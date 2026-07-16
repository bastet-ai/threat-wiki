# postcss-minify-selector-parser npm RAT

## Summary
JFrog Security Research reported a malicious npm cluster on June 22, 2026 that masqueraded around the legitimate `postcss-selector-parser` ecosystem and led to a Windows RAT. The main package, `postcss-minify-selector-parser`, was not a one-character typosquat; it used plausible PostCSS / selector / parser naming and depended on the real `postcss-selector-parser`, a package npm reported at more than 150 million weekly downloads.

JFrog observed npm publisher `abdrizak` and three related packages: `postcss-minify-selector-parser`, `postcss-minify-selector`, and `aes-decode-runner-pro`. `postcss-minify-selector` depended on `postcss-minify-selector-parser`, while `postcss-minify-selector-parser` and `aes-decode-runner-pro` both decoded to the same PowerShell downloader and Windows payload chain. JFrog said the packages were still live and accessible when it published.

The durable lesson is import-time execution: installing a dependency is not the only risk boundary. In JFrog's analysis, `index.js` immediately required `src/config/defaults.js`, decoded an AES/custom-codec blob, wrote `../../settings.ps1`, and launched PowerShell with execution-policy bypass. That stage downloaded a Windows bundle from `nvidiadriver[.]net`, extracted a bundled Python 3.10 runtime plus Nuitka-compiled `.pyd` modules, and ran a RAT with HTTP C2, persistence, remote shell, file transfer, host profiling, VM checks, Chrome extension-data collection, and Chrome saved-login theft.

## Tags
- ops
- operations
- malware
- supply-chain
- npm
- PostCSS
- JavaScript
- Windows
- RAT
- PowerShell
- Nuitka
- Python
- credential-theft
- browser-credential-theft
- persistence

## Why this matters
- The package name looked ecosystem-plausible rather than obviously mistyped, which can bypass quick dependency-review heuristics that only catch near-neighbor typos.
- The trigger was a package entry-point import path, not an obvious `preinstall` / `postinstall` lifecycle script.
- The Windows payload brought its own Python runtime and Nuitka native extensions, so defenders need to hunt both Node.js and Python artifacts in affected developer environments.
- Browser-stored credentials and extension data were explicit targets; responders should rotate secrets used from affected hosts, not just npm tokens.

## Reported chain

### npm package cluster
- JFrog tied the cluster to npm publisher `abdrizak`.
- Reported packages:
  - `postcss-minify-selector-parser`
  - `postcss-minify-selector`
  - `aes-decode-runner-pro`
- `postcss-minify-selector-parser` used PostCSS / selector-parser terminology and depended on the legitimate `postcss-selector-parser` package.
- `postcss-minify-selector` presented itself as a PostCSS selector minifier and depended on `postcss-minify-selector-parser`.
- JFrog found that decoded blobs from `postcss-minify-selector-parser` and `aes-decode-runner-pro` led to the same downloader and Windows RAT chain.

### JavaScript and PowerShell stages
- `package.json` declared `index.js` as the main entry point.
- `index.js` immediately required `src/config/defaults.js`.
- Instead of normal parser logic, `src/config/defaults.js` contained a large encoded blob with layered decoding, including AES-256-GCM.
- The decoded JavaScript wrote a PowerShell script to `../../settings.ps1` and executed it with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ../../settings.ps1
```

- The PowerShell stage downloaded a Windows payload from `nvidiadriver[.]net`, wrote it under `%TEMP%`, extracted it, and launched `update.vbs` through `wscript`.
- JFrog's decoded command downloaded `winpatch-xd7d.win` to `%TEMP%\winPatch.zip`, extracted to `%TEMP%\winPatch`, and ran `%TEMP%\winPatch\update.vbs`.

### Bundled Windows RAT
- The downloaded bundle contained a bundled Python runtime, a Python loader, a VBS bootstrapper, and Nuitka-compiled Python 3.10 native extension modules.
- Reported files included:
  - `chost.exe`
  - `python310.dll`
  - `python3.dll`
  - `pythonw.exe`
  - `dll.zip`
  - `loader.py`
  - `update.vbs`
  - `api.cp310-win_amd64.pyd`
  - `audiodriver.cp310-win_amd64.pyd`
  - `auto.cp310-win_amd64.pyd`
  - `command.cp310-win_amd64.pyd`
  - `config.cp310-win_amd64.pyd`
  - `util.cp310-win_amd64.pyd`
- The VBS bootstrapper extracted `dll.zip` and ran `cmd /c chost.exe loader.py`.
- JFrog assessed `chost.exe` as a renamed Python 3.10 console launcher importing `python310.dll!Py_Main`.
- `loader.py` imported `audiodriver`, which started the main malware logic.

### Capabilities
JFrog reconstructed these RAT capabilities from Nuitka module resources and code references:

- HTTP C2 over encrypted `POST` packets.
- RC4 / ARC4-wrapped packet transport with MD5 checksum material.
- Registry persistence under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Single-instance marker `%TEMP%\.store`.
- Persistent victim UUID marker `%TEMP%\.host`.
- Host profiling and VM checks.
- File upload and download.
- Remote shell execution.
- Randomized wait / sleep and exit handling.
- Chrome extension-data collection.
- Chrome saved-login theft.

JFrog described the module split as:

- `config.pyd` — constants, command IDs, C2 URL, registry key names.
- `api.pyd` — HTTP C2 packet exchange.
- `audiodriver.pyd` — main RAT orchestration loop.
- `command.pyd` — host actions, VM checks, file transfer, shell execution.
- `auto.pyd` — Chrome credential and extension theft.
- `util.pyd` — tar / gzip archive helpers.

## Defender heuristics

### Dependency and build review
- Search dependency manifests and lockfiles for `postcss-minify-selector-parser`, `postcss-minify-selector`, and `aes-decode-runner-pro`.
- Treat suspicious ecosystem-plausible names as a review class; not every malicious package is a single-character typo.
- Diff package tarballs against prior good versions or expected minimal utilities. A small parser/minifier package should not contain AES-GCM blob decoders, PowerShell writers, or Windows payload downloaders.
- Expand JavaScript package review beyond lifecycle scripts. Entry-point imports can execute when tools import the package during builds, tests, transpilation, or application startup.

### Windows endpoint hunting
- Search for PowerShell execution of `../../settings.ps1` with `-NoProfile -ExecutionPolicy Bypass` from Node.js or package-manager contexts.
- Search for `%TEMP%\winPatch`, `%TEMP%\winPatch.zip`, `%TEMP%\.store`, and `%TEMP%\.host`.
- Search process and command-line telemetry for `wscript` launching `update.vbs`, and `chost.exe loader.py`.
- Review `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` for suspicious `csshost` values or paths under `%TEMP%`.
- Alert on developer workstations downloading from `nvidiadriver[.]net` or posting to `95[.]216[.]92[.]207:8080`.
- Treat Chrome credential access from a Python/Nuitka process as high severity, especially references to `Local State`, `Login Data`, DPAPI, `NCryptDecrypt`, `lsass.exe`, or `SeDebugPrivilege`.

### Response
- Remove the reported packages and any transitive dependency that pulled them in.
- Preserve package-manager logs, process telemetry, PowerShell logs, downloaded archives, and the extracted `%TEMP%\winPatch` directory when available.
- Rotate credentials used from affected Windows developer hosts, including browser-stored credentials, GitHub / Git / npm tokens, cloud credentials, and secrets available through Chrome extensions.
- Block reported network indicators and review proxy / EDR telemetry for historical contact.

## Reported indicators
- npm publisher: `abdrizak`
- Packages: `postcss-minify-selector-parser`, `postcss-minify-selector`, `aes-decode-runner-pro`
- Main entry path: `index.js` requiring `src/config/defaults.js`
- Dropped PowerShell path: `../../settings.ps1`
- PowerShell invocation: `powershell -NoProfile -ExecutionPolicy Bypass -File ../../settings.ps1`
- Download domain: `nvidiadriver[.]net`
- Download path: `/verv1432/winpatch-xd7d.win`
- Extracted directory: `%TEMP%\winPatch`
- VBS bootstrapper: `%TEMP%\winPatch\update.vbs`
- Runtime launcher: `chost.exe loader.py`
- C2: `hxxp[:]//95[.]216[.]92[.]207:8080`
- Registry persistence location: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Reported Run value: `csshost`
- State markers: `%TEMP%\.store`, `%TEMP%\.host`
- Chrome theft strings: `Local State`, `Login Data`, `SELECT origin_url, username_value, password_value, date_created FROM logins`, `DPAPI`, `NCryptOpenStorageProvider`, `NCryptOpenKey`, `NCryptDecrypt`, `Google Chromekey1`, `lsass.exe`, `SeDebugPrivilege`, `AES.MODE_GCM`, `ChaCha20_Poly1305`
- VM / sandbox checks reported by JFrog: `wmic computersystem get model,manufacturer`, `wmic bios get serialnumber,version`, `wmic diskdrive get model`, `tasklist`, `vmware`, `virtualbox`, `kvm`, `qemu`, `hyper-v`, `vboxservice`, `vboxtray`, `vmtoolsd`, `vmwaretray`, `vmwareuser`, MAC prefixes `00:05:69`, `00:0c:29`, `00:50:56`, `08:00:27`, `00:15:5d`

## Related pages
- [npm install explicit-trust controls](../patterns/npm-install-explicit-trust-controls.md)
- [procwire / routecraft npm Windows dropper](procwire-routecraft-npm-windows-dropper.md)
- [MYRA RAT](../tools/myra-rat.md)
- [binding.gyp npm CI/CD worm](binding-gyp-npm-cicd-worm.md)

## Sources
- [JFrog Security Research](https://research.jfrog.com/post/from-postcss-typosquat-to-windows-rat/)
