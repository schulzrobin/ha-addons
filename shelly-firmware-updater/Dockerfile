# Der Supervisor setzt automatisch das passende {arch}-Base-Image
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Python + venv + pip aus Alpine installieren (kein systemweites pip-upgrade!)
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Virtuelle Umgebung anlegen
RUN python3 -m venv "$VIRTUAL_ENV"

# Requirements zuerst kopieren und in venv installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Dateien
COPY app.py .
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Ingress-Port (intern)
EXPOSE 8099

CMD [ "/run.sh" ]