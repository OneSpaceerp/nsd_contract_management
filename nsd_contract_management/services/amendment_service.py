# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime
from nsd_contract_management.services.contract_service import transition_status
from nsd_contract_management.services.contract_version_service import create_version


def create_amendment(
	contract_name: str,
	amendment_type: str = "Scope Change",
	effective_date: str = None,
	description: str = None,
	new_value: float = None,
	new_end_date: str = None
) -> str:
	"""
	Initiates a contract amendment process, setting contract status to Amendment In Progress.
	Strictly blocks amendment creation if contract is under active Legal Hold.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.legal_hold:
		frappe.throw(
			_("Contract {0} is under an active Legal Hold and cannot be amended.").format(contract_name),
			frappe.PermissionError
		)

	if contract.status not in ["Effective", "Executed"]:
		frappe.throw(
			_("Only Effective or Executed contracts can be amended (Current: {0}).").format(contract.status),
			frappe.ValidationError
		)

	existing_count = frappe.db.count("Contract Amendment", {"contract": contract_name})
	amendment_number = existing_count + 1

	amd = frappe.new_doc("Contract Amendment")
	amd.contract = contract_name
	amd.amendment_number = f"AMD-{contract_name}-{amendment_number:02d}"
	amd.amendment_type = amendment_type
	amd.status = "Draft"
	amd.effective_date = effective_date or contract.effective_date
	amd.description = description
	amd.new_contract_value = new_value
	amd.new_end_date = new_end_date
	amd.insert()

	transition_status(contract_name, "Amendment In Progress", reason=f"Amendment {amd.amendment_number} drafted")

	return amd.name


def apply_amendment(amendment_name: str) -> None:
	"""
	Applies the approved amendment to the master Contract: updates values, terms,
	seals a new Contract Version, and transitions contract back to Effective.
	"""
	amd = frappe.get_doc("Contract Amendment", amendment_name)
	contract = frappe.get_doc("Contract", amd.contract)

	if contract.legal_hold:
		frappe.throw(_("Contract {0} is under active Legal Hold.").format(contract.name), frappe.PermissionError)

	updates = {}
	if amd.new_contract_value:
		updates["total_contract_value"] = amd.new_contract_value
	if amd.new_end_date:
		updates["end_date"] = amd.new_end_date

	if updates:
		frappe.db.set_value("Contract", contract.name, updates)

	# Generate new major contract version
	ver_name = create_version(
		contract_name=contract.name,
		title=f"{contract.title} - Amended ({amd.amendment_number})",
		content=f"# Amended Agreement: {contract.title}\n\nAmendment: {amd.amendment_number}\n\nDetails:\n{amd.description or ''}",
		change_summary=f"Applied Amendment {amd.amendment_number}: {amd.description or ''}",
		is_major=True
	)

	amd.db_set("amended_version", ver_name)
	amd.db_set("status", "Applied")

	transition_status(contract.name, "Effective", reason=f"Amendment {amd.amendment_number} successfully applied")
