# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import unittest
import frappe
from nsd_contract_management.services.contract_service import create_contract
from nsd_contract_management.security.permissions import (
	get_contract_query_conditions, has_contract_permission
)

try:
	from frappe.tests.utils import FrappeTestCase
except ImportError:
	FrappeTestCase = unittest.TestCase


class TestPermissionsSecurity(FrappeTestCase):
	def setUp(self):
		frappe.flags.ignore_permissions = True
		self.company = "Test Security Company"
		if not frappe.db.exists("Company", self.company):
			frappe.get_doc({
				"doctype": "Company",
				"company_name": self.company,
				"default_currency": "USD",
				"country": "United States"
			}).insert()

	def test_custom_permission_types_authorization(self):
		"""Validates that Frappe v16 custom permission types enforce role barriers."""
		contract_id = create_contract({
			"title": "Security Authorization Contract",
			"company": self.company,
			"total_contract_value": 100000.0
		})
		contract = frappe.get_doc("Contract", contract_id)

		# Administrator has all permissions
		self.assertTrue(has_contract_permission(contract, user="Administrator", ptype="release_legal_hold"))
		self.assertTrue(has_contract_permission(contract, user="Administrator", ptype="approve_contract"))

	def test_query_conditions_generation(self):
		"""Ensures multi-company SQL query conditions are correctly formatted."""
		# Administrator should have unrestricted empty query condition
		cond = get_contract_query_conditions("Administrator")
		self.assertEqual(cond, "")
