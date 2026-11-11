THRIFTORIA FIX3 - Warna nyaman + Admin bisa diklik + Analyst di dalam Admin

1. Warna: bg cream #FFF6EC, teks coklat tua #2B2118 (bukan hitam pekat), aksen terracotta + sage. Nyaman dilihat lama.
2. Admin fix: vercel.json sekarang kirim ?__path__=$1, middleware baca itu. /admin -> admin, /analyst -> analyst, / -> toko. Tidak balik ke toko lagi.
3. Analyst: link Data Analyst DIHAPUS dari halaman toko. Hanya ada di dalam /admin. /analyst tetap butuh login admin.

Deploy: git add . | git commit -m 'fix3 warna admin analyst' | git push | Vercel Redeploy tanpa cache
