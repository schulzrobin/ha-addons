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

# Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY app.py .

# s6-Services einspielen
COPY rootfs/ /

# WICHTIG: Service-Runfile ausführbar machen (und keine CRLFs!)
RUN chmod +x /etc/services.d/shelly/run

# Ingress-Port intern
EXPOSE 8099

# WICHTIG: s6 als PID 1
ENTRYPOINT ["/init"]
