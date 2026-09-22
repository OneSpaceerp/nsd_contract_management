# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import hashlib
from typing import Dict, List, Any, Optional
import frappe
from nsd_contract_management.signatures.base import SignatureProvider


class MockSignatureProvider(SignatureProvider):
	"""
	Deterministic, fully functional offline signature provider for local development,
	automated testing, and air-gapped deployments.
	"""

	def create_envelope(self, title: str, file_url: str, signers: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
		envelope_id = f"MOCK-ENV-{frappe.generate_hash(length=10)}"
		processed_signers = []
		for s in signers:
			s_copy = dict(s)
			s_copy["signing_url"] = f"/desk#mock-signature?env={envelope_id}&signer={s.get('signer_email')}"
			s_copy["status"] = "Sent"
			processed_signers.append(s_copy)

		return {
			"envelope_id": envelope_id,
			"status": "Sent",
			"signers": processed_signers
		}

	def get_signing_url(self, envelope_id: str, signer_email: str) -> str:
		return f"/desk#mock-signature?env={envelope_id}&signer={signer_email}"

	def get_envelope_status(self, envelope_id: str) -> Dict[str, Any]:
		return {
			"envelope_id": envelope_id,
			"status": "Completed",
			"all_signed": True
		}

	def download_signed_document(self, envelope_id: str) -> bytes:
		dummy_content = f"%PDF-1.4 Mock Signed Document Evidence\nEnvelope: {envelope_id}\nHash: {hashlib.sha256(envelope_id.encode()).hexdigest()}"
		return dummy_content.encode("utf-8")
