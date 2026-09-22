# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.utils import nowdate, add_months
from nsd_contract_management.services.contract_service import (
	create_contract, transition_status, apply_legal_hold, release_legal_hold
)
from nsd_contract_management.services.contract_version_service import (
	create_version, seal_executed_version, compare_versions
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestContractLifecycle(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Lifecycle Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_lifecycle_state_transitions(self):
		"""Tests linear deterministic status transitions and guards."""
		contract_id = create_contract({
			"title": "MSA Lifecycle Unit Test",
			"company": self.company,
			"total_contract_value": 50000.0,
			"currency": "USD"
		})

		contract = frappe.get_doc("Contract", contract_id)
		self.assertEqual(contract.status, "Draft")

		# Valid progression
		transition_status(contract_id, "In Review")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "In Review")

		transition_status(contract_id, "Approval Pending")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Approval Pending")

		transition_status(contract_id, "Approved")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Approved")

		transition_status(contract_id, "Signature Pending")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Signature Pending")

		seal_executed_version(contract_id, "/files/signed_test.pdf")
		transition_status(contract_id, "Executed")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Executed")

		transition_status(contract_id, "Effective")
		self.assertEqual(frappe.db.get_value("Contract", contract_id, "status"), "Effective")

	def test_invalid_lifecycle_transition_raises(self):
		"""Ensures illegal status jump raises ValidationError."""
		contract_id = create_contract({
			"title": "Invalid Transition Test",
			"company": self.company,
			"total_contract_value": 25000.0
		})

		with self.assertRaises(frappe.ValidationError):
			# Cannot jump directly from Draft to Executed
			transition_status(contract_id, "Executed")

	def test_legal_hold_blocks_termination_and_cancellation(self):
		"""Ensures active legal hold strictly blocks termination, cancellation, and deletion."""
		contract_id = create_contract({
			"title": "Legal Hold Enforced Contract",
			"company": self.company,
			"total_contract_value": 100000.0
		})

		# Place under legal hold
		apply_legal_hold(contract_id, reason="Pending regulatory inquiry CASE-99.")
		contract = frappe.get_doc("Contract", contract_id)
		self.assertEqual(contract.legal_hold, 1)

		# Attempting to move to Cancelled must raise PermissionError
		with self.assertRaises(frappe.PermissionError):
			transition_status(contract_id, "Cancelled")

		# Release hold
		release_legal_hold(contract_id, reason="Inquiry resolved.")
		contract.reload()
		self.assertEqual(contract.legal_hold, 0)

	def test_version_sealing_and_comparison(self):
		"""Tests version creation, diff comparison, and executed version locking."""
		contract_id = create_contract({
			"title": "Version Hash Verification",
			"company": self.company
		})

		v1 = create_version(contract_id, content="Clause 1: Initial terms.")
		v2 = create_version(contract_id, content="Clause 1: Revised terms.\nClause 2: New terms.")

		diff_result = compare_versions(v1, v2)
		self.assertFalse(diff_result["identical"])
		self.assertGreater(diff_result["additions_count"], 0)

		# Seal executed version
		v_exec = seal_executed_version(contract_id, "/files/executed.pdf", signed_content="Clause 1: Final executed.")
		ver_doc = frappe.get_doc("Contract Version", v_exec)
		self.assertEqual(ver_doc.is_locked, 1)
		self.assertEqual(ver_doc.is_executed, 1)
		self.assertTrue(bool(ver_doc.content_hash))
