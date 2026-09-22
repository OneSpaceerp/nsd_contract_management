# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, date_diff, add_days, now_datetime
from nsd_contract_management.services.contract_service import transition_status


def scan_and_apply_retention_policy() -> dict:
	"""
	Scheduled maintenance job:
	- Scans contracts in Terminated or Expired status.
	- Checks retention age threshold (default: 7 years / 2555 days).
	- STRICTLY ignores any contract under an active Legal Hold.
	- Transitions qualified contracts to Archived status with immutable audit logging.
	"""
	retention_years = frappe.db.get_single_value("Contract Management Settings", "retention_period_years") or 7
	retention_days = int(retention_years) * 365
	cutoff_date = add_days(getdate(nowdate()), -retention_days)

	contracts = frappe.get_all(
		"Contract",
		filters={
			"status": ["in", ["Terminated", "Expired"]],
			"modified": ["<=", str(cutoff_date)]
		},
		fields=["name", "title", "legal_hold", "status", "modified"]
	)

	archived_count = 0
	skipped_legal_hold = 0

	for c in contracts:
		if c.legal_hold:
			skipped_legal_hold += 1
			continue

		# Move to Archived
		transition_status(c.name, "Archived", reason=f"Automated retention policy applied: age exceeds {retention_years} years.")
		archived_count += 1

		frappe.get_doc({
			"doctype": "Comment",
			"comment_type": "Info",
			"reference_doctype": "Contract",
			"reference_name": c.name,
			"content": _("Contract moved to Archived status under {0}-year retention schedule on {1}.").format(
				retention_years, now_datetime()
			)
		}).insert(ignore_permissions=True)

	return {
		"eligible_scanned": len(contracts),
		"archived": archived_count,
		"skipped_due_to_legal_hold": skipped_legal_hold
	}


def enforce_retention_policies():
	"""Scheduler alias for scan_and_apply_retention_policy."""
	return scan_and_apply_retention_policy()
