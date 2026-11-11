THRIFTORIA FIX30 - Redesign: toko seperti Uniqlo, human-crafted

WARNA (sesuai permintaan):
- Background: #FBF9F5 Ivory hangat
- Teks Utama: #2C2A29 Charcoal lembut
- Primary/Brand: #A35C3A Terakota / Bata hangat
- Aksen: #D4A373 Pasir / Sand

YANG DIUBAH:
- Layout toko: header sticky tipis, hero 2 kolom, grid 4 kolom (2 di HP), kartu produk putih border tipis, tanpa glassmorphism / blur / gradient ungu / badge berlebihan.
- Tipografi: Inter/Helvetica, judul besar tapi rapat, huruf kecil untuk meta (kategori, grade, ukuran). Tidak ada emoji, tidak ada kata-kata AI seperti "dikurasi", "no tipu-tipu", "rebutan", "est", "selamat datang".
- Copy ditulis seperti manusia: "Pakaian bekas yang masih layak dipakai." "Diperiksa satu per satu." "Kondisi ditulis apa adanya." "Kalau habis, tidak restock."
- Filter tetap: Kategori + Lengan, langsung jalan saat dipilih. Banner hasil sederhana: "Menampilkan X dari Y produk".
- Keranjang / checkout: fungsi sama, hanya tampilan dibersihkan. Total, ongkir, kota, kurir tetap.
- Admin: tampilan sama dengan toko (Ivory, Charcoal, Terakota), tabel bersih, form sama. Semua name field tidak diubah, jadi tidak merusak Supabase / Biteship.
- Backend: tidak diubah kecuali copy error yang lebih netral. Supabase, /tmp fallback, Biteship, foto 10, validasi tetap sama seperti Fix29.

CARA UPDATE: upload SEMUA isi zip, git add . ; commit ; push ; Vercel Redeploy ; Ctrl+Shift+R
PENTING: Env di Vercel JANGAN diubah. SUPABASE_URL / SUPABASE_KEY / SUPABASE_TABLE / BITESHIP_API_KEY tetap sama seperti yang sudah jalan di Fix29.
CARA TES: Buka toko - cek hero, grid 4 kolom, filter Lengan Pendek, tambah ke keranjang, checkout sampai WhatsApp. Admin - tambah produk 1 foto, edit, hapus.
