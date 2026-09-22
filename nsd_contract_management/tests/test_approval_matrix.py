# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from nsd_contract_management.services.contract_service import create_contract
from nsd_contract_management.services.approval_service import (
	evaluate_approval_requirements, submit_for_approval, approve_step, reject_step
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestApprovalMatrix(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Approval Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_approval_threshold_evaluation(self):
		"""Verifies that contract values and risk triggers populate the correct required approval roles."""
		# Low value contract ($50k) -> Contract Manager only
		c1 = create_contract({
			"title": "Low Value Contract",
			"company": self.company,
			"total_contract_value": 50000.0,
			"risk_level": "Low"
		})
		steps1 = evaluate_approval_requirements(c1)
		roles1 = [s["approver_role"] for s in steps1]
		self.assertIn("Contract Manager", roles1)
		self.assertNotIn("CFO", roles1)
		self.assertNotIn("CEO", roles1)

		# $1.5M contract -> Must require CFO
		c2 = create_contract({
			"title": "High Value Contract",
			"company": self.company,
			"total_contract_value": 1500000.0,
			"risk_level": "Low"
		})
		steps2 = evaluate_approval_requirements(c2)
		roles2 = [s["approver_role"] for s in steps2]
		self.assertIn("CFO", roles2)

		# $6M + Critical Risk -> CEO, CFO, and General Counsel
		c3 = create_contract({
			"title": "Enterprise Strategic Contract",
			"company": self.company,
			"total_contract_value": 6000000.0,
			"risk_level": "Critical"
		})
		steps3 = evaluate_approval_requirements(c3)
		roles3 = [s["approver_role"] for s in steps3]
		self.assertIn("CEO", roles3)
		self.assertIn("CFO", roles3)
		self.assertIn("General Counsel", roles3)

	def test_approval_workflow_execution(self):
		"""Tests submitting for approval, advancing step approval, and final contract approval."""
		c_id = create_contract({
			"title": "Multi-Step Approval Execution",
			"company": self.company,
			"total_contract_value": 150000.0,
			"status": "In Review"
		})

		# Submit
		approval_id = submit_for_approval(c_id, submitted_by="test@example.com")
		contract = frappe.get_doc("Contract", c_id)
		self.assertEqual(contract.status, "Approval Pending")

		approval = frappe.get_doc("Contract Approval", approval_id)
		self.assertEqual(approval.status, "Pending")

		# Approve step 1
		approve_step(approval_id, step_idx=1, approver="manager@example.com", comments="Commercial terms look good.")
		contract.reload()
		self.assertEqual(contract.status, "Approved")

	def test_rejection_workflow(self):
		"""Tests rejection of an approval step."""
		c_id = create_contract({
			"title": "Rejection Step Test",
			"company": self.company,
			"total_contract_value": 100000.0,
			"status": "In Review"
		})

		approval_id = submit_for_approval(c_id)
		reject_step(approval_id, step_idx=1, approver="cfo@example.com", reason="Budget exceeded for Q3.")

		contract = frappe.get_doc("Contract", c_id)
		self.assertEqual(contract.status, "Rejected")
