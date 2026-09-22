# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract


def sync_asset_contract(doc, method=None):
	"""Syncs Asset maintenance and lease contracts."""
	if not hasattr(doc, "contract") or not doc.contract:
		return

	link_transaction_to_contract(
		contract_name=doc.contract,
		reference_doctype="Asset",
		reference_name=doc.name,
		reference_role="Asset",
		amount=0.0,
		status=doc.get("status") or "Draft"
	)
