THRIFTORIA FIX18 - Ongkir ASLI dari Ekspedisi (RajaOngkir) + Fix Ongkir Muncul Sebelum Pilih Kota

BUG DI SCREENSHOT:
- Order THR-FV5ZQM: No HP -, Alamat -, Kota -, tapi Ongkir Rp 11.000 sudah muncul.
- Penyebab: order lama (sebelum Fix17), ongkir flat default 11000, tidak nunggu kota.
- Perbaikan: ongkir sekarang 0 sampai customer pilih kota + kurir. Kalau belum pilih kota, Total Bayar = Subtotal saja, dan checkout DITOLAK dengan alert "Pilih kota dulu".

YANG BARU - ONGKIR DARI PIHAK EKSPEDISI:
1. Customer pilih Kota dari dropdown (diambil dari /api/kota)
   - Kalau sudah pasang API Key RajaOngkir: daftar kota lengkap 500+ kota dari RajaOngkir
   - Kalau belum: daftar fallback kota besar (Medan, Jakarta, Bandung, dll) biar tetap jalan
2. Customer pilih Kurir (J&T, JNE, SiCepat, Pos, AnterAja, TIKI)
3. Web otomatis hitung ke /api/ongkir:
   - Berat = jumlah item x 500 gram (1 kaos/cargo = 500 gram)
   - Kirim origin (Medan/Batu Bara) -> destination (kota customer) -> weight -> courier ke RajaOngkir
   - RajaOngkir balas ongkir asli + estimasi hari (ETD) + pilihan layanan (REG, YES, dll)
   - Tampil: "Ongkir ASLI dari ekspedisi (JNT, 500 gram, ke Medan). Estimasi 2-3 hari"
   - Pilihan layanan: REG Rp 11.000 (2-3 hari) | YES Rp 22.000 (1 hari) dst.
4. Total Bayar = Subtotal + Ongkir ASLI. QRIS = Total Bayar itu.

CARA PASANG API KEY RAJAONGKIR (GRATIS, STARTER):
1. Daftar di https://rajaongkir.com atau https://komerce.id
2. Login -> Dashboard -> API Key -> Copy API Key Starter (gratis, 1000 hit / hari, cukup untuk thrift)
3. Di Vercel: Project thriftoria-lilac -> Settings -> Environment Variables -> Add:
   - Name: RAJAONGKIR_API_KEY
   - Value: (paste API Key kamu)
   - Name: ORIGIN_CITY_ID
   - Value: 152 (Medan) atau cari ID kota Indrapura/Batu Bara di https://rajaongkir.com/dokumentasi
4. Redeploy tanpa cache.
5. Tes: pilih kota Medan -> ongkir harusnya muncul angka asli, bukan estimasi lagi. Di bawah ongkir ada tulisan "Ongkir ASLI dari ekspedisi".

KALAU BELUM PASANG API KEY:
- Web tetap jalan, tapi ongkir pakai estimasi flat + tulisan "Ini masih ESTIMASI (belum pasang API Key RajaOngkir)".
- Jadi tidak menipu customer, jelas itu estimasi.

CARA UPDATE:
git add .
git commit -m "ongkir asli rajaongkir fix ongkir muncul sebelum kota"
git push
Vercel -> Redeploy tanpa cache

CARA TES:
1. Tambah Kaos Oversize ke keranjang
2. Isi Nama, No HP, Alamat
3. Kota: belum pilih -> Ongkir harus Rp 0, Total = Rp 35.000 saja
4. Pilih Kota Medan -> tunggu 2 detik -> Ongkir muncul (misal Rp 11.000), Total jadi Rp 46.000
5. Ganti kurir JNE -> ongkir berubah lagi
6. Checkout -> di halaman QRIS, alamat + ongkir + total harus sama dengan yang di keranjang
