# Einkaufsliste – Home Assistant Add-on (Ingress)

Dieses Add-on verpackt die Python/Flask-Einkaufsliste mit lokalem SQLite in ein Home Assistant Add-on mit **Ingress**.

## Installation (lokaler Add-on-Ordner)
1. Entpacke diesen Ordner in den `addons`-Share deiner HA-Installation (z. B. via Samba) unter `addons/einkaufsliste`.
2. Home Assistant → **Einstellungen → Add-ons → Add-on-Store** → Menü (⋮) → **Auf Updates prüfen**.
3. Unter **Lokale Add-ons** *Einkaufsliste* → **Installieren** → **Starten** → **Öffne Web-UI**.

## Hinweise
- Ingress läuft intern auf Port `8099` (Siehe `config.yaml`). Kein Portmapping nötig.
- Die Datenbank liegt in `/data/einkaufsliste.db` und bleibt bei Updates erhalten.
- Standardmäßig sind nur Zugriffe vom Ingress-Gateway (`172.30.32.2`) erlaubt. Für lokales Debugging: `DISABLE_INGRESS_IP_FILTER=1`.

## Optional: Umgebungsvariablen
- `SQLITE_PATH` (default `/data/einkaufsliste.db`)
- `FLASK_SECRET` (default `change-me`)
- `DISABLE_INGRESS_IP_FILTER` (`0`/`1`)
