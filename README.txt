THRIFTORIA FIX5 - Hapus info login + hapus API JSON

YANG DIHAPUS:
1. Di halaman login (/admin-login): tulisan "Username: admin | Password: thriftoria123" DIHAPUS TOTAL.
   Sekarang halaman login cuma ada kolom Username + Password kosong, tanpa bocoran.
   Password tetap sama di kode (api/index.py), cuma tidak ditampilkan lagi.

2. Di halaman admin (/admin): tombol "API JSON" DIHAPUS. Itu memang tidak guna buat kamu, itu cuma untuk developer.
   Sekarang di admin tinggal: Lihat Toko | Data Analyst | Logout

3. Kartu Data Analyst di admin disederhanakan: tidak ada lagi penjelasan panjang "Klik tombol di atas..."
   Cuma: Data Analyst - Lihat laporan penjualan.

CARA UPDATE:
git add .
git commit -m "hapus info login dan api json"
git push
Vercel -> Redeploy tanpa cache

LOGIN ADMIN (hafalin, jangan ditulis di web):
URL: https://thriftoria-lilac.vercel.app/admin-login
Username: admin
Password: (yang lama, jangan ditulis di mana-mana)
