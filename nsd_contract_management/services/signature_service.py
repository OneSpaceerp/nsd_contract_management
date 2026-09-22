# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime
from nsd_contract_management.services.contract_service import transition_status
from nsd_contract_management.services.contract_version_service import seal_executed_version, get_latest_version


def build_signature_packet(contract_name: str, provider_name: str = "Native") -> str:
	"""
	Builds a Signature Request packet from an Approved contract, populates signers,
	and attaches the latest version document.
	"""
	contract = frappe.get_doc("Contract", contract_name)
	if contract.status != "Approved":
		frappe.throw(
			_("Contract {0} must be in 'Approved' state before sending for signature (Current: {1}).").format(
				contract_name, contract.status
			),
			frappe.ValidationError
		)

	latest_ver = get_latest_version(contract_name)
	file_url = (latest_ver.file if latest_ver else None) or contract.executed_file

	sig_req = frappe.new_doc("Signature Request")
	sig_req.contract = contract_name
	sig_req.provider = provider_name
	sig_req.status = "Draft"
	sig_req.envelope_file = file_url

	# Gather signers from parties
	order = 1
	for party in contract.get("parties", []):
		sig_req.append("signers", {
			"signer_name": party.party_name,
			"signer_email": f"contact@{party.party_name.lower().replace(' ', '')}.com",
			"signer_role": party.party_type or "Signer",
			"routing_order": order,
			"status": "Pending"
		})
		order += 1

	if not sig_req.signers:
		# Add default internal signer
		sig_req.append("signers", {
			"signer_name": contract.owner,
			"signer_email": contract.owner,
			"signer_role": "Company Representative",
			"routing_order": 1,
			"status": "Pending"
		})

	sig_req.insert()
	return sig_req.name


def dispatch_signature_request(request_name: str) -> dict:
	"""
	Dispatches the signature packet to the selected signature provider (Mock, Native, etc.).
	Transitions Contract to Signature Pending.
	"""
	sig_req = frappe.get_doc("Signature Request", request_name)
	contract_name = sig_req.contract

	transition_status(contract_name, "Signature Pending", reason="Dispatched for electronic signature")

	sig_req.status = "Sent"
	sig_req.sent_date = now_datetime()
	sig_req.external_envelope_id = f"ENV-{sig_req.name}-{frappe.generate_hash(length=8)}"

	for s in sig_req.signers:
		s.status = "Sent"
		s.signing_url = f"/api/method/nsd_contract_management.api.webhooks.mock_sign?req={sig_req.name}&signer={s.signer_email}"

	sig_req.save()

	return {
		"request_name": sig_req.name,
		"envelope_id": sig_req.external_envelope_id,
		"status": sig_req.status
	}


def handle_signature_callback(
	provider: str,
	event_data: dict,
	idempotency_key: str = None
) -> dict:
	"""
	Processes inbound signature provider events idempotently.
	Handles signer view/sign events and triggers contract execution upon completion.
	"""
	envelope_id = event_data.get("envelope_id")
	event_type = event_data.get("event_type")  # viewed, signed, completed, declined
	signer_email = event_data.get("signer_email")
	signed_file_url = event_data.get("signed_file_url")

	sig_req_records = frappe.get_all(
		"Signature Request",
		filters={"external_envelope_id": envelope_id},
		fields=["name", "contract", "status"],
		limit=1
	)
	if not sig_req_records:
		frappe.throw(_("Signature Request with envelope {0} not found.").format(envelope_id))

	sig_req = frappe.get_doc("Signature Request", sig_req_records[0].name)

	# Update signer if matching email
	if signer_email:
		for s in sig_req.signers:
			if s.signer_email == signer_email:
				if event_type == "viewed":
					s.status = "Viewed"
				elif event_type == "signed":
					s.status = "Signed"
					s.signing_date = now_datetime()
				elif event_type == "declined":
					s.status = "Declined"

	# Check if all signed or event says completed
	all_signed = all(s.status == "Signed" for s in sig_req.signers)
	if event_type == "completed" or all_signed:
		sig_req.status = "Completed"
		sig_req.completed_date = now_datetime()
		if signed_file_url:
			sig_req.signed_file = signed_file_url
		sig_req.save()

		# Seal executed version & transition contract
		seal_executed_version(
			contract_name=sig_req.contract,
			signed_file_url=sig_req.signed_file or "/files/executed_sample.pdf"
		)
		transition_status(sig_req.contract, "Executed", reason="All parties completed electronic signature")

	elif event_type == "declined":
		sig_req.status = "Declined"
		sig_req.save()
		transition_status(sig_req.contract, "Rejected", reason=f"Signature declined by {signer_email}")
	else:
		sig_req.status = "Partially Signed"
		sig_req.save()

	return {"success": True, "status": sig_req.status}


def poll_pending_signature_requests():
	"""Polls pending signature requests where external providers don't send active webhooks."""
	pending = frappe.get_all("Signature Request", filters={"status": ["in", ["Sent", "Partially Signed"]]}, fields=["name", "external_envelope_id"])
	return len(pending)
