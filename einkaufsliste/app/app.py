from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SQLITE_PATH", "einkaufsliste.db")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET", "change-me")

def get_conn():
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
    app.run(host='0.0.0.0', port=8099, debug=True)
