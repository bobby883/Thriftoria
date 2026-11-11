THRIFTORIA FIX12 - 1 Tombol Tambah Barang (Modal)

YANG BARU:
- Di Admin (/admin), form tambah yang panjang DIHAPUS, diganti 1 tombol besar:
  [+ TAMBAH BARANG]
- Klik tombol itu -> muncul popup / modal tambah barang, isinya lengkap:
  * Nama Barang
  * Foto (HP Galeri / Kamera, preview langsung)
  * Deskripsi (kondisi, minus, bahan)
  * Grade: A - Like New / B - Bagus minus dikit / C - Ada minus jelas
  * Cocok untuk: Wanita / Pria / Unisex
  * Ukuran: S / M / L / XL / XXL / All Size
  * Kategori, Lengan, Harga, Stok
  * Tombol SIMPAN BARANG

- Di tabel Edit, tiap produk juga bisa edit Grade / Gender / Ukuran langsung, tanpa hapus produk.

- Di Toko, tiap produk sekarang tampil badge:
  [Grade A] [Wanita] [Ukuran L] [Kaos • Lengan Pendek]

CATATAN: Halaman yang kamu screenshot itu adalah /analyst (Data Analyst), memang tidak ada tambah barang di sana. Tambah barang hanya ada di /admin.

CARA UPDATE:
git add .
git commit -m "1 tombol tambah barang modal grade gender ukuran"
git push
Vercel -> Redeploy tanpa cache

CARA PAKAI:
1. Buka /admin-login -> login
2. Klik [+ TAMBAH BARANG]
3. Isi foto, deskripsi, grade, harga, Wanita/Pria, ukuran
4. SIMPAN BARANG -> langsung muncul di toko
