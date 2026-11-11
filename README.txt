THRIFTORIA FIX28 - Filter Lengan Pendek Masih Nampilin Semua

SCREENSHOT: Dropdown sudah dipilih "Lengan Pendek", tapi yang muncul masih ada:
- Beanie Hat - Aksesoris Tanpa Lengan
- Kaos Oversize Panjang - Cream (Lengan Panjang)
Padahal harusnya cuma Lengan Pendek semua.

PENYEBAB (2 hal):
1. Filter lama baru jalan kalau klik tombol Filter. Di screenshot, URL-nya masih polos (thriftoria-lilac.vercel.app, tanpa ?lengan=...), artinya dropdown sudah dipilih tapi form belum ke-submit. Pembeli nyangka pilih dropdown langsung ke-filter - wajar, hampir semua toko begitu.
2. Perbandingan persis (==). Kalau data lama ada spasi / beda kapital ("Lengan pendek", " Lengan Pendek "), produk bisa lolos / hilang salah.

YANG DIPERBAIKI FIX28:
- Dropdown sekarang langsung ke-filter begitu dipilih (onchange submit). Tidak perlu klik tombol Filter lagi. Tombol Filter tetap ada buat yang suka klik.
- Perbandingan dinormalisasi: strip spasi + lower. "Lengan Pendek", "lengan pendek", " Lengan Pendek " dianggap sama.
- Banner hasil: "Menampilkan 2 dari 4 produk • Lengan: Lengan Pendek" + tombol Hapus Filter. Jadi jelas filter-nya aktif atau tidak.
- Kalau hasil 0: tampil pesan jelas "Tidak ada produk Lengan Pendek" + tombol Lihat Semua Produk, bukan grid kosong membingungkan.
- Kategori juga dinormalisasi sama (strip + lower).

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
CARA TES: Buka toko -> pilih Lengan Pendek -> halaman langsung reload, URL jadi ?lengan=Lengan+Pendek, yang muncul HARUS cuma Kaos Lengan Pendek (Hitam + Olive). Beanie Tanpa Lengan & Kaos Panjang Cream HARUS hilang. Pilih Semua Lengan -> semua balik lagi.
