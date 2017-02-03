# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VitalSigns(Document):
	pass

@frappe.whitelist()
def create_vital_signs(patient):
	vital_signs = frappe.new_doc("Vital Signs")
	vital_signs.patient = patient
	return vital_signs.as_dict()
