# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract, get_contract_for_doc


def sync_task_update(doc, method=None):
	"""
	Synchronizes ERPNext Task status changes with linked Contract Obligations.
	When a task completes, automatically marks the corresponding milestone obligation fulfilled.
	"""
	if doc.status == "Completed":
		obligations = frappe.get_all(
			"Contract Obligation",
			filters={"linked_task": doc.name, "status": ["in", ["Pending", "In Progress", "Overdue"]]},
			fields=["name"]
		)
		if obligations:
			from nsd_contract_management.services.obligation_service import complete_obligation
			for ob in obligations:
				try:
					complete_obligation(ob.name, completed_by=doc.modified_by)
				except Exception:
					pass


def sync_timesheet(doc, method=None):
	"""Syncs submitted Timesheet hours and billing against Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name and hasattr(doc, "parent_project") and doc.parent_project:
		contract_records = frappe.get_all("Contract", filters={"project": doc.parent_project}, fields=["name"], limit=1)
		if contract_records:
			contract_name = contract_records[0].name

	if not contract_name:
		return

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Timesheet",
		reference_name=doc.name,
		reference_role="Cost",
		amount=flt(doc.get("total_billable_amount") or doc.get("total_costing_amount")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)


def sync_expense_claim(doc, method=None):
	"""Syncs submitted Expense Claim with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name and hasattr(doc, "project") and doc.project:
		contract_records = frappe.get_all("Contract", filters={"project": doc.project}, fields=["name"], limit=1)
		if contract_records:
			contract_name = contract_records[0].name

	if not contract_name:
		return

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Expense Claim",
		reference_name=doc.name,
		reference_role="Cost",
		amount=flt(doc.get("total_sanctioned_amount") or doc.get("total_claimed_amount")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)
