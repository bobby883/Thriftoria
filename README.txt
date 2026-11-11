THRIFTORIA FIX7 - HOLOGRAM + SKELETON, NO CIRCLE

YANG BERUBAH:
- Background jadi gelap hologram #0A0A14, efek pelangi gerak (cyan-magenta-gold-green)
- Semua tombol & card jadi KOTAK TAJAM (clip-path), TIDAK ADA LAGI yang bulet / circle / pill 999px
- Judul THRIFTORIA pakai gradient hologram yang gerak
- Card ada efek kilau hologram yang jalan (shine)
- Loading pakai SKELETON: kotak-kotak abu-abu yang kedip geser, bukan spinner muter bulet. Di index, skeleton muncul 900ms lalu produk asli muncul. Di checkout, skeleton QR muncul dulu lalu QR asli muncul.
- Keranjang, checkout, admin, login semua konsisten hologram, tanpa circle.

CARA UPDATE:
git add .
git commit -m "hologram skeleton no circle"
git push
Vercel -> Redeploy tanpa cache
