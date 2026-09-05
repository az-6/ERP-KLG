# Baseline Kebutuhan Bisnis KLG — Versi 1

Status: working baseline berdasarkan informasi awal dari tim IT/teknis. Keputusan proses dan saldo awal tetap perlu disahkan pemilik proses/Finance sebelum production go-live.

## 1. Organisasi dan approval

- Badan hukum: satu.
- Pembukuan: satu.
- Lokasi operasional: satu.
- Operator melakukan data entry receiving dan produksi; pada MVP satu operator dapat menangani kedua fungsi.
- Director menjadi final approver dan tidak melakukan data entry rutin.
- Tidak ada tingkat/batas nominal approval.
- Default workflow: transaksi finansial dan adjustment yang membutuhkan approval diarahkan kepada Director tanpa tier nominal.
- Sistem tetap menggunakan role `Operator`, `Director Approver`, dan `Finance` secara terpisah agar audit trail menunjukkan tindakan yang dilakukan dan role dapat dikembangkan saat pengguna bertambah.

## 2. Receiving tuna

Alur operasional:

1. Tuna datang ke lokasi receiving.
2. Operator memberi identitas unik pada setiap tuna.
3. Operator mencatat berat aktual dan grade tuna.
4. Tuna masuk ke chiller.
5. Perpindahan dari receiving ke chiller dicatat sebagai stock/location event.
6. Tuna kemudian dikeluarkan dari chiller untuk diproses menjadi loin.

Data minimum receiving:

- purchase receipt/purchase lot;
- supplier;
- kode tuna individual;
- tanggal dan waktu receiving;
- berat aktual dalam kg;
- grade;
- status penerimaan;
- lokasi awal dan lokasi chiller;
- operator pencatat.

## 3. Produksi dan traceability

- Produk awal yang ditangani: Tuna.
- Grade yang digunakan, dipertahankan literal: `AB`, `C`, dan `D`.
- Tuna yang diterima bersama, misalnya penerimaan 2 ton, membentuk satu `Purchase Batch`.
- Setiap Purchase Batch berisi banyak tuna individual yang tetap memiliki ID dan berat masing-masing.
- Satu Purchase Batch dapat diproses sekaligus atau dibagi menjadi beberapa `Production Run` pada waktu/hari berbeda.
- Setiap Production Run memilih subset tuna dari Purchase Batch; satu tuna tidak boleh aktif pada dua run sekaligus.
- Output utama: loin.
- Jumlah loin per tuna fleksibel.
- Setiap loin memiliki identitas, berat aktual, grade, referensi ke tuna asal, Production Run, dan Purchase Batch.
- Daftar grade tuna dan loin sama (`AB`, `C`, `D`), tetapi grade loin dapat berubah setelah QC/ABF.
- Perubahan grade setelah QC/ABF wajib menyimpan grade lama, grade baru, alasan, waktu, dan pengguna yang melakukan perubahan.
- Satu loin direpresentasikan sebagai satu ERPNext Batch dengan stock UOM kg.
- Target total berat loin: 60% dari berat tuna sumber.
- By-product: `tetelan`, termasuk rahang, tulang, dan bagian lain yang masih dikelompokkan sebagai tetelan.
- Waste awal: darah.
- Tetelan dan waste ditimbang secara aktual per Production Run, bukan diestimasi atau wajib ditimbang per tuna individual.
- Reject jarang terjadi, tetapi kategori reject tetap tersedia agar kejadian pengecualian dapat dicatat.

Mass balance wajib menyimpan:

`berat tuna masuk = loin + tetelan + reject + darah/waste + process loss + unexplained variance`

Default kontrol awal:

- warning jika unexplained variance melebihi 0,5% berat input;
- blok posting jika melebihi 1,0%;
- override hingga 2,0% memerlukan alasan, evidence, dan persetujuan Production Supervisor/QA atau Director jika role tersebut belum tersedia;
- di atas 2,0% memerlukan investigasi sebelum production batch ditutup.

## 4. Warehouse, rack, dan pallet

- Area penyimpanan dibagi berdasarkan jenis/kategori barang.
- Rack/location mengikuti lokasi fisik yang tersedia.
- Setiap pallet harus memiliki lokasi/rack aktif.
- Perpindahan pallet tidak diperbolehkan tanpa pencatatan stock/location movement.
- Setiap pallet memiliki ID dan label/QR untuk tracking barang dan stok.

Default aturan pallet:

- satu legal owner/customer;
- satu item;
- satu grade;
- satu production batch;
- dapat berisi banyak loin Batch jika seluruh atribut di atas sama;
- loin dapat dipindahkan antar-pallet hanya melalui transaksi scan yang menyimpan asal, tujuan, waktu, dan operator;
- pallet merupakan handling unit, bukan pengganti identitas Batch loin.

## 5. Dokumen/evidence minimum

### Purchase Order

- Purchase Order yang telah disetujui Director.

### Pembayaran

- invoice/tagihan;
- bukti approval;
- bukti transfer atau pembayaran.

### Delivery

- Delivery Order/Surat Jalan;
- bukti penerimaan barang jika tersedia.

### Stock Adjustment

- form/dokumen adjustment;
- alasan adjustment;
- approval pihak berwenang, dengan default Director.

Evidence ditautkan ke transaksi dan menyimpan uploader, timestamp, jenis evidence, dan versi. Perubahan material setelah approval membatalkan approval sebelumnya.

## 6. Volume dan kapasitas

Volume bulanan belum tersedia. Pengukuran awal mencakup:

- penerimaan barang;
- pengeluaran/delivery;
- perpindahan stok;
- stock adjustment;
- jumlah tuna individual;
- jumlah loin;
- jumlah pallet;
- dokumen pembelian, penjualan, dan pembayaran.

Desain tidak boleh menetapkan limit kecil atau asumsi empat loin. Monitoring volume diaktifkan sejak pilot agar sizing dapat disesuaikan dari data aktual.

## 7. Opening balance dan cutover

- Fiscal year: Januari–Desember.
- Base currency: IDR.
- Saldo awal: 31 Desember 2026.
- Target go-live: 1 Januari 2027.
- Implementasi greenfield; migrasi hanya master data dan saldo awal.
- Saldo awal mencakup kas/bank, piutang, utang, persediaan, aset, dan akun terkait.
- Hanya saldo yang telah direview dan disahkan Finance yang dapat diimpor.
- Import opening balance harus direkonsiliasi kembali ke dokumen persetujuan Finance.

## 8. Chart of Accounts

Gunakan verified Indonesian Chart of Accounts yang tersedia pada ERPNext v16 sebagai baseline, lalu tambahkan akun khusus:

- raw material tuna;
- work in progress;
- finished goods;
- by-product;
- inventory variance/shrinkage;
- freight dan landed cost;
- jasa ABF/cold storage;
- COGS tuna;
- clearing HPP provisional/final.

Customer-owned stock tidak dicatat sebagai inventory asset KLG.

## 9. Keputusan yang masih memerlukan validasi bisnis

1. Apakah target yield 60% berlaku untuk semua ukuran tuna dan semua kondisi bahan baku, atau perlu target per size/grade.
2. Siapa pengguna Finance yang melakukan verifikasi invoice, payment entry, bank reconciliation, dan opening balance.
3. Apakah perubahan grade loin setelah QC/ABF memerlukan approval Director atau cukup audit log oleh operator/QA.
4. Daftar area fisik dan kode rack/location aktual.
5. Tahun pertama volume transaksi aktual untuk capacity baseline.
