THRIFTORIA FIX17 - Form Pengiriman + Ongkir Otomatis

YANG BARU:
1. Di Keranjang, setelah pilih barang, customer WAJIB isi:
   - Nama lengkap
   - No HP / WA (biar kurir bisa hubungin)
   - Alamat lengkap (Jalan, No Rumah, Patokan, RT/RW)
   - Kecamatan / Kota (contoh: Medan, Indrapura)
   - Pilih Kurir -> ongkir otomatis kehitung:
     * J&T Express Rp 11.000
     * SiCepat Reg Rp 10.000
     * SiCepat BEST Rp 9.000
     * JNE Reguler Rp 12.000
     * JNE YES Rp 22.000
     * Pos Indonesia Rp 9.000
     * GoSend Same Day (Medan) Rp 15.000
     * Ambil di Toko GRATIS Rp 0 (tidak perlu alamat)

2. Hitungan Ongkir:
   Total Bayar = Subtotal Barang + Ongkir
   Contoh di screenshot kamu:
   Cargo Pants Khaki 95.000 + Kaos Oversize 40.000 = Subtotal 135.000
   + Ongkir J&T 11.000 = Total Bayar 146.000
   QRIS yang muncul = Rp 146.000 (sudah termasuk ongkir), bukan 135.000 lagi.

3. Di Checkout QRIS & Nota, sekarang tampil:
   - Blok Pengiriman: Nama, No HP, Alamat, Kota, Kurir
   - Rincian: Subtotal Barang + Ongkir + Total Bayar
   - Di Nota yang ke-print, alamat + ongkir juga ikut ke-print di dalam kertas, jadi admin bisa langsung kirim tanpa chat lagi.

4. Cara ganti harga ongkir:
   Buka api/index.py, cari ONGKIR_TABLE, ubah angka di sana. Misalnya J&T dari 11000 jadi 13000 kalau naik.
   Kalau mau ongkir akurat per kota (pakai RajaOngkir / API ekspedisi), nanti upgrade ke Fix18 - butuh API key RajaOngkir.

CARA UPDATE:
git add .
git commit -m "form pengiriman ongkir otomatis"
git push
Vercel -> Redeploy tanpa cache

CARA TES:
1. Tambah 2 barang ke keranjang
2. Isi Nama, No HP, Alamat, Kota, pilih J&T
3. Lihat Total Bayar berubah (subtotal + ongkir)
4. Checkout -> QRIS total sudah termasuk ongkir
5. Bayar -> Nota muncul alamat + ongkir, print nota -> alamat ikut ke-print
