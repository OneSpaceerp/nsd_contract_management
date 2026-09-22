# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.renewal_service import (
	generate_renewal_brief, calculate_notice_deadline
)


@frappe.whitelist()
def create(contract_name: str, proposed_end_date: str = None) -> dict:
	"""RPC: Creates a renewal tracking record for a contract."""
	contract = frappe.get_doc("Contract", contract_name)
	notice_deadline = calculate_notice_deadline(contract.end_date, contract.notice_period_days)

	ren = frappe.new_doc("Contract Renewal")
	ren.contract = contract_name
	ren.status = "Upcoming"
	ren.current_end_date = contract.end_date
	ren.notice_deadline = notice_deadline
	ren.proposed_end_date = proposed_end_date
	ren.auto_renewal = contract.auto_renewal
	ren.assigned_to = contract.owner
	ren.insert()

	return {"renewal_name": ren.name, "status": ren.status}


@frappe.whitelist()
def start(renewal_name: str) -> dict:
	"""RPC: Moves renewal status to Under Negotiation."""
	frappe.db.set_value("Contract Renewal", renewal_name, "status", "Under Negotiation")
	return {"renewal_name": renewal_name, "status": "Under Negotiation"}


@frappe.whitelist()
def approve(renewal_name: str) -> dict:
	"""RPC: Approves contract renewal and extends expiration date."""
	ren = frappe.get_doc("Contract Renewal", renewal_name)
	if not ren.proposed_end_date:
		frappe.throw(_("Proposed end date is required to approve renewal."))

	frappe.db.set_value("Contract", ren.contract, "end_date", ren.proposed_end_date)
	ren.status = "Approved"
	ren.save()

	return {"renewal_name": renewal_name, "status": "Approved", "new_end_date": ren.proposed_end_date}


@frappe.whitelist()
def mark_not_renewed(renewal_name: str, reason: str = None) -> dict:
	"""RPC: Records decision not to renew contract."""
	frappe.db.set_value("Contract Renewal", renewal_name, {
		"status": "Not Renewed",
		"renewal_notes": reason or "Contract not renewed."
	})
	return {"renewal_name": renewal_name, "status": "Not Renewed"}


@frappe.whitelist()
def generate_brief(renewal_name: str) -> dict:
	"""RPC: Compiles executive renewal brief."""
	brief = generate_renewal_brief(renewal_name)
	return {"renewal_name": renewal_name, "brief": brief}
