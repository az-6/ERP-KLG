# ADR-0001: Kepemilikan data ERP dan Tuna Engine

Status: diterima

## Keputusan

- ERPNext/Frappe menjadi system of record untuk Purchase Order, Purchase Receipt, stock ledger, valuation, Sales Order, Delivery Note, Sales Invoice, dan accounting.
- Tuna Engine menjadi system of record untuk identitas ikan, loin individual, grade per loin, yield, mass balance, komponen biaya operasional, dan genealogy seafood.
- Integrasi memakai outbox idempoten. Status lokal baru boleh menjadi `posted` setelah dokumen ERPNext dibaca kembali dan kuantitas, nilai, serta identitasnya cocok.
- `C:\KTG\sistem` tidak diubah atau dipindahkan sebelum jalur baru lolos pengujian dan cutover disetujui.

## Konsekuensi

- ERPNext tidak menyimpan ulang seluruh detail operasional seafood jika bukan kebutuhan ledger.
- Tuna Engine tidak memelihara saldo persediaan bernilai yang bersaing dengan ERPNext.
- Setiap penulisan ERP wajib memiliki idempotency key dan remote document identity.
