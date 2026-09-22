# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Clause(Document):
	def validate(self):
		if not self.clause_code:
			self.clause_code = self.name
