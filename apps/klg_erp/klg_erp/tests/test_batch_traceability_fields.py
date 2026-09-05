import frappe
from frappe.exceptions import ValidationError
from frappe.tests import IntegrationTestCase


class TestBatchTraceabilityFields(IntegrationTestCase):
	def test_batch_klg_fields_follow_declared_sequence(self):
		meta = frappe.get_meta("Batch", cached=False)
		expected_chain = [
			("custom_klg_traceability_section", "description"),
			("custom_klg_external_loin_id", "custom_klg_traceability_section"),
			("custom_klg_purchase_batch_id", "custom_klg_external_loin_id"),
			("custom_klg_production_run_id", "custom_klg_purchase_batch_id"),
			("custom_klg_source_fish_id", "custom_klg_production_run_id"),
			("custom_klg_traceability_column", "custom_klg_source_fish_id"),
			("custom_klg_grade", "custom_klg_traceability_column"),
			("custom_klg_original_weight_kg", "custom_klg_grade"),
			("custom_klg_owner_type", "custom_klg_original_weight_kg"),
			("custom_klg_owner_customer", "custom_klg_owner_type"),
			("custom_klg_pallet_id", "custom_klg_owner_customer"),
		]

		klg_fields = [field for field in meta.fields if field.fieldname.startswith("custom_klg_")]
		self.assertEqual(
			[(field.fieldname, field.insert_after) for field in klg_fields], expected_chain
		)

	def test_batch_has_klg_loin_traceability_fields(self):
		meta = frappe.get_meta("Batch", cached=False)

		expected_fields = {
			"custom_klg_external_loin_id": "Data",
			"custom_klg_purchase_batch_id": "Data",
			"custom_klg_production_run_id": "Data",
			"custom_klg_source_fish_id": "Data",
			"custom_klg_grade": "Select",
			"custom_klg_original_weight_kg": "Float",
			"custom_klg_owner_type": "Select",
			"custom_klg_owner_customer": "Link",
			"custom_klg_pallet_id": "Data",
		}

		for fieldname, fieldtype in expected_fields.items():
			field = meta.get_field(fieldname)
			self.assertIsNotNone(field, fieldname)
			self.assertEqual(field.fieldtype, fieldtype)

		self.assertEqual(meta.get_field("custom_klg_grade").options, "AB\nC\nD")
		self.assertEqual(meta.get_field("custom_klg_owner_type").options, "KLG\nCustomer")
		self.assertEqual(meta.get_field("custom_klg_owner_customer").options, "Customer")
		self.assertTrue(meta.get_field("custom_klg_external_loin_id").unique)

	def make_item(self):
		return frappe.get_doc(
			{
				"doctype": "Item",
				"item_code": "_Test KLG Tuna Loin",
				"item_name": "_Test KLG Tuna Loin",
				"item_group": "All Item Groups",
				"stock_uom": "Kg",
				"has_batch_no": 1,
				"is_stock_item": 1,
			}
		).insert(ignore_if_duplicate=True)

	def make_customer(self):
		return frappe.get_doc(
			{
				"doctype": "Customer",
				"customer_name": "_Test KLG Custody Customer",
				"customer_type": "Company",
			}
		).insert(ignore_if_duplicate=True)

	def make_batch(self, suffix, owner_type, owner_customer=None):
		return frappe.get_doc(
			{
				"doctype": "Batch",
				"batch_id": f"_TEST-KLG-OWNER-{suffix}",
				"item": self.make_item().name,
				"custom_klg_external_loin_id": f"_TEST-LOIN-OWNER-{suffix}",
				"custom_klg_owner_type": owner_type,
				"custom_klg_owner_customer": owner_customer,
			}
		)

	def test_klg_owned_batch_rejects_customer_owner(self):
		batch = self.make_batch("KLG-WITH-CUSTOMER", "KLG", self.make_customer().name)

		with self.assertRaisesRegex(ValidationError, "Owner Customer"):
			batch.insert()

	def test_customer_owned_batch_requires_customer(self):
		batch = self.make_batch("CUSTOMER-WITHOUT-CUSTOMER", "Customer")

		with self.assertRaisesRegex(ValidationError, "Owner Customer is required"):
			batch.insert()

	def test_batch_requires_owner_type(self):
		batch = self.make_batch("WITHOUT-OWNER-TYPE", "")

		with self.assertRaisesRegex(ValidationError, "Legal Owner Type is required"):
			batch.insert()

	def test_customer_owned_batch_accepts_customer(self):
		customer = self.make_customer()
		batch = self.make_batch("VALID-CUSTOMER", "Customer", customer.name).insert()

		self.assertEqual(batch.custom_klg_owner_customer, customer.name)

	def test_klg_owned_batch_accepts_empty_customer(self):
		batch = self.make_batch("VALID-KLG", "KLG").insert()

		self.assertEqual(batch.custom_klg_owner_type, "KLG")
		self.assertFalse(batch.custom_klg_owner_customer)
