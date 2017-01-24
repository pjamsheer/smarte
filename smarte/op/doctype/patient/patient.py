# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from smarte.op.doctype.op_settings.op_settings import generate_patient_id
class Patient(Document):
	def after_insert(self):
		generate_patient_id(self)
