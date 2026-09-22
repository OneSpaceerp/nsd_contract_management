# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from nsd_contract_management.services.signature_service import handle_signature_callback


@frappe.whitelist(allow_guest=True)
def signature_webhook() -> dict:
	"""
	Inbound webhook handler for electronic signature providers.
	Guaranteed idempotent via Idempotency-Key header or event ID.
	"""
	data = frappe.request.get_json() or {}
	idempotency_key = frappe.get_request_header("Idempotency-Key") or data.get("event_id")

	if idempotency_key:
		cached_result = frappe.cache().get_value(f"webhook_idemp_{idempotency_key}")
		if cached_result:
			return json.loads(cached_result)

	provider = data.get("provider", "Native")
	result = handle_signature_callback(provider, data, idempotency_key=idempotency_key)

	if idempotency_key:
		frappe.cache().set_value(f"webhook_idemp_{idempotency_key}", json.dumps(result), expires_in_sec=86400)

	return result


@frappe.whitelist(allow_guest=True)
def mock_sign(req: str, signer: str) -> dict:
	"""
	Simulates a counterparty signing action offline for dev testing and automated QA.
	"""
	sig_req = frappe.get_doc("Signature Request", req)
	event_data = {
		"envelope_id": sig_req.external_envelope_id,
		"event_type": "signed",
		"signer_email": signer,
		"signed_file_url": "/files/mock_signed_agreement.pdf"
	}
	res = handle_signature_callback("Mock", event_data)
	return {"success": True, "message": f"Successfully signed by {signer}", "status": res.get("status")}
