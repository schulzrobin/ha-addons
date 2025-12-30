# Nutze offizielles Python-3.11 slim Image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip jq && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

# venv erstellen (in slim Images ist venv meist schon vorhanden)
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod a+x /run.sh
