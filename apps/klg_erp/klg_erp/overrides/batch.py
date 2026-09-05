import frappe
from frappe import _
from frappe.exceptions import ValidationError


def validate_batch_owner(doc, method=None):
	if not doc.custom_klg_owner_type:
		frappe.throw(_("Legal Owner Type is required."), exc=ValidationError)

	if doc.custom_klg_owner_type == "Customer" and not doc.custom_klg_owner_customer:
		frappe.throw(
			_("Owner Customer is required when Legal Owner Type is Customer."),
			exc=ValidationError,
		)

	if doc.custom_klg_owner_type == "KLG" and doc.custom_klg_owner_customer:
		frappe.throw(
			_("Owner Customer must be empty when Legal Owner Type is KLG."),
			exc=ValidationError,
		)
