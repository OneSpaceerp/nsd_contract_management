# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, nowdate, add_days


def hourly_checks():
	"""Runs hourly to check for urgent approvals, expiring sessions, and short-term alerts."""
	try:
		from nsd_contract_management.services.approval_service import check_pending_approval_slas
		check_pending_approval_slas()
	except Exception:
		frappe.log_error(title="Contract Hourly Check Failed", message=frappe.get_traceback())


def daily_obligation_scan():
	"""Scans all active contract obligations to identify upcoming deadlines, mark overdue, and trigger escalations."""
	try:
		from nsd_contract_management.services.obligation_service import run_daily_obligation_scan
		run_daily_obligation_scan()
	except Exception:
		frappe.log_error(title="Daily Obligation Scan Failed", message=frappe.get_traceback())


def daily_renewal_notice_scan():
	"""Scans contracts approaching notice periods or expiration dates and generates renewal records."""
	try:
		from nsd_contract_management.services.renewal_service import run_daily_renewal_scan
		run_daily_renewal_scan()
	except Exception:
		frappe.log_error(title="Daily Renewal Notice Scan Failed", message=frappe.get_traceback())


def daily_leakage_detection_run():
	"""Executes deterministic commercial leakage scans across linked ERPNext transactions."""
	try:
		from nsd_contract_management.integrations.leakage_engine import run_scheduled_leakage_audit
		run_scheduled_leakage_audit()
	except Exception:
		frappe.log_error(title="Daily Leakage Detection Run Failed", message=frappe.get_traceback())


def nightly_retention_and_legal_hold_check():
	"""Enforces contract retention policies and ensures legal-hold-locked agreements are protected."""
	try:
		from nsd_contract_management.services.retention_service import enforce_retention_policies
		enforce_retention_policies()
	except Exception:
		frappe.log_error(title="Nightly Retention Scan Failed", message=frappe.get_traceback())


def process_signature_status_poll():
	"""Polls active signature requests where webhooks are delayed or not supported."""
	try:
		from nsd_contract_management.services.signature_service import poll_pending_signature_requests
		poll_pending_signature_requests()
	except Exception:
		frappe.log_error(title="Signature Poll Failed", message=frappe.get_traceback())
