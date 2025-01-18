ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 python3-pip

COPY run.sh /
COPY gen1_update.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]