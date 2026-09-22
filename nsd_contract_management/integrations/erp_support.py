# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract, get_contract_for_doc


def sync_issue_update(doc, method=None):
	"""
	Monitors ERPNext Support Issues linked to a Contract and assesses SLA response/resolution breaches.
	"""
	contract_name = get_contract_for_doc(doc)
	if not contract_name and hasattr(doc, "customer") and doc.customer:
		contracts = frappe.get_all("Contract", filters={"customer": doc.customer, "status": "Effective"}, fields=["name"], limit=1)
		if contracts:
			contract_name = contracts[0].name

	if not contract_name:
		return

	if doc.status in ["Closed", "Resolved"] and hasattr(doc, "resolution_time") and doc.resolution_time:
		# Check SLA breach
		from nsd_contract_management.services.performance_service import record_metric_value
		record_metric_value(
			contract_name=contract_name,
			metric_code="support_resolution_time",
			actual_value=flt(doc.resolution_time),
			target_value=24.0,  # 24 hours standard SLA
			unit="Hours"
		)


def sync_maintenance_visit(doc, method=None):
	"""Syncs submitted Maintenance Visit with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Maintenance Visit",
		reference_name=doc.name,
		reference_role="Support",
		amount=0.0,
		status=doc.get("completion_status") or "Submitted"
	)


def sync_warranty_claim(doc, method=None):
	"""Syncs Warranty Claim with Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Warranty Claim",
		reference_name=doc.name,
		reference_role="Support",
		amount=0.0,
		status=doc.get("status") or "Submitted"
	)
