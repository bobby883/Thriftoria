THRIFTORIA FIX15 - Fix Looping Checkout + Notif Pembayaran + Logo di Nota

BUG YANG DIPERBAIKI:
- Tombol SAYA SUDAH BAYAR & CEK STATUS tadi looping di halaman checkout saja, karena pakai location.reload().
- Sekarang:
  * SAYA SUDAH BAYAR -> status jadi Lunas -> langsung pindah ke /nota?order_id=THR-XXXXXX (tidak reload di tempat)
  * CEK STATUS -> fetch /api/order -> kalau sudah Lunas, langsung pindah ke nota. Kalau belum, muncul tulisan "Belum lunas, masih Menunggu Pembayaran"

YANG BARU:
1. NOTIF PEMBAYARAN dengan LOGO di halaman Checkout:
   [Logo Thriftoria] Notif Pembayaran — THRIFTORIA
   Order THR-XXXX dibuat. Total Rp XX • Status: Menunggu Pembayaran • Bayar QRIS di bawah, jangan bayar 2x.
   Notif ini update otomatis sesuai order.

2. NOTA pakai LOGO THRIFTORIA:
   - Logo besar 170px di atas nota
   - THRIFTORIA.STORE + PRELOVED • THRIFT • VINTAGE
   - Detail order lengkap: Order ID, Pembeli, tiap produk x qty, Total, Status
   - Notif box: [Logo] Pembayaran Lunas — Terima kasih sudah belanja di THRIFTORIA. Screenshot nota ini sebagai bukti.
   - Tombol Print / Simpan Nota + Kembali ke Toko

CARA UPDATE:
git add .
git commit -m "fix looping checkout notif logo nota"
git push
Vercel -> Redeploy tanpa cache

CARA TES:
1. Buka toko -> tambah keranjang -> Checkout -> muncul QRIS
2. Klik SAYA SUDAH BAYAR -> harusnya langsung pindah ke Nota (tidak muter di checkout lagi)
3. Di Nota, cek logo Thriftoria muncul di atas + notif pembayaran muncul
