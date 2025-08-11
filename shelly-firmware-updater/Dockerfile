ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.10

FROM ${BUILD_FROM}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY run.sh .
RUN chmod +x run.sh

EXPOSE 5000

CMD ["./run.sh"]