# Deployment & Operations

## 1. Supported deployment model
Primary target: self-hosted ERPNext v16 bench/site.

## 2. Installation
```bash
bench get-app <git-url>
bench --site <site> install-app nsd_contract_management
bench --site <site> migrate
bench build --app nsd_contract_management
```

Use the exact app repository URL supplied by the implementation team; do not invent it in code.

## 3. Production prerequisites
- ERPNext/Frappe v16-compatible environment
- Redis
- workers
- scheduler
- Node build toolchain appropriate to the selected Frappe v16 patch release
- persistent file storage
- outbound HTTPS for external integrations
- optional object storage

## 4. Configuration
Use Site Config / app configuration for:
- AI providers
- eSignature provider credentials
- portal configuration
- webhook secrets
- external CRM/ERP credentials
- storage configuration
- default timezone
- rate limits

Never store credentials in Git.

## 5. Fixtures
Ship standard:
- Roles
- Role Profiles where required
- Contract Type demo/reference records only if explicitly marked as fixtures
- Clause categories
- standard workflow configuration
- custom permission types
- reports/workspaces where appropriate

## 6. Migration strategy
All schema changes must be deployable with `bench migrate`.
Never require manual database edits.

## 7. Backup
Ensure database and file backup coverage. Executed contracts and evidence are business-critical and must be included in disaster recovery planning.

## 8. Observability
Monitor:
- worker health
- scheduler health
- queue depth
- failed jobs
- API latency/errors
- AI provider latency/errors/cost
- storage failures
- webhook backlog

## 9. CI/CD
Pipeline stages:
1. lint
2. unit tests
3. build assets
4. migration test
5. integration tests
6. security checks
7. package/version
8. deploy to staging
9. smoke tests
10. production approval

## 10. Upgrade policy
Every supported ERPNext/Frappe version must have a compatibility matrix. Do not assume forward compatibility without tests.
