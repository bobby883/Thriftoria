
# THRIFTORIA - Vercel Version
# Deploy: vercel deploy atau push ke GitHub -> Import di Vercel
# Database pakai dict in-memory + JSON biar jalan di Vercel (serverless)
# Untuk produksi, ganti dengan Vercel KV / Postgres, tapi untuk sekarang ini sudah jalan full.

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json, os
from datetime import datetime
from copy import deepcopy

import os as _os
_BASE = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
app = Flask(__name__, template_folder=_os.path.join(_BASE, 'templates'), static_folder=_os.path.join(_BASE, 'static'))
app.secret_key = "thriftoria-secret-vercel"

# ===== DATA AWAL - THRIFTORIA =====
DATA_AWAL = {
  "products": [
    {"id":1, "nama":"Beanie Hat Thriftoria", "kategori":"Aksesoris", "lengan":"Tanpa Lengan", "harga":25000, "stok":36, "deskripsi":"Beanie premium Thriftoria", "gambar":""},
    {"id":2, "nama":"Kaos Oversize Pendek - Hitam", "kategori":"Kaos", "lengan":"Lengan Pendek", "harga":35000, "stok":8, "deskripsi":"Kaos oversize hitam"},
    {"id":3, "nama":"Kaos Oversize Pendek - Olive", "kategori":"Kaos", "lengan":"Lengan Pendek", "harga":35000, "stok":48, "deskripsi":"Kaos oversize olive"},
    {"id":4, "nama":"Kaos Oversize Panjang - Cream", "kategori":"Kaos", "lengan":"Lengan Panjang", "harga":40000, "stok":27, "deskripsi":"Kaos oversize cream"},
    {"id":5, "nama":"Hoodie Thriftoria Basic - Black", "kategori":"Hoodie", "lengan":"Lengan Panjang", "harga":85000, "stok":18, "deskripsi":"Hoodie basic Thriftoria"},
    {"id":6, "nama":"Cargo Pants - Khaki", "kategori":"Celana", "lengan":"Lengan Panjang", "harga":95000, "stok":13, "deskripsi":"Cargo khaki"},
  ],
  "orders": [
  ]
}

# Di Vercel serverless, simpan di file /tmp agar tetap ada selama instance hidup
DATA_FILE = "/tmp/thriftoria_data.json"  # Vercel serverless, data reset kalau redeploy

def _supabase_cfg():
    url=(os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key=os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY") or ""
    table=os.environ.get("SUPABASE_TABLE") or "thriftoria_data"
    return url, key, table
def _supabase_get():
    # Ambil data dari Supabase (database permanen). Return None kalau belum disetting / gagal.
    url,key,table=_supabase_cfg()
    if not url or not key: return None
    try:
        import urllib.request, json as _j
        req=urllib.request.Request(f"{url}/rest/v1/{table}?id=eq.1&select=data", headers={"apikey":key,"Authorization":f"Bearer {key}","Accept":"application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            rows=_j.loads(r.read().decode())
        if rows and rows[0].get("data"): return rows[0]["data"]
        return None
    except Exception as e:
        print("Supabase GET gagal:", e); return None
def _supabase_save(data):
    url,key,table=_supabase_cfg()
    if not url or not key: return False
    try:
        import urllib.request, json as _j
        body=_j.dumps({"id":1,"data":data}).encode()
        # Upsert: kalau row id=1 belum ada -> insert, kalau sudah ada -> update. Pakai merge-duplicates.
        req=urllib.request.Request(f"{url}/rest/v1/{table}?on_conflict=id", data=body, method="POST", headers={"apikey":key,"Authorization":f"Bearer {key}","Content-Type":"application/json","Prefer":"resolution=merge-duplicates,return=minimal"})
        with urllib.request.urlopen(req, timeout=8) as r: r.read()
        return True
    except Exception as e:
        print("Supabase SAVE gagal:", e); return False
def load_data():
    # Data disimpan di Supabase dan /tmp. /tmp Vercel itu sementara: tiap pindah instance / cold start / Redeploy, isinya hilang, produk baru balik ke DATA_AWAL.
    # Urutan: 1) Supabase (permanen, kalau sudah disetting) 2) /tmp (cache cepat) 3) DATA_AWAL
    d=_supabase_get()
    if isinstance(d, dict) and "products" in d: return d
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f: return json.load(f)
        except: pass
    return deepcopy(DATA_AWAL)

def save_data(data):
    ok=False
    try: ok=_supabase_save(data)
    except Exception as e: print("save supabase error", e)
    try:
        with open(DATA_FILE, "w") as f: json.dump(data, f)
    except Exception as e: print("save tmp error", e)
    return ok


def simpan_gambar(file_storage):
    # HP upload -> base64, biar jalan di Vercel serverless (tanpa simpan file)
    if not file_storage or not file_storage.filename:
        return ""
    try:
        data = file_storage.read()
        if len(data) > 2*1024*1024:
            raise ValueError("Foto lebih dari 2MB. Pilih foto lain.")
        import base64 as _b64
        mime = file_storage.mimetype or "image/jpeg"
        return f"data:{mime};base64,{_b64.b64encode(data).decode()}"
    except:
        return ""


def gambar_list_for(p):
    # Produk lama: cuma punya "gambar" (1 string). Produk baru: "gambar_list" (list, maks 10). Selalu kembalikan list.
    lst = p.get("gambar_list") or []
    if lst: return [x for x in lst if x][:10]
    g = p.get("gambar","")
    return [g] if g else []
def kumpulkan_gambar(req):
    # Catatan:
    # Form lama kirim DUA-DUANYA: file mentah (sampai 2MB/foto) + base64 hasil kompres.
    # Server lalu ngumpulin dua-duanya (dedup gagal karena isinya beda: mentah vs kompres) -> payload bisa 10-20MB -> Vercel limit 4.5MB -> 500/413.
    # Sekarang: kalau base64_list ada (sudah dikompres di browser ke max 700px), pakai ITU SAJA, file mentah diabaikan. Kalau tidak ada base64, baru pakai file.
    out=[]
    raw_list = req.form.get("gambar_base64_list","") or ""
    if raw_list.strip():
        try:
            arr=json.loads(raw_list) if raw_list.strip().startswith("[") else [raw_list]
            for x in arr:
                if isinstance(x,str) and x.startswith("data:image"): out.append(x[:260000])
        except: pass
        if out:
            seen=set(); uniq=[]
            for x in out:
                if x not in seen: seen.add(x); uniq.append(x)
            return uniq[:10]
    for f in list(req.files.getlist("gambar")) + list(req.files.getlist("gambar_list")):
        g=simpan_gambar(f)
        if g: out.append(g[:260000])
    single = req.form.get("gambar_base64","") or ""
    if single.startswith("data:image") and single not in out: out.append(single[:260000])
    seen=set(); uniq=[]
    for x in out:
        if x not in seen: seen.add(x); uniq.append(x)
    return uniq[:10]
def safe_int(v, default=0, label="angka"):
    try:
        v=str(v).strip().replace(".","").replace(",","")
        if v=="" : raise ValueError("kosong")
        return int(float(v))
    except Exception:
        raise ValueError(f"{label} harus diisi angka yang benar, bukan '{v}'")
def error_page(msg):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thriftoria</title><style>body{font-family:Inter,system-ui,sans-serif;background:#FBF9F5;color:#2C2A29;padding:24px}.card{max-width:520px;margin:40px auto;background:#fff;border:1px solid #E8E0D6;padding:28px}h2{font-size:20px;margin:0 0 12px}a{color:#A35C3A}</style></head><body><div class="card"><h2>Barang belum tersimpan</h2><p>{msg}</p><p><a href="/admin">Kembali ke Admin</a></p></div></body></html>""", 400

def next_id(items):
    return max([x["id"] for x in items], default=0) + 1

# ===== LOGO STATIC =====
@app.route("/static/logo.png")
def logo_png():
    from flask import send_file
    import os as _o
    p = _o.path.join(_BASE, "static", "logo.png")
    if _o.path.exists(p):
        return send_file(p, mimetype="image/png")
    return "logo not found", 404

# ===== ONGKIR =====
# Harga ongkir flat per kurir (bisa diganti di admin nanti).
# Ini hitungan sementara biar langsung jalan, tanpa API RajaOngkir.
# Admin bisa ubah angka di sini kalau mau.
ONGKIR_TABLE = {
  "JNE Reguler": 12000,
  "JNE YES": 22000,
  "J&T Express": 11000,
  "SiCepat Reg": 10000,
  "SiCepat BEST": 9000,
  "Pos Indonesia": 9000,
  "GoSend Same Day (Medan)": 15000,
  "Ambil di Toko (Gratis)": 0,
}


# ===== ONGKIR RAJAONGKIR (DATA ASLI DARI EKSPEDISI) =====
# Cara pakai: daftar di https://rajaongkir.com / https://komerce.id
# Ambil API Key Starter (gratis), lalu di Vercel -> Settings -> Environment Variables:
#   RAJAONGKIR_API_KEY = api_key_kamu
# Kalau key belum diisi, web pakai fallback flat (biar tetap jalan), tapi tulis "Estimasi".
# Berat default: 500 gram per 1 item thrift (kaos/cargo). Kalau 2 item = 1000 gram, dst.
import urllib.request, urllib.parse, json as _json, os as _os

RAJAONGKIR_KEY = _os.environ.get("RAJAONGKIR_API_KEY", "")
BITESHIP_KEY = _os.environ.get("BITESHIP_API_KEY", "")
# PRIORITAS ONGKIR: 1) Biteship (lebih baru, tidak ke-flag McAfee) 2) RajaOngkir/Komerce 3) Estimasi flat
# ID kota asal: Thriftoria di Indrapura, Batu Bara, Sumut.
# RajaOngkir Starter pakai city_id. Kalau belum tau, isi 0 -> nanti diisi dari daftar kota di admin.
# Default sementara: Medan (city_id 152) sebagai hub terdekat, biar ongkir kehitung.
ORIGIN_CITY_ID = _os.environ.get("ORIGIN_CITY_ID", "152")

@app.route("/api/kota")
def api_kota():
    # Kembalikan daftar kota untuk dropdown customer. Kalau ada API key, ambil dari RajaOngkir, kalau tidak pakai list utama.
    if RAJAONGKIR_KEY:
        try:
            req = urllib.request.Request("https://api.rajaongkir.com/starter/city", headers={"key": RAJAONGKIR_KEY})
            with urllib.request.urlopen(req, timeout=10) as r:
                j = _json.loads(r.read().decode())
                cities = [{"id": x["city_id"], "label": f"{x['city_name']}, {x['province']}"} for x in j["rajaongkir"]["results"]]
                return jsonify({"source":"rajaongkir", "cities": cities})
        except Exception as e:
            pass
    # Fallback: kota besar yang sering order, biar tetap jalan tanpa API key
    fallback = [
        {"id":"152","label":"Medan, Sumatera Utara"},
        {"id":"23","label":"Batu Bara, Sumatera Utara"},
        {"id":"151","label":"Medan, Sumatera Utara"},
        {"id":"21","label":"Asahan, Sumatera Utara"},
        {"id":"153","label":"Binjai, Sumatera Utara"},
        {"id":"154","label":"Tebing Tinggi, Sumatera Utara"},
        {"id":"155","label":"Pematang Siantar, Sumatera Utara"},
        {"id":"156","label":"Tanjung Balai, Sumatera Utara"},
        {"id":"501","label":"Jakarta Pusat, DKI Jakarta"},
        {"id":"502","label":"Jakarta Utara, DKI Jakarta"},
        {"id":"503","label":"Jakarta Barat, DKI Jakarta"},
        {"id":"504","label":"Jakarta Selatan, DKI Jakarta"},
        {"id":"505","label":"Jakarta Timur, DKI Jakarta"},
        {"id":"78","label":"Bandung, Jawa Barat"},
        {"id":"114","label":"Surabaya, Jawa Timur"},
        {"id":"444","label":"Makassar, Sulawesi Selatan"},
        {"id":"256","label":"Denpasar, Bali"},
        {"id":"17","label":"Banda Aceh, Aceh"},
        {"id":"398","label":"Padang, Sumatera Barat"},
        {"id":"278","label":"Pekanbaru, Riau"},
        {"id":"122","label":"Palembang, Sumatera Selatan"},
        {"id":"158","label":"Yogyakarta, DI Yogyakarta"},
        {"id":"445","label":"Manado, Sulawesi Utara"},
        {"id":"492","label":"Jayapura, Papua"},
    ]
    return jsonify({"source":"fallback", "cities": fallback, "note":"Daftar kota fallback. Pasang BITESHIP_API_KEY (biteship.com) atau RAJAONGKIR_API_KEY (komerce.id) di Vercel untuk ongkir asli."})

@app.route("/api/ongkir", methods=["POST"])
def api_ongkir():
    # Body: {"destination_city_id":"152", "weight_gram":500, "courier":"jne"}
    # Courier: jne, jnt, sicepat, pos, anteraja, tiki, wahana
    try:
        body = request.get_json(force=True)
    except:
        return jsonify({"error":"JSON tidak valid"}), 400
    dest = str(body.get("destination_city_id",""))
    weight = int(body.get("weight_gram", 500))
    courier = str(body.get("courier","jne")).lower()
    if not dest:
        return jsonify({"error":"Pilih kota tujuan dulu", "ongkir":0}), 400
    # 1) Coba Biteship dulu (daftar di biteship.com, tidak ke-flag McAfee)
    if BITESHIP_KEY:
        try:
            import urllib.request as _ur
            payload = _json.dumps({"origin_postal_code":"21172", "destination_postal_code": body.get("destination_postal_code","20111"), "couriers": courier, "items":[{"name":"Thriftoria","description":"Pakaian thrift","value":50000,"length":30,"width":20,"height":5,"weight":weight}]}).encode()
            req2 = urllib.request.Request("https://api.biteship.com/v1/rates/couriers", data=payload, headers={"Authorization": BITESHIP_KEY, "Content-Type":"application/json"})
            with urllib.request.urlopen(req2, timeout=15) as r2:
                j2 = _json.loads(r2.read().decode())
                if j2.get("success") and j2.get("pricing"):
                    p0 = j2["pricing"][0]
                    return jsonify({"source":"biteship", "courier":courier, "weight_gram":weight, "ongkir": p0["price"], "service": p0.get("courier_service_name",""), "etd": p0.get("duration","")})
        except Exception as e:
            pass
    # Kalau belum ada API key -> fallback flat, tapi tandai estimasi
    if not RAJAONGKIR_KEY:
        flat = {"jne":12000, "jnt":11000, "sicepat":10000, "pos":9000, "anteraja":10000, "tiki":13000, "wahana":12000}
        return jsonify({"source":"estimasi", "ongkir": flat.get(courier,11000), "courier":courier, "weight_gram":weight, "note":"Ini masih estimasi flat. Pasang BITESHIP_API_KEY (daftar di biteship.com) atau RAJAONGKIR_API_KEY (daftar di komerce.id) di Vercel untuk ongkir asli."})
    # Ada API key -> tanya ke RajaOngkir
    try:
        data_post = urllib.parse.urlencode({"origin": ORIGIN_CITY_ID, "destination": dest, "weight": weight, "courier": courier}).encode()
        req = urllib.request.Request("https://api.rajaongkir.com/starter/cost", data=data_post, headers={"key": RAJAONGKIR_KEY, "content-type":"application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=15) as r:
            j = _json.loads(r.read().decode())
            costs = j["rajaongkir"]["results"][0]["costs"]
            # Ambil layanan termurah (REG) sebagai default
            layanan = []
            for co in costs:
                c0 = co["cost"][0]
                layanan.append({"service": co["service"], "description": co["description"], "ongkir": c0["value"], "etd": c0["etd"]})
            layanan.sort(key=lambda x: x["ongkir"])
            return jsonify({"source":"rajaongkir", "courier":courier, "weight_gram":weight, "layanan":layanan, "ongkir": layanan[0]["ongkir"] if layanan else 0, "service": layanan[0]["service"] if layanan else ""})
    except Exception as e:
        return jsonify({"source":"error", "error":str(e), "ongkir":0}), 500


# ===== TOKO =====
@app.route("/")
def index():
    data = load_data()
    for _p in data["products"]: _p["gambar_list"]=gambar_list_for(_p)
    kategori = (request.args.get("kategori","") or "").strip()
    lengan = (request.args.get("lengan","") or "").strip()
    # FIX28: filter lama terlihat "tidak jalan" karena 2 hal:
    # 1) Perbandingan persis (==) - kalau data lama ada spasi / beda kapital ("Lengan pendek", " Lengan Pendek ") langsung gagal, produk salah lolos / hilang.
    # 2) Filter baru jalan kalau klik tombol Filter. Pembeli nyangka pilih dropdown langsung ke-filter (lihat screenshot: dropdown sudah Lengan Pendek tapi URL masih polos, belum ke-submit).
    # Sekarang: normalisasi (strip + lower) + frontend onchange langsung submit.
    products = [p for p in data["products"] if p["stok"] > 0]
    if kategori:
        kn=kategori.lower()
        products = [p for p in products if (p.get("kategori","") or "").strip().lower()==kn]
    if lengan:
        ln=lengan.lower()
        products = [p for p in products if (p.get("lengan","") or "").strip().lower()==ln]
    kategoris = sorted(set([(p["kategori"] or "").strip() for p in data["products"] if p.get("kategori")]))
    lengans = sorted(set([(p["lengan"] or "").strip() for p in data["products"] if p.get("lengan")]))
    return render_template("index.html", products=products, kategoris=kategoris, lengans=lengans, kategori_filter=kategori, lengan_filter=lengan, total_tampil=len(products), total_semua=len([p for p in data["products"] if p["stok"]>0]))

@app.route("/beli/<int:pid>", methods=["POST"])
def beli(pid):
    data = load_data()
    qty = int(request.form.get("qty",1))
    nama_pembeli = request.form.get("nama_pembeli","Pelanggan")
    p = next((x for x in data["products"] if x["id"]==pid), None)
    if not p or p["stok"] < qty:
        flash("Stok tidak cukup!"); return redirect(url_for("index"))
    total = p["harga"]*qty
    p["stok"] -= qty
    data["orders"].append({"id":next_id(data["orders"]), "tanggal":datetime.now().strftime("%Y-%m-%d %H:%M"), "nama_pembeli":nama_pembeli, "produk_nama":p["nama"], "qty":qty, "total":total, "status":"Lunas", "tipe":"penjualan"})
    save_data(data)
    return redirect(url_for("nota", produk=p["nama"], qty=qty, total=total))

@app.route("/nota")
def nota():
    # Nota baru: bisa dari order_id (checkout QRIS) atau dari beli lama (produk/qty/total)
    oid = request.args.get("order_id","")
    if oid:
        data = load_data()
        orders = [o for o in data["orders"] if o.get("order_id")==oid]
        if orders:
            total = sum(o["total"] for o in orders)
            return render_template("nota.html", order_id=oid, orders=orders, total=total, status=orders[0].get("status","Lunas"), produk=orders[0].get("produk_nama",""), qty=sum(o.get("qty",0) for o in orders), nama_pembeli=orders[0].get("nama_pembeli",""))
    return render_template("nota.html", produk=request.args.get("produk"), qty=request.args.get("qty"), total=request.args.get("total"), order_id="", orders=[], status="Lunas")


# ===== CART + QRIS - 1 TRANSAKSI = 1 KUNCI PEMBAYARAN =====
import random, string
def buat_order_id():
    return "THR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/checkout")
def checkout_page():
    oid = request.args.get("order_id","")
    return render_template("checkout.html", order_id=oid)

@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    try:
        try:
            body = request.get_json(force=True)
        except:
            return jsonify({"error":"JSON tidak valid"}), 400
        # FIX21: definisikan SEMUA field dulu, sebelum dipakai. Ini bug Fix20: kurir/ongkir dipakai sebelum didefinisikan -> NameError -> Server error 500.
        nama = body.get("nama","Pelanggan") or "Pelanggan"
        no_hp = body.get("no_hp","") or ""
        alamat = body.get("alamat","") or ""
        kota = body.get("kota","") or ""
        kota_id = body.get("kota_id","") or ""
        kurir = body.get("kurir","J&T Express") or "J&T Express"
        try:
            ongkir = int(body.get("ongkir", 0) or 0)
        except:
            ongkir = 0
        items = body.get("items",[])
        if not items:
            return jsonify({"error":"Keranjang kosong"}), 400
        # Ongkir 0 boleh lanjut, admin konfirmasi via WA. Jangan tolak, biar tombol tidak mati.
        data = load_data()
        total = 0
        for it in items:
            p = next((x for x in data["products"] if x["id"]==int(it["id"])), None)
            if not p:
                return jsonify({"error":f"Produk id {it['id']} tidak ditemukan"}), 400
            if p["stok"] < int(it["qty"]):
                return jsonify({"error":f"Stok {p['nama']} tidak cukup. Sisa {p['stok']}"}), 400
        oid = buat_order_id()
        rincian = []
        for idx_it, it in enumerate(items):
            p = next((x for x in data["products"] if x["id"]==int(it["id"])))
            qty = int(it["qty"])
            sub = p["harga"]*qty
            total += sub
            p["stok"] -= qty
            rincian.append({"nama":p["nama"],"qty":qty,"harga":p["harga"],"subtotal":sub})
            data["orders"].append({"id":next_id(data["orders"]), "order_id":oid, "tanggal":datetime.now().strftime("%Y-%m-%d %H:%M"), "nama_pembeli":nama, "no_hp":no_hp, "alamat":alamat, "kota":kota, "kota_id":kota_id, "kurir":kurir, "ongkir": ongkir if idx_it==0 else 0, "produk_nama":p["nama"], "qty":qty, "total":sub, "status":"Menunggu Pembayaran", "tipe":"penjualan"})
        save_data(data)
        total_bayar = total + ongkir
        qris_text = f"THRIFTORIA|{oid}|TOTAL:{total_bayar}|NAMA:{nama}"
        return jsonify({"order_id":oid, "total":total_bayar, "subtotal":total, "ongkir":ongkir, "total_bayar":total_bayar, "kurir":kurir, "rincian":rincian, "qris_text":qris_text, "status":"Menunggu Pembayaran", "locked":True, "message":"Stok terkunci. Bayar sesuai nominal (barang + ongkir)."})
    except Exception as e:
        # Jangan pernah return 500 kosong. Kasih pesan jelas biar frontend bisa tampilkan.
        import traceback; traceback.print_exc()
        return jsonify({"error":f"Server error: {str(e)}"}), 500

@app.route("/api/order/<oid>")
def api_order(oid):
    data = load_data()
    orders = [o for o in data["orders"] if o.get("order_id")==oid]
    if not orders:
        return jsonify({"error":"Order tidak ditemukan"}), 404
    subtotal = sum(o["total"] for o in orders)
    ongkir = orders[0].get("ongkir", 0) or 0
    total_bayar = subtotal + ongkir
    return jsonify({"order_id":oid, "total":total_bayar, "subtotal":subtotal, "ongkir":ongkir, "total_bayar":total_bayar, "kurir":orders[0].get("kurir",""), "nama_pembeli":orders[0].get("nama_pembeli",""), "no_hp":orders[0].get("no_hp",""), "alamat":orders[0].get("alamat",""), "kota":orders[0].get("kota",""), "orders":orders, "status":orders[0]["status"]})

@app.route("/api/confirm-payment/<oid>", methods=["POST"])
def api_confirm(oid):
    data = load_data()
    found=False
    for o in data["orders"]:
        if o.get("order_id")==oid:
            o["status"]="Lunas"
            found=True
    if not found:
        return jsonify({"error":"Order tidak ditemukan"}), 404
    save_data(data)
    return jsonify({"order_id":oid, "status":"Lunas"})

@app.route("/api/storage-status")
def storage_status():
    url,key,table=_supabase_cfg()
    d=_supabase_get()
    return jsonify({"supabase_disetting": bool(url and key), "supabase_url": (url[:30]+"..." if url else ""), "supabase_table": table, "supabase_ada_data": bool(d and d.get("products") is not None), "jumlah_produk_supabase": len(d.get("products",[])) if d else 0, "peringatan": "Kalau supabase_disetting=false, data HANYA di /tmp Vercel -> produk baru HILANG pas refresh / pindah instance / Redeploy. Ikuti README Fix29 untuk setting Supabase (gratis, 5 menit)."})
# ===== ADMIN =====
@app.route("/login", methods=["GET","POST"])
@app.route("/admin-login", methods=["GET","POST"])
@app.route("/thriftoria-admin", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")=="admin" and request.form.get("password")=="thriftoria123":
            session["admin"]=True; return redirect(url_for("admin_dashboard"))
        flash("Username / password salah!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin",None); return redirect(url_for("index"))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrap(*a, **kw):
        if "admin" not in session: return redirect("/admin-login")
        return f(*a, **kw)
    return wrap

@app.route("/admin")
@login_required
def admin_dashboard():
    data = load_data()
    for _p in data["products"]: _p["gambar_list"]=gambar_list_for(_p)
    total = sum(o["total"] for o in data["orders"] if o["tipe"]=="penjualan" and o.get("status")=="Lunas")
    return render_template("admin.html", products=data["products"], orders=data["orders"], total_penjualan=total, total_transaksi=len(data["orders"]))

@app.route("/admin/tambah", methods=["POST"])
@login_required
def tambah():
    try:
        data=load_data()
        nama=(request.form.get("nama","") or "").strip()
        if not nama: raise ValueError("Nama Barang wajib diisi.")
        harga=safe_int(request.form.get("harga",""), label="Harga")
        stok=safe_int(request.form.get("stok",""), label="Stok")
        if harga<=0: raise ValueError("Harga harus lebih dari 0.")
        if stok<0: raise ValueError("Stok tidak boleh minus.")
        gl = kumpulkan_gambar(request)
        gambar = gl[0] if gl else ""
        data["products"].append({"id":next_id(data["products"]), "nama":nama, "kategori":request.form.get("kategori","Kaos"), "lengan":request.form.get("lengan","Lengan Pendek"), "harga":harga, "stok":stok, "deskripsi":request.form.get("deskripsi",""), "gambar":gambar, "gambar_list":gl, "grade":request.form.get("grade","A"), "gender":request.form.get("gender","Unisex"), "ukuran":request.form.get("ukuran","All Size")})
        save_data(data); return redirect(url_for("admin_dashboard"))
    except ValueError as e:
        return error_page(str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        return error_page(f"Foto terlalu besar. Coba dengan foto lebih sedikit atau ukuran lebih kecil. Detail teknis: {str(e)[:200]}")

@app.route("/admin/edit/<int:pid>", methods=["POST"])
@login_required
def edit(pid):
    try:
        data=load_data()
        for p in data["products"]:
            if p["id"]==pid:
                nama=(request.form.get("nama","") or "").strip()
                if not nama: raise ValueError("Nama Barang wajib diisi.")
                p["nama"]=nama; p["kategori"]=request.form.get("kategori",p.get("kategori","Kaos")); p["lengan"]=request.form.get("lengan",p.get("lengan","Lengan Pendek")); p["harga"]=safe_int(request.form.get("harga",p.get("harga",0)), label="Harga"); p["stok"]=safe_int(request.form.get("stok",p.get("stok",0)), label="Stok"); p["grade"]=request.form.get("grade", p.get("grade","A")); p["gender"]=request.form.get("gender", p.get("gender","Unisex")); p["ukuran"]=request.form.get("ukuran", p.get("ukuran","All Size")); p["deskripsi"]=request.form.get("deskripsi", p.get("deskripsi",""))
                existing = gambar_list_for(p)
                hapus = request.form.getlist("hapus_gambar")
                if hapus:
                    try: idxs={int(x) for x in hapus}
                    except: idxs=set()
                    existing=[g for i,g in enumerate(existing) if i not in idxs]
                baru = kumpulkan_gambar(request)
                gabung = baru if request.form.get("ganti_semua") else (existing + baru)[:10]
                if gabung: p["gambar_list"]=gabung; p["gambar"]=gabung[0]
                elif not existing: p["gambar_list"]=[]; p["gambar"]=""
                else: p["gambar_list"]=existing; p["gambar"]=existing[0]
        save_data(data); return redirect(url_for("admin_dashboard"))
    except ValueError as e:
        return error_page(str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        return error_page(f"Foto terlalu besar. Coba dengan foto lebih sedikit atau ukuran lebih kecil. Detail teknis: {str(e)[:200]}")

@app.route("/admin/hapus/<int:pid>")
@login_required
def hapus(pid):
    data=load_data(); data["products"]=[p for p in data["products"] if p["id"]!=pid]; save_data(data); return redirect(url_for("admin_dashboard"))

@app.route("/admin/nota/tambah", methods=["POST"])
@login_required
def tambah_nota():
    data=load_data()
    data["orders"].append({"id":next_id(data["orders"]), "tanggal":datetime.now().strftime("%Y-%m-%d %H:%M"), "nama_pembeli":request.form.get("nama_pembeli",""), "produk_nama":request.form["produk_nama"], "qty":int(request.form["qty"]), "total":int(request.form["total"]), "status":request.form.get("status","Lunas"), "tipe":request.form.get("tipe","penjualan")})
    save_data(data); return redirect(url_for("admin_dashboard"))

@app.route("/admin/nota/hapus/<int:oid>")
@login_required
def hapus_nota(oid):
    data=load_data(); data["orders"]=[o for o in data["orders"] if o["id"]!=oid]; save_data(data); return redirect(url_for("admin_dashboard"))

@app.route("/admin/reset")
@login_required
def reset_data():
    save_data(deepcopy(DATA_AWAL)); return redirect(url_for("admin_dashboard"))

# ===== DATA ANALYST - 1 KLIK DARI ADMIN =====
@app.route("/analyst")
@login_required
def analyst():
    data=load_data()
    return render_template("analyst.html", products=data["products"], orders=data["orders"])

# ===== API UNTUK DATA ANALYST =====
@app.route("/api/data-analyst")
def api_analyst():
    data=load_data()
    return jsonify({"products":data["products"], "orders":data["orders"], "updated_at":datetime.now().isoformat()})


# ===== FIX VERCEL ROUTING v3 =====
# Vercel rewrite: /(.*) -> /api/index.py?__path__=$1
# Jadi Flask baca __path__ untuk tau route asli: admin, analyst, beli, dll
from urllib.parse import parse_qs
class VercelFixMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        qs = environ.get("QUERY_STRING", "")
        params = parse_qs(qs)
        p = params.get("__path__", [None])[0]
        if p is not None:
            # p = "admin" / "analyst" / "" / "beli/1"
            environ["PATH_INFO"] = "/" + p if p else "/"
            # buang __path__ dari query biar Flask tidak bingung
            rest = "&".join([f"{k}={v[0]}" for k,v in params.items() if k != "__path__"])
            environ["QUERY_STRING"] = rest
        else:
            # Fallback kalau dipanggil langsung /api/index.py
            path = environ.get("PATH_INFO", "")
            if path.startswith("/api/index.py"):
                environ["PATH_INFO"] = path[len("/api/index.py"):] or "/"
        return self.app(environ, start_response)

app.wsgi_app = VercelFixMiddleware(app.wsgi_app)

# Route cadangan kalau Vercel tetap manggil /api/index.py langsung

# Vercel butuh variable 'app' di atas, jangan dihapus
