ARG BUILD_FROM
FROM $BUILD_FROM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add -y python3 python3-pip

COPY run.sh /
COPY gen1_update.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]