# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from nsd_contract_management.services.contract_service import create_contract, transition_status
from nsd_contract_management.services.signature_service import (
	build_signature_packet, dispatch_signature_request, handle_signature_callback
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestSignatureService(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Signature Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_signature_packet_and_execution_lifecycle(self):
		"""Tests the complete eSignature lifecycle: packet assembly, dispatch, signing webhook, and execution sealing."""
		contract_id = create_contract({
			"title": "Vendor Supply Agreement - Signature Test",
			"company": self.company,
			"total_contract_value": 85000.0,
			"status": "Draft"
		})

		# Fast forward to Approved
		transition_status(contract_id, "In Review")
		transition_status(contract_id, "Approval Pending")
		transition_status(contract_id, "Approved")

		# 1. Build Packet
		sig_req_id = build_signature_packet(contract_id, provider_name="Mock")
		sig_req = frappe.get_doc("Signature Request", sig_req_id)
		self.assertEqual(sig_req.status, "Draft")
		self.assertGreater(len(sig_req.signers), 0)

		# 2. Dispatch
		dispatch_res = dispatch_signature_request(sig_req_id)
		self.assertEqual(dispatch_res["status"], "Sent")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Signature Pending")

		# 3. Handle Inbound Signer Callback
		signer_email = sig_req.signers[0].signer_email
		callback_payload = {
			"envelope_id": sig_req.external_envelope_id,
			"event_type": "signed",
			"signer_email": signer_email,
			"signed_file_url": "/files/test_signed_envelope.pdf"
		}
		result = handle_signature_callback("Mock", callback_payload, idempotency_key="TEST-IDEMP-001")
		self.assertTrue(result["success"])

		# 4. Verify contract executed
		contract = frappe.get_doc("Contract", contract_id)
		self.assertEqual(contract.status, "Executed")
		self.assertTrue(bool(contract.current_version))

		ver = frappe.get_doc("Contract Version", contract.current_version)
		self.assertEqual(ver.is_executed, 1)
		self.assertEqual(ver.is_locked, 1)
