ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
# Für andere Architekturen ersetzt HA automatisch das Basisimage per {arch}
FROM ${BUILD_FROM}

# Arbeitsverzeichnis
WORKDIR /usr/src/app

# System-Pakete (jq für Options-Parsing)
RUN apk add --no-cache python3 py3-pip jq

# Python-Abhängigkeiten
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# App-Code
COPY app ./app

# s6 service
COPY rootfs/ /

# Umgebung
ENV PYTHONUNBUFFERED=1 \
    APP_PORT=8099

# Healthcheck (einfacher Ping auf Root)
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD wget -qO- http://127.0.0.1:${APP_PORT}/ || exit 1