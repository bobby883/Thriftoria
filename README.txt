THRIFTORIA FIX26 - 1 Produk Maksimal 10 Gambar

YANG DITAMBAH:
1. ADMIN > Tambah Barang: input foto sekarang bisa pilih banyak sekaligus (multiple). Counter "0 / 10 foto". Kalau pilih >10, alert + hanya 10 pertama dipakai. Preview grid 10 thumbnail. Foto ke-1 otomatis jadi foto UTAMA (cover).
2. ADMIN > Edit produk: tampil semua foto produk (maks 10) sebagai thumbnail. Foto UTAMA ada badge oranye. Di bawah tiap foto ada checkbox kecil: centang = hapus foto itu saat Simpan. Ada checkbox "Ganti semua foto lama dengan foto baru" - kalau dicentang, foto lama dibuang semua, diganti foto baru. Kalau tidak dicentang, foto baru DITAMBAH ke foto lama (sampai total 10).
3. TOKO (halaman depan): kalau produk punya >1 foto, tampil galeri thumbnail di bawah foto utama. Klik thumbnail -> foto utama ganti. Ada tulisan "X foto - klik untuk lihat".
4. BACKEND: produk sekarang simpan "gambar_list" (list, maks 10) + "gambar" (foto pertama, buat kompatibilitas). Produk LAMA yang cuma 1 foto tetap jalan: gambar_list_for() ubah 1 foto jadi list 1 item. Tidak perlu upload ulang.
5. Bonus fix: di Edit produk, deskripsi sekarang selalu tersimpan (sebelumnya hanya tersimpan kalau upload foto baru).

BATASAN (jujur): tiap foto dikompres ke max 800px JPEG 0.8 di browser sebelum dikirim, biar 10 foto tidak bikin /tmp Vercel jebol. Total per produk kira-kira 1-2 MB.

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
CARA TES:
- Admin > Tambah Barang > pilih 3-5 foto sekaligus > lihat preview + counter > Simpan > cek di toko: foto utama + thumbnail bisa diklik.
- Admin > Edit produk itu > centang 1 foto > Simpan > foto itu hilang.
- Coba pilih 11 foto > harus muncul alert maksimal 10.
