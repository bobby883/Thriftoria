THRIFTORIA FIX23 - Keranjang Masih Model Lama (cuma Nama, tanpa Alamat/Ongkir)

MASALAH DI SCREENSHOT:
- Keranjang: Kaos Olive Rp 35.000 x 1 = Rp 35.000, cuma ada 1 kolom "yanda" (nama)
- Tidak ada: No HP, Alamat, Kota, Kurir, Ongkir
- Total langsung Rp 35.000, padahal harusnya 35.000 + ongkir
- Tombol langsung Checkout - Bayar QRIS, pembeli bingung kirim kemana
PENYEBAB: Backend Fix21 sudah support no_hp/alamat/kota/kurir/ongkir, tapi templates/index.html di Fix22 masih drawer LAMA (hanya buyerName). Jadi frontend tidak pernah kirim alamat/ongkir ke backend, backend terima ongkir=0.

YANG DIPERBAIKI FIX23:
1. Drawer keranjang ditulis ulang lengkap:
   Nama Penerima*, No HP/WA*, Alamat Lengkap*, Kota Tujuan* (dropdown dari /api/kota), Kurir* (J&T/JNE/SiCepat/POS/AnterAja/TIKI), tombol Cek Ongkir
   Rincian: Subtotal + Ongkir + Total Bayar (live)
2. Cek Ongkir: panggil /api/ongkir (Biteship kalau ada key, kalau tidak fallback flat J&T 11rb dst). Tampilkan sumber + estimasi.
3. Checkout: validasi semua field wajib. Kalau ongkir belum dicek (0), muncul confirm "Lanjut? Admin konfirmasi via WA". Kirim semua field ke /api/checkout. Tombol jadi Memproses... + kalau gagal tampilkan pesan server asli, tidak diam.
4. Halaman QRIS (checkout.html): tampilkan Penerima, No HP, Alamat, Kota, Kurir, Subtotal, Ongkir, Total (barang+ongkir) - jadi pembeli & admin tidak bingung.
5. Bonus: DATA_AWAL dummy Budi/Supplier 1,2jt yang bikin analyst -1,08jt di Fix22 ternyata belum kehapus - di Fix23 sudah benar-benar dihapus. Setelah Reset Data, analyst mulai dari 0.

CARA UPDATE (PENTING - JANGAN CUMA TIMPA 1 FILE):
Upload SEMUA isi zip ini ke GitHub (timpa index.html + index.py + checkout.html), lalu:
git add . ; git commit -m "fix keranjang alamat ongkir" ; git push
Vercel -> Redeploy (tanpa cache) -> Browser Ctrl+Shift+R (hard refresh)
Kalau masih muncul keranjang lama (cuma nama), berarti masih cache lama / file index.html belum ketimpa di GitHub.

CARA TES:
1. Tambah Kaos Olive ke keranjang
2. Harusnya muncul form Nama, HP, Alamat, Kota, Kurir, Cek Ongkir
3. Pilih Kota Medan, Kurir J&T, klik Cek Ongkir -> Ongkir muncul (misal Rp 11.000), Total jadi Rp 46.000
4. Klik Checkout -> pindah ke QRIS Rp 46.000 + tampil alamat + kurir
