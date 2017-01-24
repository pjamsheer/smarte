// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient', {
 	refresh: function(frm) {
 		if(frm.doc.name && (frappe.user.has_role("IP Physician")||frappe.user.has_role("OP Physician"))){
 			frm.add_custom_button(__('View History'), function() {
 				frappe.route_options = {"patient": frm.doc.name}
 				frappe.set_route("medical_record");
 			 });
		};
 }
});

frappe.ui.form.on("Patient", "dob", function(frm) {
  if(frm.doc.dob && !frm.doc.age){
    today = new Date();
    birthDate = new Date(frm.doc.dob);
    age = today.getFullYear() - birthDate.getFullYear();
    m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    frappe.model.set_value(frm.doctype,frm.docname, "age", age)
    frm.set_df_property("age", "read_only", 1);
  }else if(!frm.doc.age){
    frm.set_df_property("age", "read_only", 0);
  }
});

frappe.ui.form.on("Patient", "age", function(frm) {
  if(frm.doc.age){
    today = new Date()
    dob_yr = today.getFullYear() - frm.doc.age
    //dob_str = dob_yr+"-01-01"
    dob_month = today.getMonth()+1
    dob_str = dob_yr+"-"+dob_month+"-"+today.getDate()
    frappe.model.set_value(frm.doctype,frm.docname, "dob", new Date(dob_str))
    frm.set_df_property("age", "read_only", 1);
  }else{
    frm.set_df_property("age", "read_only", 0);
  }
});
