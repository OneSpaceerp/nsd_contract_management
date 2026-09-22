# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from nsd_contract_management.services.contract_service import create_contract
from nsd_contract_management.integrations.erp_selling import link_transaction_to_contract
from nsd_contract_management.integrations.leakage_engine import (
	create_leakage_finding, check_contract_value_overspend
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestFinancialLeakage(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Leakage Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_leakage_finding_creation_and_deduplication(self):
		"""Ensures leakage incidents are tracked and duplicate findings for the same doc are prevented."""
		c_id = create_contract({
			"title": "Leakage Audited Contract",
			"company": self.company,
			"total_contract_value": 100000.0
		})

		f1 = create_leakage_finding(
			contract_name=c_id,
			rule="Price Variance",
			source_doctype="Sales Invoice",
			source_name="SINV-TEST-001",
			expected_val=5000.0,
			actual_val=4200.0,
			variance=800.0,
			financial_impact=800.0,
			severity="Medium"
		)
		self.assertTrue(bool(f1))

		# Calling again with identical parameters should return existing finding ID
		f2 = create_leakage_finding(
			contract_name=c_id,
			rule="Price Variance",
			source_doctype="Sales Invoice",
			source_name="SINV-TEST-001",
			expected_val=5000.0,
			actual_val=4200.0,
			variance=800.0,
			financial_impact=800.0,
			severity="Medium"
		)
		self.assertEqual(f1, f2)

	def test_contract_overspend_detection(self):
		"""Tests automated detection when total committed POs exceed contracted financial ceiling."""
		c_id = create_contract({
			"title": "Capped Procurement Contract",
			"company": self.company,
			"total_contract_value": 50000.0,
			"currency": "USD"
		})

		# Link POs totaling $75,000 (exceeds $50,000 cap by $25,000)
		link_transaction_to_contract(
			contract_name=c_id,
			reference_doctype="Purchase Order",
			reference_name="PO-OVER-001",
			reference_role="Fulfillment",
			amount=75000.0,
			currency="USD"
		)

		check_contract_value_overspend(c_id)

		findings = frappe.get_all(
			"Contract Leakage Finding",
			filters={"contract": c_id, "rule": "Billed Beyond Quantity"},
			fields=["financial_impact", "severity"]
		)
		self.assertGreater(len(findings), 0)
		self.assertEqual(findings[0]["financial_impact"], 25000.0)
		self.assertEqual(findings[0]["severity"], "High")
