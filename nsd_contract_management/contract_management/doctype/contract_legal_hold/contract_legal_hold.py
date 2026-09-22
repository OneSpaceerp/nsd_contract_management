# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ContractLegalHold(Document):
	def on_update(self):
		if self.status == "Active":
			frappe.db.set_value("Contract", self.contract, "legal_hold", 1)
		elif self.status == "Released":
			# Only clear flag if no other active hold exists
			active_holds = frappe.db.count("Contract Legal Hold", {"contract": self.contract, "status": "Active"})
			if active_holds == 0:
				frappe.db.set_value("Contract", self.contract, "legal_hold", 0)
			if not self.release_on:
				self.release_on = now_datetime()
				self.released_by = frappe.session.user
				frappe.db.set_value(self.doctype, self.name, {
					"release_on": self.release_on,
					"released_by": self.released_by
				})
