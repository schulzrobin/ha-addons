#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json
TARGET="$(bashio::config 'target')"

ADDON_VERSION=$(jq -r '.version' /data/options.json 2>/dev/null || echo "unknown")

echo "Hello world!"
echo "server starten..."
echo "Version: $ADDON_VERSION"
python3 -m http.server 8099
