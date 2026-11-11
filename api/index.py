
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
    {"id":1, "nama":"Beanie Hat Thriftoria", "kategori":"Aksesoris", "lengan":"Tanpa Lengan", "harga":25000, "stok":36, "deskripsi":"Beanie premium Thriftoria"},
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
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f: return json.load(f)
        except: pass
    return deepcopy(DATA_AWAL)

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f: json.dump(data, f)
    except: pass

def next_id(items):
    return max([x["id"] for x in items], default=0) + 1

# ===== TOKO =====
@app.route("/")
def index():
    data = load_data()
    kategori = request.args.get("kategori","")
    lengan = request.args.get("lengan","")
    products = data["products"]
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

# ===== ADMIN =====
@app.route("/login", methods=["GET","POST"])
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
        if "admin" not in session: return redirect(url_for("login"))
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
    data["products"].append({"id":next_id(data["products"]), "nama":request.form["nama"], "kategori":request.form["kategori"], "lengan":request.form["lengan"], "harga":int(request.form["harga"]), "stok":int(request.form["stok"]), "deskripsi":request.form.get("deskripsi","")})
    save_data(data); return redirect(url_for("admin_dashboard"))

@app.route("/admin/edit/<int:pid>", methods=["POST"])
@login_required
def edit(pid):
    data=load_data()
    for p in data["products"]:
        if p["id"]==pid:
            p["nama"]=request.form["nama"]; p["kategori"]=request.form["kategori"]; p["lengan"]=request.form["lengan"]; p["harga"]=int(request.form["harga"]); p["stok"]=int(request.form["stok"]); p["deskripsi"]=request.form.get("deskripsi","")
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


# ===== FIX VERCEL ROUTING =====
# Vercel ngirim PATH_INFO = /api/index.py, Flask nyari route "/" -> 404
# Middleware ini ubah /api/index.py jadi / biar Flask ketemu route-nya
class VercelFixMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        # /api/index.py -> /
        # /api/index.py/admin -> /admin
        # /api/index.py/api/data-analyst -> /api/data-analyst
        if path.startswith("/api/index.py"):
            new_path = path[len("/api/index.py"):] or "/"
            environ["PATH_INFO"] = new_path
            environ["SCRIPT_NAME"] = "/api/index.py"
        elif path.startswith("/api/") and path not in ["/api/data-analyst"]:
            # Jangan ubah /api/data-analyst, itu route Flask asli
            pass
        return self.app(environ, start_response)

app.wsgi_app = VercelFixMiddleware(app.wsgi_app)

# Route cadangan kalau Vercel tetap manggil /api/index.py langsung
@app.route("/api/index.py")
@app.route("/api/index.py/")
def _vercel_index_alias():
    return index()

# Vercel butuh variable 'app' di atas, jangan dihapus
