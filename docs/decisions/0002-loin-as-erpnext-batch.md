# ADR-0002: Representasi loin sebagai Batch ERPNext

Status: diterima berdasarkan spike ERPNext 16.34.1

## Fixture

- Item stok: `KLG-POC-LOIN-BATCH`
- UOM stok: `Kg`
- Identitas loin/Batch: `KLG-LN-001`
- Berat: `4.25 kg`
- Valuation rate: `Rp100.000/kg`
- Gudang: `Finished Goods - KLG`

## Hasil terverifikasi

Stock Entry `MAT-STE-2026-00001` berhasil disubmit dengan:

- `actual_qty = 4.25`
- `total_incoming_value = Rp425.000`
- `valuation_rate = Rp100.000/kg`
- Batch `KLG-LN-001` memiliki `batch_qty = 4.25`
- Serial and Batch Bundle menyimpan batch, qty `4.25`, warehouse, incoming rate, voucher, dan voucher detail.

Percobaan Serial Number `KLG-SN-001` untuk berat `4.25 kg` ditolak ERPNext karena satu serial dihitung sebagai qty `1.0`, tidak sama dengan actual qty `4.25`. Draft pembuktian: `MAT-STE-2026-00002`.

## Keputusan

Gunakan **satu Batch ERPNext per loin**. Kuantitas stok tetap dalam kg dan kode batch menjadi identitas unik loin. Jangan gunakan Serial Number sebagai identitas utama loin karena model serial mengharuskan kuantitas unit bulat dan tidak cocok dengan berat variabel.

Genealogy rinci ikan → loin tetap dimiliki Tuna Engine. ERPNext Batch perlu custom field untuk ID/kode loin, fish code, purchase lot, production batch, dan idempotency key agar dapat direkonsiliasi.

## Catatan implementasi ERPNext v16

- Aktifkan `enable_serial_and_batch_no_for_item` pada Stock Settings.
- Stock Entry Detail menunjuk ke `Serial and Batch Bundle`.
- Batch identity berada pada child `Serial and Batch Entry`; field `batch_no` pada Stock Ledger Entry dapat kosong meskipun posting batch berhasil.
- Read-back reconciliation harus memeriksa Stock Entry Detail → Serial and Batch Bundle → entries, bukan hanya `Stock Ledger Entry.batch_no`.
