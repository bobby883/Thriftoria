THRIFTORIA FIX8 - Cream + iPhone Glass, BUKAN Neon

YANG BERUBAH:
- Neon / hologram gelap DIHAPUS TOTAL. Tidak ada lagi cyan-magenta nyala.
- Balik ke CREAM lembut: bg #FDF3E7, teks coklat tua #2B2118, nyaman dilihat lama.
- Action button gaya GLASS IPHONE:
  background: rgba(255,255,255,.70) + backdrop-filter: blur(20px) saturate(180%)
  border: 1px solid rgba(255,255,255,.9)
  shadow lembut + inset highlight atas (efek kaca iPhone)
  radius 14px (kotak lembut, bukan circle, bukan tajam neon)
- Card juga glass: putih transparan 68% + blur 18px + border putih
- Topbar + keranjang drawer juga glass, kayak Control Center iPhone
- Skeleton tetap kotak cream (bukan spinner bulet)
- Keranjang, QRIS, stok hilang, admin pisah, dll tetap jalan seperti fix6/fix7

CARA UPDATE:
git add .
git commit -m "cream glass iphone"
git push
Vercel -> Redeploy tanpa cache
