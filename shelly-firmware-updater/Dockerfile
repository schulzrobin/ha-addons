# Supervisor setzt {arch}-Base automatisch
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Python + venv (PEP-668-konform)
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Virtuelle Umgebung
RUN python3 -m venv "$VIRTUAL_ENV"

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY app.py .

# s6-Services (starten unseren Dienst korrekt als PID 1 via /init)
COPY rootfs/ /

# interner Port für Ingress
EXPOSE 8099

# Kein CMD/ENTRYPOINT ändern – Base-Image startet /init (s6)