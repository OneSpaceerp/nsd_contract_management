# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate


class ContractRenewal(Document):
	def validate(self):
		if self.current_expiration_date and self.notice_period_days and not self.notice_deadline:
			self.notice_deadline = add_days(self.current_expiration_date, -int(self.notice_period_days))
