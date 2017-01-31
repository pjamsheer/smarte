// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Consultation', {
	setup: function(frm) {
		frm.get_field('drug_prescription').grid.editable_fields = [
			{fieldname: 'drug_code', columns: 2},
			{fieldname: 'drug_name', columns: 2},
			{fieldname: 'dosage', columns: 2},
			{fieldname: 'interval', columns: 2},
			{fieldname: 'in_every', columns: 1},
			{fieldname: 'period', columns: 1}
		];
		frm.get_field('test_prescription').grid.editable_fields = [
			{fieldname: 'test_code', columns: 2},
			{fieldname: 'test_name', columns: 4},
			{fieldname: 'test_comment', columns: 4}
		];
	},
	onload: function(frm){
		if(frm.doc.__islocal && frm.doc.patient){
			frappe.call({
					"method": "frappe.client.get",
					args: {
							doctype: "Patient",
							name: frm.doc.patient
					},
					callback: function (data) {
						show_details(data.message);
					}
				});
		}
	},
	refresh: function(frm) {
		refresh_field('drug_prescription');
		refresh_field('test_prescription');
		if((frappe.user.has_role("IP Physician")) || (frappe.user.has_role("OP Physician"))){
			frm.add_custom_button(__('View History'), function() {
				if(frm.doc.patient){
					frappe.route_options = {"patient": frm.doc.patient}
					frappe.set_route("medical_record");
				}else{
					frappe.msgprint("Please select Patient");
				}
			} );
		}
		cur_frm.set_query("patient", function () {
			if(frm.doc.admitted){
				return {
					filters: {"admitted": 1}
				}
			}else{
				return {
					filters: {"admitted": 0}
				}
			}
		});
		frm.set_df_property("appointment", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("patient", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("patient_age", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("patient_sex", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("type", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("physician", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("ref_physician", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("visit_department", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("consultation_date", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("consultation_time", "read_only", frm.doc.__islocal ? 0:1);
		if(frm.doc.admitted){
			frm.set_df_property("appointment", "hidden", 1);
		}else{
			frm.set_df_property("appointment", "hidden", 0);
		}
		if(!frm.doc.__islocal){
			if(frappe.user.has_role("Pharmacy Manager") ||
					frappe.user.has_role("Pharmacy User")){
				frm.add_custom_button(__('Invoice from Drug Prescription'), function() {
					btn_invoice_drug(frm);
				 },__("Create") );
			}
			if(frappe.user.has_role("Laboratory Manager") ||
					frappe.user.has_role("Laboratory User")){
				frm.add_custom_button(__('Invoice from Test Prescription'), function() {
					btn_invoice_lab_test(frm);
				 },__("Create") );
			}
			if(!frm.doc.admitted && !frm.doc.admit_scheduled){
				frm.add_custom_button(__('Admit Patient'), function() {
					btn_admit_patient(frm);
				 });
			}
		}
	}
});

var show_details = function(data){
	//HTML hack to show patient details in left sidebar before saving -ROF
	var details = "<div style='padding-left:10px;'></br><b>Patient Details</b><br>";
	if(data.age) details += "<br><b>Age :</b> " + data.age;
	if(data.sex) details += "<br><b>Gender :</b> " + data.sex;
	if(data.email) details += "<br><b>Email :</b> " + data.email;
	if(data.mobile) details += "<br><b>Mobile :</b> " + data.mobile;
	if(data.occupation) details += "<br><b>Occupation :</b> " + data.occupation;
	if(data.blood_group) details += "<br><b>Blood group : </b>" + data.blood_group;
	if(data.allergies) details +=  "<br><br><b>Allergies : </b>"+  data.allergies;
	if(data.medication) details +=  "<br><b>Medication : </b>"+  data.medication;
	if(data.alcohol_current_use) details +=  "<br><br><b>Alcohol use : </b>"+  data.alcohol_current_use;
	if(data.alcohol_past_use) details +=  "<br><b>Alcohol past use : </b>"+  data.alcohol_past_use;
	if(data.tobacco_current_use) details +=  "<br><b>Tobacco use : </b>"+  data.tobacco_current_use;
	if(data.tobacco_past_use) details +=  "<br><b>Tobacco past use : </b>"+  data.tobacco_past_use;
	if(data.medical_history) details +=  "<br><br><b>Medical history : </b>"+  data.medical_history;
	if(data.surgical_history) details +=  "<br><b>Surgical history : </b>"+  data.surgical_history;
	if(data.surrounding_factors) details +=  "<br><br><b>Occupational hazards : </b>"+  data.surrounding_factors;
	if(data.other_risk_factors) details += "<br><b>Other risk factors : </b>" + data.other_risk_factors;
	if(data.patient_details) details += "<br><br><b>More info : </b>" + data.patient_details;
	details += "</div>"
	//escape / in div id with \\ -ROF
	$('#page-Form\\/Consultation').find('.layout-side-section').html(details);
	$('#page-Form\\/Consultation').find('.layout-side-section').show();
}

frappe.ui.form.on("Consultation", "appointment",
    function(frm) {
	if(frm.doc.appointment){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Appointment",
		        name: frm.doc.appointment
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "patient", data.message.patient)
				frappe.model.set_value(frm.doctype,frm.docname, "type", data.message.appointment_type)
				frappe.model.set_value(frm.doctype,frm.docname, "physician", data.message.physician)
		    }
		})
	}
});

frappe.ui.form.on("Consultation", "physician",
    function(frm) {
	if(frm.doc.physician){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Physician",
		        name: frm.doc.physician
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "visit_department",data.message.department)
		    }
		})
	}
});

frappe.ui.form.on("Consultation", "patient",
    function(frm) {
        if(frm.doc.patient){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Patient",
		        name: frm.doc.patient
		    },
		    callback: function (data) {
					frappe.model.set_value(frm.doctype,frm.docname, "patient_age", data.message.age)
					frappe.model.set_value(frm.doctype,frm.docname, "patient_sex", data.message.sex)
					frappe.model.set_value(frm.doctype,frm.docname, "admitted", data.message.admitted)
					if(data.message.admitted){
						frappe.model.set_value(frm.doctype,frm.docname, "admission", data.message.admission)
					}
					if(frm.doc.__islocal) show_details(data.message);
		    }
		})
	}
});

frappe.ui.form.on("Drug Prescription", {
	drug_code:  function(frm, cdt, cdn) {
		var child = locals[cdt][cdn]
		if(child.drug_code){
			frappe.call({
				"method": "frappe.client.get",
				args: {
				    doctype: "Item",
				    name: child.drug_code
				},
				callback: function (data) {
				frappe.model.set_value(cdt, cdn, 'drug_name',data.message.item_name)
				}
			})
		}
	},
	dosage: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
		var child = locals[cdt][cdn]
		if(child.dosage){
			frappe.model.set_value(cdt, cdn, 'in_every', 'Day')
			frappe.model.set_value(cdt, cdn, 'interval', 1)
		}
	},
	period: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
	},
	in_every: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
		var child = locals[cdt][cdn]
		if(child.in_every == "Hour"){
			frappe.model.set_value(cdt, cdn, 'dosage', null)
		}
	}
});

frappe.ui.form.on("IP Routine Observation", {
	number: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
	},
	observe: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
	},
	period: function(frm, cdt, cdn){
		frappe.model.set_value(cdt, cdn, 'update_schedule', 1)
	}
});

var btn_invoice_drug = function(frm){
	var doc = frm.doc;
	frappe.call({
		method:"smarte.op.doctype.consultation.consultation.create_drug_invoice",
		args: {consultationId: doc.name},
		callback: function(data){
			if(!data.exc){
				var doclist = frappe.model.sync(data.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}

var btn_admit_patient = function(frm){
	var doc = frm.doc;
	frappe.call({
		method:"smarte.op.doctype.consultation.consultation.admit_patient",
		args: {consultationId: doc.name},
		callback: function(data){
			if(!data.exc){
				frappe.msgprint("Patient scheduled for admission");
				cur_frm.reload_doc()
			}
		}
	});
}

var btn_invoice_lab_test = function(frm){
	var doc = frm.doc;
	frappe.call({
		method:"smarte.op.doctype.consultation.consultation.create_lab_test_invoice",
		args: {consultationId: doc.name},
		callback: function(data){
			if(!data.exc){
				var doclist = frappe.model.sync(data.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}

me.frm.set_query("appointment", function(doc, cdt, cdn) {
		return {
			filters: {
				//Scheduled filter for demo ...
				status:['in',["Open","Scheduled"]],
				//Commented for demo ..
				//physician: doc.physician
			}
		};
	});
