#!/usr/bin/with-contenv bashio
set -e

# Persistenter Datenpfad des Add-ons: /data
# Wir leeren (oder erstellen) das Log bei jedem Start:
mkdir -p /data/logs
: > /data/logs/app.log
