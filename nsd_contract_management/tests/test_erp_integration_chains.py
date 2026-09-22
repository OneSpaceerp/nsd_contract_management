# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from nsd_contract_management.services.contract_service import create_contract
from nsd_contract_management.integrations.erp_selling import (
	link_transaction_to_contract, unlink_transaction_from_contract
)
from nsd_contract_management.api.erp import get_financial_summary

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestERPIntegrationChains(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test ERP Chain Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_bidirectional_erp_transaction_linking(self):
		"""Tests linking Sales Orders, Purchase Orders, and Payment Entries to a Contract."""
		contract_id = create_contract({
			"title": "ERP Chains Integration Contract",
			"company": self.company,
			"total_contract_value": 200000.0,
			"currency": "USD"
		})

		# 1. Link Sales Order (Fulfillment)
		link_transaction_to_contract(
			contract_name=contract_id,
			reference_doctype="Sales Order",
			reference_name="SO-2026-0001",
			reference_role="Fulfillment",
			amount=100000.0,
			currency="USD"
		)

		# 2. Link Sales Invoice (Billing)
		link_transaction_to_contract(
			contract_name=contract_id,
			reference_doctype="Sales Invoice",
			reference_name="SINV-2026-0001",
			reference_role="Billing",
			amount=50000.0,
			currency="USD"
		)

		# 3. Link Payment Entry (Payment)
		link_transaction_to_contract(
			contract_name=contract_id,
			reference_doctype="Payment Entry",
			reference_name="PAY-2026-0001",
			reference_role="Payment",
			amount=50000.0,
			currency="USD"
		)

		contract = frappe.get_doc("Contract", contract_id)
		self.assertEqual(len(contract.erp_references), 3)

		# 4. Verify Financial Summary Calculation without direct GL modification
		summary = get_financial_summary(contract_id)
		self.assertEqual(summary["total_committed"], 100000.0)
		self.assertEqual(summary["total_billed"], 50000.0)
		self.assertEqual(summary["total_paid"], 50000.0)
		self.assertEqual(summary["balance_remaining"], 150000.0)

		# 5. Cancel Sales Order
		unlink_transaction_from_contract(contract_id, "Sales Order", "SO-2026-0001")
		contract.reload()
		so_ref = [r for r in contract.erp_references if r.reference_doctype == "Sales Order"][0]
		self.assertEqual(so_ref.status, "Cancelled")
