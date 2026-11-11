THRIFTORIA FIX27 - Kenapa Kadang Internal Server Error Saat Masukin Barang?

PENYEBAB UTAMA (ketemu di kode Fix26):
1. KIRIM GANDA - ini biang-nya. Form Admin kirim DUA-DUANYA:
   - File foto MENTAH (sampai 2MB per foto, dari HP)
   - + Base64 hasil kompres di browser
   Server lalu ngumpulin dua-duanya. Dedup gagal karena isinya beda (mentah vs kompres).
   Hasilnya: 1 produk 5 foto bisa jadi payload 10-20MB. Vercel limit request ~4.5MB -> server lempar 500 / Internal Server Error. Makanya KADANG error (pas foto banyak / foto besar), KADANG lolos (pas foto 1, kecil).
2. HARGA/STOK KOSONG ATAU BUKAN ANGKA -> int('') melempar ValueError -> 500 tanpa pesan. Kamu tidak tau salahnya di mana.
3. FOTO MENTAH DIPOTONG 2MB -> file jadi rusak / base64 membengkak 2.7MB per foto.

YANG DIPERBAIKI FIX27:
- Server: kalau base64_list sudah ada (sudah dikompres), pakai ITU SAJA, file mentah diabaikan. Tidak ada lagi kirim ganda.
- Browser: sebelum Simpan, kalau base64 sudah ada, input file dikosongkan otomatis, jadi browser HANYA kirim base64 kompres. Total dicek: kalau >2.5MB, Simpan dibatalkan + alert "kurangi foto".
- Kompres diperketat: max 700px (dari 800), kualitas 0.72 (dari 0.8), tiap foto dipotong max 260KB di server. 10 foto = max ~2.6MB, aman.
- Validasi: Nama wajib, Harga/Stok harus angka >/=0. Kalau salah, sekarang muncul HALAMAN ERROR JELAS ("Harga harus diisi angka...") + tombol Kembali ke Admin, bukan lagi halaman putih "Internal Server Error".
- Tambah/Edit dibungkus try/except: error apapun ditangkap, tampilkan pesan + saran (kurangi foto), bukan 500 kosong.
- Foto mentah >2MB sekarang ditolak dengan pesan jelas, bukan dipotong jadi rusak.

CARA MENGHINDARI ERROR KE DEPAN (buat kamu):
- Pilih foto lewat tombol foto di Admin (biar dikompres otomatis), jangan drag file mentah besar.
- Kalau mau 10 foto, pakai foto dari kamera HP biasa (bukan foto RAW / screenshot 4K).
- Isi Nama, Harga (angka saja, tanpa Rp / titik), Stok dulu sebelum Simpan.
- Kalau tetap muncul halaman "Gagal simpan", baca pesannya, jangan klik Simpan berulang-ulang (bisa bikin barang duplikat).

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
CARA TES: Admin > Tambah Barang > pilih 5 foto besar dari HP > Simpan > harus lolos, tidak 500. Coba Harga dikosongkan > Simpan > harus muncul halaman "Harga harus diisi angka", bukan Internal Server Error.
