#!/usr/bin/with-contenv bashio
set -e

# Gunicorn auf den Ingress-Port
exec gunicorn -b 0.0.0.0:8099 app:app --workers 4 --threads 2 --timeout 90
