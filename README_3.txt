THRIFTORIA FIX20 - Fix Tombol Checkout Tidak Respon (Mati)

BUG DI SCREENSHOT:
- Keranjang masih tampilan LAMA: cuma ada Nama (yanda), tidak ada No HP, Alamat, Kota, Kurir, Ongkir.
  Artinya browser masih buka versi lama (cache), belum Fix19.
- Backend Fix18/19 menolak checkout kalau ongkir 0 / kota kosong (return 400), tapi frontend lama tidak menampilkan error-nya.
  Hasilnya: klik Checkout -> diam, tidak pindah, tidak ada alert. Kayak tombol mati.

YANG DIPERBAIKI:
1. Backend TIDAK lagi menolak checkout kalau ongkir 0:
   - Ongkir 0 = "Ongkir Konfirmasi WA", tetap boleh checkout.
   - Admin chat WA customer untuk ongkir aslinya.
   - Jadi tombol tidak akan mati lagi karena validasi ongkir.
2. Frontend:
   - Kalau form pengiriman belum muncul (cache lama), muncul alert jelas:
     "Web kamu masih versi lama (cache). Refresh dulu pakai Ctrl+Shift+R, baru isi No HP, Alamat, Kota, baru Checkout."
   - Kalau fetch gagal / server return error, muncul alert: "Checkout gagal: <pesan error>" - tidak diam lagi.
   - Kalau ongkir 0, muncul confirm: "Ongkir belum kehitung (Rp 0). Lanjut checkout? Nanti admin chat WA kamu..."
   - Footer: "Thriftoria Fix20" biar ketahuan versi berapa yang kebuka.
3. Cara tes yang benar:
   - Habis Redeploy, di HP/browser: refresh pakai Ctrl+Shift+R (di HP: titik tiga -> Reload / Hard Reload)
   - Cek keranjang: harus ada No HP, Alamat, Kota, Kurir, Ongkir. Kalau masih cuma Nama doang, berarti masih cache lama, refresh lagi sampai muncul.
   - Isi semua, klik Checkout -> harus pindah ke QRIS, tidak diam lagi.

CARA UPDATE:
git add .
git commit -m "fix checkout tidak respon"
git push
Vercel -> Redeploy tanpa cache
Browser -> Ctrl+Shift+R
