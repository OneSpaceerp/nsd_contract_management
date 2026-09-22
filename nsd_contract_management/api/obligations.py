# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.obligation_service import (
	complete_obligation, waive_obligation
)


@frappe.whitelist()
def complete(obligation_name: str, evidence_file: str = None) -> dict:
	"""RPC: Marks contract obligation as fulfilled."""
	complete_obligation(obligation_name, evidence_file=evidence_file, completed_by=frappe.session.user)
	return {"obligation_name": obligation_name, "status": "Fulfilled"}


@frappe.whitelist()
def waive(obligation_name: str, reason: str) -> dict:
	"""RPC: Waives an obligation with mandatory business reason."""
	waive_obligation(obligation_name, reason=reason, waived_by=frappe.session.user)
	return {"obligation_name": obligation_name, "status": "Waived"}


@frappe.whitelist()
def reopen(obligation_name: str) -> dict:
	"""RPC: Reopens a fulfilled or waived obligation."""
	frappe.db.set_value("Contract Obligation", obligation_name, "status", "Pending")
	return {"obligation_name": obligation_name, "status": "Pending"}


@frappe.whitelist()
def add_evidence(obligation_name: str, file_url: str) -> dict:
	"""RPC: Attaches proof of fulfillment file."""
	frappe.db.set_value("Contract Obligation", obligation_name, "evidence_file", file_url)
	return {"obligation_name": obligation_name, "evidence_file": file_url}
