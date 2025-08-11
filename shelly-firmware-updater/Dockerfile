ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}
SHELL ["/bin/ash","-o","pipefail","-c"]

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Python + venv (PEP-668-konform)
RUN apk add --no-cache python3 py3-pip py3-virtualenv \
 && python3 -m venv "$VIRTUAL_ENV"

# Deps in venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY app.py .

# s6-Dateien
COPY rootfs/ /

# Rechte sicherstellen
RUN [ -f /etc/services.d/shelly/run ] && chmod +x /etc/services.d/shelly/run || true \
 && [ -f /etc/cont-init.d/10-clean-logs ] && chmod +x /etc/cont-init.d/10-clean-logs || true

# Ingress-Port intern
EXPOSE 8099
# WICHTIG: KEIN ENTRYPOINT/CMD setzen – Base-Image startet /init (s6) automatisch
