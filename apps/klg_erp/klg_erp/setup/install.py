from klg_erp.setup.batch_fields import sync_batch_traceability_fields


def after_install():
	sync_batch_traceability_fields()


def after_migrate():
	sync_batch_traceability_fields()
