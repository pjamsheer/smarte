# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VitalSigns(Document):
	def after_insert(self):
		insert_vital_signs_to_medical_record(self)
	def on_update(self):
		update_vital_signs_to_medical_record(self)

@frappe.whitelist()
def create_vital_signs(patient):
	vital_signs = frappe.new_doc("Vital Signs")
	vital_signs.patient = patient
	return vital_signs.as_dict()

def insert_vital_signs_to_medical_record(doc):
	subject = setting_subject_field(doc)
	medical_record = frappe.new_doc("Patient Medical Record")
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = "Open"
	medical_record.communication_date = doc.signs_date
	medical_record.reference_doctype = "Vital Signs"
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)

def update_vital_signs_to_medical_record(doc):
	medical_record_id = frappe.db.sql("select name from `tabPatient Medical Record` where reference_name=%s",(doc.name))
	if(medical_record_id[0][0]):
		subject = setting_subject_field(doc)
		frappe.db.set_value("Patient Medical Record",medical_record_id[0][0],"subject",subject)

def setting_subject_field(doc):
	subject = "Vital Signs:: "
	if(doc.temperature):
		subject += "Pulse: \n"+ str(doc.temperature)+". "
	if(doc.pulse):
		subject += "Pulse: \n"+ str(doc.pulse)+". "
	if(doc.respiratory_rate):
		subject += "RR: \n"+ str(doc.respiratory_rate)+". "
	if(doc.bp):
		subject += "BP: \n"+ str(doc.bp)+". "
	if(doc.bmi):
		subject += "BMI: \n"+ str(doc.bmi)+". "
	if(doc.nutrition_note):
		subject += "Note: \n"+ str(doc.nutrition_note)+". "

	return subject
