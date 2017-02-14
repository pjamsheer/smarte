# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, getdate, get_time, math
import time
import datetime
from datetime import timedelta
from smarte.medical.doctype.patient_medical_record.patient_medical_record import delete_attachment, insert_attachment

class Consultation(Document):
	def autoname(self):
		self.name = "-".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["consultation_date","patient"]]))

		self.name = self.name + " ( " +str(self.patient_sex)+ " ) "

		self.name = self.name + "-".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["physician", "consultation_time"]]))

	def on_update(self):
		if(self.appointment):
			frappe.db.set_value("Appointment",self.appointment,"status","Closed")
		update_consultation_to_medical_record(self)
		if(self.admitted):
			schedule_task(self)
		attachments = get_attachments(self)
		if attachments:
			delete_attachment("File", self.name)
			for i in range(0,len(attachments)):
				attachment = frappe.get_doc("File", attachments[i]['name'])
				insert_attachment(attachment,self.patient)

	def after_insert(self):
		insert_consultation_to_medical_record(self)

	def on_submit(self):
		physician = frappe.get_doc("Physician",self.physician)
		if(frappe.session.user != physician.user_id):
			frappe.throw(_("Submit only by created physician"))

def get_attachments(doc):
	return frappe.get_all("File", fields=["name"],
		filters = {"attached_to_name": doc.name, "attached_to_doctype": doc.doctype})

def setting_sales_invoice_fields(consultation):
	sales_invoice = frappe.new_doc("Sales Invoice")
	# patient is custom field in sales inv.
	sales_invoice.patient = consultation.patient
	sales_invoice.physician = consultation.physician
	sales_invoice.ref_physician = consultation.ref_physician
	sales_invoice.due_date = time.strftime("%m/%d/%Y")
	sales_invoice.territory = "India"

	return sales_invoice

def create_sales_invoice_item_lines(item, sales_invoice):
	sales_invoice_line = sales_invoice.append("items")
	sales_invoice_line.item_code = item.item_code
	sales_invoice_line.item_name =  item.item_name
	sales_invoice_line.qty = 1.0
	sales_invoice_line.description = item.description
	return sales_invoice_line

@frappe.whitelist()
def create_drug_invoice(consultationId):
	consultation = frappe.get_doc("Consultation",consultationId)
	sales_invoice = setting_sales_invoice_fields(consultation)
	sales_invoice.update_stock = 1

	if(consultation.drug_prescription):
		for item_line in consultation.drug_prescription:
			if(item_line.drug_code):
				item = frappe.get_doc("Item", item_line.drug_code)
				sales_invoice_line = create_sales_invoice_item_lines(item, sales_invoice)
				sales_invoice_line.qty = item_line.get_quantity()
	#income_account and cost_center in itemlines - by set_missing_values()
	sales_invoice.set_missing_values()
	return sales_invoice.as_dict()

@frappe.whitelist()
def create_lab_test_invoice(consultationId):
	consultation = frappe.get_doc("Consultation",consultationId)
	sales_invoice = setting_sales_invoice_fields(consultation)
	sales_invoice.update_stock = 0

	if(consultation.test_prescription):
		for item_line in consultation.test_prescription:
			if(item_line.test_code):
				item = frappe.get_doc("Item", item_line.test_code)
				create_sales_invoice_item_lines(item, sales_invoice)

	#income_account and cost_center in itemlines - by set_missing_values()
	sales_invoice.set_missing_values()
	return sales_invoice.as_dict()

@frappe.whitelist()
def admit_patient(consultationId):
	consultation = frappe.get_doc("Consultation",consultationId)
	patient_admission = frappe.new_doc("Patient Admission")

	patient_admission.op_consultation_id = consultationId
	patient_admission.physician = consultation.physician
	#patient_admission has no field ref_physician
	#patient_admission.ref_physician = consultation.ref_physician
	patient_admission.visit_department = consultation.visit_department
	patient_admission.status = "Scheduled"
	patient_admission.company = consultation.company
	patient_admission.patient = consultation.patient
	patient_admission.patient_age = consultation.patient_age
	patient_admission.patient_sex = consultation.patient_sex
	patient_admission.complaints = consultation.symptoms
	patient_admission.vitals = consultation.vitals
	patient_admission.diagnosis = consultation.diagnosis
	patient_admission.save(ignore_permissions=True)

	frappe.db.set_value("Consultation", consultationId, "admit_scheduled", True)


def schedule_task(consultation):
	#Just chek if child exist : add to schedule task
	#For Test no need of queuing, Directly create task
	#For drug and routine have chek the period and dosage and set the tasktym
	if(consultation.drug_prescription):
		schedule_list = generate_schedules_for_lines(consultation, consultation.drug_prescription, True)
		create_task_schedule(schedule_list)
	if(consultation.routine_observation):
		schedule_list = generate_schedules_for_lines(consultation, consultation.routine_observation, False)
		create_task_schedule(schedule_list)
	#frappe.msgprint("Tasks scheduled");

def get_intrvl_minutes(interval, in_every):
	if(in_every == 'Day'):
		minutes = (interval*1440)
	if(in_every == 'Hour'):
		minutes = (interval*60)
	if(in_every == 'Week'):
		minutes = (interval*10080)
	if(in_every == 'Month'):
		minutes = (interval*43800)
	return minutes

def generate_schedules_for_lines(consultation, lines, drug_rx):
	data = []
	period = None
	dosage = None
	in_every = "Day"
	interval = 1
	for line in lines:
		if line.update_schedule:
			#delete scheduled records
			frappe.db.sql("delete from `tabTask Schedule` where dt=%s and dn=%s", (line.doctype, line.name))

			if(line.period):
				period = frappe.get_doc("Duration", line.period)

			if(drug_rx):
				if(line.dosage):
					dosage = frappe.get_doc("Dosage", line.dosage)
				if(line.in_every):
					in_every = line.in_every
				if(line.interval):
					interval = line.interval
				item = line.drug_code
			else:
				if(line.observe):
					in_every = line.observe
				if(line.number):
					interval = line.number
				item = line.routine_observation

			intvl_minutes = get_intrvl_minutes(interval, in_every)
			times = create_date_time_list(period, intvl_minutes, dosage)
			for i in range(0, len(times)):
				schedule = {"t": times[i], "dt": line.doctype, "dn": line.name, "item": item ,"p_dt": consultation.doctype, "p_dn": consultation.name, "com": consultation.company, "admission":consultation.admission}
				data.append(schedule)
			line.update_schedule = 0
	return data

def create_date_time_list(period, intvl_minutes, dosage):
	today = datetime.date.today()
	time = datetime.datetime.now()
	end_dt = time
	if(period and dosage):
		end_dt = (time + datetime.timedelta(days = period.get_days()-1))
	elif(period):
		end_dt = (time + datetime.timedelta(minutes = period.get_minutes() - intvl_minutes))
	times = []

	while (time <= end_dt):
		if(dosage):
			if(dosage.dosage_strenght):
				for d_strenght in dosage.dosage_strenght:
					ds_time = datetime.datetime.strptime(str(d_strenght.strength_time), "%H:%M:%S").time()
					time = datetime.datetime.combine(today,ds_time)
					times.append(time)
			today = today + datetime.timedelta(minutes = intvl_minutes)
			time = datetime.datetime.combine(today, datetime.datetime.min.time())
		else:
			#if u schedule with the start of the time append the time  and then add with time intrval
			time = time+datetime.timedelta(minutes = intvl_minutes)
			times.append(time)

	return times

def create_task_schedule(sch_list):
	for line in sch_list:
		#if check for passed today's time - No need to create task schedule for that
		if(line["t"] >= datetime.datetime.now()):
			task_schedule = frappe.new_doc("Task Schedule")
			task_schedule.task_datetime = line["t"]
			task_schedule.dt = line["dt"]
			task_schedule.dn = line["dn"]
			task_schedule.parent_doc = line["p_dt"]
			task_schedule.parent_id = line["p_dn"]
			task_schedule.company = line["com"]
			task_schedule.patient_admission = line["admission"]
			task_schedule.physician = ""
			task_schedule.comment = line["item"]
			task_schedule.open = True
			task_schedule.save(ignore_permissions=True)

def insert_consultation_to_medical_record(doc):
	subject = setting_subject_field(doc)
	medical_record = frappe.new_doc("Patient Medical Record")
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = "Open"
	medical_record.communication_date = doc.consultation_date
	medical_record.reference_doctype = "Consultation"
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)

def update_consultation_to_medical_record(consultation):
	medical_record_id = frappe.db.sql("select name from `tabPatient Medical Record` where 			reference_name=%s",(consultation.name))
	if(medical_record_id[0][0]):
		subject = setting_subject_field(consultation)
		frappe.db.set_value("Patient Medical Record",medical_record_id[0][0],"subject",subject)

def setting_subject_field(consultation):
	subject = "This Consultation do not have any diagnosis."
	if(consultation.diagnosis):
		subject = "Diagnosis: \n"+ str(consultation.diagnosis)+". "
	if(consultation.drug_prescription):
		subject +="\nDrug(s) Prescribed. "
	if(consultation.test_prescription):
		subject += " Test(s) Prescribed."

	return subject
