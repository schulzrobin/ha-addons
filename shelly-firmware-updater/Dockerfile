ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

WORKDIR /usr/src/app

# Systempakete
RUN apk add --no-cache python3 py3-pip jq

# Python venv vorbereiten (PEP 668 umgehen)
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV} \
 && ${VIRTUAL_ENV}/bin/pip install --no-cache-dir --upgrade pip

# Requirements installieren (in die venv!)
COPY requirements.txt .
RUN ${VIRTUAL_ENV}/bin/pip install --no-cache-dir -r requirements.txt

# App-Code
COPY app ./app

# s6 service
COPY rootfs/ /

# run/finish ausführbar machen (wichtig)
RUN chmod +x /etc/services.d/gunicorn/run

# Environment
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    APP_PORT=8099

HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD wget -qO- http://127.0.0.1:${APP_PORT}/ || exit 1