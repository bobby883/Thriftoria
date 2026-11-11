THRIFTORIA FIX21 - Fix Server Error 500 pas Checkout

BUG DI SCREENSHOT:
- Frontend sudah benar (Nama tini, HP, Alamat Tanjung Gading, Kota Medan, J&T, Ongkir 11.000, Total 36.000)
- Tapi klik Checkout -> popup "Checkout gagal: Server error" + tombol jadi "Memproses..."
- Penyebab: di api/index.py, fungsi api_checkout pakai variabel kurir & ongkir SEBELUM didefinisikan.
  Python langsung NameError -> Flask return 500 -> frontend tampilkan "Server error".
  Ini yang bikin order Beanie Hat Rp 25.000 + Ongkir 11.000 = 36.000 gagal terus.

YANG DIPERBAIKI:
1. api_checkout ditulis ulang total, urutannya benar:
   - Baca body dulu
   - Definisikan nama, no_hp, alamat, kota, kota_id, kurir, ongkir (int, default 0) SEBELUM dipakai
   - Validasi stok, kunci stok, simpan order + pengiriman di setiap baris order (ongkir hanya di baris pertama)
   - total_bayar = subtotal + ongkir, QRIS = total_bayar
   - try/except: kalau masih error, return JSON {"error":"Server error: <pesan asli>"} 500, bukan 500 kosong, biar frontend bisa tampilkan pesan aslinya.
2. api_order diperbaiki: return subtotal, ongkir, total_bayar, kurir, nama, no_hp, alamat, kota.
3. Frontend: alert tampilkan pesan server asli, bukan cuma "Server error".

CARA UPDATE:
git add .
git commit -m "fix server error checkout kurir ongkir"
git push
Vercel -> Redeploy tanpa cache
Browser -> Ctrl+Shift+R

CARA TES:
1. Tambah Beanie Hat ke keranjang
2. Isi Nama tini, HP 0823..., Alamat Tanjung Gading, Kota Medan, Kurir J&T
3. Ongkir muncul Rp 11.000, Total Rp 36.000
4. Klik Checkout -> harusnya langsung pindah ke halaman QRIS, TIDAK ada popup Server error lagi
5. Di QRIS, cek Pengiriman + Subtotal + Ongkir + Total Bayar harus sama
