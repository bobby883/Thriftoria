
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
    {"id":1, "tanggal":"2026-11-11 10:00", "nama_pembeli":"Budi", "produk_nama":"Kaos Oversize Pendek - Hitam", "qty":2, "total":70000, "status":"Lunas", "tipe":"penjualan"},
    {"id":2, "tanggal":"2026-11-10 14:30", "nama_pembeli":"Supplier Jakarta", "produk_nama":"Hoodie Thriftoria Basic - Black", "qty":20, "total":1200000, "status":"Lunas", "tipe":"pembelian"},
  ]
}

# Di Vercel serverless, simpan di file /tmp agar tetap ada selama instance hidup
DATA_FILE = "/tmp/thriftoria_data.json"  # Vercel serverless, data reset kalau redeploy

def load_data():
    # pastikan produk lama tetap punya field gambar
    _d = None
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f: return json.load(f)
        except: pass
    return deepcopy(DATA_AWAL)

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f: json.dump(data, f)
    except: pass


def simpan_gambar(file_storage):
    # HP upload -> base64, biar jalan di Vercel serverless (tanpa simpan file)
    if not file_storage or not file_storage.filename:
        return ""
    try:
        data = file_storage.read()
        if len(data) > 2*1024*1024:  # max 2MB, biar tidak berat
            data = data[:2*1024*1024]
        import base64 as _b64
        mime = file_storage.mimetype or "image/jpeg"
        return f"data:{mime};base64,{_b64.b64encode(data).decode()}"
    except:
        return ""

def next_id(items):
    return max([x["id"] for x in items], default=0) + 1

# ===== TOKO =====
@app.route("/")
def index():
    data = load_data()
    kategori = request.args.get("kategori","")
    lengan = request.args.get("lengan","")
    products = [p for p in data["products"] if p["stok"] > 0]  # STOK 0 = HILANG DARI WEB
    if kategori: products = [p for p in products if p["kategori"]==kategori]
    if lengan: products = [p for p in products if p["lengan"]==lengan]
    kategoris = sorted(set([p["kategori"] for p in data["products"]]))
    lengans = sorted(set([p["lengan"] for p in data["products"]]))
    return render_template("index.html", products=products, kategoris=kategoris, lengans=lengans, kategori_filter=kategori, lengan_filter=lengan)

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
    return render_template("nota.html", produk=request.args.get("produk"), qty=request.args.get("qty"), total=request.args.get("total"))


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
    # Body: {"nama":"Budi","items":[{"id":1,"qty":1}]}
    try:
        body = request.get_json(force=True)
    except:
        return jsonify({"error":"JSON tidak valid"}), 400
    nama = body.get("nama","Pelanggan")
    items = body.get("items",[])
    if not items:
        return jsonify({"error":"Keranjang kosong"}), 400
    data = load_data()
    total = 0
    # Validasi stok dulu, kalau ada yang kurang -> gagal semua, tidak ada yang terpotong
    for it in items:
        p = next((x for x in data["products"] if x["id"]==int(it["id"])), None)
        if not p:
            return jsonify({"error":f"Produk id {it['id']} tidak ditemukan"}), 400
        if p["stok"] < int(it["qty"]):
            return jsonify({"error":f"Stok {p['nama']} tidak cukup. Sisa {p['stok']}"}), 400
    # KUNCI STOK: langsung kurangi stok, barang terkunci untuk transaksi ini
    oid = buat_order_id()
    rincian = []
    for it in items:
        p = next((x for x in data["products"] if x["id"]==int(it["id"])))
        qty = int(it["qty"])
        sub = p["harga"]*qty
        total += sub
        p["stok"] -= qty  # stok berkurang, kalau jadi 0 -> hilang dari web
        rincian.append({"nama":p["nama"],"qty":qty,"harga":p["harga"],"subtotal":sub})
        data["orders"].append({"id":next_id(data["orders"]), "order_id":oid, "tanggal":datetime.now().strftime("%Y-%m-%d %H:%M"), "nama_pembeli":nama, "produk_nama":p["nama"], "qty":qty, "total":sub, "status":"Menunggu Pembayaran", "tipe":"penjualan"})
    save_data(data)
    # QRIS text: format untuk QRIS, 1 order_id = 1 pembayaran, nominal terkunci
    qris_text = f"THRIFTORIA|{oid}|TOTAL:{total}|NAMA:{nama}"
    return jsonify({"order_id":oid, "total":total, "rincian":rincian, "qris_text":qris_text, "status":"Menunggu Pembayaran", "locked":True, "message":"Stok terkunci 10 menit. Bayar sesuai nominal, jangan bayar 2x untuk order yang sama."})

@app.route("/api/order/<oid>")
def api_order(oid):
    data = load_data()
    orders = [o for o in data["orders"] if o.get("order_id")==oid]
    if not orders:
        return jsonify({"error":"Order tidak ditemukan"}), 404
    total = sum(o["total"] for o in orders)
    return jsonify({"order_id":oid, "total":total, "orders":orders, "status":orders[0]["status"]})

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
    total = sum(o["total"] for o in data["orders"] if o["tipe"]=="penjualan")
    return render_template("admin.html", products=data["products"], orders=data["orders"], total_penjualan=total, total_transaksi=len(data["orders"]))

@app.route("/admin/tambah", methods=["POST"])
@login_required
def tambah():
    data=load_data()
    gambar = simpan_gambar(request.files.get("gambar"))
    # kalau tidak upload file, tapi kirim base64 dari HP (form gambar_base64)
    if not gambar:
        gambar = request.form.get("gambar_base64","")[:500000]
    data["products"].append({"id":next_id(data["products"]), "nama":request.form["nama"], "kategori":request.form["kategori"], "lengan":request.form["lengan"], "harga":int(request.form["harga"]), "stok":int(request.form["stok"]), "deskripsi":request.form.get("deskripsi",""), "gambar":gambar, "grade":request.form.get("grade","A"), "gender":request.form.get("gender","Unisex"), "ukuran":request.form.get("ukuran","All Size")})
    save_data(data); return redirect(url_for("admin_dashboard"))

@app.route("/admin/edit/<int:pid>", methods=["POST"])
@login_required
def edit(pid):
    data=load_data()
    for p in data["products"]:
        if p["id"]==pid:
            p["nama"]=request.form["nama"]; p["kategori"]=request.form["kategori"]; p["lengan"]=request.form["lengan"]; p["harga"]=int(request.form["harga"]); p["stok"]=int(request.form["stok"]); p["grade"]=request.form.get("grade", p.get("grade","A")); p["gender"]=request.form.get("gender", p.get("gender","Unisex")); p["ukuran"]=request.form.get("ukuran", p.get("ukuran","All Size"))
            _g = simpan_gambar(request.files.get("gambar"))
            if _g: p["gambar"]=_g
            elif request.form.get("gambar_base64"): p["gambar"]=request.form.get("gambar_base64","")[:500000]; p["deskripsi"]=request.form.get("deskripsi","")
    save_data(data); return redirect(url_for("admin_dashboard"))

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
