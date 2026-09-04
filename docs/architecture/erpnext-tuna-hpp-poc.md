# ERPNext + Tuna Traceability/HPP POC

Status: disetujui untuk implementasi awal.

## Sasaran

Membuktikan alur berikut tanpa membuat ledger ganda:

`ERPNext Purchase Receipt → lot pembelian → ikan individual → batch produksi → loin variabel + grade → yield/mass balance → HPP → stok ERPNext`

## Keputusan bisnis

- ERP core: ERPNext/Frappe.
- Setiap ikan diberi identitas dan ditimbang saat penerimaan.
- Jumlah loin per ikan fleksibel dan dapat lebih dari empat.
- Grade dicatat pada setiap loin.
- Setiap loin harus dapat ditelusuri dan dipindahkan sebagai unit stok individual, sementara kuantitas ledger tetap berbasis kg.
- Target total loin adalah 60% dari berat ikan; tidak ada target 15% per loin.
- HPP berasal dari biaya aktual bahan baku, proses/ABF, packing, freight, dan handling.

## Kepemilikan data

| Data | System of record |
|---|---|
| Supplier, item, PO, Purchase Receipt | ERPNext |
| Ikan, loin, grade, yield, mass balance, genealogy | Tuna Engine |
| Stock ledger, valuation, accounting | ERPNext |
| Outbox dan status sinkronisasi | Tuna Engine |

## Formula

- `expected_total_loin_kg = fish_weight_kg × 0.60`
- `actual_total_loin_kg = Σ berat loin QC-pass`
- `actual_yield_pct = actual_total_loin_kg / fish_weight_kg × 100`
- `variance_kg = actual_total_loin_kg - expected_total_loin_kg`
- `batch_cost = Σ komponen biaya aktual`
- HPP loin dialokasikan proporsional terhadap berat aktual loin.
- Berat maksimal tiga angka desimal; Rupiah integer.
- Sisa pembulatan diberikan kepada output terakhir dalam urutan stabil sehingga total alokasi tepat sama dengan biaya batch.

## Model integrasi

Setiap write ke ERPNext memakai idempotency key yang dapat dicari pada dokumen remote. Tuna Engine menyimpan event outbox dengan status `pending`, `processing`, `succeeded`, atau `failed`, jumlah percobaan, error terakhir, DocType, dan nama dokumen remote.

Batch lokal hanya boleh menjadi `posted` setelah dokumen ERPNext dibaca kembali dan kuantitas, nilai, serta identitasnya sesuai.

## Spike pertama

Bandingkan dua representasi:

1. satu Batch ERPNext per loin;
2. satu Serial Number ERPNext per loin dengan field berat/traceability.

Pilihan harus membuktikan:

- ledger dapat memakai kuantitas kg;
- identitas loin bertahan saat stock movement;
- valuation tetap benar;
- partial movement/sale berfungsi;
- genealogy dapat ditelusuri ke Purchase Receipt;
- tidak perlu memodifikasi core ERPNext.

## Acceptance criteria POC

- Retry tidak membuat Purchase Lot atau stock posting ganda.
- Satu ikan dapat memiliki lebih dari empat loin dengan grade berbeda.
- Yield 60%, mass balance, dan alokasi HPP teruji.
- Berat/biaya negatif dan output nol ditolak.
- Genealogy Purchase Receipt → ikan → loin → stok ERPNext dapat dibuktikan.
- Posting dibaca kembali sebelum status lokal berubah menjadi `posted`.
