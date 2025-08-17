#!/usr/bin/with-contenv bashio
export PYTHONUNBUFFERED=1
export SQLITE_PATH=${SQLITE_PATH:-/data/einkaufsliste.db}
export FLASK_SECRET=${FLASK_SECRET:-change-me}
exec python3 /opt/einkaufsliste/app.py
