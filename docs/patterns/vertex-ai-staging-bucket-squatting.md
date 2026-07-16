# Vertex AI staging-bucket squatting

## Summary
Unit 42 disclosed **Pickle in the Middle** on June 16, 2026: a vulnerability in the Google Cloud Vertex AI SDK for Python where deterministic default staging-bucket names and missing ownership checks could let an attacker pre-create a victim's expected Cloud Storage bucket, receive uploaded model artifacts, race-replace them, and obtain code execution when Vertex AI later loaded the model.

Track this as a reusable cloud / AI pattern: managed-AI services often bridge developer SDK defaults, globally unique object storage names, service agents, model serialization, and tenant infrastructure. A small staging-location trust failure can become model poisoning, credential theft, or cross-deployment exposure.

## Tags
- patterns
- cloud
- AI
- machine-learning
- Google Cloud
- Vertex AI
- bucket squatting
- model poisoning
- deserialization
- pickle
- joblib
- RCE
- service-agent
- tenant-project
- supply-chain

## Why this matters
- The attack required no access to the victim's Google Cloud project; knowledge of the victim project ID and region could be enough when the default staging bucket did not already exist.
- The vulnerable SDK path silently reused an existing bucket with the expected name without verifying ownership.
- The payload crossed trust boundaries: attacker-controlled Cloud Storage content was later read by Vertex AI service infrastructure and deserialized by the victim's deployed model container.
- The vulnerable versions named by Unit 42 were `google-cloud-aiplatform` SDK `1.139.0` and `1.140.0`; Google fixed the issue in the Vertex AI SDK for Python, with Unit 42 calling out version `1.148.0` or later as the remediation target.
- The pattern generalizes beyond this one SDK: deterministic cloud-resource names plus unsafe artifact loading create a predictable pre-positioning opportunity for attackers.

## Reported chain
1. Vertex AI SDK users uploaded a model without explicitly setting `staging_bucket`.
2. Vulnerable SDK versions derived a default Cloud Storage bucket name from the project ID and region, such as `<project>-vertex-staging-<region>`.
3. An attacker who knew the victim project ID could create that globally unique bucket name in the attacker's own Google Cloud project before the victim's first use in that region.
4. The SDK checked whether the bucket existed, but did not verify that the bucket belonged to the victim project.
5. The victim SDK uploaded model artifacts into the attacker-owned bucket.
6. The attacker used a Cloud Storage `object.finalize` trigger to replace the uploaded model artifact within a narrow race window before Vertex AI's service agent read it.
7. The malicious `joblib` / `pickle` payload executed through Python deserialization when the model was loaded for serving.
8. Unit 42's proof of concept queried the Google Compute Engine metadata service from the serving container and exfiltrated service-account credentials.

## Technical pivots
- Vulnerable package: `google-cloud-aiplatform` SDK for Python `1.139.0` and `1.140.0`.
- Fixed guidance: update to `google-cloud-aiplatform` `1.148.0` or later.
- Default staging pattern described by Unit 42: deterministic project-and-region bucket names such as `<project>-vertex-staging-<region>`.
- Exploit precondition: the victim's default staging bucket for that region does not already exist, and the SDK call does not specify an explicit `staging_bucket`.
- Attacker storage permissions in the proof of concept allowed the victim identity to create objects and Vertex AI's service agent to read them.
- Race timing reported by Unit 42: model upload at `T+0 ms`, Cloud Function observation around `T+804 ms`, malicious replacement around `T+1,433 ms`, and service-agent read around `T+2,460 ms`.
- Serialization boundary: `joblib.load()` / Python `pickle` deserialization and crafted `__reduce__` execution.
- Credential target: metadata-server OAuth token for a managed Vertex AI serving service account in a Google-managed tenant project.

## Defender heuristics
### Immediate remediation
- Upgrade `google-cloud-aiplatform` to `1.148.0` or later anywhere Vertex AI model upload or deployment automation runs.
- Search code, notebooks, CI jobs, Airflow / Vertex pipelines, and internal ML platform wrappers for `Model.upload()` or equivalent SDK calls that omit `staging_bucket`.
- Set `staging_bucket` explicitly to an organization-owned `gs://` bucket with expected project ownership, retention, access logging, and least-privilege IAM.
- Pre-create and lock down expected Vertex AI staging buckets for active regions rather than letting SDK defaults create or discover them on first use.

### Detection and response
- Review Cloud Audit Logs for model uploads where the artifact URI or staging bucket points to a project outside the expected organization or landing zone.
- Hunt for Cloud Storage bucket names matching Vertex AI staging patterns that are owned by unknown projects or external organizations.
- Alert when ML build, notebook, or deployment identities write model artifacts to buckets they do not own or that lack expected labels, org policies, CMEK settings, retention policies, or logging sinks.
- Inspect recently deployed Vertex AI models for artifact URI drift, unexpected `joblib` / pickle files, and size or checksum changes between training output and model registry ingestion.
- Treat suspicious Vertex AI model deserialization as host / workload compromise: rotate affected service-account credentials, review metadata-server token use, and check for access to model artifacts, BigQuery datasets, logs, and other tenant-project resources described by Unit 42.

### Hardening pattern
- Avoid unsafe deserialization formats for untrusted model artifacts. Where pickle / joblib is unavoidable, enforce signed artifact provenance and checksum validation before upload and before deployment.
- Prefer immutable, organization-owned artifact registries or buckets over SDK-generated defaults.
- Require ownership checks in internal SDK wrappers before reusing any globally named cloud resource.
- Include AI / ML staging locations in cloud attack-path reviews; staging buckets can be as sensitive as production model endpoints.

## Related pages
- [Cloud logging control-plane tampering](cloud-logging-control-plane-tampering.md)
- [AI-augmented adversary operations](ai-augmented-adversary-operations.md)
- [Developer-tool config auto-execution](developer-tool-config-auto-execution.md)

## Sources
- Unit 42: [https://unit42.paloaltonetworks.com/hijacking-vertex-ai-model/](https://unit42.paloaltonetworks.com/hijacking-vertex-ai-model/)
- Google Cloud Vertex AI SDK for Python release notes: [https://github.com/googleapis/python-aiplatform/releases](https://github.com/googleapis/python-aiplatform/releases)
