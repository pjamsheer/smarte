// Copyright (c) 2016, ESS
// License: ESS license.txt

frappe.ui.form.on("Lab Test Template",{
		//Refernce item.js Ln90
		test_name: function(frm) {
		if(!frm.doc.test_code)
			frm.set_value("test_code", frm.doc.test_name);
		if(!frm.doc.test_description)
			frm.set_value("test_description", frm.doc.test_name);
	}
}
)

cur_frm.cscript.custom_refresh = function(doc) {
	// use the __islocal value of doc, to check if the doc is saved or not
	cur_frm.set_df_property("test_code", "read_only", doc.__islocal ? 0 : 1);
	if(frappe.defaults.get_default("require_sample_collection")){
		cur_frm.set_df_property("sb_sample_collection", "hidden", 0);
	}else { cur_frm.set_df_property("sb_sample_collection", "hidden", 1); }

	if(!doc.__islocal) {
		cur_frm.add_custom_button(__('Change Template Code'), function() {
			change_template_code(cur_frm,doc);
		} );
		if(doc.disabled == 1){
			cur_frm.add_custom_button(__('Enable Template'), function() {
				enable_template(cur_frm);
			} );
		}
		else{
			cur_frm.add_custom_button(__('Disable Template'), function() {
				disable_template(cur_frm);
			} );
		}
	}
}

var disable_template = function(frm){
	var doc = frm.doc;
	frappe.call({
		method: 		"smarte.medical.doctype.lab_test_template.lab_test_template.disable_enable_test_template",
		args: {status: 1, name: doc.name, is_billable: doc.is_billable},
		callback: function(r){
			cur_frm.reload_doc();
		}
	});
}

var enable_template = function(frm){
	var doc = frm.doc;
	frappe.call({
		method: 		"smarte.medical.doctype.lab_test_template.lab_test_template.disable_enable_test_template",
		args: {status: 0, name: doc.name, is_billable: doc.is_billable},
		callback: function(r){
			cur_frm.reload_doc();
		}
	});
}


var change_template_code = function(frm,doc){
	var d = new frappe.ui.Dialog({
			title:__("Change Template Code"),
			fields:[
				{
					"fieldtype": "Data",
					"label": "Test Template Code",
					"fieldname": "Test Code",
					reqd:1
				},
				{
					"fieldtype": "Button",
					"label": __("Change Code"),
					click: function() {
						var values = d.get_values();
						if(!values)
							return;
						change_test_code_from_template(values["Test Code"],doc);
						d.hide();
					}
				}
			]
		})
		d.show();
		d.set_values({
			'Test Code': doc.test_code
		})

		var change_test_code_from_template = function(test_code,doc){
			frappe.call({
				"method": "smarte.medical.doctype.lab_test_template.lab_test_template.change_test_code_from_template",
				"args": {test_code: test_code, doc: doc},
			    callback: function (data) {
				frappe.set_route("Form", "Lab Test Template", data.message);
			    }
			})
		}

}


//Restrict Special, Grouped type templates in Child TestGroups
me.frm.set_query("test_template", "test_groups", function(doc, cdt, cdn) {
		return {
			filters: {
				test_template_type:['in',['Single','Compound']]
			}
		};
	});

frappe.ui.form.on("Lab Test Template", "test_name", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Lab Test Template", "test_rate", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Lab Test Template", "test_group", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Lab Test Template", "test_description", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Lab Test Template", "lab_test_type", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
