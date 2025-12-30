ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

WORKDIR /app

# Systempakete
RUN apk add --no-cache python3 py3-pip jq

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

RUN chmod +x run.sh

CMD ["./run.sh"]