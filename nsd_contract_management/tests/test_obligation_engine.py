# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from frappe.utils import nowdate, add_days
from nsd_contract_management.services.contract_service import create_contract
from nsd_contract_management.services.obligation_service import (
	generate_obligations_from_clauses, evaluate_due_obligations, complete_obligation, waive_obligation
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestObligationEngine(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Obligation Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_obligation_generation_and_fulfillment(self):
		"""Tests automatic obligation creation, evidence requirements, and fulfillment."""
		contract_id = create_contract({
			"title": "Deliverables Fulfillment Contract",
			"company": self.company,
			"total_contract_value": 75000.0,
			"end_date": add_days(nowdate(), 45)
		})

		contract = frappe.get_doc("Contract", contract_id)
		contract.append("obligations", {
			"title": "Quarterly Penetration Test Report",
			"obligation_type": "Compliance",
			"due_date": add_days(nowdate(), 30),
			"evidence_required": 1
		})
		contract.save()

		generated = generate_obligations_from_clauses(contract_id)
		self.assertGreater(len(generated), 0)

		ob_name = generated[0]
		ob_doc = frappe.get_doc("Contract Obligation", ob_name)
		self.assertEqual(ob_doc.status, "Pending")

		# Fulfilling without evidence when evidence_required=1 must fail
		if ob_doc.evidence_required:
			with self.assertRaises(frappe.ValidationError):
				complete_obligation(ob_name, evidence_file=None)

		# Fulfill with evidence
		complete_obligation(ob_name, evidence_file="/files/pen_test_report_2026.pdf", completed_by="auditor@example.com")
		ob_doc.reload()
		self.assertEqual(ob_doc.status, "Fulfilled")
		self.assertEqual(ob_doc.evidence_file, "/files/pen_test_report_2026.pdf")

	def test_overdue_scan_and_waiver(self):
		"""Tests automated scan marking past-due obligations as Overdue and waiver workflow."""
		ob = frappe.new_doc("Contract Obligation")
		ob.title = "Past Due Audit Obligation"
		ob.obligation_type = "Audit"
		ob.due_date = add_days(nowdate(), -5)  # 5 days ago
		ob.status = "Pending"
		ob.insert()

		scan_result = evaluate_due_obligations()
		ob.reload()
		self.assertEqual(ob.status, "Overdue")

		# Waive obligation
		waive_obligation(ob.name, reason="Audit waived due to vendor SOC2 recertification.")
		ob.reload()
		self.assertEqual(ob.status, "Waived")
