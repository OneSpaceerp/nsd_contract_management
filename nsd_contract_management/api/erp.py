# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract
from nsd_contract_management.integrations.leakage_engine import run_scheduled_leakage_audit


@frappe.whitelist()
def link_transaction(
	contract_name: str,
	doctype: str,
	docname: str,
	role: str = "Fulfillment",
	amount: float = 0.0
) -> dict:
	"""RPC: Links an ERPNext transaction to a Contract."""
	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype=doctype,
		reference_name=docname,
		reference_role=role,
		amount=flt(amount)
	)
	return {"success": True, "contract": contract_name, "linked": f"{doctype} {docname}"}


@frappe.whitelist()
def get_financial_summary(contract_name: str) -> dict:
	"""RPC: Aggregates real-time financial totals from linked ERP references without touching GL."""
	contract = frappe.get_doc("Contract", contract_name)
	total_billed = 0.0
	total_paid = 0.0
	total_committed = 0.0

	for ref in contract.get("erp_references", []):
		if ref.status == "Cancelled":
			continue
		if ref.reference_role == "Billing":
			total_billed += flt(ref.amount)
		elif ref.reference_role == "Payment":
			total_paid += flt(ref.amount)
		elif ref.reference_role == "Fulfillment":
			total_committed += flt(ref.amount)

	return {
		"contract": contract_name,
		"contract_value": flt(contract.total_contract_value),
		"currency": contract.currency,
		"total_committed": total_committed,
		"total_billed": total_billed,
		"total_paid": total_paid,
		"balance_remaining": flt(contract.total_contract_value) - total_billed
	}


@frappe.whitelist()
def run_leakage_audit() -> dict:
	"""RPC: Executes scheduled commercial leakage scan."""
	audited = run_scheduled_leakage_audit()
	return {"contracts_audited": audited}
