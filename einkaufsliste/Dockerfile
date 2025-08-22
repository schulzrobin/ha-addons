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

# run/finish ausführbar machen (wichtig)
RUN chmod +x /app.py

CMD [ "python3 app.py" ]
