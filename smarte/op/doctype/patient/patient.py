# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr
from smarte.op.doctype.op_settings.op_settings import generate_patient_id
class Patient(Document):
	def after_insert(self):
		generate_patient_id(self)

	def autoname(self):
		self.name = self.get_patient_name()

	def get_patient_name(self):
		if frappe.db.get_value("Patient", self.patient_name):
			count = frappe.db.sql("""select ifnull(MAX(CAST(SUBSTRING_INDEX(name, ' ', -1) AS UNSIGNED)), 0) from tabPatient
				 where name like %s""", "%{0} - %".format(self.patient_name), as_list=1)[0][0]
			count = cint(count) + 1
			return "{0} - {1}".format(self.patient_name, cstr(count))

		return self.patient_name
