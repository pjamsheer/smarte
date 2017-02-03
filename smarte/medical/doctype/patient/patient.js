// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Patient', {
 	refresh: function(frm) {
 		if(frm.doc.patient_name && (frappe.user.has_role("IP Physician")||frappe.user.has_role("OP Physician"))){
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
    if(today < birthDate){
      msgprint("Please select a valid Date");
      frappe.model.set_value(frm.doctype,frm.docname, "dob", null)
    }else{
      age_yr = today.getFullYear() - birthDate.getFullYear();
      today_m = today.getMonth()+1 //Month jan = 0
      birth_m = birthDate.getMonth()+1 //Month jan = 0
      m = today_m - birth_m;
      d = today.getDate() - birthDate.getDate()

      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age_yr--;
      }
      if (m < 0 || m==0) {
       m = (12 + m);
      }
      if (d < 0) {
        m--;
        d = 31 + d;// 31 may varry with month Feb(28,29),Even Month(30) or Odd Month(31)
      }
      age_str = null
      if(age_yr > 0)
        age_str = age_yr+" Year(s), "
      if(m > 0)
        age_str = age_str+m+" Month(s), "
      if(d > 0)
        age_str = age_str+d+" Day(s)"
      frappe.model.set_value(frm.doctype,frm.docname, "age", age_str)
      frm.set_df_property("age_int", "hidden", 1);
      frm.set_df_property("age", "hidden", 0);
    }
  }
});

frappe.ui.form.on("Patient", "age_int", function(frm) {
  if(frm.doc.age_int){
    today = new Date()
    frm.set_df_property("dob", "hidden", 1);
    frm.set_df_property("age", "hidden", 1);
    frm.set_df_property("age_as_on", "hidden", 0);
    frm.set_df_property("age_int", "hidden", 0);
    d = today.getDate();m = today.getMonth();y = today.getFullYear();
    frappe.model.set_value(frm.doctype,frm.docname, "age_as_on", today)
    frappe.model.set_value(frm.doctype,frm.docname, "age", frm.doc.age_int+" as on "+d+"-"+m+"-"+y)
  }
});
