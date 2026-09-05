from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


BATCH_TRACEABILITY_FIELDS = {
	"Batch": [
		{
			"fieldname": "custom_klg_traceability_section",
			"label": "KLG Traceability",
			"fieldtype": "Section Break",
			"insert_after": "description",
		},
		{
			"fieldname": "custom_klg_external_loin_id",
			"label": "External Loin ID",
			"fieldtype": "Data",
			"insert_after": "custom_klg_traceability_section",
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_purchase_batch_id",
			"label": "Purchase Batch ID",
			"fieldtype": "Data",
			"insert_after": "custom_klg_external_loin_id",
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_production_run_id",
			"label": "Production Run ID",
			"fieldtype": "Data",
			"insert_after": "custom_klg_purchase_batch_id",
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_source_fish_id",
			"label": "Source Fish ID",
			"fieldtype": "Data",
			"insert_after": "custom_klg_production_run_id",
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_traceability_column",
			"fieldtype": "Column Break",
			"insert_after": "custom_klg_source_fish_id",
		},
		{
			"fieldname": "custom_klg_grade",
			"label": "Tuna Grade",
			"fieldtype": "Select",
			"insert_after": "custom_klg_traceability_column",
			"options": "AB\nC\nD",
			"in_list_view": 1,
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_original_weight_kg",
			"label": "Original Weight (Kg)",
			"fieldtype": "Float",
			"insert_after": "custom_klg_grade",
			"non_negative": 1,
			"precision": "3",
		},
		{
			"fieldname": "custom_klg_owner_type",
			"label": "Legal Owner Type",
			"fieldtype": "Select",
			"insert_after": "custom_klg_original_weight_kg",
			"options": "KLG\nCustomer",
			"default": "KLG",
			"in_standard_filter": 1,
		},
		{
			"fieldname": "custom_klg_owner_customer",
			"label": "Owner Customer",
			"fieldtype": "Link",
			"insert_after": "custom_klg_owner_type",
			"options": "Customer",
			"depends_on": "eval:doc.custom_klg_owner_type=='Customer'",
			"mandatory_depends_on": "eval:doc.custom_klg_owner_type=='Customer'",
		},
		{
			"fieldname": "custom_klg_pallet_id",
			"label": "Pallet ID",
			"fieldtype": "Data",
			"insert_after": "custom_klg_owner_customer",
			"in_standard_filter": 1,
		},
	]
}


def sync_batch_traceability_fields():
	create_custom_fields(BATCH_TRACEABILITY_FIELDS, update=True)
