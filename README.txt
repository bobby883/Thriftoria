THRIFTORIA FIX14 - Tambah Logo Asli (T + Gantungan)

LOGO:
- File: static/logo.png (hasil crop dari Logo Thriftoria.pdf yang kamu kirim)
- Logo: Huruf T coklat tua + gantungan oranye di atasnya + tulisan thriftoria + PRELOVED THRIFT VINTAGE
- Route: /static/logo.png (via Flask send_file, biar jalan di Vercel)

DIPASANG DI:
- Topbar (kiri atas): logo kecil 44px + THRIFTORIA.STORE
- Hero toko: logo besar 180px di tengah, di atas judul
- Login / Admin / Analyst / Checkout: logo kecil di atas judul

CARA UPDATE:
git add .
git commit -m "tambah logo thriftoria"
git push
Vercel -> Redeploy tanpa cache

CATATAN:
- Kalau mau logo yang lebih jernih (tanpa background cream), kirim file PNG asli logo-nya (bukan screenshot PDF), nanti aku gantiin static/logo.png dengan yang asli.
- Background logo sekarang cream #FFF6EC, nyatu dengan tema cream glass.
