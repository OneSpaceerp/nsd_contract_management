# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class ContractObligation(Document):
	def validate(self):
		if self.due_date and self.status == "Open":
			if getdate(self.due_date) < getdate(nowdate()):
				self.status = "Overdue"
