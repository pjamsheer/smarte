# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _
from frappe.utils import cstr

class Physician(Document):
	def autoname(self):
		# physician first_name and last_name
		self.name = " ".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["first_name", "last_name"]]))

	def validate(self):
		if self.user_id:
			self.validate_for_enabled_user_id()
		if self.employee:
			self.validate_duplicate_employee_id()				
			existing_user_id = frappe.db.get_value("Physician", self.name, "user_id")
			if(self.user_id != existing_user_id):
				frappe.permissions.remove_user_permission(
					"Physician", self.name, existing_user_id)

				
		else:
			existing_user_id = frappe.db.get_value("Physician", self.name, "user_id")
			if existing_user_id:
				frappe.permissions.remove_user_permission(
					"Physician", self.name, existing_user_id)

	def on_update(self):
		if self.user_id:
			frappe.permissions.add_user_permission("Physician", self.name, self.user_id)


	def validate_for_enabled_user_id(self):
		enabled = frappe.db.get_value("User", self.user_id, "enabled")
		if enabled is None:
			frappe.throw(_("User {0} does not exist").format(self.user_id))
		if enabled == 0:
			frappe.throw(_("User {0} is disabled").format(self.user_id))

	def validate_duplicate_employee_id(self):
		physician = frappe.db.sql_list("""select name from `tabPhysician` where
			employee=%s and name!=%s""", (self.employee, self.name))
		if physician:
			throw(_("Employee {0} is already assigned to Physician {1}").format(
				self.employee, physician[0]), frappe.DuplicateEntryError)

