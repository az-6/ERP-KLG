# Integration contracts

Kontrak di folder ini menghubungkan Tuna Traceability/HPP Engine dengan ERPNext.

Aturan wajib:

- seluruh write memakai idempotency key;
- credential ERP hanya berada di server;
- request dan response menyimpan tipe serta nama dokumen ERPNext;
- keberhasilan posting wajib diverifikasi melalui read-back;
- payload berat memakai kg dengan presisi maksimal tiga desimal;
- Rupiah memakai integer dan total alokasi child harus sama tepat dengan biaya batch.
