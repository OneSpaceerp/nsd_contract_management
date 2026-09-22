# Copyright (c) 2026, NSD Core Architecture Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ContractVersion(Document):
	def validate(self):
		if self.get_doc_before_save() and self.get_doc_before_save().immutable:
			frappe.throw(
				_("Contract Version {0} is immutable and cannot be modified.").format(self.name),
				frappe.PermissionError
			)

	def on_trash(self):
		if self.immutable:
			frappe.throw(
				_("Contract Version {0} is immutable and cannot be deleted.").format(self.name),
				frappe.PermissionError
			)
