# Installation Guide: NSD Contract Management & Intelligence

## Prerequisites
- Frappe Framework v16.x
- ERPNext v16.x
- Python >= 3.14
- MariaDB 10.6+ or PostgreSQL 14+
- Redis 6.0+

## 1. Bench Installation

In your Frappe bench directory:

```bash
# Fetch repository or copy app into bench apps/
bench get-app nsd_contract_management /path/to/nsd_contract_management

# Install application onto your target site
bench --site [site-name] install-app nsd_contract_management

# Run database migrations to provision DocTypes, child tables, and fields
bench --site [site-name] migrate

# Build frontend assets
bench build --app nsd_contract_management

# Clear Redis and document caches
bench --site [site-name] clear-cache
```

## 2. Seed Initial Demo Data (Optional)

To seed standard clause categories, playbooks, templates, and demonstration contracts:

```bash
bench --site [site-name] execute nsd_contract_management.demo_data.seeder.seed_demo_data
```

## 3. Verify Background Schedulers

Ensure Frappe scheduler is active:
```bash
bench --site [site-name] enable-scheduler
bench --site [site-name] doctor
```
The application registers hourly alerts, daily obligation & renewal scans, and nightly retention audits.
