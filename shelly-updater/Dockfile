FROM python:3.10-slim

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten (optional: für requests)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies kopieren & installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# App-Dateien kopieren
COPY app.py .
COPY run.sh .

# Port expose
EXPOSE 5000

CMD ["./run.sh"]
