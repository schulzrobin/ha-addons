FROM ghcr.io/home-assistant/amd64-base:latest

WORKDIR /app

# Python & pip
RUN apk add --no-cache python3 py3-pip jq

# Abhängigkeiten installieren --user wegen extern verwalteter Umgebung
COPY requirements.txt .
RUN pip3 install --no-cache-dir --user -r requirements.txt

# App-Dateien kopieren
COPY . .

# Entrypoint
CMD ["/root/.local/bin/python3", "-u", "app.py"]