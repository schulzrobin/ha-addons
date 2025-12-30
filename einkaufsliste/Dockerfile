# Nutze offizielles Python-3.11 slim Image
FROM python:3.11-slim

WORKDIR /app

RUN apk add --no-cache python3 py3-pip jq

# venv erstellen (in slim Images ist venv meist schon vorhanden)
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Dependencies installieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# App kopieren
COPY . /.
COPY run.sh /run.sh
RUN chmod a+x /run.sh
