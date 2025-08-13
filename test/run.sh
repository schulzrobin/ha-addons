#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
TARGET="$(bashio::config 'target')"

echo "Hello world!"
echo "Version: 1.0.3"
echo "server starten..."
echo TARGET
python3 -m http.server 8099
