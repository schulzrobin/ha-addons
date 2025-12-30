from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['APPLICATION_ROOT'] = '/'

os.makedirs("/data", exist_ok=True)
DB_PATH = "/data/einkaufsliste.db"


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


@app.route('/', methods=["GET", "POST"])
def index():
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        try:
            menge = request.form['menge']
            einheit = request.form['einheit']
            artikel = request.form['artikel']
            c.execute('INSERT INTO einkaufsliste (menge, einheit, artikel) VALUES (?, ?, ?)',
              (menge, einheit, artikel))
            conn.commit()
        except Exception as e:
            print("DB Error:", e)
            return "Database error", 500

    c.execute("SELECT * FROM einkaufsliste")
    items = c.fetchall()
    conn.close()

    return render_template("index.html", items=items)


@app.route('/update/<int:item_id>', methods=["POST"])
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


@app.route('/delete/<int:item_id>')
def delete(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM einkaufsliste WHERE id=?', (item_id,))
        conn.commit()
    except Exception as e:
        print("DB Error:", e)
        return "Database error", 500
    finally:
        conn.close()
    return redirect('/')


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, threaded=False)
