# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from nsd_contract_management.services.contract_service import (
	transition_status, apply_legal_hold, release_legal_hold
)
from nsd_contract_management.services.intake_service import convert_request_to_contract
from nsd_contract_management.services.contract_version_service import create_version, seal_executed_version
from nsd_contract_management.services.signature_service import build_signature_packet, dispatch_signature_request
from nsd_contract_management.services.termination_service import initiate_termination


@frappe.whitelist()
def create_from_request(request_name: str) -> dict:
	"""RPC: Converts an accepted Contract Request into a Contract draft."""
	contract_name = convert_request_to_contract(request_name)
	return {"contract_name": contract_name, "message": _("Contract successfully generated from request.")}


@frappe.whitelist()
def submit_for_review(contract_name: str, reviewers: str = None) -> dict:
	"""RPC: Submits contract for formal review."""
	from nsd_contract_management.services.review_service import start_review
	reviewer_list = [r.strip() for r in reviewers.split(",")] if reviewers else []
	review_name = start_review(contract_name, reviewers=reviewer_list)
	return {"review_name": review_name, "status": "In Review"}


@frappe.whitelist()
def start_negotiation(contract_name: str, counterparty_contact: str = None) -> dict:
	"""RPC: Opens negotiation round for contract."""
	from nsd_contract_management.services.negotiation_service import create_negotiation_round
	round_name = create_negotiation_round(contract_name, counterparty_contact=counterparty_contact)
	return {"round_name": round_name, "status": "Negotiation"}


@frappe.whitelist()
def create_contract_version(contract_name: str, title: str = None, content: str = None, file_url: str = None) -> dict:
	"""RPC: Creates a new semantic contract version with cryptographic integrity hash."""
	ver_name = create_version(contract_name, title=title, content=content, file_url=file_url)
	return {"version_name": ver_name}


@frappe.whitelist()
def mark_approved(contract_name: str) -> dict:
	"""RPC: Directly marks contract approved if user has requisite authority."""
	frappe.only_for(["System Manager", "General Counsel", "Contract Manager"])
	transition_status(contract_name, "Approved", reason="Approved via administrative action")
	return {"contract_name": contract_name, "status": "Approved"}


@frappe.whitelist()
def send_for_signature(contract_name: str, provider: str = "Native") -> dict:
	"""RPC: Builds and dispatches signature envelope."""
	sig_req = build_signature_packet(contract_name, provider_name=provider)
	dispatch_res = dispatch_signature_request(sig_req)
	return dispatch_res


@frappe.whitelist()
def mark_executed(contract_name: str, signed_file_url: str = None) -> dict:
	"""RPC: Completes execution, seals version and triggers post-execution automations."""
	frappe.only_for(["System Manager", "General Counsel", "Contract Manager"])
	seal_executed_version(contract_name, signed_file_url=signed_file_url or "/files/executed_contract.pdf")
	transition_status(contract_name, "Executed", reason="Manually marked executed with signed agreement")
	return {"contract_name": contract_name, "status": "Executed"}


@frappe.whitelist()
def activate(contract_name: str) -> dict:
	"""RPC: Transitions executed contract to Effective."""
	transition_status(contract_name, "Effective", reason="Contract activated into effective lifecycle")
	return {"contract_name": contract_name, "status": "Effective"}


@frappe.whitelist()
def put_on_hold(contract_name: str, reason: str) -> dict:
	"""RPC: Places contract under legal hold lock."""
	apply_legal_hold(contract_name, reason=reason)
	return {"contract_name": contract_name, "legal_hold": 1}


@frappe.whitelist()
def resume(contract_name: str, reason: str = None) -> dict:
	"""RPC: Releases legal hold and returns contract to active status."""
	release_legal_hold(contract_name, reason=reason or "Legal hold released")
	return {"contract_name": contract_name, "legal_hold": 0}


@frappe.whitelist()
def terminate(contract_name: str, termination_type: str = "Convenience", reason: str = None) -> dict:
	"""RPC: Initiates formal termination (guarded by legal hold checks)."""
	term_name = initiate_termination(contract_name, termination_type=termination_type, reason=reason or "Termination requested via API")
	return {"termination_name": term_name, "status": "Terminated"}


@frappe.whitelist()
def archive(contract_name: str) -> dict:
	"""RPC: Moves contract to Archived."""
	transition_status(contract_name, "Archived", reason="Archived via API")
	return {"contract_name": contract_name, "status": "Archived"}
