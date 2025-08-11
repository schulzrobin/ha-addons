# Nutze das Python-Base-Image von Home Assistant (multi-arch-fähig)
ARG BUILD_FROM=ghcr.io/home-assistant/{arch}-base-python:3.11
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# App
COPY app.py .
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8099

# S6-Overlay startet /run.sh
CMD [ "/run.sh" ]
