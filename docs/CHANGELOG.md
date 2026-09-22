# Changelog: NSD Contract Management & Intelligence

## [1.0.0] - 2026-09-22

### Added
- **Core Architecture & Scaffolding**:
  - Full Frappe / ERPNext v16 custom app layout with `flit_core` build backend and Python 3.14+ compatibility.
  - Multi-company permission query isolation and v16 custom permission types.
- **Contract Lifecycle Engine**:
  - 37 DocTypes encompassing full CLM lifecycle: intake, drafting, review, negotiation, multi-factor approval, eSignature, obligations, renewals, amendments, terminations, legal hold, and archival.
  - Deterministic state machine with valid transition matrix and legal hold enforcement.
  - Semantic contract versioning (`v1.0`, `v1.1`, `v2.0`) with SHA-256 cryptographic hashing and executed version locking.
- **AI Contract Intelligence**:
  - Provider abstraction interface (`AIProvider`) with deterministic offline `MockAIProvider` and live `OpenAIProvider`.
  - Prompt injection defense, input sandboxing, and canonical schema validation.
  - Autonomous `AI Agent` runs with Human-In-The-Loop (HITL) authorization gates.
- **Deep ERPNext Integration**:
  - Real-time bidirectional integration across Selling, Buying, Accounts, Projects, Subscriptions, Support, HR, and Assets.
  - Deterministic commercial leakage engine detecting price variances, uncontracted spend, and budget ceiling breaches.
  - MCP adapter exposing safe tools to external AI agents.
- **UI, Reports & Fixtures**:
  - Frappe v16 Desk Workspace with shortcuts, cards, and quick lists.
  - 4 Script Reports: `Contract Register`, `Overdue Obligations`, `Upcoming Renewals`, `Contract Leakage Report`.
  - Custom field fixtures for 12 native ERPNext documents.
  - Seeder module generating realistic commercial demo data.
- **Test Suite**:
  - 8 automated test modules covering lifecycle states, approval matrices, obligation tracking, signature workflows, AI extraction, ERP links, leakage detection, and permissions.
