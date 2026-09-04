# KLG ERP

ERP inti PT Katalis Lintas Global berbasis ERPNext/Frappe.

## Batas sistem

ERPNext adalah **system of record** untuk supplier, item, pembelian, persediaan bernilai, penjualan, dan akuntansi. Aplikasi tuna lama di `C:/KTG/sistem` tetap menjadi mesin operasional untuk identitas ikan, loin, grade, yield, mass balance, HPP, dan genealogy sampai integrasi baru terverifikasi.

Tidak boleh ada dua stock ledger atau accounting ledger yang sama-sama dapat ditulis.

## Struktur

- `deployment/frappe_docker/` — submodule resmi Frappe Docker.
- `docs/architecture/` — desain integrasi yang telah disepakati.
- `docs/decisions/` — keputusan arsitektur.
- `contracts/` — kontrak API Tuna Engine ↔ ERPNext.
- `apps/klg_erp/` — custom Frappe app; dibuat melalui Bench pada development environment.

## Development ERPNext

Bench development memakai named volume Docker agar operasi Git/build Frappe tidak berjalan
di filesystem Windows yang lambat. Custom app yang dapat diedit berada di `apps/klg_erp`.
Site aktif di <http://klg.localhost:8000>. Petunjuk lengkap: `docs/development.md`.

## ERPNext lokal untuk eksplorasi

Konfigurasi `pwd.yml` dari submodule hanya untuk eksplorasi dan spike, bukan development atau production.

```bash
cd deployment/frappe_docker
docker compose -f pwd.yml up -d
docker compose -f pwd.yml ps
```

ERPNext tersedia di <http://localhost:8080> setelah service `create-site` selesai. Kredensial demo berasal dari `pwd.yml` dan tidak boleh digunakan untuk produksi.

Matikan demo:

```bash
docker compose -f pwd.yml down
```

## Urutan kerja

1. ~~Spike representasi loin di ERPNext (Batch vs Serial Number).~~ Selesai: satu Batch per loin; lihat `docs/decisions/0002-loin-as-erpnext-batch.md`.
2. Buat development bench dan custom app `klg_erp`.
3. Implementasi kontrak idempoten dan read-back reconciliation.
4. Hubungkan Tuna Engine tanpa menjadikan ledger lokal sebagai ledger kedua.
