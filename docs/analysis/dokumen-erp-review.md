# Analisis Kebutuhan `Dokumen-erp.pdf`

Sumber: `Dokumen-erp.pdf`, 10 halaman.

## Kesimpulan

Dokumen menggambarkan target ERP yang masuk akal, tetapi bukan satu aplikasi custom yang perlu dibangun seluruhnya dari nol. Sebagian besar transaksi komersial, procurement, inventory ledger, dan finance dapat memakai ERPNext standar. Nilai khusus KLG berada pada Tuna Traceability/HPP Engine, customer-owned stock, cold-storage/ABF operations, dan kelak investor/CAPEX portal.

Arsitektur yang dipilih tetap:

- **ERPNext/Frappe**: system of record pembelian, penjualan, stock ledger, valuation, dan accounting.
- **Tuna Engine**: identitas ikan dan loin, grade, yield, mass balance, HPP operasional, dan genealogy.
- **Custom app `klg_erp`**: konfigurasi/domain tambahan, integrasi idempoten, ownership/custody, evidence checklist, dan tampilan operasional khusus.

Penyebutan PostgreSQL pada halaman 9–10 hanya contoh. Implementasi memakai MariaDB sesuai jalur standar ERPNext.

## Pemetaan 12 modul

| Modul PDF | Implementasi utama | Status MVP |
|---|---|---|
| Executive Dashboard (hlm. 1, 3) | ERPNext Workspace/Report + dashboard custom setelah sumber KPI stabil | Ringkas, bukan seluruh visual akhir |
| Sales & CRM (hlm. 1–2) | ERPNext Customer, Quotation, Sales Order, Delivery Note, Sales Invoice, Payment Entry | Masuk |
| Procurement (hlm. 1, 5–6) | ERPNext Material Request/RFQ/Supplier Quotation/PO/Receipt/Invoice/Payment + workflow nominal configurable | Masuk |
| Supplier Management (hlm. 1) | ERPNext Supplier dan Supplier Scorecard; seafood quality metrics bila perlu | Masuk |
| Inventory & Warehouse (hlm. 1–2, 8) | ERPNext Item/Warehouse/Batch/Serial and Batch Bundle; custom owner/custody, pallet/rack/QR | Masuk |
| Seafood Production (hlm. 1–2, 7) | Tuna Engine untuk proses/yield/genealogy; posting stock dan valuation ke ERPNext | Masuk |
| Cold Storage & ABF (hlm. 1, 8) | Custom operations; ERPNext untuk stock movement dan invoice jasa | Ownership/custody masuk; billing lengkap dapat bertahap |
| Logistics (hlm. 2) | ERPNext Delivery Note/Shipment + custom POD, reefer, temperatur | Fase berikutnya kecuali delivery dasar |
| Finance & Accounting (hlm. 2, 6) | ERPNext GL/AP/AR/cash-bank/P&L/Balance Sheet/Cash Flow/Budget/Cost Center | Basic accounting masuk; pajak fase khusus |
| Investor Management (hlm. 2–4) | Custom read-only portal dan subledger yang direkonsiliasi ke GL | Fase berikutnya |
| Project & CAPEX (hlm. 2, 4–5) | ERPNext Project/Budget/Asset/Cost Center + custom workstream/progress/reimbursement | Fase berikutnya |
| Document & Audit Trail (hlm. 2, 8–9) | Frappe attachments/version/workflow log + custom evidence checklist/folder view | Minimum wajib masuk |

## Scope go-live pertama yang disepakati

1. Master supplier, customer, item, grade, warehouse, dan ownership.
2. Procurement: request → budget check → approval → RFQ/comparison → PO → receipt → invoice → payment.
3. Receiving tuna individual dan purchase lot.
4. Produksi: ikan → loin variabel → grade per loin → yield 60% total → mass balance.
5. HPP provisional, kemudian finalisasi ketika seluruh biaya aktual tersedia.
6. Inventory KLG dan customer-owned stock, tanpa memasukkan aset customer sebagai persediaan milik KLG.
7. Sales dasar: quotation/order → alokasi FIFO per grade dengan override → delivery → invoice → collection.
8. Basic accounting, cost center/project tagging, evidence, audit trail, dan dashboard ringkas.
9. Investor/CAPEX, pajak Indonesia penuh, logistics/reefer lanjutan, dan portal investor ditunda.

## Keputusan data dan costing

- Satu badan hukum, satu pembukuan, dan satu lokasi/cabang operasional pada tahap awal.
- Implementasi greenfield; migrasi hanya master data dan saldo awal.
- Setiap ikan diberi kode dan ditimbang saat receiving.
- Persediaan menyimpan kg aktual sekaligus jumlah unit/karton/pallet sesuai jenis barang.
- Jumlah loin fleksibel; grade berada pada setiap loin.
- Satu ERPNext Batch mewakili satu loin, kuantitas ledger dalam kg.
- Target yield adalah total loin `60% × berat ikan`, bukan target per loin.
- Biaya aktual batch dialokasikan proporsional berdasarkan berat loin.
- HPP provisional dipakai saat produksi; final cost dibuat setelah freight/handling/invoice aktual lengkap, dengan jejak adjustment yang dapat diaudit.
- Mass-balance tolerance configurable per proses/jenis produk.
- Sales melakukan FIFO otomatis per grade dan memberi override manual berizin.
- Customer-owned stock tidak berpindah menjadi milik KLG pada MVP.
- Receiving/produksi berjalan online dengan input manual, printer label, dan scanner QR; integrasi timbangan/offline ditunda.
- Approval matrix configurable; nominal pada PDF halaman 5–6 hanya contoh.
- Fiscal year Januari–Desember dan base currency IDR. Saldo awal per 31 Desember 2026; target go-live 1 Januari 2027.
- ERPNext v16 yang terpasang memiliki template Chart of Accounts Indonesia terverifikasi; gunakan sebagai dasar lalu tambahkan akun khusus tuna/manufaktur/cold-storage.

## Default kebijakan yang direkomendasikan

### Mass balance

- Rumus wajib: `input = loin + by-product + reject + waste + process loss + unexplained variance`.
- Sistem memberi peringatan jika unexplained variance melebihi `0,5%` dari berat input batch.
- Posting diblokir jika melebihi `1,0%`.
- Supervisor Produksi bersama QA dapat melakukan override sampai `2,0%`, dengan alasan dan evidence.
- Di atas `2,0%` memerlukan investigasi dan persetujuan manajemen sebelum batch ditutup.
- Ambang ini merupakan baseline awal; evaluasi kembali setelah satu bulan data aktual.

### Pallet dan ownership

- Satu pallet hanya boleh mempunyai satu legal owner/customer, satu item, satu grade, dan satu production batch.
- Pallet boleh berisi banyak loin Batch jika seluruh atribut tersebut sama.
- Loin boleh dipindahkan antar-pallet melalui scan transaction; histori asal dan tujuan tidak boleh dihapus.
- Pallet adalah handling unit, bukan pengganti identitas Batch loin.

### Chart of Accounts

Gunakan template Indonesia ERPNext sebagai dasar dan tambahkan minimal akun persediaan bahan baku tuna, WIP, finished goods per kelompok produk, by-product, inventory variance/shrinkage, landed cost/freight, jasa ABF/cold storage, COGS tuna, serta akun clearing untuk HPP provisional/final. Customer-owned inventory dipantau pada custody subledger dan tidak masuk inventory asset KLG.

### Evidence minimum

- PO: request, quotation/comparison, dan approval.
- Payment: invoice, approval, serta bukti transfer/bank reference.
- Delivery: delivery document dan signed POD.
- Stock adjustment: count sheet, alasan, dan foto/evidence bila relevan.
- HPP final: daftar cost component dan referensi invoice sumber.

## Gap kritis

### 1. Customer-owned stock

Daftar customer stock dan pallet pada halaman 8 bukan hanya filter UI. Sistem harus memisahkan:

- **legal owner** barang;
- **custodian/location** fisik;
- apakah stock mempunyai valuation di buku KLG;
- pallet sebagai handling unit versus loin/batch sebagai stock identity;
- transfer ownership, release, shrinkage, dan dispute.

Stock titipan tidak boleh otomatis masuk inventory asset KLG. Ini membutuhkan model custody/ownership custom dan aturan posting yang diuji.

### 2. HPP provisional dan final

Contoh HPP halaman 7 mencampur harga pembelian dan biaya proses/logistik per kg. Sistem perlu menyimpan cost component, basis biaya, source invoice/document, status provisional/final, tanggal efektif, dan adjustment ke valuation. Riwayat HPP lama tidak boleh berubah tanpa audit event.

### 3. Approval dan segregation of duties

Diagram role halaman 9 belum mendefinisikan siapa yang boleh membuat, menyetujui, membayar, mengoreksi, membatalkan, atau melakukan override FIFO. Pembuat transaksi tidak boleh menyetujui transaksi yang sama jika kebijakan KLG mengharuskan pemisahan tugas.

### 4. Evidence bukan sekadar attachment

Digital Evidence Folder halaman 8–9 perlu evidence checklist berdasarkan jenis transaksi, status wajib/opsional, versi dokumen, uploader, timestamp, relasi ke approval, retention, dan aturan penghapusan. Transaksi tertentu sebaiknya tidak dapat disubmit sebelum evidence wajib lengkap.

### 5. Dashboard bergantung pada definisi KPI

Revenue, gross profit, cash, funds managed, risk, dan forecast pada halaman 3 harus memiliki definisi sumber, periode, status dokumen, currency, dan aturan refresh. Dashboard tidak boleh dibangun dari angka manual atau query yang berbeda dari GL/stock ledger.

## Urutan implementasi

### Fase 0 — Foundation

- Company, fiscal year, chart of accounts, cost center, warehouse, item/UOM, user/role.
- Workflow approval configurable.
- Audit/evidence baseline.
- Integration idempotency dan read-back reconciliation.

### Fase 1 — Core vertical slice

`Purchase Receipt → purchase lot → ikan → loin → yield/mass balance → HPP provisional → Batch ERPNext → stock read-back`

### Fase 2 — Sales dan finance dasar

`Quotation/Sales Order → FIFO grade allocation → Delivery Note → Sales Invoice → Payment Entry → margin aktual`

### Fase 3 — Customer-owned stock dan cold storage

Custody, pallet/rack/QR, occupancy, service events, ABF, dan invoice jasa.

### Fase 4 — Logistics, investor, dan CAPEX

POD/reefer/temperature; portal investor; fund utilization; project workstream; reimbursement.

### Fase 5 — Pajak dan executive analytics lanjutan

PPN/PPh/e-Faktur sesuai proses resmi yang dipilih, forecast, alerts, dan dashboard final.

## Acceptance gates lintas modul

1. Mengirim payload integrasi identik berulang kali tetap menghasilkan tepat satu dokumen ERPNext dan satu dampak ledger.
2. Setelah posting, quantity, warehouse, batch, incoming rate, valuation, dan remote document ID harus cocok pada read-back.
3. `output + by-product + reject + waste + process loss` tidak boleh melampaui input dan toleransi yang disetujui.
4. Total HPP seluruh output setelah pembulatan harus sama persis dengan total cost pool batch.
5. Purchase lot dapat ditelusuri dua arah sampai ikan, loin, pallet, stock position, delivery, dan buyer.
6. Stok milik customer tidak boleh muncul sebagai inventory asset KLG.
7. Perubahan vendor, amount, rekening bank, currency, atau evidence setelah approval membatalkan approval sebelumnya.
8. Creator transaksi tidak boleh menjadi final approver atau payment executor pada transaksi yang sama.
9. Koreksi transaksi submitted menggunakan cancel/amendment/reversal, bukan overwrite histori.
10. Billing otomatis ABF dan portal investor tidak boleh diaktifkan sebelum idempotency, reconciliation, approval versioning, dan isolasi akses lulus pengujian.

## Operational baseline terbaru

Detail receiving, produksi, pallet/rack, evidence, opening balance, dan aturan awal telah dipindahkan ke [`docs/requirements/business-baseline-v1.md`](../requirements/business-baseline-v1.md). Baseline penting:

- Director menjadi approver tanpa tier/batas nominal.
- Receiving mencatat identitas, berat, dan grade setiap tuna sebelum masuk chiller.
- Produksi mencatat setiap loin beserta berat, grade, dan tuna sumber.
- Grade awal: `AB`, `C`, dan `D`; output utama loin; by-product tetelan; waste darah; kategori reject tetap tersedia.
- Setiap pallet memiliki label/QR dan lokasi rack aktif; perpindahan wajib melalui transaksi tercatat.
- Saldo awal yang disahkan Finance mencakup kas/bank, AP, AR, inventory, aset, dan akun terkait.

## Pertanyaan lanjutan untuk validasi bisnis

1. Apakah Director hanya final approver atau juga satu-satunya pengguna/data entry?
2. Siapa yang memasukkan berat dan grade saat receiving dan produksi?
3. Apakah tetelan serta darah/waste ditimbang, dan pada level tuna individual atau production batch?
4. Apakah satu production event memproses satu tuna atau beberapa tuna sekaligus?
5. Apakah grade tuna dan loin memakai daftar `AB`, `C`, `D` yang sama, dan apakah grade dapat berubah setelah QC/ABF?
6. Apa kode area penyimpanan dan rack aktual saat lokasi siap dipetakan?
