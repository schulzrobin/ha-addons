from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['APPLICATION_ROOT'] = '/'

os.makedirs("/data", exist_ok=True)
DATABASE = "/data/einkaufsliste.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS einkaufsliste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menge TEXT NOT NULL,
            einheit TEXT NOT NULL,
            artikel TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        c.execute(
            "INSERT INTO einkaufsliste (menge, einheit, artikel) VALUES (?, ?, ?)",
            (request.form["menge"], request.form["einheit"], request.form["artikel"])
        )
        conn.commit()
        return redirect(url_for("index"))

    c.execute("SELECT * FROM einkaufsliste")
    items = c.fetchall()
    conn.close()

    return render_template("index.html", items=items)


@app.route("/update/<int:item_id>", methods=["POST"])
def update(item_id):
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE einkaufsliste SET menge=?, einheit=?, artikel=? WHERE id=?",
        (data["menge"], data["einheit"], data["artikel"], item_id)
    )
    conn.commit()
    conn.close()
    return jsonify(success=True)


@app.route("/delete/<int:item_id>")
def delete(item_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM einkaufsliste WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
