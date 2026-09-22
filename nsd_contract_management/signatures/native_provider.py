# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import hashlib
from typing import Dict, List, Any, Optional
import frappe
from frappe.utils import now_datetime
from nsd_contract_management.signatures.base import SignatureProvider


class NativeSignatureProvider(SignatureProvider):
	"""
	Native in-app Frappe signature provider utilizing built-in security tokens,
	audit logs, and internal desk signing interfaces.
	"""

	def create_envelope(self, title: str, file_url: str, signers: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		envelope_id = f"NAT-{frappe.generate_hash(length=12)}"
		processed_signers = []
		for s in signers:
			token = frappe.generate_hash(length=24)
			s_copy = dict(s)
			s_copy["signature_id"] = token
			s_copy["signing_url"] = f"/contract-sign?envelope={envelope_id}&token={token}"
			s_copy["status"] = "Sent"
			processed_signers.append(s_copy)

		return {
			"envelope_id": envelope_id,
			"status": "Sent",
			"signers": processed_signers
		}

	def get_signing_url(self, envelope_id: str, signer_email: str) -> str:
		return f"/contract-sign?envelope={envelope_id}&signer={signer_email}"

	def get_envelope_status(self, envelope_id: str) -> Dict[str, Any]:
		sig_reqs = frappe.get_all("Signature Request", filters={"external_envelope_id": envelope_id}, fields=["status"], limit=1)
		status = sig_reqs[0].status if sig_reqs else "Draft"
		return {
			"envelope_id": envelope_id,
			"status": status,
			"all_signed": status == "Completed"
		}

	def download_signed_document(self, envelope_id: str) -> bytes:
		sig_reqs = frappe.get_all("Signature Request", filters={"external_envelope_id": envelope_id}, fields=["signed_file"], limit=1)
		file_url = sig_reqs[0].signed_file if sig_reqs else None
		return f"Native Signed Contract: {file_url}".encode("utf-8")
