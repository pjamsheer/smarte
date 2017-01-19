# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import date
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms
class OPSettings(Document):
	pass


def generate_patient_id(doc, method):
	if (frappe.db.get_value("OP Settings", None, "patient_id")=='1'):
		pid = make_autoname(frappe.db.get_value("OP Settings", None, "id_series"), "", doc)
		doc.patient_id = pid
		doc.save()
	send_registration_sms(doc, method)

def send_registration_sms(doc, method):
	if (frappe.db.get_value("OP Settings", None, "reg_sms")=='1'):
		context = {"doc": doc, "alert": doc, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))
		messages = frappe.db.get_value("OP Settings", None, "reg_msg")
		messages = frappe.render_template(messages, context)
		number = [doc.mobile]
		send_sms(number,messages)

def update_customer_age():
	customers = frappe.get_all("Customer", fields=["name", "dob", "age"])
	for d in customers:
		if d.name and d.dob:
				age = calculate_age(d.dob)
				if(d.age != age):
					frappe.db.set_value("Customer", d.name, "age", age)

def calculate_age(born):
	today = date.today()

	try:
		birthday = born.replace(year=today.year)
	except ValueError:# raised when birth date is February 29 and the current year is not a leap year
		birthday = born.replace(year=today.year, day=born.day-1)
	if birthday > today:
		return today.year - born.year - 1
	else:
		return today.year - born.year
