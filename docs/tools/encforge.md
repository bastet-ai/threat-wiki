# ENCFORGE

## Summary
**ENCFORGE** is a Linux ransomware payload written in Go and purpose-built to encrypt AI and machine-learning assets. Sysdig observed the JADEPUFFER operator deploy it through an internet-exposed Langflow instance compromised with **CVE-2025-3248**. The recovered static ELF was UPX-packed, staged as `lockd`, and configured to target roughly 180 extensions spanning model weights, fine-tuning adapters, vector indexes, embeddings, and training datasets.

Unlike JADEPUFFER's earlier improvised MySQL/Nacos encryption, ENCFORGE is a compiled locker. It uses AES-256-CTR for file data, wraps the per-run key with an embedded RSA-2048 public key, renames processed files with `.locked`, kills processes holding target files open, writes ransom notes, and removes itself. Sysdig found no exfiltration or leak-site capability in the recovered binary.

## Tags
- tools
- malware
- ransomware
- ENCFORGE
- JADEPUFFER
- Linux
- Golang
- AI infrastructure
- model weights
- training data
- vector databases
- Langflow
- CVE-2025-3248
- container escape
- Docker socket
- AES-256-CTR
- RSA-2048

## Why this matters
- The built-in target list explicitly covers PyTorch and TensorFlow checkpoints, SafeTensors, ONNX, GGUF/GGML, FAISS, Parquet, Arrow, NumPy, TensorFlow records, and LoRA adapters. This is deliberate AI/ML targeting rather than incidental generic file encryption.
- Model weights, indexes, and training state may be expensive or impossible to reconstruct even when ordinary application code and databases are recoverable.
- The observed intrusion turned unrestricted `/var/run/docker.sock` access into host root, allowing a container-level Langflow compromise to encrypt host-mounted assets.
- Sysdig reported one observed session and no victim count. The evidence supports a live encryption attempt, not a broad ENCFORGE deployment claim.

## Technical behavior
- **Format:** statically linked Go `1.22.12` ELF, packed with UPX `5.20` in the recovered sample.
- **Internal strings:** project name `encfile`; error text references a companion key-generation tool named `keyforge`.
- **Encryption:** AES-256-CTR with a per-run symmetric key wrapped under an embedded RSA-2048 public key; selected file regions are encrypted to improve speed.
- **File handling:** approximately 180 default extensions plus operator-supplied globs through `--include`; completed files receive `.locked`.
- **Execution controls:** `--try-run` scans before encryption and `--lock` starts the live pass.
- **Impact support:** kills processes that hold target files open, avoids re-encrypting completed files after restart, writes `README`, `HOW_TO_DECRYPT`, and `README_DECRYPT`, then self-deletes.
- **Extortion contact:** `e78393397@proton[.]me`, also observed in Sysdig's earlier JADEPUFFER case and the strongest public linkage between the operations.
- **No observed theft module:** the binary contained no networking, cloud-storage, or staging code; Sysdig saw no leak site, Tor payment portal, or data exfiltration in the session.

## Public indicators
### Infrastructure and artifacts
- `34.153.223[.]102:9191` — payload staging server observed by Sysdig
- `/tmp/.sk/lockd` — attempted local staging path
- `.locked` — encrypted-file extension
- `README`, `HOW_TO_DECRYPT`, `README_DECRYPT` — ransom-note names
- `e78393397@proton[.]me` — extortion contact

### SHA-256
- `8cb0c223b018cecef1d990ec81c67b826eb3c30d54f06193cf69969e9a8baea2` — packed binary
- `ea7822eac6cecef7746c606b862b4d3034856caf754c4cf69533662637905328` — unpacked binary

## Detection and response
- Alert on Langflow or other application processes accessing `/var/run/docker.sock`, creating containers, or invoking Docker container-creation APIs.
- Detect containers launched with `Privileged: true`, `PidMode: host`, `NetworkMode: host`, or `/:/host:rw`-style host-root mounts, especially followed by `nsenter` or `/proc/<pid>/root` copying.
- Hunt for `/tmp/.sk/lockd`, the published hashes, `encfile` / `keyforge` strings, the ransom-note names, and rapid creation of `.locked` files in model, vector-store, and dataset paths.
- Upgrade Langflow to a current supported release. Version `1.3.0` fixed CVE-2025-3248, but later exploited flaws require newer releases; Sysdig recommends `1.9.1` or later.
- Remove the Docker socket from containers that do not require it. If access is unavoidable, mediate it through a narrowly scoped authorization proxy.
- Rotate AI-provider keys, cloud credentials, database secrets, and tokens available to the Langflow process; patching does not revoke material already harvested.
- Keep model weights, indexes, datasets, and fine-tuning state in offline or immutable snapshots and test restoration separately from application recovery.

## Related pages
- [JADEPUFFER Langflow agentic ransomware](../ops/jadepuffer-langflow-agentic-ransomware.md)
- [Langflow CVE-2026-33017 cryptominer SSH worm](../ops/langflow-cve-2026-33017-cryptominer-ssh-worm.md)
- [Langflow CVE-2026-55255 flow authorization bypass](../ops/langflow-cve-2026-55255-flow-authorization-bypass.md)

## Sources
- Sysdig Threat Research Team: [JADEPUFFER evolves: the agentic threat actor deploys ransomware built to destroy AI models](https://www.sysdig.com/blog/jadepuffer-evolves-the-agentic-threat-actor-deploys-ransomware-built-to-destroy-ai-models)
- GitHub advisory: [GHSA-rvqx-wpfh-mfx7](https://github.com/langflow-ai/langflow/security/advisories/GHSA-rvqx-wpfh-mfx7)
