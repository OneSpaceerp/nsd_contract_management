# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime


def link_transaction_to_contract(
	contract_name: str,
	reference_doctype: str,
	reference_name: str,
	reference_role: str,
	amount: float = 0.0,
	currency: str = "USD",
	status: str = "Submitted"
) -> None:
	"""
	Adds or updates a Contract ERP Reference child table row linking the ERPNext document.
	"""
	contract = frappe.get_doc("Contract", contract_name)

	# Check existing row
	existing_row = None
	for row in contract.get("erp_references", []):
		if row.reference_doctype == reference_doctype and row.reference_name == reference_name:
			existing_row = row
			break

	if existing_row:
		existing_row.amount = flt(amount)
		existing_row.currency = currency
		existing_row.status = status
		existing_row.last_synced_on = now_datetime()
	else:
		contract.append("erp_references", {
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"reference_role": reference_role,
			"direction": "ERP -> Contract",
			"amount": flt(amount),
			"currency": currency,
			"status": status,
			"last_synced_on": now_datetime()
		})

	contract.flags.ignore_validate_update_after_submit = True
	contract.save(ignore_permissions=True)


def unlink_transaction_from_contract(contract_name: str, reference_doctype: str, reference_name: str) -> None:
	"""Updates the linked ERP reference row status to Cancelled upon ERP transaction cancellation."""
	contract = frappe.get_doc("Contract", contract_name)
	for row in contract.get("erp_references", []):
		if row.reference_doctype == reference_doctype and row.reference_name == reference_name:
			row.status = "Cancelled"
			row.last_synced_on = now_datetime()
			break
	contract.save(ignore_permissions=True)


def get_contract_for_doc(doc) -> str:
	"""Finds linked contract from explicit custom field 'contract' or matching customer."""
	if hasattr(doc, "contract") and doc.contract:
		return doc.contract
	return None


def sync_opportunity(doc, method=None):
	"""Syncs submitted Opportunity with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return
	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Opportunity",
		reference_name=doc.name,
		reference_role="Source",
		amount=flt(doc.get("opportunity_amount")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)


def sync_quotation(doc, method=None):
	"""Syncs submitted Quotation with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return
	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Quotation",
		reference_name=doc.name,
		reference_role="Source",
		amount=flt(doc.get("grand_total") or doc.get("net_total")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)


def sync_sales_order(doc, method=None):
	"""Syncs submitted Sales Order with linked Contract and checks commercial leakage."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return

	amount = flt(doc.get("grand_total") or doc.get("net_total"))
	currency = doc.get("currency") or "USD"

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Sales Order",
		reference_name=doc.name,
		reference_role="Fulfillment",
		amount=amount,
		currency=currency,
		status=doc.get("status") or "Submitted"
	)

	# Trigger commercial leakage audit
	try:
		from nsd_contract_management.integrations.leakage_engine import check_sales_order_rates
		check_sales_order_rates(doc, contract_name)
	except Exception:
		frappe.log_error(title="Sales Order Rate Audit Error", message=frappe.get_traceback())


def sync_sales_order_cancel(doc, method=None):
	"""Handles Sales Order cancellation."""
	contract_name = get_contract_for_doc(doc)
	if contract_name:
		unlink_transaction_from_contract(contract_name, "Sales Order", doc.name)


def sync_delivery_note(doc, method=None):
	"""Syncs submitted Delivery Note with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return
	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Delivery Note",
		reference_name=doc.name,
		reference_role="Fulfillment",
		amount=flt(doc.get("grand_total")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)


def sync_sales_invoice(doc, method=None):
	"""Syncs submitted Sales Invoice with linked Contract and audits billing totals."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return

	amount = flt(doc.get("grand_total") or doc.get("net_total"))
	currency = doc.get("currency") or "USD"

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Sales Invoice",
		reference_name=doc.name,
		reference_role="Billing",
		amount=amount,
		currency=currency,
		status=doc.get("status") or "Submitted"
	)

	try:
		from nsd_contract_management.integrations.leakage_engine import check_invoice_item_rate_leakage
		check_invoice_item_rate_leakage(doc, contract_name, is_sales=True)
	except Exception:
		frappe.log_error(title="Sales Invoice Rate Audit Error", message=frappe.get_traceback())


def sync_sales_invoice_cancel(doc, method=None):
	"""Handles Sales Invoice cancellation."""
	contract_name = get_contract_for_doc(doc)
	if contract_name:
		unlink_transaction_from_contract(contract_name, "Sales Invoice", doc.name)
