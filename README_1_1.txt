THRIFTORIA - VERCEL FIX 404

KENAPA TADI 404?
- vercel.json lama pakai "builds" + "routes" -> Vercel terbaru nolak, jadi route ke /api/index.py tidak dibuat.
- Sekarang sudah diganti ke "rewrites" saja, ini format resmi Vercel sekarang.
- Path templates juga sudah dibenerin pakai absolute path.

CARA DEPLOY ULANG YANG BENAR:
1. Hapus deployment lama di Vercel (thriftoria-lilac) atau buat project baru.
2. Upload file zip FIX ini ke GitHub (timpa semua file lama, pastikan vercel.json yang baru ke-upload).
   - Cara cek: buka vercel.json di GitHub, harus isinya cuma "rewrites", BUKAN "builds".
3. Di Vercel -> Deployments -> Redeploy -> pilih "Redeploy with existing build cache" dimatikan (Clear cache).
4. Tunggu sampai Status: Ready.
5. Buka: https://thriftoria-lilac.vercel.app/  -> harusnya langsung muncul THRIFTORIA.STORE

KALAU MASIH 404:
- Cek di Vercel -> Deployments -> Logs, cari "Build Completed"
- Pastikan di GitHub ada folder: api/index.py (bukan api/index.py di dalam folder lain)
- Pastikan ada file: vercel.json, requirements.txt di ROOT (sejajar api/, bukan di dalam api/)
- Jangan deploy dari folder templates/, deploy dari ROOT.

URL:
- Toko: /
- Admin: /login (admin / thriftoria123)
- Analyst: /analyst
- API: /api/data-analyst

STRUKTUR YANG BENAR DI GITHUB:
thriftoria/
  api/index.py
  templates/*.html
  vercel.json
  requirements.txt
  README.txt
