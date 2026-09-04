# Development environment

Lingkungan ini mengikuti pola resmi Frappe Docker Devcontainer dan terpisah dari demo `pwd.yml`.
Bench utama disimpan pada named volume Docker `frappe-bench-data`, sehingga operasi Git,
Python environment, `node_modules`, dan build Frappe berjalan di filesystem Linux, bukan
di bind mount `C:\ERP` yang jauh lebih lambat.

```bash
docker compose -f .devcontainer/docker-compose.yml up -d
```

Di dalam container, Bench berada di `/workspace/development/frappe-bench` dan dijalankan
dari service `frappe`. Data Bench tidak terlihat sebagai file biasa di Windows karena
berada pada named volume. Custom app berada di `apps/klg_erp` pada workspace Windows
dan hanya folder kecil ini yang di-bind-mount ke Bench.

Folder `development/frappe-bench` pada drive Windows adalah sisa percobaan bootstrap
pertama yang terhenti dan tidak digunakan lagi.

## Status lokal

- Frappe `16.33.0`
- ERPNext `16.34.1`
- Custom app `klg_erp 0.0.1`
- Site: `klg.localhost`
- URL: <http://klg.localhost:8000>
- Kredensial development awal: `Administrator` / `admin`

Kredensial tersebut hanya untuk development lokal dan wajib diganti pada deployment nyata.

## Menjalankan Bench

```bash
docker compose -f .devcontainer/docker-compose.yml up -d
docker compose -f .devcontainer/docker-compose.yml exec -T frappe \
  bash -lc 'cd /workspace/development/frappe-bench && bench start'
```

Verifikasi:

```bash
curl http://klg.localhost:8000/api/method/ping
```
