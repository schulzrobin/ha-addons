from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
import sqlite3
from datetime import datetime

class IngressPathMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        prefix = environ.get("HTTP_X_INGRESS_PATH")
        if prefix:
            environ["SCRIPT_NAME"] = prefix
        return self.app(environ, start_response)

DB_PATH = os.getenv("SQLITE_PATH", "/data/einkaufsliste.db")
ALLOWED_INGRESS_IP = os.getenv("INGRESS_ALLOWED_IP", "172.30.32.2")
DISABLE_IP_FILTER = os.getenv("DISABLE_INGRESS_IP_FILTER", "0") == "1"

app = Flask(__name__, static_folder="static", template_folder="templates")
app.wsgi_app = IngressPathMiddleware(app.wsgi_app)  # type: ignore
app.secret_key = os.getenv("FLASK_SECRET", "change-me")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS einkaufsliste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menge INTEGER NOT NULL,
                einheit TEXT NOT NULL,
                produkt TEXT NOT NULL,
                datumzeit TEXT NOT NULL
            )"""
        )
        conn.commit()

@app.before_request
def enforce_ingress_ip():
    if DISABLE_IP_FILTER:
        return
    remote = request.remote_addr or ""
    if remote != ALLOWED_INGRESS_IP:
        abort(403)

@app.get("/")
def index():
    items = []
    try:
        with get_conn() as conn:
            cur = conn.execute("SELECT id, menge, einheit, produkt FROM einkaufsliste ORDER BY id DESC")
            items = cur.fetchall()
    except Exception as e:
        flash(f"Datenbankfehler: {e}", "error")
    return render_template("index.html", items=items)

@app.post("/add")
def add():
    menge = request.form.get("menge", "").strip()
    einheit = request.form.get("einheit", "").strip()
    produkt = request.form.get("produkt", "").strip()
    if not menge or not einheit or not produkt:
        flash("Felder dürfen nicht leer sein!", "error")
        return redirect(url_for("index"))
    try:
        menge_int = int(menge)
    except ValueError:
        flash("Menge muss eine Zahl sein.", "error")
        return redirect(url_for("index"))

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO einkaufsliste (menge, einheit, produkt, datumzeit) VALUES (?, ?, ?, ?)",
                (menge_int, einheit, produkt, datetime.now().isoformat(timespec="seconds"))
            )
            conn.commit()
            flash("Produkt hinzugefügt.", "success")
    except Exception as e:
        flash(f"Speichern fehlgeschlagen: {e}", "error")
    return redirect(url_for("index"))

@app.post("/delete/<int:item_id>")
def delete(item_id: int):
    try:
        with get_conn() as conn:
            conn.execute("DELETE FROM einkaufsliste WHERE id = ?", (item_id,))
            conn.commit()
            flash("Eintrag gelöscht.", "success")
    except Exception as e:
        flash(f"Löschen fehlgeschlagen: {e}", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", "8099"))
    app.run(host="0.0.0.0", port=port, debug=False)
