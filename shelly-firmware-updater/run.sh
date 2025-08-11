#!/usr/bin/with-contenv bashio
set -e
# Gunicorn läuft in der venv (PATH wurde im Dockerfile gesetzt)
exec gunicorn -b 0.0.0.0:8099 app:app --workers 4 --threads 2 --timeout 90