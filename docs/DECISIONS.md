# Architectural Decision Records (ADR)

## ADR 001: Modular In-Process Services over Microservices
- **Context**: Contract lifecycle operations (intake, versioning, approvals, signatures, obligations, leakage) require tight transactional consistency with ERPNext records.
- **Decision**: Implement domain logic as Python service modules in `nsd_contract_management.services.*` instead of separate external HTTP microservices.
- **Consequences**: Zero network latency, transactional MariaDB/Postgres integrity, easy testability with standard Frappe tooling, simplified deployment.

## ADR 002: Zero-Dependency Architecture for Cloud AI and eSignatures
- **Context**: Enterprise deployments may operate on air-gapped systems or strict minimal-dependency Python 3.14 environments.
- **Decision**: Avoid bulky external SDKs (e.g. `openai`, `boto3`, `docusign`). Use standard Python `urllib` and `json` for external API integration, alongside a deterministic offline `MockAIProvider` and `MockSignatureProvider`.
- **Consequences**: Fast installation, zero dependency conflicts, complete offline testability.

## ADR 003: Pure Non-Invasive ERP Reference Tracking
- **Context**: CLM apps often mistakenly attempt to create GL entries or shadow invoice tables, creating accounting audit failure.
- **Decision**: Use `Contract ERP Reference` child records and custom Link fields on native ERP documents. Never write directly to GL/SL tables.
- **Consequences**: Preserves ERPNext accounting truth 100%, compliant with statutory audits, works across multi-currency and multi-company setups.

## ADR 004: Semantic Versioning with Cryptographic Hash Sealing
- **Context**: Regulatory frameworks require proof that an executed contract was not modified after signature.
- **Decision**: Model contract drafts as semantic versions (`v1.0`, `v1.1`, `v2.0`). Upon signature completion, lock the executed version record (`is_locked = 1`, `is_executed = 1`) and compute SHA-256 integrity hash.
- **Consequences**: Unalterable historical evidence, audit compliance, transparent redline diffing.
