# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, now_datetime
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract, unlink_transaction_from_contract, get_contract_for_doc


def sync_payment_entry(doc, method=None):
	"""
	Synchronizes submitted Payment Entry with linked Contract(s).
	Supports direct single contract link as well as multi-contract payment allocations.
	Preserves pure ERPNext accounting truth: never touches GL entries directly.
	"""
	contract_name = get_contract_for_doc(doc)
	allocated_contracts = []

	# Check child allocation table on payment entry if present
	if hasattr(doc, "contract_allocations") and doc.contract_allocations:
		for alloc in doc.contract_allocations:
			if alloc.contract:
				allocated_contracts.append((alloc.contract, flt(alloc.allocated_amount)))

	if not allocated_contracts and contract_name:
		amount = flt(doc.get("paid_amount") or doc.get("received_amount"))
		allocated_contracts.append((contract_name, amount))

	for c_name, c_amt in allocated_contracts:
		link_transaction_to_contract(
			contract_name=c_name,
			reference_doctype="Payment Entry",
			reference_name=doc.name,
			reference_role="Payment",
			amount=c_amt,
			currency=doc.get("paid_from_account_currency") or doc.get("paid_to_account_currency") or "USD",
			status=doc.get("status") or "Submitted"
		)

		# Check if any payment obligation can be marked fulfilled
		open_payment_obs = frappe.get_all(
			"Contract Obligation",
			filters={"contract": c_name, "obligation_type": "Payment", "status": "Pending"},
			fields=["name"]
		)
		if open_payment_obs:
			from nsd_contract_management.services.obligation_service import complete_obligation
			try:
				complete_obligation(open_payment_obs[0].name, completed_by=doc.owner)
			except Exception:
				pass


def sync_payment_entry_cancel(doc, method=None):
	"""Handles Payment Entry cancellation."""
	contract_name = get_contract_for_doc(doc)
	if contract_name:
		unlink_transaction_from_contract(contract_name, "Payment Entry", doc.name)
