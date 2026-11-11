THRIFTORIA FIX22 - Data Analyst Salah / Minus 1.080.000

YANG SALAH DI SCREENSHOT:
- Total Penjualan Rp 120.000 (Kaos 70rb + Beanie 50rb) -> hitungannya BENAR
- Total Pembelian Rp 1.200.000 -> ini DATA CONTOH / DUMMY, bukan transaksi asli kamu:
  Di DATA_AWAL ada 2 nota contoh:
  1. Budi - Kaos Oversize - Rp 70.000 - penjualan - Lunas
  2. Supplier Jakarta - Hoodie 20 pcs - Rp 1.200.000 - pembelian / kulakan - Lunas
  Jadi 120.000 - 1.200.000 = -1.080.000. Rumusnya benar, datanya yang contoh.
- Total Transaksi 3 = 2 nota contoh + 1 order asli kamu.
- Bug kedua: analyst lama hitung SEMUA status, termasuk Menunggu Pembayaran & Refund. Jadi order yang belum dibayar ikut kehitung jadi penjualan, padahal belum masuk uang.

YANG DIPERBAIKI FIX22:
1. DATA_AWAL dibersihkan: "orders": [] - tidak ada lagi nota contoh Budi / Supplier 1,2jt.
   Setelah redeploy + Reset Data di Admin, analyst mulai dari 0.
2. Analyst sekarang HANYA hitung status Lunas:
   - Penjualan = tipe penjualan + status Lunas
   - Pembelian = tipe pembelian + status Lunas
   - Menunggu Pembayaran / Belum Lunas / Refund TIDAK dihitung, cuma ditampilkan jumlahnya di kartu Total Transaksi.
3. Tambah banner penjelasan cara baca angka di atas KPI.
4. Admin Total Penjualan juga diubah jadi Lunas saja, biar konsisten dengan Analyst.
5. File sampah dibersihkan (file _1, _2, dll dihapus) biar zip tidak bingung.

CARA BERSIHKAN DATA LAMA DI VERCEL (PENTING):
Setelah push Fix22 + Redeploy:
1. Login Admin -> klik Reset Data (kalau ada) ATAU hapus manual 2 nota contoh di Admin > Nota:
   - Hapus nota "Budi - Kaos 70.000"
   - Hapus nota "Supplier Jakarta - Hoodie 1.200.000"
2. Buka /analyst -> Refresh. Harusnya:
   - Kalau belum ada penjualan Lunas asli: Penjualan Rp 0, Pembelian Rp 0, Untung Rp 0
   - Kalau Beanie Hat 50rb sudah Lunas: Penjualan Rp 50.000, Pembelian Rp 0, Untung Rp 50.000
3. Kalau masih muncul 1,2jt, berarti masih baca /tmp lama - Redeploy lagi tanpa cache + Ctrl+Shift+R.

CARA UPDATE:
git add .
git commit -m "fix analyst dummy data dan hitung lunas saja"
git push
Vercel -> Redeploy
