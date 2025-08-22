# Einkaufsliste (Flask + SQLite) – Variante 1

- **Lokale DB:** SQLite-Datei (standard: `einkaufsliste.db`).
- **Init:** `init_db()` wird beim Start (vor `app.run`) ausgeführt – kein `before_first_request` nötig (kompatibel mit Flask 3.x).

## Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
# http://127.0.0.1:5000/
```

## Tabelle
```sql
CREATE TABLE IF NOT EXISTS einkaufsliste (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menge INTEGER NOT NULL,
    einheit TEXT NOT NULL,
    produkt TEXT NOT NULL,
    datumzeit TEXT NOT NULL
);
```