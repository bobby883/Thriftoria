THRIFTORIA FIX25 - Tombol SAYA SUDAH BAYAR & CEK STATUS Tidak Respon

SCREENSHOT: QRIS sudah muncul (THR-22KYHF), tapi klik SAYA SUDAH BAYAR / CEK STATUS diam saja, tidak ada pesan, tidak pindah halaman.

PENYEBAB (ketemu di kode Fix24):
- Fungsi confirmPay() dan cekStatus() HILANG dari checkout.html. Kehapus waktu Fix24 rewrite load() pakai regex.
- Tombolnya masih onclick="confirmPay()" / onclick="cekStatus()", tapi fungsinya tidak ada -> browser lempar ReferenceError diam-diam, klik tidak ngapa-ngapain.
- Bonus bug: templates/nota.html TIDAK ADA filenya. Jadi kalaupun confirmPay jalan, redirect ke /nota akan 500 TemplateNotFound.

YANG DIPERBAIKI FIX25:
1. confirmPay() ditulis ulang lengkap:
   - Tampilkan "Memproses konfirmasi...", tombol jadi MEMPROSES... + disabled biar tidak diklik 2x
   - POST /api/confirm-payment/<oid> -> kalau sukses, update snapshot HP jadi Lunas, tampilkan "Pembayaran dikonfirmasi!" -> pindah ke /nota
   - Kalau server 404 (Vercel /tmp ke-reset): tampilkan peringatan + tetap lanjut ke Nota dari snapshot HP, suruh konfirmasi ke admin via WA. Tidak diam lagi.
2. cekStatus() ditulis ulang lengkap:
   - GET /api/order/<oid> -> kalau Lunas pindah ke Nota, kalau masih Menunggu tampilkan "Belum lunas..."
   - Kalau server error, cek snapshot HP, kalau snapshot sudah Lunas pindah ke Nota, kalau belum suruh klik SAYA SUDAH BAYAR.
3. Timer 10:00 dikembalikan (juga ikut kehapus di Fix24).
4. nota.html DIBUAT BARU (sebelumnya tidak ada):
   - Kalau server punya order, tampilkan nota dari server
   - Kalau server tidak punya (ke-reset), tampilkan nota dari snapshot HP + banner kuning "Screenshot nota ini + kirim ke admin via WA"
   - Kalau dua-duanya tidak ada, tampilkan pesan jelas + tombol Kembali ke Toko, bukan halaman 500 kosong.

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
CARA TES: Checkout lagi -> QRIS muncul -> klik CEK STATUS -> harus muncul "Belum lunas..." (bukan diam). Bayar (simulasi) -> klik SAYA SUDAH BAYAR -> harus muncul "Pembayaran dikonfirmasi!" -> pindah ke Nota.
