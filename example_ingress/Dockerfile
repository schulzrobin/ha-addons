ARG BUILD_FROM=ghcr.io/home-assistant/base:python3.11
FROM $BUILD_FROM

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]