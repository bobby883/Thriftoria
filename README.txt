THRIFTORIA FIX19 - Alternatif Ongkir Aman (Biteship / Komerce) - Gak Perlu Buka rajaongkir.com yang ke-flag McAfee

KENAPA McAfee NGE-FLAG rajaongkir.com?
- McAfee WebAdvisor sering salah flag web Indonesia.
- rajaongkir.com itu domain lama (dari 2014). Sekarang RajaOngkir sudah gabung ke Komerce, domain barunya komerce.id.
- Jadi jangan klik "Visit anyway" kalau tidak nyaman. Itu false positive, bukan berarti RajaOngkir penipuan.

PILIHAN AMAN (PILIH SALAH SATU SAJA, YANG PALING GAMPANG):

OPSI A - BITESHIP (REKOMENDASI, PALING AMAN, TIDAK KE-FLAG)
1. Buka biteship.com (aman, tidak ke-flag McAfee)
2. Daftar gratis -> Dashboard -> API Key -> Copy
3. Di Vercel: Settings -> Environment Variables:
   BITESHIP_API_KEY = (paste API Key kamu)
4. Redeploy. Ongkir langsung asli dari JNE, J&T, SiCepat, dll.

OPSI B - KOMERCE (PENERUS RAJAONGKIR)
1. Buka komerce.id (domain baru RajaOngkir, aman)
2. Daftar -> Dashboard -> API Key RajaOngkir Starter
3. Di Vercel:
   RAJAONGKIR_API_KEY = (paste API Key kamu)
   ORIGIN_CITY_ID = 152
4. Redeploy.

OPSI C - TETAP ESTIMASI + KONFIRMASI WA (KALAU MAU TANPA API SAMA SEKALI)
- Tidak perlu API sama sekali.
- Ongkir di web tampil sebagai Estimasi.
- Setelah customer checkout, admin chat WA: "Kak, ongkir aslinya Rp XX, totalnya jadi Rp XX, mau lanjut?"
- Customer transfer selisih ongkir via QRIS kedua. Ini cara yang dipakai banyak thrift kecil.

CARA UPDATE:
git add .
git commit -m "ongkir alternatif biteship komerce aman"
git push
Vercel -> Redeploy tanpa cache

CATATAN:
- API-nya (api.rajaongkir.com / api.biteship.com) beda dengan web-nya (rajaongkir.com). Jadi walaupun web lama ke-flag, API-nya tetap jalan.
- Kalau kamu tidak mau ribet API, pakai Opsi C dulu saja, tetap jalan, tidak perlu buka web yang ke-flag.
