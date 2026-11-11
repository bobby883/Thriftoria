THRIFTORIA FIX16 - Logo di DALAM Kertas Nota (ikut ke-print)

MASALAH SEBELUMNYA:
- Logo ada di LUAR kertas nota, di header atas halaman.
- Pas klik Print, yang ke-print cuma kertasnya, logo di atas kepotong / kecil, seperti di screenshot kamu.

YANG DIPERBAIKI:
1. Logo dipindah KE DALAM kertas nota (#kertasNota):
   - Logo besar 170px di paling atas kertas, di tengah
   - Di bawahnya: THRIFTORIA.STORE + PRELOVED • THRIFT • VINTAGE
   - Garis putus-putus pemisah, baru isi nota (Order ID, Status, Pembeli, Produk, Total)
2. Mode PRINT khusus (@media print):
   - Tombol Print / Kembali ke Toko + header luar + footer luar disembunyikan (class no-print) -> tidak ikut ke-print
   - Yang ke-print HANYA kertas nota, background putih, border hitam, logo tetap muncul
   - Notif Pembayaran + logo kecil di dalamnya juga tetap ikut ke-print
   - Footer "Terima kasih sudah belanja di THRIFTORIA" ikut ke-print di bawah kertas

CARA UPDATE:
git add .
git commit -m "logo di dalam kertas nota ikut ke-print"
git push
Vercel -> Redeploy tanpa cache

CARA TES PRINT:
1. Buka nota order (misal THR-164WLO)
2. Klik Print / Simpan Nota -> di preview print, cek logo Thriftoria muncul di atas kertas nota, gede, tidak kepotong
3. Kalau masih kecil / kepotong, refresh Ctrl+Shift+R dulu
