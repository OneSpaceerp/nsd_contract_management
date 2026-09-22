# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ContractRequest(Document):
	def validate(self):
		if self.target_start_date and self.target_end_date:
			if frappe.utils.getdate(self.target_end_date) < frappe.utils.getdate(self.target_start_date):
				frappe.throw(_("Target End Date cannot be before Target Start Date"))
