# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract, unlink_transaction_from_contract, get_contract_for_doc


def sync_purchase_order(doc, method=None):
	"""Syncs submitted Purchase Order with linked Contract and audits procurement budget."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		# Check uncontracted spend
		try:
			from nsd_contract_management.integrations.leakage_engine import check_uncontracted_spend
			check_uncontracted_spend(doc)
		except Exception:
			pass
		return

	amount = flt(doc.get("grand_total") or doc.get("net_total"))
	currency = doc.get("currency") or "USD"

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Purchase Order",
		reference_name=doc.name,
		reference_role="Fulfillment",
		amount=amount,
		currency=currency,
		status=doc.get("status") or "Submitted"
	)

	# Audit spend against contract ceiling
	try:
		from nsd_contract_management.integrations.leakage_engine import check_contract_value_overspend
		check_contract_value_overspend(contract_name)
	except Exception:
		frappe.log_error(title="PO Budget Audit Error", message=frappe.get_traceback())


def sync_purchase_order_cancel(doc, method=None):
	"""Handles Purchase Order cancellation."""
	contract_name = get_contract_for_doc(doc)
	if contract_name:
		unlink_transaction_from_contract(contract_name, "Purchase Order", doc.name)


def sync_purchase_receipt(doc, method=None):
	"""Syncs submitted Purchase Receipt with linked Contract."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return
	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Purchase Receipt",
		reference_name=doc.name,
		reference_role="Fulfillment",
		amount=flt(doc.get("grand_total")),
		currency=doc.get("currency") or "USD",
		status=doc.get("status") or "Submitted"
	)


def sync_purchase_invoice(doc, method=None):
	"""Syncs submitted Purchase Invoice with linked Contract and audits supplier pricing."""
	contract_name = get_contract_for_doc(doc)
	if not contract_name:
		return

	amount = flt(doc.get("grand_total") or doc.get("net_total"))
	currency = doc.get("currency") or "USD"

	link_transaction_to_contract(
		contract_name=contract_name,
		reference_doctype="Purchase Invoice",
		reference_name=doc.name,
		reference_role="Billing",
		amount=amount,
		currency=currency,
		status=doc.get("status") or "Submitted"
	)

	try:
		from nsd_contract_management.integrations.leakage_engine import check_invoice_item_rate_leakage
		check_invoice_item_rate_leakage(doc, contract_name, is_sales=False)
	except Exception:
		frappe.log_error(title="Purchase Invoice Rate Audit Error", message=frappe.get_traceback())


def sync_purchase_invoice_cancel(doc, method=None):
	"""Handles Purchase Invoice cancellation."""
	contract_name = get_contract_for_doc(doc)
	if contract_name:
		unlink_transaction_from_contract(contract_name, "Purchase Invoice", doc.name)
