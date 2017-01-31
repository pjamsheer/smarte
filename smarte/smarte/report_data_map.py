# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

# mappings for table dumps
# "remember to add indexes!"

data_map = {
	"Patient": {
		"columns": ["name", "creation", "owner", "if(patient_name=name, '', patient_name) as patient_name"],
		"conditions": ["docstatus < 2"],
		"order_by": "name",
		"links": {
			"owner" : ["User", "name"]
		}
	},
	"Appointment": {
		"columns": ["name", "appointment_type", "patient", "physician", "start_dt", "department", "status"],
		"order_by": "name",
		"links": {
			"physician": ["Physician", "name"],
			"appointment_type": ["Appointment Type", "name"]
		}
	},
	"Physician": {
		"columns": ["name", "department"],
		"order_by": "name",
		"links": {
			"department": ["Department", "name"],
		}

	},
	"Appointment Type": {
		"columns": ["name"],
		"order_by": "name"
	},
	"Department": {
		"columns": ["name"],
		"order_by": "name"
	},
	"User": {
		"columns": ["name"],
		"order_by": "name"
	}
}
