# Der Supervisor setzt automatisch das passende {arch}-Image.
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Python & pip im Alpine-Baseimage installieren
RUN apk add --no-cache python3 py3-pip \
 && python3 -m ensurepip \
 && pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Abhängigkeiten
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# App
COPY app.py .
COPY run.sh /run.sh
RUN chmod +x /run.sh

# interner Web-Port (Ingress bindet darauf)
EXPOSE 8099

CMD [ "/run.sh" ]