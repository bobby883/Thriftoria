THRIFTORIA FIX6 - Keranjang + QRIS + Stok Hilang

YANG BARU:
1. KERANJANG: Pembeli bisa + Keranjang banyak barang, ubah qty, hapus, lihat total. Keranjang tersimpan di browser.
2. STOK 1 = HILANG: Di api/index.py, produk stok 0 disembunyikan dari web. Jadi kalau stok 1 dan kebeli, langsung hilang.
   Di toko ada badge: SISA 1 - REBUTAN, Sisa 3 aja, dll.
3. QRIS 1 TRANSAKSI = 1 KUNCI:
   - Checkout -> POST /api/checkout -> stok langsung dikurangi (dikunci), order dibuat status Menunggu Pembayaran
   - Muncul halaman /checkout?order_id=THR-XXXXXX dengan QRIS (scan via GoPay/OVO/DANA)
   - QR berisi: THRIFTORIA|ORDER_ID|TOTAL -> 1 QR hanya untuk 1 order, nominal terkunci pas
   - Timer 10 menit kunci stok
   - Tombol Saya Sudah Bayar -> status jadi Lunas
   - Jangan bayar 2x untuk order yang sama.

CARA UPDATE:
git add .
git commit -m "keranjang qris stok hilang"
git push
Vercel -> Redeploy tanpa cache

CATATAN QRIS ASLI:
QR di demo ini adalah QR contoh dari qrserver. Untuk QRIS asli yang masuk ke rekening kamu, ganti qris_text di api/index.py dengan string QRIS statis dari bank / QRIS merchant kamu (dari GoPay Merchant / QRIS BRI / dll), dan ganti URL QR di checkout.html dengan gambar QRIS asli kamu.
