from __future__ import unicode_literals
from frappe import _
import frappe
import datetime as dt

def get_data():

	return [
		{
			"label": _("Laboratory"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Patient",
					"label": _("Patient"),
					"description": _("Patient."),
				},
				{
					"type": "doctype",
					"name": "Physician",
					"description": _("Physician."),
				},
				{
					"type": "doctype",
					"name": "Lab Procedure",
					"description": _("Results"),
					"icon": "octicon octicon-clippy",
				},
				{
					"type": "doctype",
					"name": "Sample Collection",
					"description": _("Sample Collection."),
				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Invoice."),
				},

			]
		},
		{
			"label": _("Lab Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Laboratory Settings",
					"description": _("Settings for Laboratory Module")
				},
				{
					"type": "doctype",
					"name": "Lab Test Type",
					"description": _("Lab Test Type")
				},
				{
					"type": "doctype",
					"name": "Lab Test Template",
					"description": _("Lab Test Configurations.")
				},
				{
					"type": "doctype",
					"name": "Lab Test Samples",
					"description": _("Test Sample Master."),
				},
				{
					"type": "doctype",
					"name": "Lab Test UOM",
					"description": _("UOM Refer to Laboratory.")
				},
				{
					"type": "doctype",
					"name": "Antibiotics",
					"description": _("Antibiotics.")
				},
				{
					"type": "doctype",
					"name": "Sensitivity",
					"description": _("Sensitivity Naming.")
				},

			]
		},
		{
			"label": _("Lab Standard Reports"),
			"icon": "icon-list",
			"items": [
				{
					"type": "doctype",
					"name": "Invoice Test Report",
					"description": _("Invoiced Results."),
					"icon": "octicon octicon-tasklist",
				},
				{
					"type": "report",
					"name": "Lab Procedure Report",
					"is_query_report": True,
					"doctype": "Lab Procedure"
				},
				{
					"type": "report",
					"name": "Laboratory Sales Register",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				}
			]
		},
			{
				"label": _("OP"),
				"icon": "icon-star",
				"items": [
					{
						"type": "doctype",
						"name": "Appointment",
						"description": _("Patient Appointment"),
					},
					{
						"type": "doctype",
						"name": "Consultation",
						"description": _("Patient Doctor Consulation"),
					},
				]
			},
			{
				"label": _("OP Setup"),
				"icon": "icon-cog",
				"items": [
					{
						"type": "doctype",
						"name": "OP Settings",
						"label": _("OP Settings"),
					},
					{
						"type": "doctype",
						"name": "Referring Physician",
						"description": _("Referring Physician."),
					},
					{
						"type": "doctype",
						"name": "Appointment Type",
						"description": _("Appointment Type Master"),
					},
					{
						"type": "doctype",
						"name": "Duration",
						"description": _("Drug Prescription Period")
					},
					{
						"type": "doctype",
						"name": "Dosage",
						"description": _("Drug Prescription Dosage")
					},
				]
			},
			{
				"label": _("OP Standard Reports"),
				"icon": "icon-list",
				"items": [
					{
						"type": "doctype",
						"name": "Appointment",
						"description": _("Patient Appointment"),
						"label": _("Today's Appoinment"),
						"route_options": {"appointment_date": dt.date.today()}
					},
					{
						"type": "page",
						"name": "medical_record",
						"label": _("Patient Medical Records"),
						"icon": "icon-bar-chart",
					},
					{
						"type": "page",
						"name": "appointment-analytic",
						"label": _("Appointment Analytics"),
						"icon": "icon-bar-chart",
					},
					{
						"type": "page",
						"name": "patient-registration",
						"label": _("Patient Registration Analytics"),
						"icon": "icon-bar-chart",
					},

				]
			},

	]
