ARG BUILD_FROM=ghcr.io/home-assistant/amd64-python3:latest
FROM $BUILD_FROM

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# alles kopieren
COPY . .
# run ausführbar machen
RUN chmod +x run.sh

CMD ["./run.sh"]
