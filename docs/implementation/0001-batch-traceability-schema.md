# Batch Traceability Schema — Tracer Bullet 1

## Tujuan

Menambahkan metadata minimum pada ERPNext `Batch` agar satu loin dapat ditelusuri ke Tuna Engine tanpa membuat stock ledger kedua.

## Field pada ERPNext Batch

| Field | Tipe | Tujuan |
|---|---|---|
| `custom_klg_external_loin_id` | Data, unique | Idempotency/reference ID loin dari Tuna Engine |
| `custom_klg_purchase_batch_id` | Data | Batch penerimaan tuna, misalnya satu lot 2 ton |
| `custom_klg_production_run_id` | Data | Sesi produksi yang menghasilkan loin |
| `custom_klg_source_fish_id` | Data | Tuna individual sumber loin |
| `custom_klg_grade` | Select | Grade literal `AB`, `C`, atau `D` |
| `custom_klg_original_weight_kg` | Float | Berat awal loin dalam kg dengan presisi tiga desimal |
| `custom_klg_owner_type` | Select | Legal owner: `KLG` atau `Customer` |
| `custom_klg_owner_customer` | Link Customer | Customer pemilik untuk custody stock |
| `custom_klg_pallet_id` | Data | Handling unit pallet aktif |

## Aturan

- Satu ERPNext Batch merepresentasikan satu loin.
- Quantity dan valuation resmi tetap berasal dari ERPNext stock ledger.
- `external_loin_id` unik untuk mencegah loin yang sama dibuat dua kali.
- `Legal Owner Type` wajib diisi.
- Batch milik `Customer` wajib memiliki `Owner Customer`.
- Batch milik `KLG` wajib mengosongkan `Owner Customer`.
- Aturan ownership divalidasi di server agar berlaku untuk Desk, REST API, dan import.
- Custom fields disinkronkan melalui `after_install` dan `after_migrate`, sehingga schema dapat direproduksi pada site baru.

## TDD evidence

RED pertama:

- test schema gagal karena `custom_klg_external_loin_id` belum tersedia.

RED kedua:

- test ownership gagal karena Batch KLG masih menerima `Owner Customer`.

RED ketiga, dari independent review:

- test layout gagal karena custom fields tanpa `insert_after` tidak tersusun di bawah section traceability.

RED keempat, dari independent review kedua:

- API/import masih dapat menyimpan owner `Customer` tanpa customer dan owner type kosong karena `mandatory_depends_on` hanya mengatur form, bukan invariant server.

GREEN:

```bash
bench --site klg.localhost run-tests --module klg_erp.tests.test_batch_traceability_fields
bench --site klg.localhost run-tests --app klg_erp
```

Keduanya lulus dengan tujuh integration tests yang mencakup schema, urutan layout, owner type wajib, kombinasi ownership valid, dan kombinasi ownership yang harus ditolak.

## Langkah berikutnya

Tracer bullet berikutnya adalah endpoint idempoten untuk menerima satu production run, membuat Batch loin, melakukan posting stock ERPNext, lalu membaca kembali quantity, batch identity, warehouse, dan valuation untuk reconciliation.
