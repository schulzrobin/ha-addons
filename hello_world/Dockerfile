ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 \
    py3-pip \
    && pip3 install --no-cache-dir -U \
        Flask \
        requests \

COPY run.sh /
COPY gen1_update.py /
RUN chmod a+x /run.sh

CMD [ "python3 gen1_update.py" ]