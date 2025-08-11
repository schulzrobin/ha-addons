ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Ingress-Port
EXPOSE 8099

CMD [ "/run.sh" ]