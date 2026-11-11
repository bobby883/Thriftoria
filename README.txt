THRIFTORIA FIX24 - QRIS Nyangkut di Skeleton "Memuat QRIS..."

SCREENSHOT: /checkout?order_id=THR-JXTVBF - skeleton muter terus, QRIS tidak muncul.

ADA 2 PENYEBAB, 2-DUANYA DIBENERIN:
1. BUG JS (penyebab langsung): di checkout.html load() lama, kalau /api/order balikin error/404, kode ini jalan:
   d.total.toLocaleString() -> padahal d.total = undefined (karena d = {error:...})
   -> TypeError, fungsi load() berhenti di tengah, box TIDAK PERNAH diganti, skeleton muter selamanya.
   Jadi bukan QRIS-nya yang lama, tapi halaman-nya crash diam-diam.

2. BUG SERVERLESS (penyebab kenapa 404): data disimpan di /tmp Vercel. Vercel bisa pindah instance / reset /tmp kapan saja, apalagi habis Redeploy.
   Order dibuat di instance A, halaman QRIS kebuka di instance B -> /api/order bilang "Order tidak ditemukan" -> kena bug no.1 -> skeleton.

YANG DIPERBAIKI FIX24:
- load() ditulis ulang: cek error dulu TANPA pakai d.total. Kalau error, tampilkan pesan jelas + tombol COBA LAGI + KEMBALI KE TOKO, tidak pernah lagi nyangkut di skeleton.
- Fallback localStorage: pas checkout di index.html, snapshot order (order_id, total, subtotal, ongkir, nama, alamat, kurir, rincian) disimpan di HP (thriftoria_last_order). Kalau /api/order 404, halaman QRIS tetap render dari snapshot HP, dengan peringatan kuning "Server Vercel ke-reset, QRIS dari data HP". Jadi pembeli tetap bisa bayar.
- confirmPay() juga anti-crash: kalau server 404, tetap lanjut ke Nota dari snapshot + suruh konfirmasi ke admin via WA.
- renderOrder() dipisah jadi fungsi sendiri, dipakai API maupun fallback, biar tampilannya sama.

CATATAN JUJUR: Fix ini bikin QRIS tetap muncul walau server ke-reset, tapi data order di server tetap bisa hilang kalau Vercel reset /tmp. Solusi permanennya nanti pindah database (misal Supabase / Upstash Redis), bukan /tmp. Untuk sekarang, kalau order hilang di server, admin cek Nota dari pembeli + konfirmasi WA.

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
CARA TES: checkout Kaos Olive lagi -> halaman QRIS harus langsung muncul (tidak skeleton). Matikan / refresh berkali-kali tetap muncul. Kalau muncul banner kuning, itu artinya fallback HP yang jalan - totalnya tetap benar.
